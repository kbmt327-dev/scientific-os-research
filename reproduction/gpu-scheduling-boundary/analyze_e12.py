"""Grade PRED-011 against results/E12.json.

Z0 is a gate: if the E9 replay does not reproduce, nothing else is graded.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E12 = json.load(open(os.path.join(HERE, "results", "E12.json")))
E9 = json.load(open(os.path.join(HERE, "results", "E9.json")))
CFG, ROWS = E12["config"], E12["rows"]
RATIOS = CFG["ratios"]
E_LABELS = ["C10", "C15", "C28"]
P_LEVELS = CFG["p_levels"]
P_EXT = CFG["p_extension"]
SAFE_FB = 0.9
BELOW = "BELOW_GRID"
verdicts = {}
notes = {}


def mean_of(rows, key):
    vals = [r[key] for r in rows
            if r.get(key) is not None and r.get(key) == r.get(key)]
    return float(np.mean(vals)) if vals else float("nan")


def cell(arm, e_label, ratio, p, policy="srpt"):
    return [r for r in ROWS if r["arm"] == arm and r.get("e_label") == e_label
            and abs(r["ratio"] - ratio) < 1e-9 and abs(r["p"] - p) < 1e-12
            and r["policy"] == policy]


def fb(e_label, ratio, p, arm="A"):
    return mean_of(cell(arm, e_label, ratio, p), "fb_m")


def conc(e_label, ratio, p, arm="A"):
    return mean_of(cell(arm, e_label, ratio, p), "mean_running")


def jct(e_label, ratio, p, arm="A"):
    return mean_of(cell(arm, e_label, ratio, p), "jct_m")


def r_safe(e_label, p, arm="A"):
    ok = [r for r in RATIOS if fb(e_label, r, p, arm) >= SAFE_FB]
    return max(ok) if ok else BELOW


def steps(a, b):
    if a == BELOW or b == BELOW:
        idx = {BELOW: -1}
        ia = idx.get(a, RATIOS.index(a) if a != BELOW else -1)
        ib = idx.get(b, RATIOS.index(b) if b != BELOW else -1)
        return abs(ia - ib)
    return abs(RATIOS.index(a) - RATIOS.index(b))


# ----------------------------------------------------------------- Z0 gate
e9_key = {}
for r in E9["rows"]:
    e9_key[(r["s"], round(r["ratio"], 4), r["seed"])] = r
GATE_METRICS = ["mean_jct", "utilization", "rho_emp", "mean_running", "fb_m"]
gate_diff, gate_missing = 0.0, 0
for r in [x for x in ROWS if x["arm"] == "R"]:
    old = e9_key.get((r["s"], round(r["ratio"], 4), r["seed"]))
    if old is None:
        gate_missing += 1
        continue
    for k in GATE_METRICS:
        a, b = r.get(k), old.get(k)
        if a is None or b is None:
            gate_missing += 1
            continue
        gate_diff = max(gate_diff, abs(float(a) - float(b)))
verdicts["Z0"] = "PASS" if (gate_diff <= 1e-12 and gate_missing == 0) else "FAIL"
notes["Z0"] = f"max abs diff {gate_diff:.3e}, missing {gate_missing}, " \
              f"{len([x for x in ROWS if x['arm'] == 'R'])} replay rows"
print(f"Z0 replay gate: {verdicts['Z0']}  ({notes['Z0']})")
if verdicts["Z0"] != "PASS":
    raise SystemExit("Z0 failed: not grading Z1..Z9 (pre-committed).")

# --------------------------------------------------------------- main tables
print("\nN=256, rho=0.85, greedy SRPT. r_safe = largest ratio with "
      "flow balance >= 0.9\n")
header = "  ".join(f"{r:>6}" for r in RATIOS)
for e_label in E_LABELS:
    e_target = CFG["e_targets"][e_label]
    print(f"{e_label}  E[need]={e_target:.3f}  "
          f"Little's-law concurrency={0.85 * 256 / e_target:.2f}")
    print(f"{'p':>7}{'conc':>8}{'w_max':>8}{'r_safe':>9}   {header}")
    ps = P_LEVELS + ([P_EXT[e_label]] if e_label in P_EXT else [])
    for p in ps:
        arm = "A" if p in P_LEVELS else "B"
        cs = [conc(e_label, r, p, arm) for r in RATIOS]
        w = p * 256 / e_target
        rs = r_safe(e_label, p, arm)
        line = "  ".join(f"{fb(e_label, r, p, arm):>6.3f}" for r in RATIOS)
        print(f"{p:>7}{np.nanmean(cs):>8.2f}{w:>8.3f}{str(rs):>9}   {line}")
    print()

# ------------------------------------------------------------------- Z1
z1_fail = []
for e_label in E_LABELS:
    for r in RATIOS:
        cs = [conc(e_label, r, p) for p in P_LEVELS]
        rr = (max(cs) - min(cs)) / float(np.mean(cs))
        if rr > 0.10:
            z1_fail.append(f"{e_label} r={r} rel_range={rr:.3f}")
    allc = [conc(e_label, r, p) for r in RATIOS for p in P_LEVELS]
    little = 0.85 * 256 / CFG["e_targets"][e_label]
    off = abs(float(np.mean(allc)) - little) / little
    if off > 0.08:
        z1_fail.append(f"{e_label} mean conc off Little by {off:.3f}")
verdicts["Z1"] = "PASS" if not z1_fail else "FAIL"
notes["Z1"] = "; ".join(z1_fail) if z1_fail else \
    "all (E,r) groups within 10%, all E within 8% of Little's law"

# ------------------------------------------------------------------- Z2
z2_fail = []
RS = {}
for e_label in E_LABELS:
    base = r_safe(e_label, P_LEVELS[0])
    RS[e_label] = {p: r_safe(e_label, p) for p in P_LEVELS}
    for p in P_LEVELS[1:]:
        s = steps(RS[e_label][p], base)
        if s != 0:
            z2_fail.append(f"{e_label} p={p}: {RS[e_label][p]} vs {base} "
                           f"({s} grid steps)")
verdicts["Z2"] = "PASS" if not z2_fail else "FAIL"
notes["Z2"] = "; ".join(z2_fail) if z2_fail else \
    "r_safe identical across p at all three concurrency levels: " + \
    ", ".join(f"{e}={RS[e][P_LEVELS[0]]}" for e in E_LABELS)

# ------------------------------------------------------------------ Z2b
z2b_fail, z2b_max = [], 0.0
for e_label in E_LABELS:
    for r in RATIOS:
        fs = [fb(e_label, r, p) for p in P_LEVELS]
        rng = max(fs) - min(fs)
        z2b_max = max(z2b_max, rng)
        if rng > 0.15:
            z2b_fail.append(f"{e_label} r={r} range={rng:.3f}")
verdicts["Z2b"] = "PASS" if not z2b_fail else "FAIL"
notes["Z2b"] = (f"max flow-balance range across p = {z2b_max:.3f}"
                + ("" if not z2b_fail else "; " + "; ".join(z2b_fail)))

# ------------------------------------------------------------------- Z3
EXPECTED = {"C10": 0.875, "C15": 0.8125, "C28": 0.625}
z3_fail = []
for e_label in E_LABELS:
    got = r_safe(e_label, 0.002)
    if steps(got, EXPECTED[e_label]) != 0:
        z3_fail.append(f"{e_label}: got {got}, E9 says {EXPECTED[e_label]}")
verdicts["Z3"] = "PASS" if not z3_fail else "FAIL"
notes["Z3"] = "; ".join(z3_fail) if z3_fail else \
    "p=0.002 layer reproduces E9's r_safe under a different background family"

# ------------------------------------------------------------------- Z4
z4_fail = []
for e_label in E_LABELS:
    ps = P_LEVELS + ([P_EXT[e_label]] if e_label in P_EXT else [])
    for p in ps:
        arm = "A" if p in P_LEVELS else "B"
        fs = [fb(e_label, r, p, arm) for r in RATIOS]
        for i in range(len(fs) - 1):
            if fs[i + 1] - fs[i] > 0.03:
                z4_fail.append(f"{e_label} p={p} r={RATIOS[i]}->{RATIOS[i+1]}: "
                               f"{fs[i]:.3f}->{fs[i+1]:.3f}")
verdicts["Z4"] = "PASS" if not z4_fail else "FAIL"
notes["Z4"] = "; ".join(z4_fail) if z4_fail else \
    "flow balance non-increasing in r in every (E,p) row"

# ------------------------------------------------------------------- Z5
z5_fail = []
for p in P_LEVELS:
    seq = [r_safe(e, p) for e in E_LABELS]
    vals = [-1 if x == BELOW else RATIOS.index(x) for x in seq]
    if not (vals[0] >= vals[1] >= vals[2]):
        z5_fail.append(f"p={p}: {seq}")
verdicts["Z5"] = "PASS" if not z5_fail else "FAIL"
notes["Z5"] = "; ".join(z5_fail) if z5_fail else \
    "r_safe non-increasing in concurrency at every p"

# ------------------------------------------------------------------- Z6
z6_fail = []
for e_label, p in P_EXT.items():
    a, b = r_safe(e_label, p, "B"), r_safe(e_label, 0.002)
    if steps(a, b) != 0:
        z6_fail.append(f"{e_label}: p={p} gives {a}, p=0.002 gives {b}")
verdicts["Z6"] = "PASS" if not z6_fail else "FAIL"
notes["Z6"] = "; ".join(z6_fail) if z6_fail else \
    "r_safe unchanged at p=0.05 (25x) in both feasible concurrency levels"

# ------------------------------------------------------------------- Z7
ref = []
for e_label in E_LABELS:
    for r in CFG["ref_ratios"]:
        v = mean_of(cell("C", e_label, r, CFG["ref_p"], "easy_backfill"),
                    "fb_m")
        ref.append((e_label, r, v))
z7_fail = [f"{e} r={r}: {v:.3f}" for e, r, v in ref if not v >= SAFE_FB]
verdicts["Z7"] = "PASS" if not z7_fail else "FAIL"
notes["Z7"] = "; ".join(z7_fail) if z7_fail else \
    f"EASY backfill flow balance {min(v for _, _, v in ref):.3f}.." \
    f"{max(v for _, _, v in ref):.3f} in all 9 reference cells"

# ------------------------------------------------------------------- Z8
z8_fail = []
print("Z8: per-r, all A+B cells sorted by observed concurrency")
for r in RATIOS:
    pts = []
    for e_label in E_LABELS:
        for p in P_LEVELS:
            pts.append((conc(e_label, r, p), fb(e_label, r, p), e_label, p))
        if e_label in P_EXT:
            p = P_EXT[e_label]
            pts.append((conc(e_label, r, p, "B"), fb(e_label, r, p, "B"),
                        e_label, p))
    pts.sort()
    print(f"  r={r}: " + " ".join(f"{c:.1f}/{f:.2f}" for c, f, _, _ in pts))
    for i in range(len(pts) - 1):
        if pts[i + 1][1] - pts[i][1] > 0.05:
            z8_fail.append(
                f"r={r}: conc {pts[i][0]:.1f}(p={pts[i][3]}) fb={pts[i][1]:.3f}"
                f" -> conc {pts[i+1][0]:.1f}(p={pts[i+1][3]}) "
                f"fb={pts[i+1][1]:.3f}")
verdicts["Z8"] = "PASS" if not z8_fail else "FAIL"
notes["Z8"] = "; ".join(z8_fail) if z8_fail else \
    "given r, flow balance is ordered by observed concurrency alone"

# ------------------------------------------------------------------- Z9
z9_groups, z9_up = [], []
for e_label in E_LABELS:
    for r in RATIOS:
        if all(fb(e_label, r, p) >= SAFE_FB for p in P_LEVELS):
            lo, hi = jct(e_label, r, 0.002), jct(e_label, r, 0.02)
            z9_groups.append((e_label, r, lo, hi))
            if hi > lo:
                z9_up.append((e_label, r))
frac = len(z9_up) / len(z9_groups) if z9_groups else float("nan")
verdicts["Z9"] = "PASS" if z9_groups and frac >= 2 / 3 else "FAIL"
notes["Z9"] = (f"{len(z9_up)}/{len(z9_groups)} healthy groups have "
               f"jct_m rising with p ({frac:.2f})")

# ------------------------------------------------------------------ output
print("\n" + "=" * 72)
passed = sum(1 for v in verdicts.values() if v == "PASS")
for k in ["Z0", "Z1", "Z2", "Z2b", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9"]:
    print(f"{k:>4} {verdicts[k]:<5} {notes[k]}")
print(f"\nPRED-011: {passed}/{len(verdicts)}")

grading = {
    "pred_id": "PRED-011",
    "episode": "EP-0010",
    "score": f"{passed}/{len(verdicts)}",
    "verdicts": verdicts,
    "notes": notes,
    "r_safe_table": {
        e: {str(p): r_safe(e, p) for p in P_LEVELS
            + ([P_EXT[e]] if e in P_EXT else [])}
        for e in E_LABELS},
    "flow_balance": {
        e: {str(p): {str(r): fb(e, r, p, "A" if p in P_LEVELS else "B")
                     for r in RATIOS}
            for p in P_LEVELS + ([P_EXT[e]] if e in P_EXT else [])}
        for e in E_LABELS},
    "concurrency": {
        e: {str(p): {str(r): conc(e, r, p, "A" if p in P_LEVELS else "B")
                     for r in RATIOS}
            for p in P_LEVELS + ([P_EXT[e]] if e in P_EXT else [])}
        for e in E_LABELS},
    "jct_m": {
        e: {str(p): {str(r): jct(e, r, p, "A" if p in P_LEVELS else "B")
                     for r in RATIOS}
            for p in P_LEVELS + ([P_EXT[e]] if e in P_EXT else [])}
        for e in E_LABELS},
}
out = os.path.join(HERE, "results", "E12_grading.json")
json.dump(grading, open(out, "w", encoding="utf-8"), indent=1)
print(f"wrote {out}")
