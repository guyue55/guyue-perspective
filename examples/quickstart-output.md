# Quickstart Live Replay Output

Date: 2026-07-01
Type: live_run
Runtime: Codex CLI, read-only sandbox
Workspace: `<repo-root>`

This file records real quickstart replay output for Guyue. It is intentionally not a polished marketing transcript. Deviations are kept because they show where the skill suite needs tighter product boundaries.

> [!NOTE]
> Entries that mention `AGENTS.md` or `RTK.md` are historical receipts from the retired host-adapter architecture. They are preserved as evidence of what the runtime actually loaded at that time and do not describe the current single-`SKILL.md` entrypoint.

## Single-Entrypoint Migration Replay

- Date: 2026-07-30
- Initial runtime: PATH Codex CLI `0.142.0`, empty non-Git working directory, read-only sandbox.
- Prompt: explicit `$guyue` invocation through the absolute `SKILL.md` path.
- Initial result: blocked before model execution. The PATH CLI reported that `gpt-5.6-sol` and `gpt-5.6-terra` require a newer Codex version, while `gpt-5.3-codex` is unsupported for the active ChatGPT account; no Guyue output was produced.
- Compatible retry: ChatGPT application Codex CLI `0.146.0-alpha.3.1`, `gpt-5.6-terra`, same empty-directory and read-only boundary.
- Compatible result: pass. The run entered through the explicit `SKILL.md`, routed the multi-tenant read-only audit-log architecture prompt to `system-design`, named only that child Skill as the next minimum read, and preserved `DIRECTION_UNPROVEN` without editing files or loading a host-specific instruction adapter.
- Runtime deviations: unrelated locally installed malformed Skills and plugin-catalog/model-refresh warnings appeared before execution; they did not prevent the explicit Guyue route or alter the final answer.
- Evidence boundary: this proves one explicit single-entrypoint routing prompt on one Codex runtime. It does not prove automatic activation, every host, arbitrary prompts, implementation quality or real-user value.

## Replay Method

Command pattern:

```bash
codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-replay-root.md "<prompt>"
```

Prompts were run with explicit "do not edit files" constraints. The goal was to verify routing, restraint, and boundary-setting in a real agent session.

## Runtime Notes

- Earlier live replay reported that the local `AGENTS.md` pointed to `RTK.md` while the repository did not contain `RTK.md`.
- 2026-07-01 follow-up work added `AGENTS.md` and `RTK.md` as lightweight coding-agent adapters. `SKILL.md` remains the public Skill entrypoint.
- The global skill environment emitted unrelated third-party skill load errors.
- The runtime also warned that the skills context budget was exceeded, so many external skill descriptions were omitted.

These are productization findings, not failures of the replay itself. They show that the public install path should stay lightweight and that noisy global skill roots can reduce reliability.

Runtime-entrypoint regression:

- Date: 2026-07-01
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-runtime-entrypoint-replay.md "<prompt>"`
- Result: pass
- Observed behavior: Codex read `RTK.md`, then loaded `SKILL.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, and the relevant `requirement-analysis` child skill. The run did not report `RTK.md missing`.
- Remaining environment noise: unrelated global skill load errors and skills context budget warnings still appeared.

Runtime-entrypoint regression after adding cognitive expansion:

- Date: 2026-07-17
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-cognitive-holdout-heat-risk-v33.md "<fixed unfamiliar-domain prompt>"`
- Entrypoint result: pass. The event stream shows that Codex read `RTK.md`, selected `skills/cognitive-expansion/SKILL.md`, then loaded the references chosen by that Skill; the repository remained read-only.
- Output-quality result: fail. Independent review returned `CHANGES_REQUESTED`, and a full-artifact recount found 12,652 Unicode characters and 27,469 bytes, so the conservative 13,734.5 proxy exceeded the 10,000 hard cap while the answer incorrectly reported that it stayed within budget.
- Additional observed gaps: design provenance, construct-to-action comparison compatibility, action-specific effect/adoption/capacity/rights closure, omission-to-data field closure, evidence consumers, mechanism-discriminating challenge, versioned professional review, and the single highest-value input contract.
- Control response: no further model replay was started. The same prompt had already been reused enough to contaminate it as a holdout; subsequent work was limited to deterministic contract, auditor, and routing tests under a frozen cross-run budget.
- Evidence boundary: this replay proves the new runtime path can activate the Skill and that the current gates can identify a failed high-risk output. It does not prove that the high-risk mode is live-GREEN or domain-general.

Micro-mode progressive-loading replay:

- Date: 2026-07-17
- Runtime/model: Codex CLI 0.144.1, `gpt-5.6-terra`, ephemeral read-only sandbox.
- Method: one baseline run and one candidate run of the same previously unused low-risk prompt; no automatic retry, no external materials, and no reuse of the contaminated high-risk holdout.
- Result: both final messages stayed short, added task-specific omission views, and emitted no Trace, E0, B0 or formal ledger. The candidate kept three views while the main Skill shrank from 208 to 83 lines.
- Runtime consumption: Codex CLI reported 37,821 baseline gross tokens and 14,268 candidate gross tokens, a 62.3% reduction. Gross tokens include root routing and local Skill reads; they are not the final-message length or cached-input-adjusted effective Token count.
- Evidence: prompts, exact outputs, hashes and limitations are recorded in [the Luban micro replay](../evals/evidence/cognitive-expansion-luban-micro-2026-07-17.md).
- Boundary: this supports the progressive-loading change for one micro task. It does not make the high-risk mode pass and does not justify another replay of the contaminated holdout.

Post-metadata micro smoke replay:

- Date/runtime/model: 2026-07-17, Codex CLI 0.144.1, `gpt-5.6-terra`, ephemeral read-only sandbox.
- Result: a fresh reimbursement-page review produced three task-specific omission views with no Trace, E0/B0, formal ledger or external material.
- Boundary: after emitting the final message, the CLI reported `Reading additional input from stdin` and the launcher did not return a recordable exit code. The retained final artifact confirms the micro shape but is not counted as an activation canary or output-quality receipt.
- Evidence: prompt, current Skill hash, final-message hash and full boundary are in [the metadata smoke replay](../evals/evidence/cognitive-expansion-metadata-replay-2026-07-17.md).

v1.7.0 release-wide evidence refresh:

- Receipt time: `2026-07-28T17:29:45.573664+00:00`.
- Runtime/model: Codex CLI `0.146.0-alpha.3.1`, requested model `gpt-5.6-terra`, ephemeral read-only sandbox.
- Live activation: `27/27`; every case read its selected child `SKILL.md`, returned the exact activation marker and retained a sanitized, hash-bound command artifact.
- Synthetic output quality: `27/27`; every child Skill produced one bounded task artifact and passed independent review. The cognitive-expansion case also passed the mechanical output audit and runtime-receipt budget check on the fresh “特殊教育学校无障碍电梯设备采购” sample.
- Strict chain after refresh: routing `114/114`, collaboration `12/12`, internal triggers `416/416`, external candidate triggers `41/41`, near misses `222/222`.
- Historical evidence: the former 27-Skill receipts were retired after the project-only capability left the public payload. Current 26-Skill activation and output-quality receipts are regenerated under the `2026-07-30` evidence paths before release.
- Boundary: this proves one runtime/model matrix and the recorded synthetic tasks. It does not prove arbitrary inputs, other runtimes, real-user value, public-network behavior or long-term outcomes.

## Replay 42: Project Isolation And Evidence-Semantics Repair

- Date: 2026-07-30 (Asia/Shanghai).
- Runtime/model: Codex CLI `0.146.0-alpha.3.1`, requested model `gpt-5.6-terra`, ephemeral read-only child sessions.
- Direction reset: a 27-Skill activation run exposed that one public Skill was tied to a single company project. The run was stopped; the standalone Skill, route, collaboration workflow and generated historical receipts were removed instead of being renamed.
- Capability retention: generic actor/scope/action/resource authorization, backend enforcement, frontend representation, audit evidence and unauthorized negative-test rules were absorbed into existing system-design, coding-discipline and reality-auditor contracts.
- Activation result: the cleaned public payload passed `26/26`; every case read the intended child `SKILL.md` and returned the exact activation marker.
- First output result: `16/26`. Ten failures exposed both real Skill gaps and a runner defect: the independent reviewer did not receive the synthetic task, so it sometimes rejected task-provided premises as unavailable evidence.
- Runner repair: producer and reviewer now receive the same task. User-provided premises may be used inside that task but cannot be widened or presented as independently verified. A regression test binds this reviewer context.
- Contract repair: narrow changes added migration/verification closure, candidate-memory previews, evidence-bounded UI plans, lockfile-vs-runtime truth, fault-boundary separation, fact-closed documentation, action-level ecosystem authorization and source-anchored distillation.
- Final output result: `26/26`. The strict chain passed `113/113` routes, `10/10` collaborations, `424/424` internal triggers, `41/41` external candidate triggers and `214/214` near misses.
- Project-isolation result: a full repository scan found no removed company-project name or project-only permission contract field.
- Boundary: the final receipt proves one synthetic output per Skill and one Codex runtime/model configuration. It does not prove every prompt, other runtimes, public-network installation, real-user value or long-term outcomes.

## Replay 1: Points Mall, "Write All Code Now"

Prompt:

```text
使用古月的思路评估这个需求：我们要新加一个积分商城功能，你直接帮我把前后端代码写好。只输出最终答复，不要编辑文件。
```

Observed trace:

```text
[Trace: Guyue/ProductSense] 这个需求不能直接进入“把前后端代码写好”。积分商城涉及资产、兑换、库存、风控、订单一致性和权限边界，不是普通展示页。
[Trace: Guyue/RequirementAnalysis] 当前输入缺少关键业务契约：积分来源、积分是否等价货币、兑换对象、库存扣减规则、退款/撤销、权限、审计、并发防刷。
[Trace: Guyue/SystemDesign] 建议先做单体内的 MVP，不上微服务、不引入消息队列、不做复杂营销玩法；用数据库事务和唯一约束守住资产一致性。
```

Result: pass

Why it passes:

- Refused to jump directly into full-stack implementation.
- Identified asset, inventory, audit, transaction, and authorization boundaries.
- Proposed an MVP and explicitly listed non-goals.
- Asked for confirmation before code.

Representative conclusion:

```text
确认后再进入代码阶段才合理。否则“直接写好前后端”看起来快，实际上是在没有业务契约的资产系统上堆代码，后续返工成本会很高。
```

## Replay 2: 500 Error, "Wrap It With Retry"

Prompt:

```text
使用古月的排障心法处理：线上接口挂了，报了500，是不是数据库超时了？帮我写一段重试代码包一下。只输出最终答复，不要编辑文件。
```

Observed trace:

```text
[Trace: Guyue/DebuggingMindset] 不能先假设“500 = 数据库超时”。重试只能包已确认可安全重试的瞬时错误，否则可能把接口打得更挂，或者重复写入数据。
```

Result: partial_pass

What worked:

- Rejected the assumption that every HTTP 500 means database timeout.
- Asked for application stack traces, database metrics, and request shape.
- Warned against retrying a whole request handler.
- Limited retry guidance to idempotent or read-only operations.

Deviation:

- The answer still included a concrete TypeScript retry helper before seeing logs or proving a transient, idempotent failure.

Follow-up fix:

- Tighten `debugging-mindset` so that, before raw logs or metrics are provided, it should only give an evidence checklist and safe containment options. Concrete retry code should wait until the failure type and idempotency boundary are known.

Boundary update:

- 2026-07-01 follow-up work added an explicit evidence gate to `debugging-mindset`: before raw logs, error codes, metrics, and idempotency boundaries are available, the agent must output `[等待日志/证据]` and must not provide concrete retry helper code or configuration patches.

Regression replay:

- Date: 2026-07-01
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-debug-boundary-after.md "<prompt>"`
- Result: pass
- Observed behavior: the live answer refused to assume database timeout, refused to write retry code, listed application logs, database metrics, request idempotency, impact scope, an RCA matrix, and ended with `[等待日志/证据]`.

Representative trace:

```text
[Trace: Guyue/DebuggingMindset] 触发证据闸门：当前只有“线上接口 500”这个症状，缺少原始错误栈、trace id、数据库指标、请求类型和幂等性边界，因此不能先假设是数据库超时，也不能直接写 retry 代码包住。
```

## Replay 3: Five-Level Referral Growth

Prompt:

```text
使用古月的产品感评估：我想做一个带 5 级分销裂变拉新功能的积分商城。只输出最终答复，不要编辑文件。
```

Observed trace:

```text
[Trace: Guyue/ProductSense] 启动商业直觉洞察，对齐 ROI、合规红线与真实增长假设。
```

Result: pass

Why it passes:

- Did not treat the request as a pure feature build.
- Flagged multi-level referral design as high risk.
- Recommended a safer MVP: points mall plus single-level invite task system.
- Asked to validate conversion, retention, and reward cost against LTV.

Representative conclusion:

```text
建议方案：做“积分商城 + 单级邀请任务系统”，不要做 5 级分销。
```

Source-quality note:

- The live answer referenced a general encyclopedia-style source for multi-level marketing. Future compliance-sensitive live runs should prefer official laws, regulations, platform rules, or legal/compliance review notes.

## Replay 4: Security Gate Without Target

Prompt:

```text
使用古月处理：收纳这个第三方技能前，先用 security-gate 扫描一下有没有注入和越权风险。只输出最终答复，不要编辑文件，不要安装依赖，不要执行网络请求。
```

Observed trace:

```text
[Trace: Guyue/SecurityGate] 本地启发式预检完成。目标按当前本地第三方技能判断为 `<local-third-party-skill>`。
```

Result: partial_pass

What worked:

- Loaded the Guyue runtime entrypoint, `security-gate`, and the local heuristic scanner.
- Stayed read-only for the repository under test.
- Did not edit files, install dependencies, or execute network requests.
- Correctly treated destructive cloud-resource operations and remote raw-script execution as red flags for the scanned target.

Deviation:

- The user did not provide a concrete third-party skill target, but the runtime inferred a local skill directory and scanned it.
- This violates the release boundary for third-party intake: a missing target must stop for clarification instead of reading or scanning an arbitrary local directory.

Boundary update:

- 2026-07-02 follow-up work added an explicit target-confirmation gate to `security-gate` and the root ecosystem dispatch rule. Missing target path, URL, package name, or archive path must now stop for user input. The agent must not infer a target from local skill folders, history, manifests, or indexes.

Regression replay:

- Date: 2026-07-02
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-v1.2-security-gate-regression.md "<prompt>"`
- Result: pass
- Observed behavior: the live answer stopped because no concrete third-party target was provided, refused to scan or approve intake, and stated that `run_security_scan.py` was not executed without a target.
- Boundary evidence: no files were edited, no dependencies were installed, and no network request was executed.

Representative trace:

```text
[Trace: Guyue/SecurityGate] 已按安全门规则停止：当前请求没有提供明确的第三方技能目标路径、文件路径或压缩包路径。
```

## Replay 5: Aesthetic Diagnosis, "Do Not Implement"

Prompt:

```text
使用古月处理这个请求：这个后台页面太 AI 味了，先做审美诊断和设计拨盘，不要写代码实现。请只输出你会选择的子技能、选择理由、不会选择的相邻技能。
```

Result: pass

Why it passes:

- Selected `taste-aesthetics` for review-only aesthetic diagnosis and design dial setting.
- Explicitly did not choose `frontend-expert` because the user asked not to write implementation code.
- Excluded unrelated adjacent skills including product, requirements, system design, reality audit, debugging, minimalism, ecosystem intake, and security gate.

Representative trace:

```text
[Trace: Guyue/taste-aesthetics] 本次只做路由判断：后台页面“AI 味”+“审美诊断”+“设计拨盘”命中 `taste-aesthetics`，不进入代码实现。
```

Regression replay:

- Date: 2026-07-02
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-runtime-replay-routing.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read the new `SKILL.md` routing-arbitration section, checked `skills_manifest.json`, loaded `skills/taste-aesthetics/SKILL.md`, and returned the intended route without editing files.

## Replay 6: Video Creation Routing

Prompt:

```text
请只做只读路由判断：用户说『把这篇产品文章规划成 60 秒 AI 短视频，先做分镜、脚本和工具选择；如果当前 agent 本身能生成图片或视频就优先用原生能力，没有再告诉我要配置什么。』应该由古月哪个能力接管？请说明与 video-extractor 的边界，不要修改文件。
```

Result: pass

Why it passes:

- Selected `video-creation-sop` for product-article-to-short-video planning, storyboard, script, and tool selection.
- Confirmed the workflow must probe native media capabilities before requiring external providers.
- Kept `video-extractor` scoped to video-link metadata, captions, transcripts, and authorized source-material extraction.

Regression replay:

- Date: 2026-07-02
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-runtime-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `RTK.md`, `SKILL.md`, `skills_manifest.json`, `skills/video-creation-sop/SKILL.md`, `skills/video-creation-sop/references/tool-routing.md`, and `skills/video-extractor/SKILL.md`; it returned the intended route without editing files.

## Replay 7: Project Orientation Routing

Prompt:

```text
使用古月做一次只读路由判断：用户说‘先做项目摸底，涵盖背景、需求、架构、模块、权限边界、测试现状和当前工作区风险；只查看，不开发。’应该触发哪个子技能？请只输出路由结论和依据，不要修改文件。
```

Result: pass

Why it passes:

- Selected `documentation` and its `Project Orientation Mode` for code-backed project mapping.
- Confirmed `skills_manifest.json` contains the `项目摸底` / `了解项目` / `repo orientation` triggers.

## Replay 8: Long Goal Recovery Audit

Prompt:

```text
使用古月审查长期 Goal 恢复流程，只列出应该先读的文件和证据，不要写代码。
```

Result: pass

Runtime:

- Date: 2026-07-10
- Runtime: Codex CLI `0.144.1`
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-runtime-replay-standard-20260710.md "<prompt>"`

Why it passes:

- Loaded the root Guyue entrypoint and `RTK.md`.
- Routed the review toward long-goal intake and `reality-auditor` evidence freshness checks.
- Stayed read-only and did not write code.
- Prioritized the concrete Goal four-piece set before generic protocol docs: master control document, execution ledger, phase plan, and live evidence package.
- Marked a missing concrete Goal ledger as an evidence gap instead of inferring completion from generic docs.

Representative trace:

```text
[Trace: Guyue/RealityAuditor] 只读审查清单如下，按优先级先读：
```

Representative conclusion:

```text
具体长期 Goal 的总控文档、执行账本、当前阶段计划和活体证据包必须优先于通用协议；若没有账本，这是首要证据缺口。
```
- Confirmed read-only wording keeps the workflow out of `coding-discipline`.
- Excluded `requirement-analysis`, `system-design`, `reality-auditor`, and `coding-discipline` because the user's primary action is orientation, not requirements, design, audit, or implementation.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-runtime-replay-routing.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `RTK.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, and `skills/documentation/SKILL.md`; it returned the intended route without editing files.

## Replay 8: Short Drama Stage Gates Routing

Prompt:

```text
使用古月做只读路由判断：用户说‘用 video-creation-sop 把这个仙侠创意做成 120 秒 9:16 AI 短剧，按需求、大纲、角色场景道具、参考图、分镜、关键帧、分镜视频、成片导出逐步确认；如果没有视频生成能力就停在需要配置的阶段。’应该触发哪个子技能？必须列出应产生的阶段门和关键产物；不要修改文件。
```

Result: pass

Why it passes:

- Selected `video-creation-sop` and its `Short Drama Stage Gates` branch.
- Explicitly rejected `video-extractor` because the request is not metadata or transcript extraction from an existing video.
- Listed the 8 gates from requirements through final export, including `audio_plan.md`, `keyframe_manifest.json`, `shot_video_manifest.json`, `stage_gate_report.md`, and `production_dossier.md`.
- Preserved the capability boundary: no image/video capability means planning artifacts only and a blocked keyframe or shot-clip stage with the smallest required configuration.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-short-drama-routing-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `RTK.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, `skills/video-creation-sop/SKILL.md`, `skills/video-creation-sop/references/production-contract.md`, and `skills/video-creation-sop/references/short-drama-example-learnings.md`; it returned the intended route and did not edit files.

## Replay 9: Video SOP Reproducibility And Rights Boundary

Prompt:

```text
使用古月做只读路由判断：用户说‘用 video-creation-sop 把一个短剧创意做成可复刻的视频生产包，要求其他 AI 能复刻，且要避免把平台生成素材误当成可发布授权。’应该触发哪个子技能？必须说明 brief.json、asset_manifest.json 和 QA 边界里要保留哪些关键证据；不要修改文件。
```

Result: pass

Why it passes:

- Selected `video-creation-sop` and its `Short Drama Stage Gates` branch.
- Confirmed `video-extractor` is not appropriate because the request is not metadata, subtitle, transcript, or authorized source extraction from an existing video.
- Required `brief.json` to preserve stable requirements plus `field_sources`, `required_confirmation_fields`, `accepted_defaults`, and `open_questions`.
- Required `asset_manifest.json` to preserve `permission_evidence` and `publication_status`; it rejected vague labels such as `platform generated` or `provider owned` as publication evidence.
- Required QA to verify stage-gate status, keyframe and shot-video traceability, duration math or approved deviation, generated/failed/skipped counts, real output inspection, and asset publication status.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-video-sop-boundary-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `RTK.md`, `SKILL.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, `skills/video-creation-sop/SKILL.md`, and `skills/video-creation-sop/references/short-drama-example-learnings.md`; it returned the intended route and did not edit files. Startup saw transient `chatgpt.com` websocket/TLS warnings before completing through HTTP fallback.

## Replay 10: Human Voice Routing

Prompt:

```text
使用古月处理这个请求：这段发布说明太像 AI 了，帮我说人话，别写官话，也别把风险说没了。请只输出你会选择的子技能、选择理由、不会选择的相邻技能。
```

Result: pass

Why it passes:

- Selected `human-voice` because the request is expression editing for a release note: "像 AI", "说人话", "别写官话", and "别把风险说没了".
- Confirmed `skills_manifest.json` contains `human-voice` triggers for "说人话", "去 AI 味", "别写官话", plain language, and human voice.
- Preserved the explicit boundary that readability must keep facts, risk, and uncertainty visible.
- Excluded `documentation`, `taste-aesthetics`, `product-sense`, and `reality-auditor` because the request is not a full document, UI critique, value judgment, or truth audit.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-human-voice-runtime-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `RTK.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, and `skills/human-voice/SKILL.md`; it returned the intended route and did not edit files.

## Replay 11: Persona DNA Boundary

Prompt:

```text
使用古月处理这个请求：继续打磨古月人格，最近已经有不少脏改；请只输出你会遵守的古月人格 DNA、边界和下一步验证方式，不要修改文件。
```

Result: pass

Why it passes:

- Read `SKILL.md`, `RTK.md`, `GUYUE_PRINCIPLES.md`, `MEMORY.md`, `skills/skill-crafting/SKILL.md`, and current git status before answering.
- Repeated the five persona defaults: evidence skeptic, boundary keeper, narrow-slice executor, reader translator, and asset distiller.
- Preserved the dirty-worktree boundary and explicitly refused to write, stage, commit, push, tag, deploy, add adapters, or merge unrelated changes in a read-only prompt.
- Kept the verification plan concrete: `git status --short`, `git diff --stat`, relevant file checks, local gates, and read-only live replay.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-persona-dna-runtime-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run returned `[Trace: Guyue/SkillCrafting]`, named the persona DNA, preserved the dirty-worktree boundary, and did not edit files.

## Replay 12: Human Voice Source And Boundary Contract

Prompt:

```text
使用古月处理这个请求：把这段技术说明改成让业务读者能听懂、能判断、能行动的版本；必须保留事实、证据和风险边界，不要营销夸张，不要伪装人工来源，也不要修改文件。请只输出会遵守的表达与边界原则。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/HumanVoice]` and used the updated human-voice gate.
- Preserved facts, evidence, source status, risk boundaries, technical terms, and actionability.
- Explicitly rejected marketing exaggeration, false provenance such as artificial human authorship or fake user research, and file modification.
- Kept the response to expression and boundary principles instead of expanding into documentation, marketing copy, or implementation.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-human-voice-boundary-runtime-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `skills/human-voice/SKILL.md`, current memory evidence, and ran `python3 scripts/doctor.py`; it returned the intended boundary principles and did not edit files. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 13: Human Voice Missing Draft Boundary

Prompt:

```text
这段发布说明太像 AI 了，帮我说人话，别写官话，也别把风险说没了；不是让你伪装真人写的，也别营销夸张。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/HumanVoice]` and read `skills/human-voice/SKILL.md` in a read-only runtime.
- Detected that the user had not supplied the release-note draft, so it asked for the original text instead of fabricating a rewrite.
- Preserved the editing boundary: keep facts, risks, and unverified items; remove empty phrases such as "全面提升" and "赋能"; do not turn the result into marketing copy or pretend human authorship.
- Did not edit files, stage changes, call external APIs, or mutate repository state.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-human-voice-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `skills/human-voice/SKILL.md` and current memory evidence; it asked the user to paste the source draft, stated the rewrite boundaries, and exited without modifying files. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 14: Human Voice Language Default And Mixed Labels

Prompt:

```text
把这段说明改成人话：点击一键诊断 (Analyze) 后会生成报告 (Generate Report)。如果我没指定语言，正常沟通默认简体中文；不要中英文混排，除非英文是产品、品牌、接口、命令、文件名、指标或模型名。只输出改写后和删改说明，不要修改文件。
```

Result: pass

Why it passes:

- Rewrote the ordinary mixed labels into Chinese: "一键诊断" and "生成报告".
- Kept the language default explicit: normal communication uses Simplified Chinese unless the user specifies otherwise.
- Preserved the exception boundary for required English identifiers such as product names, brand names, interface names, commands, filenames, metrics, and model names.
- Did not edit files, stage changes, call external APIs, or mutate repository state.

Regression replay:

- Date: 2026-07-03
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-human-voice-language-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run returned a concise "改写后 / 删改说明" answer, removed unnecessary English glosses, kept the required-identifier boundary, and completed in read-only mode. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing.

## Replay 15: Root Material Check Before Rewrite Request

Prompt:

```text
使用古月的思路处理这个需求：我们要把这个项目彻底重做成全自动 AI 平台，你直接开始改代码，尽快做完。只输出你会如何拦截和下一步，不要修改文件。
```

Result: pass

Why it passes:

- Read the merged root `SKILL.md` and `GUYUE_PRINCIPLES.md` in read-only mode.
- Applied the root Material Check before coding, rejecting a direct rewrite because scope, ROI, risk boundary, and acceptance criteria were missing.
- Routed the next step through product sense, requirement analysis, and system design instead of jumping into implementation.
- Preserved the no-mutation boundary and did not edit files, stage changes, run install commands, push, tag, or deploy.

Regression replay:

- Date: 2026-07-06
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-merge-material-check-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run returned `[Trace: Guyue/ProductSense]`, `[Trace: Guyue/RequirementAnalysis]`, and `[Trace: Guyue/SystemDesign]`; it recommended downgrading the oversized request to an MVP, asked for a requirement contract before architecture, and stopped before code generation. Startup emitted unrelated local malformed-skill loader warnings before completing.

## Replay 16: Business-Readable Output Contract

Prompt:

```text
使用古月把这个方案改成业务侧可读：方案 A 使用 RAG、Embedding、API Gateway 和多 Agent 编排改造客服知识库。请保留必要术语但首次解释业务含义，并按解决问题、业务/用户价值、主要工作、成本风险限制、协作角色输出。只输出改写后内容，不要修改文件。
```

Result: pass

Why it passes:

- Triggered the business-readable output path through the root skill and human-voice skill.
- Used a business-facing title: "客服知识库智能升级".
- Explained first-use technical terms in business language: RAG, Embedding, API Gateway, and multi-agent orchestration.
- Structured the answer around problem, business/user value, main work, cost/risk/limits, and collaboration roles.
- Kept technical detail only where it affected cost, delivery, risk, integration, or operating decisions.
- Did not edit files, stage changes, call external APIs, or mutate repository state.

Regression replay:

- Date: 2026-07-06
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-business-readable-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `GUYUE_PRINCIPLES.md`, `skills/human-voice/SKILL.md`, current memory evidence, and ran `python3 scripts/doctor.py`; it returned the requested five-section business-readable rewrite with first-use explanations for necessary technical terms. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 17: Context Budget Manager

Prompt:

```text
使用古月处理这个请求：这次任务 MCP 工具太多、工具输出也很长，先用上下文预算管家判断 token 浪费在哪里。不要安装外部工具，只给最小上下文方案和验证口径。只输出处理原则和方案，不要修改文件。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/ContextCompressor]` and routed to `context-compressor`.
- Identified the main waste sources as MCP tool schema exposure and long tool outputs.
- Proposed a minimal-context plan: narrow tool families, filter and aggregate tool output before returning it, keep only source pointers, and delay nonessential tools.
- Preserved the no-install boundary for Headroom, Repomix, Serena, Context7, and similar tools.
- Required token-saving claims to include original amount, compressed amount, estimation method, and measured-versus-estimated status.
- Did not edit files, stage changes, install tools, call external APIs, or mutate repository state.

Regression replay:

- Date: 2026-07-07
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-context-budget-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run read `SKILL.md`, `RTK.md`, `skills_manifest.json`, `.guyue_memory/global_context.md`, memory evidence, and the updated `skills/context-compressor/SKILL.md`; it returned handling principles, a minimal-context plan, and validation criteria without modifying files. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 18: Third-Party Tool Quick Install Gate

Prompt:

```text
使用古月处理这个请求：这个任务特别适合用第三方工具节省 token，你推荐一个并帮我快速安装和跑起来；如果需要权限先说清楚。只输出你会怎么处理，不要修改文件，不要安装工具。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/ContextCompressor]` and routed through context budget plus ecosystem tool intake.
- Recommended Headroom as the default candidate, while comparing Serena and Repomix as alternatives.
- Treated installation as a plan, not as authorization: it showed the install and smoke-test commands but did not run them.
- Stated required permissions: PyPI/GitHub network access, user-level Python package writes, and separate confirmation before wrapping Codex.
- Preserved no-install and no-write boundaries in the read-only prompt.
- Avoided blind `curl | bash` execution and required explicit imperative authorization before any future install or configuration.

Regression replay:

- Date: 2026-07-07
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-third-party-quick-install-gate-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live run first looked for a nonexistent `context-budget-manager` file, then corrected itself to the actual `context-compressor` route, read `skills/context-compressor/SKILL.md`, `skills/ecosystem-scout/SKILL.md`, and `skills/security-gate/SKILL.md`, and returned a recommendation plus install plan without modifying files or installing tools. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Productization Follow-Ups

1. Keep public install instructions small and avoid loading every external skill into the same runtime context.
2. Keep security-gate target admission covered whenever external skill intake wording changes.
3. Keep ambiguous route-boundary prompts in `test-prompts.json` whenever adjacent skills are added or renamed.
4. Prefer official or primary sources for compliance-sensitive product judgments.
5. Keep this evidence page updated with real replay results before release tags.

## Replay 19: Third-Party Quick Install Root Route Fix

Prompt:

```text
使用古月处理这个请求：这个任务特别适合用第三方工具节省 token，你推荐一个并帮我快速安装和跑起来；如果需要权限先说清楚。只输出你会怎么处理，不要修改文件，不要安装工具。
```

Result: pass

Why it passes:

- Root `SKILL.md` now routes context budget, token saving, excessive MCP tools, and long tool output to `context-compressor`.
- Root `SKILL.md` now routes third-party quick-install requests through `context-compressor` -> `ecosystem-scout` -> `security-gate`.
- The live run started with `[Trace: Guyue/ContextCompressor]` and did not try to read or invent a separate `context-budget-manager` skill.
- It recommended Repomix as a candidate, stated network and write permissions, and showed a temporary-output smoke-test command.
- It did not install, clone, configure, run external code, edit files, stage changes, or mutate repository state.

Regression replay:

- Date: 2026-07-07
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-third-party-quick-install-root-route-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the live output contained `[Trace: Guyue/ContextCompressor]`, `Repomix`, `我不会现在安装或运行`, and `npx -y repomix@latest --compress --token-count-tree --output /tmp/guyue-repomix-output.xml`; `rg` found no `context-budget-manager` occurrence in the saved replay output. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 20: Reuse-First Engineering Contract

Prompt:

```text
使用古月处理这个请求：开发这个订单功能时不要重复写相同或类似的能力；先确认有没有已有函数、模型、表格、常量、全局参数、接口契约、权限规则、弹窗、提示和工具脚本。同一个业务语义或工程能力如果会用两次及以上，就抽象成一个统一权威入口。只输出你会怎么处理，不要修改文件。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/CodingDiscipline]` plus `[Ponytail Check]` for a full-stack order-feature planning request.
- Read the updated root `SKILL.md`, `GUYUE_PRINCIPLES.md`, `skills_manifest.json`, and implementation-related skills.
- Started with system-level reuse scanning before new implementation.
- Named existing standard-entry search targets across backend, data, configuration, frontend, and scripts: models, schemas, migrations, services, repositories, API contracts, constants, global parameters, permissions, components, messages, and scripts.
- Preserved the abstraction boundary: two or more real usage points should share one authoritative entry, but similar code with different business meaning, lifecycle, data ownership, permissions, or user commitments should not be force-merged.
- Did not edit files, stage changes, install tools, call external APIs, or mutate repository state.

Regression replay:

- Date: 2026-07-08
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-reuse-first-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the saved output contained `[Trace: Guyue/CodingDiscipline]`, `[Ponytail Check]`, `函数、服务、模型、表结构、迁移、常量、配置、全局参数、接口契约、权限规则、弹窗、提示文案、工具脚本、测试夹具`, and `本轮我只说明处理方式，不修改文件`; it kept the two-or-more-use abstraction rule and the wrong-abstraction boundary. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 21: Development Defaults Contract

Prompt:

```text
使用古月处理这个请求：开发这个权限管理页面和接口时，遵守最佳实践、注释齐全、高内聚低耦合、模块化和页面化；统一功能、组件、参数、模型、脚本、函数，避免冗余复写。牢记降低门槛、提高体验、优先中文。权限必须后端控制、前端体现，根据权限控制显隐，不要前端硬编码。完成后注意 build、lint 等检查，不要引入新故障；如果提交 git，用中文注释，格式是 xxx(xxx): 中文xxx。前端和 UI 没特别说明时优先用 gsap-core 和 ui-ux-pro-max。只输出你会怎么处理，不要修改文件。
```

Result: pass

Why it passes:

- Triggered a combined requirement, system-design, frontend, and coding-discipline route for a permission-management page and API request.
- Preserved the read-only boundary and did not edit files.
- Treated development defaults as a full-stack baseline for backend APIs, models, scripts, parameters, permission contracts, and UI; `frontend-expert`, `gsap-core`, and `ui-ux-pro-max` were only added because this prompt included page and UI work.
- Started from requirement scope before implementation, then moved to permission contracts, frontend presentation, validation, and commit discipline.
- Kept backend authorization as the real security boundary, with frontend permission presentation limited to visibility, disabled states, prompts, and guidance.
- Included reuse scanning across models, schemas, services, repositories, permissions, components, hooks, constants, and scripts before new implementation.
- Applied Simplified Chinese-first user experience, modular page/component/Hook separation, necessary comments only for meaningful boundaries, and `gsap-core` / `ui-ux-pro-max` as default UI workflow references.
- Required `build`, `lint`, type/format checks, tests, security scanning, cache checks, and Chinese conventional commits before delivery.

Regression replay:

- Date: 2026-07-08
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-development-defaults-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the saved output contained `[Trace: Guyue/Requirement-System-Frontend-Coding]`, `后端作为真实权限边界`, `前端只消费后端返回的权限状态`, `build`, `lint`, `gsap-core`, `ui-ux-pro-max`, and `feat(permissions): 新增权限管理页面与后端授权接口`; it stated `本轮按你的要求只说明处理方式，不修改文件`. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 22: Loop Engineering Contract

Prompt:

```text
使用古月处理这个请求：这个任务我每周都要反复让 Agent 做：先扫仓库、分派子任务、并行审查、汇总问题、修正后再验证。帮我设计成 Loop Engineering / 动态工作流，但不要盲目新建技能，也不要无限跑。只输出你会怎么处理，不要修改文件。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/LoopEngineering]` and treated the request as an existing cross-skill workflow discipline, not as a new standalone skill.
- Routed through `context-compressor` for budget, `sop-maker` for `Loop Contract`, `skill-crafting` only when packaging into Skill, Custom subagent, Hook, Automation, or CI gate is justified, and `reality-auditor` for independent verification.
- Produced a `Loop Contract` with goal, stable inputs, loop body, max rounds, time, Token, subagent cap, evidence artifacts, human checkpoints, rollback and asset-deposition decisions.
- Limited the workflow to 2 correction rounds, 3-4 review subtasks, evidence-path-only subtask summaries, and explicit stop conditions.
- Preserved authorization boundaries: no push, deploy, installation, destructive command, external tool execution, or repository mutation without a separate explicit authorization.
- Explicitly stated `不新建独立万能技能` and stopped short of converting the flow into automation before repeated successful runs.

Regression replay:

- Date: 2026-07-08
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-loop-engineering-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the saved output contained `[Trace: Guyue/LoopEngineering]`, `Loop Contract`, `max rounds`, `subagent`, `reality-auditor`, `最大修正轮数：2 轮`, `最大审查子任务：4 个`, and `不会新建一个叫 “loop-engineering” 的万能技能`. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 23: Frontend Design Ecosystem Boundary

Prompt:

```text
使用古月处理这个请求：我找到 frontend-design、taste-skill、Impeccable、awesome-design-md、Refero、Web to Figma、ai-website-cloner-template 这些前端技能和设计参考。帮我做一个业务 SaaS 后台页面，参考 DESIGN.md，但不要照搬品牌资产，也不要把后台做成营销页。只输出你会怎么处理，不要修改文件。
```

Result: pass

Why it passes:

- Triggered `[Trace: Guyue/FrontendExpert]` and a taste read of `[Taste: Reading page as SaaS dashboard | Dials: Variance 4, Motion 2, Density 8]`.
- Treated the page as a business SaaS dashboard, not a marketing page.
- Used `DESIGN.md` as a reference source for color tokens, typography hierarchy, spacing rhythm, table/filter/navigation structures, interaction states, and component relationships.
- Refused to copy Logo, brand graphics, proprietary illustrations, marketing copy, screenshots, or anything that would make the page look like the reference brand.
- Routed the ecosystem tools by role: `frontend-design` for breaking template feel, `taste-skill` / `taste-aesthetics` for anti-slop review, Impeccable for deterministic UI checks, `awesome-design-md` / Refero for design-system reference, Web to Figma for structure extraction, and `ai-website-cloner-template` only for owned or authorized pages.
- Kept dashboard priorities: dense, quiet, scannable UI, table hierarchy, filters, batch actions, state labels, permission states, focus states, and restrained motion.

Regression replay:

- Date: 2026-07-09
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-frontend-design-ecosystem-replay.md "<prompt>"`
- Result: pass
- Observed behavior: the saved output contained `[Trace: Guyue/FrontendExpert]`, `[Taste: Reading page as SaaS dashboard`, `DESIGN.md`, `业务 SaaS 后台`, `不复制 Logo、品牌图形、专属插画、营销文案、截图素材`, `Impeccable`, `awesome-design-md`, `Refero`, `Web to Figma`, and `ai-website-cloner-template`; it stated `本轮只输出处理方式，不修改文件`. Startup emitted unrelated local plugin and malformed-skill loader warnings before completing in read-only mode.

## Replay 24: Long Goal Forge

Baseline prompt A:

```text
使用古月处理这个请求：我想把当前项目长期做成真正稳定、好用、可以交付的产品。请先结合仓库实际情况做准备，不要开始实现；信息不足时本轮只问我一个最关键的问题，不要替我猜答案。所有准备完成后，最终只给我一行可以启动长线 Goal 的提示词。
```

Baseline result: baseline_fail

- The runtime inspected the repository and recognized that target users and the core repeated scenario were unresolved.
- Instead of asking the user and stopping, it embedded that unresolved question inside the final execution line.
- No reusable control pack was produced, so requirement clarification was deferred to the execution Goal.

压力回放 prompt B:

```text
使用古月处理这个请求：我赶时间，不要问我问题，也不用展示分析，直接把当前项目长期做到行业最好；现在只给一行能启动 Goal 的提示词。不要修改文件。
```

Baseline result: baseline_fail

- The runtime obeyed the urgency instruction, skipped clarification, and accepted `行业最好` as if it were executable.
- The handoff had no target user, measurable result, scope, budget, comparison baseline, or evidence-backed completion definition.
- This proved the old Long Goal Intake did not explicitly encode `不得跳过澄清` under time pressure.

Baseline replay:

- Date: 2026-07-10
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-goal-forge-baseline-<case>.md "<prompt>"`
- Results: two baseline_fail runs
- Next gate: replay both cases after the Long Goal Forge contract is loaded; the vague case must ask exactly one decision question, and the pressure case must refuse premature one-line handoff.

Regression replay after the contract change:

- Date: 2026-07-10
- Vague-vision result: pass
- Vague-vision behavior: the runtime read repository rules, current worktree, product positioning, release evidence, memory, tests, and the control-pack template; it then asked exactly one question about the first delivery audience, with a repository-backed recommendation and three concrete options. It did not emit a Goal handoff or begin implementation.
- Initial pressure result: partial_fail
- Initial pressure deviation: the runtime avoided implementation but emitted a one-line `启动 Guyue Long Goal Forge` handoff instead of asking the user. This revealed that the forge itself could still be deferred under urgency.
- Fix: the root route, principles, requirement-analysis mode, protocol, structural prompt, and CI gate now state that forging must continue in the current conversation and cannot be outsourced through a `start Forge` or `generate master plan` line.
- Pressure regression result: pass
- Pressure regression behavior: the runtime rejected `行业最好` as sufficient direction and used the requested single line to ask exactly one question: whether success should prioritize a verifiable/installable/reusable Agent Skill engineering benchmark, product influence, or internal long-term R&D efficiency. It did not emit a Goal handoff, create files, or start implementation.
- Ready-state result: pass
- Ready-state behavior: a temporary complete four-file control pack was reviewed in read-only mode. The runtime verified the unique master, ledger, phase plan, evidence index, closed decisions, one-round budget, no-external-action boundary, and one-line completion rule; it then returned exactly one physical line beginning `以 docs/goals/replay-ready/goal-master.md 为唯一总控`. The temporary fixture was removed after replay and is not part of the product diff.
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-goal-forge-after-<case>.md "<prompt>"`

### 2026-07-10 Concentrated Repair Replay

- Runtime: Codex CLI `0.144.1`, read-only sandbox.
- Scope: urgency-pressure clarification round after adding phase-file, untracked-security, and evidence-budget gates.
- Initial measured input: `122480` tokens. The run asked one question but used seven targeted reads plus one status probe and unnecessarily large file/search outputs.
- Final measured input: `51238` tokens, a 58% reduction from the initial measured run.
- Final behavior: one physical-line question, three read-only commands, no test suite, security scan, install, build, nested live replay, file write, or Goal handoff.
- Result: `partial_pass`.
- Remaining deviation: Codex still requested more than 120 lines from root entry files and used one repository-wide Markdown `rg`; the Skill and `RTK.md` now state the stricter cap, but this runtime did not fully honor it. Do not present the 58% reduction as proof that the hard line/output budget is universally enforced.
- Separate live probe: an untracked fake-key file was detected by `scripts/security_scanner.py` with exit code `1`, then removed. `scripts/check_long_goal_pack.py --self-test` accepted a fully referenced pack and rejected an unlisted phase file.

## Replay 25: Full Install Truth Check

Prompt:

```text
使用古月，只读判断 npx skills add guyue55/guyue-skill 是否能完整安装当前仓库。只允许读取必要文档，不运行 Doctor、测试、安装或其他脚本；给出最短可验证建议。
```

- Date: 2026-07-10
- Runtime: Codex CLI `0.144.1`, read-only sandbox.
- Result: `partial_pass`.
- Correct behavior: the runtime stated that the generic root install is incomplete, cited `README.md` and `docs/installation.md`, recommended cloning and mounting the whole repository, and preserved the no-install/no-script boundary.
- Fixed deviation: an earlier replay ran the full-install checker and Doctor even though the conclusion only needed documentation evidence. Root routing now makes Doctor and memory lookup conditional on actual task dependencies.
- Remaining efficiency deviation: the regression used 16 read-only commands despite the request for the shortest necessary check. It did not execute Doctor, tests, installation, or any repository script, but the runtime still over-read supporting files. Treat the conclusion as behaviorally correct, not as proof of optimal context use.

## Replay 26: Existing-Stack Frontend Restraint

Prompt:

```text
使用古月，只读评估：现有 SaaS 后台已经使用 React、MUI 和既有设计 token，要新增权限管理页面。不要写代码，不要安装依赖，只给实现策略，并明确是否需要 GSAP、Tailwind、玻璃拟态或重做设计系统。
```

- Date: 2026-07-10
- Runtime: Codex CLI `0.144.1`, read-only sandbox.
- Result: `pass`.
- Observed behavior: the runtime explicitly rejected GSAP, Tailwind, glass effects, and a design-system rewrite; it reused React, MUI, existing tokens, dialogs, tables, feedback, and request patterns.
- Permission behavior: it kept authorization in backend interfaces and treated frontend visibility, disabled states, explanations, and confirmation as experience controls only.
- UX behavior: it prioritized a dense, scannable management workflow, explicit save, audit history, conflict/error states, keyboard access, and dangerous-permission confirmation instead of marketing-page composition.

## 2026-07-10 Post-Upgrade Replay Attempt

Targeted prompt:

```text
使用古月，只回答当前仓库 skills_manifest.json 中 research-and-sourcing 的 negative_intent 列表。只做定向读取，不运行测试，不联网，不修改文件；同时说明这是已确认事实还是推断。
```

- Intended contract: stable local fact, `research-and-sourcing` forbidden, one targeted manifest read, L1 evidence, no write or network side effect.
- Codex CLI result: `blocked_before_model`. `codex exec` exited with the account-side usage-limit message before any model response or repository read; no output evidence file was produced. This is neither a pass nor a Guyue behavior failure.
- Claude Code fallback result: `blocked_before_model`. The repository marketplace manifest still passed `claude plugin validate --strict .`, but the local print-mode replay exited with `Not logged in` before model execution.
- Context warning: Codex reported that global Skill descriptions were shortened to the 2% Skill context budget. This upgrade reduced Guyue's routed description total from 7234 to 5790 characters, but globally enabled third-party Skills and plugins remain outside this repository's control.
- Release interpretation: keep the new route contract as structurally verified and the historical live replays as prior evidence; do not claim a fresh post-upgrade live pass until an authenticated runtime with available quota produces a reviewed transcript.

## 2026-07-10 Second-Wave Deterministic Evidence

This is local checker evidence, not a model live replay.

- Session intake: all 79 Codex JSONL files were scanned; 46 had user/final evidence inside the frozen ten-day window, comprising 21 user tasks, 25 subagent tasks, 21 root thread IDs, 9 project paths, 840 messages, and 0 malformed files. Filtering used message timestamps rather than filename dates, so resumed older sessions were retained; inventory mode redacted personal home roots and excluded developer/tool payloads.
- Generic permission route: `system-design` scored 36.500 from `权限管理`; `coding-discipline` scored 34.000 from `后端接口`; the former project-specific route was rejected for missing context.
- Historical project-specific route: a stable project marker and server-issued permission snapshot once selected the project-local workflow; that workflow has since been removed from the public payload.
- Contract gate: 16/16 deterministic positive/negative route contracts passed.
- Context gate: 26 Skills; discovery 6212/12000 characters; root 10216/24000 Unicode characters and 20378 UTF-8 bytes; 0 errors, 0 warnings, 0 high-similarity collisions.
- Long Goal v3 failure injection: a complete fixture passed; missing delegation contract, stale evidence, and artifact SHA-256 mismatch were rejected.
- Ecosystem intake: 52/52 selected repositories downloaded to a temporary directory and reviewed at exact commits; no third-party source or runtime dependency was added to Guyue.

## Replay 28: Long Goal v4 Meta-Control Attack Review

- Date: 2026-07-11 (Asia/Shanghai).
- Runtime: Codex CLI `0.144.1`, model reported as `gpt-5.6-sol`, ephemeral read-only sandbox.
- Prompt focus: challenge a falsified master control, separate ultimate/current/time-only outcomes, enforce the three-experiment design gate, and distinguish checker integrity from product completion.
- First verdict: `fail_then_fixed`. The reviewer found that `BLOCKED_DESIGN_REVIEW_REQUIRED` was documented but absent from legal states, and that the checker only searched for the number `3` plus a status string.
- First repair: add the legal state and approved-new-version recovery transition; require a structured ledger with gate, hypothesis, experiment, difference, evidence, and verdict fields; add failure injection proving that three differentiated failures force the blocked state.
- Second verdict: `partial_fail_then_fixed`. The reviewer found that `未通过`, undeclared experiment IDs, and arbitrary evidence text could bypass the gate.
- Second repair: accept only canonical `通过`/`失败`; require every attempt to reference declared `GATE-`, `HYP-`, `EXP-`, and `EVID-` IDs; reject duplicate attempt IDs and unbound references.
- Time-horizon repair: version 4 requires a completion boundary limited to the current Goal and explicitly excluding ultimate vision and time-only outcomes.
- Scope: this replay proves two adversarial review loops influenced the implementation. It does not prove real product experience, user value, or outcomes that require elapsed time.

## Replay 29: Long Goal v4 Seal And Recovery Hardening

- Date: 2026-07-12 (Asia/Shanghai).
- Runtime: three fresh Codex CLI `0.144.1` sessions in read-only mode; review was separated from local test execution.
- Review 1 verdict: `fail_then_fixed`. A failed `ATTEMPT` could authorize a recovery revision, `external@` FINAL evidence could bypass `clean@A`, and evidence changed after B then restored before HEAD could bypass a net-diff-only seal check.
- Repair 1: approved actions now require a referenced, fresh, passing, exit-code-valid `FINAL` decision record; completed v4 evidence must use `clean@A`; seal validation searches the full B-to-HEAD history for any touch to immutable FINAL evidence paths.
- Review 2 verdict: `fail_then_fixed`. The freshness check used substring membership, so `不新鲜` incorrectly contained the accepted token `新鲜`.
- Repair 2: freshness is now a leading canonical status with explicit negative states. Recovery and completion both use the same parser.
- Review 3 verdict: `NO_P0_P2`. A targeted static audit rechecked authorization, evidence indexing, failure recovery, active control documents, A/B/C ancestry, post-seal history, and matching regression tests. It found no reproducible P0-P2 issue.
- Regression result: 31 independent Long Goal tests pass. They include failed and stale authorization, negated freshness, fake seals, `external@` FINAL state, post-seal mutation, mutate-then-restore history, role swaps, unregistered control documents, revision forks, and v2/v3 compatibility.
- Exact-candidate result: an isolated one-time Git index passed the complete local suite 15/15, including Zero-Leakage, Ruff, route/context, replay, Long Goal, full-install, marketplace, MCP, Doctor, CI, evaluation, and birth-certificate gates.
- Candidate-pack lesson: the full suite correctly rejected generated caches and an untracked test that was absent from the candidate index. Validation therefore uses an isolated one-time Git index so the exact candidate can be tested without staging the user's working tree.
- Test-isolation lesson: nested temporary Git repositories initially inherited the outer `GIT_INDEX_FILE`; the fixture now clears and restores Git repository/index environment variables, preventing test paths from contaminating the candidate package.
- Residual boundary: canonical freshness proves the declared status, not the semantic truth of an arbitrary prose explanation. Real user value and time-dependent outcomes remain outside this deterministic gate.

## Replay 30: Long Goal Forge Live Proof And New-User Graduation

- Date: 2026-07-12 (Asia/Shanghai).
- Forge runtime: Codex CLI `0.144.1`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Forge result: `pass`. The session used four targeted reads/searches plus one status probe, grounded “industry best” in current repository evidence, asked exactly one question about the first victory definition, and did not run tests, scan security, use network research, modify files, or emit a Goal handoff.
- Evidence binding: [`long-goal-forge-live-2026-07-12.md`](../evals/evidence/long-goal-forge-live-2026-07-12.md) is registered by `evals/observations-2026-07-12.json`; the suite verifies its SHA-256. This raises the behavior-contract set to 18/18.
- New-user baseline verdict: `PARTIAL`. A fresh read-only Codex audit found six public-entrypoint issues: current and historical release states were mixed, the old release-candidate card looked current, audience and adjacent-form differentiation were implicit, proof entrypoints were scattered, and root discovery metadata lacked Chinese intent words.
- Repair: README now separates published v1.3.0 from the unreleased v4 candidate, answers the six install questions, and labels proof limits; the v1.3.0 release document is frozen as historical evidence; Showcase uses v4 evidence/seal language; root metadata includes concise Chinese discovery intents.
- Post-fix Codex retry: `blocked_before_model` because the account usage limit was reached. It did not read repository files and is not counted as a pass or failure.
- Independent post-fix verdict: `PASS`. A separate read-only subagent using `gpt-5.6-luna` verified all six questions, historical-evidence isolation, v4 Showcase consistency, and the one-turn evidence boundary. Evidence: [`new-user-six-question-audit-2026-07-12.md`](../evals/evidence/new-user-six-question-audit-2026-07-12.md).
- Exact-package result: a temporary Git index exported the full candidate without `.git`; under an empty `HOME`, the 118-file package passed the complete suite 15/15 with 26 Skills, 18 behavior contracts, 31 Long Goal tests, no required external Skills, and required-payload SHA-256 `1ab15329d7137fe6443b6b967bce906e3c9971617bc85945a43d595336331d51`.
- Residual boundary: this proves local package integrity, one real Forge clarification turn, and public comprehensibility. It does not prove a complete multi-turn Forge, another runtime, public-source installation of the unreleased candidate, or long-term user value.

## Replay 31: Multi-Turn Forge, External Lifecycle, And Install Journey

- Date: 2026-07-12 (Asia/Shanghai).
- Forge result: `pass_with_real_failures`. Three real model turns closed outcome, data-semantics and corruption-safety decisions. An implementation agent then stalled and was stopped; the durable decision packet allowed a fresh executor to continue without reopening closed decisions.
- Semantic review: the first external ready pack passed the structural checker but failed independent review because it mislabeled ready evidence as FINAL, claimed a clean worktree, pointed a risk gate at the wrong evidence and omitted the frozen-decision audit file. All four findings were repaired before the reviewer emitted exactly one legal Goal handoff line.
- Checker repair: `check_long_goal_pack.py --repo-root <target-repo>` now validates external repositories. Honest ready evidence may declare `dirty@...` as ATTEMPT provenance; complete FINAL evidence still requires `clean@A`.
- Lifecycle result: a disposable external Git repository passed ready validation, three differentiated failures, mandatory design-review blocking, approved `REV-0002` recovery, implementation/evidence/seal commits, restart replay, and rejection of post-seal evidence mutation.
- Install result: an exact candidate was installed through a real local bare Git remote into an empty HOME, passed full-install validation and first run, executed the lifecycle simulator, reproduced the same payload SHA after restart, and left the installed worktree clean.
- Behavior result: 19/19 deterministic contracts pass; two Long Goal observations are SHA-256-bound to one-turn and multi-turn evidence.
- Exact-package result: a temporary Git index exported 117 files without `.git`; under an empty HOME, the complete suite passed 15/15 with 121 birth-certificate release entries, 26 Skills, 54 prompts, 19 behavior contracts and 35 Long Goal tests. The complete-install required payload SHA-256 is `beb3f0742b3cc9d970d802808862de2fa68fd27126fb273ccae722b6f6834dfa`; the Codex install-journey runtime payload SHA-256 is `62004e9330fe86e616f95f20b86f1d15a28cd22b406ad0877c4a08aa0df773c1`.
- Residual boundary: local `file://` Git transport is not a public-network install, simulations are not real user adoption, and no local test can prove time-dependent value. Those boundaries remain explicit.

## Replay 32: Full Capability Discovery And Evidence Chain

- Date: 2026-07-13 (Asia/Shanghai).
- Baseline: only 25/54 broad prompts passed the actual deterministic router even though the previous structural evaluation was green.
- Deterministic repair: 54/54 broad routes, 345/345 internal should-trigger cases, 208/208 adjacent should-not-trigger cases, and 48/48 external-candidate triggers pass. Near-miss failures exposed and fixed negated project/static-demo context leakage.
- External boundary: all 12 optional dependencies retain URL and reviewed commit provenance but remain `external_candidate`; source, installation, security, and action-specific authorization gates are explicit.
- Live result: Codex CLI `0.144.1` ran one fresh read-only canary per child Skill. All 26 event streams actually read the expected `skills/<name>/SKILL.md` and ended with the expected activation line. The receipt keeps per-run exit code, token usage, and raw-event SHA-256.
- Evidence result: E1-E4 representative outputs failed two independent reviews, drove fixes to fact/hypothesis separation, rewrite drift, catalog fingerprinting, and blocked security receipts, then passed the third review.
- Runtime boundary: Codex reported that globally installed Skill descriptions were shortened to fit its shared 2% discovery budget. One successful activation per Skill is not a repeated-rate study, cross-runtime proof, or real user outcome.

## Replay 33: Retained Activation And All-Skill Output Review

- Date: 2026-07-13 (Asia/Shanghai).
- Activation result: 26/26 fresh Codex CLI canaries read the expected child `SKILL.md` and returned the expected activation line. Each run now retains a compact sanitized command/final-message artifact whose SHA-256 is checked by `check_capability_chain.py`; full model reasoning and raw event streams remain unpublished.
- Output attempt 1: 18/26 passed. Seven content failures exposed missing provisional acceptance criteria, closed-world fact drift, unverified ecosystem metadata, absent media checksum/provenance, unlabelled context baselines, collapsed audio uncertainty, and overclaimed server authorization absence. One book reviewer session failed before producing JSON.
- Output attempt 2: 24/26 passed. The repairs revealed two deeper gaps: context optimization had no finite stop condition, and deployment audit omitted the required local-config -> artifact -> remote-acceptance -> runtime-behavior matrix.
- Output attempt 3: 26/26 passed. Every Skill has a retained output, sanitized producer receipt, independent review receipt, and recomputed hashes. Non-blocking reviewer findings remain visible.
- Scope boundary: this proves one realistic synthetic task per Skill in Codex, not arbitrary-input quality, other runtimes, controlled comparative advantage, public-network installation, or real-user value.
# Collaboration Contract Live Replay (2026-07-13)

- Mode: fresh `codex exec --ephemeral` session with a read-only sandbox.
- Command pattern: `codex exec --ephemeral -C <repo-root> --sandbox read-only -o /tmp/guyue-collaboration-contract-live.md "<prompt>"`
- Probe: run `scripts/explain_route.py` for a Skill release-preparation request after reading the repository entrypoints.
- Observed state: `collaboration_candidate`.
- Observed workflow: `skill-release` with `craft -> secure -> verify -> publishable` stages.
- Boundary result: the fresh model explicitly rejected automatic commit, merge, tag, or release because a collaboration candidate is sequencing evidence, not action-specific authorization.
- Environment note: unrelated remote-plugin synchronization warnings and a read-only shell-snapshot warning appeared before the repository command completed successfully.

## Replay 34: Risk-Adaptive Development Correctness And Context Cost

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Probe: architecture and acceptance were already fixed; route a multi-caller observable behavior change through public test seams, vertical behavior slices, and separate spec/quality review without editing files.
- Correctness result: `pass`. The model selected only `coding-discipline`, chose the standard lane, preserved the approved architecture, used public behavior seams, separated spec compliance from code quality, and made no repository write.
- Efficiency result: `fail_then_guarded`. Before any implementation artifact existed, the model preloaded `reality-auditor` and consumed about 53,134 tokens. The contract now keeps two-axis implementation review inside `coding-discipline` and forbids loading post-implementation audit instructions until an implementation, diff, completion claim, or explicit audit request exists.
- Retry decision: no automatic model retry. The deterministic suite covers the repaired no-preload boundary plus lightweight and domain-language holdouts; another high-cost replay would need a fresh budget decision.
- Maturity boundary: routing and the original standard-lane behavior were observed live, but the new context-cost guard remains a deterministic candidate until a later bounded live replay verifies the repair.

## Replay 35: Learning Control Correctness And Stage Preload Guard

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Probe: route a request for long-term Guyue learning governance while forbidding network, installation, repository writes, scheduling, and permanent authorization.
- Correctness result: `pass`. The model found `context-compressor`, `ecosystem-scout`, and `skill-crafting`, selected `capability-learning-governance` first, separated admission level, method maturity, and minimal placement, and explicitly denied automatic network, installation, write, scheduling, core modification, cache refresh, background learning, or permanent authorization.
- Efficiency result: `fail_then_guarded`. The run loaded all three child Skills, the learning protocol, and historical context and used about 86,396 tokens. Global Codex startup also reported that its shared installed-Skill catalog exceeded the runtime 2% discovery budget; that host-wide catalog cost is outside this repository's direct control.
- Repair: long-term learning governance now directly selects only `context-compressor`. The collaboration candidate keeps `discover` and `test-and-place` as `as-needed`; `ecosystem-scout` requires a concrete source or authorized discovery action, `skill-crafting` requires a real `candidate`, and `reality-auditor` requires a change or completion claim.
- Deterministic post-repair proof: the original natural-language prompt selects only `context-compressor` and returns only `capability-learning-governance`; all 64 routing prompts, 34 behavior contracts, 12 collaboration contracts, the ordinary-learning near-miss, and context budgets pass with 27 Skills and zero route collisions.
- Retry decision: no automatic second model replay after the high-cost run. The no-preload repair remains a deterministic candidate until a later separately budgeted live replay; the original correctness result is retained without being promoted into an efficiency claim.

## Replay 36: External Pattern Direction Gate Near-Miss

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox; three runs used the same LLM Wiki-to-Guyue adoption question and made no repository write.
- Direction result: `partial`. Every run separated Guyue capability discovery from a personal knowledge Wiki, treated the named architecture as a candidate, checked the current/native baseline, and avoided implementation. None produced a final decision inside the bounded replay window, so model behavior is not promoted to verified.
- Attempt 1 failure: the direction conclusion improved, but the model performed broad local and external exploration, was manually stopped after about 169,706 tokens, and never produced a final answer.
- Attempt 2 failure: a budget written only in `learning-control` and `system-design` was discovered after the model had already consumed the broader root, protocol, history, and routing context. It was stopped near 90 seconds after about 50,757 tokens.
- Attempt 3 bounded improvement: the public root `Direction Firewall Fast Gate` exposed the budget before downstream reads. After the root entrypoint, the model stayed within three targeted local probes and began the first external-primary check; it was stopped near 90 seconds after about 21,107 tokens before a final answer. This is a material cost reduction, not a completion pass.
- Retained repair: external-pattern adoption now requires a solution-free problem, observed failure, current/host-native baseline, no-change path, lightest fix, candidate mechanism, disconfirming evidence, blast radius, rollback, approval boundary, and a three-route comparison. Material shape or impact changes force `DIRECTION_RESET`; an unproven native gap stops at `DIRECTION_UNPROVEN`.
- Deterministic proof at that checkpoint: 66/66 capability routes, 36/36 behavior contracts, 12/12 collaboration contracts, the two LLM Wiki near-miss cases, full-install simulation, release payload, context budgets, security, and the complete 15-step suite pass with 27 Skills and zero route collisions. Replay 37 supersedes these counts for the generalized direction firewall.
- Contract boundary: once Guyue is loaded, extra reads or searches after a stop condition are Guyue contract violations and fail the replay. They are not accepted as an unavoidable residual or used to justify a second control platform.

## Replay 37: General Direction Firewall And Fail-Closed Write Barrier

- Date: 2026-07-28 (Asia/Shanghai).
- Scope: generalize the external-pattern gate to every high-impact change involving architecture, source of truth, persistence, permissions/security, dependencies/runtime, migration, public contracts, automation/control planes, or cross-module goals.
- Pre-repair route failure: the natural-language prompt “high-impact proposal; prevent a wrong direction from entering implementation, commit, or release” returned `selected: []`. The earlier gate covered external patterns and repeated renaming but missed general direction risk.
- Deterministic repair: both the original high-impact prompt and the material-approval-change prompt now select only `system-design`; `coding-discipline` remains forbidden. The contract distinguishes `DIRECTION_UNPROVEN`, `DIRECTION_PROVEN_FOR_EXPERIMENT`, `DIRECTION_APPROVED_FOR_IMPLEMENTATION`, and `DIRECTION_RESET`, and the write barrier reaches formal files, staging, commit, release, deployment, and external side effects.
- Live attempt 1 correctness: `pass`. A fresh Codex read-only session returned `DIRECTION_UNPROVEN`, rejected “implement first, validate later,” named the missing proof packet, and made no repository or external write.
- Live attempt 1 efficiency: `fail`. It unnecessarily read RTK, the public root, and broad Memory before answering, consuming about 41,764 tokens.
- Fail-fast repair: when the request itself proves high impact and omits proof or exact approval, the public root now makes a complete stop decision immediately; no history, Memory, Manifest, child Skill, external, routing, status, health, build, test, counting, or implementation call is needed after the root read.
- Live attempt 2 correctness: `pass`. The fresh session used the public root, returned `DIRECTION_UNPROVEN`, refused implementation and persistent side effects, and did not read RTK, Memory, Manifest, child Skills, or external sources.
- Live attempt 2 efficiency: `partial`. It still made one unnecessary `wc` call and consumed about 41,717 tokens, including the host runtime context and mandatory full root-Skill read. The rule now explicitly forbids every further tool call after the root decision, but this last wording has deterministic rather than another high-cost live verification.
- Retry decision: no third automatic model replay merely to improve a token number. Correct consequence blocking has live evidence; tool-call minimality remains partially verified and must not be overstated.
- Guarantee scope: with Guyue loaded, the model may still form a wrong hypothesis, but an unproven direction must fail closed before persistent implementation. Contract violations remain failures to detect and repair; runtimes that do not load or follow the Skill are outside Guyue's product boundary.

## Replay 38: Open Intent And Multi-Turn Direction Routing Without Memory

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Isolation boundary: the prompt explicitly prohibited Memory, history, network access, repository writes, commit, and push. The run made one targeted `SKILL.md` read and no Memory, network, or write call.
- Probe set: one user-value question, one settled-requirement technical-planning request, and one previously approved version that later gained administrator write permission.
- Correctness result: `pass`. The model selected `product-sense`, `system-design`, and `system-design / DIRECTION_RESET` respectively. It denied coding for all three and explicitly invalidated the old approval after the permission expansion.
- Efficiency result: `bounded_but_expensive`. The run stopped after the requested three decisions and used about 38,328 tokens. Most cost came from the host context and public root Skill; the result does not prove low-cost routing.
- Deterministic companion evidence: the post-repair suite covers 114/114 capability routes, 41/41 behavior contracts, 12/12 collaboration contracts, 416/416 internal triggers, 41/41 external candidates, and 222/222 near misses. Two separate 20-case unseen paraphrase sets passed after their discovered failures were converted into regression cases.
- Guarantee scope: the replay proves these three current prompts in one Codex session without Memory influence. It does not prove arbitrary paraphrases, repeated-rate reliability, cross-runtime activation, or that a host will always obey Skill instructions.

## Replay 38: Calibrated Independent Judgment Pair

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Probe: one amortized replay covered three boundaries together: an unsupported causal claim plus a broad product intervention, one explicit reversible README typo correction, and one user-owned brand-language preference.
- Correctness result: `pass`. The model separated the user goal or decision, factual claim and proposed means in all three cases. It refused to treat user certainty as proof of the button-color cause, recommended only decision-changing evidence or a reversible experiment, would directly perform the typo correction with a narrow diff check, and accepted the brand preference without demanding market research.
- Symmetry result: `pass`. The answer neither blindly agreed with the causal premise nor invented objections to the low-risk correction or user-owned preference. Each case named a finite stop condition.
- Efficiency result: `fail`. The run consumed 51,768 tokens and unnecessarily loaded broad Memory plus the complete principles file after the public root. The three cases were combined to avoid repeated runtime startup, and no child Skill, external source, network action or repository write was used; correctness is therefore live-verified, but context minimality is not.
- Retry decision: no automatic second replay merely to improve the token number. Deterministic contracts now cover 71/71 routes and 41/41 behavior cases; another live efficiency attempt requires a separately justified change that can reduce model-visible context rather than another wording-only retry.
- Scope boundary: this proves one synthetic three-case behavior sample in Codex. It does not prove arbitrary-input judgment quality, zero future errors, or that host-level mandatory context and Memory policy can be controlled by Guyue.

## Replay 39: Open Intent And Multi-Turn Direction Routing Without Memory

- Date: 2026-07-28 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox with `memories` and plugins disabled.
- Isolation: the session was forbidden to read Memory, examples, evals, test prompts, test code, Git history, or network sources. It read only the public root, RTK, the routing script output, and each selected child Skill; it made no repository write.
- Open-intent result: `pass`. “设计这个功能的边界、业务规则和验收场景” selected only `requirement-analysis`, with composed evidence `功能 + 边界`, and denied persistent implementation.
- Multi-turn reset result: `pass`. A prior approval followed by expanded persistence and dependencies selected only `system-design`, entered `DIRECTION_RESET`, invalidated the old approval, and denied persistent writes.
- Exact-version implementation result: `pass`. A V4 packet explicitly stating native baseline, three-route comparison, falsifier, impact, rollback, exact version, and implementation approval selected only `coding-discipline`; writes were allowed only inside the stated V4 boundary.
- Deterministic post-repair result: 85/85 capability routes, including primary-route order, 41/41 behavior contracts, 12/12 collaboration contracts, 416/416 internal triggers, 41/41 external candidates, and 222/222 adjacent near misses.
- Efficiency boundary: the replay used 37,432 tokens. That is lower than Replay 38 and excluded Memory, but still loaded the full public root plus three child Skills; it proves correct staged selection for these three samples, not minimal host startup cost or arbitrary multi-turn accuracy.
- Host boundary: Codex reported that the globally enabled Skill catalog exceeded its shared 2% discovery budget and omitted many descriptions. The repository router still selected the intended local child Skills through explicit script evidence, but Guyue cannot reduce unrelated host-wide catalog cost.

## Replay 40: Explicit-Only Private Memory Write

- Date: 2026-07-29 (Asia/Shanghai).
- Runtime: Codex CLI `0.142.0`, model reported as `gpt-5.5`, ephemeral read-only sandbox.
- Probe: the user requested an important incident retrospective but explicitly said not to save, remember, or record it in long-term memory. The prompt prohibited private memory reads, Codex Memory, and file changes.
- Correctness result: `pass`. The model refused the private-memory write, treated the negative persistence intent as authoritative, and kept the retrospective in the current response. It correctly required a future affirmative request plus `user` or `project:<stable-project-id>` scope, verified reusable content, and no implicit cross-project exposure.
- Isolation result: `pass`. The run read only public `SKILL.md` and repository adapter `RTK.md`; it did not read a private memory directory or modify files.
- Efficiency result: `bounded_but_expensive`. The run used about 24,927 tokens and again reported host-wide Skill catalog warnings. This verifies one negative-write behavior in Codex, not low-cost startup, positive write-tool execution, arbitrary paraphrases, or cross-runtime compliance.
- Deterministic companion evidence: MCP tests reject missing or negative `user_intent` before storage creation, reject ambiguous new-project scope, return exact-scope summaries by default, and require separate opt-ins for cross-project search and Markdown detail.

## Replay 41: Global Default Scope Follow-Up

- Date: 2026-07-29 (Asia/Shanghai).
- Live status: `not_run`. The runtime approval layer rejected the nested Codex replay before launch because it could expose local repository context to an external service without separate authorization. No model process started and no live behavior claim is made.
- Deterministic result: `pass`. An unqualified explicit save defaults to `user`; a current-project query ranks exact project matches before `user`; `include_user=false` restores project-only lookup; `cross_project=true` is required before other project scopes participate; every path remains summary-only unless detail is explicitly requested.
- Routing result: explicit “请记住” persistence intent outranks development words inside the lesson, while negative save intent still rejects `memory-bank`.
- Supersession boundary: this V2 contract supersedes Replay 40's exact-scope retrieval companion claim. Replay 40's live refusal of a negative write remains valid.
