"""Grade PRED-012 against results/E13.json plus the archived E7/E9/E12.

D0 is a gate: if the 30000-job replay does not reproduce E12, nothing else is
graded.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    return json.load(open(os.path.join(HERE, "results", name),
                          encoding="utf-8"))


E13, E12, E9, E7 = load("E13.json"), load("E12.json"), load("E9.json"), \
    load("E7.json")
CFG, ROWS = E13["config"], E13["rows"]
RATIOS = CFG["ratios"]
E_LABELS = ["C10", "C15", "C28"]
P_LEVELS = CFG["p_levels"]
HORIZONS = CFG["horizons"]
BELOW = "BELOW_GRID"
THRESHOLDS = [0.8, 0.9, 0.95]
verdicts, notes = {}, {}


def mean_of(rows, key):
    v = [r[key] for r in rows
         if r.get(key) is not None and r.get(key) == r.get(key)]
    return float(np.mean(v)) if v else float("nan")


def sem_of(rows, key):
    v = [r[key] for r in rows
         if r.get(key) is not None and r.get(key) == r.get(key)]
    return float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else \
        float("nan")


def cell(e_label, ratio, p, n_jobs, policy="srpt", arm="H"):
    return [r for r in ROWS if r["arm"] == arm and r["e_label"] == e_label
            and abs(r["ratio"] - ratio) < 1e-9 and abs(r["p"] - p) < 1e-12
            and r["n_jobs"] == n_jobs and r["policy"] == policy]


def r_star(fbs, thr, ratios=None):
    """Interpolated crossing of `thr`, walking the ratio grid upward."""
    ratios = ratios or RATIOS
    if fbs[-1] >= thr:
        return ratios[-1]
    if fbs[0] < thr:
        return BELOW
    for i in range(len(ratios) - 1):
        a, b = fbs[i], fbs[i + 1]
        if a >= thr > b:
            return ratios[i] + (a - thr) / (a - b) * (ratios[i + 1] - ratios[i])
    return BELOW


def r_safe(fbs, thr, ratios=None):
    ratios = ratios or RATIOS
    ok = [r for r, f in zip(ratios, fbs) if f >= thr]
    return max(ok) if ok else BELOW


def fb_row(e_label, p, n_jobs):
    return [mean_of(cell(e_label, r, p, n_jobs), "fb_m") for r in RATIOS]


def rs(e_label, p, n_jobs, thr=0.9):
    return r_star(fb_row(e_label, p, n_jobs), thr)


# ------------------------------------------------------------------ D0 gate
e12_key = {}
for r in E12["rows"]:
    if r["arm"] in ("A", "B"):
        e12_key[(r["e_label"], round(r["ratio"], 6), round(r["p"], 6),
                 r["seed"])] = r
GATE = ["mean_jct", "utilization", "rho_emp", "mean_running", "fb_m"]
gate_diff, gate_missing, gate_n = 0.0, 0, 0
for r in [x for x in ROWS if x["arm"] == "H" and x["n_jobs"] == 30_000]:
    gate_n += 1
    old = e12_key.get((r["e_label"], round(r["ratio"], 6), round(r["p"], 6),
                       r["seed"]))
    if old is None:
        gate_missing += 1
        continue
    for k in GATE:
        a, b = r.get(k), old.get(k)
        if a is None or b is None:
            gate_missing += 1
            continue
        gate_diff = max(gate_diff, abs(float(a) - float(b)))
verdicts["D0"] = "PASS" if gate_diff <= 1e-12 and gate_missing == 0 else "FAIL"
notes["D0"] = f"max abs diff {gate_diff:.3e}, missing {gate_missing}, " \
              f"{gate_n} replay rows"
print(f"D0 replay gate: {verdicts['D0']}  ({notes['D0']})")
if verdicts["D0"] != "PASS":
    raise SystemExit("D0 failed: not grading D1..D10 (pre-committed).")

# ------------------------------------------------------------- main tables
print("\nN=256, rho=0.85, greedy SRPT. r* = interpolated crossing of the line\n")
for e_label in E_LABELS:
    print(f"{e_label}  (Little concurrency "
          f"{0.85 * 256 / CFG['e_targets'][e_label]:.2f})")
    print(f"{'p':>7}{'n_jobs':>9}{'conc':>7}{'r*@.8':>8}{'r*@.9':>8}"
          f"{'r*@.95':>8}{'r_safe@.9':>11}   flow balance by ratio")
    for p in P_LEVELS:
        for n in HORIZONS:
            fbs = fb_row(e_label, p, n)
            conc = float(np.mean([mean_of(cell(e_label, r, p, n),
                                          "mean_running") for r in RATIOS]))
            line = " ".join(f"{f:>6.3f}" for f in fbs)
            def fmt(x):
                return f"{x:>8.4f}" if x != BELOW else f"{'<0.5':>8}"
            print(f"{p:>7}{n:>9}{conc:>7.2f}"
                  + "".join(fmt(r_star(fbs, t)) for t in THRESHOLDS)
                  + f"{str(r_safe(fbs, 0.9)):>11}   {line}")
    print()

# ------------------------------------------------------------------- D1
d1, d1_detail = [], []
for e_label in ["C15", "C28"]:
    for p in P_LEVELS:
        a, b = rs(e_label, p, 30_000), rs(e_label, p, 120_000)
        if a == BELOW or b == BELOW:
            d1.append(f"{e_label} p={p}: off-grid ({a} -> {b})")
            continue
        d = b - a
        d1_detail.append(f"{e_label} p={p}: {a:.4f} -> {b:.4f} ({d:+.4f})")
        if d < 0.02:
            d1.append(f"{e_label} p={p}: delta={d:+.4f} < +0.02")
verdicts["D1"] = "PASS" if not d1 else "FAIL"
notes["D1"] = "; ".join(d1_detail) + ("" if not d1 else "  || FAILING: "
                                      + "; ".join(d1))

# ------------------------------------------------------------------- D2
d2_ok, d2_detail = 0, []
combos = [(e, p) for e in E_LABELS for p in P_LEVELS]
for e_label, p in combos:
    a, b, c = (rs(e_label, p, n) for n in HORIZONS)
    if BELOW in (a, b, c):
        d2_detail.append(f"{e_label} p={p}: off-grid")
        continue
    first, second = abs(b - a), abs(c - b)
    d2_detail.append(f"{e_label} p={p}: |30->60|={first:.4f} "
                     f"|60->120|={second:.4f}")
    if second < first:
        d2_ok += 1
verdicts["D2"] = "PASS" if d2_ok >= (2 / 3) * len(combos) else "FAIL"
notes["D2"] = f"{d2_ok}/{len(combos)} converging. " + "; ".join(d2_detail)

# ------------------------------------------------------------------- D3
d3 = []
for n in HORIZONS:
    for p in P_LEVELS:
        seq = [rs(e, p, n) for e in E_LABELS]
        if BELOW in seq or not (seq[0] > seq[1] > seq[2]):
            d3.append(f"n={n} p={p}: " + " ".join(
                f"{x:.4f}" if x != BELOW else "<0.5" for x in seq))
verdicts["D3"] = "PASS" if not d3 else "FAIL"
notes["D3"] = "; ".join(d3) if d3 else \
    "r*(C10) > r*(C15) > r*(C28) in all 6 horizon x p combinations"

# ------------------------------------------------------------------- D4
d4, d4_below = [], []
for thr in THRESHOLDS:
    for n in [30_000, 120_000]:
        seq = [r_star(fb_row(e, 0.002, n), thr) for e in E_LABELS]
        if BELOW in seq:
            d4_below.append(f"thr={thr} n={n}: {seq}")
            continue
        if not (seq[0] > seq[1] > seq[2]):
            d4.append(f"thr={thr} n={n}: " + " ".join(f"{x:.4f}" for x in seq))
verdicts["D4"] = "PASS" if not d4 else "FAIL"
notes["D4"] = ("; ".join(d4) if d4 else
               "ordering holds at every threshold and both horizons") + \
    ("" if not d4_below else "  || off-grid rows excluded: "
     + "; ".join(d4_below))

# ------------------------------------------------------------------- D5
d5, d5_detail = [], []
for e_label in ["C15", "C28"]:
    lo, hi = rs(e_label, 0.002, 120_000), rs(e_label, 0.02, 120_000)
    if BELOW in (lo, hi):
        d5.append(f"{e_label}: off-grid")
        continue
    d5_detail.append(f"{e_label}@120k: p=.002 {lo:.4f}, p=.02 {hi:.4f} "
                     f"(diff {hi - lo:+.4f})")
    if abs(hi - lo) < 0.02:
        d5.append(f"{e_label}: |diff|={abs(hi - lo):.4f} < 0.02")
s30 = rs("C15", 0.02, 30_000) - rs("C15", 0.002, 30_000)
s120 = rs("C15", 0.02, 120_000) - rs("C15", 0.002, 120_000)
if not (s30 < 0 and s120 < 0):
    d5.append(f"C15 sign flipped: 30k {s30:+.4f}, 120k {s120:+.4f}")
verdicts["D5"] = "PASS" if not d5 else "FAIL"
notes["D5"] = "; ".join(d5_detail) + f"; C15 sign 30k {s30:+.4f} / 120k " \
    f"{s120:+.4f}" + ("" if not d5 else "  || FAILING: " + "; ".join(d5))

# ------------------------------------------------------------------- D6
d6, d6_detail = [], []
for e_label in E_LABELS:
    for n in HORIZONS:
        fbs = fb_row(e_label, 0.002, n)
        a, b = r_star(fbs, 0.8), r_star(fbs, 0.95)
        if BELOW in (a, b):
            d6_detail.append(f"{e_label} n={n}: off-grid")
            continue
        d6_detail.append(f"{e_label} n={n}: {a - b:.4f}")
        if a - b < 0.05:
            d6.append(f"{e_label} n={n}: spread {a - b:.4f} < 0.05")
verdicts["D6"] = "PASS" if not d6 else "FAIL"
notes["D6"] = "r*(0.8)-r*(0.95): " + "; ".join(d6_detail) + \
    ("" if not d6 else "  || FAILING: " + "; ".join(d6))

# ---------------------------------------------------- D7/D8 (E9 revisited)
E9_RATIOS = E9["config"]["ratios"]
e9g = {}
for x in E9["rows"]:
    e9g.setdefault((x["s"], round(x["ratio"], 4)), []).append(x)
E9_S = [16, 12, 8, 4, 2, 1]
e9_tab = []
for s in E9_S:
    fbs = [mean_of(e9g[(s, round(r, 4))], "fb_m") for r in E9_RATIOS]
    conc = float(np.mean([mean_of(e9g[(s, round(r, 4))], "mean_running")
                          for r in E9_RATIOS]))
    e9_tab.append((s, conc, r_safe(fbs, 0.9, E9_RATIOS),
                   r_star(fbs, 0.9, E9_RATIOS)))
print("E9 re-measured (EP-0007 concurrency curve), threshold 0.9")
print(f"{'s':>4}{'conc':>9}{'r_safe':>10}{'r*':>10}{'gap':>9}")
gaps = []
for s, conc, safe, star in e9_tab:
    gap = (star - safe) if BELOW not in (safe, star) else float("nan")
    gaps.append(gap)
    print(f"{s:>4}{conc:>9.1f}{str(safe):>10}"
          + (f"{star:>10.4f}" if star != BELOW else f"{'<0.5':>10}")
          + f"{gap:>9.4f}")
n_up = sum(1 for g in gaps if g == g and g > 0)
mean_gap = float(np.nanmean(gaps))
verdicts["D7"] = "PASS" if (n_up >= 5 and mean_gap >= 0.03) else "FAIL"
notes["D7"] = f"r* > r_safe in {n_up}/6 rows, mean gap {mean_gap:.4f}"

stars = [t[3] for t in e9_tab]
d8 = [] if BELOW in stars else [
    f"s={E9_S[i]}->{E9_S[i+1]}: {stars[i]:.4f}->{stars[i+1]:.4f}"
    for i in range(len(stars) - 1) if stars[i + 1] - stars[i] > 0.01]
verdicts["D8"] = "PASS" if (BELOW not in stars and not d8) else "FAIL"
notes["D8"] = "; ".join(d8) if d8 else \
    "r* non-increasing across E9's concurrency sweep: " + \
    " ".join(f"{x:.3f}" for x in stars if x != BELOW)

# ------------------------------------------------------- D9 (E7 revisited)
E7_RATIOS = E7["config"]["ratios"]
E7_NS = E7["config"].get("n_values") or E7["config"].get("ns") or \
    sorted({x["n_servers"] for x in E7["rows"]})
e7g = {}
for x in E7["rows"]:
    if x.get("policy", "srpt") != "srpt":
        continue
    e7g.setdefault((x["n_servers"], round(x["ratio"], 4)), []).append(x)
print("\nE7 re-measured (EP-0005 pool-size sweep), threshold 0.9")
print(f"{'N':>6}{'r_safe':>10}{'r*':>10}")
e7_stars = []
for n in sorted(E7_NS):
    fbs = [mean_of(e7g.get((n, round(r, 4)), []), "fb_m") for r in E7_RATIOS]
    if any(f != f for f in fbs):
        print(f"{n:>6}{'incomplete':>10}")
        continue
    safe, star = r_safe(fbs, 0.9, E7_RATIOS), r_star(fbs, 0.9, E7_RATIOS)
    e7_stars.append(star)
    print(f"{n:>6}{str(safe):>10}"
          + (f"{star:>10.4f}" if star != BELOW else f"{'<0.5':>10}"))
d9 = [] if BELOW in e7_stars else [
    f"{i}: {e7_stars[i]:.4f}->{e7_stars[i+1]:.4f}"
    for i in range(len(e7_stars) - 1) if e7_stars[i + 1] - e7_stars[i] > 0.01]
verdicts["D9"] = "PASS" if (e7_stars and BELOW not in e7_stars and not d9) \
    else "FAIL"
notes["D9"] = "; ".join(d9) if d9 else \
    "r* non-increasing across E7's pool sizes: " + \
    " ".join(f"{x:.3f}" for x in e7_stars if x != BELOW)

# ------------------------------------------------------------------ D10
easy = []
for e_label in E_LABELS:
    for r in CFG["easy_ratios"]:
        easy.append((e_label, r, mean_of(
            cell(e_label, r, CFG["easy_p"], CFG["easy_horizon"],
                 "easy_backfill", "E"), "fb_m")))
d10 = [f"{e} r={r}: {v:.3f}" for e, r, v in easy if not v >= 0.9]
verdicts["D10"] = "PASS" if not d10 else "FAIL"
notes["D10"] = "; ".join(d10) if d10 else \
    f"EASY backfill at 120k jobs: {min(v for _, _, v in easy):.3f}.." \
    f"{max(v for _, _, v in easy):.3f}"

# --------------------------------------------------------- seed noise note
print("\nper-seed spread of r* (threshold 0.9), to weigh the verdicts")
for e_label in E_LABELS:
    for p in P_LEVELS:
        for n in HORIZONS:
            per = []
            for sd in CFG["seeds"]:
                fbs = [next((x["fb_m"] for x in cell(e_label, r, p, n)
                             if x["seed"] == sd), float("nan"))
                       for r in RATIOS]
                v = r_star(fbs, 0.9)
                if v != BELOW:
                    per.append(v)
            if len(per) > 1:
                a = np.array(per)
                print(f"  {e_label} p={p:<6} n={n:>7}: mean={a.mean():.4f} "
                      f"sd={a.std(ddof=1):.4f} se={a.std(ddof=1)/np.sqrt(len(a)):.4f}")

print("\n" + "=" * 72)
order = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]
passed = sum(1 for k in order if verdicts[k] == "PASS")
for k in order:
    print(f"{k:>4} {verdicts[k]:<5} {notes[k]}")
print(f"\nPRED-012: {passed}/{len(order)}")

json.dump({
    "pred_id": "PRED-012", "episode": "EP-0011",
    "score": f"{passed}/{len(order)}",
    "verdicts": verdicts, "notes": notes,
    "r_star": {e: {str(p): {str(n): rs(e, p, n) for n in HORIZONS}
                   for p in P_LEVELS} for e in E_LABELS},
    "r_star_by_threshold": {
        e: {str(t): {str(n): r_star(fb_row(e, 0.002, n), t) for n in HORIZONS}
            for t in THRESHOLDS} for e in E_LABELS},
    "e9_remeasured": [{"s": s, "conc": c, "r_safe": sa, "r_star": st}
                      for s, c, sa, st in e9_tab],
    "e7_remeasured": e7_stars,
}, open(os.path.join(HERE, "results", "E13_grading.json"), "w",
        encoding="utf-8"), indent=1)
print("wrote results/E13_grading.json")
