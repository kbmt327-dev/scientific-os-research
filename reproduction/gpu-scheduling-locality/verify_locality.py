"""Verify the EP-0029 (E18 / PRED-017) package.

1. PRED-017.json matches its sealed digest (LF byte stream).
2. The sealed analyze_e18.py, rerun on the published E18.json, reproduces the
   published grades: P0 PASS, P1-P5 FAIL (1/6).
3. gang_heavy is a structural null: every run spans zero excess nodes, and the
   eight pi x placement variants of each run give the same mean JCT.
4. Eight runs are re-simulated at the 40k horizon and match E18.json.

This does not rerun all 768 runs (about 20 minutes on 15 workers; use
`python run_e18.py` after moving results/E18.json aside).
"""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_e18  # noqa: E402
import run_e18  # noqa: E402

SEALED = "e6da2a070aef8329b3ef8c459741e27cc098854d44d26d84e986a2c5fce359b8"
RERUN = [
    ("gang_heavy", "fcfs", 0.6, 0.3, "first_fit", 1801, 40_000),
    ("gang_heavy", "sf_srpt", 0.7, 0.6, "first_fit", 1802, 40_000),
    ("trace_like", "fcfs", 0.6, 0.1, "first_fit", 1801, 40_000),
    ("trace_like", "easy_backfill", 0.6, 0.3, "compact", 1802, 40_000),
    ("trace_like", "srpt", 0.6, 0.0, "compact", 1803, 40_000),
    ("trace_like", "srpt", 0.6, 0.1, "first_fit", 1801, 40_000),
    ("trace_like", "sf_srpt", 0.7, 0.1, "compact", 1803, 40_000),
    ("trace_like", "easy_backfill", 0.7, 0.1, "first_fit", 1801, 40_000),
]


def main():
    path = os.path.join(HERE, "predictions", "PRED-017.json")
    text = open(path, encoding="utf-8").read()
    got = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert got == SEALED, (got, SEALED)
    want = open(os.path.join(HERE, "predictions", "PRED-017.sha256")).read().split()[0]
    assert want == SEALED, want

    cfg, runs = analyze_e18.load()
    cells = analyze_e18.cells(cfg, runs)
    grades = analyze_e18.grade(cfg, runs, cells)
    passed = {k: v["passed"] for k, v in grades.items()}
    assert passed == {"P0": True, "P1": False, "P2": False, "P3": False,
                      "P4": False, "P5": False}, passed
    pub = json.load(open(os.path.join(HERE, "results", "E18_grading.json")))
    assert {k: v["passed"] for k, v in pub["grades"].items()} == passed
    labels = {}
    for v in cells.values():
        labels[v["label"]] = labels.get(v["label"], 0) + 1
    assert labels == {"STABLE": 100, "DIVERGING": 21, "UNKNOWN": 7}, labels

    rows = json.load(open(os.path.join(HERE, "results", "E18.json")))["rows"]
    gh = [r for r in rows if r["mix"] == "gang_heavy"]
    assert len(gh) == 384 and max(r["excess_nodes_per_placement"] for r in gh) == 0.0
    groups = {}
    for r in gh:
        groups.setdefault((r["policy"], r["rho"], r["seed"], r["horizon"]), set()).add(r["mean_jct"])
    assert len(groups) == 48 and all(len(v) == 1 for v in groups.values())

    index = {(r["mix"], r["policy"], r["rho"], r["penalty"], r["placement"],
              r["seed"], r["horizon"]): r for r in rows}
    for task in RERUN:
        new, old = run_e18.one(task), index[task]
        for k in ("mean_jct", "excess_nodes_per_placement"):
            assert math.isclose(new[k], old[k], rel_tol=1e-9), (task, k, new[k], old[k])

    print("gpu-locality: PRED-017 digest, 1/6 grading (P3 FAIL), 100/21/7 labels, "
          f"gang_heavy null (48/48 groups identical), {len(RERUN)} reruns match")


if __name__ == "__main__":
    main()
