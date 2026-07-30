# Changelog

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
