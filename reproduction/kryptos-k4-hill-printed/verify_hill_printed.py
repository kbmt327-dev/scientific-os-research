#!/usr/bin/env python3
"""Bounded checks for printed-transformation data and recorded outcomes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
transcript = json.loads((ROOT / "data" / "hill1929-c3c4.json").read_text(encoding="utf-8"))

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")

require(data["projection_only"] is True and data["registered_search_rerun"] is False, "projection boundary")
require(len(data["episodes"]) == 4, "four recorded episodes")
require(transcript["C3"]["n"] == 3 and transcript["C4"]["n"] == 4, "C3/C4 dimensions")
require(len(transcript["C3"]["determinant_rows"]) == 3, "C3 determinant rows")
require(len(transcript["C4"]["identity_determinant_4Ij"]) == 4, "C4 identity rows")
require(len(transcript["matrices_numeric"]) == 2, "two printed transformation matrices")
require(all(row["registered_pass_count"] == 0 for row in data["episodes"]), "recorded pass counts")
require(data["new_plaintext_characters"] == 0 and data["independent_replications"] == 0, "claim boundary")
print("PASS: transcript dimensions and four recorded projections checked; no registered search rerun")