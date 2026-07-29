#!/usr/bin/env python3
"""Structural evaluator for Guyue test prompts.

This script does not call a model. It verifies that the local prompt suite is
complete enough to support repeatable live evaluation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.skill_router import resolve_routes  # noqa: E402


PROMPTS_PATH = ROOT / "test-prompts.json"
MANIFEST_PATH = ROOT / "skills_manifest.json"
CONTRACTS_PATH = ROOT / "evals" / "behavior-contracts.json"
CAPABILITY_ROUTES_PATH = ROOT / "evals" / "capability-routing.json"

SAFETY_KEYWORDS = {
    "trace": ["trace", "[Trace", "轨迹"],
    "approval": ["确认", "等待", "halt", "approval", "授权"],
    "research": ["research", "联网", "官方", "latest", "检索"],
    "debugging": ["RCA", "日志", "stack", "盲猜"],
    "memory": ["memory", "记忆", ".guyue_memory"],
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def normalize_skill_name(name: str) -> str:
    return name.split("/", 1)[-1].lower()


def prompt_text(entry: dict[str, str]) -> str:
    return f"{entry.get('name', '')}\n{entry.get('prompt', '')}\n{entry.get('expected_behavior', '')}".lower()


def main() -> int:
    prompts = load_json(PROMPTS_PATH)
    manifest = load_json(MANIFEST_PATH)
    contracts = load_json(CONTRACTS_PATH)
    capability_routes = load_json(CAPABILITY_ROUTES_PATH)

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(prompts, list):
        errors.append("test-prompts.json must contain a list")
        prompts = []

    if not isinstance(manifest, dict):
        errors.append("skills_manifest.json must contain an object")
        manifest = {}

    names_seen: set[str] = set()
    combined_text = ""

    for index, raw_entry in enumerate(prompts, start=1):
        if not isinstance(raw_entry, dict):
            errors.append(f"prompt #{index} must be an object")
            continue

        name = str(raw_entry.get("name", "")).strip()
        user_prompt = str(raw_entry.get("prompt", "")).strip()
        expected = str(raw_entry.get("expected_behavior", "")).strip()

        if not name:
            errors.append(f"prompt #{index} is missing name")
        elif name in names_seen:
            errors.append(f"duplicate prompt name: {name}")
        else:
            names_seen.add(name)

        if not user_prompt:
            errors.append(f"prompt '{name or index}' is missing prompt")
        if not expected:
            errors.append(f"prompt '{name or index}' is missing expected_behavior")

        combined_text += "\n" + prompt_text(raw_entry)

    manifest_skills = manifest.get("skills", []) if isinstance(manifest, dict) else []
    if not isinstance(manifest_skills, list):
        errors.append("skills_manifest.json field 'skills' must be a list")
        manifest_skills = []

    missing_skills: list[str] = []
    for raw_skill in manifest_skills:
        if not isinstance(raw_skill, dict):
            errors.append("each manifest skill must be an object")
            continue
        skill_name = normalize_skill_name(str(raw_skill.get("name", "")).strip())
        if not skill_name:
            errors.append("manifest skill is missing name")
            continue
        if skill_name not in combined_text:
            missing_skills.append(skill_name)

    if missing_skills:
        errors.append("missing test prompt coverage for skills: " + ", ".join(sorted(missing_skills)))

    manifest_names = {
        normalize_skill_name(str(item.get("name", "")).strip())
        for item in manifest_skills
        if isinstance(item, dict)
    }
    contract_ids: set[str] = set()
    deterministic_routes_passed = 0
    capability_routes_passed = 0
    evidence_levels = {"L0", "L1", "L2", "L3", "L4"}
    if not isinstance(contracts, list):
        errors.append("evals/behavior-contracts.json must contain a list")
        contracts = []

    for index, raw_contract in enumerate(contracts, start=1):
        if not isinstance(raw_contract, dict):
            errors.append(f"behavior contract #{index} must be an object")
            continue
        contract_id = str(raw_contract.get("id", "")).strip()
        if not contract_id:
            errors.append(f"behavior contract #{index} is missing id")
        elif contract_id in contract_ids:
            errors.append(f"duplicate behavior contract id: {contract_id}")
        else:
            contract_ids.add(contract_id)

        if not str(raw_contract.get("prompt", "")).strip():
            errors.append(f"behavior contract '{contract_id or index}' is missing prompt")

        route_sets: dict[str, set[str]] = {}
        for field in ("expected_routes", "forbidden_routes"):
            values = raw_contract.get(field)
            if not isinstance(values, list):
                errors.append(f"behavior contract '{contract_id or index}' field '{field}' must be a list")
                values = []
            normalized = {normalize_skill_name(str(value).strip()) for value in values if str(value).strip()}
            unknown = normalized - manifest_names
            if unknown:
                errors.append(
                    f"behavior contract '{contract_id or index}' has unknown {field}: "
                    + ", ".join(sorted(unknown))
                )
            route_sets[field] = normalized

        overlap = route_sets.get("expected_routes", set()) & route_sets.get("forbidden_routes", set())
        if overlap:
            errors.append(
                f"behavior contract '{contract_id or index}' expects and forbids: "
                + ", ".join(sorted(overlap))
            )

        for field in ("required_actions", "forbidden_side_effects"):
            values = raw_contract.get(field)
            if not isinstance(values, list) or not values or not all(str(value).strip() for value in values):
                errors.append(
                    f"behavior contract '{contract_id or index}' field '{field}' must be a non-empty string list"
                )

        expected_external = raw_contract.get("expected_external_candidates", [])
        if not isinstance(expected_external, list):
            errors.append(
                f"behavior contract '{contract_id or index}' field "
                "'expected_external_candidates' must be a list"
            )
            expected_external = []
        known_external = {
            normalize_skill_name(str(item.get("name", "")).strip())
            for item in manifest.get("external_dependencies", [])
            if isinstance(item, dict)
        }
        normalized_external = {
            normalize_skill_name(str(value).strip())
            for value in expected_external
            if str(value).strip()
        }
        unknown_external = normalized_external - known_external
        if unknown_external:
            errors.append(
                f"behavior contract '{contract_id or index}' has unknown "
                "expected_external_candidates: "
                + ", ".join(sorted(unknown_external))
            )
        expected_lifecycle = str(
            raw_contract.get("expected_lifecycle_state", "")
        ).strip()
        if expected_lifecycle and expected_lifecycle not in {
            "selected",
            "collaboration_candidate",
            "local_candidate",
            "external_candidate",
            "failed",
        }:
            errors.append(
                f"behavior contract '{contract_id or index}' has invalid "
                f"expected_lifecycle_state: {expected_lifecycle}"
            )

        level = str(raw_contract.get("minimum_evidence_level", "")).strip()
        if level not in evidence_levels:
            errors.append(
                f"behavior contract '{contract_id or index}' has invalid minimum_evidence_level: {level or '<missing>'}"
            )

        prompt = str(raw_contract.get("prompt", "")).strip()
        if prompt and isinstance(manifest, dict):
            try:
                decision = resolve_routes(manifest, prompt, limit=8)
            except ValueError as exc:
                errors.append(
                    f"behavior contract '{contract_id or index}' route check failed: {exc}"
                )
            else:
                selected = {
                    normalize_skill_name(str(item.get("name", "")))
                    for item in decision["selected"]
                }
                expected = route_sets.get("expected_routes", set())
                forbidden = route_sets.get("forbidden_routes", set())
                missing_expected = expected - selected
                selected_forbidden = forbidden & selected
                actual_external = {
                    normalize_skill_name(str(item.get("name", "")))
                    for item in decision["external_candidates"]
                }
                missing_external = normalized_external - actual_external
                lifecycle_mismatch = bool(
                    expected_lifecycle
                    and decision["lifecycle_state"] != expected_lifecycle
                )
                if missing_expected:
                    errors.append(
                        f"behavior contract '{contract_id or index}' missed expected routes: "
                        + ", ".join(sorted(missing_expected))
                    )
                if selected_forbidden:
                    errors.append(
                        f"behavior contract '{contract_id or index}' selected forbidden routes: "
                        + ", ".join(sorted(selected_forbidden))
                    )
                if missing_external:
                    errors.append(
                        f"behavior contract '{contract_id or index}' missed "
                        "expected external candidates: "
                        + ", ".join(sorted(missing_external))
                    )
                if lifecycle_mismatch:
                    errors.append(
                        f"behavior contract '{contract_id or index}' expected "
                        f"lifecycle {expected_lifecycle}, got "
                        f"{decision['lifecycle_state']}"
                    )
                if (
                    not missing_expected
                    and not selected_forbidden
                    and not missing_external
                    and not lifecycle_mismatch
                ):
                    deterministic_routes_passed += 1

    capability_cases = (
        capability_routes.get("cases", [])
        if isinstance(capability_routes, dict)
        else []
    )
    if not isinstance(capability_routes, dict):
        errors.append("evals/capability-routing.json must contain an object")
    elif capability_routes.get("schema_version") != 1:
        errors.append("evals/capability-routing.json must use schema_version 1")
    if not isinstance(capability_cases, list):
        errors.append("evals/capability-routing.json field 'cases' must be a list")
        capability_cases = []

    prompts_by_name = {
        str(entry.get("name", "")).strip(): entry
        for entry in prompts
        if isinstance(entry, dict) and str(entry.get("name", "")).strip()
    }
    capability_ids: set[str] = set()
    capability_prompt_names: set[str] = set()
    for index, raw_case in enumerate(capability_cases, start=1):
        if not isinstance(raw_case, dict):
            errors.append(f"capability route case #{index} must be an object")
            continue
        case_id = str(raw_case.get("id", "")).strip()
        case_label = case_id or str(index)
        prompt_name = str(raw_case.get("prompt_name", "")).strip()
        if not case_id:
            errors.append(f"capability route case #{index} is missing id")
        elif case_id in capability_ids:
            errors.append(f"duplicate capability route case id: {case_id}")
        else:
            capability_ids.add(case_id)
        if not prompt_name:
            errors.append(f"capability route case '{case_label}' is missing prompt_name")
            continue
        if prompt_name in capability_prompt_names:
            errors.append(f"duplicate capability route prompt binding: {prompt_name}")
        capability_prompt_names.add(prompt_name)
        prompt_entry = prompts_by_name.get(prompt_name)
        if prompt_entry is None:
            errors.append(
                f"capability route case '{case_label}' references unknown prompt: {prompt_name}"
            )
            continue

        route_sets: dict[str, set[str]] = {}
        for field in ("expected_routes", "forbidden_routes"):
            values = raw_case.get(field)
            if not isinstance(values, list):
                errors.append(
                    f"capability route case '{case_label}' field '{field}' must be a list"
                )
                values = []
            normalized = {
                normalize_skill_name(str(value).strip())
                for value in values
                if str(value).strip()
            }
            unknown = normalized - manifest_names
            if unknown:
                errors.append(
                    f"capability route case '{case_label}' has unknown {field}: "
                    + ", ".join(sorted(unknown))
                )
            route_sets[field] = normalized
        overlap = route_sets["expected_routes"] & route_sets["forbidden_routes"]
        if overlap:
            errors.append(
                f"capability route case '{case_label}' expects and forbids: "
                + ", ".join(sorted(overlap))
            )
        expected_primary = normalize_skill_name(
            str(raw_case.get("expected_primary", "")).strip()
        )
        if expected_primary:
            if expected_primary not in manifest_names:
                errors.append(
                    f"capability route case '{case_label}' has unknown expected_primary: "
                    f"{expected_primary}"
                )
            if expected_primary not in route_sets["expected_routes"]:
                errors.append(
                    f"capability route case '{case_label}' expected_primary must also "
                    "appear in expected_routes"
                )

        prompt = str(prompt_entry.get("prompt", "")).strip()
        try:
            decision = resolve_routes(manifest, prompt, limit=8)
        except ValueError as exc:
            errors.append(
                f"capability route case '{case_label}' route check failed: {exc}"
            )
            continue
        selected_order = [
            normalize_skill_name(str(item.get("name", "")))
            for item in decision["selected"]
        ]
        selected = set(selected_order)
        missing_expected = route_sets["expected_routes"] - selected
        selected_forbidden = route_sets["forbidden_routes"] & selected
        primary_mismatch = bool(
            expected_primary
            and (not selected_order or selected_order[0] != expected_primary)
        )
        if missing_expected:
            errors.append(
                f"capability route case '{case_label}' missed expected routes: "
                + ", ".join(sorted(missing_expected))
            )
        if selected_forbidden:
            errors.append(
                f"capability route case '{case_label}' selected forbidden routes: "
                + ", ".join(sorted(selected_forbidden))
            )
        if primary_mismatch:
            actual_primary = selected_order[0] if selected_order else "<none>"
            errors.append(
                f"capability route case '{case_label}' expected primary "
                f"{expected_primary}, got {actual_primary}"
            )
        if not missing_expected and not selected_forbidden and not primary_mismatch:
            capability_routes_passed += 1

    unbound_prompts = set(prompts_by_name) - capability_prompt_names
    if unbound_prompts:
        errors.append(
            "test prompts missing capability route bindings: "
            + ", ".join(sorted(unbound_prompts))
        )

    for safety_name, keywords in SAFETY_KEYWORDS.items():
        if not any(keyword.lower() in combined_text for keyword in keywords):
            warnings.append(f"weak safety coverage: {safety_name}")

    print("==========================================")
    print("Guyue Test Prompt Evaluation")
    print("==========================================")
    print(f"prompts: {len(prompts)}")
    print(f"behavior contracts: {len(contracts)}")
    print(f"deterministic route checks: {deterministic_routes_passed}/{len(contracts)}")
    print(
        "required action execution checks: 0/"
        f"{len(contracts)} (declarative; requires live replay evidence)"
    )
    print(
        f"capability route checks: {capability_routes_passed}/{len(capability_cases)}"
    )
    print(f"manifest skills: {len(manifest_skills)}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nEvaluation structure passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
