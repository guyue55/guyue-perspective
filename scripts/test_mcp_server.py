#!/usr/bin/env python3
"""Focused safety, lifecycle, and GC tests for Guyue local memory."""

from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from scripts import memory_gc  # noqa: E402
from src import mcp_server  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_memory(
    symptom: str,
    root_cause: str,
    solution: str,
    tags: list[str],
    *,
    user_intent: str = "请记住这个已经验证的项目经验",
    scope: str | None = "project:alpha",
    review_after: str = "",
    supersedes: list[str] | None = None,
) -> str:
    kwargs = {
        "user_intent": user_intent,
        "review_after": review_after,
        "supersedes": supersedes,
    }
    if scope is not None:
        kwargs["scope"] = scope
    return mcp_server.guyue_write_memory(
        symptom,
        root_cause,
        solution,
        "Add a targeted regression check before the next release.",
        "Reproduced locally and verified by the focused test.",
        tags,
        **kwargs,
    )


def main() -> int:
    generic_route = json.loads(
        mcp_server.guyue_explain_route(
            "给当前项目做一个普通权限管理页面和后端接口。",
            limit=8,
        )
    )
    generic_names = {item["name"] for item in generic_route["selected"]}
    require(
        "static-demo-hardening" not in generic_names,
        "generic requests must not select context-gated workflows",
    )
    static_route = json.loads(
        mcp_server.guyue_explain_route(
            "继续加固报告导出。",
            context_markers=["static demo", "Demo/index.html"],
        )
    )
    require(
        static_route["selected"][0]["name"] == "static-demo-hardening",
        "MCP route explanations must honor explicit context markers",
    )
    require(
        "must contain" in mcp_server.guyue_explain_route("   "),
        "MCP route explanations must reject empty intent",
    )
    external_route = json.loads(mcp_server.guyue_explain_route("找工具"))
    require(
        external_route["lifecycle_state"] == "external_candidate"
        and external_route["external_candidates"][0]["name"] == "find-skills",
        "MCP route explanations must preserve external-only candidates",
    )

    originals = {
        "MEMORY_DIR": mcp_server.MEMORY_DIR,
        "ACTIVE_DIR": mcp_server.ACTIVE_DIR,
        "INDEX_FILE": mcp_server.INDEX_FILE,
        "CURATED_MEMORY_DIR": mcp_server.CURATED_MEMORY_DIR,
        "CURATED_INDEX_FILE": mcp_server.CURATED_INDEX_FILE,
        "LEGACY_MEMORY_DIR": mcp_server.LEGACY_MEMORY_DIR,
        "LEGACY_INDEX_FILE": mcp_server.LEGACY_INDEX_FILE,
    }

    with tempfile.TemporaryDirectory(prefix="guyue-mcp-test-") as temp_dir:
        root = Path(temp_dir)
        memory_dir = root / ".guyue" / "knowledge" / "memory"
        curated_dir = root / "skill" / "references" / "curated"
        legacy_dir = root / "legacy-install" / ".guyue_memory" / "local"
        mcp_server.MEMORY_DIR = memory_dir
        mcp_server.ACTIVE_DIR = memory_dir / "active"
        mcp_server.INDEX_FILE = memory_dir / "index.json"
        mcp_server.CURATED_MEMORY_DIR = curated_dir
        mcp_server.CURATED_INDEX_FILE = curated_dir / "index.json"
        mcp_server.LEGACY_MEMORY_DIR = legacy_dir
        mcp_server.LEGACY_INDEX_FILE = legacy_dir / "index.json"

        try:
            empty_result = mcp_server.guyue_read_memory("   ")
            require(
                "must contain" in empty_result, "empty memory queries must be rejected"
            )
            missing_scope = mcp_server.guyue_read_memory(
                "stale-artifact",
                scope="   ",
            )
            require(
                "scope" in missing_scope,
                "memory lookup must require an explicit scope",
            )
            invalid_limit = mcp_server.guyue_read_memory(
                "stale-artifact",
                scope="project:alpha",
                limit=0,
            )
            require(
                "between 1 and" in invalid_limit,
                "memory lookup must reject an invalid result limit",
            )

            missing_intent = write_memory(
                "A lesson was verified",
                "The write had no user authorization",
                "Require an explicit request",
                ["authorization"],
                user_intent="",
            )
            require(
                "explicit user request" in missing_intent,
                "memory writes without explicit user intent must be rejected",
            )
            negative_intent = write_memory(
                "A lesson was verified",
                "The user explicitly declined persistence",
                "Do not write the lesson",
                ["authorization"],
                user_intent="不要保存或记录这条经验",
            )
            require(
                "explicit user request" in negative_intent,
                "negative memory intent must be rejected",
            )
            ambiguous_scope = write_memory(
                "A lesson was verified",
                "The project identity was omitted",
                "Require a stable scope",
                ["scope"],
                scope="project",
            )
            require(
                "ambiguous memory scope" in ambiguous_scope,
                "new project memories must require a stable project scope",
            )
            require(
                not memory_dir.exists(),
                "unauthorized memory writes must not create storage files",
            )

            fake_credential = "sk" + "-" + "1234567890abcdefghijkl"
            secret_result = write_memory(
                "Provider request failed",
                f"The provider credential {fake_credential} was expired",
                "Rotate and redact the credential",
                ["provider"],
            )
            require(
                "Refused" in secret_result, "secret-bearing memory must be rejected"
            )
            require(
                not memory_dir.exists(), "rejected memory must not create storage files"
            )

            personal_path = "/" + "Users" + "/example/private-project/config.json"
            path_result = write_memory(
                "A local file was missing",
                f"The command depended on {personal_path}",
                "Use a repository-relative path",
                ["portability"],
            )
            require(
                "Refused" in path_result, "personal absolute paths must be rejected"
            )
            require(
                not memory_dir.exists(),
                "rejected path memory must not create storage files",
            )

            invalid_date = write_memory(
                "A valid-looking lesson had invalid lifecycle metadata",
                "The review date could not be parsed",
                "Validate metadata before writing",
                ["schema"],
                review_after="not-a-date",
            )
            require(
                "Refused invalid memory metadata" in invalid_date,
                "invalid review dates must be rejected",
            )
            require(
                not memory_dir.exists(),
                "invalid metadata must not create storage files",
            )

            first = write_memory(
                "The release page showed stale assets",
                "A previous development server was still running",
                "Restart the server and inspect the served HTML",
                ["release", "stale-artifact"],
                review_after="2000-01-01",
            )
            second = write_memory(
                "The theme script appeared missing",
                "The browser was connected to an old process",
                "Restart and compare the live artifact",
                ["theme", "stale-artifact"],
            )
            beta = write_memory(
                "A different project reused a stale artifact",
                "Beta had its own long-running process",
                "Restart Beta without changing Alpha",
                ["beta", "stale-artifact"],
                scope="project:beta",
            )
            user_preference = write_memory(
                "The user requested a reusable release check",
                "User preferences must not leak through a project expansion",
                "Query user memory with the user scope",
                ["user", "stale-artifact"],
                scope=None,
            )
            require(
                all(
                    "Successfully saved" in result
                    for result in (first, second, beta, user_preference)
                ),
                "explicitly requested memories must be stored",
            )
            require(
                "scope user" in user_preference,
                "write confirmation must disclose the default global scope",
            )

            index = json.loads(mcp_server.INDEX_FILE.read_text(encoding="utf-8"))
            require(
                index["schema_version"] == 2, "runtime index must use schema version 2"
            )
            filenames = [item["filename"] for item in index["memories"]]
            memory_ids = [item["id"] for item in index["memories"]]
            require(len(filenames) == 4, "four memory entries must be indexed")
            require(len(set(memory_ids)) == 4, "rapid writes must not collide")
            require(
                index["memories"][3]["scope"] == "user",
                "an unqualified explicit save must default to user-global scope",
            )
            require(
                all(filename.startswith("active/") for filename in filenames),
                "details must live under active/",
            )
            require(
                all(
                    {
                        "provenance",
                        "scope",
                        "evidence",
                        "confidence",
                        "status",
                        "supersedes",
                        "review_after",
                    }
                    <= set(item)
                    for item in index["memories"]
                ),
                "memory lifecycle metadata must be complete",
            )
            detail = (memory_dir / filenames[0]).read_text(encoding="utf-8")
            require("## Prevention" in detail, "memory detail must include prevention")

            third = write_memory(
                "The stale-process pattern recurred",
                "A long-running process served an older artifact",
                "Verify the process start time before changing source code",
                ["stale-artifact", "superseding"],
                supersedes=[memory_ids[1]],
            )
            require(
                "Successfully saved" in third,
                "a verified memory must supersede an older lesson",
            )
            index = json.loads(mcp_server.INDEX_FILE.read_text(encoding="utf-8"))
            require(
                index["memories"][1]["status"] == "superseded",
                "superseded memory status must be updated",
            )

            read_result = mcp_server.guyue_read_memory(
                "stale-artifact",
                scope="project:alpha",
            )
            read_entries = json.loads(read_result)
            require(
                len(read_entries) == 3,
                "project lookup must include current-project and user-global entries",
            )
            require(
                all(entry["source"] == "local" for entry in read_entries),
                "runtime results must identify their source",
            )
            require(
                [entry["scope"] for entry in read_entries]
                == ["project:alpha", "project:alpha", "user"],
                "project lookup must rank current-project entries before global entries",
            )
            require(
                all("detail" not in entry for entry in read_entries),
                "routine lookup must return summaries without Markdown details",
            )
            project_only_entries = json.loads(
                mcp_server.guyue_read_memory(
                    "stale-artifact",
                    scope="project:alpha",
                    include_user=False,
                )
            )
            require(
                len(project_only_entries) == 2
                and all(
                    entry["scope"] == "project:alpha"
                    for entry in project_only_entries
                ),
                "callers must be able to disable user-global enrichment",
            )
            global_entries = json.loads(
                mcp_server.guyue_read_memory("stale-artifact")
            )
            require(
                len(global_entries) == 1 and global_entries[0]["scope"] == "user",
                "unqualified lookup must default to user-global memory",
            )

            detail_entries = json.loads(
                mcp_server.guyue_read_memory(
                    "stale-artifact",
                    scope="project:alpha",
                    include_detail=True,
                )
            )
            require(
                all("## Root Cause" in entry["detail"] for entry in detail_entries),
                "detail lookup must return verified Markdown only when requested",
            )
            cross_project_entries = json.loads(
                mcp_server.guyue_read_memory(
                    "stale-artifact",
                    scope="project:alpha",
                    cross_project=True,
                )
            )
            require(
                {entry["scope"] for entry in cross_project_entries}
                == {"project:alpha", "project:beta", "user"},
                "cross-project lookup must require explicit opt-in",
            )
            require(
                [entry["scope"] for entry in cross_project_entries]
                == ["project:alpha", "project:alpha", "user", "project:beta"],
                "cross-project lookup must rank current project, then global, then others",
            )
            require(
                all("detail" not in entry for entry in cross_project_entries),
                "cross-project lookup must remain summary-only by default",
            )

            dry_run_dir = root / "dry-run-must-not-exist"
            changed, messages = memory_gc.run_gc(dry_run_dir, dry_run=True)
            require(changed == 0 and not messages, "empty dry-run must report no work")
            require(
                not dry_run_dir.exists(), "dry-run must not create storage directories"
            )

            changed, messages = memory_gc.run_gc(
                memory_dir,
                now=dt.datetime(2026, 7, 10, tzinfo=dt.timezone.utc),
            )
            require(
                changed == 1,
                f"one due memory must require review, got {changed}: {messages}",
            )
            index = json.loads(mcp_server.INDEX_FILE.read_text(encoding="utf-8"))
            review_entry = index["memories"][0]
            require(
                review_entry["status"] == "needs_review",
                "an expired review date must require review, not archive the lesson",
            )
            normalized_review = mcp_server.load_memory_index()["memories"][0]
            require(
                "review_reason" in normalized_review,
                "schema normalization must preserve lifecycle extension fields",
            )
            require(
                review_entry["filename"].startswith("active/"),
                "review-required memory must keep its active detail path",
            )
            require(
                (memory_dir / review_entry["filename"]).is_file(),
                "review-required memory must preserve the full detail file",
            )
            review_result = json.loads(
                mcp_server.guyue_read_memory(
                    "stale-artifact",
                    scope="project:alpha",
                    include_user=False,
                )
            )
            due_result = next(
                item for item in review_result if item["id"] == review_entry["id"]
            )
            require(
                due_result["requires_review"] is True,
                "lookup must disclose stale evidence instead of treating it as current",
            )

            future_index = root / "future-index.json"
            future_index.write_text(
                json.dumps({"schema_version": 99, "memories": []}),
                encoding="utf-8",
            )
            try:
                mcp_server.load_index(future_index)
            except ValueError:
                pass
            else:
                raise AssertionError("unknown future memory schema must fail safe")
        finally:
            for name, value in originals.items():
                setattr(mcp_server, name, value)

    print("MCP route and memory lifecycle tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
