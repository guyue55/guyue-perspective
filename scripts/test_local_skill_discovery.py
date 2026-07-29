#!/usr/bin/env python3
"""Regression tests for private local Skill discovery and routed candidates."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from src.local_skill_index import (  # noqa: E402
    SCHEMA_VERSION,
    build_local_skill_index,
    load_local_skill_index,
    router_inputs,
)
from src.skill_router import resolve_routes  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_skill(path: Path, *, name: str, description: str, body: str) -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"{body}\n",
        encoding="utf-8",
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="guyue-local-skills-") as temp_dir:
        root = Path(temp_dir)
        primary = root / "codex"
        secondary = root / "shared"
        write_skill(
            primary / "documentation",
            name="documentation",
            description="Code-backed project documentation.",
            body='## 触发词示例\n“写文档”、“README”、“项目摸底”',
        )
        write_skill(
            secondary / "documentation",
            name="documentation",
            description="Duplicate documentation Skill.",
            body="Secondary copy.",
        )
        write_skill(
            secondary / "testing",
            name="testing",
            description="Testing workflows.",
            body='## When to use\n“test automation”',
        )

        built = build_local_skill_index(
            [("codex", primary), ("agents", secondary)]
        )
        require(
            built["schema_version"] == SCHEMA_VERSION,
            "local discovery index must use the current schema",
        )
        require(len(built["skills"]) == 2, "duplicate Skill names must be compacted")
        documentation = next(
            item for item in built["skills"] if item["name"] == "documentation"
        )
        require(
            documentation["source"] == "codex"
            and documentation["alternate_paths"],
            "host-native Skill must win while duplicate locations remain visible",
        )
        require(
            "写文档" in documentation["search_text"],
            "local discovery must retain compact semantic trigger evidence",
        )

        index_path = root / "skills-index.json"
        index_path.write_text(
            json.dumps(built, ensure_ascii=False),
            encoding="utf-8",
        )
        loaded = load_local_skill_index(index_path)
        capabilities, metadata = router_inputs(loaded)
        require(
            metadata["status"] == "available"
            and metadata["skill_count"] == 2,
            "router metadata must expose local catalog readiness without paths",
        )

        manifest = json.loads(
            (ROOT / "skills_manifest.json").read_text(encoding="utf-8")
        )
        route = resolve_routes(
            manifest,
            "帮我找一个能写文档的技能",
            local_capabilities=capabilities,
            local_catalog=metadata,
            limit=8,
        )
        local_names = [item["name"] for item in route["local_candidates"]]
        require(
            "documentation" in local_names,
            f"local semantic evidence must surface documentation: {local_names}",
        )
        require(
            all(
                "path" not in item and "description" not in item
                for item in route["local_candidates"]
            ),
            "public route receipts must not expose private local content",
        )

        legacy_path = root / "legacy.json"
        legacy_path.write_text(
            json.dumps({"documentation": str(primary / "documentation")}),
            encoding="utf-8",
        )
        legacy = load_local_skill_index(legacy_path)
        require(
            legacy["status"] == "legacy"
            and legacy["skills"][0]["name"] == "documentation",
            "legacy name-to-path caches must remain readable during migration",
        )

    print("Local Skill discovery tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
