#!/usr/bin/env python3
"""验证能力验收运行器可安全记录仓库内外的产物路径。"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from scripts.run_capability_live_canaries import (  # noqa: E402
    artifact_ref as live_artifact_ref,
    write_audit_artifact,
)
from scripts.check_capability_chain import (  # noqa: E402
    model_activation_claim_verified,
    output_quality_identity_current,
)
from scripts import run_capability_output_quality as quality_runner  # noqa: E402
from scripts.run_capability_output_quality import (  # noqa: E402
    artifact_ref as quality_artifact_ref,
    evaluation_identity,
    evaluation_identity_matches,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    live_claim = {
        "status": "pass",
        "claims": {"model_activation_verified": True},
    }
    require(
        not model_activation_claim_verified(
            live_claim,
            routing_current=False,
            live_passed=27,
            live_total=27,
            expected_total=27,
        ),
        "stale routing evidence must never preserve model activation truth",
    )
    require(
        model_activation_claim_verified(
            live_claim,
            routing_current=True,
            live_passed=27,
            live_total=27,
            expected_total=27,
        ),
        "current complete live evidence should preserve model activation truth",
    )
    quality_identity = evaluation_identity()
    require(
        output_quality_identity_current(quality_identity) == (True, True),
        "output-quality receipt identity must bind the current contract and runner",
    )
    stale_identity = dict(quality_identity)
    stale_identity["evaluation_runner_sha256"] = "0" * 64
    require(
        output_quality_identity_current(stale_identity) == (True, False),
        "a changed output-quality runner must invalidate prior evidence",
    )
    require(
        evaluation_identity_matches(quality_identity)
        and not evaluation_identity_matches(stale_identity),
        "merge mode must reject receipts produced by a stale contract or runner",
    )
    repository_artifact = ROOT / "evals" / "evidence" / "sample.json"
    expected_repository_ref = "evals/evidence/sample.json"
    require(
        live_artifact_ref(repository_artifact) == expected_repository_ref,
        "激活验收运行器必须保留仓库内相对路径",
    )
    require(
        quality_artifact_ref(repository_artifact) == expected_repository_ref,
        "输出质量运行器必须保留仓库内相对路径",
    )

    with tempfile.TemporaryDirectory(prefix="guyue-runner-artifacts-") as temp_dir:
        artifact_dir = Path(temp_dir)
        external_artifact = artifact_dir / "cognitive-expansion.json"
        require(
            live_artifact_ref(external_artifact) == str(external_artifact),
            "激活验收运行器必须接受仓库外绝对产物路径",
        )
        require(
            quality_artifact_ref(external_artifact) == str(external_artifact),
            "输出质量运行器必须接受仓库外绝对产物路径",
        )

        reference, digest = write_audit_artifact(
            artifact_dir,
            {
                "skill": "cognitive-expansion",
                "prompt_name": "Absolute artifact directory regression",
            },
            [],
            "ACTIVATED:cognitive-expansion",
            0,
            "",
        )
        require(
            reference == str(external_artifact),
            "仓库外小样写入后必须在收据中保留绝对路径",
        )
        require(
            len(digest) == 64,
            "小样产物必须生成 SHA-256 摘要",
        )
        payload = json.loads(external_artifact.read_text(encoding="utf-8"))
        require(
            payload["observed_final"] == "ACTIVATED:cognitive-expansion",
            "路径回退不得改变模型小样结果",
        )

        skill = "code-minimalism"
        skill_path = f"skills/{skill}/SKILL.md"
        case = {
            "skill": skill,
            "prompt": "给出一个精炼的代码审查结论。",
            "criteria": ["结论具体且不编造事实"],
        }
        producer = {
            "messages": ["这是经过证据约束的精炼结论。" * 12],
            "commands": [
                {
                    "command": f"sed -n '1,80p' {skill_path}",
                    "exit_code": 0,
                    "status": "completed",
                }
            ],
            "usage": {},
            "exit_code": 0,
            "timed_out": False,
            "elapsed_seconds": 0.01,
            "failure_diagnostic": "",
            "raw_sha256": "1" * 64,
        }
        reviewer = {
            "messages": [
                json.dumps(
                    {
                        "status": "pass",
                        "criteria": [
                            {
                                "criterion": "结论具体且不编造事实",
                                "status": "pass",
                                "evidence": "输出保持证据边界。",
                            }
                        ],
                        "findings": [],
                        "boundary": "synthetic",
                    },
                    ensure_ascii=False,
                )
            ],
            "commands": [],
            "usage": {},
            "exit_code": 0,
            "timed_out": False,
            "elapsed_seconds": 0.01,
            "failure_diagnostic": "",
            "raw_sha256": "2" * 64,
        }
        original_run_codex = quality_runner.run_codex
        try:
            responses = iter((producer, reviewer))
            observed_prompts: list[str] = []

            def run_codex_stub(prompt: str, *_args: object, **_kwargs: object) -> dict:
                observed_prompts.append(prompt)
                return dict(next(responses))

            quality_runner.run_codex = run_codex_stub
            passed_result = quality_runner.run_case(
                case,
                artifact_dir / "quality-pass",
                10,
                None,
                "codex",
                False,
            )
            require(
                passed_result["status"] == "pass"
                and passed_result["skill_sha256"]
                == quality_runner.file_sha256(ROOT / skill_path),
                "successful output-quality results must bind the evaluated Skill hash",
            )
            require(
                len(observed_prompts) == 2
                and case["prompt"] in observed_prompts[1]
                and "用户提供前提" in observed_prompts[1],
                "独立审核必须看到同一任务原文并区分任务前提与独立核验事实",
            )

            failed_producer = dict(producer)
            failed_producer.update(
                {
                    "messages": [],
                    "commands": [],
                    "exit_code": 1,
                    "failure_diagnostic": "synthetic producer failure",
                }
            )
            quality_runner.run_codex = lambda *_args, **_kwargs: dict(failed_producer)
            failed_result = quality_runner.run_case(
                case,
                artifact_dir / "quality-fail",
                10,
                None,
                "codex",
                False,
            )
            require(
                failed_result["status"] == "fail"
                and failed_result["skill_sha256"]
                == quality_runner.file_sha256(ROOT / skill_path),
                "failed output-quality results must also bind the evaluated Skill hash",
            )
        finally:
            quality_runner.run_codex = original_run_codex

    print("Capability runner path regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
