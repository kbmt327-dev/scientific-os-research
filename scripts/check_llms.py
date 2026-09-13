#!/usr/bin/env python3
"""Validate llms.txt as a scope-preserving index over canonical Markdown pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from publish_episode import frontmatter


SITE = "https://kbmt327-dev.github.io/scientific-os-research"


def main() -> int:
    llms_path = Path(sys.argv[1] if len(sys.argv) > 1 else "quartz/static/llms.txt")
    content = Path(sys.argv[2] if len(sys.argv) > 2 else "content")
    text = llms_path.read_text(encoding="utf-8-sig")
    errors: list[str] = []

    if "The Markdown Research Notes are the canonical public representation" not in text:
        errors.append("llms.txt must say that Markdown Research Notes are canonical")
    if f"{SITE}/research/" in text:
        errors.append("llms.txt contains a legacy unscoped English research URL")

    pairs: dict[str, set[str]] = {}
    for lang in ("en", "ja"):
        for note in sorted((content / lang / "research").glob("*/index.md")):
            meta, _ = frontmatter(note.read_text(encoding="utf-8-sig"))
            research_id = str(meta["research_id"])
            slug = note.parent.name
            url = f"{SITE}/{lang}/research/{slug}/"
            pairs.setdefault(research_id, set()).add(lang)
            if research_id not in text:
                errors.append(f"missing research_id from llms.txt: {research_id}")
            if url not in text:
                errors.append(f"missing Research Note URL from llms.txt: {url}")

    for research_id, langs in sorted(pairs.items()):
        if langs != {"en", "ja"}:
            errors.append(f"{research_id}: llms index source lacks a language counterpart")

    local_urls = set(re.findall(rf"{re.escape(SITE)}/([^\s)]+)", text))
    allowed_roots = {"", "en/", "ja/", "en/how-to-read/", "ja/how-to-read/", "en/contribute/", "ja/contribute/"}
    for suffix in sorted(local_urls):
        suffix = suffix.rstrip(".,")
        if suffix in allowed_roots or suffix.startswith(("en/research/", "ja/research/", "en/programs/", "ja/programs/")):
            continue
        errors.append(f"unrecognized site URL in llms.txt: {SITE}/{suffix}")

    if errors:
        print("llms.txt validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"llms.txt validation passed: {len(pairs)} bilingual research objects indexed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
