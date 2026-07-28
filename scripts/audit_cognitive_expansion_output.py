#!/usr/bin/env python3
"""机械审计精简后的 cognitive-expansion 专业/高风险交付。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SECTION_ORDER = (
    "## PRE-EVIDENCE-SNAPSHOT E0", "## B0 PRE-TOOL 预算账本",
    "## 问题地图", "## 证据边界", "## 竞争解释与遗漏",
    "## 专业交接", "## 下一证据", "## B1 FINAL 与停止",
)

BUDGET_RESOURCES = (
    "最大轮数", "墙钟时间", "近似有效 Token", "只读工具调用",
    "材料打开", "可见输出", "授权子任务", "付费成本",
)

MAP_HEADER = ("视角", "状态与依据", "对决定的影响", "关键未知", "下一证据")
CHALLENGE_HEADER = (
    "对象", "主解释", "竞争解释或遗漏机制", "可区分证据",
    "结果如何改变地图",
)
HANDOFF_HEADER = (
    "责任域", "具体专业角色", "待交付的版本化工件",
    "可观察通过条件", "当前状态",
)


def section_text(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    tail = text[start + len(heading) :]
    match = re.search(r"^## ", tail, re.MULTILINE)
    end = start + len(heading) + match.start() if match else len(text)
    return text[start:end]


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            rows.append(cells)
    return rows


def normalized(value: str) -> str:
    return re.sub(r"\s+", "", value)


def contains_any(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in patterns)


def rows_for_header(section: str, header: tuple[str, ...]) -> list[list[str]]:
    expected = tuple(normalized(cell) for cell in header)
    rows = table_rows(section)
    index = next(
        (i for i, row in enumerate(rows)
         if tuple(normalized(cell) for cell in row) == expected),
        None,
    )
    return rows[index:] if index is not None else []


def parse_quantity(value: str) -> float | None:
    match = re.search(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*([kK万]?)", value)
    if not match:
        return None
    number = float(match.group(1).replace(",", ""))
    if match.group(2) in {"k", "K"}:
        number *= 1_000
    elif match.group(2) == "万":
        number *= 10_000
    return number


def budget_rows(text: str, heading: str) -> dict[str, list[str]]:
    rows = table_rows(section_text(text, heading))
    return {row[0]: row for row in rows[1:]
            if len(row) >= 2 and row[0] in BUDGET_RESOURCES}


def require_receipt_number(
    receipt: dict[str, Any],
    key: str,
    errors: list[str],
) -> float | None:
    value = receipt.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"运行后收据缺少数值字段 {key}")
        return None
    return float(value)


def compare_cap(
    label: str,
    actual: float | None,
    cap_text: str,
    errors: list[str],
    *,
    multiplier: float = 1.0,
) -> None:
    cap = parse_quantity(cap_text)
    if cap is None:
        errors.append(f"{label} 的硬上限不可解析: {cap_text}")
    elif actual is not None and actual > cap * multiplier:
        errors.append(f"{label} 超过硬上限: actual={actual:g}, cap={cap * multiplier:g}")


def audit_receipt(
    caps: dict[str, list[str]],
    receipt: dict[str, Any],
    errors: list[str],
) -> None:
    input_tokens = require_receipt_number(receipt, "input_tokens", errors)
    cached_tokens = require_receipt_number(receipt, "cached_input_tokens", errors)
    output_tokens = require_receipt_number(receipt, "output_tokens", errors)
    if None not in (input_tokens, cached_tokens, output_tokens):
        effective = max(input_tokens - cached_tokens, 0) + output_tokens
        if "近似有效 Token" in caps:
            compare_cap("有效 Token", effective, caps["近似有效 Token"][1], errors)

    comparisons = (
        ("最大轮数", "rounds", 1.0), ("墙钟时间", "wall_clock_seconds", 60.0),
        ("只读工具调用", "read_only_tool_calls", 1.0),
        ("材料打开", "materials_opened", 1.0),
        ("授权子任务", "authorized_subtasks", 1.0),
        ("付费成本", "paid_cost", 1.0),
    )
    for resource, key, multiplier in comparisons:
        actual = require_receipt_number(receipt, key, errors)
        if resource in caps:
            compare_cap(
                resource,
                actual,
                caps[resource][1],
                errors,
                multiplier=multiplier,
            )


def audit_output(
    text: str,
    receipt: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if re.search(r"[ \t]+$", text, re.MULTILINE):
        errors.append("终稿不得包含行尾空格")
    headings = re.findall(r"^## .+$", text, re.MULTILINE)
    positions: list[int] = []
    for heading in SECTION_ORDER:
        try:
            positions.append(headings.index(heading))
        except ValueError:
            positions.append(-1)
            errors.append(f"缺少精确 H2 区块: {heading}")
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        errors.append("终稿区块未按规范顺序排列")
    if headings[:2] != list(SECTION_ORDER[:2]):
        errors.append("E0 和 B0 必须是终稿前两个语义区块")

    e0 = section_text(text, SECTION_ORDER[0])
    e0_fields = {
        "用户原始框架": (r"(?:用户)?原始框架\s*[：:]",),
        "已给事实": (r"已给事实\s*[：:]",),
        "候选/假设": (r"候选/假设\s*[：:]",),
        "未知": (r"(?:当前)?未知\s*[：:]",),
    }
    for label, patterns in e0_fields.items():
        if not contains_any(e0, patterns):
            errors.append(f"E0 缺少 {label}")

    b0 = budget_rows(text, SECTION_ORDER[1])
    b1 = budget_rows(text, SECTION_ORDER[-1])
    for label, rows in (("B0", b0), ("B1", b1)):
        missing = set(BUDGET_RESOURCES) - set(rows)
        if missing:
            errors.append(f"{label} 缺少预算资源: {', '.join(sorted(missing))}")
    if "BΣ" not in text:
        errors.append("缺少任务级总账 BΣ")

    map_rows = rows_for_header(section_text(text, SECTION_ORDER[2]), MAP_HEADER)
    map_count = max(len(map_rows) - 1, 0)
    if not 3 <= map_count <= 6:
        errors.append(f"问题地图必须保留 3–6 个视角，实际 {map_count}")
    allowed_states = (
        "已给事实",
        "候选/假设",
        "未知",
        "冲突",
        "来源主张",
        "有界推断",
        "价值/决定",
    )
    for row in map_rows[1:]:
        if len(row) != len(MAP_HEADER):
            errors.append("问题地图列数不正确")
            continue
        if not any(state in row[1] for state in allowed_states):
            errors.append("问题地图使用了非闭集状态")
        if not row[2] or not row[3] or not row[4]:
            errors.append("问题地图必须写决定影响、关键未知和下一证据")

    evidence = section_text(text, SECTION_ORDER[3])
    if "给定片段不是已核来源" not in evidence:
        errors.append("证据边界缺少: 给定片段不是已核来源")
    identity_missing = contains_any(
        evidence,
        (
            r"(?:没有|无|缺少|不可恢复).{0,12}(?:可恢复)?.{0,12}"
            r"(?:材料)?(?:身份|版本|日期|支持位置|来源)",
            r"(?:材料)?(?:身份|版本|日期|支持位置|来源).{0,12}不可恢复",
            r"不可恢复材料",
        ),
    )
    se_not_granted = contains_any(
        evidence,
        (
            r"(?:不授予|未授予|不授|未授).{0,8}S/E",
            r"S/E.{0,8}(?:不授予|未授予|不授|未授)",
        ),
    )
    if not identity_missing or not se_not_granted:
        errors.append("证据边界缺少: 不可恢复材料不授 S/E")
    if identity_missing and any("来源主张" in row[1] for row in map_rows[1:]):
        errors.append("不可恢复材料不得在问题地图标记来源主张")
    if "联网=禁止且未使用" not in evidence:
        errors.append("证据边界缺少: 联网=禁止且未使用")
    if re.search(r"\|\s*E\d+\s*\|", evidence):
        errors.append("不可恢复给定片段不得生成 E#")

    challenge_rows = rows_for_header(
        section_text(text, SECTION_ORDER[4]), CHALLENGE_HEADER
    )
    if len(challenge_rows) < 3:
        errors.append("竞争解释与遗漏必须至少包含竞争机制和遗漏机制两行")
    challenge_body_rows = [
        row for row in challenge_rows[1:]
        if len(row) == len(CHALLENGE_HEADER)
    ]
    omission_patterns = (r"遗漏", r"漏掉", r"未覆盖", r"未纳入", r"未进入")
    has_omission = any(
        contains_any("|".join(row), omission_patterns)
        for row in challenge_body_rows
    )
    # 固定表头已声明本列的两种语义；机械层只验证两类行齐备，
    # “候选机制是否真的不同”留给独立语义评审，避免关键词口令化。
    has_competitor = any(
        len(normalized(row[2])) >= 8
        and not contains_any("|".join(row), omission_patterns)
        for row in challenge_body_rows
    )
    if not has_competitor:
        errors.append("竞争解释与遗漏缺少 竞争 行")
    if not has_omission:
        errors.append("竞争解释与遗漏缺少 遗漏 行")

    handoff_rows = rows_for_header(section_text(text, SECTION_ORDER[5]), HANDOFF_HEADER)
    handoff_body = "\n".join("|".join(row) for row in handoff_rows[1:])
    for marker in ("效果", "运营", "安全"):
        if marker not in handoff_body:
            errors.append(f"专业交接缺少 {marker} 责任域")
    if len(handoff_rows) < 4:
        errors.append("高风险专业交接至少需要三个独立责任域")
    for row in handoff_rows[1:]:
        if len(row) != len(HANDOFF_HEADER):
            errors.append("专业交接列数不正确")
            continue
        if row[1] in {"专家", "领域专家", "独立专家"}:
            errors.append("专业交接必须给出具体专业角色")
        if not re.search(r"v(?:\d+|待定)|版本", row[2], re.IGNORECASE):
            errors.append("专业交接工件缺少版本规则")
        if "CE-PROFESSIONAL-REVIEW" not in row[4]:
            errors.append("未闭合专业交接必须标记 CE-PROFESSIONAL-REVIEW")

    next_section = section_text(text, SECTION_ORDER[6])
    if next_section.count("最高价值下一项：") != 1:
        errors.append("必须且只能给一个最高价值下一项")
    for marker in ("所有者：", "选择依据："):
        if marker not in next_section:
            errors.append(f"最高价值下一项缺少 {marker}")

    stop = section_text(text, SECTION_ORDER[7])
    for marker in (
        "地图状态：",
        "决策就绪：",
        "证据边界：",
        "重新开启条件：",
        "不得据此直接实施",
        "CE-EVIDENCE-GAP",
        "CE-PROFESSIONAL-REVIEW",
    ):
        if marker not in stop:
            errors.append(f"停止声明缺少: {marker}")

    for claim in ("已经可以采购", "已经可以实施", "专业批准已通过"):
        if claim in text:
            errors.append(f"高风险未就绪输出包含越界声明: {claim}")

    proxy = max(len(text), len(text.encode("utf-8")) / 2)
    visible_cap = b1.get("可见输出", b0.get("可见输出"))
    if visible_cap:
        compare_cap("可见输出字符代理", proxy, visible_cap[1], errors)

    receipt_caps = {**b0, **b1}
    if receipt is not None:
        audit_receipt(receipt_caps, receipt, errors)

    if any("超过硬上限" in error for error in errors):
        if "CE-BUDGET-EXHAUSTED" not in stop:
            errors.append("预算已越界却未返回 CE-BUDGET-EXHAUSTED")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8")) if args.receipt else None
    errors = audit_output(args.artifact.read_text(encoding="utf-8"), receipt)
    result = {"status": "pass" if not errors else "fail", "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("Cognitive-expansion output audit passed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
