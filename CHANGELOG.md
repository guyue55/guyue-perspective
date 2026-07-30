# Changelog

## v1.7.2 - 2026-07-30

Status: Released

### Changed

- Remove the company-project workflow from the public Skill payload and retain only its generic permission-governance principles in existing system design, coding and audit capabilities.
- Add project-fingerprint scanning and regressions so company names or project-only contract fields cannot return unnoticed.
- Distinguish user-provided task premises from independently verified facts without widening their meaning.
- Make independent output-quality reviewers read the same synthetic task as producers.
- Strengthen migration/verification closure, evidence-bounded work packages, candidate-memory previews, dependency-version truth, fault-boundary reasoning, fact-closed documentation, action-level ecosystem authorization and source-anchored distillation.
- Remove the host-specific `AGENTS.md` / `RTK.md` instruction chain and runtime-adapter document; make `SKILL.md` the only public instruction entrypoint and enforce that boundary in CI.

### Verification

- `26/26` live activations remain current with the routing contract; the changed `documentation` Skill was regenerated and independently reviewed, restoring current `26/26` synthetic output-quality evidence on Codex CLI `0.146.0-alpha.3.1` with `gpt-5.6-terra`.
- An empty-directory, read-only replay entered through `SKILL.md`, routed the architecture prompt to `system-design`, and did not load a host-specific instruction adapter.
- Strict capability chain: `113/113` routes, `10/10` collaborations, `424/424` internal triggers, `41/41` external candidate triggers and `214/214` near misses.
- Full release suite and exact payload lock passed before tag promotion.

### Boundaries

- This version builds on the corrected `v1.7.1` public base; release metadata, tags and payload locks must preserve the normal SemVer lineage.
- Codex evidence does not prove Claude activation, every runtime, arbitrary inputs, real-user value or public-network installation.

## v1.7.1 - 2026-07-29

Status: Released

### Fixed

- Pin Ruff to `0.16.0` and select the previously effective lint rules explicitly, preventing Ruff 0.16's expanded defaults from making local and CI release gates disagree.
- Include the Ruff dependency and configuration in the required release payload without formatting or refactoring unrelated historical code.

### Verification

- Ruff `0.16.0` with `ruff.toml`
- `bash scripts/test_suite.sh` under the pinned toolchain
- GitHub Actions on `dev` and `main`

### Boundaries

- This hotfix stabilizes the existing lint contract; adopting additional Ruff rules remains separate work.

## v1.7.0 - 2026-07-29

Status: Released

### Changed

- Add a high-impact direction firewall that requires a real problem, native baseline, no-change and repair paths, falsifier, blast radius and rollback before a new mechanism can enter implementation.
- Reset inherited confidence when a multi-turn proposal is materially reshaped, preventing repeated local optimization of an unproven direction.
- Strengthen external-learning admission, maturity, minimal-placement, subtraction, regression and retirement gates so Guyue can absorb reusable value without accumulating redundant machinery.
- Replace the oversized high-risk `cognitive-expansion` ledger with an eight-section evidence spine and align the root orchestration boundary with one-pass, read-only analysis.
- Improve live and output-quality runners with explicit runtime selection, bounded diagnostics, hash-matched review reuse and consistent routing-semantic hashing.

### Verification

- `bash scripts/test_suite.sh`
- `ruff check --no-cache scripts src`
- `git diff --check`
- generated-cache scan
- `python3 scripts/security_scanner.py`
- `python3 scripts/check_capability_chain.py --strict --json`
- Codex CLI `0.146.0-alpha.3.1` with requested model `gpt-5.6-terra`: `27/27` live activations and `27/27` all-Skill synthetic output-quality cases

### Boundaries

- The live matrix proves one Codex runtime/model configuration, not every runtime, arbitrary prompt or long-term user outcome.
- No autonomous browsing, self-modification, automatic promotion or external installation loop is enabled.
- Model-side budget estimates remain proxies until the runner receipt is available.

## v1.6.0 - 2026-07-21

Status: Released

### Changed

- Rename the former project-bound static demo hardening Skill to the generic `static-demo-hardening` capability.
- Replace customer/project-specific wording with anonymous static-demo surface language across routing contracts, evidence artifacts, examples, docs, and tests.
- Promote the current public package metadata to `1.6.0` across the Skill manifest, release manifest, Claude marketplace metadata, README, release checklist, and payload lock.

### Security

- Add project-fingerprint checks to the zero-leakage scanner so the old private demo name, old Skill id, and related styling tokens cannot re-enter release files.
- Exclude local-only `.worktrees` and `.git` paths from release payload verification while still scanning the local copy for residual sensitive strings during this cleanup.

### Removed

- Remove previous release-note files and old release-candidate lineage documents from the current release payload.
- Remove the former project-specific static-demo Skill path and replace it with `skills/static-demo-hardening/SKILL.md`.

### Verification

- `bash scripts/test_suite.sh`
- `ruff check --no-cache scripts src`
- `git diff --check`
- generated-cache scan
- `python3 scripts/security_scanner.py`
- full install payload proof for the generic runtime
- custom full-tree residue scan including ignored local worktrees

### Boundaries

- This release removes the old project-specific Skill identity from the current file tree and release payload.
- It does not rewrite Git commit history, remote tags, or already-published release objects.
