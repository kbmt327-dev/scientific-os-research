#!/usr/bin/env python3
"""Assert that the built site contains the expected public routes and Mermaid payload."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    required = [
        "index.html",
        "research/gpu-scheduling/index.html",
        "research/simulation-worlds/index.html",
        "research/human-model/index.html",
        "research/badminton-biomechanics/index.html",
    ]
    missing = [name for name in required if not (public / name).exists()]
    if missing:
        print("Missing built routes: " + ", ".join(missing))
        return 1
    home = (public / "index.html").read_text(encoding="utf-8")
    if "mermaid" not in home.lower():
        print("Mermaid payload not found in built home page")
        return 1
    print(f"Built-site check passed: {len(required)} routes and Mermaid payload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

