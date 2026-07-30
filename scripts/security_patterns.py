#!/usr/bin/env python3
"""Shared secret and privacy patterns for Guyue security scanners."""

from __future__ import annotations

import re


ALLOW_MARKER = "security-scan: allow-example"

SECRET_PATTERNS = [
    (re.compile(r"sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}"), "provider API key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{12,}"), "bearer token"),
    (
        re.compile(
            r"(?i)(?:api[_ -]?key|access[_ -]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/-]{12,}"
        ),
        "credential assignment",
    ),
    (re.compile(r"/(?:Users|home)/[^/\s]+/"), "personal absolute path"),
    (re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"), "Windows personal path"),
]

PROJECT_FINGERPRINT_PATTERNS = [
    (
        re.compile("Nexus" + "Flow", re.IGNORECASE),
        "private governance project marker",
    ),
    (
        re.compile("permission" + "Snapshot"),
        "private permission-state identifier",
    ),
    (
        re.compile(r"\b" + "E" + r"AC\b"),
        "redacted project marker",
    ),
    (
        re.compile("eac" + r"-demo-hardening"),
        "redacted project skill id",
    ),
    (
        re.compile("B2B" + r"\s+Site\s+Auditor"),
        "redacted project product name",
    ),
]


def find_secret_matches(line: str, *, allow_example: bool = False) -> list[str]:
    """Return unique secret categories found in a line."""
    if allow_example and ALLOW_MARKER in line:
        return []
    return [label for pattern, label in SECRET_PATTERNS if pattern.search(line)]


def find_project_fingerprint_matches(line: str) -> list[str]:
    """Return project/client fingerprints that must not ship in public payloads."""
    return [
        label
        for pattern, label in PROJECT_FINGERPRINT_PATTERNS
        if pattern.search(line)
    ]


def redact_sensitive_text(text: str) -> str:
    """Redact common credentials and personal home roots from extracted text."""
    redacted = re.sub(
        r"(?s)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "[REDACTED:private key]",
        text,
    )
    replacements = [
        (
            re.compile(r"sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}"),
            "[REDACTED:provider API key]",
        ),
        (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "[REDACTED:GitHub token]"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED:AWS access key]"),
        (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "[REDACTED:Google API key]"),
        (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{12,}"), "Bearer [REDACTED]"),
        (
            re.compile(
                r"(?i)((?:api[_ -]?key|access[_ -]?token|secret|password)\s*[:=]\s*['\"]?)[A-Za-z0-9._~+/-]{12,}"
            ),
            r"\1[REDACTED]",
        ),
        (re.compile(r"/(Users|home)/[^/\s]+/"), r"/\1/<redacted>/"),
        (re.compile(r"([A-Za-z]:\\Users\\)[^\\\s]+\\"), r"\1<redacted>\\"),
    ]
    for pattern, replacement in replacements:
        redacted = pattern.sub(replacement, redacted)
    return redacted
