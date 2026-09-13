#!/usr/bin/env python3
"""Install the validated llms.txt source at the built site's public root."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "quartz/static/llms.txt")
    target = Path(sys.argv[2] if len(sys.argv) > 2 else "public/llms.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"Installed {source} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
