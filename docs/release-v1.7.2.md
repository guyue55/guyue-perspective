# Guyue v1.7.2 Release Candidate

Date: 2026-07-30
Base tag: `v1.7.1`
State: `candidate`

## Why This Release Exists

The public Guyue payload had absorbed a workflow tied to one company project. The useful permission-governance discipline was general, but its project identity, route and standalone Skill did not belong in a reusable public operating layer.

This candidate removes that project surface, keeps only general backend authorization and audit principles, and strengthens the evidence contracts exposed by the cleanup replay.

## What Changed

- Removed the standalone company-project Skill, route, collaboration workflow, examples and historical generated receipts.
- Kept generic permission design in `system-design`, implementation discipline in `coding-discipline`, and frontend-vs-backend truth checking in `reality-auditor`.
- Added project-fingerprint detection and scanner regressions.
- Corrected the output-quality reviewer so it receives the same synthetic task as the producer and distinguishes user-provided premises from independent verification.
- Added narrow contracts for migration and verification, candidate memory, evidence-bounded UI work packages, dependency lockfile semantics, fault-boundary reasoning, closed-world documentation, action-level ecosystem authorization and source-anchored distillation.
- Removed the host-specific instruction-adapter layer (`AGENTS.md`, `RTK.md`, and its runtime-adapter policy) so every supported runtime enters through the same `SKILL.md` contract.

## Verification

- 26/26 live activations remain current with the routing contract.
- The changed `documentation` Skill was regenerated and independently reviewed on Codex CLI `0.146.0-alpha.3.1` with `gpt-5.6-terra`; current synthetic output quality passes at 26/26.
- An empty non-Git directory replay activated Guyue through `SKILL.md`, routed a multi-tenant audit-log architecture prompt to `system-design`, and did not load a host-specific instruction adapter.
- Strict capability chain passed:
  - 113/113 capability routes
  - 10/10 collaboration routes with 26/26 Skill coverage
  - 424/424 internal triggers
  - 41/41 external candidate triggers
  - 214/214 near misses
- Full release-suite and exact-payload results are recorded in the release checklist before tag promotion.

## Version Lineage

`1.7.2` follows the corrected public sequence `v1.6.0 → v1.7.0 → v1.7.1`. The release manifest, Marketplace metadata, tag and payload lock must all identify the same version before publication.

## Evidence Boundary

The live matrix covers Codex CLI `0.146.0-alpha.3.1` with requested model `gpt-5.6-terra` and one synthetic task per Skill. It does not prove Claude activation, other runtimes, arbitrary prompts, real-user value, public-network installation or long-term outcomes.
