# Release Checklist

Release only when installation, verification, safety, and examples are understandable to a new user.

## v1.60 Release Evidence

Date: 2026-07-21
Candidate version: `1.60`
Base tag: `v1.5.1`

- [x] The former private static-demo Skill wording is renamed to `static-demo-hardening`.
- [x] Current release files use anonymous static-demo surface wording.
- [x] Previous release-note and old candidate-lineage files are removed from the current payload.
- [x] The exact payload lock is rebuilt after the release metadata and documentation changes.
- [x] The complete local suite passes.
- [x] Ruff runs with `--no-cache`.
- [x] Diff whitespace, generated-cache, zero-leakage, full-install, and static-demo routing proofs pass.
- [x] A custom residue scan over the repository and ignored local worktree copy reports `findings=0`.

## Reusable Release Gate

## Positioning

- [ ] README says Guyue is a Personal Agent Operating Layer, not a complete autonomous person.
- [ ] README explains who should use it and why they should install it instead of asking an agent ad hoc.
- [ ] README links to installation, security, and evaluation docs.
- [ ] Skill count is consistent across `README.md`, `skills_manifest.json`, and `skills/`.

## Installation

- [ ] `docs/installation.md` covers Codex.
- [ ] `docs/installation.md` covers Claude Code.
- [ ] `docs/installation.md` covers MCP clients.
- [ ] `docs/installation.md` covers VS Code/Copilot-style Agent Skills.
- [ ] `docs/installation.md` covers OpenClaw local install.
- [ ] Installation preserves the full repository payload; do not approve a root-only generic CLI copy as a complete Guyue install.
- [ ] Default optional dependency handling is plan-only; networked third-party installation requires explicit mode selection.
- [ ] `docs/runtime-adapters.md` is current before adding or changing runtime-specific adapter files.
- [ ] `python3 scripts/try_guyue.py` passes before runtime installation and states that deterministic proof is not activation proof.

## Verification

- [ ] Current deterministic contract contains 60 structural prompts; update this count whenever `test-prompts.json` changes.
- [ ] `python3 scripts/security_scanner.py` passes.
- [ ] `python3 scripts/doctor.py` passes.
- [ ] `python3 scripts/ci_validate_skills.py` passes.
- [ ] `python3 scripts/run_eval.py` passes.
- [ ] `python3 scripts/test_skill_router.py` passes all positive/negative route contracts.
- [ ] `python3 scripts/check_capability_chain.py --json` has no errors; strict live-evidence refresh is required before claiming new all-runtime model behavior.
- [ ] `python3 scripts/test_context_budget.py` and `python3 scripts/check_context_budget.py` pass without budget or collision errors.
- [ ] `python3 scripts/test_try_guyue.py` passes and the JSON proof reports a complete payload with at least one evidence-backed route.
- [ ] `python3 scripts/check_birth_certificate.py` passes.
- [ ] `python3 scripts/check_long_goal_pack.py --self-test` passes.
- [ ] `python3 scripts/check_full_install.py --self-test` passes.
- [ ] `python3 scripts/test_release_payload.py` rejects hash tampering and private-state leakage.
- [ ] `python3 scripts/check_full_install.py --runtime <target> --json` returns a complete payload receipt and the recorded SHA-256 matches the installed candidate.
- [ ] `python3 scripts/build_release_lock.py` has been run after the final source change.
- [ ] `claude plugin validate --strict .` passes when preparing a Claude marketplace release.
- [ ] `python3 scripts/test_mcp_server.py` passes.
- [ ] `python3 scripts/test_guyue_paths.py`, `scripts/test_memory_concurrency.py`, and `scripts/test_memory_migration.py` pass.
- [ ] `python3 scripts/test_codex_extractor.py` passes.
- [ ] `python3 scripts/check_behavior_replay.py --self-test` passes, and every `evals/observations-*.json` file is hash-checked.
- [ ] `ruff check --no-cache scripts src` passes.
- [ ] `bash scripts/test_suite.sh` passes.
- [ ] Any new `references/`, `scripts/`, `assets/`, or `examples/` file mentioned from a `SKILL.md` is included in the release source archive before release packaging.

## Security

- [ ] No API keys, tokens, cookies, private keys, or personal account details are present.
- [ ] No generated cache files are tracked.
- [ ] External skill intake requires `ecosystem-scout` assessment and approval.
- [ ] Unknown install scripts are not auto-executed.
- [ ] Private runtime memory remains under `GUYUE_HOME`.
- [ ] Public release actions such as push, tag, marketplace submission, or deployment require explicit action-specific authorization.
- [ ] History rewrite requires a separate exact scope and force-push authorization.

## Showcase

- [ ] README includes a visible demo or links to one.
- [ ] `examples/showcase.md` includes before/after behavior.
- [ ] Any recorded GIF or screenshot can be regenerated or explained.
- [ ] Evaluation evidence is attached to the release notes.

## Release Notes

- [ ] `CHANGELOG.md` explains why the release exists, not only what changed.
- [ ] Known limitations are listed.
- [ ] Next iteration entry points are listed.
