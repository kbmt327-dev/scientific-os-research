#!/usr/bin/env python3
"""Fail closed on likely private paths, local identity, or credential material."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".js", ".json", ".jsx", ".md", ".mjs",
    ".py", ".scss", ".toml", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
SKIP_PARTS = {".git", ".quartz", "node_modules", "public", "__pycache__"}
PATTERNS = {
    "windows_local_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Documents and Settings)[\\/]"),
    "unix_home_path": re.compile(r"(?i)(?:^|[\s'\"`])/(?:Users|home)/[^/\s]+/"),
    "local_username": re.compile(r"(?i)(?:[\\/]|\b)kbmt3(?:[\\/]|\b)(?!27-dev)"),
    "github_token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{16,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name == Path(__file__).name:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 5_000_000:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[str] = []
    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(f"{path.relative_to(root)}:{number}: {label}")
    if findings:
        print("Privacy scan failed:")
        print("\n".join(findings))
        return 1
    print(f"Privacy scan passed: {sum(1 for _ in iter_text_files(root))} text files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

