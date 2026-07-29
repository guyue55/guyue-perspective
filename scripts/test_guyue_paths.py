#!/usr/bin/env python3
"""Focused path-ownership and compatibility tests for Guyue user data."""

from __future__ import annotations

import sys
import tempfile
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from src.memory_store import (  # noqa: E402
    legacy_runtime_memory_dir,
    legacy_runtime_memory_dirs,
    runtime_memory_dir,
)
from src.paths import (  # noqa: E402
    discovery_cache_file,
    ensure_private_directory,
    guyue_home,
    private_memory_dir,
)
from scripts.doctor import dependency_health  # noqa: E402
from scripts.discover_local_skills import write_index_atomic  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="guyue-paths-") as temp_dir:
        root = Path(temp_dir)
        home = root / "home"
        configured = root / "portable"

        default_root = guyue_home(environ={}, user_home=home)
        require(
            default_root == (home / ".guyue").resolve(),
            "default root must be ~/.guyue",
        )
        require(
            private_memory_dir(environ={}, user_home=home)
            == (home / ".guyue" / "knowledge" / "memory").resolve(),
            "private memory must be owned by GUYUE_HOME",
        )
        require(
            discovery_cache_file(environ={}, user_home=home)
            == (
                home / ".guyue" / "cache" / "discovery" / "skills-index.json"
            ).resolve(),
            "skill discovery belongs in rebuildable cache",
        )
        require(
            guyue_home(environ={"GUYUE_HOME": str(configured)}, user_home=home)
            == configured.resolve(),
            "GUYUE_HOME must override the default root",
        )
        private_leaf = configured / "cache" / "discovery"
        ensure_private_directory(private_leaf, private_root=configured)
        require(
            all(
                (path.stat().st_mode & 0o777) == 0o700
                for path in (configured, configured / "cache", private_leaf)
            ),
            "every private root component must use mode 0700",
        )
        external_leaf = root / "external-private" / "nested"
        ensure_private_directory(external_leaf, private_root=configured)
        require(
            all(
                (path.stat().st_mode & 0o777) == 0o700
                for path in (root / "external-private", external_leaf)
            ),
            "new external private path components must use mode 0700",
        )
        fresh_root = root / "missing-parent" / "portable"
        fresh_leaf = fresh_root / "knowledge" / "memory"
        ensure_private_directory(fresh_leaf, private_root=fresh_root)
        require(
            all(
                (path.stat().st_mode & 0o777) == 0o700
                for path in (
                    root / "missing-parent",
                    fresh_root,
                    fresh_root / "knowledge",
                    fresh_leaf,
                )
            ),
            "a new nested GUYUE_HOME must initialize with private permissions",
        )
        memory_override = root / "memory-only"
        require(
            private_memory_dir(
                environ={
                    "GUYUE_HOME": str(configured),
                    "GUYUE_MEMORY_DIR": str(memory_override),
                },
                user_home=home,
            )
            == memory_override.resolve(),
            "GUYUE_MEMORY_DIR must remain a narrow compatibility override",
        )

        install = root / "read-only-install"
        install.mkdir()
        require(
            legacy_runtime_memory_dir(install)
            == (install / ".guyue_memory" / "local").resolve(),
            "legacy lookup must remain install-relative and read-only",
        )
        require(
            legacy_runtime_memory_dirs(install)
            == (
                (install / ".guyue_memory" / "local").resolve(),
                (install / ".guyue_memory").resolve(),
            ),
            "both historical private memory layouts must remain discoverable",
        )

        previous_home = os.environ.get("GUYUE_HOME")
        previous_memory = os.environ.get("GUYUE_MEMORY_DIR")
        try:
            os.environ["GUYUE_HOME"] = str(configured)
            os.environ.pop("GUYUE_MEMORY_DIR", None)
            require(
                runtime_memory_dir(install)
                == (configured / "knowledge" / "memory").resolve(),
                "runtime writes must not follow the installation root",
            )
        finally:
            if previous_home is None:
                os.environ.pop("GUYUE_HOME", None)
            else:
                os.environ["GUYUE_HOME"] = previous_home
            if previous_memory is None:
                os.environ.pop("GUYUE_MEMORY_DIR", None)
            else:
                os.environ["GUYUE_MEMORY_DIR"] = previous_memory

        unverified_skill = root / "skills" / "find-skills"
        unverified_skill.mkdir(parents=True)
        (unverified_skill / "SKILL.md").write_text(
            "---\nname: find-skills\n---\n",
            encoding="utf-8",
        )
        health = dependency_health(
            {
                "name": "find-skills",
                "package_id": "vercel-labs/skills@find-skills",
                "ref": "4ce6d48ac44c8b637db87b2102fea3baca719df1",
            },
            [root / "skills"],
            source_root=root / "sources",
        )
        require(
            health["status"] == "unverified",
            "a loose Skill directory must not be reported as a verified dependency",
        )
        cache_file = configured / "cache" / "discovery" / "skills-index.json"
        write_index_atomic(
            cache_file,
            {"schema_version": 2, "generated_at": None, "skills": []},
        )
        require(
            (cache_file.stat().st_mode & 0o777) == 0o600,
            "private discovery cache files must use mode 0600",
        )

    print("Guyue path ownership tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
