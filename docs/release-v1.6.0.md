# Guyue v1.6.0 Release

Date: 2026-07-21
State: `released`
Base tag: `v1.5.1`

## Purpose

v1.6.0 is a privacy and release-hygiene release. It converts the former private static-demo hardening wording into a generic `static-demo-hardening` capability and removes previous release-note files from the current payload.

## What Changed

- The former private static-demo Skill path was renamed to `skills/static-demo-hardening/SKILL.md`.
- Public routing, README, examples, behavior contracts, live-canary references, output-quality evidence, and release metadata now use anonymous static-demo surface language.
- The release manifest, Skill manifest, Claude marketplace metadata, README certificate, and release checklist now identify version `1.6.0`.
- The security scanner now detects the old private project fingerprint, old Skill id, old demo title, and old styling-token family before a release can pass.
- Release payload verification skips local-only `.git` and `.worktrees` directories so scratch worktrees cannot leak into install artifacts.

## Removed

- Previous release-note files and old release-candidate lineage documents are no longer part of the current release payload.
- The former private static-demo Skill id is no longer present in the current file tree.

## Verification

- Complete local suite: pass.
- Ruff with no cache: pass.
- Diff whitespace check: pass.
- Generated-cache scan: no output.
- Zero-leakage scanner: pass.
- Generic full-install payload proof: pass.
- Static-demo routing proof: pass.
- Custom residue scan over the repository and ignored local worktree copy: `findings=0`.

## Boundaries

The current repository tree and release payload are anonymous. This release does not rewrite Git history, delete remote tags, or remove already-published external release objects.
