#!/usr/bin/env python3
"""Regression tests for Guyue's local security scanners."""

from __future__ import annotations

import subprocess
import tempfile
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import run_security_scan  # noqa: E402
from security_patterns import find_secret_matches  # noqa: E402


ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    suite = (ROOT / "test_suite.sh").read_text(encoding="utf-8")
    require(
        "ruff check --no-cache scripts src" in suite,
        "the release gate must not create a Ruff cache inside source archives",
    )

    with tempfile.TemporaryDirectory(prefix="guyue-zero-leakage-test-") as temp_dir:
        root = Path(temp_dir)
        cache_dir = root / ".ruff_cache"
        cache_dir.mkdir()
        (cache_dir / "CACHEDIR.TAG").write_text("generated cache\n", encoding="utf-8")
        scanner = subprocess.run(
            [sys.executable, str(ROOT / "security_scanner.py")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        require(scanner.returncode != 0, ".ruff_cache must fail Zero-Leakage")
        require(
            "Generated cache present" in scanner.stdout,
            "Zero-Leakage must explain the Ruff cache failure",
        )

    with tempfile.TemporaryDirectory(prefix="guyue-security-test-") as temp_dir:
        root = Path(temp_dir)
        for index in range(204):
            (root / f"safe-{index:03d}.md").write_text(
                "ordinary documentation\n", encoding="utf-8"
            )
        (root / "safe-204.md").write_text(
            "run rm" + " -rf only in a disposable fixture\n", encoding="utf-8"
        )

        result = run_security_scan.run_scan(root)
        require(
            result["total_files"] == 205, "scanner must enumerate every eligible file"
        )
        require(
            result["scanned_files"] == 205,
            "scanner must not silently truncate after 200 files",
        )
        require(
            result["status"] == "Red", "a red flag in file 205 must block the target"
        )

        empty = root / "empty"
        empty.mkdir()
        empty_result = run_security_scan.run_scan(empty)
        require(
            empty_result["status"] == "Yellow", "an empty target must not receive Green"
        )
        require(
            empty_result["total_files"] == 0,
            "empty target file count must remain explicit",
        )

        remote_result = run_security_scan.run_scan(
            "https://github.com/example/remote-skill"
        )
        require(
            remote_result["status"] == "Yellow",
            "a URL target must require manual review rather than crashing",
        )
        require(
            remote_result["scanned_files"] == 0
            and remote_result["total_files"] == 0,
            "URL targets must keep explicit zero scan counts",
        )

    fake_github_token = "gh" + "p_" + "a" * 24
    fake_aws_key = "AKIA" + "A" * 16
    fake_private_key = "-----BEGIN " + "PRIVATE KEY-----"
    require(
        "GitHub token" in find_secret_matches(fake_github_token),
        "GitHub tokens must be detected",
    )
    require(
        "AWS access key" in find_secret_matches(fake_aws_key),
        "AWS keys must be detected",
    )
    require(
        "private key" in find_secret_matches(fake_private_key),
        "private-key headers must be detected",
    )
    marked_fixture = fake_github_token + " # security-scan: allow-example"
    require(
        "GitHub token" in find_secret_matches(marked_fixture),
        "an allow marker must not bypass production scans",
    )
    require(
        not find_secret_matches(marked_fixture, allow_example=True),
        "a test-only caller may explicitly allow a synthetic fixture",
    )

    print("Security scanner regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
