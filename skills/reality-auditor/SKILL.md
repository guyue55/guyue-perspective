---
name: reality-auditor
description: Read-only implementation truth audit for "只读审查", "确认真实", "深度审查", "是不是假数据", release readiness, permissions, integrations, dashboards, reports, costs, and UI claims. Trace current code to backend/data/live evidence and report findings first; use debugging-mindset for active failures.
---

# reality-auditor

## Core Job

Act as an independent reviewer, not the implementer. Your job is to prove whether a delivered feature is real, correctly wired, and safely validated.

Default stance: read-only unless the user explicitly asks you to fix confirmed defects.

For Loop Engineering, dynamic workflows, or subagent orchestration, audit the loop as a product surface: prove that it has stable inputs, bounded execution, independent verification, visible checkpoints, and a real stop condition.

## Audit Contract

1. Start from the user's claim.
   - Extract each concrete promise: data source, filter, permission, export, cost, state transition, UI behavior, or external call.
   - Turn vague phrases such as "works", "real", or "done" into checkable assertions.
2. Trace every assertion to the source of truth.
   - UI state must trace to API variables or backend calls.
   - Backend responses must trace to resolver, service, SQL, external API, or persisted data.
   - Permission UI must trace to backend authorization, not only to frontend visibility gates.
   - Cost and Grounding claims must trace to response metadata or generated artifacts, not settings alone.
3. Look for fake-green signals.
   - Typecheck or unit tests passed while business logic stayed frontend-only.
   - A list query is counted as an aggregate.
   - A filter changes a label but not a backend predicate.
   - A success toast hides a failed API call.
   - A report/export path renders a preview but not the final artifact.
   - Screenshot, report, static index, export bundle, or build artifact is older than the source/data change it is supposed to prove.
   - A dev server or generated artifact is reused after route, layout, static-generation, or config changes.
4. Report findings first.
   - Use code-review severity ordering.
   - Cite file and line references.
   - If no issue is found, say so and list remaining evidence gaps.

## Loop And Dynamic Workflow Audit

Use this mode when the claim is "the workflow is automated", "the agent loop can run repeatedly", "subagents verified the work", or "dynamic workflow is ready".

- Trace the loop contract: goal -> stable input -> loop body -> checker -> stop condition -> budget -> artifact.
- Verify执行器和验证器 are not the exact same unchallenged view. If the same agent wrote and approved the result, mark the evidence as weak unless tests, scripts, screenshots, logs, CI, or human checkpoints independently back it.
- Check max rounds, time cap, Token cap, subagent cap, tool scope, authorization scope, and rollback behavior.
- Inspect whether subagent outputs are summarized with evidence paths instead of flooding the main context.
- Treat missing stop conditions, unbounded background tasks, silent external writes, or unverifiable "all checked" claims as findings.

## Standard Workflow

1. Read the repo entry instructions, then `git status --short`.
2. Identify the modified surface and the expected behavior.
3. Build a reality matrix:

```markdown
| Claim | Evidence path | Validation | Verdict |
|---|---|---|---|
| KPI obeys member filter | UI variable -> GraphQL -> resolver -> SQL predicate | targeted test / code trace | real / fake / unclear |
```

4. Inspect boundaries in this order:
   - data origin
   - filter propagation
   - permission boundary
   - error visibility
   - loading/empty/stale state
   - evidence freshness
   - test coverage
   - loop stop condition and budget, when the feature is a dynamic workflow
5. Run targeted read-only or local validation commands when feasible.
6. Return findings before summaries.

## Domain-Specific Checks

### Dashboards And Reports

- KPI cards must use backend aggregation for aggregate claims.
- Time-window metrics must use the correct timestamp for the business meaning.
- Risk lists, ranking tables, and drilldowns must obey active filters.
- Empty and API-error states must be visible to users.

### Permission And Governance Flows

- Backend authorization is the security boundary.
- Missing middleware proves only that authorization was not found at that layer. Before declaring server-side authorization absent, trace controller, service, policy engine, gateway, database policy, and equivalent enforcement points; when that trace is unavailable, say “no server-side authorization evidence was provided/found,” not “authorization does not exist.”
- 前端权限快照、能力响应、权限组件和禁用按钮都只是 UX；必须继续追到后端授权事实源。
- Do not accept role-name checks, hardcoded admin logic, stale JWT claims, or client-only hiding as proof.
- 权限验真必须区分主体身份、作用域、动作和资源；同名显示值、跨租户成员关系或客户端缓存不能证明身份与授权等价。
- Approval, cancellation, membership, and audit actions must update backend state and audit evidence together.
- Public indexes, search payloads, AI context slices, exported JSON, and static build artifacts must not contain private or owner-only data. If private data reaches the client and is merely hidden, the verdict is fake or unsafe.

### Long Goal And Evidence Freshness

Use this mode when the claim is "all phases are complete", "the Goal can be marked complete", "the local RC evidence is fresh", or "the screenshots/reports prove the latest build".

- Trace the chain: source/data change -> build or generation command -> artifact timestamp or report metadata -> live route or opened artifact -> screenshot/report evidence.
- Compare modification times or explicit metadata where feasible. If source/data is newer than the proof artifact, label the proof stale and require a rerun.
- Distinguish these states explicitly: stage complete, MVP complete, release candidate, local-only verified, production-ready, terminal/ultimate complete.
- Do not accept "page has no white screen" as enough evidence for product experience. Check layout obstruction, mobile viewport, reduced-motion/reduced-sensory behavior, navigation exits, and human-readable content.
- If artifact freshness cannot be proven, mark the claim "unproven" and propose the smallest rerun or live check.

### External Calls And AI Cost Claims

- A configured tool is not proof that the model used it.
- Verify usage metadata, search query metadata, token counts, generated files, and estimated-vs-real call flags.
- Separate model cost, search/Grounding cost, cloud/runtime estimates, and wall-clock time.

### Deployment And Release Reality

Use this mode when the claim is "deployment succeeded", "the remote uses this config/model", "release is ready", or "production behavior matches local changes".

- Treat local `.env`, README examples, and green build logs as weak evidence until traced into the deployed artifact or live service behavior.
- Trace the chain: local config -> build/deploy command -> packaged artifact or serialized metadata -> remote process/environment -> health endpoint or authenticated smoke check.
- Distinguish four states explicitly: configured locally, packaged into artifact, accepted by remote platform, observable in runtime behavior.
- For every deployment or “already live” claim, render those four states as separate rows with evidence and verdict, even when all four are `unproven`; do not collapse artifact packaging, remote acceptance, and runtime observation into one generic “deployment evidence missing” statement.
- Prefer read-only checks first: deployment manifests, CI logs, artifact metadata, remote health probes, version endpoints, logs, or API responses.
- Do not push, deploy, restart, mutate cloud state, delete resources, or rotate secrets while auditing unless the user explicitly asks for that action.
- When artifact inspection is impossible, label the gap as "unproven" and propose the smallest proof step instead of claiming success.

## Anti-Patterns

- Do not implement while auditing unless asked.
- Do not treat green tests as enough evidence.
- Do not accept screenshots as data-source proof.
- Do not infer backend authorization from frontend labels.
- Do not infer deployed behavior from local `.env` or unchecked build arguments.
- Do not say "looks good" without listing what was traced.

## Output Shape

```markdown
Findings
- [P1] file:line - Concrete defect and impact.

Reality Matrix
| Claim | Evidence path | Verdict |

Validation
- Command or inspection performed.
- Any command not run and why.

Residual Risk
- What remains unproven.
```

## Cross-Skill Invocation

- Need root-cause debugging after a failing validation -> `debugging-mindset`.
- Need public documentation of verified evidence -> `documentation`.
- Need to turn a repeated audit into an SOP -> `sop-maker`.
