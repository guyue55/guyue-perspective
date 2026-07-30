# Installation

This document keeps installation paths explicit. Use the path that matches your agent runtime, then run the local verification command before relying on the skill.

## 30-Second Read-Only Proof

From the repository root, verify the package and deterministic router before installing dependencies or connecting a model:

```bash
python3 scripts/try_guyue.py
python3 scripts/try_guyue.py --json
```

The command reads the full-package receipt, route manifest, project-context gates, and context budget. It does not write files, access the network, install dependencies, or call a model. A pass proves that the local package and deterministic route evidence are coherent; it does not prove that a target runtime discovered or activated Guyue.

## Verify The Development Environment

From the repository root:

```bash
python3 scripts/install_guyue.py
bash scripts/test_suite.sh
```

This installs the small validation/runtime dependency set, prints a dry-run plan for optional enhancement skills from `skills_manifest.json`, runs the dependency doctor, then runs the zero-leakage scanner, SKILL.md validator, MCP tests, and test prompt evaluator. The default command does not download or link third-party skills.

## Full-Package Contract

Guyue is one root orchestrator with repository-local principles, routed modules, scripts, docs, and optional MCP support. A complete installation must preserve the whole repository tree under one runtime skill directory.

Do not use `npx skills add guyue55/guyue-skill` as a full installation path. Current generic Skills CLI behavior intentionally installs only a root-level `SKILL.md`; the resulting directory omits files that the Guyue entrypoint references. Clone the repository, then link or copy that checkout into the skill directory supported by your runtime.

Verify the mounted directory itself before relying on it:

```bash
python3 /path/to/guyue/scripts/check_full_install.py /path/to/guyue
python3 /path/to/guyue/scripts/check_full_install.py /path/to/guyue --runtime codex --json
```

The JSON form is a local install receipt: package version, routed Skill count, runtime-specific required files, source commit when available, dirty-worktree state, and a SHA-256 over the required payload. Save or attach it to release evidence when needed; a complete receipt proves payload presence, not behavioral activation.

## Optional Enhancement Skills

Guyue can discover optional third-party skills listed in `skills_manifest.json`, but optional dependencies are not required for the core skill to run.

The default installer only plans optional dependency changes:

```bash
python3 scripts/install_guyue.py
```

It scans the manifest and local skill roots, reports what is already present, and prints proposed actions without cloning, downloading, or linking anything.

Use the lower-level planner when you want to preview or audit optional skill changes before touching local skill directories:

```bash
python3 scripts/install_optional_dependencies.py
```

The default mode is a dry run. It scans local skill roots first, verifies that an existing Skill comes from the reviewed origin and exact commit recorded in the manifest, and prints the actions it would take without cloning or linking anything. A directory merely existing no longer counts as verified installation.

To install green optional skills after reviewing the plan, while stopping on yellow/red findings:

```bash
python3 scripts/install_guyue.py --optional-mode safe
```

Some optional skills contain shell helpers, command execution examples, or project layouts that are not a single `SKILL.md` directory. Only after reviewing those findings should you explicitly allow every declared dependency:

```bash
python3 scripts/install_guyue.py --optional-mode all
```

The installer keeps third-party source checkouts under:

```text
~/.cc-switch/skills/_sources
```

Then it creates links from `~/.cc-switch/skills/<skill-name>` and `~/.codex/skills/<skill-name>` back to the single source location. This avoids multiple editable copies drifting apart.

## Codex

Codex discovers local skills from configured skill roots. Use your local checkout path as the source:

```text
/path/to/guyue
```

For a portable setup, link or copy the repository into your local Codex skills directory and restart the prompt session:

```bash
ln -s /path/to/guyue ~/.codex/skills/guyue
```

Use a fresh Codex turn to confirm that the `guyue` root skill appears and can resolve routed files such as `skills/coding-discipline/SKILL.md`, `skills/debugging-mindset/SKILL.md`, and `skills/frontend-expert/SKILL.md`. Do not assume every runtime advertises repository-local routed modules as separate top-level skills.

This repository also includes a minimal `AGENTS.md` and `RTK.md` for coding-agent runtime guidance. They are adapters, not public Skill standards:

- `SKILL.md` remains the public Skill entrypoint.
- `README.md` remains the human-facing entrypoint.
- `AGENTS.md` tells compatible coding agents to read `RTK.md`.
- `RTK.md` defines the local source-of-truth order, verification gates, and safety boundaries.

Cross-runtime adapter policy lives in [runtime-adapters.md](runtime-adapters.md). Do not add active `CLAUDE.md`, `GEMINI.md`, Copilot, or Cursor adapter files until that runtime has a real user path and a read-only live replay.

For a quick runtime check:

```bash
codex exec --ephemeral -C <repo-root> --sandbox read-only "使用古月的思路评估这个需求：我们要加一个支付模块。只分析，不写代码。"
```

## Claude Code

Use the repository's validated marketplace manifest for a complete plugin install:

```bash
claude plugin marketplace add guyue55/guyue-skill
claude plugin install guyue@guyue
claude plugin details guyue@guyue
```

Before publication, `claude plugin validate --strict .` and an isolated local marketplace install must pass. After the candidate is pushed, repeat the same install from the public GitHub source before tagging the release.

The source checkout path remains available when you want to develop or customize Guyue:

```bash
git clone https://github.com/guyue55/guyue-skill.git /path/to/guyue
```

Then start a new Claude Code session and trigger it with:

```text
使用古月的思路帮我分析这个需求，先别写代码。
```

Claude Code has its own project memory conventions. If you need persistent Claude-specific guidance, mirror the small runtime-entrypoint summary into `CLAUDE.md` instead of assuming Claude will load `AGENTS.md` or `RTK.md`.

When adding `CLAUDE.md`, keep it as a thin adapter to `RTK.md`; do not copy the full runtime rules.

## MCP Clients

Use the optional MCP server when you want the agent to read the skill manifest, explain candidate routes without loading every Skill body, or use the local memory bank through tools. Guyue's public Skill behavior does not depend on MCP. The exposed route tool is `guyue_explain_route`; it returns match and rejection evidence but does not execute a Skill.

```json
{
  "mcpServers": {
    "guyue": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]>=1.0.0,<2.0.0",
        "--with",
        "PyYAML>=6.0,<7.0",
        "mcp_server.py"
      ],
      "cwd": "/path/to/guyue/src"
    }
  }
}
```

Replace `/path/to/guyue/src` with the absolute path to your checkout's `src` directory.
The version range keeps the documented FastMCP v1 import contract stable; the YAML dependency is required by Guyue's route index loader.

Private memory writes require the current user request to explicitly say to remember, save, or record the lesson. Callers must pass that request as `user_intent`. An unqualified save defaults to the cross-project `user` scope; an explicitly project-only request must use `project:<stable-project-id>`. Reads without a project scope use `user`; project reads rank the current project before `user`, and `include_user=false` disables that enrichment. Set `cross_project=true` or `include_detail=true` only for the corresponding explicit need.

## Private Data And Migration

Guyue keeps installable code and private runtime data separate:

```text
~/.guyue/
├── knowledge/memory/   # verified private lessons
├── cache/discovery/    # rebuildable local Skill paths
└── state/migrations/   # sanitized migration receipts
```

These subdirectories are created lazily. In particular, `knowledge/memory/` is absent until the first explicitly authorized memory write succeeds; an installation with only `cache/discovery/` is normal and does not mean memory support is broken.

Set `GUYUE_HOME` when you need a portable or policy-controlled root. `GUYUE_MEMORY_DIR` remains supported only as a memory-specific compatibility override. Public curated knowledge stays inside the active Skill package and is not copied into HOME.

Older installations may contain `.guyue_memory/local/`, while the earliest releases wrote runtime entries directly under `.guyue_memory/`. The new runtime can read both layouts but never writes to either. Inspect and migrate explicitly; use `--legacy-dir /path/to/old/.guyue_memory` when migrating an early installation from a different checkout:

```bash
python3 scripts/migrate_guyue_data.py plan
python3 scripts/migrate_guyue_data.py migrate
python3 scripts/migrate_guyue_data.py verify --receipt <receipt.json>
```

Migration refuses damaged, conflicting, or sensitive entries. It preserves the legacy source and writes a receipt that can be used with `rollback`. Do not delete the legacy directory until verification and a later backup are complete.

Do not symlink the complete `~/.guyue` directory into a project. That would expose global private state to project-scoped tools and increase accidental commit, backup, and cross-project access risk. Configure `GUYUE_HOME` only when a managed external location is required.

The installation payload is governed by `release-manifest.json` and hash-bound by `release-payload.lock.json`. Verify it with:

```bash
python3 scripts/check_full_install.py --runtime codex --json
```

## VS Code And GitHub Copilot

Agent Skills are directory-based. The skill directory must contain `SKILL.md`, and the frontmatter `name` should match the directory name. For a workspace-level setup, copy or link this repository into the workspace skill directory supported by your VS Code/Copilot configuration.

After installation, review `SKILL.md` before enabling script execution. Keep terminal auto-approval narrow and avoid broad shell allow-lists.

GitHub Copilot and Cursor have their own repository instruction mechanisms. Keep `SKILL.md` as the canonical Skill asset and only copy the runtime-entrypoint summary into those tool-specific instruction files when needed.

If a Copilot or Cursor adapter is added, it must pass the adapter admission gate in [runtime-adapters.md](runtime-adapters.md).

## OpenClaw

For a local install:

```bash
openclaw skills install /path/to/guyue --as guyue
```

Before installing any third-party dependency suggested by `ecosystem-scout`, inspect its `SKILL.md`, source repository, and security scan results. Do not install unknown skills globally until they have been reviewed.

## First Run Prompt

Use this prompt to verify behavior without touching project files:

```text
使用古月的思路评估这个需求：我们要加一个支付模块。只做需求边界和风险分析，不写代码。
```

Expected behavior:

- The agent respects the explicit read-only boundary and inspects available project evidence before making claims.
- The agent routes to requirement-analysis or system-design concerns; it uses external research only when an unstable, unfamiliar, high-stakes, explicitly requested, or decision-critical fact remains.
- If one unresolved decision would change the direction, it asks only that highest-impact question. It does not invent missing facts or demand duplicate approval for already bounded reversible work.
