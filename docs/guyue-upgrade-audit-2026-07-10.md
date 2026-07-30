# 古月再度全面升级与鲁班审查报告（2026-07-10）

> [!NOTE]
> 本文冻结的是 2026-07-10 状态。2026-07-11 已补 1 条成功且哈希绑定的 Codex 路由审查回放，并据此把确定性合同从“任一期望路由命中”收紧为“全部期望路由命中”；当前结论见 [古月首轮体验打磨报告](guyue-first-run-polish-2026-07-11.md)。本文其余数字保留为历史基线。

## 结论

两轮升级都没有新增万能 Skill，也没有引入重型 Agent 框架。第二轮完整复核近十天 Codex 会话，并逐仓下载、阅读 52 个近期活跃或持续热门的 Skill、插件、提示词、上下文、记忆、长任务和评测项目。最终只吸收四个能被本地证明的缺口：可解释路由、上下文预算、Long Goal v3 委派收束、终局证据哈希绑定。

当前结论：**实现、定向门禁和故障注入已经通过；新版本的独立活体回放仍待可用且已登录的运行时补证。** Codex 与 Claude 的最新尝试都在模型执行前被外部账户状态阻断，因此不能写成行为通过，也没有把本轮未发布工作树冒充成发版。

## 证据顺序

### 1. 最近会话和任务记录

以 2026-07-10 15:59:10Z 为冻结点，扫描会话目录全部 79 份 Codex JSONL，其中 46 份在近十天窗口内有 user/final 证据：21 个主任务、25 个子任务、21 个根线程、9 个项目路径，共 840 条消息，0 个损坏文件。按消息时间而不是文件名日期筛选，因此较早创建但在窗口内恢复的任务不会漏掉；开发者指令和工具载荷不进入学习语料。

反复出现的模式：

- 首轮分类已证明“项目摸底”和“深度审查”各自在至少 11 个根线程、6 个项目重复，“测试-修复-重跑”在至少 15 个根线程、8 个项目重复；补入恢复型旧会话后这些结论只增强，不据此伪造新的精确分类数。
- 用户控制词中“提交”77 次、“继续”71 次、“全面”55 次、“真实”49 次，说明恢复、边界和完成口径不是偶发偏好。
- 结构门禁和脚本全绿后，真实 UI、旧 dev server、内容机器噪声仍可能失败。
- 阶段完成容易膨胀为愿景完成，缺少逐条用户承诺覆盖。
- 安装成功不等于运行时真正发现、激活并读取完整资源。
- 大批量一次性生成和大脚本修改容易放大格式、字符串和回滚成本。
- 手工翻 Codex JSONL 本身已成为重复且高成本的工作流。
- 子任务多次需要“停止扩张”“收束”；稳定委派包、所有权、BASE 版本、报告与独立审查应进入控制协议，而不是继续靠聊天催促。

### 2. 记忆、部署和发布证据

检查发现：

- 公开 `.guyue_memory/index.json` 指向被发布规则排除的 active 文件，形成悬空索引。
- MCP 写详情到记忆根目录，GC 却只扫描 `active/`，生命周期不一致。
- GC 通过截取首尾生成摘要后删除原文，存在无声信息损失。
- 发布文档声称 active memory 不随包发布，但被 Git 跟踪的索引仍暴露该路径。
- 发布证据虽丰富，但结构 prompt、真实行为和证据文件没有机器绑定。

### 3. 现有 Skills、Agent 与自动化

审查了 26 个路由 Skill、根 `SKILL.md`、原则、manifest、MCP、安装器、Doctor、CI、54 个测试 prompt 和发布脚本。

关键冲突：

- `system-design` 对所有架构工作强制停在 `approve`，与用户已经明确委托的可逆实现冲突。
- `research-and-sourcing` 对所有新需求强制联网，造成稳定本地问题过读。
- 根人格要求每个探针都输出 Trace，多个子技能又重复规定 Trace，制造上下文噪声。
- “零依赖”和固定技术年龄会诱导自研解析、鉴权、加密和协议实现。
- 项目专用治理流与 static-demo 技能包含泛触发词，容易污染无关项目。
- `skill-crafting` 要求每次扫描本机历史、重复等写盘授权，并引用不存在的固定审计脚本。
- Long Goal 自测的“有效包”只有三个空标题，无法证明控制包真的可执行。
- 安全预检只扫描前 200 个文件；已安装外部 Skill 可因目录存在绕过提交锁定。

## 外部工法调研

调研样本覆盖 Skill 规范、插件、提示词、任务持久化、上下文、记忆、编码 Agent 和评测体系。52 个仓库的精确 URL、冻结提交、逐仓判断和吸收映射见 [16-ecosystem-study-2026-q2.md](../references/research/16-ecosystem-study-2026-q2.md)。没有复制第三方源码，也没有把这些框架加入运行依赖。

### Skill 与插件

- [Agent Skills specification](https://agentskills.io/specification)：名称/描述在发现阶段加载，正文激活后读取，资源按需读取。吸收为 `discovered -> selected -> activated -> resource_read -> verified/failed` 生命周期。
- [Anthropic Skills](https://github.com/anthropics/skills)、[Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) 与 [SkillOpt](https://github.com/microsoft/SkillOpt)：吸收无 Skill 基线、留出回放、正负路由、碰撞检测和默认关闭的离线优化；不让生产 Skill 自动自改。
- [Superpowers](https://github.com/obra/superpowers)、[planning-with-files](https://github.com/OthmanAdi/planning-with-files) 与 [Symphony](https://github.com/openai/symphony)：吸收 brief/report/review、BASE..HEAD、稳定运行 ID、工作区所有权、心跳、停滞和预算收束；没有新增多 Agent 框架。

### 长任务、记忆与评测

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) 与 [human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)：吸收 checkpoint、恢复和中断审批概念，区分可重放、重放前核验、补偿和人工重批。
- [Letta memory blocks](https://docs.letta.com/tutorials/attaching-detaching-blocks/)：吸收记忆作用域、挂载边界和生命周期；没有引入 Letta 依赖。
- [OpenAI Agents tracing](https://openai.github.io/openai-agents-python/tracing/) 与 [human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)：吸收可观察动作轨迹、审批绑定和证据审计；Trace 不公开隐藏推理。
- [OpenHands](https://github.com/All-Hands-AI/OpenHands)、[SWE-agent](https://github.com/SWE-agent/SWE-agent)、[AutoGen](https://github.com/microsoft/autogen)、[Aider](https://github.com/Aider-AI/aider) 和 [Temporal Python SDK](https://github.com/temporalio/sdk-python)：用于对照任务边界、轨迹、恢复和确定性工作流。当前仓库用 Markdown + Python 已能实现所需语义，因此未增加框架依赖。

## 已落地升级

| 领域 | 升级结果 | 主要证据 |
|---|---|---|
| 人格 | 五类事实状态、L0-L4 证据阶梯、证据充分即停、可逆自治、版本化审批 | `GUYUE_PRINCIPLES.md`、根 `SKILL.md` |
| Trace | 首次接管一次，状态/风险变化才追加；不公开隐藏推理 | 根原则与各关键子 Skill |
| 依赖 | 从零依赖教条改为总生命周期成本；成熟领域能力优先验证库 | `system-design`、`code-minimalism` |
| 路由 | 确定性候选解释器、16 个正负行为契约、MCP 解释入口 | `src/skill_router.py`、`scripts/explain_route.py`、`guyue_explain_route` |
| 上下文 | 发现面、路由元数据、根入口、单 Skill 体积和相似碰撞预算 | `src/context_budget.py`、`scripts/check_context_budget.py` |
| Long Goal | v3 委派包、所有权、BASE、报告、双审、心跳与收束；v2 解析兼容 | 模板、协议、检查器与故障注入 |
| 活体证据 | 终局证据绑定仓库文件 SHA-256、实现版本、工作树状态、命令和退出码 | v3 evidence index 与篡改测试 |
| 记忆 | 公共精选/私有运行分离，schema v2，来源/证据/置信度/替代/复查，无损 GC | `src/memory_store.py`、MCP 测试 |
| 安全 | 全量文件扫描、空目标不绿、共享密钥规则、allow 标记不可绕过、精确提交锁 | 安全脚本与 205 文件回归 |
| 会话取证 | Codex JSONL 流式、限长、角色过滤、项目/日期/关键词、去重、统计、脱敏 | `scripts/codex_extractor.py` |
| 评测 | 结构 prompt + 行为契约 + 证据哈希绑定的真实观察 | `run_eval.py`、`check_behavior_replay.py` |
| 安装 | 运行时载荷收据、必要文件 SHA-256、来源提交与脏状态；已安装外部技能核对 origin/HEAD | `check_full_install.py`、可选依赖安装器 |
| 代码质量 | Ruff 纳入主门禁，修复重复字典键和静态告警 | `requirements.txt`、`test_suite.sh` |

## 量化变化

- 路由 Skill：26 个，未继续扩张。
- 结构测试 prompt：54 个。
- 机器可读行为契约：16 个，确定性路由 16/16。
- Skill 发现面：6212 / 12000 字符；根入口：10216 / 24000 字符（20378 UTF-8 字节）；高相似路由碰撞 0 个，预算告警 0 个。
- 安全扫描回归：205 个文件，第 205 个红旗可被拦截；空目录返回 Yellow。
- Long Goal 自测：空账本、未覆盖承诺、未知重放类别、未列阶段、缺失委派契约、孤立委派 TASK、重复证据 ID、过期终局证据和文件哈希篡改均被拒绝。
- 记忆测试：密钥/个人路径/坏日期拒绝，快速写入不碰撞，替代链生效，GC 无损归档。
- 官方 `skills-ref`：26/26 子 Skill 通过。
- Luban 出生证：13 PASS / 2 WARN / 0 FAIL。27 个 `SKILL.md` 是有意的根路由 + 窄能力结构；skills.sh 徽章因根级通用安装不完整而有意不加。
- 生态逐仓研究：52/52 下载并审阅，0 个运行时依赖加入。
- 本地主门禁：15 个阶段。

## 鲁班工坊结论

### 1. 验料结果

- 真实问题：成立。古月的核心价值不是“多一个提示词”，而是把模糊、长线、高风险工作变成有边界、有证据、可恢复的工程过程。
- 独特角度：来自跨项目实战纪律、可执行检查器、长任务控制包和活体对账，不来自模仿名人语气或堆 Skill 数量。
- 安装理由：临时问 Agent 很难稳定复现路由边界、证据等级、恢复协议、安全门和失败注入；完整仓库能提供这些持久资产。
- 公共传播性：钩子仍是“把浪漫目标变成可验证工程系统”；可展示物是路由解释 JSON、Long Goal 控制包、安装收据、回放观察和门禁报告。

验料结论：好料，继续精雕；不扩套件。

### 2. 访行记录

完整同行清单、URL、冻结提交与逐仓取舍见 [生态逐仓研究账本](../references/research/16-ecosystem-study-2026-q2.md)。直接同行覆盖 Agent Skills、Anthropic Skills、SkillOpt、Superpowers、planning-with-files、SkillSpector；间接同行覆盖 Symphony、LangGraph、Beads、Promptfoo、DeepEval；手艺同行覆盖 Impeccable、Ponytail、Vercel Skills 和官方供应商 Skill 集。

### 3. 生态位判断

- 纵向：古月已从人格提示词演进为个人 Agent 操作层，下一步应提高行为可证性，而不是继续扩角色。
- 横向：热门项目的共同优势是入口窄、安装清楚、产物可见、评测可复跑；共同风险是目录膨胀、运行时绑定和“装上即生效”的假设。
- 交叉定位：古月应占据“证据优先、可恢复、Anti-Bloat 的中文个人 Agent 操作层”，不与通用多 Agent 框架竞争。

### 4. 过尺结果

以下为本轮冻结基线与本地实测后评分；模型活体回放仍被账户状态阻断，因此实测表现没有给满分。

| 维度 | 权重 | 前 | 后 | 证据 |
|---|---:|---:|---:|---|
| Frontmatter 与触发条件 | 7 | 7 | 7 | 26 个公开 Skill 结构保持兼容 |
| 工作流清晰度 | 12 | 10 | 11 | 路由解释与 Long Goal v3 |
| 失败模式编码 | 12 | 9 | 11 | 负路由、停滞收束、哈希篡改注入 |
| 检查点设计 | 6 | 5 | 6 | 路由、预算、委派、终局证据四门 |
| 可执行具体性 | 17 | 14 | 16 | CLI、MCP、控制包字段与退出码 |
| 资源整合度 | 4 | 3 | 4 | 会话提取、研究账本、评测统一落点 |
| 整体架构 | 12 | 10 | 11 | 26 个 Skill 不扩张，新增能力落在公共基础层 |
| 实测表现 | 23 | 17 | 20 | 16/16 路由、故障注入、主门禁；新模型回放待补 |
| 反例与黑名单 | 7 | 5 | 7 | 项目误触、无限续派、旧证据、热门即质量均入门禁 |
| **总分** | **100** | **80** | **93** | **本地实测；非发布或跨运行时满分声明** |

### 5. 差距清单

- P0：新版本仍缺成功的独立模型活体回放，不能据此发布。
- P1：运行时还可能同时加载古月之外的大量全局 Skill；本地预算只能证明古月自身没有超限，不能替整个运行时背书。
- P1：通用 Skill CLI 的根包安装仍不保证携带完整载荷，必须继续要求完整仓库挂载与安装收据。
- P2：可以在额度恢复后补路由 A/B 盲评和不同 runtime 的发现/激活对账。

### 6. 三个打磨方向

- 方案 A，细修：只补文案与触发词。成本低，但无法解决委派漂移和旧证据。
- 方案 B，精雕：保留 26 个 Skill，新增可执行路由、预算、委派和证据门。能直接覆盖会话中的重复失败。
- 方案 C，开套件：引入多 Agent、评测与记忆框架。能力面更大，但依赖、上下文和维护成本失控。

推荐并已执行方案 B。用户已明确“全面升级、不要终止、按建议自动推进”，无需再次停在方向选择；公开发布仍不在该授权内。

### 7. 候选改写与验证资产

本轮保留的改动都已沉淀成仓库资产：`explain_route.py`、`check_context_budget.py`、Long Goal v3 检查器、Codex 会话提取器、16 条行为契约和 52 项研究账本。没有只留一次性分析脚本，也没有把第三方仓库 vendor 进来。

关键使用入口：

```bash
python3 scripts/explain_route.py "给当前项目做一个普通权限管理页面和后端接口"
python3 scripts/check_context_budget.py
python3 scripts/codex_extractor.py ~/.codex/sessions --since 2026-07-01 --until 2026-07-10 --thread-source user,subagent --inventory --stats --format json
python3 scripts/check_long_goal_pack.py --mode complete <goal-master.md>
```

### 8. README 与 Showcase

README 增加路由解释、上下文预算、Long Goal v3 与会话清单入口；现有可复现 GIF 和 quickstart 继续使用。没有为本轮伪造新截图或把被额度阻断的回放包装成 showcase。

### 9. 执行计划

- [x] 读取近十天全部 Codex 会话并冻结时间窗。
- [x] 下载并逐仓审阅 52 个纳入项目。
- [x] 实现路由、预算、委派与证据门。
- [x] 将门禁接入主评测和主测试套件。
- [ ] 额度和登录状态可用后，补至少 4 条留出模型回放。
- [ ] 只有收到明确发布祈使句后，才进行版本、提交、推送、tag 与发布动作。

### 10. 出师证书

```text
┌──────────────────────────────────────────────┐
│ 出师证书 · 鲁班工坊                         │
│                                              │
│ 作品：古月 Personal Agent Operating Layer   │
│ 过尺：80 分 -> 93 分（本地实测）             │
│ 定位：证据优先、可恢复、Anti-Bloat 的操作层  │
│ 绝活：路由、长任务和证据都能解释并复跑       │
│ 下一步：补独立模型活体回放，再判断发版       │
│                                              │
│ 验收师傅：鲁班                               │
└──────────────────────────────────────────────┘
```

### 11. 回炉清单

- 观察 Agent Skills 规范、Anthropic Skills、SkillOpt、Superpowers、Symphony 的变更，但只在现有门禁被真实案例推翻时吸收。
- 每次升级先跑会话清单和留出契约；连续两轮没有新失败模式时停止扩张。
- 不做清单：新 mega-skill、自动生产自改、第三方框架运行依赖、提示词抄录、无活体证据的发布声明。

### 12. 需要用户确认的问题

当前实现方向没有未决问题。提交、推送、打 tag、发布和公开元数据变更不在本轮授权内，留到用户明确下达对应祈使句。

### 13. 参考来源

来源以 [52 项逐仓研究账本](../references/research/16-ecosystem-study-2026-q2.md) 为准；热度发现补充参考 [Skills.sh](https://skills.sh/) 与 [Skills.sh FAQ](https://www.skills.sh/docs/faq)。

## 没有做的事

- 没有新增 Skill：本轮问题属于现有根人格、`skill-crafting`、Long Goal、memory、security 和 evaluation 的升级。
- 没有引入 LangGraph、Letta、Temporal、AutoGen 等框架：当前需求不值得增加运行复杂度。
- 没有提交、推送、打标签或发布：本轮用户未对这些具体 Git/外部动作下达命令。
- 没有修改公共仓库描述、Topics 或 Homepage：这属于公开元数据写入，需要单独授权。

## 当前验证与残余风险

已通过：

- 修复回炉问题后，`bash scripts/test_suite.sh` 连续 3 次通过全部 15 阶段；完整载荷收据 SHA-256 为 `9788ceef6df33915b7b546163166175e6912a216b9e4525fdc0794f4ad9cdbbd`
- `ruff check scripts src`
- `git diff --check`
- `claude plugin validate --strict .`
- 26 个子 Skill 的 `npx skills-ref validate`
- Codex 提取器对用户提供的 WorldOS JSONL 真实只读运行
- Luban 本地来源与精确提交验证

残余风险：

1. **新版本独立活体回放未补齐**：Codex CLI 在模型前命中 usage limit；Claude CLI 未登录。已记录 `blocked_before_model`，不能写成 pass。
2. **全局 Skill 上下文预算**：Codex 仍提示 2% description 预算截断。Guyue 已减重约 23.5%，但其他全局 Skills/插件需由用户按任务禁用或拆分环境。
3. **通用 Skills CLI 根包限制**：根 `SKILL.md` 安装不保证带完整路由载荷，仍需完整仓库挂载和安装收据。
4. **ShellCheck 未验证**：本机没有 `shellcheck`；`test_suite.sh` 已真实执行通过，脚本语法简单，但发布前可在具备 ShellCheck 的 CI 环境补一层。
5. **公开版本尚未切换**：manifest 和 badge 仍为已发布的 v1.3.0；只有在决定发布下一版本时才统一升版、重跑公开源安装并生成新证书。

## 发版前下一入口

1. 在额度可用的 Codex 或已登录 Claude 中回放至少 4 个留出契约：稳定本地事实、泛权限不误触上下文型能力、已批准可逆实现不重复询问、终局证据过期拒绝完成。
2. 把人工观察写成 observation JSON，绑定回放文件 SHA-256，运行 `check_behavior_replay.py`。
3. 决定版本号后统一更新 manifest、marketplace、badge、Changelog 和发布证书。
4. 再跑两遍主门禁、完整包收据、隔离安装、源码归档和公共来源安装。
