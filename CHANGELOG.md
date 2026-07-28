# Changelog

## v1.70.1 - 2026-07-29

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

## v1.70 - 2026-07-29

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

## v1.60 - 2026-07-21

Status: Released

### Changed

- Rename the former project-bound static demo hardening Skill to the generic `static-demo-hardening` capability.
- Replace customer/project-specific wording with anonymous static-demo surface language across routing contracts, evidence artifacts, examples, docs, and tests.
- Promote the current public package metadata to `1.60` across the Skill manifest, release manifest, Claude marketplace metadata, README, release checklist, and payload lock.

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
