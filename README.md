# guyue (古月)

> 一句话钩子：让 Agent 在复杂任务里先定边界、再执行、用证据收尾。

古月是从真实 AI 协作记录中蒸馏出来的 Personal Agent Operating Layer。它把需求判断、工程纪律、长任务恢复、记忆、安全和验收组织成一套可安装、可解释、可复跑的工作方式，并用机器可检的协作合同约束相邻能力何时串联、何时独立复验、何时必须停在授权边界前。

![Skill Badge](https://img.shields.io/badge/Agent_Skill-guyue-blue)
![Architecture](https://img.shields.io/badge/Architecture-Digital_Twin_Core_%2B_Specialties-success)
![Status](https://img.shields.io/badge/Release-v1.7.0-brightgreen)

> [!WARNING]
> `v1.7.0` 是判断治理与精简验真版本：高影响想法必须先证明问题和方向，跨轮方案实质改形会清空继承置信度；认知拓界的高风险输出合同已缩为可机械审计的最小证据脊柱。正式载荷通过完整本地套件、严格能力链、零泄漏扫描，以及 Codex CLI 上 `27/27` 真实激活和 `27/27` 全能力合成输出质量验证。

> [!IMPORTANT]
> 古月不是“完整的人”或万能自动化系统。它会主动完成边界明确、仓库内可逆的工作；公开发布、付费、凭证、权限扩大、不可逆迁移等高影响动作仍需绑定具体版本的授权。它不会把 AI 参与伪装成人工来源，也不会为了好听删除证据缺口或风险。

![Guyue read-only first-run flow](assets/demo.gif)

## 快速开始：30 秒验货

先验货，不安装依赖、不联网、不调用模型：

```bash
git clone https://github.com/guyue55/guyue-skill.git
cd guyue-skill
python3 scripts/try_guyue.py
```

下面是当前 `v1.7.0` 的本地验货样例：

```text
[PASS] 包体 complete | v1.7.0 | 27 Skills
1. static-demo-hardening | 证据: 静态 demo
2. coding-discipline | 证据: PDF 导出
项目边界: 静态 Demo 演示面、NexusFlow 专属能力未误触
上下文: 0 个高相似路由碰撞
[PASS] 本地验货通过
```

这个入口复用真实的包体收据、路由解释器和上下文预算器，只读、不写文件。它证明当前载荷、确定性路由和上下文预算，不证明目标运行时已经激活或模型行为回放通过。入口源码见 [scripts/try_guyue.py](scripts/try_guyue.py)，完整场景见 [examples/showcase.md](examples/showcase.md)，活体回放见 [examples/quickstart-output.md](examples/quickstart-output.md)。

### 证明口径

| 证据 | 能证明 | 不能证明 |
|---|---|---|
| `scripts/try_guyue.py` | 当前载荷、确定性路由、项目边界和上下文预算 | 目标运行时已激活，或模型一定遵守合同 |
| 哈希绑定的只读回放 | 指定提示词在指定运行时中的真实行为 | 其余行为合同、其他运行时或长期结果 |
| `v1.7.0` 的本地发布套件 | 当前 27 个 Skill 的结构、路由、协作、安装载荷、安全和上下文预算 | 其他运行时、任意输入质量、真实用户价值或长期效果 |
| 当前发布套件与发布清单 | 精确载荷的本地结构、安全、远程 CI 和公开源安装完整性 | 其他运行时、GitHub Release 或长期用户价值 |

> [!NOTE]
> 当前发布已定义 27 个子 Skill、114 个路由用例、42 个行为合同、12 个协作用例、222 个近邻负例和 11 个工作流。严格发布收据另在 Codex CLI `0.146.0-alpha.3.1`、请求模型 `gpt-5.6-terra` 上通过 `27/27` 真实激活和 `27/27` 全能力合成输出质量验证；这仍不代表任意输入、其他运行时、真实用户价值或长期效果。

普通开发门会把“活体收据陈旧/不完整”保留为可见警告，并维持相应能力声明为 `false`，避免额度阻断诱发无价值的全量重跑；正式发布仍必须用 `check_capability_chain.py --strict --json` 或 `GUYUE_RELEASE_STRICT=1` 将这些警告恢复为阻断门。

## 适合谁

- 长期让 Agent 参与复杂工程、需要跨会话恢复和验收的人。
- 维护多个 Skill、多个项目或多个 Agent 运行时，需要稳定路由和上下文边界的人。
- 不能接受“测试全绿就算完成”，需要发布前证据、安全边界和可追溯决定的人。

## 它解决什么

- **模糊需求直接进入实现**：先用项目事实关闭目标、范围、成本和验收边界，再决定是否编码。
- **稳定本地事实与外部时效信息混用**：本地状态直接检查；当前 API、法规或高风险事实才查一手来源。
- **测试全绿却不是当前产物**：把源码版本、工作树、活体文件、哈希、命令和退出码绑定到结论。
- **长任务靠聊天残影恢复**：模糊愿景先进入长线目标铸造，用总控、执行账本、阶段计划、委派包和证据索引关闭决策；准备就绪后只交付一行 Goal 提示词，不把阶段完成扩大成愿景完成。

古月的底盘是三件事：**验料**，先判断什么值得做；**造镜子**，把经验沉淀成可复用判断；**活体对账**，能运行就运行，能打开就打开，不让绿色状态灯替代真实结果。

## 认知拓界：先找到该看什么

“多维度分析”或“全面分析”只表达了想看得更广，却没有说明分析服务什么决定、边界在哪里、维度从何而来、哪些事实需要更新、何时可以停止。直接回答通常只会得到熟悉框架和更长的列表。

`cognitive-expansion` 有两种使用形态。日常默认是**微量拓界**：在原任务内从模型已有认知补 2–5 个真正相关的视角、一个反向或遗漏视角和必要的时效提醒，通常不超过约 300 tokens；它不另起报告、不打 Trace、不建正式账本，也不默认联网。只有陌生领域、系统学习、争议或高风险任务才升级为正式认知地图：标出领域术语、对象、关系、参与者、竞争定义、标准、证据状态、冲突和未知，再按当前目的保留真正有信息价值的维度。

“例如、按钮/加载态等、等等、之类、包括但不限于”默认只是**种子集合**。Agent 会先识别上位类别，再补 1–3 个足以改变答案的相邻遗漏，并区分哪些来自用户、哪些是模型候选；连同必要的种子、反向面或时效提醒，最终通常呈现 2–5 个视角。只有“仅、只、严格限于、就这几项、不要扩展”才关闭扩展。这条规则适用于其他主 Skill，不会因为一个“等”把普通开发任务升级成长调研。

联网遵循升级门：低风险且不依赖当前事实时先展开模型内知识；用户要求来源/最新资料，或信息具有时效、争议、高风险、版本依赖时，才定向转 `research-and-sourcing`。除非用户指定历史快照、旧版本或明确不在意时效，联网结果会区分发布日、事实发生期或数据期、版本/更正/撤回和访问日；搜索摘要只用于发现候选，重要结论优先原始材料并寻找独立约束。预计超过 10 分钟、打开超过 2 份材料、使用子任务或升级深度时，会先给出模式、预计耗时区间、材料/调用上限、停止检查点和主要不确定性；已有持续授权也不会取消预警与跨重试总预算。

门禁按后果分级：造假、越权、安全/权利边界和会改变结论的语义错配是硬门；轻微格式、顺序或估算偏差只提示，不为“刷绿”反复调用模型。额度或运行时暂不可用时立即保留当前结果并转做本地检查，不等待、不自动重试；严格高风险验收未通过也可以交付明确标边界的认知地图，但不能冒充决策就绪。

### 30 秒看到微量拓界

给 `gpt-5.6-terra` 同一句“第一次使用团队知识库搜索页，已经想到关键词、筛选器等，还有什么容易遗漏”，候选版没有联网、没有 Trace、没有正式账本，只补了三件会改变体验的事：

> - **搜索范围与权限**：结果为空时，先区分没资料、空间没覆盖和无权限；
> - **排序与版本**：确认“最新、最权威、最相关”到底按什么规则；
> - **无结果后的接力**：提供同义词、相关知识库入口或联系人，而不是让用户反复换关键词。

同模型、同提示、各运行一次后，主 Skill 从 208 行降到 83 行，Codex CLI 报告的 gross tokens 从 37,821 降到 14,268（-62.3%）。这些数字包含运行时入口与 Skill 读取，不是最终回答的 Token 数；完整提示、原始输出、哈希和证据边界见[微量回放记录](evals/evidence/cognitive-expansion-luban-micro-2026-07-17.md)，生态对标、九维评分和回炉入口见[鲁班打磨报告](docs/luban-report-cognitive-expansion-2026-07-17.md)。

可以这样触发：

- “按钮、加载态等还有没有遗漏？轻量补一下，不联网。”
- “我对量子传感完全陌生，先帮我画出这个领域的问题空间和专业判断标准。”
- “不要直接套 SWOT，帮我找出新能源汽车出海最容易漏掉的维度、反例和未知。”
- “先全面理解这个公共政策争议，给出可修订的认知地图，再告诉我最值得补证的问题。”

边界也很明确：模型记忆只用于生成候选线索，不能冒充外部事实；涉及当前变化时转 `research-and-sourcing` 查一手来源；医疗、法律、金融等高风险结论需要具名专业人士或正式机构复核；安装、发布、付费、外部写入、权限扩大和不可逆动作仍需针对具体动作授权。

## 为什么不只是临时问 Agent

| 形态 | 擅长 | 缺少什么 |
|---|---|---|
| 临时提示 | 一次性回答和局部执行 | 没有版本化路由、恢复账本、证据合同和回归门 |
| 单一任务 Skill | 固化一个领域的稳定步骤 | 通常不负责跨任务仲裁、长线控制修订和终局封账 |
| Guyue（当前发布清单） | 用 27 个窄能力组织认知建图、需求、实现、恢复、审查和沉淀 | 仍依赖目标运行时执行；本地发布套件不替代用户价值判断或时间型结果 |

## 安装到 Agent

### v1.7.0：GitHub 源与 Claude Code Marketplace 元数据

```bash
claude plugin marketplace add guyue55/guyue-skill
claude plugin install guyue@guyue
```

安装后可用 `claude plugin details guyue@guyue` 核对版本和组件清单。公开 tag `v1.7.0` 固定本次判断治理与精简验真载荷，Marketplace 元数据与版本一致。Claude 模型激活和 Marketplace 提交仍是独立证据面，不能由 Codex 活体回放、结构校验、GitHub Release 或本地安装证据替代。

**Codex 完整安装：**

```bash
git clone https://github.com/guyue55/guyue-skill.git ~/.codex/skills/guyue
python3 ~/.codex/skills/guyue/scripts/check_full_install.py ~/.codex/skills/guyue --runtime codex --json
```

**其他兼容运行时的完整仓库挂载：**

```bash
git clone https://github.com/guyue55/guyue-skill.git /path/to/guyue
cd /path/to/guyue
python3 scripts/install_guyue.py
bash scripts/test_suite.sh
```

把 `/path/to/guyue` 链接或复制到运行时的技能目录，并重新开始会话。`scripts/install_guyue.py` 会安装 Python 运行依赖、只读规划可选增强技能，再运行 Doctor；默认不会下载或链接第三方技能。

> [!WARNING]
> 不要把 `npx skills add guyue55/guyue-skill` 当成完整安装。当前通用 Skills CLI 对仓库根技能只复制 `SKILL.md`，不会带上本项目运行所需的 `GUYUE_PRINCIPLES.md`、`skills_manifest.json`、`skills/`、`scripts/` 和 `docs/`。完整古月必须以整个仓库作为一个技能目录挂载。

安装后直接用自然语言触发：

```text
使用古月的思路帮我分析这个需求，先别写代码。
线上报错了，启动古月的排障心法。
把这次成功排障沉淀成 SOP，并记住关键教训。
```

更完整的运行时安装路径见 [docs/installation.md](docs/installation.md)。安全边界见 [docs/security.md](docs/security.md)。评测方式见 [docs/evaluation.md](docs/evaluation.md)。

运行时边界见 [docs/runtime-adapters.md](docs/runtime-adapters.md)，长任务协议见 [docs/long-goal-protocol.md](docs/long-goal-protocol.md)，控制包字段见 [docs/templates/long-goal-control-pack.md](docs/templates/long-goal-control-pack.md)。当前证据见 [v1.7.0 发布说明](docs/release-v1.7.0.md) 和 [发布清单](docs/release-checklist.md#v170-release-evidence)。

## 核心心智矩阵：1 个核心分身 + 14 个基础能力 + 13 个扩展能力

本系统采用类似操作系统的技能路由架构（Digital Twin Orchestrator）。当运行时加载根 `SKILL.md` 后，主干根据意图选择最窄的内部能力模块：

> [!NOTE]
> 这里描述当前发布分支的 27 个子 Skill 和确定性合同。活体激活和输出质量收据必须按当前版本单独刷新，不能从旧版本继承。

- 🚦 **核心分身 (guyue)**：接管意图，强制注入模块化解耦、全局规划、规范化纪律的底层思维 SOP。
- 🗺️ **认知拓界 (cognitive-expansion)**：日常以微量模式补少数高价值遗漏，陌生或高风险领域才建立可被新证据修订的正式认知地图；把“等/等等/之类”视为种子而非闭集，模型知识优先，时效或证据门命中后才定向联网，不替代事实检索、需求拆解或架构设计。
- 🔍 **证据型调研 (research-and-sourcing)**：外部事实不稳定、陌生、高风险、用户明确要求或会改变决定时，查当前一手来源；稳定的本地事实直接检查仓库与运行产物，不为仪式感联网。
- 🤔 **需求反问 (requirement-analysis)**：拒绝单向接受模糊需求，优先从项目证据补齐事实，再只追问会改变目标、范围、成本或验收的事项。
- 🎯 **价值拷问 (product-sense)**：在进入系统设计前，强制剥离技术滤镜，审视需求的 ROI 和商业逻辑。
- 🏛️ **系统设计 (system-design)**：统一模型、表格、全局参数、接口契约和权限规则；仓库内可逆小改主动推进，技术栈替换、不可逆迁移、权限模型和公开发布等高影响动作使用绑定版本的审批。
- 💻 **全栈开发纪律 (coding-discipline)**：前端、后端、数据、脚本、配置、基础设施和文档进入实现阶段时，先查已有函数、模型、表格、常量、全局参数、接口契约、组件、弹窗、提示和脚本，二次使用即抽象，再执行高内聚低耦合、必要注释、权限分层、验证闭环和中文提交规范。
- 🕵️ **受控排障 (debugging-mindset)**：用症状、假设、最小验证动作和 RCA 矩阵定位根因；失败测试、错误栈、日志、指标或活体产物都可作为证据，证据不足时拒绝猜测性补丁。
- 📝 **结构化沉淀 (documentation)**：按读者、任务、格式和细节组织 README、架构决策记录与代码背书的项目地图；区分材料事实、推断和决定，不把分隔标签误当安全边界。
- 🗣️ **说人话门禁 (human-voice)**：把回答、报告、技术解释和发布说明改成读者能听懂、能判断、能行动的表达；默认正常沟通用简体中文，避免不必要中英文混排；保留事实、证据、来源、授权和风险边界，不做 AI 检测规避，不伪装人工来源。
- ✨ **前端与交互美学 (frontend-expert)**：先服从产品类型、现有设计系统和技术栈，再落实 a11y、响应式与 UI 标准件复用；只有复杂时序或现有项目确有需要时才引入 GSAP 等增强能力。
- 🏭 **标准件车间 (sop-maker)**：当一项复杂排障、开发流或重复 Agent 工作成功闭环后，将其提炼、泛化并打包为可复用的操作手册 (SOP) 或 Loop Contract。
- 📒 **长线目标铸造与长程自治**：Long Goal v4 在 v3 的稳定 ID、委派收束和哈希证据上，增加三层时间尺度、事实/决定/假设/实验台账、可追溯控制修订、先纵切后扩张和 A/B/C Git 封账。检查器可通过 `--repo-root` 验证任意目标仓库；连续模拟覆盖三次失败、设计复核、批准恢复、封账、重启与篡改拒绝。承诺与 `FINAL/ATTEMPT` 证据双向对账，检查器通过仍只证明控制结构完整。v2/v3 仅保留历史解析兼容。
- 🧠 **证据型双轨记忆 (memory-bank)**：公共精选索引与本地私有运行记忆分离；每条教训记录来源、证据、作用域、置信度、替代关系和复查日期，避免把过期经验当成当前事实。
- 🛠️ **技能制作 (skill-crafting)**：先验证重复价值、稳定输入、可复用步骤和验证标准，再选择 Skill、Custom subagent、SOP、脚本、Hook、Automation 或 CI gate；用无 Skill 基线、留出样本、重复回放和安装验真取代评分表自嗨。
- 📡 **能力链验真**：当前 manifest 的 27 个子 Skill、114 个路由用例、42 个行为合同、12 个协作用例、222 个近邻负例和 11 个工作流证明确定性发现与选择合同。10 个外部增强只能进入候选态，未完成来源、安装、安检和动作授权前不能冒充已激活能力。
- 🧭 **生态寻猎 (ecosystem-scout)**：调研外部技能/工具，按 Two-Phase Loading 轻量注册；确实适合第三方工具时，先给安装计划和安全边界，获明确授权后再快速接入。

扩展能力用于处理更细分的高风险工作流，默认仍受安全、授权和验证门约束：

- 🛡️ **技能安检 (security-gate)**：收纳或使用第三方技能前，先做本地启发式安全预检，见红旗即拦截。
- 🧱 **网页重建 (ai-website-cloner)**：在授权边界内重建公开或自有页面，学习信息架构、组件关系和设计 token，禁止绕过登录、付费墙、反爬、DRM、钓鱼仿冒和复制第三方品牌资产。
- 🧰 **软件顾问 (software-advisor)**：优先查询本地精选库，未命中时明确标注来源边界。
- 🎛️ **审美约束 (taste-aesthetics)**：审查和约束 AI 味 UI，先区分官网、后台、报告、作品集等页面类型，再输出设计拨盘、确定性检查项、参考设计边界和修正方向。
- ✂️ **极简代码 (code-minimalism)**：用 YAGNI 阶梯和复用扫描削减过度设计、重复代码、重复模型/参数/契约和错误抽象，保留安全、错误处理和可访问性底线。
- 📚 **长文蒸馏 (book-distiller)**：把方法论文档提炼为可复用技能结构，而不是普通摘要。
- 🎬 **视频创作 SOP (video-creation-sop)**：把文章、产品、口播、短剧或创意拆成可审核的视频生产包；短剧走需求、大纲、风格锁定、视觉/音频资产、分镜、关键帧、分镜视频、成片合成导出和全案沉淀阶段门，保留复刻所需的字段来源、待确认项、授权证据、发布状态、时间线、参考图、连续性指标、音频混音、字幕、耗时成本和导出证据，优先使用当前 Agent 原生媒体能力，缺能力时再要求配置 provider。
- 🎞️ **视频提取 (video-extractor)**：在授权和平台规则内提取元数据、字幕和可选媒体。
- 🗜️ **上下文预算 (context-compressor)**：先判断 token 浪费来自文件、工具、文档、长会话还是动态工作流，再用最小上下文、子任务预算和可追溯证据完成任务。
- 🔎 **真实性审查 (reality-auditor)**：实现后独立验收，专查假数据、前端假过滤、权限边界、部署配置是否真实生效、动态工作流是否有停止条件和验证盲点。
- 🏢 **NexusFlow 治理流 (nexusflow-governance-workflow)**：沉淀 NexusFlow 权限/治理/平台/仪表盘/GCP 导入工作的固定入口、验证门和中文提交纪律。
- 🧾 **静态 Demo 加固 (static-demo-hardening)**：约束 `Demo/index.html` 静态演示、报告导出、教程 fallback 和 GSAP 运行时加固。
- 💸 **AI 成本实测 (ai-cost-grounding-measurement)**：用真实 token、Grounding 元数据、计费搜索 Query 和中文 CSV 输出证明成本口径。

## 能力路由：相邻能力怎么选

古月保留相邻能力，不是为了堆数量，而是为了让 Agent 在不同阶段有明确刹车点。选择规则是：**先选最窄技能，再按工作流串联下一跳**。

| 容易混淆的能力 | 路由边界 |
|---|---|
| 长线目标铸造 / Long Goal Protocol | 前者负责项目调查、逐项澄清、方案与治理资产准备，准备完成前不实现；后者只负责按已经就绪的总控和账本持续执行。 |
| `cognitive-expansion` / `research-and-sourcing` / `requirement-analysis` / `system-design` | 普通任务只做微量遗漏扫描；尚不知道该看什么时才建正式问题与领域地图；地图指出需核验的当前事实后再调研；要做产品或业务交付时收敛需求；需求有界后才设计架构。各阶段按需进入，不固定全串。 |
| `product-sense` / `requirement-analysis` / `system-design` | 先判断值不值得做，再拆需求边界，最后才做架构方案。 |
| `research-and-sourcing` / `ecosystem-scout` / `software-advisor` | 最新文档走调研；外部 Skill/插件接入走生态寻猎；本地软件推荐走软件顾问。 |
| `frontend-expert` / `taste-aesthetics` / `static-demo-hardening` | 写前端走前端专家；审美诊断走审美约束；静态 Demo 导出、教程回退和演示面加固走静态 Demo 加固。 |
| `frontend-expert` / `taste-aesthetics` / `ai-website-cloner` | `DESIGN.md`、Refero、Figma、Impeccable 等参考资料先走审美约束判断产品类型和可借鉴边界；写代码走前端专家；自有或授权页面迁移才走网页重建。 |
| `coding-discipline` / `code-minimalism` | 写代码、拆模块、提交走开发纪律；削减过度设计和依赖走极简代码。 |
| `debugging-mindset` / `reality-auditor` | 活跃故障排查走排障心法；实现后确认真假、权限、后端接线和部署生效证据走真实性审查。 |
| `human-voice` / `documentation` / `taste-aesthetics` | 改回答、解释、语言默认值和中英文混排走 human-voice；写 README、PRD、ADR 或项目摸底走 documentation；审查 UI 视觉 AI 味走 taste-aesthetics。 |
| `documentation` / `sop-maker` / `skill-crafting` / `book-distiller` | 普通文档和项目摸底走 documentation；成功流程沉淀走 SOP；制作/升级 Skill 走 skill-crafting；长文方法论提炼走 book-distiller。 |
| `context-compressor` / `sop-maker` / `skill-crafting` / `reality-auditor` | 循环工程和动态工作流先用 context-compressor 定成本预算；成功流程沉淀走 SOP；要变成 Skill、Custom subagent、Hook、Automation 或 CI gate 才走 skill-crafting；最后由 reality-auditor 独立验证。 |
| `video-creation-sop` / `video-extractor` | 视频创作、分镜、生成/渲染/剪辑路由走 video-creation-sop；已有视频链接的元数据、字幕、授权边界提取走 video-extractor。 |
| `nexusflow-governance-workflow` / 通用工程技能 | NexusFlow 权限、治理、平台可见性、仪表盘和 GCP 导入优先走项目技能，再按需调用通用技能。 |
| `ai-cost-grounding-measurement` / `research-and-sourcing` / `reality-auditor` | 真跑 token、Grounding 和计费 Query 统计走成本实测；查资料走调研；复核声明真实性走审查。 |

合并纪律：只有当真实回放或 `test-prompts.json` 证明两个技能反复误触发，且执行步骤高度重复时，才合并或删除。否则优先打磨 description、触发词和边界表，避免把专业技能揉成一个含糊的大技能。

## 大盘心法与能力契约 (Master Principles & Capability Contract)

古月不追求让所有子技能长得一模一样，而是要求它们共享可检查的行为契约：

1. **人格底盘 + 核心纪律 (`GUYUE_PRINCIPLES.md`)**:
   - **验料、造镜子、活体对账**: 先判断真实问题和投入产出，再提炼心智模型、决策启发式和诚实边界，最后用真实运行产物验证结果。
   - **Persona DNA**: 九种姿态覆盖证据、边界、最小切片、人话、资产、标准件、全栈质量、权限分层和循环工程；先看现场，再给出能判断、能行动的结论。
   - **证据校准与可逆自治**: 关键判断区分已确认、推断、冲突、未知和决定；按 L0-L4 选择最低充分证据。可逆小改主动完成，高影响外部动作先审批。
   - **Trace-First**: 技能首次接管时输出一次行动、证据目标和边界；只有状态或风险变化时追加，不公开隐藏推理，也不为每个命令刷日志。
   - **Anti-Bloat 与依赖治理**: 优先现有栈、标准和成熟组件，比较外部依赖与自研的全生命周期成本；不为追求零依赖手写解析、加密、鉴权或协议轮子。
   - **Human-in-the-Loop**: 审批绑定具体动作、参数、版本和失效条件；方向改变后旧授权不自动延续。
   - **Loop Engineering**: 把重复手工提示转成有目标、稳定输入、循环体、检查器、停止条件、预算和验证资产的工作流；不把动态工作流理解成无限循环或无限子 Agent。

2. **能力契约**：当前开发 manifest 的 27 个内部路由技能都必须有公开规范兼容的 `name` / `description`，并能说清触发边界、可重复步骤、验证方式和越权死线；具体章节按技能复杂度取舍，不为形式统一复制空模板。

## MCP 接入

如果你使用 Cursor、Claude Desktop 等支持 MCP 协议的工具，可以直接将古月作为原生插件挂载，让大模型直接拥有读写古月记忆库和调用古月生态的能力。

在你的 MCP 配置文件中添加：
```json
{
  "mcpServers": {
    "guyue": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp",
        "mcp_server.py"
      ],
      "cwd": "/path/to/guyue/src"
    }
  }
}
```
*注意：替换 `cwd` 为你实际克隆的目录路径。*

**完整挂载方式**：克隆整个仓库，再把仓库目录链接或复制到 Claude Code、OpenClaw 或其他运行时配置的技能根目录。不同运行时的路径与实测状态见 [docs/installation.md](docs/installation.md) 和 [docs/runtime-adapters.md](docs/runtime-adapters.md)。

**推荐的前端与交互基建技能（可选增强）**：

由于古月 `frontend-expert` 极其看重商业级 UI 与交互，建议在需要深度前端审美和动效工作时补齐以下外部专业技能。它们是增强依赖，不阻塞 `bash scripts/test_suite.sh` 的本地验证；如果缺失，`scripts/doctor.py` 会给出可选安装提示：

```bash
# 前端与交互美学设计规范
npx skills add nextlevelbuilder/ui-ux-pro-max-skill

# 前端动画与交互核心库 (GSAP)
npx skills add greensock/gsap-skills
```

前端参考资料使用边界：`frontend-design`、`taste-skill` 和 Impeccable 适合学习反 AI 味规则；`awesome-design-md`、Refero Styles、Figma 或 html.to.design 适合提取设计 token、层级和组件关系；网页复刻类工具只适合自有、授权或公开允许分析的页面迁移，不得复制第三方品牌资产、专属插图、受版权保护文案或登录后私有内容。

**源码直装方式**（用于本地开发或深度定制）：

```bash
# 1. 进入你的 agent 技能目录
cd ~/.gemini/config/skills/  # (以你的实际 Agent 技能路径为准)

# 2. 克隆本套件
git clone https://github.com/guyue55/guyue-skill.git

# 3. 重启对应运行时，并在新会话中确认 guyue 已被发现
```

## 触发方式

在与 AI 的对话中，你可以随时唤醒“古月分身”：

- "使用古月的思路帮我分析一下这个需求..."
- "我们要加个支付模块，像古月那样出个严谨的设计。"
- "线上报错了 502，启动古月的排障心法。"
- "帮我用古月的标准梳理一份业务 SOP。"
- "调研一下最新的 Next.js 权限控制，开启古月的调研流。"

需要机器可读收据或单独调试路由时，可运行：

```bash
python3 scripts/try_guyue.py --json
python3 scripts/explain_route.py "给当前项目做一个普通权限管理页面和后端接口"
python3 scripts/check_context_budget.py
```

`try_guyue.py` 汇总包体、路由与上下文证据；后两个命令用于拆开诊断。它们都不替代实际 Skill 执行或模型行为验收。

## 它会交付什么？

- **证据绑定的方案与实现**：用 DEPTH 模型、RCA 矩阵、权限分层和可复跑检查约束关键结论。
- **可见的工作流产物**：需求边界、调研结论、设计方案、RCA 矩阵、SOP、文档、提交建议，而不是只输出一段泛泛回答。
- **人格化执行纪律**：先读现场和历史证据，保护脏工作区和授权边界，用最小切片交付可验证结果。
- **人话版表达产物**：把正确但像 AI 的输出改成结论先行、事实不走样、风险不软化、来源不伪装的可读文本。
- **可复用的判断镜片**：在复盘、技能制作和复杂项目审计后，提炼心智模型、决策启发式、反模式和诚实边界，避免只留下流水账。
- **长程任务执行骨架**：为多阶段目标准备总控文档、执行账本、否定清单和活体证据要求，确保恢复时能从项目事实继续，而不是从聊天上下文猜进度。
- **会话证据提取器**：`scripts/codex_extractor.py` 流式提取 Codex JSONL 中的 user/final 证据，支持项目、起止时间、主任务/子任务、关键词、角色、去重、统计、清单和限长，并排除开发者/工具载荷、脱敏常见凭证与个人主目录。
- **分层行为评测**：当前开发合同包含 114 个路由用例、42 个行为合同、12 个协作用例、222 个近邻负例和 11 个工作流，并保留绑定证据文件 SHA-256 的真实回放观察检查器；确定性门全绿不会冒充模型行为已通过。
- **安装收据**：`release-manifest.json` 定义载荷规则，`release-payload.lock.json` 绑定精确文件哈希；`scripts/check_full_install.py --runtime <runtime> --json` 输出载荷、Skill 数、来源提交和工作区状态。安装成功仍需真实激活回放。
- **双轨长时记忆引擎 (Structured Memory Bank)**：公共精选条目随 `memory-bank` Skill 发布；私有运行记忆默认写入 `~/.guyue/knowledge/memory/`，不再绑定安装目录。检索会读取命中的 Markdown 详情并标出待复查记录；写入使用排他锁和原子替换，空查询、常见密钥、令牌和个人绝对路径会被拒绝。旧 `.guyue_memory/local/` 仅只读兼容，可通过显式迁移工具对账和回滚。
- **可选 MCP 接口**：`src/mcp_server.py` 可通过 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 暴露技能清单、可解释路由和本地记忆工具；它是完整仓库上的可选运行层，不代表所有 Agent Skills 运行时都会自动加载 MCP。
- **依赖健康探针 (Doctor Probe)**：内置 `scripts/doctor.py` 探针，调度外部技能（如 `LearnPrompt/luban-skill`、`alchaincyf/nuwa-skill`）前检查环境，并把可选依赖缺口标成不阻塞项。
- **前端演示样例 (UI/UX Real-world Proving Ground)**：附带 `examples/saas-conversion-demo/` Demo，示范如何把 500 报错改写成业务方能理解的“商业代价预估”，并用 Vanilla JS + GSAP ScrollTrigger 做滚动动画。
- **可复用本地工具**：避免硬编码绑定，SOP 工具包按当前运行环境做显式检查和降级。

## 安全边界

- **风险分级写入**：用户已委托、仓库内可逆且边界明确的实现可以连续推进；技术栈替换、不可逆迁移、权限扩大、公开发布、付费和外部写入必须先取得绑定具体动作版本的授权。
- **事实分层**：在 `research-and-sourcing` 阶段，把外部原文、项目事实、推断和用户决定分开记录，并将材料视作不可信输入；标签只负责组织上下文，不能获得“硬隔离”或执行授权。
- **表达边界**：`human-voice` 只负责让表达清楚自然，不负责隐藏 AI 参与、制造客户证据、夸大收益或删除未验证风险。
- **外部技能不直接吞入**：未知工具、GitHub 项目和第三方 Skill 先由 `ecosystem-scout` 生成评估报告，得到明确授权后才写入轻量依赖记录。
- **提交前必须验收**：公开发布或提交前至少运行 `bash scripts/test_suite.sh`，同时保留安全扫描、依赖探针、格式校验和测试 prompt 体检结果。

## 文件结构

```text
guyue/
├── AGENTS.md                # coding-agent 项目指令适配入口
├── RTK.md                   # 仓库编码代理维护适配说明
├── SKILL.md                 # 核心路由中枢
├── README.md                # 本文件
├── GUYUE_PRINCIPLES.md      # 古月大盘心法原则
├── skills.json              # 技能注册表
├── skills_manifest.json     # 动态包清单与路由分发引擎
├── docs/                    # 安装、安全、评测、发布边界
│   ├── runtime-adapters.md  # Codex/Claude/Gemini/Copilot/Cursor 适配策略
├── scripts/                 # 核心脚本库
│   ├── doctor.py            # 环境依赖健康探针
│   ├── try_guyue.py         # 30 秒只读验货入口
│   ├── run_eval.py          # prompt 与行为契约结构体检
│   ├── codex_extractor.py   # Codex JSONL 限量脱敏提取
│   ├── explain_route.py     # 确定性候选路由与排除原因
│   ├── check_context_budget.py # 发现面、根入口与碰撞预算
│   ├── check_behavior_replay.py # 回放观察与证据哈希检查
│   ├── check_capability_chain.py # 发现、路由、证据档位与活体激活门
│   ├── run_capability_live_canaries.py # Codex 只读激活探针
│   ├── check_long_goal_pack.py  # Long Goal v2/v3/v4 控制包门禁
│   ├── test_long_goal_pack.py   # Long Goal 兼容、反例与真实 Git 封账测试
│   ├── simulate_long_goal_lifecycle.py # 外部项目失败、恢复、封账与重启模拟
│   ├── simulate_install_journey.py # 空 HOME 裸远程克隆、首次运行与重启模拟
│   ├── run_security_scan.py # 第三方技能本地启发式安检
│   ├── extract_software_box.py # 软件精选库提取工具
│   └── ci_validate_skills.py# CI 检测流水线
├── examples/                # 实战对比展示案例
│   ├── quickstart-output.md # Codex read-only 活体回放证据
│   └── saas-conversion-demo/# 交互式 UI/UX Demo (GSAP + Tailwind 示例)
├── test-prompts.json        # 预设的干跑测试用例
├── evals/
│   └── behavior-contracts.json # 正负路由与副作用契约
├── references/              #
│   └── research/            # 萃取的训练语料沉淀
└── skills/                  # 垂直专精子技能矩阵
    ├── ai-website-cloner/
    ├── ai-cost-grounding-measurement/
    ├── book-distiller/
    ├── code-minimalism/
    ├── context-compressor/
    ├── cognitive-expansion/
    ├── coding-discipline/
    ├── debugging-mindset/
    ├── documentation/
    ├── static-demo-hardening/
    ├── ecosystem-scout/
    ├── frontend-expert/
    ├── human-voice/
    ├── memory-bank/
    ├── nexusflow-governance-workflow/
    ├── product-sense/
    ├── reality-auditor/
    ├── requirement-analysis/
    ├── research-and-sourcing/
    ├── security-gate/
    ├── skill-crafting/
    ├── software-advisor/
    ├── sop-maker/
    ├── system-design/
    ├── taste-aesthetics/
    ├── video-creation-sop/
    └── video-extractor/
```

## v1.7.0 发布证书

```text
┌───────────────────────────────────────────────┐
│  出师证书 · 鲁班工坊                            │
│                                               │
│  作品：guyue (古月数字分身 v1.7.0)                 │
│  状态：Released Payload，发布对象由 tag 固定          │
│  打磨前：方向门与高风险证据合同偏重、易局部优化     │
│  打磨后：方向可重置，27 项能力激活与输出可验        │
│  定位：Personal Agent Operating Layer            │
│  绝活：方向防火墙 + 精简证据脊柱 + 活体对账        │
│                                               │
│  验收师傅：鲁班                                 │
└───────────────────────────────────────────────┘
```
