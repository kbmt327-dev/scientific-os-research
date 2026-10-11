#!/usr/bin/env python3
"""Bounded input and result-projection checks; does not rerun registered searches."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")

spec = importlib.util.spec_from_file_location("k4_printed", ROOT / "k4_printed.py")
if spec is None or spec.loader is None:
    raise SystemExit("FAIL: cannot load existing input module")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
require(data["projection_only"] is True and data["registered_search_rerun"] is False, "projection boundary")
require(len(data["episodes"]) == 5, "five recorded episodes")
require(len(module.K4) == 97 and len(module.CRIB) == 24, "public ciphertext/crib dimensions")
require(len(module.GAINES_FIG173) == 30, "transcribed Gaines table entries")
by_id = {row["episode"]: row for row in data["episodes"]}
require(by_id["EP-0234"]["scope"] == "separate free-square diagnostic", "EP-0234 diagnostic remains separate")
require(by_id["EP-0234"]["two_square_auxiliary"].startswith("not decisionable"), "EP-0234 two-square boundary")
for row in data["episodes"]:
    require(row.get("registered_pass_count", 0) == 0, f"recorded pass count for {row['episode']}")
require(data["new_plaintext_characters"] == 0 and data["independent_replications"] == 0, "claim boundary")
print("PASS: five projections; public input dimensions and EP-0234 diagnostic boundary checked")