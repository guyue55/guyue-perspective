#!/usr/bin/env python3
"""Regression tests for explainable Guyue Skill routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from src.skill_router import resolve_routes  # noqa: E402
from scripts.check_capability_chain import routing_sha256 as expected_routing_sha256  # noqa: E402
from scripts.run_capability_live_canaries import routing_sha256 as live_routing_sha256  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    manifest = json.loads((ROOT / "skills_manifest.json").read_text(encoding="utf-8"))
    require(
        live_routing_sha256() == expected_routing_sha256(manifest),
        "live evidence runner and strict gate must hash the same routing semantics",
    )
    contracts = json.loads(
        (ROOT / "evals" / "behavior-contracts.json").read_text(encoding="utf-8")
    )
    collaboration_contracts = json.loads(
        (ROOT / "evals" / "capability-collaboration.json").read_text(
            encoding="utf-8"
        )
    )["cases"]

    for contract in contracts:
        result = resolve_routes(manifest, contract["prompt"], limit=8)
        selected = [item["name"] for item in result["selected"]]
        expected = set(contract["expected_routes"])
        forbidden = set(contract["forbidden_routes"])
        require(
            expected.issubset(selected),
            f"{contract['id']} missed expected routes "
            f"{sorted(expected - set(selected))}: {selected}",
        )
        require(
            forbidden.isdisjoint(selected),
            f"{contract['id']} selected a forbidden route: {selected}",
        )
        if contract.get("forbid_external_candidates"):
            require(
                not result["external_candidates"]
                and result["external_candidate_blockers"],
                f"{contract['id']} must suppress external candidates with visible blockers: "
                f"{result['external_candidates']}",
            )

    generic = resolve_routes(
        manifest,
        "给当前项目做一个普通权限管理页面和后端接口。",
        limit=8,
    )
    nexus_rejection = next(
        item
        for item in generic["rejected"]
        if item["name"] == "nexusflow-governance-workflow"
    )
    require(
        nexus_rejection["reason"] == "missing_required_context",
        "context-gated skills must explain missing context markers",
    )

    nexus = resolve_routes(
        manifest,
        "修复租户治理权限。",
        context_markers=["NexusFlow", "permissionSnapshot"],
        limit=5,
    )
    require(
        nexus["selected"][0]["name"] == "nexusflow-governance-workflow",
        "explicit context markers must select the matching workflow first",
    )
    require(
        nexus["selected"][0]["matched_context"],
        "selected routes must expose the context evidence used",
    )

    for meta_phrase in ("是否触发", "是否应触发"):
        route_audit = resolve_routes(
            manifest,
            (
                "只读审查这个需求：给当前项目做一个普通权限管理页面和后端接口。"
                f"请判断 NexusFlow/static-demo专属能力{meta_phrase}；不要修改文件。"
            ),
            limit=8,
        )
        audit_selected = [item["name"] for item in route_audit["selected"]]
        require(
            audit_selected[0] == "reality-auditor",
            f"read-only audit must take routing priority: {audit_selected}",
        )
        require(
            {
                "nexusflow-governance-workflow",
                "static-demo-hardening",
            }.isdisjoint(audit_selected),
            f"route-audit meta text must not activate project skills: {audit_selected}",
        )

    negative = resolve_routes(
        manifest,
        "implementation already approved and bounded; write code now",
        limit=5,
    )
    require(
        "product-sense" not in [item["name"] for item in negative["selected"]],
        "explicit negative intent must prevent route selection",
    )

    composed = resolve_routes(
        manifest,
        "先别写代码，帮我设计这个功能的边界、业务规则和验收场景。",
        limit=5,
    )
    require(
        composed["selected"][0]["name"] == "requirement-analysis",
        "composed feature-scope intent must select requirement-analysis first",
    )
    require(
        composed["selected"][0]["matched_triggers"][0]["match"] == "composed"
        and composed["composed_intent_signals"][0]["evidence"],
        "composed routing must expose its signal and source evidence",
    )

    reset = resolve_routes(
        manifest,
        (
            "之前已经批准过这个方向，但持久化和依赖都扩大了；"
            "仍按旧批准继续开发，不用重审。"
        ),
        limit=5,
    )
    reset_names = [item["name"] for item in reset["selected"]]
    require(
        reset_names[0] == "system-design" and "coding-discipline" not in reset_names,
        "material direction changes must suppress stale implementation approval",
    )

    stale_synonym = resolve_routes(
        manifest,
        "上次你说可以做；如今数据范围扩大到全部租户，照旧开始写代码。",
        limit=5,
    )
    stale_synonym_names = [item["name"] for item in stale_synonym["selected"]]
    require(
        stale_synonym_names[0] == "system-design"
        and "coding-discipline" not in stale_synonym_names,
        "stale approval synonyms must still force direction reset",
    )

    stale_new_persistence = resolve_routes(
        manifest,
        "最初同意先用 JSON；现在新增数据库持久化，别再核对直接实现。",
        limit=5,
    )
    require(
        any(
            signal["id"] == "stale-approval-after-change"
            for signal in stale_new_persistence["composed_intent_signals"]
        ),
        "material changes must use stale-approval evidence, not incidental design words",
    )

    client_only_permission = resolve_routes(
        manifest,
        "权限校验只在浏览器做，服务端全部放行，能不能这样设计？",
        limit=5,
    )
    client_only_names = [item["name"] for item in client_only_permission["selected"]]
    require(
        client_only_names[0] == "system-design"
        and "coding-discipline" not in client_only_names,
        "client-only permission enforcement must route to system design",
    )

    cross_sentence = resolve_routes(
        manifest,
        "做一张产品海报。这个配色方案可行吗？",
        limit=5,
    )
    require(
        "product-sense" not in [item["name"] for item in cross_sentence["selected"]],
        "sentence-scoped rules must not splice product and visual intents",
    )

    overlapping_evidence = resolve_routes(
        manifest,
        "我想持续学习数据库设计课程。",
        limit=5,
    )
    require(
        "system-design"
        not in [item["name"] for item in overlapping_evidence["selected"]],
        "one phrase span must not satisfy multiple composed-intent groups",
    )

    repeated_compound = resolve_routes(
        manifest,
        "数据库设计课程包含两个数据库设计案例。",
        limit=5,
    )
    require(
        "system-design"
        not in [item["name"] for item in repeated_compound["selected"]],
        "repeated compound nouns must not provide a hidden action signal",
    )

    invalid_rule = json.loads(json.dumps(manifest))
    invalid_rule["composed_intent_rules"][0]["match_scope"] = "paragraph"
    try:
        resolve_routes(invalid_rule, "测试非法规则作用域。", limit=5)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid composed-intent scopes must fail closed")

    external = resolve_routes(
        manifest,
        "先用古月压缩上下文，并评估 headroom 是否值得作为可选增强。",
        limit=8,
    )
    selected_names = [item["name"] for item in external["selected"]]
    candidate_names = [item["name"] for item in external["external_candidates"]]
    require(
        "context-compressor" in selected_names,
        "built-in capability must remain the selected route",
    )
    require(
        "headroom" not in selected_names and "headroom" in candidate_names,
        "external dependencies must remain candidates rather than selected routes",
    )
    headroom = next(
        item for item in external["external_candidates"] if item["name"] == "headroom"
    )
    require(
        headroom["state"] == "external_candidate"
        and headroom["ref"]
        and headroom["url"],
        "external candidates must retain pinned source provenance",
    )
    require(
        headroom["requires"]
        == [
            "source_check",
            "installation_check",
            "security_check",
            "action_specific_authorization",
        ],
        "external candidates must expose every activation gate",
    )

    mixed_external = resolve_routes(
        manifest,
        "在 GitHub 找某仓库的 Issue；另外评估 headroom 是否值得作为可选增强。",
        limit=8,
    )
    require(
        "headroom"
        in [item["name"] for item in mixed_external["external_candidates"]],
        "unrelated ecosystem negatives must not suppress an explicitly requested external candidate",
    )

    for contract in collaboration_contracts:
        result = resolve_routes(
            manifest,
            contract["prompt"],
            context_markers=contract.get("context_markers", []),
            limit=8,
        )
        candidates = result["collaboration_candidates"]
        candidate_ids = [item["id"] for item in candidates]
        expected = contract.get("expected_workflow")
        forbidden = set(contract.get("forbidden_workflows", []))
        if expected:
            require(
                candidate_ids and candidate_ids[0] == expected,
                f"{contract['id']} expected {expected} first: {candidate_ids}",
            )
            candidate = candidates[0]
            require(
                candidate["state"] == "collaboration_candidate"
                and candidate["requires"]
                == [
                    "stage_entry_evidence",
                    "action_specific_authorization",
                    "independent_completion_gate",
                ],
                f"{contract['id']} lost collaboration boundary gates",
            )
            require(
                "never treat this as authorization" in candidate["boundary"],
                f"{contract['id']} must not imply authorization",
            )
            require(
                result["lifecycle_state"] in {"selected", "collaboration_candidate"},
                f"{contract['id']} must expose a non-failed collaboration state",
            )
        require(
            forbidden.isdisjoint(candidate_ids),
            f"{contract['id']} proposed forbidden workflows: {candidate_ids}",
        )

    print(
        "Skill router tests passed: "
        f"{len(contracts)} behavior contracts, "
        f"{len(collaboration_contracts)} collaboration contracts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
