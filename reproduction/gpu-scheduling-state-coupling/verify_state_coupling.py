"""Verify the EP-0031-EP-0034 package (E20-E23 / PRED-019-PRED-022).

1. The four sealed prediction files match their sealing digests.
2. The sealed analysers, rerun on the published results, reproduce the
   published grades:
     E20  P0 PASS, P1-P5 unscorable (14 of 27 cells UNKNOWN)
     E21  5/6, decision P2 PASS (share of a in T at (0.6, 0.2) = 0.56)
     E22  R1 PASS, R2 PASS (pooled 12-seed lower bound > 0), R3 FAIL
     E23  P0, D, S1-S4 PASS (d_CO / a = 0.77 at (0.55, 0.2)); 4 of 36 cells UNKNOWN
3. Two tasks are re-simulated at the 160k horizon and match the published
   rows: one E21 FCFS task (the BASE/F/RP/CS/CM/U ladder behind a, b, c) and
   one E23 FCFS task (C-058 mode: CO/CQ/CT arms and the placement-state
   summaries). About two minutes on one core.

This does not rerun the 2,808 simulations of E20-E23 (use run_e20.py to
run_e23.py after moving the matching results file aside).
"""
import hashlib
import json
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_e20  # noqa: E402
import analyze_e21  # noqa: E402
import analyze_e22  # noqa: E402
import analyze_e23  # noqa: E402
import run_e20  # noqa: E402

# Digest of the LF byte stream as committed. PRED-022 was hashed in the private
# record from its CRLF working copy; that digest is checked too.
SEALED = {
    "PRED-019.json": "294870b90dc6f47b9103cbb6e145cb0b9a59cffdd160e0e216d2f958d0bbe98d",
    "PRED-020.json": "c21ae6da67e37814ddc6bebefc1c2a27c506c746fe1f733e6eed35f33693d4c1",
    "PRED-021.json": "ed3f40aabc8907de8b3a1a07415ef5f5c65f91a8718ef55f448ea47609c94de6",
    "PRED-022.json": "ca8da3c9cc905ed4eaa397bef7e218ffa7c612d658ecebd185a3dc760a1194ef",
}
PRED_022_CRLF = "9f53e9f12d2c337f7414bd81d626c657fac68c3cf2be636181e61a36488551ad"

RERUN = [
    ("E21.json", ("fcfs", 0.55, 0.2, 2101, 160_000)),
    ("E23.json", ("fcfs", 0.6, 0.1, 2301, 160_000, {"c058": True})),
]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def passed(g, keys):
    return {k: g[k]["passed"] for k in keys}


def published(name):
    return json.load(open(os.path.join(HERE, "results", name)))


def labels(c):
    return dict(Counter(v["label"] for v in c.values()))


def check_digests():
    for name, want in SEALED.items():
        text = open(os.path.join(HERE, "predictions", name), encoding="utf-8").read()
        assert sha(text) == want, (name, sha(text))
    text = open(os.path.join(HERE, "predictions", "PRED-022.json"), encoding="utf-8").read()
    assert sha(text.replace("\n", "\r\n")) == PRED_022_CRLF


def check_grades():
    p = ("P0", "P1", "P2", "P3", "P4", "P5")
    cfg, runs = analyze_e20.load()
    c = analyze_e20.cells(cfg, runs)
    g = analyze_e20.grade(cfg, runs, c)
    want = {"P0": True, "P1": False, "P2": False, "P3": False, "P4": False, "P5": False}
    assert passed(g, p) == want == passed(published("E20_grading.json")["grades"], p)
    assert labels(c) == {"STABLE": 13, "UNKNOWN": 14}, labels(c)

    cfg, runs = analyze_e21.load()
    c = analyze_e21.cells(cfg, runs)
    g21 = analyze_e21.grade(cfg, runs, c)
    want = {"P0": True, "P1": True, "P2": True, "P3": False, "P4": True, "P5": True}
    assert passed(g21, p) == want == passed(published("E21_grading.json")["grades"], p)
    assert labels(c) == {"STABLE": 27}, labels(c)
    row = g21["rows"]["0.6|0.2"]
    share21 = row["a"]["mean"] / row["T"]["mean"]
    assert round(share21, 2) == 0.56, share21

    cfg, runs = analyze_e22.load("E22.json")
    c = analyze_e21.cells(cfg, runs)
    g22 = analyze_e21.grade(cfg, runs, c)
    assert passed(g22, p) == want, passed(g22, p)
    assert labels(c) == {"STABLE": 27}, labels(c)
    m22 = analyze_e22.margins(g22["rows"]["0.6|0.2"])
    m21 = analyze_e22.margins(g21["rows"]["0.6|0.2"])
    r2, r3 = analyze_e22.lower(m21 + m22), analyze_e22.lower(m22)
    rep = published("E22_grading.json")["replication"]
    assert g22["P2"]["passed"] and rep["R1"]["passed"]
    assert r2["lower95"] > 0 and rep["R2"]["passed"]
    assert r3["lower95"] <= 0 and not rep["R3"]["passed"]
    assert math.isclose(r2["lower95"], rep["R2"]["lower95"], rel_tol=1e-9)
    assert sum(x < 0 for x in m22) == 3
    row = g22["rows"]["0.6|0.2"]
    share22 = row["a"]["mean"] / row["T"]["mean"]

    cfg, runs = analyze_e22.load("E23.json")
    c = analyze_e21.cells(cfg, runs)
    g23 = analyze_e23.grade(cfg, runs, c)
    k23 = ("P0", "D", "S1", "S2", "S3", "S4")
    want = {k: True for k in k23}
    assert passed(g23, k23) == want == passed(published("E23_grading.json")["grades"], k23)
    assert labels(c) == {"STABLE": 32, "UNKNOWN": 4}, labels(c)
    assert g23["D"]["scored"] == 1
    row = g23["rows"]["0.55|0.2"]
    return share21, share22, row["share_CO"], row["share_CQ"], row["share_CT"], r2["lower95"]


def check_reruns():
    n = 0
    for name, task in RERUN:
        rows = published(name)["rows"]
        index = {(r["policy"], r["rho"], r["penalty"], r["arm"], r["seed"], r["horizon"]): r
                 for r in rows}
        new = run_e20.one(task)
        assert new, task
        n += len(new)
        for r in new:
            old = index[(r["policy"], r["rho"], r["penalty"], r["arm"], r["seed"], r["horizon"])]
            for k in ("mean_jct", "excess_nodes_per_placement"):
                assert math.isclose(r[k], old[k], rel_tol=1e-9), (task, r["arm"], k, r[k], old[k])
            if "placement_state" in old:
                got = json.loads(json.dumps(r["placement_state"], default=lambda o: o.item()))
                assert got == old["placement_state"], (task, r["arm"])
    return n


def main():
    check_digests()
    s21, s22, s_co, s_cq, s_ct, low = check_grades()
    n = check_reruns()
    print(f"gpu-state-coupling: 4 sealed digests; E20 1/6 unscorable; E21 5/6 (a/T {s21:.2f}); "
          f"E22 R1 R2 PASS R3 FAIL (a/T {s22:.2f}, pooled lower {low:.4f}); "
          f"E23 6/6 (CO {s_co:.2f}, CQ {s_cq:.2f}, CT {s_ct:.2f}); {n} rerun arms match")


if __name__ == "__main__":
    main()
