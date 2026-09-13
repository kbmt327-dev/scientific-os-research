#!/usr/bin/env python3
"""Check local Markdown and Obsidian wikilinks used by the public content."""

from __future__ import annotations

import re
import sys
from pathlib import Path


WIKI = re.compile(r"!?\[\[([^\]]+)\]\]")
MARKDOWN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def candidates(content: Path, source: Path, target: str) -> list[Path]:
    target = target.split("#", 1)[0].split("|", 1)[0].strip()
    if not target:
        return []
    clean = Path(target)
    bases = [source.parent / clean, content / clean]
    found: list[Path] = []
    for base in bases:
        found.extend([base, base.with_suffix(".md"), base / "index.md"])
    if len(clean.parts) == 1:
        found.extend(content.rglob(clean.name + ".md"))
        found.extend(content.rglob(clean.name + "/index.md"))
    return found


def main() -> int:
    content = Path(sys.argv[1] if len(sys.argv) > 1 else "content").resolve()
    failures: list[str] = []
    files = list(content.rglob("*.md"))
    for source in files:
        text = source.read_text(encoding="utf-8-sig")
        targets = [m.group(1) for m in WIKI.finditer(text)]
        targets += [m.group(1).strip("<>") for m in MARKDOWN.finditer(text)]
        for target in targets:
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not any(path.exists() for path in candidates(content, source, target)):
                failures.append(f"{source.relative_to(content)} -> {target}")
    if failures:
        print("Broken internal links:")
        print("\n".join(failures))
        return 1
    print(f"Internal link check passed: {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

