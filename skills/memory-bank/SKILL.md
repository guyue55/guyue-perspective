---
name: memory-bank
description: Record or recall verified decisions, fixes, lessons, and prevention for "记住这个坑", "上次怎么修的", /guyue-remember, and /guyue-recall. Separate public curation from private runtime memory, require provenance/evidence/lifecycle metadata, reject secrets, and never invent a match.
---

# guyue / memory-bank

记忆不是聊天摘要仓库，也不自动保存模型认为“以后可能有用”的内容。只有用户明确要求保存、记住或记录时，才把经证据确认、未来可能改变判断的决策与教训写入私有记忆，并带来源、作用域、置信度、生命周期和复查期限。

## 存储边界

- `skills/memory-bank/references/curated/index.json` 是随 Skill 发布的**公共精选索引**，默认可以为空；普通运行时不得写入。
- `~/.guyue/knowledge/memory/index.json` 与 `active/` 是默认的**本地私有运行存储**；`GUYUE_HOME` 可覆盖统一用户根目录，`GUYUE_MEMORY_DIR` 只保留为窄兼容覆盖。
- `~/.guyue/knowledge/memory/archive/` 保存无损归档详情。旧安装目录中的 `.guyue_memory/local/` 及更早的 `.guyue_memory/` 根布局只读发现，不再写入。
- 索引是定位入口，Markdown 是详情；先查索引，命中后只读相关详情。

## 何时使用

- **写入**：用户本轮明确要求“保存、记住、记录、记下来”或等价持久化动作，并且内容已经验证。
- **检索**：用户要求回忆或更新历史教训，或者当前任务与已知历史故障、长期 Goal 恢复或既往决定高度相关。

普通新请求不默认加载全部记忆。检索失败只说明“未命中”，继续当前任务的正常取证路线，不自动假设需要联网调研。
任务完成、信息重要、模型认为值得沉淀，或用户只要求复盘，都不能自动触发私有记忆写入。

## 写入契约

优先调用 `guyue_write_memory`。调用时必须传入用户本轮明确要求保存、记住或记录的 `user_intent`；缺失或是否定表达时拒绝写入。`user_intent` 只用于当次授权判断，不进入索引或 Markdown 详情。

每条 schema v2 记忆必须包含：

- `id`：稳定 `MEM-...` 标识；
- `Symptom`、`Root Cause`、`Solution`、`Prevention`；
- `provenance`：来自哪次任务、决定或证据；
- `scope`：未限定作用域的明确保存请求默认使用跨项目生效的 `user`；只有用户明确要求限于本项目时才使用 `project:<稳定项目标识>`；含糊的 `project` 不允许用于新写入；
- `evidence`：支持根因和解法的测试、日志、产物或人工确认；
- `confidence`：`low`、`medium` 或 `high`；
- `status`：`active`、`needs_review`、`superseded` 或 `archived`；
- `supersedes`：被本条替代的记忆 ID；
- `review_after`：需要重新验证的日期；
- `tags`、一句话 `summary` 和 UTC `timestamp`。

只记录已验证教训。仍在猜测的根因应留在排障记录，不写成高置信记忆。写入前扫描密钥、Token、私有地址、个人绝对路径和敏感日志；发现后先脱敏。索引更新必须取得排他锁并使用临时文件原子替换；锁超时或索引损坏时拒绝覆盖，不能对 JSON 做无锁字符串追加。

用户只要求“判断、整理候选记忆”而未授权写入时，输出 `candidate` 预览而不是伪造已落盘记录：保留来源、作用域、状态、置信度、失效条件和已知内容；`id`、`timestamp`、Trace 与存储收据留到真实写入时生成。长期决定不必硬套事故叙事，输入没有提供历史症状或根因时明确标为“不适用/未提供”，不得为了填满 `Symptom`、`Root Cause` 等字段编造事故。

## 检索契约

1. 把查询收敛为项目、模块、错误、决定或风险关键词；没有项目上下文时默认查询 `user` 全局经验。
2. 明确当前项目时，默认按“当前 `project:<稳定项目标识>` → `user`”检索公共精选索引和本地私有索引的 `tags`、`summary`、`scope`、`evidence`，最多返回 5 条摘要；需要纯项目结果时设置 `include_user=false`。
3. 只有显式设置 `cross_project=true` 才追加其他项目，排序保持“当前项目 → user → 其他项目”；Markdown 详情必须另行设置 `include_detail=true`。
4. 默认返回 `active` 和带 `requires_review` 标记的 `needs_review`；`superseded` 和 `archived` 仅在追溯历史时读取。
5. 命中后核对 `scope`、`confidence`、`review_after` 和证据是否仍适用于当前版本。
6. 只有高相关且未过期的记录才影响当前决定；否则把它标成历史线索并重新验证。
7. 未命中时明确输出 `[Trace: 未命中本地记忆]`，严禁编造“我们上次处理过”。

## 生命周期与 GC

- 新结论替代旧结论时，写新记忆并用 `supersedes` 把旧条目标成 `superseded`，保留审计链。
- 到达 `review_after` 或超过年龄上限时，运行 `python3 scripts/memory_gc.py --dry-run` 预览；实际执行只把条目标为 `needs_review`。详情超过大小上限时才无损归档。
- GC 必须移动完整详情、原子更新索引并保留 `archived_at` 与原因；缺文件、非法路径或坏索引要报告，不能静默删除。
- 旧数据迁移使用 `python3 scripts/migrate_guyue_data.py plan` 先检查，再显式执行 `migrate`；跨安装迁移用 `--legacy-dir` 指定旧目录。收据支持 `verify` 与 `rollback`，迁移不双写、不删除旧目录。
- 记忆不是完成证据。发布、权限和架构结论仍需对当前源码与活体产物重新核验。

## Trace 与边界

首次检索或写入时输出一次：

`[Trace: Guyue/MemoryBank] 检索或记录已验证教训；只读取命中项，不暴露私有内容`

只有命中状态、写入结果或安全边界变化时追加 Trace。不得逐条输出索引内容、内部推演或敏感详情。

## 反模式

- 不把整段聊天、原始日志或未经验证的猜测存成记忆。
- 不因任务完成、内容重要、模型推荐或“以后可能有用”自动写入记忆。
- 不把含糊的 `project` 当成所有项目共用桶，不默认混入其他项目，也不默认返回完整详情。
- 不让公开索引指向被发布规则排除或不存在的私有文件。
- 不把“曾经有效”写成“当前仍然有效”。
- 不因检索命中就跳过当前项目的测试、权限或版本核验。
- 不在用户未要求且历史不会改变判断时，为仪式感加载记忆。
