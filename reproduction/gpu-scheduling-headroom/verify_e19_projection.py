#!/usr/bin/env python3
"""Re-grade the compact E19 projection using only Python's standard library."""
from __future__ import annotations

import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "ep0030_summary.json"
ORDER = ("srpt", "sf_srpt", "easy_backfill", "fcfs")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"FAIL: {message}")


def finite(value) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def grade_order(rows: list[dict], minimum: int) -> dict:
    details = []
    for row in rows:
        selected = [(p, row["degradation"].get(p)) for p in ORDER if row["degradation"].get(p) is not None]
        if len(selected) < 3:
            details.append({"mix": row["mix"], "scored": False, "passed": None})
            continue
        passed = all(a[1] < b[1] for i, a in enumerate(selected) for b in selected[i + 1:])
        details.append({"mix": row["mix"], "scored": True, "passed": passed})
    scored = [r for r in details if r["scored"]]
    return {
        "passed": len(scored) >= minimum and all(r["passed"] for r in scored),
        "scored": len(scored),
        "passed_rows": sum(r["passed"] is True for r in scored),
        "rows": details,
    }


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    require(data["schema"] == "gpu-scheduling-ep0030-projection-v1", "unexpected schema")
    require(data["research_id"] == "GPU-SCHED-EP-0030", "wrong research id")
    for key in ("prediction_sha256", "results_sha256", "grading_sha256"):
        value = data["source_artifacts"][key]
        require(isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value), f"invalid {key}")
    d = data["design"]
    require(d["main_runs"] + d["load_control_runs"] == d["total_runs"] == 912, "run totals do not reconcile")
    require(d["grade_cells"] == sum(d["cell_labels"].values()) == 152, "cell totals do not reconcile")
    require(d["cell_labels"] == {"STABLE": 144, "UNKNOWN": 8}, "cell labels differ")
    require(d["total_gpus"] == 64 and d["gpus_per_node"] == 8, "model dimensions differ")
    require(data["rank_order"] == list(ORDER), "rank order differs")
    pred = data["predictions"]
    require(set(pred) == {"P0", "P1", "P2", "P3", "P4", "P5"}, "prediction set differs")
    require(finite(pred["P0"]["observed_max_abs_diff"]) and pred["P0"]["observed_max_abs_diff"] == 0.0, "P0 control is not exact")

    p1rows = pred["P1"]["rows"]
    require(len(p1rows) == 8, "P1 row count differs")
    p1 = all(finite(r["first_fit"]) and finite(r["compact"]) and r["first_fit"] >= 0.1 and r["compact"] < r["first_fit"] for r in p1rows)
    p2 = grade_order(pred["P2"]["rows"], pred["P2"]["minimum_scorable_rows"])
    p3 = grade_order(pred["P3"]["rows"], pred["P3"]["minimum_scorable_rows"])
    p4 = grade_order(pred["P4"]["rows"], pred["P4"]["minimum_scorable_rows"])
    require(len(pred["P2"]["rows"]) == 8 and len(pred["P3"]["rows"]) == 4 and len(pred["P4"]["rows"]) == 4, "rank row count differs")

    p5check = []
    shares = []
    require(len(pred["P5"]["rows"]) == 8, "P5 row count differs")
    for row in pred["P5"]["rows"]:
        vals = [row[k] for k in ("fcfs_degradation", "srpt_degradation", "fcfs_R", "srpt_R")]
        if not all(finite(v) for v in vals):
            continue
        raw = row["fcfs_degradation"] - row["srpt_degradation"]
        residual = row["fcfs_R"] - row["srpt_R"]
        require(raw > 0, "P5 raw gap must be positive")
        p5check.append(residual <= 0.5 * raw)
        shares.append(1.0 - residual / raw)
    p5 = len(p5check) >= pred["P5"]["minimum_computable_rows"] and all(p5check)
    require(len(shares) == 4, "P5 computable count differs")

    outcomes = {"P0": True, "P1": p1, "P2": p2["passed"], "P3": p3["passed"], "P4": p4["passed"], "P5": p5}
    passed = sum(outcomes.values())
    require(passed == 3, "sealed prediction total differs")
    p2mix = {m: {
        "scored": sum(r["mix"] == m and r["scored"] for r in p2["rows"]),
        "passed": sum(r["mix"] == m and r["passed"] is True for r in p2["rows"]),
    } for m in ("trace_like", "gang_odd")}
    reversals = sum(
        r["degradation"].get("srpt") is not None
        and r["degradation"].get("sf_srpt") is not None
        and r["degradation"]["srpt"] >= r["degradation"]["sf_srpt"]
        for r in pred["P2"]["rows"] if r["mix"] == "gang_odd"
    )
    require(p2mix == {"trace_like": {"scored": 3, "passed": 3}, "gang_odd": {"scored": 4, "passed": 0}}, "P2 mix split differs")
    require(reversals == 4, "P2 reversal count differs")

    print("PASS: bounded E19 projection arithmetic")
    print(f"Runs: {d['total_runs']} ({d['main_runs']} main + {d['load_control_runs']} load-control)")
    print(f"Cells: {d['grade_cells']} (STABLE {d['cell_labels']['STABLE']}, UNKNOWN {d['cell_labels']['UNKNOWN']})")
    print(f"Sealed predictions: {passed}/6")
    print(f"P2: FAIL; scorable {p2['scored']}/8; trace_like 3/3; gang_odd 0/4, reversals {reversals}/4")
    print(f"P3: {'PASS' if p3['passed'] else 'FAIL'}; {p3['passed_rows']}/{p3['scored']} scorable rows")
    print(f"P4: {'PASS' if p4['passed'] else 'FAIL'}; {p4['passed_rows']}/{p4['scored']} scorable rows")
    print(f"P5: {'PASS' if p5 else 'FAIL'}; {len(p5check)}/8 computable; explained share {min(shares):.1%}-{max(shares):.1%}")


if __name__ == "__main__":
    main()
