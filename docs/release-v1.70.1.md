# Guyue v1.70.1 Release

Date: 2026-07-29
State: `released`
Base tag: `v1.70`

## Purpose

v1.70.1 is a reproducibility hotfix for v1.70. The runtime behavior and evidence contracts are unchanged; this patch prevents a Ruff upstream default-rule expansion from making local and GitHub Actions release gates evaluate different rule sets.

## What Changed

- Pin Ruff to `0.16.0` in `requirements.txt`.
- Add `ruff.toml` with the previously effective `E4`, `E7`, `E9` and `F` rules selected explicitly.
- Require both the dependency declaration and Ruff configuration in the install payload.
- Preserve the v1.70 direction firewall, learning-governance, cognitive-expansion and evidence-runner changes without broad formatting churn.

## Verification

- Ruff `0.16.0` with the repository configuration: pass.
- Complete local suite under the pinned toolchain: pass.
- Ruff with no cache: pass.
- Diff whitespace check: pass.
- Generated-cache scan: no output.
- Zero-leakage scanner: pass.
- Strict capability chain: pass.
- Codex CLI `0.146.0-alpha.3.1`, requested model `gpt-5.6-terra`: live activation `27/27` and all-Skill synthetic output quality `27/27`.
- GitHub Actions on `dev` and `main`: pass.

## Boundaries

- This patch freezes the lint contract; it does not claim that all 413 Ruff 0.16 default rules have been adopted.
- Expanding the lint policy remains a separate refactor and must not be smuggled into a release hotfix.
- Runtime behavior evidence is inherited only because no routing or Skill behavior changed after the v1.70 receipts.
