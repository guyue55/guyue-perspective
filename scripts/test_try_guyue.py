#!/usr/bin/env python3
"""Regression tests for the read-only Guyue first-run proof."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from scripts import try_guyue  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    proof = try_guyue.build_proof(
        try_guyue.DEFAULT_INTENT,
        context_markers=[],
        runtime="generic",
        limit=3,
    )
    selected = [item["name"] for item in proof["routing"]["selected"]]
    gated = {item["name"] for item in proof["routing"]["context_gated"]}

    require(proof["status"] == "pass", "the default local proof must pass")
    require(
        proof["package"]["payload_status"] == "complete"
        and proof["package"]["skill_count"] == 27,
        "the proof must expose full-package truth",
    )
    require(
        {"requirement-analysis", "system-design", "coding-discipline"}
        <= set(selected),
        f"the default intent must expose useful routes, got {selected}",
    )
    require(
        "nexusflow-governance-workflow" not in selected
        and "nexusflow-governance-workflow" in gated,
        "project-specific routes must stay behind an explained context gate",
    )
    require(
        not proof["context"]["errors"]
        and not proof["context"]["route_collisions"],
        "the proof must surface a clean local context budget",
    )
    require(
        proof["claims"] == {
            "deterministic_local_proof": True,
            "runtime_activation_verified": False,
            "model_behavior_verified": False,
        },
        "the proof must not inflate deterministic checks into live activation",
    )

    human = try_guyue.render_human(proof)
    require("30 秒验货" in human, "human output must identify the first-run proof")
    require("本地验货通过" in human, "human output must show a visible verdict")
    require(
        "不等于运行时已激活" in human,
        "human output must preserve the evidence boundary",
    )
    require(
        str(ROOT) not in human and str(Path.home()) not in human,
        "human output must not disclose a personal absolute path",
    )
    json.dumps(proof, ensure_ascii=False)

    nexus = try_guyue.build_proof(
        "修复租户治理权限。",
        context_markers=["NexusFlow", "permissionSnapshot"],
        runtime="generic",
        limit=3,
    )
    require(
        nexus["routing"]["selected"][0]["name"]
        == "nexusflow-governance-workflow",
        "explicit project markers must promote the project workflow",
    )

    external = try_guyue.build_proof(
        "找工具",
        context_markers=[],
        runtime="generic",
        limit=3,
    )
    require(
        external["routing"]["lifecycle_state"] == "external_candidate"
        and external["routing"]["external_candidates"][0]["name"] == "find-skills",
        "external-only candidates must remain visible instead of becoming failures",
    )

    try:
        try_guyue.build_proof("   ", context_markers=[], runtime="generic", limit=3)
    except ValueError:
        pass
    else:
        raise AssertionError("blank intent must be rejected")

    print("Guyue first-run proof tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
