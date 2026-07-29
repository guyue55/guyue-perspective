"""Build and read Guyue's private, rebuildable local Skill discovery index."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import yaml


SCHEMA_VERSION = 2
MAX_SKILL_READ_CHARS = 131_072
MAX_INDEX_AGE = timedelta(hours=24)
MAX_FUTURE_SKEW = timedelta(minutes=5)
DEFAULT_SEARCH_ROOTS = (
    ("codex", "~/.codex/skills"),
    ("agents", "~/.agents/skills"),
    ("cc-switch", "~/.cc-switch/skills"),
    ("gemini", "~/.gemini/config/skills"),
    ("gemini-plugin", "~/.gemini/config/plugins"),
    ("gemini-antigravity", "~/.gemini/antigravity/skills"),
    ("cursor", "~/.cursor/skills"),
    ("guyue-home", "~/skills"),
    ("codex-plugin", "~/.codex/plugins/cache"),
)
QUOTED_TERM_RE = re.compile(r"[“\"]([^”\"\n]{2,80})[”\"]|`([^`\n]{2,80})`")


def _frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    _, separator, remainder = text.partition("\n---\n")
    if not separator:
        return {}
    raw = text[4 : len(text) - len(remainder) - len(separator)]
    try:
        value = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _quoted_terms(text: str) -> list[str]:
    terms = [
        next(group for group in match.groups() if group).strip()
        for match in QUOTED_TERM_RE.finditer(text)
    ]
    return list(dict.fromkeys(term for term in terms if term))[:48]


def _search_text(text: str, metadata: dict) -> str:
    description = str(metadata.get("description", "")).strip()
    body = text.split("\n---\n", 1)[-1][:6000]
    headings = [
        line.lstrip("# ").strip()
        for line in body.splitlines()
        if line.startswith("#")
    ][:24]
    quoted = _quoted_terms(body)
    return "\n".join([description, *headings, *quoted, body[:2500]]).strip()


def read_skill_entry(skill_file: Path, *, source: str) -> dict | None:
    try:
        with skill_file.open(encoding="utf-8") as handle:
            raw_text = handle.read(MAX_SKILL_READ_CHARS + 1)
    except (OSError, UnicodeError):
        return None
    content_truncated = len(raw_text) > MAX_SKILL_READ_CHARS
    text = raw_text[:MAX_SKILL_READ_CHARS].replace("\r\n", "\n")
    metadata = _frontmatter(text)
    name = str(metadata.get("name", "")).strip() or skill_file.parent.name
    if not name:
        return None
    return {
        "name": name,
        "path": str(skill_file.parent),
        "source": source,
        "description": str(metadata.get("description", "")).strip(),
        "trigger_intent": list(
            dict.fromkeys(
                [
                    *_string_list(metadata.get("trigger_intent")),
                    *_quoted_terms(text.split("\n---\n", 1)[-1][:6000]),
                ]
            )
        )[:48],
        "search_text": _search_text(text, metadata),
        "content_truncated": content_truncated,
        "path_available": True,
        "alternate_paths": [],
    }


def build_local_skill_index(
    search_roots: Iterable[tuple[str, Path]] | None = None,
) -> dict:
    roots = list(search_roots or ())
    if not roots:
        roots = [
            (source, Path(raw_path).expanduser())
            for source, raw_path in DEFAULT_SEARCH_ROOTS
        ]
    entries_by_name: dict[str, dict] = {}
    for source, root in roots:
        if not root.exists():
            continue
        try:
            skill_files = sorted(root.rglob("SKILL.md"), key=lambda item: str(item))
        except OSError:
            continue
        for skill_file in skill_files:
            entry = read_skill_entry(skill_file, source=source)
            if entry is None:
                continue
            key = entry["name"].casefold()
            current = entries_by_name.get(key)
            if current is None:
                entries_by_name[key] = entry
                continue
            current["alternate_paths"].append(
                {"path": entry["path"], "source": entry["source"]}
            )
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills": sorted(
            entries_by_name.values(),
            key=lambda item: (item["name"].casefold(), item["source"]),
        ),
    }


def _index_observed_at(generated_at: object) -> datetime | None:
    if not isinstance(generated_at, str) or not generated_at.strip():
        return None
    try:
        observed_at = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    if observed_at.tzinfo is None:
        return None
    return observed_at.astimezone(timezone.utc)


def _index_status(observed_at: datetime | None, *, now: datetime) -> str:
    if observed_at is None:
        return "stale"
    age = now - observed_at.astimezone(timezone.utc)
    if age < -MAX_FUTURE_SKEW or age > MAX_INDEX_AGE:
        return "stale"
    return "available"


def _validated_cached_skills(
    skills: list[object],
    *,
    refresh: bool,
    observed_at: datetime | None,
) -> tuple[list[dict], int]:
    available: list[dict] = []
    unavailable_count = 0
    for raw_item in skills:
        if not isinstance(raw_item, dict):
            continue
        raw_path = raw_item.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            unavailable_count += 1
            continue
        skill_file = Path(raw_path) / "SKILL.md"
        try:
            modified_after_index = (
                observed_at is not None
                and datetime.fromtimestamp(
                    skill_file.stat().st_mtime,
                    tz=timezone.utc,
                )
                > observed_at
            )
        except OSError:
            unavailable_count += 1
            continue
        if refresh or modified_after_index:
            item = read_skill_entry(
                skill_file,
                source=str(raw_item.get("source", "local-cache")),
            )
            if item is None:
                unavailable_count += 1
                continue
        elif skill_file.is_file():
            item = dict(raw_item)
            item["path_available"] = True
        else:
            unavailable_count += 1
            continue
        available.append(item)
    return available, unavailable_count


def load_local_skill_index(path: Path, *, now: datetime | None = None) -> dict:
    if not path.is_file():
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "missing",
            "generated_at": None,
            "skills": [],
        }
    try:
        import json

        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "invalid",
            "generated_at": None,
            "skills": [],
        }
    if (
        isinstance(raw, dict)
        and raw.get("schema_version") == SCHEMA_VERSION
        and isinstance(raw.get("skills"), list)
    ):
        current_time = now or datetime.now(timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
        observed_at = _index_observed_at(raw.get("generated_at"))
        status = _index_status(observed_at, now=current_time)
        skills, unavailable_count = _validated_cached_skills(
            raw["skills"],
            refresh=observed_at is None,
            observed_at=observed_at,
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "status": status,
            "generated_at": raw.get("generated_at"),
            "skills": skills,
            "unavailable_skill_count": unavailable_count,
        }
    if isinstance(raw, dict):
        legacy_skills = []
        unavailable_count = 0
        for name, raw_path in raw.items():
            if not isinstance(raw_path, str):
                continue
            entry = read_skill_entry(Path(raw_path) / "SKILL.md", source="legacy-cache")
            if entry is None:
                unavailable_count += 1
                continue
            legacy_skills.append(entry)
        return {
            "schema_version": 1,
            "status": "legacy",
            "generated_at": None,
            "skills": legacy_skills,
            "unavailable_skill_count": unavailable_count,
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "invalid",
        "generated_at": None,
        "skills": [],
    }


def router_inputs(index: dict) -> tuple[list[dict], dict]:
    skills = [
        item
        for item in index.get("skills", [])
        if isinstance(item, dict) and item.get("path_available") is True
    ]
    metadata = {
        "status": str(index.get("status", "available")),
        "schema_version": index.get("schema_version"),
        "generated_at": index.get("generated_at"),
        "skill_count": len(skills),
        "unavailable_skill_count": int(index.get("unavailable_skill_count", 0)),
    }
    return skills, metadata
