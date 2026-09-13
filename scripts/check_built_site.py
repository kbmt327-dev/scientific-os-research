#!/usr/bin/env python3
"""Assert that the built site contains the bilingual interface and compatibility routes."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    slugs = [
        "gpu-scheduling",
        "gpu-scheduling-phase-diagram",
        "gpu-scheduling-starvation-mechanism",
        "gpu-scheduling-real-traces",
        "simulation-worlds",
        "human-model",
        "badminton-biomechanics",
    ]
    required = [
        "index.html",
        "llms.txt",
        "en/index.html",
        "ja/index.html",
        "en/research/index.html",
        "ja/research/index.html",
        "en/how-to-read/index.html",
        "ja/how-to-read/index.html",
        "en/contribute/index.html",
        "ja/contribute/index.html",
        *[f"en/research/{slug}/index.html" for slug in slugs],
        *[f"ja/research/{slug}/index.html" for slug in slugs],
    ]
    missing = [name for name in required if not (public / name).exists()]
    if missing:
        print("Missing built routes: " + ", ".join(missing))
        return 1
    for lang in ("en", "ja"):
        page = (public / lang / "research/gpu-scheduling/index.html").read_text(encoding="utf-8")
        if "mermaid" not in page.lower():
            print(f"Mermaid payload not found in built {lang} Research Note")
            return 1
        if f'<html lang="{lang}"' not in page:
            print(f"Incorrect or missing html lang on {lang} Research Note")
            return 1
        if 'rel="alternate"' not in page or "hreflang" not in page:
            print(f"Missing hreflang alternate on {lang} Research Note")
            return 1
    for slug in slugs:
        legacy = public / "research" / slug / "index.html"
        if not legacy.exists() or 'http-equiv="refresh"' not in legacy.read_text(encoding="utf-8"):
            print(f"Missing legacy redirect for /research/{slug}/")
            return 1
    llms = (public / "llms.txt").read_text(encoding="utf-8")
    if "The Markdown Research Notes are the canonical public representation" not in llms:
        print("Built llms.txt is missing its canonical-representation boundary")
        return 1
    print(f"Built-site check passed: {len(required)} canonical routes, {len(slugs)} redirects, bilingual Mermaid and hreflang")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
