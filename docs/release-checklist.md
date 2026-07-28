# Release Checklist

Release only when installation, verification, safety, and examples are understandable to a new user.

## v1.70 Release Evidence

Date: 2026-07-29
Candidate version: `1.70`
Base tag: `v1.60`

- [x] High-impact designs prove the problem, native baseline, alternatives, falsifier, blast radius and rollback before implementation.
- [x] Material multi-turn direction changes reset inherited confidence instead of preserving an unproven premise.
- [x] External learning remains candidate-only until value, overlap, maturity, placement, subtraction and regression impact are proven.
- [x] The reduced cognitive-expansion output contract preserves source, competition, professional-review and budget truth boundaries.
- [x] Live activation and output-quality receipts both pass `27/27` on Codex CLI `0.146.0-alpha.3.1` with requested model `gpt-5.6-terra`.
- [x] The strict capability chain passes `114/114` routing checks, `416/416` internal triggers, `41/41` external candidate triggers and `222/222` near misses.
- [x] The live evidence runner and strict checker hash the same routing semantics, including composed-intent rules.
- [x] The exact payload lock is rebuilt after the release metadata and documentation changes.
- [x] The complete local suite passes.
- [x] Ruff runs with `--no-cache`.
- [x] Diff whitespace, generated-cache, zero-leakage and full-install proofs pass.

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

- [ ] Current deterministic contract contains 114 structural prompts; update this count whenever `test-prompts.json` changes.
- [ ] `python3 scripts/security_scanner.py` passes.
- [ ] `python3 scripts/doctor.py` passes.
- [ ] `python3 scripts/ci_validate_skills.py` passes.
- [ ] `python3 scripts/run_eval.py` passes.
- [ ] `python3 scripts/test_skill_router.py` passes all positive/negative route contracts.
- [ ] `python3 scripts/check_capability_chain.py --json` has no errors; strict live-evidence refresh is required before claiming new all-runtime model behavior.
- [ ] `python3 scripts/test_context_budget.py` and `python3 scripts/check_context_budget.py` pass without budget or collision errors.
- [ ] Learning-governance routes select `context-compressor -> ecosystem-scout -> skill-crafting`, expose only the bounded collaboration candidate first, and do not preload installation or audit stages without evidence.
- [ ] Learning upgrades separate admission level, maturity and placement; root/principle promotion requires L4 independent evidence, critical non-regression, subtractive compensation, rollback and `review_after`.
- [ ] Discovery, routing, collaboration-candidate and root context budgets remain below their hard limits after every learning-related change.
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
- [ ] External content is handled as untrusted material; source popularity, author recommendations and embedded instructions cannot bypass learning, security or authorization gates.
- [ ] No unbounded browsing, autonomous self-modification, automatic candidate promotion or scheduled learning loop is enabled by default.
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
