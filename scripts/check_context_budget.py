#!/usr/bin/env python3
"""Check Guyue discovery and activated Skill context budgets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.context_budget import analyze_context_budget  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "skills_manifest.json").read_text(encoding="utf-8"))
    report = analyze_context_budget(ROOT, manifest)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        metrics = report["metrics"]
        print(
            "Context budget: "
            f"{metrics['skill_count']} skills, "
            f"discovery {metrics['discovery_chars']}/{metrics['discovery_budget_chars']} chars, "
            f"routing {metrics['routing_metadata_chars']}/{metrics['routing_metadata_budget_chars']} chars, "
            f"collaboration {metrics['collaboration_chars']}/{metrics['collaboration_budget_chars']} chars "
            f"(largest workflow {metrics['largest_workflow_chars']}/{metrics['workflow_budget_chars']}), "
            f"root {metrics['root_skill_chars']}/{metrics['root_skill_budget_chars']} chars "
            f"({metrics['root_skill_bytes']} UTF-8 bytes), "
            f"collisions {len(report['route_collisions'])}"
        )
        for warning in report["warnings"]:
            print(f"WARN: {warning}")
        for error in report["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
