# Security Boundaries

Guyue is designed to reduce agent risk, not to bypass human approval. Treat every skill, script, MCP server, and external dependency as part of the agentic supply chain.

## Non-Negotiable Boundaries

- Do not execute unknown installation scripts from a third-party repository.
- Do not copy third-party README files or source trees into `skills/` just to make the agent "know more".
- Do not store API keys, tokens, cookies, private SSH keys, or personal account details in examples, tests, or docs.
- Do not ship private runtime memory in public source packages. Curated knowledge lives with the owning Skill under `skills/*/references/`; private knowledge lives under `GUYUE_HOME` (default `~/.guyue`) and legacy `.guyue_memory/**` is always excluded.
- Do not publish, tag, push to a marketplace, or deploy without an explicit user command.
- Do not let an agent rewrite `SKILL.md` or `skills_manifest.json` from a vague suggestion; require a visible proposal and approval.

## External Skill Intake

`ecosystem-scout` exists to keep external tool intake lightweight and reviewable.

Required flow:

1. Search for the tool or skill and at least one comparable alternative.
2. Produce a short evaluation artifact that explains the use case, dependency cost, risks, and fit.
3. Stop for approval.
4. If approved, register only a lightweight dependency pointer in `skills_manifest.json`.

Allowed registry fields:

```json
{
  "name": "tool-name",
  "description": "short purpose",
  "package_id": "owner/repo-or-unique-id",
  "command": "install command",
  "url": "official source"
}
```

Do not import the whole external skill into this repository unless the user explicitly asks for vendoring and accepts the maintenance burden.

## MCP And Script Execution

MCP servers and scripts can expose local files, shell commands, credentials, and network access. Keep them scoped.

- Prefer workspace-level installs over global installs.
- Prefer read-only tools unless write access is required.
- Review every new script before adding it to `scripts/`.
- Keep script dependencies explicit and minimal.
- Run `python3 scripts/security_scanner.py` before every commit.
- `scripts/run_security_scan.py` scans every eligible text file and reports `scanned/total`; a truncated or unreadable target cannot receive Green. Green means only that the built-in local heuristics found no match, not that the dependency is supply-chain safe.
- Optional external dependencies are fetched at the reviewed commit recorded in `skills_manifest.json`; a missing or mismatched ref blocks linking until it is reviewed again.
- The scanner covers tracked files plus unignored untracked files, so newly generated control packs and release assets are checked before staging. Git-ignored local material remains outside the release scan.
- `guyue_read_memory` rejects empty queries and scopes, caps routine results at 5 summaries, and does not read Markdown details unless `include_detail=true`. The default scope is `user`; a project query ranks its exact scope before `user`, while `include_user=false` suppresses global enrichment. `cross_project=true` is required before other project scopes participate. `needs_review` results are disclosed as stale evidence.
- `guyue_write_memory` refuses missing or negative `user_intent`. Unqualified writes default to `user`; explicitly project-only writes require `project:<stable-project-id>` rather than a shared `project` bucket. It also rejects common API keys, bearer tokens, provider credentials, and personal absolute paths before creating storage files. Valid writes require provenance, scope, evidence, confidence, lifecycle status, prevention, and review timing, and go to user-owned private storage. This is a narrow local guard, not a complete secret detector; callers must still redact logs and account data before writing memory.
- Memory index mutations use a recoverable exclusive lock, temporary files, `fsync`, and atomic replacement. A corrupt index, lock timeout, or conflicting migration blocks the write instead of resetting or overwriting data.
- Legacy migration is explicit and receipt-backed. `plan` and `doctor` are read-only; `migrate` preserves the old source; `verify` checks IDs and hashes; `rollback` refuses if migrated content changed.
- `release-manifest.json` and `release-payload.lock.json` define and hash the installable payload. `.gitattributes` remains a second boundary, not a separate authority.

## Approval Points

The agent must stop before:

- Deleting files or directories.
- Installing external skills globally.
- Running unknown shell commands copied from a website.
- Writing credentials or environment files.
- Pushing code, creating releases, publishing packages, or submitting marketplace entries.
- Changing the public positioning of the project in a way that implies the skill is a full autonomous person.

## Commit Gate

Before committing:

```bash
python3 scripts/security_scanner.py
ruff check scripts src
python3 scripts/test_codex_extractor.py
python3 scripts/test_mcp_server.py
python3 scripts/test_guyue_paths.py
python3 scripts/test_memory_concurrency.py
python3 scripts/test_memory_migration.py
python3 scripts/check_behavior_replay.py --self-test
python3 scripts/doctor.py
python3 scripts/ci_validate_skills.py
python3 scripts/run_eval.py
```

`scripts/test_suite.sh` runs the same gate as a single command.
