#!/usr/bin/env python3
"""Check local Markdown and Obsidian wikilinks used by the public content."""

from __future__ import annotations

import re
import sys
from pathlib import Path


WIKI = re.compile(r"!?\[\[([^\]]+)\]\]")
MARKDOWN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HTML_HREF = re.compile(r"\bhref=[\"']([^\"']+)[\"']", flags=re.IGNORECASE)
SITE_PREFIX = "/scientific-os-research/"

# Quartz resolves an href that starts with "/" against the content root, not the
# deployed base path. A link written with the base path baked in (for example
# "/scientific-os-research/ja/") is therefore emitted as a broken relative URL,
# so the base path is rejected here and content-root links are checked instead.


def candidates(content: Path, source: Path, target: str) -> list[Path]:
    # Markdown tables require the wikilink alias separator to be escaped.
    # Normalize it before parsing so behavior is identical on Windows and POSIX.
    target = target.replace(r"\|", "|")
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
        targets += [m.group(1) for m in HTML_HREF.finditer(text)]
        for target in targets:
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith(SITE_PREFIX):
                failures.append(
                    f"{source.relative_to(content)} -> {target} "
                    "(drop the base path; write it as a content-root link)"
                )
                continue
            clean_target = target.split("#", 1)[0].split("|", 1)[0].strip()
            if clean_target.endswith("/"):
                relative = clean_target.lstrip("/").rstrip("/")
                direct_candidates = [source.parent / relative, content / relative]
                direct_page = any(path.with_suffix(".md").exists() for path in direct_candidates)
                folder_index = any((path / "index.md").exists() for path in direct_candidates)
                if direct_page and not folder_index:
                    failures.append(
                        f"{source.relative_to(content)} -> {target} "
                        "(leaf Markdown pages must not use a trailing slash)"
                    )
                    continue
            target = target.lstrip("/")
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
