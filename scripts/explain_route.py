#!/usr/bin/env python3
"""Explain Guyue Skill candidates for one user intent."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from src.skill_router import resolve_routes  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intent", help="user intent to route")
    parser.add_argument(
        "--context-marker",
        action="append",
        default=[],
        help="verified project or environment marker; repeat as needed",
    )
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "skills_manifest.json").read_text(encoding="utf-8"))
    try:
        result = resolve_routes(
            manifest,
            args.intent,
            context_markers=args.context_marker,
            limit=args.limit,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["lifecycle_state"] != "failed" else 2

    collaborations = result.get("collaboration_candidates", [])
    if not result["selected"] and not collaborations:
        print("No route reached the local evidence threshold.")
        return 2
    if result["selected"]:
        print("Guyue route candidates:")
        for index, route in enumerate(result["selected"], start=1):
            trigger_evidence = ", ".join(
                (
                    f"{item['trigger']}<-{item['signal']}"
                    f"({' + '.join(item['evidence'])})"
                    if item["match"] == "composed"
                    else item["trigger"]
                )
                for item in route["matched_triggers"]
            ) or "description similarity"
            context_evidence = ", ".join(route["matched_context"])
            suffix = f"; context={context_evidence}" if context_evidence else ""
            print(
                f"{index}. {route['name']} score={route['score']:.3f}; "
                f"evidence={trigger_evidence}{suffix}"
            )
    else:
        print("No direct Skill route matched; showing a bounded workflow candidate.")
    if collaborations:
        workflow = collaborations[0]
        print(
            f"Collaboration candidate: {workflow['id']} "
            f"score={workflow['score']:.3f}"
        )
        for stage in workflow["stages"]:
            print(
                f"- {stage['id']} [{stage['mode']}]: "
                f"{', '.join(stage['skills'])}"
            )
        print(f"Completion gate: {workflow['completion_gate']}")
        print(f"Boundary: {workflow['boundary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
