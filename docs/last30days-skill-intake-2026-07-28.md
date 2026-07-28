# last30days-skill 收纳评估与最小证明

日期：2026-07-28
对象：`mvanhorn/last30days-skill`
结论级别：`仅学习`
执行边界：未安装、未下载、未执行外部代码，未写入 `skills_manifest.json`

## 1. 结论先行

`last30days-skill` 有明确方法价值，但不应直接收纳为古月核心能力，也不应在当前阶段作为运行时依赖。

推荐状态：

- `拒绝核心收纳`：能力面太宽，默认牵涉社媒抓取、凭证、浏览器会话、脚本执行和输出合约，容易污染古月现有调研路由。
- `拒绝运行时依赖`：尚无固定 commit 的本地安全扫描、真实 A/B 回放、凭证边界、退出方案和路由混淆测试。
- `仅学习`：吸收其工程方法，尤其是近时社区信号、doctor 诊断、输出合约前置、宿主渲染差异、来源状态和社区评论权重。
- `保留隔离候选条件`：只有当真实任务反复需要“近 30 天社区/社媒/市场信号”，且 `research-and-sourcing` 不能低成本完成，才进入隔离候选回放。

## 2. 已确认事实

外部项目公开 README 声称它是近 30 天 AI Agent 调研工具，按 upvotes、likes 和真实资金信号评分；当前运行时规范以 `skills/last30days/SKILL.md` 为准，并提供 `npx skills add mvanhorn/last30days-skill -g` 等安装方式。

当前公开 `SKILL.md` 的 frontmatter 显示：

- `name`: `last30days`
- `version`: `3.18.3`
- `description`: 研究任意主题近 30 天内的真实讨论，覆盖 Reddit、X、YouTube、TikTok、Hacker News、Polymarket、GitHub 和 Web，并带 doctor 健康检查。
- `allowed-tools`: `Bash`, `Read`, `Write`, `AskUserQuestion`, `WebSearch`
- 可选环境变量覆盖 ScrapeCreators、OpenAI、xAI、OpenRouter、Perplexity、Brave、Apify、X token、Bluesky、小红书等。

公开 README 还列出 Reddit、X、YouTube、TikTok、Instagram、HN、Polymarket、GitHub、Digg、arXiv、Techmeme、LinkedIn、StockTwits、Threads、Pinterest、小红书、Bluesky、Perplexity 和 Web 等来源。这个覆盖面证明它是“社区信号聚合器”，不是普通调研提示词。

来源：

- https://github.com/mvanhorn/last30days-skill
- https://raw.githubusercontent.com/mvanhorn/last30days-skill/main/skills/last30days/SKILL.md

## 3. 当前古月基线

古月已有 `research-and-sourcing`，负责当前事实、一手来源、版本、访问时间、冲突与引用核验；`skills_manifest.json` 明确把 `external Skill intake` 排除给 `ecosystem-scout`。

因此当前基线不是“古月没有调研能力”，而是：

- 已有能力：官方文档、当前事实、开源项目、API 变化、重要结论的一手来源核验。
- 明显缺口：跨 Reddit、X、YouTube、TikTok、HN、Polymarket 等社区/社媒/下注市场的近时声量排序。
- 不应混淆：社区热度不是事实真相；上游社媒抓取能力不能替代古月的来源谱系、事实期和业务决策边界。

## 4. 安全预检结果

本轮先修复了古月自己的 URL 目标扫描回归：`scripts/run_security_scan.py` 在目标不是本地路径时，之前会返回缺少 `scanned_files / total_files` 的结果，导致 CLI 输出崩溃。现在 URL 目标会稳定返回 Yellow，并明确“没有完成本地代码扫描”。

实际命令：

```bash
python3 scripts/run_security_scan.py https://github.com/mvanhorn/last30days-skill
```

结果：

- 状态：`Yellow`
- 扫描文件：`0/0`
- 命中项：`Manual Review`
- 判断：目标不是本地可读路径，只能记录来源，不能宣称已完成代码扫描。

回归验证：

```bash
python3 scripts/test_security_scanners.py
```

结果：通过。

安全边界：这不是供应链审计；没有固定 commit、本地隔离目录、文件哈希和全量文本扫描前，不得把该技能标为安全。

## 5. A/B 最小证明状态

推荐回放样本：`Hermes Agent Use Cases`

选择原因：

- 上游 `last30days` 自己在 `SKILL.md` 中记录过这个主题的失败样本：曾有运行把 raw evidence clusters 直接输出，后续通过输出合同修复。
- 这个主题正好测试“近时社区/视频/Reddit 讨论是否比普通 Web 调研更有价值”。
- 古月现有调研链路能完成事实核验，但不天然拥有跨社媒参与度排序。

当前可执行到的证明阶段：

| 项 | 状态 | 说明 |
|---|---|---|
| 外部来源识别 | 已完成 | README 与运行时 `SKILL.md` 已核验 |
| 本地去重 | 已完成 | 无 `last30days` 同名项；与 `research-and-sourcing` 是互补而非替代 |
| URL 安全预检 | 已完成 | Yellow，不再崩溃，但未扫描代码 |
| 固定版本本地扫描 | 未执行 | 需要下载或克隆外部仓库 |
| `last30days` 实跑 | 未执行 | 需要安装或执行外部脚本，并可能联网与写缓存 |
| A/B 结果对比 | 未完成 | 必须等外部执行授权后才成立 |

若后续授权，最小 A/B 动作应限定为：

1. 克隆固定 commit 到 `/private/tmp/last30days-skill-intake-*`，不安装到全局目录。
2. 对克隆目录运行 `python3 scripts/run_security_scan.py <clone-dir>`。
3. 只运行一个样本：`Hermes Agent Use Cases`。
4. 禁用或不配置私有凭证，只使用公开/零配置来源。
5. 记录输出、来源状态、耗时、写入位置、失败项和回滚动作。
6. 与古月 `research-and-sourcing` 的普通当前事实核验结果比较：覆盖、准确性、引用质量、社区信号独特性、成本、风险和误路由。

## 6. 可吸收方法

优先学习以下方法，不复制其长合约：

- 输出合同前置：把最容易被模型忽略的格式和事实纪律放在文件前部。
- stale clone 自检：运行前先检查是否读到过期安装位置。
- source status：区分 `no-results`、`partial`、`auth-failed`、`rate-limited`、`timeout`，避免把缺数据误写成“没有发生”。
- doctor 诊断：把缺 key、cookie 过期、source broken 变成可诊断状态，而不是让用户猜。
- 宿主渲染差异：Codex、Claude Code 等环境对链接显示不同，输出合约要按宿主调整。
- 社区评论权重：在“用户真实反馈/舆情/市场热度”任务中，评论和互动数是独特信号，但只能作为社区证据，不能替代事实核验。

## 6.1 本轮吸收落位

已按“仅学习”完成最小落位：

- `skills/research-and-sourcing/SKILL.md`：吸收 `source status` 纪律，要求记录 `found / no-results / partial / auth-failed / rate-limited / timeout / unreachable / skipped-unconfigured / error`，并明确只有 `no-results` 能支持“该来源本轮未发现相关证据”。
- `skills/research-and-sourcing/SKILL.md`：吸收社区信号边界，说明社媒、评论、点赞、浏览量、下注市场和趋势榜只能证明参与和偏好，不能替代事实核验。
- `skills/ecosystem-scout/SKILL.md`：吸收“仅学习收据”格式，固定来源主张、内置映射、验证样本、未采纳原因和退役条件。

未吸收：

- 不复制 `last30days` 的输出模板、运行命令、安装路径、插件缓存路径、凭证清单或长篇 voice laws。
- 不让 `research-and-sourcing` 默认抓取社媒；只有用户目标明确需要社区/市场声量时才把社区信号作为辅助证据。
- 不新增脚本、外部候选、manifest 项、发现缓存或运行时依赖。

## 7. 明确拒绝项

- 不把 `last30days` 写入 `external_dependencies`。
- 不增加一个 `last30days` 内置子 Skill。
- 不把社媒热度默认纳入所有调研任务。
- 不在未授权时执行 `npx skills add ... -g`。
- 不读取、使用或导出用户本机社媒 cookie、token、浏览器会话。
- 不把上游 README 的功能宣传当作已验证能力。

## 8. 最终决策

当前决策：`DIRECTION_UNPROVEN`

可落位等级：`仅学习`

下一步授权门：如果要升级到 `隔离候选`，需要用户明确批准一次隔离 A/B 回放，且批准必须绑定具体动作、目录、版本、样本和不使用私有凭证的边界。
