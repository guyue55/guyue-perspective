#!/usr/bin/env python3
import contextlib
import io
import json
import tempfile
from pathlib import Path

from ci_validate_skills import check_public_skill_single_entrypoint_contract


ROOT_SKILL = """
## Long Goal Forge Fast Gate
## Direction Firewall Fast Gate
DIRECTION_UNPROVEN
DIRECTION_APPROVED_FOR_IMPLEMENTATION
decide `DIRECTION_UNPROVEN` immediately after this root entrypoint
after the root read, make no further tool call
never auto-renew the budget
"""


def write_fixture(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text(ROOT_SKILL, encoding="utf-8")
    (root / "docs" / "installation.md").write_text(
        "`SKILL.md` is the single instruction entrypoint",
        encoding="utf-8",
    )
    (root / "release-manifest.json").write_text(
        json.dumps(
            {
                "profiles": {"install": {"required_paths": ["SKILL.md"]}},
                "runtime_required": {"generic": [], "codex": [], "claude": []},
            }
        ),
        encoding="utf-8",
    )


def check(root: Path) -> bool:
    with contextlib.redirect_stderr(io.StringIO()):
        return check_public_skill_single_entrypoint_contract(str(root))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="guyue-single-entrypoint-") as temp_dir:
        root = Path(temp_dir)
        write_fixture(root)
        assert check(root), "clean single-entrypoint fixture must pass"

        forbidden_files = [
            "RTK.md",
            "AGENTS.md",
            "AGENTS.override.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".cursorrules",
            "docs/runtime-adapters.md",
            ".github/copilot-instructions.md",
        ]
        for relative_path in forbidden_files:
            adapter = root / relative_path
            adapter.parent.mkdir(parents=True, exist_ok=True)
            adapter.write_text("host adapter", encoding="utf-8")
            assert not check(root), (
                f"{relative_path} must fail the single-entrypoint gate"
            )
            adapter.unlink()

        manifest_path = root / "release-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["runtime_required"]["codex"] = ["AGENTS.md"]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        assert not check(root), "manifest-declared AGENTS.md must fail the gate"
        write_fixture(root)

        cursor_rule = root / ".cursor" / "rules" / "guyue.md"
        cursor_rule.parent.mkdir(parents=True)
        cursor_rule.write_text("host adapter", encoding="utf-8")
        assert not check(root), "Cursor instruction rules must fail the gate"
        cursor_rule.unlink()

        copilot_rule = root / ".github" / "instructions" / "guyue.instructions.md"
        copilot_rule.parent.mkdir(parents=True, exist_ok=True)
        copilot_rule.write_text("host adapter", encoding="utf-8")
        assert not check(root), "Copilot instruction rules must fail the gate"

    print("Single-entrypoint contract regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
