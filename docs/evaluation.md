# Evaluation

Guyue is a workflow skill suite. Evaluation focuses on whether the agent follows the intended discipline, not whether it gives a single fixed answer.

## Local Evaluation Command

Run:

```bash
python3 scripts/run_eval.py
```

The evaluator checks `test-prompts.json` for:

- valid JSON structure;
- unique test names;
- non-empty user prompts;
- non-empty expected behavior;
- coverage for every registered skill in `skills_manifest.json`;
- coverage for the core safety disciplines: bounded trace logging, version-bound approval, calibrated research, controlled debugging, and memory write behavior.

It also validates `evals/behavior-contracts.json`. These machine-readable contracts separate expected routes, forbidden routes, required observable actions, forbidden side effects, and minimum evidence level. `run_eval.py` runs the deterministic route candidate check for every contract; that proves manifest routing consistency, not that a model already followed the required actions.

Inspect one route or the whole context budget with:

```bash
python3 scripts/try_guyue.py
python3 scripts/explain_route.py "<intent>" --context-marker "<project-marker>"
python3 scripts/check_context_budget.py --json
```

`try_guyue.py` is the public first-run proof. It composes the package receipt, route explanation, project-context exclusions, and context budget without model or network access, and explicitly marks runtime activation and model behavior as unverified. The budget gate measures discovery metadata, routing metadata, Unicode characters and UTF-8 bytes for the root entry, activated Skill bodies, and high-similarity route collisions.

Reviewed live observations can be checked with:

```bash
python3 scripts/check_behavior_replay.py <observations.json>
python3 scripts/check_behavior_replay.py <observations.json> --require-all
```

Each observation records the contract ID, observed routes/actions/side effects, evidence level, reviewer, observation time, evidence path, and SHA-256. The checker verifies the referenced file and rejects stale hashes. `scripts/test_suite.sh` checks every `evals/observations-*.json` file. Human labeling remains a judgment step; the script makes that judgment auditable rather than pretending to replace it.

The 2026-07-11 read-only route-audit replay is recorded in [`evals/evidence/route-audit-live-2026-07-11.md`](../evals/evidence/route-audit-live-2026-07-11.md) and bound by `evals/observations-2026-07-11.json`. The 2026-07-12 one-turn and multi-turn Long Goal Forge replays are recorded in [`evals/evidence/long-goal-forge-live-2026-07-12.md`](../evals/evidence/long-goal-forge-live-2026-07-12.md) and [`evals/evidence/long-goal-forge-multiturn-simulation-2026-07-12.md`](../evals/evidence/long-goal-forge-multiturn-simulation-2026-07-12.md), then bound by `evals/observations-2026-07-12.json`. These are partial contract observations; do not use them as `--require-all` evidence. A separate [`new-user-six-question-audit-2026-07-12.md`](../evals/evidence/new-user-six-question-audit-2026-07-12.md) checks public comprehensibility but does not replace runtime replay or package tests.

Use the full suite before a commit:

```bash
bash scripts/test_suite.sh
```

During development the validator includes unignored untracked files so new linked docs and scripts can be checked before staging. After staging the exact release candidate, run strict archive mode:

```bash
GUYUE_RELEASE_STRICT=1 bash scripts/test_suite.sh
```

Strict mode accepts only Git-indexed files as release payload; it should fail if a tracked document links to an untracked candidate file.

The 15-stage suite also runs `python3 scripts/check_full_install.py --self-test`, `python3 scripts/simulate_install_journey.py --json`, `python3 scripts/check_long_goal_pack.py --self-test`, `python3 scripts/simulate_long_goal_lifecycle.py --json`, official `claude plugin validate --strict .` when the Claude CLI is available, `python3 scripts/test_mcp_server.py`, `python3 scripts/test_codex_extractor.py`, `python3 scripts/test_skill_router.py`, `python3 scripts/test_context_budget.py`, `python3 scripts/test_try_guyue.py`, the real first-run command, `python3 scripts/check_behavior_replay.py --self-test`, and `python3 scripts/check_birth_certificate.py`. These verify the full-package payload, empty-HOME Git clone and restart identity, external-target Long Goal CLI, v2/v3 compatibility, v4 counterexamples and a continuous failure/recovery/seal/restart/mutation lifecycle, marketplace metadata, first-run truth, explainable route boundaries, context budgets, memory lifecycle safety, bounded session extraction, replay-evidence binding, public entrypoint, trigger surface, visible evidence links, safety boundaries, and current skill/prompt counts.

The routing stage also runs `python3 scripts/check_capability_chain.py --json`. Current deterministic routing, trigger, near-miss, collaboration, file-integrity, and schema defects always fail. Stale global activation receipts or incomplete all-Skill synthetic output evidence remain visible as warnings during ordinary development, with the corresponding model-activation and output-quality claims left `false`; this prevents a temporary quota or a changed global routing hash from forcing repetitive model calls merely to unblock local implementation. Release verification must run `python3 scripts/check_capability_chain.py --strict --json` (or set `GUYUE_RELEASE_STRICT=1`), where the same warnings become blocking errors. Never hand-edit or relabel a failed receipt to satisfy either mode.

The current contract covers 27 built-in Skills, 56 structural routing prompts, 26 behavior contracts, 12 collaboration contracts and 217 near-miss cases. The receipt separately reports arbitrary-input, real-user, cross-runtime and public-network boundaries; a green deterministic development result cannot silently promote those claims or a failed high-risk live replay.

Both live runners accept `--model <runtime-model-id>` or `GUYUE_EVAL_MODEL`. When the runtime exposes the Terra 5.6 alias, use that identifier for new agents; the receipt records the requested model. A model switch does not authorize extra retries or make old failed evidence pass.

For public Agent Skills frontmatter compatibility, run the official reference validator against every child skill and against a temporary root directory named `guyue`:

```bash
npx skills-ref validate skills/<skill-name>
npx skills-ref validate /tmp/<staging-root>/guyue
```

The repository checkout is named `guyue-skill`, while the installed root skill is named `guyue`; validate the installed/staged directory for the root name-to-directory rule.

## Current Test Categories

`test-prompts.json` currently covers:

- root orchestration;
- 长线目标铸造、逐项澄清、一行交接、long Goal intake、execution-ledger recovery、stale-evidence refusal；
- debugging discipline;
- system design and human confirmation;
- documentation;
- business-readable output;
- research and sourcing;
- coding discipline, reuse-first engineering, and development defaults;
- loop engineering and dynamic workflow routing;
- frontend expert behavior;
- frontend design ecosystem boundaries;
- SOP generation;
- memory bank;
- product sense;
- skill crafting;
- ecosystem scout;
- security gate;
- server-side permission boundary review;
- website reconstruction;
- software advising;
- UI taste review;
- code minimalism and duplicate-code reduction;
- book distillation;
- video extraction;
- video creation and short-drama stage gates;
- context compression, context budget management, and third-party quick-install gates;
- reality auditing;
- NexusFlow governance workflow;
- static demo hardening;
- AI cost and Grounding measurement.

`ecosystem-scout` must stay covered because it controls external dependency intake.

## Pass Criteria

A release candidate passes evaluation when:

- every prompt has an expected behavior statement;
- each registered skill has at least one matching test prompt or explicit manifest coverage;
- safety-related tests require a pause, refusal, confirmation, or source check where relevant;
- vague long-goal replay inspects project evidence before asking exactly one direction-changing question, while urgency cannot force a premature handoff;
- decision-open long-goal replay uses only targeted reads and a lightweight status probe; it does not run the full suite, security scan, installation, build, or live replay unless that evidence is necessary for the current decision or a safety risk;
- ready long-goal replay creates or identifies the version-4 control pack, separates ultimate vision/current Goal/time-only outcomes, records verified facts/frozen decisions/falsifiable hypotheses/experiments, proves a vertical risk slice before scale, explicitly lists every phase-plan file, maps every promise bidirectionally to a stage and evidence ID, classifies side-effect replay, binds high-risk approval to an action version, defines delegation ownership/BASE/report/review/convergence budgets, passes the checker with an explicit target repository root, and returns one physical handoff line without unresolved questions;
- complete long-goal validation requires every phase to be complete, separates `FINAL` evidence from historical `ATTEMPT` evidence, verifies artifact SHA-256/provenance/freshness, and proves the direct A implementation -> B evidence -> C master-and-ledger Git seal while allowing unrelated descendant commits and rejecting post-seal evidence mutation;
- the full `bash scripts/test_suite.sh` exits with status code `0`;
- `scripts/check_birth_certificate.py` confirms the public release assets are present and synchronized;
- `scripts/check_full_install.py --self-test` rejects a root-only install and accepts the complete repository payload;
- `scripts/test_guyue_paths.py` proves private data is owned by `GUYUE_HOME`, discovery data is cache, and legacy install paths remain read-only;
- `scripts/test_memory_concurrency.py` proves concurrent index writers do not lose rows;
- `scripts/test_memory_migration.py` proves explicit planning, idempotent migration, hash verification, sensitive-data blocking, and rollback;
- `scripts/test_release_payload.py` proves payload hash tampering and legacy private-state leakage are rejected;
- `scripts/test_mcp_server.py` proves explainable project-context routing plus public/private memory separation, real detail retrieval, schema-v2 lifecycle metadata, secret rejection, supersession, `needs_review`, and zero-side-effect dry-run;
- `scripts/test_codex_extractor.py` proves user/final extraction excludes developer/tool payloads, redacts common secrets and personal home roots, and enforces cwd/time-window/thread-source/keyword/deduplication/inventory filters;
- `scripts/test_context_budget.py` proves Unicode characters are not confused with UTF-8 bytes and rejects overlong descriptions, missing bodies, and route collisions;
- all child skills pass the official `skills-ref` validator, and the root passes when staged under its install name `guyue`;
- the report does not contain missing skills or duplicate prompt names.

## Dry Run Versus Live Run

`scripts/run_eval.py` is a structural evaluator. It does not call an LLM and does not prove output quality by itself.

Live evaluation means replaying the prompts in a real agent session and saving the observed outputs under `examples/` or a release report. Mark structural checks as `dry_run`; mark real agent replay results as `live_run`.

For evidence mining from existing Codex sessions, use the bounded extractor instead of reading raw rollout files into context:

```bash
python3 scripts/codex_extractor.py <jsonl-or-session-dir> \
  --cwd <project-root> --since <YYYY-MM-DD> --until <YYYY-MM-DD> \
  --thread-source user,subagent --roles user,final \
  --keyword <term> --dedupe --inventory --stats --format json
```

The extractor streams JSONL, ignores system/developer/tool payloads, marks the last assistant message of a completed turn as `final`, truncates each message, and redacts common credential and personal-home patterns. Its output remains local evidence and must be reviewed before publication.

## Live Replay Evidence

Current quickstart replay evidence lives in [../examples/quickstart-output.md](../examples/quickstart-output.md).

Use a read-only runtime when collecting replay output:

```bash
codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-replay-root.md "<prompt>"
```

Record both passes and deviations. For example, if the runtime follows Guyue's debugging trace but still emits concrete retry code before raw logs are available, mark it as `partial_pass` and convert it into a follow-up boundary fix.

Security-gate live runs must be strict about target admission: if the prompt says only "this third-party skill" but provides no path, URL, package name, or archive path, the correct result is to ask for the target and stop. Inferring a local skill directory is a replay deviation and must be fixed before release.

Runtime-entrypoint changes must also confirm that the agent no longer reports missing project instruction files such as `RTK.md`. Record that result in the live replay evidence.

Runtime adapter changes must follow [runtime-adapters.md](runtime-adapters.md):

- keep adapters thin and point them back to `RTK.md`;
- run the local validation suite;
- run a read-only live replay in the target runtime when feasible;
- remove the adapter before commit if the runtime does not load it or if it creates duplicated/conflicting instructions.

## Release Evidence Template

Current release lineage is tracked in [release-v1.6.0.md](release-v1.6.0.md), while the reusable release gates and remaining boundaries live in [release-checklist.md](release-checklist.md). Update both before a release tag or marketplace submission.

Use this template when preparing a release:

```markdown
## Evaluation Evidence

- Date:
- Commit:
- Command: `bash scripts/test_suite.sh`
- Result:
- Live prompts replayed:
- Deviations:
- Follow-up fixes:
```
