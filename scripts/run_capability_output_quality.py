#!/usr/bin/env python3
"""Run one realistic output task and an independent review for every Guyue Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

try:
    from audit_cognitive_expansion_output import audit_output
except ModuleNotFoundError:
    from scripts.audit_cognitive_expansion_output import audit_output


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTIFACT_DIR = Path(
    "evals/evidence/artifacts/capability-output-quality-2026-07-13"
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sanitize(value: object) -> str:
    text = str(value)
    for source, target in (
        (str(ROOT), "<REPO_ROOT>"),
        (str(Path.home()), "<HOME>"),
    ):
        if source:
            text = text.replace(source, target)
    return text


def decode_stream(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def extract_failure_diagnostic(stdout: str, stderr: str) -> str:
    """保留有界、已脱敏的非事件诊断，避免失败只剩异常堆栈。"""
    non_event_stdout = [
        line for line in stdout.splitlines()
        if line.strip() and not line.lstrip().startswith("{")
    ]
    diagnostic_lines = [*stderr.splitlines(), *non_event_stdout]
    diagnostic = sanitize("\n".join(diagnostic_lines[-20:])).strip()
    return diagnostic[-2000:]


def parse_events(raw: str) -> tuple[list[dict[str, object]], list[str], dict[str, object]]:
    commands: list[dict[str, object]] = []
    messages: list[str] = []
    usage: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") == "command_execution":
            commands.append(
                {
                    "command": sanitize(item.get("command", "")),
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                }
            )
        if isinstance(item, dict) and item.get("type") == "agent_message":
            messages.append(str(item.get("text", "")))
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
    return commands, messages, usage


def run_codex(
    prompt: str,
    timeout: int,
    model: str | None,
    codex_bin: str,
) -> dict[str, object]:
    started_at = time.monotonic()
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--json",
        "-C",
        str(ROOT),
        "--sandbox",
        "read-only",
    ]
    if model:
        command.extend(["--model", model])
    command.append(prompt)
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        stdout = result.stdout
        stderr = result.stderr
        exit_code = result.returncode
        timed_out = False
    except subprocess.TimeoutExpired as error:
        stdout = decode_stream(error.stdout)
        stderr = decode_stream(error.stderr)
        exit_code = 124
        timed_out = True
    raw = stdout + stderr
    commands, messages, usage = parse_events(raw)
    failure_diagnostic = ""
    if exit_code != 0 or not messages:
        failure_diagnostic = extract_failure_diagnostic(stdout, stderr)
    if timed_out:
        timeout_message = f"Codex execution timed out after {timeout} seconds"
        failure_diagnostic = (
            f"{timeout_message}\n{failure_diagnostic}".strip()
        )[-2000:]
    return {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "failure_diagnostic": failure_diagnostic,
        "commands": commands,
        "messages": messages,
        "usage": usage,
        "elapsed_seconds": round(time.monotonic() - started_at, 3),
        "raw_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    }


def parse_review(message: str) -> dict[str, object] | None:
    candidates = [message.strip()]
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", message, re.DOTALL)
    if fenced:
        candidates.insert(0, fenced.group(1))
    first = message.find("{")
    last = message.rfind("}")
    if first >= 0 and last > first:
        candidates.append(message[first : last + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def artifact_ref(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_case(
    case: dict[str, object],
    artifact_dir: Path,
    timeout: int,
    model: str | None,
    codex_bin: str,
    review_existing: bool,
) -> dict[str, object]:
    skill = str(case["skill"])
    skill_path = f"skills/{skill}/SKILL.md"
    output_path = artifact_dir / f"{skill}.output.md"
    producer_path = artifact_dir / f"{skill}.producer.json"
    review_path = artifact_dir / f"{skill}.review.json"
    if review_existing:
        if not output_path.is_file() or not producer_path.is_file():
            raise RuntimeError(f"{skill} lacks existing producer artifacts")
        output = output_path.read_text(encoding="utf-8").rstrip()
        producer_artifact = json.loads(producer_path.read_text(encoding="utf-8"))
        if producer_artifact.get("output_sha256") != file_sha256(output_path):
            raise RuntimeError(f"{skill} existing producer/output hash mismatch")
    else:
        producer_prompt = (
            f"你正在接受 Guyue 子能力输出质量验收。必须先读取 `{skill_path}`，"
            "然后仅依据该 Skill、仓库内可用事实和下面的自包含任务作答。"
            "全程只读；不修改文件、不联网、不安装、不提交。若完成任务缺少必要输入，"
            "正确输出应明确阻断、缺口和最小下一步，禁止编造。"
            "不要使用行尾空格制造 Markdown 硬换行。"
            "不要解释验收流程，直接交付用户产物。\n\n"
            f"用户任务：{case['prompt']}"
        )
        producer = run_codex(producer_prompt, timeout, model, codex_bin)
        messages = producer.pop("messages")
        output = sanitize(messages[-1].strip()) if messages else ""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")
        producer_artifact = {
            "schema_version": 1,
            "skill": skill,
            "skill_file_read": any(
                skill_path in str(item.get("command", ""))
                for item in producer["commands"]
                if isinstance(item, dict)
            ),
            "output_artifact": artifact_ref(output_path),
            "output_sha256": file_sha256(output_path),
            **producer,
            "boundary": "Sanitized command evidence; full raw stream and reasoning are not retained.",
        }
    mechanical_errors: list[str] = []
    if skill == "cognitive-expansion" and output:
        usage = producer_artifact["usage"]
        runtime_receipt = (
            producer_artifact.get("runtime_receipt") if review_existing else None
        )
        if not isinstance(runtime_receipt, dict):
            runtime_receipt = {
                "input_tokens": usage.get("input_tokens"),
                "cached_input_tokens": usage.get("cached_input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "reasoning_output_tokens": usage.get("reasoning_output_tokens"),
                "wall_clock_seconds": producer_artifact["elapsed_seconds"],
                "rounds": 1,
                "read_only_tool_calls": sum(
                    1
                    for item in producer_artifact["commands"]
                    if isinstance(item, dict) and item.get("status") == "completed"
                ),
                "materials_opened": 0,
                "authorized_subtasks": 0,
                "paid_cost": 0,
            }
        mechanical_errors = audit_output(output, runtime_receipt)
        producer_artifact["runtime_receipt"] = runtime_receipt
        producer_artifact["mechanical_audit_errors"] = mechanical_errors
    write_json(producer_path, producer_artifact)

    if producer_artifact["exit_code"] != 0 or not output or mechanical_errors:
        failure = (
            str(producer_artifact.get("failure_diagnostic", "")).strip()
            or "; ".join(mechanical_errors)
            or "producer returned no usable output"
        )
        review_artifact = {
            "schema_version": 1,
            "skill": skill,
            "parsed_review": {
                "status": "fail",
                "criteria": [],
                "findings": [failure],
                "boundary": "Reviewer skipped because the producer did not complete.",
            },
            "raw_final": "",
            "exit_code": 125,
            "timed_out": False,
            "failure_diagnostic": failure,
            "commands": [],
            "usage": {},
            "raw_sha256": hashlib.sha256(b"").hexdigest(),
            "review_skipped": True,
            "boundary": "No model review was run after producer failure.",
        }
        write_json(review_path, review_artifact)
        return {
            "skill": skill,
            "status": "fail",
            "criteria_count": len(case.get("criteria", [])),
            "producer_artifact": artifact_ref(producer_path),
            "producer_artifact_sha256": file_sha256(producer_path),
            "output_artifact": artifact_ref(output_path),
            "output_sha256": file_sha256(output_path),
            "review_artifact": artifact_ref(review_path),
            "review_artifact_sha256": file_sha256(review_path),
            "producer_usage": producer_artifact["usage"],
            "reviewer_usage": {},
            "findings": [failure],
            "boundary": "Producer or mechanical audit failed; model review was not started.",
        }

    criteria = [str(item) for item in case.get("criteria", [])]
    review_inputs = f"`{skill_path}` 和 `{artifact_ref(output_path)}`"
    if skill == "cognitive-expansion":
        review_inputs += f" 以及 `{artifact_ref(producer_path)}` 中的运行器收据和机械审计结果"
    reviewer_prompt = (
        "你是独立只读验收者，不采信作者自述。先读取 "
        f"{review_inputs}，逐项核验以下标准：\n"
        + "\n".join(f"{index}. {criterion}" for index, criterion in enumerate(criteria, 1))
        + "\n同时检查输出是否实质回答任务、是否编造事实、是否越过授权或证据边界。"
        "最终只能输出一个 JSON 对象，格式："
        '{"status":"pass|fail","criteria":[{"criterion":"...","status":"pass|fail","evidence":"..."}],'
        '"findings":["..."],"boundary":"..."}。'
        "只有全部标准通过且无重大真实性问题时总状态才是 pass。"
    )
    reviewer = run_codex(reviewer_prompt, timeout, model, codex_bin)
    review_messages = reviewer.pop("messages")
    review_message = sanitize(review_messages[-1].strip()) if review_messages else ""
    parsed_review = parse_review(review_message)
    review_artifact = {
        "schema_version": 1,
        "skill": skill,
        "parsed_review": parsed_review,
        "raw_final": review_message,
        **reviewer,
        "boundary": "Independent Codex session; synthetic task, not a real-user outcome.",
    }
    write_json(review_path, review_artifact)
    criteria_results = (
        parsed_review.get("criteria", []) if isinstance(parsed_review, dict) else []
    )
    passed = (
        producer_artifact["exit_code"] == 0
        and producer_artifact["skill_file_read"] is True
        and len(output) >= 120
        and reviewer["exit_code"] == 0
        and isinstance(parsed_review, dict)
        and parsed_review.get("status") == "pass"
        and len(criteria_results) >= len(criteria)
        and all(
            isinstance(item, dict) and item.get("status") == "pass"
            for item in criteria_results
        )
        and not mechanical_errors
    )
    return {
        "skill": skill,
        "status": "pass" if passed else "fail",
        "criteria_count": len(criteria),
        "producer_artifact": artifact_ref(producer_path),
        "producer_artifact_sha256": file_sha256(producer_path),
        "output_artifact": artifact_ref(output_path),
        "output_sha256": file_sha256(output_path),
        "review_artifact": artifact_ref(review_path),
        "review_artifact_sha256": file_sha256(review_path),
        "producer_usage": producer_artifact["usage"],
        "reviewer_usage": review_artifact["usage"],
        "findings": parsed_review.get("findings", []) if isinstance(parsed_review, dict) else ["review JSON was not parseable"],
        "boundary": "One synthetic read-only task and one independent review for this Skill.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--model",
        default=os.getenv("GUYUE_EVAL_MODEL"),
        help="Codex model identifier, for example the locally configured Terra 5.6 alias",
    )
    parser.add_argument(
        "--codex-bin",
        default=os.getenv("GUYUE_CODEX_BIN", "codex"),
        help="Codex CLI executable path; defaults to GUYUE_CODEX_BIN or PATH",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument(
        "--review-existing",
        action="store_true",
        help="Reuse hash-matched producer artifacts and run only their review",
    )
    args = parser.parse_args()
    config = json.loads(
        (ROOT / "evals/capability-output-quality.json").read_text(encoding="utf-8")
    )
    cases = [
        case
        for case in config["cases"]
        if not args.skills or case["skill"] in args.skills
    ]
    if not cases:
        raise SystemExit(f"unknown output-quality skills: {args.skills}")
    artifact_dir = args.artifact_dir if args.artifact_dir.is_absolute() else ROOT / args.artifact_dir
    if args.workers <= 0:
        raise SystemExit("workers must be positive")
    results_by_skill: dict[str, dict[str, object]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_case,
                case,
                artifact_dir,
                args.timeout,
                args.model,
                args.codex_bin,
                args.review_existing,
            ): str(case["skill"])
            for case in cases
        }
        for completed, future in enumerate(as_completed(futures), 1):
            skill = futures[future]
            result = future.result()
            results_by_skill[skill] = result
            print(
                f"[{completed}/{len(cases)}] {skill}: "
                f"{result['status']} {result['findings']}",
                flush=True,
            )
    results = [results_by_skill[str(case["skill"])] for case in cases]
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    if args.merge_existing and output_path.is_file():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        merged = {
            str(result["skill"]): result
            for result in existing.get("results", [])
            if isinstance(result, dict)
        }
        merged.update(results_by_skill)
        configured_order = [str(case["skill"]) for case in config["cases"]]
        results = [merged[skill] for skill in configured_order if skill in merged]
    passed = sum(result["status"] == "pass" for result in results)
    receipt = {
        "schema_version": 1,
        "status": "pass" if passed == len(results) else "fail",
        "runtime": "codex-cli",
        "runtime_version": subprocess.run(
            [args.codex_bin, "--version"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip(),
        "requested_model": args.model or "runtime-default",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": len(results),
        "results": results,
        "claims": {
            "all_skill_synthetic_output_quality_verified": passed == len(results),
            "real_user_value_verified": False,
            "cross_runtime_verified": False,
            "public_network_verified": False,
        },
        "boundary": (
            "Covers one realistic synthetic task per Skill with an independent review; "
            "does not prove every domain input or real-user value."
        ),
    }
    write_json(output_path, receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
