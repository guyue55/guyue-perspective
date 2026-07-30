# Guyue Showcase

这页只展示能追到代码、合同或历史回放的结果，并明确区分三种证据：本地确定性验货、行为合同、真实模型回放。

![Guyue read-only first-run flow](../assets/demo.gif)

## 1. 30 秒本地验货

运行：

```bash
python3 scripts/try_guyue.py
```

真实输出摘要：

```text
Guyue 30 秒验货
[PASS] 包体 complete | v1.3.0 | 26 Skills
意图: 给当前项目做一个普通权限管理页面和后端接口。
候选路由:
  1. requirement-analysis | 证据: 给当前项目做一个
  2. system-design | 证据: 权限管理
  3. coding-discipline | 证据: 后端接口
项目边界: static-demo-hardening 未误触
上下文: 0 个高相似路由碰撞
[PASS] 本地验货通过
```

它证明了四件事：完整仓库载荷存在；通用任务能命中有证据的候选路由；上下文型能力不会被泛词误触；发现面和根入口没有越过本地预算。它不证明目标运行时已发现古月，也不证明模型一定遵守行为合同。

## 2. 行为合同前后对照

这些是仓库已经固化的合同变化，不是假装刚刚完成的模型对话。

| 旧失败模式 | 当前合同 | 可复跑证据 |
|---|---|---|
| 新需求一律联网 | 稳定本地事实直接检查；只有不稳定、陌生、高风险或明确要求的外部事实查当前一手来源 | `stable-local-fact-avoids-web-research`、`current-api-uses-primary-research` |
| 没有用户贴日志就一律拒绝排障 | Agent 先读取当前可得的错误、测试、日志和活体产物；证据仍不足时才请求最小缺口，不用猜测性补丁 | `debugging-mindset`、Replay 3 |
| 模糊长目标直接交给执行 Agent 猜 | Forge 先做项目摸底，每轮只关闭一个最高影响问题；中断后从持久决定恢复，v4 再用控制修订、纵向风险门和批准恢复约束方向变化 | Long Goal Forge one-turn/multi-turn replay、`check_long_goal_pack.py --self-test` |
| 方案已确认仍重复要授权 | 仓库内可逆且边界明确的改动主动完成；只为公开、付费、破坏性、权限或不可逆动作保留版本化授权 | `bounded-reversible-work-does-not-reask-approval` |
| 一次绿色检查被写成全部完成 | 阶段、MVP、local-only、release candidate、production-ready 和 Goal complete 分开；FINAL 证据必须绑定 `clean@A`，并通过 A/B/C Git 封账 | Long Goal v4 evidence and seal gates |
| Skill 文件存在就算能力可用 | 分开验证原生发现、确定性选择、目标 body 实际加载、逐 Skill 输出、证据档位和安装载荷；外部依赖只进入候选态 | `check_capability_chain.py`、26 Skill live canaries、26 output reviews |

机器可读合同见 [`evals/behavior-contracts.json`](../evals/behavior-contracts.json)。当前执行 65 条正负行为合同；有期望子路由的合同必须完整命中，根编排合同可以不伪造子路由，但真实观察仍必须绑定独立证据文件和 SHA-256。

## 3. 真实模型回放

[`quickstart-output.md`](quickstart-output.md) 保留了真实 Codex 只读回放的通过、偏差、修复和阻断记录。它不会把 `partial_pass` 改写成成功，也不会把模型执行前的额度或登录阻断算作行为通过。

2026-07-12 的 one-turn 回放证明模糊 Long Goal 会在读取预算内收敛到一个最高影响问题；multi-turn 回放又真实保留了澄清、执行 Agent 停滞、结构失败、独立语义审查失败、修复与最终一行交接。证据见 [`long-goal-forge-live-2026-07-12.md`](../evals/evidence/long-goal-forge-live-2026-07-12.md) 与 [`long-goal-forge-multiturn-simulation-2026-07-12.md`](../evals/evidence/long-goal-forge-multiturn-simulation-2026-07-12.md)。诚实边界仍然是：这些回放不能替代其他运行时、公开网络安装或真实长期用户结果。

## 4. 可复现方式

- 本地验货：`python3 scripts/try_guyue.py`
- JSON 收据：`python3 scripts/try_guyue.py --json`
- GIF 校验：`python3 scripts/render_demo_gif.py --check`
- GIF 重建：`python3 scripts/render_demo_gif.py`
- VHS 录制：`vhs assets/demo.tape`
- 全量门禁：`bash scripts/test_suite.sh`

`assets/demo.tape` 运行真实的 `try_guyue.py`，不再通过 `echo` 编造记忆、路由或授权结果。没有 VHS 时，仓库内置渲染器会生成同一条 INPUT -> ROUTE -> BOUND -> PROVE 叙事的 GIF。
