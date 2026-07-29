# 古月全能力发现、激活与证据链审计方案

日期：2026-07-12
审计对象：根编排能力、26 个内置子 Skill、12 个外部增强依赖、路由器、评测、安装与证据链
基线提交：`54a99ea0791f058da56108495961e9451d76044d`
文档性质：审计结论、实施账本与发布边界；本地修复已实施，但尚未提交或发布

## 1. 结论先行

古月当前的问题不是“少数 Skill 写得不够好”，而是存在三套没有完全闭环的能力系统：

1. Agent Skills 原生发现依赖每个 `SKILL.md` 的 `name + description`。
2. 古月自带确定性路由依赖 `skills_manifest.json` 的 `trigger_intent / negative_intent / required_any_context`。
3. 根编排又依赖根 `SKILL.md` 的自然语言路由表和模型判断。

三者都能单独工作一部分，但没有共同的机器可读能力合同，也没有一套覆盖全部 26 个 Skill 的真实激活评测。因此，“文件存在”“manifest 已注册”“结构测试全绿”“模型曾经用过一次”目前会被误写成同一种完成。

本轮发现四个系统级问题：

- **P0：宽测试集没有真正进入路由门。** `test-prompts.json` 有 54 条样本，但 `run_eval.py` 只检查结构和名称覆盖。按 `expected_behavior` 中的技能名做初筛并调用真实 `resolve_routes()`，54 条中有 30 条至少漏掉一个声明能力。部分标签包含条件性路由，后续需先规范化，但这已经足以证明当前绿灯不能代表宽意图召回。
- **P0：外部增强只是登记，不是古月可执行路由。** 12 个 `external_dependencies` 不在 `resolve_routes()` 的遍历范围内，其中 5 个没有 `trigger_intent`。它们被当前运行时另行安装时可能原生可见，但古月自身并没有完成“外部候选发现 -> 选择 -> 定位 -> 安检 -> 激活”的机器链。
- **P1：证据规则有根层原则，没有按能力继承。** 调研、推荐、安全、记忆、内容蒸馏、视频素材、项目治理等能力对来源和谱系要求差异很大；当前有的 Skill 已有强证据合同，有的只依赖根原则，有的甚至允许“全网经验推荐”却没有来源、时间和检索路径。
- **P1：评测偏向少量精心措辞。** 26 个 Skill 的 259 个自定义触发短语中，258 个能反向选中自身；但换成现有测试中的自然用户表达，多个能力召回归零。这证明触发词自测主要验证配置自洽，不验证真实可发现性。

**总判断：不应逐个堆关键词。** 推荐建立一份统一“能力合同”，让原生 description、古月路由扩展、根曝光策略、证据等级、测试样本和活体观察指向同一能力 ID；再按风险分层补齐 26 个 Skill，而不是让每个文件复制一套庞大的证据模板。

### 1.1 2026-07-13 实施结果

- 54/54 宽意图路由合同通过；原 19/19 行为合同保持通过。
- 345/345 内置 should-trigger 通过，208/208 近邻 should-not-trigger 通过；负例真实发现并修复“无 NexusFlow/static-demo标记”仍误触发的问题。
- 12 个外部增强改为独立 `external_candidates`，48/48 外部触发只进入候选态，不混入内置 selected；每项绑定 URL、commit、证据 profile 和四道激活门。
- 26 个 Skill 全部声明 E1-E4 证据 profile，并由根证据合同机器校验。
- Codex CLI `0.144.1` 对 26 个 Skill 逐项执行真实只读探针，26/26 都实际读取目标 `SKILL.md` 后输出正确激活结果；证据绑定 routing SHA-256、原始事件 hash、退出码和 token。
- 26 个激活探针均保留脱敏命令与最终消息工件，门禁可独立反算 hash 并确认目标 `SKILL.md` 实际读取。
- E1-E4 输出语义经过三轮 failure-first 回放：前两轮 FAIL 触发修复，第三轮由独立审查判定四档全部 PASS。
- 26 个 Skill 逐项完成一个现实型合成任务和独立审查：首轮 18/26、二轮 24/26、三轮 26/26；七条能力规则修复与一次 reviewer 重试均保留在收据历史中。
- 第三轮输出和独立审查原文已从临时产物恢复为可分发工件；门禁会反算工件 SHA-256，不再只相信收据字段。
- v1.4.0 最终精确候选与严格索引出生证明均识别 236 个发布文件，在空 HOME、无 `.git` 环境通过 15/15；不可变身份由最终 commit 与 annotated tag 提供，避免把整树 hash 写回树内造成自指失效。
- 诚实边界：以上证明确定性路由、Codex 激活、四档代表样本和每个 Skill 的一个合成输出，不证明任意真实业务输入、其他 runtime 或长期用户价值。

### 1.2 2026-07-29 复审校正

- 当前基线是 27 个内置 Skill、10 个登记外部候选、114 条结构路由、66 条行为合同、12 条协作合同和 222 条近邻负例；上面的 26/12/19 等数字只保留为历史快照。
- 新版私有本地索引已经接入 CLI、MCP 和首轮验货，路由只返回名称、来源、匹配证据与边界，不返回本机绝对路径或本地描述；旧 `名称 -> 路径` 缓存仅按降级模式读取。
- `external_candidate` 已能作为独立成功候选态返回，不再被 CLI/MCP/验货入口误写成无路由失败。
- manifest 的外部 lifecycle 是必须依次通过的门清单，不是持久状态机。仓库当前没有保存 `source_checked -> installed -> security_checked -> authorized -> activated` 的迁移状态；每一步仍需单独动作收据。
- 行为合同的确定性门只执行路由断言。`required_actions` 与 `forbidden_side_effects` 当前执行证据为 `0/66`，不得由 66/66 路由绿灯替代。
- 旧模型激活和逐 Skill 输出质量收据未绑定当前路由/Skill 哈希时，相关 claim 必须为 `false`；开发门只警告，严格发布门阻断。

## 2. 审计口径

### 2.1 六段能力链

| 环节 | 真正成立的判据 | 不能代替它的东西 |
|---|---|---|
| D1 可发现 | 安装后的运行时目录中能看到 Skill，且 frontmatter description 能表达“做什么、何时用、何时不用” | 文件在仓库里 |
| D2 可选择 | 真实用户表达能让古月路由选中正确 Skill，并压住相邻误触发 | 手工输入 manifest 原样触发词 |
| D3 可激活 | 运行时确实加载目标 `SKILL.md`，不是模型凭常识完成 | 路由器打印候选名 |
| D4 可执行 | Skill 的步骤、脚本、资源、权限和失败回退在目标环境可运行 | 文档描述完整 |
| D5 可证明 | 输出绑定输入、来源、动作、时间、版本、验证和诚实边界 | “已完成”“测试通过”文字 |
| D6 可安装复现 | 无开发仓库上下文、空 HOME 或目标运行时安装后仍能走完 D1-D5 | 当前作者机器可用 |

### 2.2 状态标记

- `✅ 已建立`：现有证据已覆盖该链路，不只是待办。
- `🟡 部分成立`：静态合同存在，但自然路由、活体激活或证据链仍缺一段。
- `🔴 当前未建立`：现有证据不能证明链路成立，或已复现明确断点。
- `⬜ 待执行`：本方案提出、尚未实施。
- `🚫 不适用`：能力性质不需要该项，必须写明原因，不能用来逃避验证。

## 3. 已完成的审计清单

- [x] 读取根入口、运行时规则、manifest、路由器、评测器、行为合同和安装门。
- [x] 枚举 26 个内置子 Skill，并核对目录、frontmatter、manifest、README 和测试样本。
- [x] 核对 259 个内置触发短语的自身召回：258/259；唯一明确失败是 static demo surface 的 `Demo/index.html` 触发与上下文门不一致。
- [x] 将 54 条现有测试 prompt 初步回放到真实确定性路由器，记录每个能力的声明命中率。
- [x] 核对 19 条行为合同：只有 12 个 Skill 被正向合同直接覆盖。
- [x] 核对已登记 observations：只有 `reality-auditor`、`requirement-analysis`、`system-design`、`coding-discipline`、`taste-aesthetics` 出现过观察路由。
- [x] 核对 12 个外部依赖：路由器不读取 `external_dependencies`，5 个条目没有触发意图。
- [x] 按 Skill 内容检查证据、来源、事实状态、产物、失败和新鲜度规则的分布。
- [x] 查阅 Agent Skills 官方发现/激活规范、触发评测指南、输出质量评测指南和 W3C provenance 模型。
- [x] 修复能力合同、路由、评测、证据继承和外部依赖候选链。
- [x] 对 26 个 Skill 完成 Codex 真实运行时激活回放，并完成 E1-E4 代表输出的失败优先验收。
- [ ] 完成其他 runtime 与公开来源安装；空 HOME 精确候选包终验在本轮 M5 执行。

## 4. 根能力审计

| 根能力 | 当前状态 | 证据 | 主要缺口 |
|---|---|---|---|
| 原生安装与 26 Skill 枚举 | ✅ 已建立 | 完整安装检查、空 HOME 本地 Git 克隆、当前 Codex 能枚举 26 个子 Skill | 仍需公开来源和其他运行时的新候选证据 |
| Long Goal Forge | ✅ 已建立 | one-turn/multi-turn 观察、19 号行为合同、外部项目 ready 检查 | 真实用户长期价值仍属于现实边界 |
| Long Goal Intake 与恢复 | 🟡 部分成立 | 连续失败/阻塞/批准恢复/A-B-C/重启模拟 | 尚缺真实长期项目的完整结果与用户反馈 |
| Material Check / 上游质疑 | 🟡 部分成立 | 根原则和产品/需求 Skill 均有规则 | 自然 prompt 对 `product-sense`、`requirement-analysis` 的确定性召回不成立 |
| 确定性路由与仲裁 | 🔴 当前未建立 | 19 个窄行为合同通过 | 54 条宽样本有 30 条初筛漏路由；外部依赖完全不参与选择 |
| 证据分级与独立判断 | 🟡 部分成立 | 根层 L0-L4、事实/推断/冲突/未知、Long Goal 证据门 | 没有按 Skill 类型继承，执行结果缺统一 receipt |
| 可逆自治与授权 | 🟡 部分成立 | 多条行为合同和根红线 | 尚未覆盖全部高风险子 Skill 的活体副作用回放 |
| Zero-Leakage 与发布卫生 | ✅ 已建立 | 安全扫描、缓存门、候选包门和失败注入 | 公开发布仍需重新取证 |
| Loop Engineering | 🟡 部分成立 | 根路由、`context-compressor`、`sop-maker`、`skill-crafting` 规则 | 没有完整动态循环的跨 Skill 激活观察 |
| 外部生态 Two-Phase Loading | 🔴 当前未建立 | manifest 有 12 个指针、Doctor 可检查安装状态 | 路由器不消费外部依赖，Level 2 只是文档承诺 |

## 5. 26 个子 Skill 逐项清单

“宽样本命中”来自现有 `test-prompts.json` 中声明该 Skill 的样本初筛；它用于找问题，不是最终统计基准。`0/N` 表示当前证据未建立，不表示该 Skill 在所有模型提示下必然无法使用。

| # | Skill | 宽样本命中 | 合同 / 活体观察 | 当前判断 | 具体问题与建议证据档位 | 审计 |
|---:|---|---:|---|---|---|---|
| 1 | `sop-maker` | 0/2 | 0 / 0 | 🔴 当前未建立 | “写一份可复用 SOP”不能路由；必须绑定成功案例、输入证据和适用边界，采用 E2 | [x] |
| 2 | `frontend-expert` | 1/5 | 1 / 0 | 🟡 部分成立 | 前端自然表达召回弱；需记录现有设计系统、运行截图、视口和交互验证，采用 E2 | [x] |
| 3 | `product-sense` | 0/3 | 1 / 0 | 🟡 部分成立 | 根上游能力无法由宽 prompt 选中；主观 ROI 公式会制造伪精确，应改成证据/假设/最小实验，采用 E1 | [x] |
| 4 | `research-and-sourcing` | 0/2 | 1 / 0 | 🟡 部分成立 | 来源合同强但自然召回弱；需要当前一手来源、版本、访问时间和冲突记录，采用 E3 | [x] |
| 5 | `requirement-analysis` | 0/3 | 3 / 1 | 🟡 部分成立 | 窄合同和活体成立，宽表达未进入确定性路由；冻结决定与来源需保留，采用 E2 | [x] |
| 6 | `system-design` | 2/4 | 3 / 1 | 🟡 部分成立 | 高影响设计可激活，但相邻产品/需求链仍漏；ADR、基线、权衡和批准版本采用 E2 | [x] |
| 7 | `coding-discipline` | 3/4 | 5 / 1 | 🟡 部分成立 | 底座较强，仍有复用型 prompt 漏 `frontend-expert`；实现基线、diff、命令与结果采用 E2 | [x] |
| 8 | `debugging-mindset` | 0/3 | 0 / 0 | 🔴 当前未建立 | 内容证据纪律最强之一，但发现链没有证明；症状、假设、验证、日志和失败证据采用 E3 | [x] |
| 9 | `documentation` | 4/5 | 1 / 0 | 🟡 部分成立 | 大多数宽样本可选中；应将每个事实绑定代码/运行来源并区分推断，采用 E2 | [x] |
| 10 | `human-voice` | 5/5 | 0 / 0 | 🟡 部分成立 | 确定性召回好但缺行为和活体证据；必须保留事实、来源、作者身份和不确定性，采用 E2 | [x] |
| 11 | `skill-crafting` | 0/2 | 0 / 0 | 🔴 当前未建立 | 关键封装能力只有结构样本；应保留基线、来源、with/without 结果和安装收据，采用 E3 | [x] |
| 12 | `memory-bank` | 0/1 | 0 / 0 | 🔴 当前未建立 | 存储实现有测试，但用户表达被错误候选干扰；来源、作用域、置信度、替代链和复查时间采用 E3 | [x] |
| 13 | `ecosystem-scout` | 2/3 | 1 / 0 | 🟡 部分成立 | “20 字描述”与可发现性目标冲突； intake 必须记录官方 URL、commit、许可证、扫描与决策，采用 E3 | [x] |
| 14 | `ai-website-cloner` | 0/1 | 0 / 0 | 🔴 当前未建立 | 授权和资产边界较好，但自然路由与活体证据为空；页面来源、许可、截图、替换资产采用 E3 | [x] |
| 15 | `software-advisor` | 0/2 | 0 / 0 | 🔴 当前未建立 | fallback 允许“全网经验推荐”却未强制调研和引用；本地目录也无新鲜度合同，采用 E3 | [x] |
| 16 | `taste-aesthetics` | 3/3 | 1 / 1 | ✅ 已建立 | 当前唯一同时具备宽样本、合同和观察路由的子 Skill；下一步补视觉产物与前后对比，采用 E2 | [x] |
| 17 | `code-minimalism` | 0/1 | 0 / 0 | 🔴 当前未建立 | 规则存在但没有激活证据；应保留删改前基线、复杂度/依赖变化和回归门，采用 E2 | [x] |
| 18 | `book-distiller` | 0/1 | 0 / 0 | 🔴 当前未建立 | 缺章节/页码定位、版本和引文合规；“两处支持”也需可追溯来源，采用 E3 | [x] |
| 19 | `video-extractor` | 1/1 | 0 / 0 | 🟡 部分成立 | metadata 谱系设计较好，但无真实资产回放；URL、授权、字段来源、时间和失败资产采用 E3 | [x] |
| 20 | `video-creation-sop` | 3/3 | 0 / 0 | 🟡 部分成立 | 宽样本召回好；素材授权、模型/provider、提示词、生成参数和导出证据采用 E3 | [x] |
| 21 | `context-compressor` | 2/3 | 1 / 0 | 🟡 部分成立 | 有预算合同，缺活体前后成本对比；基线 token、工具输出、压缩动作和损失采用 E2 | [x] |
| 22 | `security-gate` | 0/3 | 1 / 0 | 🟡 部分成立 | 能扫描但 Skill 自身没有标准证据收据；目标来源、版本/hash、规则版本、命中和边界采用 E4 | [x] |
| 23 | `reality-auditor` | 1/4 | 5 / 1 | 🟡 部分成立 | 窄合同最强但宽召回不稳；实现链、命令、活体产物、新鲜度和独立审查采用 E4 | [x] |
| 24 | `nexusflow-governance-workflow` | 1/1 | 1 / 0 | 🟡 部分成立 | 上下文门有效，缺项目活体观察；权限快照、后端事实源、租户和审计日志采用 E4 | [x] |
| 25 | `static-demo-hardening` | 2/2 | 1 / 0 | 🟡 部分成立 | 宽样本通过，但自定义触发 `Demo/index.html` 被自身上下文门拒绝；截图、导出、视口和来源采用 E3 | [x] |
| 26 | `ai-cost-grounding-measurement` | 1/1 | 0 / 0 | 🟡 部分成立 | 证据合同强但无行为/活体绑定；原始响应、token、query、价格版本、汇率和账单边界采用 E4 | [x] |

### 5.1 优先级汇总

- **发现链 P0**：`sop-maker`、`debugging-mindset`、`skill-crafting`、`memory-bank`、`ai-website-cloner`、`software-advisor`、`code-minimalism`、`book-distiller`。
- **路由协作 P0**：`product-sense -> requirement-analysis -> system-design`、`taste-aesthetics -> frontend-expert`、`reality-auditor -> debugging-mindset`、`skill-crafting -> sop-maker/documentation`。
- **证据 P0**：`security-gate`、`software-advisor`、`ecosystem-scout`、`memory-bank`、`book-distiller`、`video-extractor`、`ai-cost-grounding-measurement`。
- **项目上下文 P1**：`nexusflow-governance-workflow`、`static-demo-hardening`；保留严格上下文门，不用扩大泛词召回换取表面命中率。

## 6. 12 个外部增强依赖清单

| 外部能力 | 触发意图 | 古月自身可路由 | 当前处理 |
|---|---:|---|---|
| `luban` | 0 | 🔴 | [ ] 补公共意图、负向边界和安装状态；不得仅靠当前会话显式点名 |
| `huashu-nuwa` | 0 | 🔴 | [ ] 补人物/人格 Skill 生成意图和与 `skill-crafting` 的边界 |
| `superpowers` | 0 | 🔴 | [ ] 不作为一个泛能力直接路由；拆成可验证的具体外部能力索引 |
| `ui-ux-pro-max` | 0 | 🔴 | [ ] 与 `taste-aesthetics/frontend-expert` 建立受控参考链 |
| `gsap-core` | 0 | 🔴 | [ ] 仅在前端动效上下文和已安装条件下成为候选 |
| `find-skills` | 4 | 🔴 | [ ] trigger 存在但路由器不读取外部依赖；接入外部候选解析器 |
| `taste-skill` | 5 | 🔴 | [ ] 与内置审美能力做去重/互补裁决后再激活 |
| `headroom` | 4 | 🔴 | [ ] 由 `context-compressor` 提出候选，不直接自动安装 |
| `ponytail` | 4 | 🔴 | [ ] 与 `code-minimalism` 去重，默认内置能力优先 |
| `cangjie-skill` | 4 | 🔴 | [ ] 与 `book-distiller` 去重并保留来源版本 |
| `video-downloader` | 3 | 🔴 | [ ] 由 `video-extractor` 在 source-media 模式下受控候选 |
| `skillspector` | 4 | 🔴 | [ ] 由 `security-gate` 作为增强扫描器候选，未安装时明确降级 |

外部能力不应直接混入内置 `selected`。建议增加独立状态：`external_candidate`。只有同时满足“意图命中、已安装或有明确安装计划、来源已固定、安检通过、动作已授权”后，才进入 `activated`。普通库和 Agent Skill 也必须分开，前者不能假装成可加载 `SKILL.md` 的能力。

## 7. 统一能力合同设计

### 7.1 权威顺序

1. 子目录 `SKILL.md` frontmatter 是跨运行时原生发现的权威 name/description。
2. `skills_manifest.json` 只保存古月扩展字段：正向意图、近邻负例、上下文门、优先级、证据档位和曝光策略。
3. 根 `SKILL.md` 只保存仲裁原则和高价值路线，不复制全部触发词。
4. 测试样本从同一能力 ID 关联，不再从自由文本 `expected_behavior` 猜路由。
5. observations 只记录真实运行，不反向修改历史证据；每条绑定文件、hash、runtime、版本和时间。

### 7.2 建议字段

```json
{
  "name": "debugging-mindset",
  "path": "skills/debugging-mindset/SKILL.md",
  "trigger_intent": ["..."],
  "negative_intent": ["..."],
  "required_any_context": [],
  "root_exposure": "explicit",
  "evidence_profile": "E3-diagnostic",
  "activation_policy": "model-or-explicit",
  "adjacent_skills": ["reality-auditor"],
  "live_canary_required": true
}
```

`root_exposure` 只允许：

- `explicit`：根路由表直接展示的常用能力。
- `contextual`：项目名或稳定标记出现后才展示的能力。
- `manual-only`：只允许用户显式调用，不能自动激活。
- `external-candidate`：外部候选，必须走安装、来源和安检状态机。

### 7.3 证据档位

| 档位 | 适用能力 | 最小字段 |
|---|---|---|
| E1 决策 | 产品判断、需求澄清 | 已确认事实、假设、决定、未知、可推翻条件 |
| E2 变更 | 设计、编码、前端、文档、语言、极简化、上下文压缩 | 输入基线、变更动作、产物、验证、未验证边界 |
| E3 谱系 | 调研、推荐、SOP、Skill 制作、生态 intake、内容/视频、记忆 | 来源标识、版本/commit、获取时间、派生关系、授权、产物 hash、新鲜度 |
| E4 审计 | 安全、真实性、权限治理、AI 成本、发布 | E3 全部字段 + 命令/退出码、规则版本、独立复核、失败证据、不变性要求 |

证据规则遵循“按声明风险触发”，不是每次闲聊都输出表格。只有答案包含外部事实、推荐、重要决定、文件变更、安全结论、完成声明或可复用资产时才生成持久 receipt。

### 7.4 最小证据封套

```yaml
claim_status: confirmed | inferred | conflicting | unknown | decided
source_ref: repo-relative path | official URL | command | runtime artifact
source_version: commit | release | observed state
observed_at: ISO-8601
activity: read | transform | execute | verify | review
artifact_ref: repo-relative path or none
artifact_sha256: hash or not-applicable
verification: command / human check / independent replay
result: pass | fail | blocked | partial
boundary: what this evidence does not prove
```

这不是照搬 W3C RDF，而是借用其 `Entity -> Activity -> Agent` 思路：来源实体经过什么活动，由谁或什么运行时产生哪个结果。对于普通回答可压缩成一句来源说明；对于高风险产物才写完整封套。

## 8. 路由与评测重构方案

### 8.1 拆分四类测试

1. **静态发现测试**：frontmatter 合规、description 同时包含用途和使用时机、安装后可枚举。
2. **确定性路由测试**：每个 Skill 至少 8 个 should-trigger、8 个相邻 should-not-trigger；固定 60/40 train/holdout。
3. **真实激活测试**：每个 Skill 选 2 个正例和 2 个近邻负例，在新会话运行 3 次，记录 Skill body 是否真的加载。
4. **输出质量测试**：高价值能力采用 with-skill vs without/previous-version 基线，断言必须引用真实产物。

### 8.2 修复 `test-prompts.json`

自由文本继续作为人类期望说明，但新增机器字段：

```json
{
  "id": "debugging-production-500",
  "prompt": "线上接口 500，先帮我查根因",
  "expected_routes": ["debugging-mindset"],
  "forbidden_routes": ["coding-discipline"],
  "required_context": [],
  "required_actions": ["separate symptom hypothesis and validation"],
  "forbidden_actions": ["patch before evidence"],
  "split": "train"
}
```

`run_eval.py` 必须真实运行全部机器字段，不能再只检查技能名是否出现在文本里。条件性路由要显式编码，不能把“仅在某条件下使用 research”误解析成始终 expected。

### 8.3 防止为测试过拟合

- 不直接把失败 prompt 原句塞进 trigger。
- 先归纳用户意图类别，再修改 description 或 intent family。
- train 用于修改，holdout 只用于选版本。
- 相邻技能必须成对测试，例如产品/需求/设计、审美/前端、排障/真实性审查。
- 描述优化不能突破 1024 字符，也不能让全局 discovery budget 失控。

## 9. 具体执行计划

### M0：冻结基线与清理标签（P0）

- [x] 保存当前 26 Skill frontmatter、manifest、54 prompts、19 contracts 和 observations 的基线快照/hash。
- [x] 为 54 条 prompt 增加稳定 ID 和机器字段，人工修正条件性路由标签。
- [x] 固化本轮初筛脚本，生成 `evals/capability-chain-baseline.json`，不靠临时 shell 统计。
- [x] 在 CI 中禁止“prompt 只提到技能名就算覆盖”。

验收：现有 54 条样本全部能被机器解释为明确 expected/forbidden/conditional；旧绿灯不再掩盖 30 条漏路由。

### M1：修复内置发现与仲裁（P0）

- [x] 先修 静态 Demo 演示面 `Demo/index.html` trigger/context 自相矛盾。
- [x] 为 26 个 Skill 建立 8 正 + 8 近邻负例，共 416 条确定性路由样本；先核心 12 个，再扩到全部。
- [x] 优先修复 8 个当前未被证据建立的发现链能力。
- [x] 修复四条相邻能力链，不追求所有相关 Skill 同时触发，只要求阶段顺序正确。
- [x] 对 frontmatter description 做 train/holdout 优化；manifest triggers 作为扩展，不替代公共 description。
- [x] 增加 CI：frontmatter 与 manifest 名称/定位冲突、root exposure 未声明、context gate 吞掉自身 trigger 时失败。

验收：416 条确定性样本 train 与 holdout 均达到预定阈值；每个 Skill 至少有一个正例和一个负例进入 CI；无上下文项目 Skill 不误触发。

### M2：建立外部候选状态机（P0）

- [x] `resolve_routes()` 增加独立 `external_candidates` 输出，不把外部候选冒充内置 selected。
- [x] 为当时登记的外部依赖补 `type`、意图、负例、来源 URL、固定 ref、风险级别和替代关系；安装与来源健康继续由环境探针和动作收据判定。
- [x] 移除 `ecosystem-scout` 的“20 字以内 description”硬规则，改为受 discovery budget 约束的有效描述。
- [x] 连接 `discover_local_skills.py` 的位置索引与路由候选，但不将私人绝对路径写入公开收据。
- [x] 声明必须顺序通过的门：candidate -> source_checked -> installed -> security_checked -> authorized -> activated / blocked；明确它不是持久状态机，列表本身不证明任何迁移已发生。
- [x] 为内置能力优先、外部互补和外部替代分别增加回放。

验收：未安装、未安检、未授权的外部能力只能显示候选和边界；任何情况下都不能直接执行命令。

### M3：证据规则分层融合（P1）

- [x] 在根原则定义最小证据封套和按风险触发规则。
- [x] manifest 为 26 个 Skill 增加 `evidence_profile`，CI 验证枚举值。
- [x] E1/E2 Skill 只补差异化字段，不复制整套模板。
- [x] E3/E4 Skill 增加产物路径、source/version/time、hash、失败和新鲜度要求。
- [x] 集中修复 `software-advisor` fallback：本地未命中时必须转 `research-and-sourcing`，禁止无来源“经验推荐”。
- [x] 为 `security-gate` 生成机器收据，绑定目标指纹、扫描规则版本、命中和能力边界。
- [x] 为 `book-distiller` 增加章节/页码/版本定位和引文边界；为视频能力统一素材 lineage。
- [x] 为 `product-sense` 移除伪精确公式，改为证据、假设、成本区间和最小实验。

验收：高风险完成声明没有 source/version/time/verification/boundary 时 CI 或 checker 失败；低风险回答不被迫输出冗长表格。

### M4：真实激活与输出质量（P1，按实测成本修订）

- [x] 先用 345 条 should-trigger、208 条近邻 should-not-trigger 和 54 条宽合同完成确定性全覆盖。
- [x] 26 个 Skill 各运行一次独立 Codex 新会话；只有事件流实际读取目标 Skill body 且最终路线正确才算通过。
- [x] 记录 `runtime`、版本、prompt ID、目标文件读取、最终路线、退出码、token、证据文件与原始事件 hash。
- [x] 对 E1-E4 四个证据档位做失败优先输出回放；两轮 FAIL 触发规则修复，第三轮独立审查全部 PASS。
- [x] 对全部 26 个 Skill 各运行一个现实型合成任务和独立审查；保留 18/26、24/26、26/26 三轮失败优先历史及每项三层工件。
- [x] 保留运行时 2% Skills discovery budget 警告，以及“单次激活不等于统计稳定性或全领域输出质量”的边界。

原定 312 次模型调用和 12 项 with/without 盲评没有机械执行。首轮真实探针显示单项约 6.5 万至 11.5 万输入 token，扩大到 312 次主要重复全局 catalog 成本，并不能替代真实领域输入。最终门采用“553 条确定性正负例 + 26 条真实激活 + 26 条逐 Skill 输出及独立审查 + 四档 failure-first 输出”，把其他 runtime、重复触发率和真实用户结果留在明确边界中。

验收：26 个 Skill 均有可反算 Codex 激活工件和一个独立审查输出；不再只看路由名字，同时不把单个合成任务扩大成任意输入质量。

### M5：安装、跨运行时与独立审查（P1）

- [x] 从临时 Git 索引构造精确候选，在空 HOME 中完成安装、重启、26 内置 Skill、12 外部候选和证据 profile 复查；发布前按最终工件重新取数。
- [x] Codex 26/26 全量 canary 完成；Claude 只完成 marketplace manifest 严格校验，其他 runtime 和 Claude 模型激活均不声明已验证。
- [x] 精确候选完整套件 15/15 通过；Ruff、安全、出生证明和安装旅程包含在套件中，diff 与缓存检查在最终收口单独执行。
- [x] 独立审查者先检查失败历史、receipts、当前源码和哈希绑定，再输出判定；审查发现的可修复问题进入下一轮门禁。
- [x] 新用户六问扩展为八问；初审真实返回 `FAIL`，修复输出工件不可反查和 17/19 计数不一致，保留不可由本地伪造的现实边界。

验收：候选包 D1-D6 全链通过；跨运行时只声明实际验证的范围；报告中保留失败、未覆盖和现实边界。

### M6：发布与回炉（需单独授权）

- [x] 更新 README、showcase、evaluation、release checklist、changelog、总控账本和候选出生证明口径。
- [x] 用户已明确授权本轮提交、推送、打 tag 和发布；只有最终门禁全绿后执行。
- [ ] 发布后记录公网安装、真实触发失败、误触发和用户结果，作为下一轮 holdout。

验收：公开声明不复用旧版本证据；本地 100% 不能替代真实用户价值。

## 10. 逐 Skill 执行追踪表

以下状态均由本轮机器合同和活体证据逐层取得；勾选不包含其他 runtime、全领域输出质量或真实用户价值：

| Skill | 标签规范化 | 路由修复 | 证据 profile | Codex 活体激活 | 确定性终验 |
|---|---|---|---|---|---|
| sop-maker | [x] | [x] | [x] | [x] | [x] |
| frontend-expert | [x] | [x] | [x] | [x] | [x] |
| product-sense | [x] | [x] | [x] | [x] | [x] |
| research-and-sourcing | [x] | [x] | [x] | [x] | [x] |
| requirement-analysis | [x] | [x] | [x] | [x] | [x] |
| system-design | [x] | [x] | [x] | [x] | [x] |
| coding-discipline | [x] | [x] | [x] | [x] | [x] |
| debugging-mindset | [x] | [x] | [x] | [x] | [x] |
| documentation | [x] | [x] | [x] | [x] | [x] |
| human-voice | [x] | [x] | [x] | [x] | [x] |
| skill-crafting | [x] | [x] | [x] | [x] | [x] |
| memory-bank | [x] | [x] | [x] | [x] | [x] |
| ecosystem-scout | [x] | [x] | [x] | [x] | [x] |
| ai-website-cloner | [x] | [x] | [x] | [x] | [x] |
| software-advisor | [x] | [x] | [x] | [x] | [x] |
| taste-aesthetics | [x] | [x] | [x] | [x] | [x] |
| code-minimalism | [x] | [x] | [x] | [x] | [x] |
| book-distiller | [x] | [x] | [x] | [x] | [x] |
| video-extractor | [x] | [x] | [x] | [x] | [x] |
| video-creation-sop | [x] | [x] | [x] | [x] | [x] |
| context-compressor | [x] | [x] | [x] | [x] | [x] |
| security-gate | [x] | [x] | [x] | [x] | [x] |
| reality-auditor | [x] | [x] | [x] | [x] | [x] |
| nexusflow-governance-workflow | [x] | [x] | [x] | [x] | [x] |
| static-demo-hardening | [x] | [x] | [x] | [x] | [x] |
| ai-cost-grounding-measurement | [x] | [x] | [x] | [x] | [x] |

## 11. 停止条件与反膨胀约束

- 不为追求召回率让多个相邻 Skill 同时触发；要验证正确阶段和最窄路线。
- 不把 26 份相同证据模板塞入 26 个正文；根定义协议，manifest 声明 profile，子 Skill 只写差异。
- 不把 deterministic route 等同模型激活，也不把模型激活等同输出质量。
- 不为了外部生态数量扩大 catalog；没有稳定意图、来源、安装和安检状态的条目移入观察清单。
- 不给所有建议强制联网；只有外部事实、推荐、新鲜度和高风险声明需要来源。
- 不把“引用了来源”当作来源可靠；必须记录来源类型、版本、时间、冲突与适用边界。
- 不追求本地 100 分。公开安装、不同 runtime 和真实用户结果只能由现实发生。

## 12. 参考来源

- [Agent Skills Overview](https://agentskills.io/home)：发现、激活、执行的三级 progressive disclosure。
- [Agent Skills Specification](https://agentskills.io/specification)：description 必须说明做什么和何时使用，并包含帮助识别任务的具体关键词。
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)：正/负触发样本、近邻负例、多次运行、train/validation 拆分和避免过拟合。
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)：with-skill/without-skill 基线、可验证断言、产物证据、时间与 Token 成本。
- [Claude Code Skills](https://code.claude.com/docs/en/skills)：Skill body 按需加载、自动发现、显式调用、评测与“不触发/过度触发”排查。
- [W3C PROV Constraints](https://www.w3.org/TR/prov-constraints/)：来源记录用于评估质量、可靠性和可信度；有效谱系需要一致的实体、活动和责任关系。

## 13. 最终方向判断

古月下一阶段不应继续以“人格更强、能力更多”为主目标，而应转为：

> **让每项已有能力都能被正确发现、在正确上下文激活、产生可追溯结果，并能用真实失败推翻自己的完成声明。**

这条路线比继续增加 Skill 更慢，但会把古月从“拥有一组好文档”推进成“能力声明、运行行为和证据结果一致的个人 Agent 操作层”。
