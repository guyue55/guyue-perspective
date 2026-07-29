#!/usr/bin/env python3
"""Run a read-only, zero-network first proof of the Guyue package and router."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from scripts.check_full_install import build_receipt  # noqa: E402
from src.context_budget import analyze_context_budget  # noqa: E402
from src.local_skill_index import load_local_skill_index, router_inputs  # noqa: E402
from src.paths import discovery_cache_file  # noqa: E402
from src.skill_router import resolve_routes  # noqa: E402


DEFAULT_INTENT = "给当前项目做一个普通权限管理页面和后端接口。"
RUNTIMES = ("generic", "codex", "claude")


def load_manifest() -> dict:
    return json.loads((ROOT / "skills_manifest.json").read_text(encoding="utf-8"))


def compact_selected(item: dict) -> dict:
    return {
        "name": item["name"],
        "path": item["path"],
        "score": item["score"],
        "matched_triggers": [
            {"trigger": match["trigger"], "match": match["match"]}
            for match in item["matched_triggers"]
        ],
        "matched_context": item["matched_context"],
    }


def build_proof(
    intent: str,
    *,
    context_markers: list[str],
    runtime: str,
    limit: int,
) -> dict:
    """Build one bounded proof without writes, network calls, or model execution."""
    if not intent.strip():
        raise ValueError("intent must contain non-whitespace text")
    if runtime not in RUNTIMES:
        raise ValueError(f"runtime must be one of: {', '.join(RUNTIMES)}")
    if limit <= 0:
        raise ValueError("limit must be positive")

    manifest = load_manifest()
    receipt = build_receipt(ROOT, runtime)
    local_capabilities, local_catalog = router_inputs(
        load_local_skill_index(discovery_cache_file())
    )
    route = resolve_routes(
        manifest,
        intent,
        context_markers=context_markers,
        local_capabilities=local_capabilities,
        local_catalog=local_catalog,
        limit=limit,
    )
    budget = analyze_context_budget(ROOT, manifest)
    selected = [compact_selected(item) for item in route["selected"]]
    context_gated = [
        {
            "name": item["name"],
            "reason": item["reason"],
            "required_context": item["required_context"],
        }
        for item in route["rejected"]
        if item["reason"] == "missing_required_context"
    ]
    negative_rejections = [
        {
            "name": item["name"],
            "negative_matches": item["negative_matches"],
        }
        for item in route["rejected"]
        if item["reason"] == "negative_intent"
    ]
    problems = []
    if receipt["payload_status"] != "complete":
        problems.append("package payload is incomplete")
    if route["lifecycle_state"] == "failed":
        problems.append("no route reached the local evidence threshold")
    problems.extend(budget["errors"])

    return {
        "schema_version": 1,
        "status": "pass" if not problems else "fail",
        "intent": intent.strip(),
        "context_markers": [item.strip() for item in context_markers if item.strip()],
        "package": {
            "name": receipt["package"],
            "version": receipt["version"],
            "runtime": receipt["runtime"],
            "payload_status": receipt["payload_status"],
            "required_file_count": receipt["required_file_count"],
            "skill_count": receipt["skill_count"],
            "required_payload_sha256": receipt["required_payload_sha256"],
            "source_commit": receipt["source_commit"],
            "worktree_dirty": receipt["worktree_dirty"],
            "missing": receipt["missing"],
        },
        "routing": {
            "contract_version": route["routing_contract_version"],
            "lifecycle_state": route["lifecycle_state"],
            "selected": selected,
            "local_catalog": route["local_catalog"],
            "local_candidates": route["local_candidates"],
            "external_candidates": route["external_candidates"],
            "collaboration_candidates": route["collaboration_candidates"],
            "context_gated": context_gated,
            "negative_rejections": negative_rejections,
        },
        "context": {
            "metrics": budget["metrics"],
            "errors": budget["errors"],
            "warnings": budget["warnings"],
            "route_collisions": budget["route_collisions"],
        },
        "claims": {
            "deterministic_local_proof": True,
            "runtime_activation_verified": False,
            "model_behavior_verified": False,
        },
        "problems": problems,
    }


def trigger_summary(route: dict) -> str:
    triggers = [item["trigger"] for item in route["matched_triggers"]]
    context = route["matched_context"]
    evidence = [*triggers, *context]
    return ", ".join(dict.fromkeys(evidence)) or "description similarity"


def render_human(proof: dict) -> str:
    package = proof["package"]
    metrics = proof["context"]["metrics"]
    dirty = "有未发布修改" if package["worktree_dirty"] else "clean"
    lines = [
        "Guyue 30 秒验货",
        (
            f"[{'PASS' if package['payload_status'] == 'complete' else 'FAIL'}] "
            f"包体 {package['payload_status']} | v{package['version']} | "
            f"{package['skill_count']} Skills | 工作树 {dirty}"
        ),
        f"意图: {proof['intent']}",
        "候选路由:",
    ]
    for index, route in enumerate(proof["routing"]["selected"], start=1):
        lines.append(
            f"  {index}. {route['name']} | {route['score']:.3f} | "
            f"证据: {trigger_summary(route)}"
        )

    gated_names = [item["name"] for item in proof["routing"]["context_gated"]]
    if gated_names:
        lines.append("项目边界: " + ", ".join(gated_names) + " 未误触")
    lines.append(
        "上下文: "
        f"发现面 {metrics['discovery_chars']}/{metrics['discovery_budget_chars']} | "
        f"根入口 {metrics['root_skill_chars']}/{metrics['root_skill_budget_chars']} | "
        f"碰撞 {len(proof['context']['route_collisions'])}"
    )

    if proof["status"] == "pass":
        lines.append("[PASS] 本地验货通过")
    else:
        lines.append("[FAIL] " + "; ".join(proof["problems"]))
    lines.append(
        "证据边界: 这是只读确定性检查，不等于运行时已激活或模型行为已通过。"
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intent", nargs="?", default=DEFAULT_INTENT)
    parser.add_argument(
        "--context-marker",
        action="append",
        default=[],
        help="verified context marker; repeat as needed",
    )
    parser.add_argument("--runtime", choices=RUNTIMES, default="generic")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        proof = build_proof(
            args.intent,
            context_markers=args.context_marker,
            runtime=args.runtime,
            limit=args.limit,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(proof, ensure_ascii=False, indent=2))
    else:
        print(render_human(proof), end="")
    return 0 if proof["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
