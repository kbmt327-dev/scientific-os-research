#!/usr/bin/env python3
"""Bounded checks for the public inputs and recorded EP projection; no search rerun."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_module():
    spec = importlib.util.spec_from_file_location("k4_fsmask", ROOT / "k4_fsmask.py")
    if spec is None or spec.loader is None:
        raise SystemExit("FAIL: cannot load existing input module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


data = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
module = load_module()
require(data["projection_only"] is True and data["registered_search_rerun"] is False, "projection boundary")
require(len(data["episodes"]) == 7, "seven recorded episodes")
require(len(module.K4) == 97 and len(module.CRIB) == 24, "public ciphertext/crib dimensions")
by_id = {row["episode"]: row for row in data["episodes"]}
require(len(by_id) == 7, "unique episode identifiers")
require(by_id["EP-0213"]["two_square_compatible_labels"] == 24, "EP-0213 compatible labels retained")
require(by_id["EP-0213"]["two_square_compatible_classes"] == 12, "EP-0213 equivalence classes retained")
require(by_id["EP-0229"]["still_compatible_classes"] == 3, "EP-0229 compatible classes retained")
require(all(row.get("registered_pass_count", 0) == 0 for row in data["episodes"]), "recorded decisionable pass counts")
require(data["new_plaintext_characters"] == 0 and data["independent_replications"] == 0, "claim boundary")
print("PASS: 7 projections; input dimensions and compatibility boundaries checked; no registered search rerun")