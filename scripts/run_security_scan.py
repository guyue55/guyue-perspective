#!/usr/bin/env python3
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from security_patterns import find_secret_matches  # noqa: E402

RED_PATTERNS = [
    "ignore previous instructions",
    "curl -s",
    "| bash",
    "rm -rf",
    "os.system(",
    "subprocess.run(",
    "password=",
    "token=",
    "api_key=",
]

YELLOW_PATTERNS = [
    "http://",
    "https://",
    "chmod +x",
    "eval(",
    "exec(",
    "open(",
]

TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}
IGNORED_PARTS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
}


def candidate_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and candidate.suffix.lower() in TEXT_SUFFIXES
        and not IGNORED_PARTS.intersection(candidate.parts)
    )


def run_scan(target_path):
    print(
        f"[Trace: Guyue/SecurityGate] 启动本地启发式预检，扫描目标: {target_path} ..."
    )

    path = Path(target_path).expanduser()
    if not path.exists():
        return {
            "status": "Yellow",
            "total_files": 0,
            "scanned_files": 0,
            "findings": [
                {
                    "type": "Manual Review",
                    "severity": "Medium",
                    "desc": "目标不是本地可读路径；仅能记录来源，不能宣称已完成代码扫描",
                }
            ],
        }

    files = candidate_files(path)

    findings = []
    if not files:
        findings.append(
            {
                "type": "No Eligible Files",
                "severity": "Medium",
                "desc": "目标中没有可读的受支持文本文件；不能据此给出 Green",
            }
        )
    scanned_files = 0
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(
                {
                    "type": "Read Error",
                    "severity": "Medium",
                    "desc": f"{file_path}: {exc}",
                }
            )
            continue
        except UnicodeDecodeError as exc:
            findings.append(
                {
                    "type": "Decode Error",
                    "severity": "Medium",
                    "desc": f"{file_path}: {exc}",
                }
            )
            continue

        scanned_files += 1
        lowered = content.lower()

        for pattern in RED_PATTERNS:
            if pattern in lowered:
                findings.append(
                    {
                        "type": "Red Flag Pattern",
                        "severity": "Critical",
                        "desc": f"{file_path}: contains `{pattern}`",
                    }
                )
        for pattern in YELLOW_PATTERNS:
            if pattern in lowered:
                findings.append(
                    {
                        "type": "Sensitive Pattern",
                        "severity": "Medium",
                        "desc": f"{file_path}: contains `{pattern}`",
                    }
                )

        for line_number, line in enumerate(content.splitlines(), start=1):
            for label in find_secret_matches(line):
                findings.append(
                    {
                        "type": "Credential or Privacy Pattern",
                        "severity": "Critical",
                        "desc": f"{file_path}:{line_number}: contains {label}",
                    }
                )

    result = {
        "findings": findings,
        "total_files": len(files),
        "scanned_files": scanned_files,
    }

    if any(item["severity"] == "Critical" for item in findings):
        return {"status": "Red", **result}
    if findings:
        return {"status": "Yellow", **result}
    return {"status": "Green", **result}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_security_scan.py <target_path>")
        sys.exit(1)

    target = sys.argv[1]
    result = run_scan(target)

    print("\n" + "=" * 40)
    print("🛡️ 安全检查报告 (Local Heuristic Preflight)")
    print("=" * 40)
    print(f"扫描文件: {result['scanned_files']}/{result['total_files']}")

    if result["status"] == "Green":
        print("✅ 状态: Green (未命中内置红旗)")
        print("说明: 这只是全量本地启发式预检，不等于完整供应链安全证明。")
    elif result["status"] == "Yellow":
        print("⚠️ 状态: Yellow (敏感告警)")
        for f in result["findings"]:
            print(f" - [{f['severity']}] {f['type']}: {f['desc']}")
        print("建议: 需人工确认授权后方可执行。")
    elif result["status"] == "Red":
        print("❌ 状态: Red (致命拦截)")
        for f in result["findings"]:
            print(f" - [{f['severity']}] {f['type']}: {f['desc']}")
        print("建议: 存在红旗指标，严禁挂载！")
    else:
        print("❓ 状态: Error (扫描失败)")

    exit_codes = {"Green": 0, "Yellow": 1, "Red": 2}
    sys.exit(exit_codes.get(result["status"], 3))
