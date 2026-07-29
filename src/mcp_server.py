import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

try:
    from src.memory_store import (
        CONFIDENCE_LEVELS,
        SCHEMA_VERSION,
        default_review_after,
        find_sensitive_memory_content,
        index_lock,
        isoformat,
        legacy_runtime_memory_dir,
        legacy_runtime_memory_dirs,
        load_index,
        new_memory_id,
        runtime_memory_dir,
        safe_detail_path,
        utc_now,
        validate_entry,
        write_index_atomic,
        write_text_atomic,
    )
    from src.local_skill_index import load_local_skill_index, router_inputs
    from src.paths import discovery_cache_file
    from src.skill_router import resolve_routes
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from memory_store import (  # type: ignore[no-redef]
        CONFIDENCE_LEVELS,
        SCHEMA_VERSION,
        default_review_after,
        find_sensitive_memory_content,
        index_lock,
        isoformat,
        legacy_runtime_memory_dir,
        legacy_runtime_memory_dirs,
        load_index,
        new_memory_id,
        runtime_memory_dir,
        safe_detail_path,
        utc_now,
        validate_entry,
        write_index_atomic,
        write_text_atomic,
    )
    from local_skill_index import (  # type: ignore[no-redef]
        load_local_skill_index,
        router_inputs,
    )
    from paths import discovery_cache_file  # type: ignore[no-redef]
    from skill_router import resolve_routes  # type: ignore[no-redef]


mcp = FastMCP("guyue")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CURATED_MEMORY_DIR = WORKSPACE_ROOT / "skills" / "memory-bank" / "references" / "curated"
CURATED_INDEX_FILE = CURATED_MEMORY_DIR / "index.json"
MEMORY_DIR = runtime_memory_dir(WORKSPACE_ROOT)
ACTIVE_DIR = MEMORY_DIR / "active"
INDEX_FILE = MEMORY_DIR / "index.json"
LEGACY_MEMORY_DIR = legacy_runtime_memory_dir(WORKSPACE_ROOT)
LEGACY_INDEX_FILE = LEGACY_MEMORY_DIR / "index.json"
LEGACY_MEMORY_DIRS = legacy_runtime_memory_dirs(WORKSPACE_ROOT)
MANIFEST_FILE = WORKSPACE_ROOT / "skills_manifest.json"
MAX_MEMORY_RESULTS = 20
MAX_MEMORY_DETAIL_BYTES = 64 * 1024

def load_memory_index() -> dict:
    """Load the private runtime index, normalizing legacy rows if encountered."""
    return load_index(INDEX_FILE)


def load_search_indexes() -> list[tuple[str, Path, dict]]:
    indexes: list[tuple[str, Path, dict]] = []
    if CURATED_INDEX_FILE.exists():
        indexes.append(("curated", CURATED_MEMORY_DIR, load_index(CURATED_INDEX_FILE)))
    if INDEX_FILE.exists():
        indexes.append(("local", MEMORY_DIR, load_index(INDEX_FILE)))
    for position, legacy_dir in enumerate(LEGACY_MEMORY_DIRS):
        legacy_index = legacy_dir / "index.json"
        if legacy_index.exists() and legacy_index != INDEX_FILE:
            source = "legacy-local" if position == 0 else "legacy-root"
            indexes.append((source, legacy_dir, load_index(legacy_index)))
    for source, _, index in indexes:
        for entry in index.get("memories", []):
            errors = validate_entry(entry)
            if errors:
                raise ValueError(
                    f"invalid {source} memory {entry.get('id', '<unknown>')}: {'; '.join(errors)}"
                )
    return indexes


def read_memory_detail(memory_dir: Path, entry: dict) -> str:
    detail_path = safe_detail_path(memory_dir, str(entry.get("filename", "")))
    if not detail_path.is_file():
        raise ValueError(f"missing memory detail: {entry.get('filename', '')}")
    if detail_path.stat().st_size > MAX_MEMORY_DETAIL_BYTES:
        raise ValueError(f"memory detail exceeds {MAX_MEMORY_DETAIL_BYTES} bytes")
    return detail_path.read_text(encoding="utf-8")


@mcp.tool()
def guyue_list_skills() -> str:
    """Read skills_manifest.json to report available skills."""
    if not MANIFEST_FILE.exists():
        return "skills_manifest.json not found. Ensure you are running in the guyue workspace."
    return MANIFEST_FILE.read_text(encoding="utf-8")


@mcp.tool()
def guyue_explain_route(
    intent: str,
    context_markers: list[str] | None = None,
    limit: int = 5,
) -> str:
    """Rank Skill candidates and explain matches, exclusions, and context gates."""
    if not MANIFEST_FILE.exists():
        return "skills_manifest.json not found. Ensure you are running in the guyue workspace."
    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        local_capabilities, local_catalog = router_inputs(
            load_local_skill_index(discovery_cache_file())
        )
        decision = resolve_routes(
            manifest,
            intent,
            context_markers=context_markers,
            local_capabilities=local_capabilities,
            local_catalog=local_catalog,
            limit=limit,
        )
    except json.JSONDecodeError:
        return "Failed to parse skills_manifest.json."
    except ValueError as exc:
        return f"Route request rejected: {exc}"
    return json.dumps(decision, ensure_ascii=False, indent=2)


@mcp.tool()
def guyue_read_memory(query: str) -> str:
    """Return active curated or local memories matching a keyword query."""
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return "Memory query must contain a non-whitespace keyword."

    try:
        indexes = load_search_indexes()
    except (json.JSONDecodeError, ValueError):
        return "Failed to parse memory index."
    if not indexes:
        return "No memory bank index found."

    results = []
    seen_ids: set[str] = set()
    for source, memory_dir, index in indexes:
        for memory in index.get("memories", []):
            if memory.get("status") not in {"active", "needs_review"}:
                continue
            memory_id = str(memory.get("id", ""))
            if memory_id in seen_ids:
                continue
            searchable = " ".join(
                [
                    *memory.get("tags", []),
                    str(memory.get("summary", "")),
                    str(memory.get("scope", "")),
                    str(memory.get("evidence", "")),
                ]
            ).casefold()
            if normalized_query in searchable:
                try:
                    detail = read_memory_detail(memory_dir, memory)
                except (OSError, UnicodeError, ValueError) as exc:
                    return f"Failed to read memory detail for {memory_id}: {exc}"
                results.append(
                    {
                        **memory,
                        "source": source,
                        "requires_review": memory.get("status") == "needs_review",
                        "detail": detail,
                    }
                )
                seen_ids.add(memory_id)
                if len(results) >= MAX_MEMORY_RESULTS:
                    return json.dumps(results, ensure_ascii=False, indent=2)

    if not results:
        return f"No memories found for query: {query}"
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def guyue_write_memory(
    symptom: str,
    root_cause: str,
    solution: str,
    prevention: str,
    evidence: str,
    tags: list[str],
    provenance: str = "current verified task",
    scope: str = "project",
    confidence: str = "high",
    review_after: str = "",
    supersedes: list[str] | None = None,
) -> str:
    """Write a verified lesson to private, versioned local memory storage."""
    normalized_tags = [str(tag).strip() for tag in (tags or []) if str(tag).strip()]
    normalized_supersedes = [
        str(memory_id).strip()
        for memory_id in (supersedes or [])
        if str(memory_id).strip()
    ]
    values = [
        symptom,
        root_cause,
        solution,
        prevention,
        evidence,
        provenance,
        scope,
        *normalized_tags,
        *normalized_supersedes,
    ]
    sensitive_label = find_sensitive_memory_content(values)
    if sensitive_label:
        return f"Refused to store memory containing {sensitive_label}. Redact it and try again."
    if not all(
        str(value).strip()
        for value in (
            symptom,
            root_cause,
            solution,
            prevention,
            evidence,
            provenance,
            scope,
        )
    ):
        return "Refused to store incomplete memory. Symptom, root cause, solution, prevention, evidence, provenance, and scope are required."
    if confidence not in CONFIDENCE_LEVELS:
        return (
            "Refused to store memory with invalid confidence; use low, medium, or high."
        )

    now = utc_now()
    memory_id = new_memory_id(now)
    timestamp = isoformat(now)
    review_date = review_after.strip() or default_review_after(now)
    filename = f"active/{memory_id.lower()}.md"
    entry = {
        "schema_version": SCHEMA_VERSION,
        "id": memory_id,
        "filename": filename,
        "tags": normalized_tags,
        "summary": root_cause[:160] + ("..." if len(root_cause) > 160 else ""),
        "timestamp": timestamp,
        "provenance": provenance.strip(),
        "scope": scope.strip(),
        "evidence": evidence.strip(),
        "confidence": confidence,
        "status": "active",
        "supersedes": normalized_supersedes,
        "review_after": review_date,
    }
    validation_errors = validate_entry(entry)
    if validation_errors:
        return "Refused invalid memory metadata: " + "; ".join(validation_errors)

    filepath = safe_detail_path(MEMORY_DIR, filename)
    detail = (
        f"# Memory {memory_id}\n\n"
        f"- Timestamp: {timestamp}\n"
        f"- Provenance: {provenance.strip()}\n"
        f"- Scope: {scope.strip()}\n"
        f"- Evidence: {evidence.strip()}\n"
        f"- Confidence: {confidence}\n"
        f"- Review After: {review_date}\n\n"
        f"## Symptom\n{symptom.strip()}\n\n"
        f"## Root Cause\n{root_cause.strip()}\n\n"
        f"## Solution\n{solution.strip()}\n\n"
        f"## Prevention\n{prevention.strip()}\n"
    )
    try:
        with index_lock(INDEX_FILE):
            try:
                index_data = load_memory_index()
            except (json.JSONDecodeError, ValueError) as exc:
                return f"Refused to write because the private memory index is invalid: {exc}"
            existing_ids = {item.get("id") for item in index_data.get("memories", [])}
            unknown_superseded = set(normalized_supersedes) - existing_ids
            if unknown_superseded:
                return "Refused unknown supersedes IDs: " + ", ".join(
                    sorted(unknown_superseded)
                )
            if memory_id in existing_ids:
                return f"Refused duplicate memory ID: {memory_id}"
            if filepath.exists():
                return f"Refused existing unindexed memory detail: {filename}"
            for item in index_data.get("memories", []):
                if item.get("id") in normalized_supersedes:
                    item["status"] = "superseded"
            index_data.setdefault("memories", []).append(entry)
            index_data["schema_version"] = SCHEMA_VERSION
            write_text_atomic(filepath, detail)
            try:
                write_index_atomic(INDEX_FILE, index_data)
            except OSError:
                filepath.unlink(missing_ok=True)
                raise
    except (OSError, TimeoutError) as exc:
        return f"Failed to save private memory safely: {exc}"
    return f"Successfully saved private memory {memory_id} to {filename}."


if __name__ == "__main__":
    mcp.run()
