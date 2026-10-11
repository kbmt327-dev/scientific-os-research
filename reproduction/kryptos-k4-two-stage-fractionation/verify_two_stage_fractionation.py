#!/usr/bin/env python3
"""Bounded input and recorded-boundary checks; no candidate/null search is run."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")

spec = importlib.util.spec_from_file_location("k4_two_stage", ROOT / "k4_two_stage.py")
if spec is None or spec.loader is None:
    raise SystemExit("FAIL: cannot load existing input module")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
require(data["projection_only"] is True and data["registered_search_rerun"] is False, "projection boundary")
require(len(data["episodes"]) == 6, "six recorded episodes")
require(len(module.K4) == 97 and len(module.CRIB) == 24, "public ciphertext/crib dimensions")
by_id = {row["episode"]: row for row in data["episodes"]}
require(by_id["EP-0222"]["square_bank_size"] == 16, "EP-0222 fixed subset size")
require(by_id["EP-0222"]["full_2622_square_bank_closed"] is False, "EP-0222 full-bank boundary")
require(by_id["EP-0222"]["R3-3_specificity"].startswith("failed"), "EP-0222 R3-3 unrun status")
for row in data["episodes"]:
    require(row.get("registered_pass_count", 0) == 0, f"recorded pass count for {row['episode']}")
require(data["new_plaintext_characters"] == 0 and data["independent_replications"] == 0, "claim boundary")
print("PASS: six projections; public input dimensions and EP-0222 subset boundary checked")