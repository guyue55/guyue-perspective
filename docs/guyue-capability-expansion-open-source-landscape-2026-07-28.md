# 古月能力扩展与开源生态准入矩阵

日期：2026-07-28，2026-07-29 复审更新
状态：本地发现与 GitHub 项目路由已实施；外部运行时准入未证明
边界：两份指定上游已下载到临时隔离区并只读审查；未安装依赖、未执行上游代码、未注册新外部能力

## 1. 结论摘要

古月不缺能力名称，缺的是把“已有大脑、宿主工具、外部候选”稳定接起来的能力解析层。

本轮建议：

1. **不新增万能 Skill**：保留 27 个内置窄能力，核心只负责判断、路由、边界、证据与收尾。
2. **发现面已补齐，扩张仍从严**：中文 Skill 查找、GitHub 项目发现、本地优先和外部不足兜底已经进入确定性路由与留出样本；这不等于模型动作、联网检索或外部依赖已验证。
3. **宿主能力优先**：GitHub、浏览器、当前库文档、文档/表格/幻灯片等能力，优先调用运行时已提供的 Connector、Plugin、CLI 或 MCP，不复制进古月。
4. **优先验证 6 个候选**：Serena、Playwright CLI、Context7、MarkItDown、SkillSpector、Inspect AI；按用户当前边界，已知仓库 Issue/PR/代码操作的 GitHub Connector/MCP 暂不进入本轮。
5. **当前不升级任何新运行时依赖**：没有候选完成固定基线、安全扫描、留出样本、A/B 回放和退出验证；最高只能是“隔离候选”。

> [!IMPORTANT]
> 古月应像一颗小而强的大脑：内置判断与方法，外接眼、手和工具。外部工具失效时，核心仍能完成基础任务；外部工具存在时，古月负责挑选、约束、调度和验真。

## 2. 能力扩展分层

| 层级 | 古月保留什么 | 外部生态负责什么 | 防臃肿规则 |
|---|---|---|---|
| 核心大脑 | 需求、架构、实现纪律、调研、文档、记忆、安全、验真 | 不替代 | 只保留跨任务稳定判断 |
| 能力发现 | `ecosystem-scout`、`software-advisor`、路由器 | Skills 目录、MCP Registry、GitHub 搜索 | 只加载名称、用途、边界 |
| 能力执行 | 现有 Skill 组织任务 | GitHub、浏览器、代码语义、文档转换等工具 | 宿主已有优先，按需启用 |
| 质量保证 | `security-gate`、`reality-auditor`、现有评测 | 外部安全扫描、跨运行时评测、文档检查器 | 外部绿灯不能替代本地硬门 |

统一准入级别：

| 级别 | 含义 |
|---|---|
| 拒绝 | 冗余、风险大、维护重或无独特增益 |
| 仅学习 | 吸收方法，现有 Skill 执行；不注册、不安装 |
| 隔离候选 | 有明确补位价值，等待固定版本、安全扫描和 A/B |
| 运行时依赖 | 内置替代不可行且真实回放证明净收益；本轮无新增项 |

## 3. 当前能力与真实缺口

### 3.1 本地基线

| 能力域 | 当前权威入口 | 已覆盖 | 当前缺口 | 判断 |
|---|---|---|---|---|
| 找 Skill / 工具 | `ecosystem-scout`、私有本地索引、`find-skills` 外部候选 | 本地优先、语义候选、否定意图、外部兜底与四级准入 | `find-skills` 本机副本来源未验证；目录热度不能替代裁决 | 本地 MVP 已建立 |
| 找 GitHub 项目 | `ecosystem-scout`、Web / `gh search repos` | 中文路由、查询压缩、保护技术词、最多三轮增删词、查询谱系 | 未做真实 Web-vs-gh A/B；许可证与维护事实仍需逐仓核验 | 本地合同已建立 |
| 理解代码仓库 | `context-compressor`、`coding-discipline`、`rg` | 文件树、定向读取、复用扫描、验证 | 大仓符号关系和跨文件重构缺少稳定宿主能力 | P0 候选 |
| 更好地辅助工作 | Long Goal、调试、实现、验真、SOP | 从需求到交付的完整脑力链 | 浏览器验证、外部系统操作依赖宿主是否提供 | P0 候选 |
| 写文档 | `documentation`、`human-voice` | README、PRD、ADR、报告、项目摸底 | 输入格式转换、链接检查、风格自动检查未形成工具链 | P1 |
| 当前技术资料 | `research-and-sourcing` | 一手来源、版本、时间、冲突与引用 | 库/API 文档定点检索依赖宿主能力 | P0 候选 |
| Skill 安全 | `security-gate`、内置扫描器 | 本地启发式预检、授权边界、固定引用 | 语义攻击、供应链和 MCP 工具面仍需第二检查器 | P0 保留候选 |
| 评测与验真 | 路由、行为合同、活体回放、`reality-auditor` | 结构、路由、行为、证据哈希分层 | 跨运行时、外部 Agent 轨迹评测覆盖不足 | P1 候选 |
| 记忆与长任务 | `memory-bank`、Long Goal | 恢复、控制修订、证据索引、终局封账 | 当前没有证据证明需要数据库或知识图谱 | 不扩框架 |

### 3.2 当前路由探针

| 输入 | 当前结果 | 结论 |
|---|---|---|
| `帮我找技能` | `ecosystem-scout` + `find-skills` 候选 | 先查宿主、古月和登记能力；外部枚举不等于可信 |
| `帮我找一个能写文档的技能` | `ecosystem-scout` + 本地 `documentation` 候选 | 私有索引能提供轻量语义候选，公开收据不返回路径或描述 |
| `找工具` | lifecycle=`external_candidate`，候选 `find-skills` | 外部候选态不再被误写为失败 |
| `帮我找一个 GitHub 开源项目` | `ecosystem-scout` | GitHub 项目发现中文路由已建立 |
| `查找 GitHub 项目` | `ecosystem-scout` | 进入 Web / `gh search repos` 项目发现路径 |
| `写一份技术文档` | `documentation` | 复用现有文档 Skill，不新增能力 |
| `不要找技能，只解释 Skill 是什么` | 不进入 `ecosystem-scout`，无外部候选 | 显式否定优先 |
| `推荐提升沟通技能的课程` | 不进入 Agent Skill 发现 | 人类技能语义与 Agent Skill 分离 |

以上是确定性路由合同，不等于模型已执行本地检查、联网查询、来源复核或所声明动作。

### 3.3 两份指定上游逐文件审查

两份源码下载到本机临时隔离目录，只用于本轮只读审查；临时目录不进入发布包，长期谱系由下表的仓库 URL、固定提交和阅读范围保留。

| 上游 | 固定提交与阅读范围 | 可学习 | 不吸收 / 风险 | 古月落位 |
|---|---|---|---|---|
| [`github-research`](https://github.com/ranjanpoudel1234/ai-tools/tree/initial-tools/Opencode/skills/github-research) | `4039563ea501f6059cfbe8ae709137f6206603cd`；目标目录只有一份 306 行 `SKILL.md`，已完整读取 | `gh search repos`、owner/language 等显式过滤、`gh repo view --json` 的结构化取证思路 | 文件在未闭合示例中截断；写死企业组织、账号、Token scope 和 `~/bin/gh`；`AUTOMATICALLY INVOKE` 过宽；frontmatter 声称 MIT 但仓库未见许可证文件。按用户边界不吸收 Issue/PR/代码操作 | 仅学习；项目发现保留在 `ecosystem-scout`，不注册、不依赖 |
| [`gitsearchai`](https://github.com/TPFLegionaire/gitsearchai) | `4f5afeaf2e0316701cd75e203d2eec0b7768a932`；29 个版本文件，逐一读取一方源码/配置/文档，机械核对两份依赖锁和静态资源清单 | 非英文请求压缩为英文核心词；保护框架/品牌/用途词；只有显式语言才加 `language:`；结果过少删一词、过宽加一词；最多三轮；记录每轮查询、动作、结果数与耗时 | 需要 OpenRouter + GitHub Token，模型写死；没有许可证、业务 README、测试、鉴权、限流和成本门；仅搜仓库，未核验许可证/归档/维护；错误原文与服务端日志边界偏宽；不适合作为古月默认依赖 | 方法已压缩进 `ecosystem-scout` 和行为合同；不复制代码、不新增运行时 |

审查裁决：

| 项目 | 裁决 | 原因 |
|---|---|---|
| `github-research` | 仅学习 | 命令分类有用，但内容截断、强绑定个人/企业环境且触发过宽 |
| `gitsearchai` | 仅学习 | 查询改写与有界重试有独特方法价值，但双凭证、LLM 成本和服务面远重于 Web / `gh` |
| 新建 `github-research` Skill | 拒绝 | `ecosystem-scout` 已覆盖项目发现；已知仓库操作由宿主能力负责，避免重叠 |
| 引入 OpenRouter / GitHub Token | 拒绝默认依赖 | 宿主 Web 或已登录 `gh` 可以先完成轻量项目发现 |
| 吸收查询改写与重试纪律 | 适合纳入 | 已有明确失败模式、可独立表达、可用行为合同约束，且不增加运行时依赖 |

## 4. 开源 Skill 与目录生态

| 对象 | 独特价值 | 与古月关系 | 准入裁决 | 匹配度 | 优先级 |
|---|---|---|---|---:|---|
| [Agent Skills 规范](https://agentskills.io/home) | 跨运行时 `SKILL.md` 与渐进披露基线 | 已是公共兼容标准 | 仅学习，不另造格式 | 5/5 | P0 |
| [Vercel Skills / find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | `npx skills find`、Skills 目录与安装入口 | 已登记外部候选；补 Skill 发现 | 隔离候选，保留 | 5/5 | P0 |
| [OpenAI Plugins](https://github.com/openai/plugins) | 当前 Codex 插件、Skill、App、MCP 组合样本 | [`openai/skills`](https://github.com/openai/skills) 已弃用，不能继续当当前目录 | 仅作为当前目录和包装参考 | 4/5 | P0 |
| [MCP Registry](https://github.com/modelcontextprotocol/registry) | 官方 MCP 服务器目录/API | 补外部工具发现，不证明安全 | 仅作为候选目录 | 4/5 | P0 |
| [Anthropic Skills](https://github.com/anthropics/skills) | 生产型 Skill 结构与复杂文档能力参考 | 方法有价值；文档四件套为 source-available，不是开源依赖 | 仅学习 | 4/5 | P1 |
| [NVIDIA Skills](https://github.com/nvidia/skills) | 官方同步、签名、安全扫描与评测治理 | 可学习供应链治理；领域能力较专 | 仅学习；按 NVIDIA 任务单独候选 | 4/5 | P1 |
| [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) | 大量 Agent、Skill、Hook、Workflow 线索 | 第三方贡献多，适合发现不适合直接信任 | 仅作线索源 | 3/5 | P2 |
| [JetBrains Skills](https://github.com/JetBrains/skills) | 经筛选快照并保留上游来源 | 可帮助发现 IDE/工程类 Skill | 仅作线索源 | 3/5 | P2 |
| [MicrosoftDocs Agent Skills](https://github.com/MicrosoftDocs/Agent-Skills) | 把 Microsoft Learn 编译成 Azure Skill | 只在 Azure / Microsoft 任务有独特价值 | 领域隔离候选 | 3/5 | P2 |
| [Hugging Face Skills](https://github.com/huggingface/skills) | 模型、数据集、Hub、SageMaker 领域工作流 | 只在 Hugging Face 任务有独特价值 | 领域隔离候选 | 3/5 | P2 |

结论：**目录是雷达，不是能力仓库**。古月只需要统一查询与准入，不应复制目录内容。

## 5. GitHub、代码理解与工作辅助

| 对象 | 补的缺口 | 与现有能力的关系 | 准入裁决 | 匹配度 | 最小验证 |
|---|---|---|---|---:|---|
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | 已知仓库的代码、Issue、PR、Actions 等结构化操作 | 不属于本轮“按需求发现 GitHub 项目”；用户已要求先忽略 | 本轮排除，不进入项目发现 A/B | — | 用户重新打开该范围后再单独验证 |
| [Serena](https://github.com/oraios/serena) | 符号、引用、跨文件关系和语义编辑 | 补 `rg` 的符号关系，不替代小改和普通读取 | 隔离候选 | 5/5 | 在大型多语言仓做定位/改名 A/B |
| [Playwright CLI + Skills](https://github.com/microsoft/playwright-cli) | 浏览器流程、截图和页面验证 | CLI 比 MCP 工具定义更轻；补活体对账 | 隔离候选 | 5/5 | 同一页面流程与宿主浏览器工具对比 |
| [Context7](https://github.com/upstash/context7) | 当前、版本化的库/API 文档定点检索 | 补 `research-and-sourcing` 的技术文档入口 | 隔离候选；宿主已有时直接调度 | 5/5 | 3 个版本敏感 API 与官方文档交叉核对 |
| [Repomix](https://github.com/yamadashy/repomix) | 远程/本地仓库打包、Token 计数、结构压缩 | 已被 `context-compressor` 列为候选处方 | 隔离候选 | 4/5 | 大仓打包前后 Token、漏读和 Secretlint 对比 |
| [Aider repo map](https://aider.chat/docs/repomap.html) | 按依赖图和 Token 预算挑选关键代码 | 方法可由现有代码地图吸收 | 仅学习 | 4/5 | 用留出仓验证关键文件召回率 |
| [Superpowers](https://github.com/obra/superpowers) | 规格、计划、实现、评审阶段门 | 已登记候选；与古月中型开发互补 | 隔离候选，按具体工作流调用 | 4/5 | 不得作为所有任务的默认总流程 |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 领域语言、TDD、测试 seam、双轴评审 | 可直接映射进现有工程 Skill | 仅学习 | 4/5 | 留出功能验证质量增益 |
| [Spec Kit](https://github.com/github/spec-kit) | spec → plan → tasks → implement 的交接产物链 | 团队/多 Agent 交接强，个人小任务偏重 | 仅学习 | 3/5 | 只在多人交接任务试验 |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 持久浏览器状态、丰富结构和长循环 | 比 CLI 更重，适合探索式长循环 | 条件性隔离候选 | 3/5 | 只有持久状态收益超过上下文成本时启用 |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | 多角色、全生命周期方法 | 与古月小而强的定位冲突，角色与文档成本高 | 拒绝依赖；仅学习按规模调流程 | 2/5 | 无 |

建议的能力解析顺序：

1. 现有内置 Skill；
2. 当前运行时已提供的 Connector、Plugin、CLI 或 MCP；
3. `skills_manifest.json` 的隔离候选；
4. `find-skills`、MCP Registry、GitHub 原生搜索；
5. 安全预检和单样本 A/B；
6. 最后才考虑运行时依赖。

## 6. 文档输入、写作与质量工具链

| 对象 | 解决什么 | 与 `documentation` 的关系 | 准入裁决 | 匹配度 | 优先级 |
|---|---|---|---|---:|---|
| [MarkItDown](https://github.com/microsoft/markitdown) | PDF、Office、图片、音频、HTML 等转 Markdown | 补“读取输入”，不替代写作判断 | 隔离候选，优先于重型解析器 | 5/5 | P1 |
| [Pandoc](https://github.com/jgm/pandoc) | Markdown 与 DOCX、PPTX、HTML、PDF 等互转 | 补“交付格式”；转换可能有损 | 条件性隔离候选 | 4/5 | P1 |
| [Lychee](https://github.com/lycheeverse/lychee) | 检查 Markdown、HTML 与站点死链 | 补文档真实性门，不增加提示词 | 隔离候选，适合 CI | 4/5 | P1 |
| [Diátaxis](https://diataxis.fr/) | 区分教程、操作指南、参考、解释 | 可压缩进现有文档心智模型 | 仅学习 | 4/5 | P1 |
| [Vale](https://github.com/vale-cli/vale) | 对 Markdown 等文本执行可配置风格检查 | 补稳定术语和风格门；中文规则需单独证明 | 条件性隔离候选 | 3/5 | P2 |
| [Docling](https://github.com/docling-project/docling) | 高级 PDF 版面、表格、OCR、音频和多格式解析 | 比 MarkItDown 重；只在复杂文档失败时有价值 | 后备隔离候选 | 3/5 | P2 |

推荐最小链路：

`输入转换（MarkItDown） → 古月写作与证据判断 → 格式输出（Pandoc） → 链接检查（Lychee）`

Vale 与 Docling 不进入默认链路；有稳定中文风格规则或复杂 PDF 失败样本后再启用。

## 7. 调研、安全与评测

| 对象 | 独特价值 | 与古月关系 | 准入裁决 | 匹配度 | 关键风险 |
|---|---|---|---|---:|---|
| [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) | Skill 静态、AST、依赖与可选语义扫描 | 已登记高风险外部候选，补内置启发式 | 隔离候选，保留 | 5/5 | 仍不是完整供应链审计 |
| [Inspect AI](https://inspect.aisi.org.uk/) | 可运行 Codex、Claude Code、Gemini CLI 等外部 Agent 评测 | 补跨运行时和轨迹评测 | 隔离候选 | 4/5 | 体量、模型成本与运行沙箱 |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | 提示词回归、多模型对比和红队测试 | 现有评测已覆盖主要结构，方法仍可借鉴 | 仅学习 | 3/5 | Node 依赖与重复评测面 |
| [OpenEvals](https://github.com/langchain-ai/openevals) | 现成 LLM Judge、工具轨迹和多轮模拟 | 可学习评判接口；当前无独特硬门 | 仅学习 | 3/5 | 模型 Judge 不能自证正确 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | Reddit、X、YouTube、HN 等近时社区信号 | 已有独立评估；与事实核验互补 | 仅学习 | 3/5 | 凭证、抓取、社媒热度不等于事实 |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | 多页抓取、清洗和 LLM 友好 Markdown | 只在重复网站采集时有独特价值 | 后备隔离候选 | 3/5 | 浏览器、代理、站点授权与供应链 |
| [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) | Skill 注入、数据外传和代码模式扫描 | 与 SkillSpector 重叠，可作独立对照 | 仅学习 / 备用复核 | 3/5 | 新项目，需固定版本与误报验证 |
| [Snyk Agent Scan](https://github.com/snyk/agent-scan) | Agent、MCP、Skill 统一清单与扫描 | 覆盖广，但扫描 MCP 配置可能执行其中命令 | 拒绝默认依赖 | 2/5 | 未隔离执行会扩大风险 |

## 8. 明确不进入古月核心的重型体系

| 类别 | 代表项目 | 可学什么 | 为什么不依赖 |
|---|---|---|---|
| 多 Agent 框架 | [AutoGen](https://github.com/microsoft/autogen)、[CrewAI](https://github.com/crewAIInc/crewAI) | 所有权、交接、停止条件 | 古月不是 Agent 运行时；增加角色、状态和维护面 |
| 持久工作流 | [LangGraph](https://github.com/langchain-ai/langgraph)、[Temporal](https://github.com/temporalio/sdk-python) | checkpoint、补偿、重放 | Long Goal 已用 Markdown + Python 覆盖所需语义 |
| 编码 Agent 平台 | [OpenHands](https://github.com/OpenHands/OpenHands)、[SWE-agent](https://github.com/SWE-agent/SWE-agent) | 轨迹、环境隔离、任务接口 | 平台替代宿主，超出 Skill 层职责 |
| 记忆/知识图谱服务 | [Letta](https://github.com/letta-ai/letta)、[Cognee](https://github.com/topoteretes/cognee) | 作用域、生命周期、检索边界 | 当前两层记忆与索引足够，无已复现缺口 |
| 生产观测平台 | [Phoenix](https://github.com/Arize-ai/phoenix)、[Langfuse](https://github.com/langfuse/langfuse) | Trace、数据集、实验与回放 | 只适合具体 Agent 产品，不应成为 Guyue 安装前提 |

这些项目不是差，而是与“小而强、可独立运行”的产品边界不匹配。

## 9. 推荐优先级

### P0：已有能力发现（已完成本地切片）

1. 已为 `documentation`、`ecosystem-scout`、`find-skills`、GitHub 项目发现、否定意图和人类技能语义增加中文留出样本，没有新增 Skill。
2. 已建立私有本地语义索引，覆盖主要宿主 Skill 目录；默认只读使用，刷新仍需用户明确要求。
3. 已把 CLI、MCP、首轮验货统一到同一路由输入，并保留外部候选态。
4. 尚未完成：宿主 GitHub/Web 探针的真实 A/B、行为合同 required actions 的模型回放、当前版本活体激活和逐 Skill 输出质量刷新。

### P1：逐个做隔离 A/B

| 顺序 | 候选 | 固定基线 | 通过条件 | 回退 |
|---:|---|---|---|---|
| 1 | Serena | `rg` + 定向读取 | 大仓定位更快且引用召回不降 | 停用 MCP，回到文本工具 |
| 2 | Playwright CLI | 宿主浏览器或手工 smoke | 更少上下文完成同一活体验证 | 卸载 CLI / Skill |
| 3 | Context7 | 官方 Web 文档定点检索 | 版本准确率提升，引用能回到官方原文 | 停用工具，回到官方搜索 |
| 4 | MarkItDown | 当前文件解析路径 | 结构保真提高，敏感文件不外发 | 删除隔离环境 |
| 5 | SkillSpector | 内置安全扫描 | 新增有效发现且误报、网络、执行边界可控 | 保留内置扫描 |
| 6 | Inspect AI | 当前活体回放 | 跨运行时结果可重复且成本受控 | 保留当前回放脚本 |

每次只推进一个候选；没有旧失败样本和留出样本，不进入 A/B。

### P2：出现重复真实需求后再开

- Docling：复杂 PDF、OCR 或表格解析反复失败。
- Crawl4AI / last30days：多页采集或社区信号任务反复出现。
- Vale：形成稳定中文术语和风格规则。
- Microsoft、NVIDIA、Hugging Face 领域 Skill：进入对应技术栈项目。

## 10. 最终裁决

| 方向 | 本轮裁决 |
|---|---|
| 新增内置 Skill | 拒绝 |
| 扩大外部目录 | 仅作为发现源 |
| 吸收外部方法 | 允许，优先压缩进现有 Skill |
| 新增隔离候选 | 本轮不新增；6 个既有研究方向仍需逐个证明 |
| 新增运行时依赖 | 暂无 |
| 优先实施项 | 刷新真实动作证据与 Web-vs-gh A/B，不扩核心 |

方向状态：`LOCAL_DISCOVERY_MVP_VERIFIED / EXTERNAL_ADMISSION_UNPROVEN`

原因：本地路由、候选边界、否定意图、私有索引和声明式留出样本已经建立；但外部候选尚未完成来源健康、安检、真实 A/B、动作回放、相邻混淆与退出验证。下一步最小证明是用约 10 条真实中文问题比较 Skill 搜索的本地索引 vs `find-skills`、GitHub 项目的 Web vs `gh search repos`，记录召回、来源完整度、Token、延迟和误推荐；仍不安装新依赖。

## 11. 证据与时效

本地事实源：

- [`skills_manifest.json`](../skills_manifest.json)
- [`SKILL.md`](../SKILL.md)
- [`docs/learning-control.md`](learning-control.md)
- [`skills/context-compressor/SKILL.md`](../skills/context-compressor/SKILL.md)
- [`skills/ecosystem-scout/SKILL.md`](../skills/ecosystem-scout/SKILL.md)
- [`skills/documentation/SKILL.md`](../skills/documentation/SKILL.md)
- [2026 Q2 的 52 项逐仓研究账本](../references/research/16-ecosystem-study-2026-q2.md)
- [`last30days-skill` 独立评估](last30days-skill-intake-2026-07-28.md)

外部事实以表格中的官方仓库、官方规范或官方文档为一手来源，访问日均为 2026-07-28。搜索摘要只用于发现；匹配度、优先级和准入裁决是针对古月当前基线的判断，不是对上游项目的通用排名。任何安装或接入前必须重新核对精确提交、许可、维护状态、权限、网络、凭证与回退路径。
