"""Build and read Guyue's private, rebuildable local Skill discovery index."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml


SCHEMA_VERSION = 2
MAX_SKILL_READ_CHARS = 131_072
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


def load_local_skill_index(path: Path) -> dict:
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
        skills = [item for item in raw["skills"] if isinstance(item, dict)]
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "available",
            "generated_at": raw.get("generated_at"),
            "skills": skills,
        }
    if isinstance(raw, dict):
        legacy_skills = []
        for name, raw_path in raw.items():
            if not isinstance(raw_path, str):
                continue
            entry = read_skill_entry(Path(raw_path) / "SKILL.md", source="legacy-cache")
            if entry is None:
                entry = {
                    "name": str(name),
                    "path": raw_path,
                    "source": "legacy-cache",
                    "description": "",
                    "trigger_intent": [],
                    "search_text": str(name),
                    "alternate_paths": [],
                }
            legacy_skills.append(entry)
        return {
            "schema_version": 1,
            "status": "legacy",
            "generated_at": None,
            "skills": legacy_skills,
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "invalid",
        "generated_at": None,
        "skills": [],
    }


def router_inputs(index: dict) -> tuple[list[dict], dict]:
    skills = [item for item in index.get("skills", []) if isinstance(item, dict)]
    metadata = {
        "status": str(index.get("status", "available")),
        "schema_version": index.get("schema_version"),
        "generated_at": index.get("generated_at"),
        "skill_count": len(skills),
    }
    return skills, metadata
