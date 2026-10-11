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
require(len(data["episodes"]) == 8, "eight recorded episodes")
require(len(module.K4) == 97 and len(module.CRIB) == 24, "public ciphertext/crib dimensions")
by_id = {row["episode"]: row for row in data["episodes"]}
require(len(by_id) == 8, "unique episode identifiers")
require(by_id["EP-0213"]["two_square_compatible_labels"] == 24, "EP-0213 compatible labels retained")
require(by_id["EP-0213"]["two_square_compatible_classes"] == 12, "EP-0213 equivalence classes retained")
require(by_id["EP-0229"]["still_compatible_classes"] == 3, "EP-0229 compatible classes retained")
require(all(row.get("registered_pass_count", 0) == 0 for row in data["episodes"]), "recorded decisionable pass counts")
require(data["new_plaintext_characters"] == 0 and data["independent_replications"] == 0, "claim boundary")
ep224 = by_id["EP-0224"]
require(ep224["source_episode_sha256"] == "f91c1f43e6ffaaab900d71fbc37a0040f1763513d46174f3afac47f3c3274099", "EP-0224 source digest")
require(ep224["unknown_count"] == 0, "EP-0224 K4 UNKNOWN count")
require(ep224["k4_scope"]["ph_columns"] == 4 and ep224["k4_scope"]["spf_columns"] == 6, "EP-0224 K4 column counts")
require(ep224["registered_nulls"]["ph_seed_count_per_column"] == 200, "EP-0224 PH null count")
require(ep224["registered_nulls"]["ph_main_h1_by_column"] == {"PH1-main": 0, "PH2-main": 1}, "EP-0224 PH-main h=1 counts")
require(ep224["registered_nulls"]["ph_sensitivity_null_cutoff"] == "h=0 only; h=1 not evaluated", "EP-0224 PH-sensitivity cutoff boundary")
require(ep224["registered_nulls"]["spf_seed_count_per_column"] == 2, "EP-0224 SPF null count")
conditional = ep224["registered_nulls"]["conditional_sp2_d0"]
require(len(conditional["p_open_periods"]) == 8 and conditional["accepted_samples_per_period"] == 20, "EP-0224 conditional-null scope")
require(conditional["sat_total"] == 0 and conditional["unknown_total"] == 0, "EP-0224 conditional-null outcome")
require(ep224["registered_empirical_p"] == {"ph_main_p0": 1.0, "ph_main_p1": 1.0, "ph_sensitivity_p0": 1.0, "spf_p0": 1.0}, "EP-0224 registered P-value scopes")
require(ep224["spf_control_detection"] == {"detected": 25, "total": 60, "interpretation": "retained control result; not a K4 detection-power claim"}, "EP-0224 control boundary")
require(ep224["capacity_e_approximation"]["sum_e0_approx_upper_ignoring_overlap"] == 0.005, "EP-0224 approximate capacity boundary")
require(ep224["capacity_e_approximation"]["ph_main_columns_combined"] == 2, "EP-0224 PH-main combined E scope")
require(ep224["capacity_e_approximation"]["ph_main_e0_two_columns_combined"] == 4.7e-5 and ep224["capacity_e_approximation"]["ph_main_e1_h_le_1_two_columns_combined"] == 0.028, "EP-0224 PH-main combined E values")
print("PASS: 8 projections; input dimensions and recorded result boundaries checked; no registered search or null rerun")
