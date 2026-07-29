#!/usr/bin/env python3
"""Verify Guyue capability discovery, routing, evidence, and external gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from src.skill_router import resolve_routes  # noqa: E402


DEVELOPMENT_EVIDENCE_WARNINGS = {
    "live activation evidence must cover every manifest skill exactly once",
    "live activation evidence is stale for routing semantics",
    "all-Skill output-quality evidence is incomplete",
    "all-Skill output-quality evidence is stale for current Skill files",
    "all-Skill output-quality evidence is stale for evaluation contract",
    "all-Skill output-quality evidence is stale for evaluation runner",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output_quality_identity_current(
    receipt: object,
    *,
    root: Path = ROOT,
) -> tuple[bool, bool]:
    if not isinstance(receipt, dict):
        return False, False
    contract_path = root / "evals/capability-output-quality.json"
    runner_path = root / "scripts/run_capability_output_quality.py"
    return (
        contract_path.is_file()
        and receipt.get("evaluation_contract_sha256") == file_sha256(contract_path),
        runner_path.is_file()
        and receipt.get("evaluation_runner_sha256") == file_sha256(runner_path),
    )


def routing_sha256(manifest: dict[str, object]) -> str:
    skill_fields = (
        "name", "path", "trigger_intent", "negative_intent",
        "external_candidate_negative_intent",
        "required_any_context", "routing_priority", "description",
        "root_exposure", "activation_policy",
    )
    external_fields = (
        "name", "trigger_intent", "negative_intent", "description",
        "url", "ref", "root_exposure", "activation_policy",
    )
    payload = {
        "routing_contract": manifest["routing_contract"],
        "composed_intent_rules": manifest.get("composed_intent_rules", []),
        "skills": [
            {key: skill[key] for key in skill_fields if key in skill}
            for skill in manifest["skills"]
        ],
        "external_dependencies": [
            {key: item[key] for key in external_fields if key in item}
            for item in manifest["external_dependencies"]
        ],
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def model_activation_claim_verified(
    live: dict,
    *,
    routing_current: bool,
    live_passed: int,
    live_total: int,
    expected_total: int,
) -> bool:
    return (
        routing_current
        and live.get("status") == "pass"
        and live.get("claims", {}).get("model_activation_verified") is True
        and live_passed == expected_total
        and live_total == expected_total
    )


def build_receipt(root: Path = ROOT) -> dict[str, object]:
    manifest = load_json(root / "skills_manifest.json")
    prompts = load_json(root / "test-prompts.json")
    route_contract = load_json(root / "evals/capability-routing.json")
    near_miss_contract = load_json(root / "evals/capability-near-misses.json")
    collaboration_eval = load_json(root / "evals/capability-collaboration.json")
    if not isinstance(manifest, dict) or not isinstance(prompts, list):
        raise AssertionError("manifest and prompts must have their documented shapes")
    if not isinstance(route_contract, dict) or not isinstance(
        route_contract.get("cases"), list
    ):
        raise AssertionError("capability-routing.json must contain a cases list")
    if not isinstance(collaboration_eval, dict) or not isinstance(
        collaboration_eval.get("cases"), list
    ):
        raise AssertionError("capability-collaboration.json must contain a cases list")

    skills = manifest.get("skills", [])
    external = manifest.get("external_dependencies", [])
    if not isinstance(skills, list) or not isinstance(external, list):
        raise AssertionError("manifest capability collections must be lists")
    skill_names = {str(skill.get("name", "")) for skill in skills}
    evidence_contract = manifest.get("evidence_contract", {})
    envelope_fields = set(evidence_contract.get("envelope_fields", []))
    evidence_profiles = evidence_contract.get("profiles", {})
    if evidence_contract.get("version") != 1:
        raise AssertionError("evidence_contract.version must be 1")
    if not isinstance(evidence_profiles, dict) or not envelope_fields:
        raise AssertionError("evidence contract profiles and fields are required")
    for profile, required_fields in evidence_profiles.items():
        if not isinstance(required_fields, list) or not set(required_fields) <= envelope_fields:
            raise AssertionError(f"invalid evidence profile fields: {profile}")
    prompts_by_name = {
        str(prompt.get("name", "")): prompt
        for prompt in prompts
        if isinstance(prompt, dict)
    }

    errors: list[str] = []
    collaboration_contract = manifest.get("collaboration_contract", {})
    collaboration_workflows = (
        collaboration_contract.get("workflows", [])
        if isinstance(collaboration_contract, dict)
        else []
    )
    collaboration_modes = set(
        collaboration_contract.get("stage_modes", [])
        if isinstance(collaboration_contract, dict)
        else []
    )
    if not isinstance(collaboration_contract, dict) or (
        collaboration_contract.get("version") != 1
    ):
        errors.append("collaboration_contract.version must be 1")
    if not isinstance(collaboration_workflows, list) or not collaboration_workflows:
        errors.append("collaboration contract workflows are required")
        collaboration_workflows = []
    workflow_ids: set[str] = set()
    collaboration_skill_coverage: set[str] = set()
    for workflow in collaboration_workflows:
        if not isinstance(workflow, dict):
            errors.append("collaboration workflows must be objects")
            continue
        workflow_id = str(workflow.get("id", "")).strip()
        if not workflow_id or workflow_id in workflow_ids:
            errors.append(f"missing or duplicate collaboration workflow id: {workflow_id!r}")
            continue
        workflow_ids.add(workflow_id)
        if not str(workflow.get("description", "")).strip():
            errors.append(f"{workflow_id} is missing description")
        if not workflow.get("trigger_intent") or not workflow.get("entry_skills"):
            errors.append(f"{workflow_id} requires triggers and entry skills")
        if not str(workflow.get("completion_gate", "")).strip():
            errors.append(f"{workflow_id} is missing completion_gate")
        stages = workflow.get("stages", [])
        if not isinstance(stages, list) or not stages:
            errors.append(f"{workflow_id} requires collaboration stages")
            continue
        referenced = set(workflow.get("entry_skills", []))
        for stage in stages:
            if not isinstance(stage, dict):
                errors.append(f"{workflow_id} stages must be objects")
                continue
            mode = str(stage.get("mode", ""))
            if mode not in collaboration_modes:
                errors.append(f"{workflow_id} uses unknown stage mode: {mode}")
            stage_skills = set(stage.get("skills", []))
            if not stage_skills:
                errors.append(f"{workflow_id} has an empty stage: {stage.get('id')}")
            referenced.update(stage_skills)
        unknown_skills = referenced - skill_names
        if unknown_skills:
            errors.append(
                f"{workflow_id} references unknown skills: {sorted(unknown_skills)}"
            )
        collaboration_skill_coverage.update(referenced & skill_names)
    minimum_collaboration_coverage = int(
        collaboration_eval.get("minimum_skill_coverage", len(skills))
    )
    if len(collaboration_skill_coverage) < minimum_collaboration_coverage:
        errors.append(
            "collaboration workflows cover only "
            f"{len(collaboration_skill_coverage)}/{minimum_collaboration_coverage} skills"
        )

    route_passed = 0
    bound_prompt_names: set[str] = set()
    case_ids: set[str] = set()
    for case in route_contract["cases"]:
        if not isinstance(case, dict):
            errors.append("capability route cases must be objects")
            continue
        case_id = str(case.get("id", "")).strip()
        prompt_name = str(case.get("prompt_name", "")).strip()
        if not case_id or case_id in case_ids:
            errors.append(f"missing or duplicate capability case id: {case_id!r}")
            continue
        case_ids.add(case_id)
        if prompt_name in bound_prompt_names:
            errors.append(f"duplicate prompt binding: {prompt_name}")
        bound_prompt_names.add(prompt_name)
        prompt = prompts_by_name.get(prompt_name)
        if prompt is None:
            errors.append(f"unknown prompt binding: {prompt_name}")
            continue
        expected = set(case.get("expected_routes", []))
        forbidden = set(case.get("forbidden_routes", []))
        expected_primary = str(case.get("expected_primary", "")).strip()
        unknown = (expected | forbidden | ({expected_primary} if expected_primary else set())) - skill_names
        if unknown:
            errors.append(f"{case_id} references unknown routes: {sorted(unknown)}")
            continue
        if expected & forbidden:
            errors.append(f"{case_id} expects and forbids the same route")
            continue
        if expected_primary and expected_primary not in expected:
            errors.append(f"{case_id} expected_primary must also be expected")
            continue
        decision = resolve_routes(manifest, str(prompt.get("prompt", "")), limit=8)
        selected_order = [
            str(item.get("name", "")) for item in decision["selected"]
        ]
        selected = set(selected_order)
        missing = expected - selected
        leaked = forbidden & selected
        primary_mismatch = bool(
            expected_primary
            and (not selected_order or selected_order[0] != expected_primary)
        )
        if missing:
            errors.append(f"{case_id} missed expected routes: {sorted(missing)}")
        if leaked:
            errors.append(f"{case_id} selected forbidden routes: {sorted(leaked)}")
        if primary_mismatch:
            actual_primary = selected_order[0] if selected_order else "<none>"
            errors.append(
                f"{case_id} expected primary {expected_primary}, got {actual_primary}"
            )
        if not missing and not leaked and not primary_mismatch:
            route_passed += 1

    unbound = set(prompts_by_name) - bound_prompt_names
    if unbound:
        errors.append(f"unbound test prompts: {sorted(unbound)}")

    collaboration_passed = 0
    for case in collaboration_eval["cases"]:
        if not isinstance(case, dict):
            errors.append("collaboration eval cases must be objects")
            continue
        case_id = str(case.get("id", "")).strip()
        expected = case.get("expected_workflow")
        forbidden = set(case.get("forbidden_workflows", []))
        referenced_workflows = forbidden | ({str(expected)} if expected else set())
        unknown_workflows = referenced_workflows - workflow_ids
        if unknown_workflows:
            errors.append(
                f"{case_id} references unknown workflows: {sorted(unknown_workflows)}"
            )
            continue
        decision = resolve_routes(
            manifest,
            str(case.get("prompt", "")),
            context_markers=[str(item) for item in case.get("context_markers", [])],
            limit=8,
        )
        candidate_ids = [
            str(item.get("id", ""))
            for item in decision.get("collaboration_candidates", [])
        ]
        wrong_first = bool(expected) and (
            not candidate_ids or candidate_ids[0] != expected
        )
        leaked = forbidden & set(candidate_ids)
        if wrong_first:
            errors.append(
                f"{case_id} expected {expected} first, got {candidate_ids}"
            )
        if leaked:
            errors.append(
                f"{case_id} proposed forbidden workflows: {sorted(leaked)}"
            )
        if not wrong_first and not leaked:
            collaboration_passed += 1

    trigger_total = 0
    trigger_passed = 0
    profile_counts: dict[str, int] = {}
    for skill in skills:
        if not isinstance(skill, dict):
            errors.append("manifest skills must be objects")
            continue
        name = str(skill.get("name", ""))
        profile = str(skill.get("evidence_profile", ""))
        profile_counts[profile] = profile_counts.get(profile, 0) + 1
        if profile not in evidence_profiles:
            errors.append(f"{name} references unknown evidence profile: {profile}")
        skill_path = root / str(skill.get("path", ""))
        try:
            frontmatter = yaml.safe_load(
                skill_path.read_text(encoding="utf-8").split("---", 2)[1]
            )
        except (OSError, IndexError, yaml.YAMLError) as exc:
            errors.append(f"{name} frontmatter is unreadable: {exc}")
            continue
        description = str((frontmatter or {}).get("description", "")).strip()
        if not 80 <= len(description) <= 1024:
            errors.append(
                f"{name} public description must be 80-1024 characters, got {len(description)}"
            )
        for trigger in skill.get("trigger_intent", []):
            trigger_total += 1
            selected = {
                item["name"]
                for item in resolve_routes(manifest, str(trigger), limit=len(skills))[
                    "selected"
                ]
            }
            if name in selected:
                trigger_passed += 1
            else:
                errors.append(f"{name} cannot select itself from trigger: {trigger}")

    external_trigger_total = 0
    external_trigger_passed = 0
    for dependency in external:
        if not isinstance(dependency, dict):
            errors.append("external dependencies must be objects")
            continue
        name = str(dependency.get("name", ""))
        for field in ("url", "ref", "package_id", "command", "evidence_profile"):
            if not str(dependency.get(field, "")).strip():
                errors.append(f"external dependency {name} is missing {field}")
        triggers = dependency.get("trigger_intent", [])
        if not isinstance(triggers, list) or not triggers:
            errors.append(f"external dependency {name} has no trigger_intent")
            continue
        for trigger in triggers:
            external_trigger_total += 1
            decision = resolve_routes(manifest, str(trigger), limit=len(external))
            selected = {item["name"] for item in decision["selected"]}
            candidates = {item["name"] for item in decision["external_candidates"]}
            if name in candidates and name not in selected:
                external_trigger_passed += 1
            else:
                errors.append(
                    f"external dependency {name} did not remain a candidate for: {trigger}"
                )

    near_miss_total = 0
    near_miss_passed = 0
    near_miss_cases = (
        near_miss_contract.get("cases", [])
        if isinstance(near_miss_contract, dict)
        else []
    )
    minimum_near_misses = (
        near_miss_contract.get("minimum_per_skill", 0)
        if isinstance(near_miss_contract, dict)
        else 0
    )
    covered_near_miss_skills: set[str] = set()
    for case in near_miss_cases:
        if not isinstance(case, dict):
            errors.append("near-miss cases must be objects")
            continue
        name = str(case.get("skill", ""))
        prompts_for_skill = case.get("prompts", [])
        if name not in skill_names:
            errors.append(f"near-miss case references unknown skill: {name}")
            continue
        if name in covered_near_miss_skills:
            errors.append(f"duplicate near-miss skill: {name}")
            continue
        covered_near_miss_skills.add(name)
        if not isinstance(prompts_for_skill, list) or len(prompts_for_skill) < minimum_near_misses:
            errors.append(
                f"{name} requires at least {minimum_near_misses} near-miss prompts"
            )
            continue
        for prompt in prompts_for_skill:
            near_miss_total += 1
            selected = {
                item["name"]
                for item in resolve_routes(manifest, str(prompt), limit=len(skills))[
                    "selected"
                ]
            }
            if name not in selected:
                near_miss_passed += 1
            else:
                errors.append(f"{name} false-triggered for near miss: {prompt}")
    missing_near_miss_skills = skill_names - covered_near_miss_skills
    if missing_near_miss_skills:
        errors.append(
            f"skills missing near-miss coverage: {sorted(missing_near_miss_skills)}"
        )

    live_path = root / "evals/evidence/capability-live-canaries-2026-07-13.json"
    model_activation_verified = False
    live_routing_current = False
    live_passed = 0
    live_total = 0
    if live_path.is_file():
        live = load_json(live_path)
        if not isinstance(live, dict):
            errors.append("capability live evidence must be an object")
        else:
            live_results = live.get("results", [])
            if not isinstance(live_results, list):
                errors.append("capability live evidence results must be a list")
                live_results = []
            live_total = len(live_results)
            live_names: set[str] = set()
            for result in live_results:
                if not isinstance(result, dict):
                    errors.append("capability live evidence result must be an object")
                    continue
                name = str(result.get("skill", ""))
                live_names.add(name)
                passed = (
                    result.get("status") == "pass"
                    and result.get("target_skill_file_read") is True
                    and result.get("observed_final") == f"ACTIVATED:{name}"
                    and result.get("exit_code") == 0
                )
                artifact_path = root / str(result.get("audit_artifact", ""))
                artifact_valid = False
                if artifact_path.is_file():
                    try:
                        artifact = load_json(artifact_path)
                    except (OSError, json.JSONDecodeError):
                        artifact = None
                    commands = artifact.get("commands", []) if isinstance(artifact, dict) else []
                    artifact_valid = (
                        result.get("audit_artifact_sha256")
                        == file_sha256(artifact_path)
                        and artifact.get("skill") == name
                        and artifact.get("observed_final") == f"ACTIVATED:{name}"
                        and any(
                            f"skills/{name}/SKILL.md" in str(command.get("command", ""))
                            for command in commands
                            if isinstance(command, dict)
                        )
                    )
                passed = passed and artifact_valid
                if passed:
                    live_passed += 1
                else:
                    errors.append(f"invalid live activation evidence for {name}")
            if live_names != skill_names:
                errors.append(
                    "live activation evidence must cover every manifest skill exactly once"
                )
            live_routing_current = (
                live.get("routing_sha256") == routing_sha256(manifest)
            )
            if not live_routing_current:
                errors.append("live activation evidence is stale for routing semantics")
            model_activation_verified = model_activation_claim_verified(
                live,
                routing_current=live_routing_current,
                live_passed=live_passed,
                live_total=live_total,
                expected_total=len(skills),
            )
    else:
        errors.append("missing capability live activation evidence")

    profile_replay_path = (
        root / "evals/evidence/capability-evidence-profile-replay-2026-07-13.json"
    )
    profile_output_quality_verified = False
    if not profile_replay_path.is_file():
        errors.append("missing evidence-profile output replay")
    else:
        profile_replay = load_json(profile_replay_path)
        if not isinstance(profile_replay, dict):
            errors.append("evidence-profile output replay must be an object")
        else:
            replay_results = profile_replay.get("results", [])
            replay_profiles = set()
            for result in replay_results if isinstance(replay_results, list) else []:
                if not isinstance(result, dict):
                    continue
                replay_profiles.add(str(result.get("profile", "")))
                skill_path = root / "skills" / str(result.get("skill", "")) / "SKILL.md"
                if (
                    result.get("status") != "pass"
                    or not skill_path.is_file()
                    or result.get("skill_sha256") != file_sha256(skill_path)
                ):
                    errors.append(
                        f"stale or failed evidence-profile replay: {result.get('profile')}"
                    )
            attempts = profile_replay.get("attempts", [])
            final_attempt = attempts[-1] if isinstance(attempts, list) and attempts else {}
            for artifact_field, hash_field in (
                ("output_artifact", "output_sha256"),
                ("independent_review_artifact", "independent_review_sha256"),
            ):
                artifact = root / str(final_attempt.get(artifact_field, ""))
                if (
                    not artifact.is_file()
                    or final_attempt.get(hash_field) != file_sha256(artifact)
                ):
                    errors.append(
                        f"missing or stale evidence-profile artifact: {artifact_field}"
                    )
            profile_output_quality_verified = (
                profile_replay.get("status") == "pass"
                and replay_profiles == set(evidence_profiles)
                and profile_replay.get("claims", {}).get(
                    "profile_output_quality_verified"
                )
                is True
            )
            if not profile_output_quality_verified:
                errors.append("evidence-profile output replay is incomplete")

    output_quality_path = (
        root / "evals/evidence/capability-output-quality-2026-07-13.json"
    )
    all_skill_output_quality_verified = False
    stale_quality_skills: list[str] = []
    if not output_quality_path.is_file():
        errors.append("missing all-Skill output-quality evidence")
    else:
        output_quality = load_json(output_quality_path)
        quality_contract_current, quality_runner_current = (
            output_quality_identity_current(output_quality, root=root)
        )
        if not quality_contract_current:
            errors.append(
                "all-Skill output-quality evidence is stale for evaluation contract"
            )
        if not quality_runner_current:
            errors.append(
                "all-Skill output-quality evidence is stale for evaluation runner"
            )
        quality_results = (
            output_quality.get("results", [])
            if isinstance(output_quality, dict)
            else []
        )
        quality_names: set[str] = set()
        valid_quality_results = 0
        for result in quality_results if isinstance(quality_results, list) else []:
            if not isinstance(result, dict):
                continue
            name = str(result.get("skill", ""))
            quality_names.add(name)
            artifact_pairs = (
                ("producer_artifact", "producer_artifact_sha256"),
                ("output_artifact", "output_sha256"),
                ("review_artifact", "review_artifact_sha256"),
            )
            artifacts_valid = all(
                (root / str(result.get(path_field, ""))).is_file()
                and result.get(hash_field)
                == file_sha256(root / str(result.get(path_field, "")))
                for path_field, hash_field in artifact_pairs
            )
            review_path = root / str(result.get("review_artifact", ""))
            producer_path = root / str(result.get("producer_artifact", ""))
            review = load_json(review_path) if review_path.is_file() else None
            producer = load_json(producer_path) if producer_path.is_file() else None
            skill_path = root / "skills" / name / "SKILL.md"
            skill_current = (
                skill_path.is_file()
                and result.get("skill_sha256") == file_sha256(skill_path)
            )
            parsed_review = (
                review.get("parsed_review") if isinstance(review, dict) else None
            )
            base_valid = (
                result.get("status") == "pass"
                and artifacts_valid
                and isinstance(producer, dict)
                and producer.get("skill_file_read") is True
                and isinstance(parsed_review, dict)
                and parsed_review.get("status") == "pass"
            )
            valid = base_valid and skill_current
            if valid:
                valid_quality_results += 1
            elif base_valid and not skill_current:
                stale_quality_skills.append(name)
            else:
                errors.append(f"invalid output-quality evidence for {name}")
        if stale_quality_skills:
            errors.append(
                "all-Skill output-quality evidence is stale for current Skill files"
            )
        all_skill_output_quality_verified = (
            isinstance(output_quality, dict)
            and output_quality.get("status") == "pass"
            and output_quality.get("claims", {}).get(
                "all_skill_synthetic_output_quality_verified"
            )
            is True
            and quality_names == skill_names
            and valid_quality_results == len(skills)
            and quality_contract_current
            and quality_runner_current
        )
        if not all_skill_output_quality_verified:
            errors.append("all-Skill output-quality evidence is incomplete")

    return {
        "schema_version": 1,
        "status": "pass" if not errors else "fail",
        "skill_count": len(skills),
        "capability_route_checks": {
            "passed": route_passed,
            "total": len(route_contract["cases"]),
        },
        "collaboration_route_checks": {
            "passed": collaboration_passed,
            "total": len(collaboration_eval["cases"]),
        },
        "collaboration_workflow_count": len(workflow_ids),
        "collaboration_skill_coverage": {
            "covered": len(collaboration_skill_coverage),
            "total": len(skills),
        },
        "internal_trigger_checks": {
            "passed": trigger_passed,
            "total": trigger_total,
        },
        "external_candidate_trigger_checks": {
            "passed": external_trigger_passed,
            "total": external_trigger_total,
        },
        "near_miss_checks": {
            "passed": near_miss_passed,
            "total": near_miss_total,
        },
        "live_activation_checks": {
            "passed": live_passed,
            "total": live_total,
            "routing_current": live_routing_current,
        },
        "evidence_profiles": dict(sorted(profile_counts.items())),
        "stale_output_quality_skills": sorted(stale_quality_skills),
        "external_dependency_count": len(external),
        "claims": {
            "deterministic_routing_verified": (
                route_passed == len(route_contract["cases"])
                and collaboration_passed == len(collaboration_eval["cases"])
                and trigger_passed == trigger_total
                and external_trigger_passed == external_trigger_total
                and near_miss_passed == near_miss_total
            ),
            "collaboration_routing_verified": (
                collaboration_passed == len(collaboration_eval["cases"])
                and len(collaboration_skill_coverage) == len(skills)
            ),
            "model_activation_verified": model_activation_verified,
            "required_action_execution_verified": False,
            "profile_output_quality_verified": profile_output_quality_verified,
            "all_skill_synthetic_output_quality_verified": (
                all_skill_output_quality_verified
            ),
            "output_quality_verified": all_skill_output_quality_verified,
            "public_network_verified": False,
        },
        "errors": errors,
    }


def apply_evidence_policy(receipt: dict[str, object], *, strict: bool) -> dict[str, object]:
    """Keep stale live evidence visible without blocking ordinary development checks."""
    raw_errors = [str(item) for item in receipt.get("errors", [])]
    if strict:
        receipt["evidence_policy"] = "release_strict"
        receipt["warnings"] = []
        receipt["status"] = "pass" if not raw_errors else "fail"
        return receipt

    warnings = [
        error for error in raw_errors if error in DEVELOPMENT_EVIDENCE_WARNINGS
    ]
    errors = [
        error for error in raw_errors if error not in DEVELOPMENT_EVIDENCE_WARNINGS
    ]
    receipt["evidence_policy"] = "development_advisory"
    receipt["warnings"] = warnings
    receipt["errors"] = errors
    receipt["status"] = "pass_with_warnings" if warnings and not errors else (
        "pass" if not errors else "fail"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat stale or incomplete all-Skill live evidence as release-blocking",
    )
    args = parser.parse_args()
    strict = args.strict or os.getenv("GUYUE_RELEASE_STRICT") == "1"
    receipt = apply_evidence_policy(build_receipt(), strict=strict)
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    else:
        route = receipt["capability_route_checks"]
        collaboration = receipt["collaboration_route_checks"]
        internal = receipt["internal_trigger_checks"]
        external = receipt["external_candidate_trigger_checks"]
        near_miss = receipt["near_miss_checks"]
        print(
            "Capability chain: "
            f"routes {route['passed']}/{route['total']}, "
            f"collaboration {collaboration['passed']}/{collaboration['total']}, "
            f"internal triggers {internal['passed']}/{internal['total']}, "
            f"external candidates {external['passed']}/{external['total']}, "
            f"near misses {near_miss['passed']}/{near_miss['total']}"
        )
        for warning in receipt["warnings"]:
            print(f"WARNING: {warning}", file=sys.stderr)
        for error in receipt["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if receipt["status"] in {"pass", "pass_with_warnings"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
