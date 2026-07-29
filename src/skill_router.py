"""Deterministic, explainable candidate routing for Guyue Skills."""

from __future__ import annotations

import re
import unicodedata
from bisect import bisect_right
from collections.abc import Iterable


MIN_ROUTE_SCORE = 10.0
MIN_COLLABORATION_SCORE = 20.0
LATIN_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+_.-]*")
HAN_RUN_RE = re.compile(r"[\u3400-\u9fff]+")
SENTENCE_BOUNDARY_RE = re.compile(r"[。！？!?\n]+")
COMPOSED_RULE_SCOPES = {"document", "sentence"}


def normalize_text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFKC", str(value)).casefold().split())


def text_features(value: object) -> set[str]:
    """Return word and Han n-gram features without external tokenizers."""
    text = normalize_text(value)
    features = set(LATIN_TOKEN_RE.findall(text))
    for run in HAN_RUN_RE.findall(text):
        if len(run) == 1:
            features.add(run)
            continue
        features.update(run[index : index + 2] for index in range(len(run) - 1))
        if len(run) >= 3:
            features.update(run[index : index + 3] for index in range(len(run) - 2))
    return features


def feature_similarity(left: object, right: object) -> float:
    left_features = text_features(left)
    right_features = text_features(right)
    if not left_features or not right_features:
        return 0.0
    return len(left_features & right_features) / len(left_features | right_features)


def phrase_coverage(phrase: object, haystack: object) -> float:
    phrase_features = text_features(phrase)
    if not phrase_features:
        return 0.0
    return len(phrase_features & text_features(haystack)) / len(phrase_features)


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _validated_composed_rules(value: object, skills_by_name: dict[str, dict]) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("manifest composed_intent_rules must be a list")
    validated: list[dict] = []
    seen_ids: set[str] = set()
    for index, rule in enumerate(value, start=1):
        if not isinstance(rule, dict):
            raise ValueError(f"composed intent rule #{index} must be an object")
        rule_id = str(rule.get("id", "")).strip()
        route = str(rule.get("route", "")).strip()
        canonical = str(rule.get("canonical_trigger", "")).strip()
        if not rule_id or rule_id in seen_ids:
            raise ValueError(f"missing or duplicate composed intent rule id: {rule_id!r}")
        seen_ids.add(rule_id)
        if route not in skills_by_name:
            raise ValueError(f"composed intent rule {rule_id} has unknown route: {route}")
        target_triggers = _string_list(skills_by_name[route].get("trigger_intent"))
        if canonical not in target_triggers:
            raise ValueError(
                f"composed intent rule {rule_id} canonical trigger is not owned by {route}"
            )
        score = rule.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or score <= 0:
            raise ValueError(f"composed intent rule {rule_id} requires a positive score")
        match_scope = str(rule.get("match_scope", "document")).strip()
        exclude_scope = str(rule.get("exclude_scope", match_scope)).strip()
        for field, scope in (
            ("match_scope", match_scope),
            ("exclude_scope", exclude_scope),
        ):
            if scope not in COMPOSED_RULE_SCOPES:
                raise ValueError(
                    f"composed intent rule {rule_id} field {field} "
                    f"must be one of {sorted(COMPOSED_RULE_SCOPES)}"
                )
        groups = rule.get("all_any")
        if not isinstance(groups, list) or not groups:
            raise ValueError(f"composed intent rule {rule_id} requires all_any groups")
        for group in groups:
            if not isinstance(group, list) or not group or len(_string_list(group)) != len(group):
                raise ValueError(
                    f"composed intent rule {rule_id} groups must contain strings"
                )
        for field in ("exclude_any", "blocks_routes"):
            if field not in rule:
                continue
            values = rule[field]
            if not isinstance(values, list) or len(_string_list(values)) != len(values):
                raise ValueError(
                    f"composed intent rule {rule_id} field {field} must contain strings"
                )
        reject_nested = rule.get("reject_nested_evidence", False)
        if not isinstance(reject_nested, bool):
            raise ValueError(
                f"composed intent rule {rule_id} field "
                "reject_nested_evidence must be boolean"
            )
        unknown_blocks = set(_string_list(rule.get("blocks_routes"))) - set(skills_by_name)
        if unknown_blocks:
            raise ValueError(
                f"composed intent rule {rule_id} blocks unknown routes: "
                f"{sorted(unknown_blocks)}"
            )
        validated.append(rule)
    return validated


def _direct_matches(phrases: Iterable[str], text: str) -> list[str]:
    normalized_text = normalize_text(text)
    return [phrase for phrase in phrases if normalize_text(phrase) in normalized_text]


def _negative_matches(phrases: list[str], text: str) -> list[str]:
    direct = _direct_matches(phrases, text)
    if direct:
        return direct
    fuzzy = []
    for phrase in phrases:
        features = text_features(phrase)
        if len(features) >= 2 and phrase_coverage(phrase, text) >= 0.85:
            fuzzy.append(phrase)
    return fuzzy


def _unnegated_phrase_spans(
    phrase: str, normalized_text: str
) -> list[tuple[int, int]]:
    normalized_phrase = normalize_text(phrase)
    if not normalized_phrase:
        return []
    clause_boundaries = "，。；！？,;!?\n"
    negative_markers = (
        "不要",
        "无需",
        "不需要",
        "暂不",
        "先别",
        "禁止",
        "不是",
        "不做",
        "避免",
        "不评估",
        "不判断",
    )
    spans: list[tuple[int, int]] = []
    start = 0
    while True:
        index = normalized_text.find(normalized_phrase, start)
        if index < 0:
            return spans
        clause_start = max(normalized_text.rfind(mark, 0, index) for mark in clause_boundaries)
        prefix = normalized_text[clause_start + 1 : index]
        if not any(marker in prefix for marker in negative_markers):
            spans.append((index, index + len(normalized_phrase)))
        start = index + len(normalized_phrase)


def _match_composed_groups(
    groups: list,
    segment: str,
    *,
    reject_nested_evidence: bool,
) -> list[str] | None:
    candidates: list[list[tuple[str, int, int]]] = []
    for group in groups:
        group_candidates: list[tuple[str, int, int]] = []
        for phrase in _string_list(group):
            group_candidates.extend(
                (phrase, start, end)
                for start, end in _unnegated_phrase_spans(phrase, segment)
            )
        if not group_candidates:
            return None
        candidates.append(group_candidates)

    if reject_nested_evidence:
        distinct_candidates: list[list[tuple[str, int, int]]] = []
        for group_index, group_candidates in enumerate(candidates):
            other_intervals = sorted(
                (start, end)
                for other_index, other_group in enumerate(candidates)
                if other_index != group_index
                for _, start, end in other_group
            )
            other_starts = [start for start, _ in other_intervals]
            prefix_max_ends: list[int] = []
            for _, end in other_intervals:
                prefix_max_ends.append(
                    max(prefix_max_ends[-1] if prefix_max_ends else -1, end)
                )

            def nested_in_other_group(candidate: tuple[str, int, int]) -> bool:
                index = bisect_right(other_starts, candidate[1]) - 1
                return index >= 0 and prefix_max_ends[index] >= candidate[2]

            distinct_candidates.append(
                [
                    candidate
                    for candidate in group_candidates
                    if not nested_in_other_group(candidate)
                ]
            )
        if any(not group for group in distinct_candidates):
            return None
        candidates = distinct_candidates

    def choose(
        group_index: int,
        occupied: list[tuple[int, int]],
        evidence: list[str],
    ) -> list[str] | None:
        if group_index == len(candidates):
            return evidence
        for phrase, start, end in candidates[group_index]:
            if any(start < used_end and used_start < end for used_start, used_end in occupied):
                continue
            matched = choose(
                group_index + 1,
                [*occupied, (start, end)],
                [*evidence, phrase],
            )
            if matched is not None:
                return matched
        return None

    return choose(0, [], [])


def _intent_segments(text: str, scope: str) -> list[str]:
    if scope == "document":
        normalized = normalize_text(text)
        return [normalized] if normalized else []
    return [
        normalized
        for part in SENTENCE_BOUNDARY_RE.split(
            unicodedata.normalize("NFKC", str(text)).casefold()
        )
        if (normalized := normalize_text(part))
    ]


def _derive_intent_signals(rules: object, text: str) -> list[dict]:
    if not isinstance(rules, list):
        return []
    normalized_text = normalize_text(text)
    signals: list[dict] = []
    segments_by_scope: dict[str, list[str]] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        match_scope = str(rule.get("match_scope", "document")).strip()
        exclude_scope = str(rule.get("exclude_scope", match_scope)).strip()
        groups = rule.get("all_any")
        if not isinstance(groups, list) or not groups:
            continue
        if any(
            not any(
                normalize_text(phrase) in normalized_text
                for phrase in _string_list(group)
            )
            for group in groups
        ):
            continue
        exclude_phrases = _string_list(rule.get("exclude_any"))
        if exclude_scope == "document" and any(
            normalize_text(phrase) in normalized_text for phrase in exclude_phrases
        ):
            continue
        if match_scope not in segments_by_scope:
            segments_by_scope[match_scope] = _intent_segments(text, match_scope)
        segments = segments_by_scope[match_scope]
        segment_cache: dict[str, list[str] | None] = {}
        for segment in segments:
            if segment in segment_cache:
                evidence = segment_cache[segment]
            else:
                exclusion_text = (
                    normalized_text if exclude_scope == "document" else segment
                )
                if any(
                    normalize_text(phrase) in exclusion_text
                    for phrase in exclude_phrases
                ):
                    evidence = None
                else:
                    evidence = _match_composed_groups(
                        groups,
                        segment,
                        reject_nested_evidence=bool(
                            rule.get("reject_nested_evidence", False)
                        ),
                    )
                segment_cache[segment] = evidence
            if evidence is not None:
                signals.append(
                    {
                        "id": str(rule.get("id", "")),
                        "route": str(rule.get("route", "")),
                        "canonical_trigger": str(rule.get("canonical_trigger", "")),
                        "score": float(rule.get("score", 0)),
                        "evidence": evidence,
                        "match_scope": match_scope,
                        "blocks_routes": _string_list(rule.get("blocks_routes")),
                    }
                )
                break
    return signals


def _score_skill(
    skill: dict,
    intent: str,
    context_markers: list[str],
    composed_signals: list[dict] | None = None,
) -> dict:
    name = str(skill.get("name", "")).strip()
    triggers = _string_list(skill.get("trigger_intent"))
    negatives = _string_list(skill.get("negative_intent"))
    required_context = _string_list(skill.get("required_any_context"))
    combined_context = "\n".join([intent, *context_markers])

    matched_context = _direct_matches(required_context, combined_context)
    if required_context and not matched_context:
        return {
            "name": name,
            "path": str(skill.get("path", "")),
            "score": 0.0,
            "reason": "missing_required_context",
            "matched_triggers": [],
            "matched_context": [],
            "negative_matches": [],
            "required_context": required_context,
        }

    negative_matches = _negative_matches(negatives, combined_context)
    if negative_matches:
        return {
            "name": name,
            "path": str(skill.get("path", "")),
            "score": 0.0,
            "reason": "negative_intent",
            "matched_triggers": [],
            "matched_context": matched_context,
            "negative_matches": negative_matches,
            "required_context": required_context,
        }

    score = 0.0
    matched_triggers: list[dict] = []
    normalized_query = normalize_text(combined_context)
    signal_by_trigger = {
        normalize_text(signal["canonical_trigger"]): signal
        for signal in (composed_signals or [])
        if signal["route"] == name
    }
    for trigger in triggers:
        normalized_trigger = normalize_text(trigger)
        if normalized_trigger and normalized_trigger in normalized_query:
            contribution = 30.0 + min(len(normalized_trigger), 12)
            score += contribution
            matched_triggers.append(
                {"trigger": trigger, "match": "exact", "score": contribution}
            )
            continue
        signal = signal_by_trigger.get(normalized_trigger)
        if signal:
            contribution = float(signal["score"])
            score += contribution
            matched_triggers.append(
                {
                    "trigger": trigger,
                    "match": "composed",
                    "score": contribution,
                    "signal": signal["id"],
                    "evidence": signal["evidence"],
                }
            )
            continue
        coverage = phrase_coverage(trigger, combined_context)
        if len(text_features(trigger)) >= 2 and coverage >= 0.6:
            contribution = round(14.0 * coverage, 3)
            score += contribution
            matched_triggers.append(
                {"trigger": trigger, "match": "partial", "score": contribution}
            )

    description = str(skill.get("description", ""))
    description_similarity = feature_similarity(combined_context, description)
    if description_similarity >= 0.08:
        score += min(10.0, description_similarity * 28.0)
    if score > 0:
        score += max(0, int(skill.get("routing_priority", 0))) / 20.0
        if matched_context:
            score += 20.0

    return {
        "name": name,
        "path": str(skill.get("path", "")),
        "score": round(score, 3),
        "reason": "matched" if score >= MIN_ROUTE_SCORE else "insufficient_signal",
        "matched_triggers": matched_triggers,
        "matched_context": matched_context,
        "negative_matches": [],
        "required_context": required_context,
    }


def _workflow_skill_names(workflow: dict) -> set[str]:
    names: set[str] = set()
    for stage in workflow.get("stages", []):
        if isinstance(stage, dict):
            names.update(_string_list(stage.get("skills")))
    return names


def _resolve_collaborations(
    manifest: dict,
    intent: str,
    context_markers: list[str],
    selected: list[dict],
    *,
    limit: int,
) -> tuple[int | None, list[dict]]:
    contract = manifest.get("collaboration_contract")
    if not isinstance(contract, dict):
        return None, []
    workflows = contract.get("workflows")
    if not isinstance(workflows, list):
        return contract.get("version"), []

    combined_context = "\n".join([intent, *context_markers])
    selected_names = {str(item.get("name", "")) for item in selected}
    candidates: list[dict] = []
    for workflow in workflows:
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("id", "")).strip()
        triggers = _string_list(workflow.get("trigger_intent"))
        entry_skills = set(_string_list(workflow.get("entry_skills")))
        workflow_skills = _workflow_skill_names(workflow)
        required_context = _string_list(workflow.get("required_any_context"))
        matched_context = _direct_matches(required_context, combined_context)
        if required_context and not matched_context:
            continue
        matched_triggers = _direct_matches(triggers, combined_context)
        entry_matches = sorted(entry_skills & selected_names)
        selected_matches = sorted(workflow_skills & selected_names)
        if not matched_triggers and not entry_matches:
            continue
        score = sum(30.0 + min(len(normalize_text(item)), 12) for item in matched_triggers)
        score += 8.0 * len(entry_matches) + 3.0 * len(selected_matches)
        if score < MIN_COLLABORATION_SCORE:
            continue
        candidates.append(
            {
                "id": workflow_id,
                "state": "collaboration_candidate",
                "score": round(score, 3),
                "description": str(workflow.get("description", "")),
                "matched_triggers": matched_triggers,
                "matched_context": matched_context,
                "matched_entry_skills": entry_matches,
                "matched_selected_skills": selected_matches,
                "stages": workflow.get("stages", []),
                "completion_gate": str(workflow.get("completion_gate", "")),
                "requires": [
                    "stage_entry_evidence",
                    "action_specific_authorization",
                    "independent_completion_gate",
                ],
                "boundary": (
                    "Candidate sequence only; activate the minimum necessary stages, "
                    "preserve each Skill boundary, and never treat this as authorization."
                ),
            }
        )
    ranked = sorted(candidates, key=lambda item: (-item["score"], item["id"]))
    return contract.get("version"), ranked[:limit]


def resolve_routes(
    manifest: dict,
    intent: str,
    *,
    context_markers: list[str] | None = None,
    limit: int = 5,
) -> dict:
    """Rank route candidates and retain explainable rejection evidence."""
    if not intent.strip():
        raise ValueError("intent must contain non-whitespace text")
    if limit <= 0:
        raise ValueError("limit must be positive")
    skills = manifest.get("skills")
    if not isinstance(skills, list):
        raise ValueError("manifest skills must be a list")
    skills_by_name = {
        str(skill.get("name", "")).strip(): skill
        for skill in skills
        if isinstance(skill, dict) and str(skill.get("name", "")).strip()
    }
    composed_rules = _validated_composed_rules(
        manifest.get("composed_intent_rules"),
        skills_by_name,
    )
    markers = [marker.strip() for marker in (context_markers or []) if marker.strip()]
    composed_signals = _derive_intent_signals(
        composed_rules,
        "\n".join([intent, *markers]),
    )
    blocked_routes = {
        route
        for signal in composed_signals
        for route in signal["blocks_routes"]
    }
    decisions = [
        _score_skill(skill, intent, markers, composed_signals)
        for skill in skills
        if isinstance(skill, dict) and str(skill.get("name", "")).strip()
    ]
    for decision in decisions:
        if decision["name"] not in blocked_routes:
            continue
        decision["score"] = 0.0
        decision["reason"] = "blocked_by_composed_intent"
        decision["blocking_signals"] = [
            signal["id"]
            for signal in composed_signals
            if decision["name"] in signal["blocks_routes"]
        ]
    selected = sorted(
        (
            decision
            for decision in decisions
            if decision["reason"] == "matched"
        ),
        key=lambda item: (-item["score"], item["name"]),
    )[:limit]
    selected_names = {item["name"] for item in selected}
    rejected = sorted(
        (
            decision
            for decision in decisions
            if decision["name"] not in selected_names
            and decision["reason"]
            in {
                "missing_required_context",
                "negative_intent",
                "insufficient_signal",
                "blocked_by_composed_intent",
            }
        ),
        key=lambda item: (item["reason"], item["name"]),
    )
    ecosystem_skill = skills_by_name.get("ecosystem-scout", {})
    external_candidate_blockers = _negative_matches(
        _string_list(ecosystem_skill.get("external_candidate_negative_intent")),
        "\n".join([intent, *markers]),
    )
    external_decisions = (
        []
        if external_candidate_blockers
        else [
            _score_skill(dependency, intent, markers)
            for dependency in manifest.get("external_dependencies", [])
            if isinstance(dependency, dict)
            and str(dependency.get("name", "")).strip()
        ]
    )
    external_by_name = {
        str(item.get("name", "")): item
        for item in manifest.get("external_dependencies", [])
        if isinstance(item, dict)
    }
    external_candidates = []
    for decision in sorted(
        (item for item in external_decisions if item["reason"] == "matched"),
        key=lambda item: (-item["score"], item["name"]),
    )[:limit]:
        dependency = external_by_name[decision["name"]]
        external_candidates.append(
            {
                **decision,
                "state": "external_candidate",
                "url": str(dependency.get("url", "")),
                "ref": str(dependency.get("ref", "")),
                "package_id": str(dependency.get("package_id", "")),
                "relationship": str(dependency.get("relationship", "")),
                "evidence_profile": str(dependency.get("evidence_profile", "")),
                "requires": [
                    "source_check",
                    "installation_check",
                    "security_check",
                    "action_specific_authorization",
                ],
                "boundary": (
                    "Candidate only; this result does not prove installation, "
                    "safety, authorization, or activation."
                ),
            }
        )
    contract = manifest.get("routing_contract", {})
    collaboration_version, collaboration_candidates = _resolve_collaborations(
        manifest,
        intent,
        markers,
        selected,
        limit=limit,
    )
    lifecycle_state = "selected" if selected else "failed"
    if not selected and collaboration_candidates:
        lifecycle_state = "collaboration_candidate"
    return {
        "routing_contract_version": (
            contract.get("version") if isinstance(contract, dict) else None
        ),
        "lifecycle_state": lifecycle_state,
        "selected": selected,
        "collaboration_contract_version": collaboration_version,
        "collaboration_candidates": collaboration_candidates,
        "external_candidates": external_candidates,
        "external_candidate_blockers": external_candidate_blockers,
        "rejected": rejected,
        "context_markers": markers,
        "composed_intent_signals": composed_signals,
        "blocked_routes": sorted(blocked_routes),
    }
