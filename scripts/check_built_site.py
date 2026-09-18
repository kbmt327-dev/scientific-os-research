#!/usr/bin/env python3
"""Assert that the built site contains the bilingual interface and compatibility routes."""

from __future__ import annotations

import sys
import re
from pathlib import Path
from urllib.parse import unquote


HREF = re.compile(r'<a\s[^>]*href="([^"]+)"', flags=re.IGNORECASE)


BASE_PATH = "/scientific-os-research/"


def broken_local_links(public: Path) -> list[tuple[str, str]]:
    """Follow every local <a href> in the built HTML and report the dead ones.

    Links written inside raw HTML blocks are rewritten by Quartz, so a link that
    looks right in Markdown can still resolve outside the site. Only the built
    output shows that.
    """
    broken: list[tuple[str, str]] = []
    for page in sorted(public.rglob("*.html")):
        html = page.read_text(encoding="utf-8", errors="ignore")
        image_sources = re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
        for href in HREF.findall(html) + image_sources:
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            path = unquote(href.split("#")[0].split("?")[0])
            if not path:
                continue
            if path.rstrip("/") == BASE_PATH.rstrip("/"):
                path = BASE_PATH
            if path.startswith("/"):
                # Components emit deploy-absolute links; resolve them at the site root.
                if not path.startswith(BASE_PATH):
                    broken.append((str(page.relative_to(public)), href))
                    continue
                target = (public / path[len(BASE_PATH):]).resolve()
            else:
                target = (page.parent / path).resolve()
            if path.endswith("/"):
                target = target / "index.html"
            elif target.is_dir():
                target = target / "index.html"
            elif not target.suffix:
                target = target.with_suffix(".html")
            if not target.exists():
                broken.append((str(page.relative_to(public)), href))
    return broken


def main() -> int:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    slugs = [
        "gpu-scheduling",
        "gpu-scheduling-phase-diagram",
        "gpu-scheduling-starvation-mechanism",
        "gpu-scheduling-real-traces",
        "gpu-scheduling-u31-calibration",
        "gpu-scheduling-known-controls",
        "gpu-scheduling-drift-uncertainty",
        "gpu-scheduling-mmc-transfer",
        "gpu-scheduling-information-tiers",
        "gpu-scheduling-critical-loss",
        "gpu-scheduling-two-class-control",
        "gpu-scheduling-past-only-learning",
        "simulation-worlds",
        "human-model",
        "human-model-dataset-portfolio",
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
        "en/about/open-research-lab.html",
        "ja/about/open-research-lab.html",
        "en/research-notes/index.html",
        "ja/research-notes/index.html",
        "en/programs/gpu-scheduling/index.html",
        "ja/programs/gpu-scheduling/index.html",
        "en/programs/queueing-system-identification/index.html",
        "ja/programs/queueing-system-identification/index.html",
        "en/programs/human-model-interface/index.html",
        "ja/programs/human-model-interface/index.html",
        "en/programs/badminton-biomechanics/index.html",
        "ja/programs/badminton-biomechanics/index.html",
        *[f"en/research/{slug}/index.html" for slug in slugs],
        *[f"ja/research/{slug}/index.html" for slug in slugs],
    ]
    missing = [name for name in required if not (public / name).exists()]
    if missing:
        print("Missing built routes: " + ", ".join(missing))
        return 1
    root = (public / "index.html").read_text(encoding="utf-8")
    if "orl-language" not in root or "location.replace" not in root:
        print("Root page is missing automatic language selection")
        return 1
    for lang in ("en", "ja"):
        home = (public / lang / "index.html").read_text(encoding="utf-8")
        for marker in ("lab-sidebar-toggle", "lab-primary-nav", "program-index", "GitHub"):
            if marker not in home:
                print(f"Missing {marker} on {lang} home")
                return 1
        if "Powered by" not in home or "© 2026 kbmt327" not in home:
            print(f"Missing site-owner footer on {lang} home")
            return 1
        about_href = f'/scientific-os-research/{lang}/about/open-research-lab'
        if f'href="{about_href}"' not in home or f'href="{about_href}/"' in home:
            print(f"About navigation has a non-deployable URL on {lang} home")
            return 1
        research = (public / lang / "research" / "index.html").read_text(encoding="utf-8")
        for page_name, page in (("home", home), ("research", research)):
            if "items under this folder" in page:
                print(f"Automatic folder listing leaked into curated {lang} {page_name}")
                return 1
    for lang, other_lang in (("en", "ja"), ("ja", "en")):
        for path in (f"{lang}/index.html", f"{lang}/research/gpu-scheduling/index.html"):
            page = (public / path).read_text(encoding="utf-8")
            if f'<html lang="{lang}"' not in page:
                print(f"Incorrect or missing html lang on {path}")
                return 1
            for hreflang in (lang, other_lang):
                if f'hreflang="{hreflang}"' not in page:
                    print(f"Missing {hreflang} hreflang view on {path}")
                    return 1
        note_page = (public / lang / "research/gpu-scheduling/index.html").read_text(
            encoding="utf-8"
        )
        if "mermaid" not in note_page.lower():
            print(f"Mermaid payload not found in built {lang} Research Note")
            return 1
    for slug in slugs:
        legacy = public / "research" / slug / "index.html"
        if not legacy.exists() or 'http-equiv="refresh"' not in legacy.read_text(encoding="utf-8"):
            print(f"Missing legacy redirect for /research/{slug}/")
            return 1
    broken = broken_local_links(public)
    if broken:
        print("Broken links in the built site:")
        for where, href in broken[:40]:
            print(f"- {where} -> {href}")
        return 1
    llms = (public / "llms.txt").read_text(encoding="utf-8")
    if "Program current-state pages are canonical for current claims" not in llms:
        print("Built llms.txt is missing its current-claim authority boundary")
        return 1
    print(f"Built-site check passed: {len(required)} canonical routes, {len(slugs)} redirects, language routing, lab chrome, bilingual Mermaid and hreflang")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
