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
)
from scripts.run_capability_output_quality import (  # noqa: E402
    artifact_ref as quality_artifact_ref,
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

    print("Capability runner path regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
