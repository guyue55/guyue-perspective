#!/usr/bin/env python3
"""回归测试 cognitive-expansion 的精简高风险输出审计器。"""

from __future__ import annotations

from audit_cognitive_expansion_output import audit_output


VALID_OUTPUT = """## PRE-EVIDENCE-SNAPSHOT E0

- 用户原始框架：只比较采购价和标称能力。
- 已给事实：用户给了验收、事故、宣传和访谈片段。
- 候选/假设：真实决定还受失效恢复和保障能力影响。
- 冲突：宣传能力与现场工况是否一致未知。
- 未知：阈值、总体、事故频率和恢复窗口未知。

## B0 PRE-TOOL 预算账本

任务级总账 BΣ：本轮加一次独立复核共享上限，不自动续杯。

| 资源 | 硬上限 | 起始消耗 | 安全预留 | 状态 | 测量依据 |
|---|---:|---:|---:|---|---|
| 最大轮数 | 4 | 1 | 1 | 未触顶 | 会话计数 |
| 墙钟时间 | 35 分钟 | 1 分钟 | 5 分钟 | 未触顶 | 单调时钟 |
| 近似有效 Token | 350k | 20k 代理 | 52.5k | 未触顶 | 运行器收据后验 |
| 只读工具调用 | 12 | 2 | 2 | 未触顶 | 完成命令计数 |
| 材料打开 | 8 | 0 | 1 | 未触顶 | 无外部材料 |
| 可见输出 | 10k | 0 | 2k | 未触顶 | 完整产物字符代理 |
| 授权子任务 | 1 | 0 | 0 | 未使用 | 无子任务 |
| 付费成本 | 0 | 0 | 0 | 未使用 | 禁止付费 |

## 问题地图

| 视角 | 状态与依据 | 对决定的影响 | 关键未知 | 下一证据 |
|---|---|---|---|---|
| 验收可判定性 | 已给事实：有指标无阈值 | 决定能否判定合格 | 阈值与测试条件 | 验收方案 |
| 现场失效恢复 | 候选/假设：事故会改变可用性 | 决定是否进入试运行 | 频率与恢复时长 | 事故明细 |
| 运营保障 | 未知：补给与道路窗口未量化 | 决定实际产能和成本 | 停机分布 | 保障台账 |

## 证据边界

给定片段不是已核来源。不可恢复材料不授 S/E。
本轮 联网=禁止且未使用；因此只建立候选地图并返回 CE-EVIDENCE-GAP。

## 竞争解释与遗漏

| 对象 | 主解释 | 竞争解释或遗漏机制 | 可区分证据 | 结果如何改变地图 |
|---|---|---|---|---|
| 现场停机 | 主解释：设备可靠性 | 竞争解释：保障窗口才是瓶颈 | 同任务的故障与保障时序 | 决定先查设备还是保障 |
| 观察框 | 已记录常规工况 | 遗漏机制：极端工况未进入验收 | 极端工况复现实验 | 决定是否扩大验收范围 |

## 专业交接

| 责任域 | 具体专业角色 | 待交付的版本化工件 | 可观察通过条件 | 当前状态 |
|---|---|---|---|---|
| 效果识别 | 可靠性试验工程师 | 验收试验方案-v待定 | 指标、总体与判定规则完整 | CE-PROFESSIONAL-REVIEW |
| 运营容量与成本 | 应急保障运营负责人 | 容量成本模型-v待定 | 分母、窗口和停机数据完整 | CE-PROFESSIONAL-REVIEW |
| 安全与法域遗漏 | 公共安全合规负责人 | 安全边界审查-v待定 | 适用规则与遗漏场景闭合 | CE-PROFESSIONAL-REVIEW |

## 下一证据

最高价值下一项：验收试验方案-v待定｜所有者：可靠性试验工程师｜选择依据：先让采购验收变得可判定

## B1 FINAL 与停止

| 资源 | 硬上限 | 实际或代理消耗 | 状态 | 测量依据 |
|---|---:|---:|---|---|
| 最大轮数 | 4 | 1 | 未触顶 | 会话计数 |
| 墙钟时间 | 35 分钟 | 3 分钟 | 未触顶 | 单调时钟 |
| 近似有效 Token | 350k | 80k | 未触顶 | 运行器收据 |
| 只读工具调用 | 12 | 3 | 未触顶 | 完成命令计数 |
| 材料打开 | 8 | 0 | 未触顶 | 无外部材料 |
| 可见输出 | 10k | 3k 代理 | 未触顶 | 完整产物字符代理 |
| 授权子任务 | 1 | 0 | 未使用 | 无子任务 |
| 付费成本 | 0 | 0 | 未使用 | 禁止付费 |

地图状态：有界可用
决策就绪：否，CE-EVIDENCE-GAP、CE-PROFESSIONAL-REVIEW
证据边界：仅证明给定片段暴露了调研缺口。
重新开启条件：取得唯一下一证据并完成对应专业复核。
不得据此直接实施。
"""

VALID_RECEIPT = {
    "input_tokens": 100_000,
    "cached_input_tokens": 40_000,
    "output_tokens": 8_000,
    "reasoning_output_tokens": 3_000,
    "wall_clock_seconds": 180,
    "rounds": 1,
    "read_only_tool_calls": 3,
    "materials_opened": 0,
    "authorized_subtasks": 0,
    "paid_cost": 0,
}


def require_error(errors: list[str], fragment: str) -> None:
    if not any(fragment in error for error in errors):
        raise AssertionError(f"missing expected error {fragment!r}: {errors}")


def main() -> int:
    errors = audit_output(VALID_OUTPUT, VALID_RECEIPT)
    if errors:
        raise AssertionError(f"valid output was rejected: {errors}")

    wrong_order = VALID_OUTPUT.replace(
        "## PRE-EVIDENCE-SNAPSHOT E0",
        "## TEMP",
        1,
    )
    require_error(audit_output(wrong_order, VALID_RECEIPT), "E0")

    equivalent_wording = VALID_OUTPUT.replace(
        "用户原始框架：",
        "原始框架：",
    ).replace(
        "不可恢复材料不授 S/E。",
        "材料身份不可恢复，因此本轮未授予任何 S/E。",
    ).replace(
        "竞争解释：保障窗口才是瓶颈",
        "停机也可能主要由保障窗口造成，而不只是设备故障",
    )
    equivalent_errors = audit_output(equivalent_wording, VALID_RECEIPT)
    if equivalent_errors:
        raise AssertionError(f"equivalent wording was rejected: {equivalent_errors}")

    distributed_omission = VALID_OUTPUT.replace(
        "| 观察框 | 已记录常规工况 | 遗漏机制：极端工况未进入验收 |",
        "| 实际通行 | 原框架遗漏：只记录常规工况 | 极端工况可能阻断替代通行 |",
    )
    distributed_errors = audit_output(distributed_omission, VALID_RECEIPT)
    if distributed_errors:
        raise AssertionError(
            f"same-row omission semantics were rejected: {distributed_errors}"
        )

    comma_caps = VALID_OUTPUT.replace("350k", "350,000").replace("10k", "10,000")
    comma_errors = audit_output(comma_caps, VALID_RECEIPT)
    if comma_errors:
        raise AssertionError(f"comma-separated caps were rejected: {comma_errors}")

    source_laundering = VALID_OUTPUT.replace(
        "给定片段不是已核来源。不可恢复材料不授 S/E。",
        "给定片段已经核实。| E1 | 用户片段 | 已核来源 |",
    )
    require_error(audit_output(source_laundering, VALID_RECEIPT), "不可恢复材料不授")

    unrecoverable_source_claim = VALID_OUTPUT.replace(
        "候选/假设：事故会改变可用性",
        "来源主张：事故会改变可用性",
    )
    require_error(
        audit_output(unrecoverable_source_claim, VALID_RECEIPT),
        "不得在问题地图标记来源主张",
    )

    missing_competitor = VALID_OUTPUT.replace(
        "竞争解释：保障窗口才是瓶颈",
        "",
    )
    require_error(audit_output(missing_competitor, VALID_RECEIPT), "竞争")

    vague_role = VALID_OUTPUT.replace("可靠性试验工程师", "专家", 1)
    require_error(audit_output(vague_role, VALID_RECEIPT), "具体专业角色")

    bundled_next = VALID_OUTPUT.replace(
        "最高价值下一项：",
        "最高价值下一项：第一项\n最高价值下一项：",
    )
    require_error(audit_output(bundled_next, VALID_RECEIPT), "必须且只能")

    missing_stop = VALID_OUTPUT.replace("不得据此直接实施。", "")
    require_error(audit_output(missing_stop, VALID_RECEIPT), "不得据此直接实施")

    trailing_space = VALID_OUTPUT.replace(
        "地图状态：有界可用\n",
        "地图状态：有界可用  \n",
    )
    require_error(audit_output(trailing_space, VALID_RECEIPT), "行尾空格")

    overrun_receipt = {**VALID_RECEIPT, "input_tokens": 500_000}
    require_error(audit_output(VALID_OUTPUT, overrun_receipt), "超过硬上限")
    require_error(audit_output(VALID_OUTPUT, overrun_receipt), "CE-BUDGET-EXHAUSTED")

    print("Cognitive-expansion output auditor tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
