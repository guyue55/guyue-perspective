#!/usr/bin/env python3
"""Regression checks for cognitive-expansion's progressive contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise AssertionError(f"{label} is missing required marker: {marker}")


def require_all(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        require(text, marker, label)


def forbid_all(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker in text:
            raise AssertionError(f"{label} must not duplicate heavy protocol marker: {marker}")


def main() -> int:
    root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    skill_path = ROOT / "skills/cognitive-expansion/SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    agent_metadata = (
        ROOT / "skills/cognitive-expansion/agents/openai.yaml"
    ).read_text(encoding="utf-8")
    output_contract = (
        ROOT / "skills/cognitive-expansion/references/output-contract.md"
    ).read_text(encoding="utf-8")
    behaviors = json.loads(
        (ROOT / "evals/behavior-contracts.json").read_text(encoding="utf-8")
    )
    output_cases = json.loads(
        (ROOT / "evals/capability-output-quality.json").read_text(encoding="utf-8")
    )["cases"]

    require_all(
        skill,
        (
            "默认只补会改变判断的少量遗漏",
            "## 先选最小深度",
            "深度按**后果风险**而不是请求动词选择",
            "公共基础设施、安全关键设备",
            "准备后续调研",
            "证据不足只降低决策就绪度，不得把交付降成轻量清单",
            "## 默认运行微量拓界",
            "多维度/多角度/全面一点/有没有遗漏/第一次用/不懂这个产品",
            "种子集合",
            "新增遗漏数和最终视角数不是同一口径",
            "仅、只、严格限于、就这几项、不要扩展",
            "不读本 Skill 的 references",
            "不联网",
            "约 300 tokens",
            "## 通过升级门才加深",
            "发布日、事实发生期/数据期、版本/更正/撤回和访问日",
            "模式｜预计耗时区间｜联网/材料上限｜停止检查点｜主要不确定性",
            "不得仅因进入专业/高风险档再次索要“确认继续”",
            "只在联网、追加材料、委派、付费、写入或跨越单次预算前等待确认",
            "## 冻结探索预算",
            "PRE-EVIDENCE-SNAPSHOT E0",
            "B0 PRE-TOOL 预算账本",
            "任务级总账 BΣ",
            "最多 1 次自动实质重试",
            "额度/usage limit 阻断时自动重试为 0",
            "有效 Token",
            "缓存输入",
            "15% Token 安全预留",
            "材料打开只计算外部证据材料",
            "上限不是证据充分性",
            "## 正式地图按需加载",
            "references/output-contract.md` 控制卡",
            "references/domain-bootstrap.md",
            "references/cognitive-loop.md",
            "references/evidence-and-challenge.md",
            "references/output-contract.md",
            "唯一规范来源",
            "微量与轻量模式不加载输出合同卡",
            "地图完成与决策就绪分开判断",
            "不得据此直接实施",
            "事实伪造",
            "运行条件阻断",
            "## 保持协作与安全边界",
        ),
        "cognitive-expansion/SKILL.md",
    )

    # The public entrypoint should route into the detailed protocol, not duplicate it.
    if len(skill.splitlines()) > 130:
        raise AssertionError(
            "cognitive-expansion/SKILL.md exceeds the 130-line progressive-loading budget"
        )
    forbid_all(
        skill,
        (
            "## 使用 C → S → E → I 证据链",
            "### 原子来源主张 `E#`",
            "`A1.E；状态=...；总体=",
            "消费者只计算**直接写出该 E#",
            "发送终稿前做一次**字面序列化门**",
        ),
        "cognitive-expansion/SKILL.md",
    )

    require_all(
        output_contract,
        (
            "微量与轻量模式不加载本卡",
            "## 固定交付顺序",
            "## PRE-EVIDENCE-SNAPSHOT E0",
            "## B0 PRE-TOOL 预算账本",
            "## 问题地图",
            "给定片段不是已核来源",
            "不可恢复材料不授 `S/E`",
            "竞争解释与遗漏",
            "同一观察结果的另一条因果链",
            "只是证据状态，不算竞争机制",
            "效果或有效性识别",
            "运营容量与成本",
            "安全、权利或法域遗漏",
            "生产模型看不到任务结束后才生成的运行器收据",
            "模型侧代理，运行器收据待补",
            "运行器收据才是最终用量事实",
            "所有正式表格必须使用 ASCII `|`",
            "B0 表后必须单独写一行 `BΣ：`",
            "题面给出的材料类型只能写成“用户标注为……”",
            "不得自行补充匿名、官方、内部、独立或具体机构",
            "证据边界认定材料身份不可恢复时",
            "不得出现 `来源主张`",
            "3–6 个会改变",
            "版本规则",
            "CE-BUDGET-EXHAUSTED",
            "CE-PROFESSIONAL-REVIEW",
            "最高价值下一项",
            "不得据此直接实施",
        ),
        "output-contract.md",
    )
    if len(output_contract.splitlines()) > 180:
        raise AssertionError("output-contract.md exceeds the 180-line lean contract budget")
    for relative, limit in (
        ("scripts/audit_cognitive_expansion_output.py", 350),
        ("scripts/test_cognitive_expansion_output_audit.py", 250),
    ):
        line_count = len((ROOT / relative).read_text(encoding="utf-8").splitlines())
        if line_count > limit:
            raise AssertionError(f"{relative} exceeds its {limit}-line budget")
    forbid_all(
        output_contract,
        (
            "最多 2 次实质重试",
            "最多 2 次自动实质重试",
        ),
        "output-contract.md",
    )

    require_all(
        root_skill,
        (
            "开放列举与微量拓界",
            "种子而非闭集",
            "只新增会改变当前答案的 1–3 个关键遗漏",
            "最终通常呈现 2–5 个视角",
            "仅、只、严格限于、就这几项、不要扩展",
            "发布日、事实发生期/数据期、版本/更正/撤回和访问日",
            "预计超过 10 分钟",
            "不因“等”自动联网",
            "一次只读、自包含交付不因专业或高风险标签重复索要确认",
            "额度/usage limit",
        ),
        "root SKILL.md",
    )

    require_all(
        agent_metadata,
        (
            "日常微量补盲；陌生或高风险领域建立可追溯认知地图",
            "surface a few decision-changing omissions",
            "map an unfamiliar domain when deeper evidence is needed",
        ),
        "cognitive-expansion agent metadata",
    )

    behavior = next(
        (
            item
            for item in behaviors
            if item["id"]
            == "unfamiliar-domain-budget-pressure-bounds-cognitive-loop"
        ),
        None,
    )
    if behavior is None:
        raise AssertionError("budget-pressure behavior contract is missing")
    required_forbidden_effects = {
        "continue searching after a hard cap",
        "wait indefinitely or repeatedly retry after runtime quota exhaustion",
    }
    if not required_forbidden_effects.issubset(behavior["forbidden_side_effects"]):
        raise AssertionError("budget-pressure contract does not bound overrun and retry")

    behavior_ids = {item["id"] for item in behaviors}
    required_behavior_ids = {
        "ambient-micro-expands-open-list-without-research",
        "explicit-closed-list-suppresses-expansion",
        "public-infrastructure-procurement-forces-high-risk-cognitive-contract",
    }
    missing_behavior_ids = required_behavior_ids - behavior_ids
    if missing_behavior_ids:
        raise AssertionError(
            f"missing open-set behavior contracts: {sorted(missing_behavior_ids)}"
        )

    quality_case = next(
        (item for item in output_cases if item["skill"] == "cognitive-expansion"),
        None,
    )
    if quality_case is None or not any(
        "CE-BUDGET-EXHAUSTED" in criterion
        for criterion in quality_case["criteria"]
    ):
        raise AssertionError(
            "output-quality contract does not cover budget exhaustion"
        )

    print("Cognitive-expansion progressive contract checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
