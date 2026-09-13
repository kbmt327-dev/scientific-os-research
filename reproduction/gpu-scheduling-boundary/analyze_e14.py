"""Grade PRED-013 against results/E14.json.

G0 is a gate: if the E13 replay does not reproduce, nothing else is graded.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    return json.load(open(os.path.join(HERE, "results", name),
                          encoding="utf-8"))


E14, E13 = load("E14.json"), load("E13.json")
CFG, ROWS = E14["config"], E14["rows"]
RATIOS = CFG["ratios"]
E_LABELS = ["C10", "C15", "C28"]
P_LEVELS = CFG["p_levels"]
H4 = CFG["horizons"]
H3 = [30_000, 60_000, 120_000]
SEEDS = CFG["seeds"]
BELOW, ABOVE = "BELOW_GRID", "ABOVE_GRID"
ALPHA_LINE = 0.5
verdicts, notes = {}, {}
CELLS = [(e, p) for e in E_LABELS for p in P_LEVELS]


def rows_of(e_label, ratio, p, n_jobs, policy="srpt", arm="A", seeds=None):
    out = [r for r in ROWS if r["arm"] == arm and r["e_label"] == e_label
           and abs(r["ratio"] - ratio) < 1e-9 and abs(r["p"] - p) < 1e-12
           and r["n_jobs"] == n_jobs and r["policy"] == policy]
    if seeds is not None:
        out = [r for r in out if r["seed"] in seeds]
    return out


def mean_of(rs, key):
    v = [r[key] for r in rs if r.get(key) is not None and r[key] == r[key]]
    return float(np.mean(v)) if v else float("nan")


def alpha(e_label, ratio, p, horizons, policy="srpt", arm="A", seeds=None):
    y, x = [], []
    for h in horizons:
        t = mean_of(rows_of(e_label, ratio, p, h, policy, arm, seeds), "jct_m")
        if t != t or t <= 0:
            return float("nan")
        y.append(np.log(t))
        x.append(np.log(h))
    return float(np.polyfit(x, y, 1)[0])


def cross(vals, line=ALPHA_LINE):
    """ratio where an increasing sequence crosses `line`, interpolated."""
    if any(v != v for v in vals):
        return float("nan")
    if vals[0] >= line:
        return BELOW
    if vals[-1] < line:
        return ABOVE
    for i in range(len(vals) - 1):
        a, b = vals[i], vals[i + 1]
        if a < line <= b:
            return RATIOS[i] + (line - a) / (b - a) * (RATIOS[i + 1] - RATIOS[i])
    return float("nan")


def r_alpha(e_label, p, horizons, seeds=None):
    return cross([alpha(e_label, r, p, horizons, seeds=seeds) for r in RATIOS])


def r_star_fb(e_label, p, n_jobs=240_000, thr=0.9):
    fbs = [mean_of(rows_of(e_label, r, p, n_jobs), "fb_m") for r in RATIOS]
    if fbs[-1] >= thr:
        return RATIOS[-1]
    if fbs[0] < thr:
        return BELOW
    for i in range(len(RATIOS) - 1):
        a, b = fbs[i], fbs[i + 1]
        if a >= thr > b:
            return RATIOS[i] + (a - thr) / (a - b) * (RATIOS[i + 1] - RATIOS[i])
    return BELOW


# ------------------------------------------------------------------ G0 gate
key = {}
for r in E13["rows"]:
    if r["arm"] == "H":
        key[(r["e_label"], round(r["ratio"], 6), round(r["p"], 6),
             r["n_jobs"], r["seed"])] = r
GATE = ["mean_jct", "utilization", "rho_emp", "mean_running", "fb_m", "jct_m"]
gate_diff, gate_missing, gate_n = 0.0, 0, 0
for r in ROWS:
    if r["arm"] != "A" or r["seed"] > 905 or r["n_jobs"] == 240_000:
        continue
    gate_n += 1
    old = key.get((r["e_label"], round(r["ratio"], 6), round(r["p"], 6),
                   r["n_jobs"], r["seed"]))
    if old is None:
        gate_missing += 1
        continue
    for k in GATE:
        a, b = r.get(k), old.get(k)
        if a is None or b is None:
            gate_missing += 1
            continue
        gate_diff = max(gate_diff, abs(float(a) - float(b)))
verdicts["G0"] = "PASS" if gate_diff <= 1e-12 and gate_missing == 0 else "FAIL"
notes["G0"] = f"max abs diff {gate_diff:.3e}, missing {gate_missing}, " \
              f"{gate_n} replay rows"
print(f"G0 replay gate: {verdicts['G0']}  ({notes['G0']})")
if verdicts["G0"] != "PASS":
    raise SystemExit("G0 failed: not grading G1..G10 (pre-committed).")

# ---------------------------------------------------------------- tables
print("\nalpha4 = dlog E[T largest class] / dlog horizon, 4 horizons, "
      "8 seeds.  0 = converged, 1 = linear divergence\n")
print(f"{'':>13}" + "".join(f"{r:>8}" for r in RATIOS)
      + f"{'r_alpha':>10}{'r*(fb)':>9}{'gap':>8}")
A4, A3 = {}, {}
for e_label, p in CELLS:
    A4[(e_label, p)] = [alpha(e_label, r, p, H4) for r in RATIOS]
    A3[(e_label, p)] = [alpha(e_label, r, p, H3) for r in RATIOS]
    ra, rf = cross(A4[(e_label, p)]), r_star_fb(e_label, p)
    gap = (rf - ra) if isinstance(ra, float) and isinstance(rf, float) \
        else float("nan")
    print(f"{e_label + ' p=' + str(p):>13}"
          + "".join(f"{v:>8.2f}" for v in A4[(e_label, p)])
          + (f"{ra:>10.4f}" if isinstance(ra, float) else f"{str(ra):>10}")
          + (f"{rf:>9.4f}" if isinstance(rf, float) else f"{str(rf):>9}")
          + f"{gap:>8.4f}")

# ------------------------------------------------------------------- G1
g1, g1_detail = [], []
for e_label, p in CELLS:
    a, b = cross(A3[(e_label, p)]), cross(A4[(e_label, p)])
    if not (isinstance(a, float) and isinstance(b, float)):
        g1.append(f"{e_label} p={p}: off-grid ({a} / {b})")
        continue
    g1_detail.append(f"{e_label} p={p}: 3h {a:.4f} -> 4h {b:.4f} ({b - a:+.4f})")
    if abs(b - a) > 0.03:
        g1.append(f"{e_label} p={p}: moved {b - a:+.4f}")
verdicts["G1"] = "PASS" if not g1 else "FAIL"
notes["G1"] = "; ".join(g1_detail) + ("" if not g1 else "  || FAILING: "
                                      + "; ".join(g1))

# ------------------------------------------------------------------- G2
g2 = []
for e_label, p in CELLS:
    a = A4[(e_label, p)]
    for i in range(len(a) - 1):
        if a[i] - a[i + 1] > 0.05:
            g2.append(f"{e_label} p={p} r={RATIOS[i]}->{RATIOS[i+1]}: "
                      f"{a[i]:.2f}->{a[i+1]:.2f}")
verdicts["G2"] = "PASS" if not g2 else "FAIL"
notes["G2"] = "; ".join(g2) if g2 else \
    "alpha non-decreasing in r in every (E,p) row"

# ------------------------------------------------------------------- G3
gaps = []
for e_label, p in CELLS:
    ra, rf = cross(A4[(e_label, p)]), r_star_fb(e_label, p)
    gaps.append(rf - ra if isinstance(ra, float) and isinstance(rf, float)
                else float("nan"))
n_big = sum(1 for g in gaps if g == g and g >= 0.04)
mean_gap = float(np.nanmean(gaps))
verdicts["G3"] = "PASS" if (n_big >= 5 and mean_gap >= 0.06) else "FAIL"
notes["G3"] = f"gap >= 0.04 in {n_big}/6 cells, mean gap {mean_gap:.4f}; " \
              + " ".join(f"{g:+.3f}" for g in gaps)

# ------------------------------------------------------------------- G4
g4 = []
for p in P_LEVELS:
    seq = [cross(A4[(e, p)]) for e in E_LABELS]
    if not all(isinstance(x, float) for x in seq) or \
            not (seq[0] > seq[1] > seq[2]):
        g4.append(f"p={p}: " + " ".join(
            f"{x:.4f}" if isinstance(x, float) else str(x) for x in seq))
verdicts["G4"] = "PASS" if not g4 else "FAIL"
notes["G4"] = "; ".join(g4) if g4 else \
    "r_alpha(C10) > r_alpha(C15) > r_alpha(C28) at both p: " + "; ".join(
        f"p={p}: " + " ".join(f"{cross(A4[(e, p)]):.3f}" for e in E_LABELS)
        for p in P_LEVELS)

# ------------------------------------------------------------- G5 / G6
g5 = [f"{e} p={p}: {A4[(e, p)][-1]:.3f}" for e, p in CELLS
      if not A4[(e, p)][-1] >= 0.85]
verdicts["G5"] = "PASS" if not g5 else "FAIL"
notes["G5"] = "; ".join(g5) if g5 else \
    "alpha at r=1.0: " + " ".join(f"{A4[(e, p)][-1]:.3f}" for e, p in CELLS)
g6 = [f"{e} p={p}: {A4[(e, p)][0]:.3f}" for e, p in CELLS
      if not A4[(e, p)][0] <= 0.25]
verdicts["G6"] = "PASS" if not g6 else "FAIL"
notes["G6"] = "; ".join(g6) if g6 else \
    "alpha at r=0.5: " + " ".join(f"{A4[(e, p)][0]:.3f}" for e, p in CELLS)

# ------------------------------------------------------------------- G7
rng = np.random.default_rng(20260914)
g7, g7_detail = [], []
for e_label, p in CELLS:
    draws = []
    for _ in range(2000):
        pick = list(rng.choice(SEEDS, size=len(SEEDS), replace=True))
        v = r_alpha(e_label, p, H4, seeds=pick)
        if isinstance(v, float) and v == v:
            draws.append(v)
    if len(draws) < 100:
        g7.append(f"{e_label} p={p}: only {len(draws)} usable resamples")
        continue
    lo, hi = np.percentile(draws, [5, 95])
    half = (hi - lo) / 2
    g7_detail.append(f"{e_label} p={p}: {np.mean(draws):.4f} "
                     f"[{lo:.4f},{hi:.4f}] half={half:.4f}")
    if half > 0.06:
        g7.append(f"{e_label} p={p}: half-width {half:.4f}")
verdicts["G7"] = "PASS" if not g7 else "FAIL"
notes["G7"] = "; ".join(g7_detail) + ("" if not g7 else "  || FAILING: "
                                      + "; ".join(g7))

# ------------------------------------------------------------------- G8
easy = []
for e_label in E_LABELS:
    for r in CFG["easy_ratios"]:
        easy.append((e_label, r, alpha(e_label, r, CFG["easy_p"], H4,
                                       "easy_backfill", "E")))
g8 = [f"{e} r={r}: {a:.3f}" for e, r, a in easy if not a <= 0.25]
verdicts["G8"] = "PASS" if not g8 else "FAIL"
notes["G8"] = "; ".join(g8) if g8 else \
    "EASY backfill alpha: " + " ".join(f"{a:.3f}" for _, _, a in easy)

# ------------------------------------------------------------------- G9
ratios_c = []
for e_label, p in CELLS:
    for r in RATIOS:
        for h in H4:
            rs_ = rows_of(e_label, r, p, h)
            fb, t = mean_of(rs_, "fb_m"), mean_of(rs_, "jct_m")
            win = mean_of(rs_, "window")
            if fb != fb or t != t or t <= 0 or fb >= 1.0:
                continue
            ratios_c.append((1 - fb) * win / t)
ratios_c = np.array(ratios_c)
med = float(np.median(ratios_c))
frac = float(np.mean((ratios_c >= 1.2) & (ratios_c <= 2.5)))
verdicts["G9"] = "PASS" if (1.4 <= med <= 2.1 and frac >= 0.8) else "FAIL"
notes["G9"] = f"median censoring ratio {med:.3f} over {len(ratios_c)} cells, " \
              f"{frac * 100:.1f}% inside [1.2,2.5]"

# ------------------------------------------------------------------ G10
g10 = []
for p in P_LEVELS:
    v = cross(A4[("C10", p)])
    if not (isinstance(v, float) and v > 0.59):
        g10.append(f"p={p}: r_alpha(C10)={v}")
verdicts["G10"] = "PASS" if not g10 else "FAIL"
notes["G10"] = "; ".join(g10) if g10 else \
    "Philly ratio 0.59 stays inside the stable region: r_alpha(C10) = " + \
    " ".join(f"{cross(A4[('C10', p)]):.4f}" for p in P_LEVELS)

# ---------------------------------------------------------------- output
print("\n" + "=" * 72)
order = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]
passed = sum(1 for k in order if verdicts[k] == "PASS")
for k in order:
    print(f"{k:>4} {verdicts[k]:<5} {notes[k]}")
print(f"\nPRED-013: {passed}/{len(order)}")

json.dump({
    "pred_id": "PRED-013", "episode": "EP-0012",
    "score": f"{passed}/{len(order)}",
    "verdicts": verdicts, "notes": notes,
    "alpha4": {f"{e}|{p}": A4[(e, p)] for e, p in CELLS},
    "alpha3": {f"{e}|{p}": A3[(e, p)] for e, p in CELLS},
    "r_alpha4": {f"{e}|{p}": cross(A4[(e, p)]) for e, p in CELLS},
    "r_alpha3": {f"{e}|{p}": cross(A3[(e, p)]) for e, p in CELLS},
    "r_star_fb_240k": {f"{e}|{p}": r_star_fb(e, p) for e, p in CELLS},
    "easy_alpha": [{"e": e, "r": r, "alpha": a} for e, r, a in easy],
    "censoring_median": med,
}, open(os.path.join(HERE, "results", "E14_grading.json"), "w",
        encoding="utf-8"), indent=1)
print("wrote results/E14_grading.json")
