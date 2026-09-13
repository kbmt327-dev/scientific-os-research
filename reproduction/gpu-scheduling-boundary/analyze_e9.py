"""Grade PRED-008 against results/E9.json: what is r_safe at the concurrency
where the real cluster actually operates?"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E9 = json.load(open(os.path.join(HERE, "results", "E9.json")))
CFG, ROWS = E9["config"], E9["rows"]
S_VALUES, RATIOS = CFG["s_values"], CFG["ratios"]
SAFE_FB, STARVE_FB = 0.9, 0.5
PHILLY_CONC = 10.2       # Philly VC 11cb48, measured in EP-0006
PHILLY_RATIO = 0.59
E8_CONC = 28.5           # the lowest concurrency EP-0006 measured


def cell(s, r):
    rs = [x for x in ROWS if x["s"] == s and abs(x["ratio"] - r) < 0.004]
    if not rs:
        return None
    def m(k):
        v = [x[k] for x in rs if x.get(k) is not None and x.get(k) == x.get(k)]
        return float(np.mean(v)) if v else float("nan")
    fb = m("fb_m")
    return {"fb": fb, "jct_m": m("jct_m"), "jct_bg": m("jct_bg_small"),
            "run": m("mean_running"), "m": rs[0]["m"], "n": len(rs)}


def conc(s):
    """measured concurrency for this s, averaged over the ratio sweep"""
    v = [x["mean_running"] for x in ROWS if x["s"] == s
         and x["mean_running"] == x["mean_running"]]
    return float(np.mean(v)) if v else float("nan")


def r_safe(s):
    ok = [r for r in RATIOS if (cell(s, r) or {}).get("fb", 0) >= SAFE_FB]
    return max(ok) if ok else None


CONC = {s: conc(s) for s in S_VALUES}
RS = {s: r_safe(s) for s in S_VALUES}

print("N=256, rho=0.85, greedy SRPT. Concurrency swept by coarsening the "
      "background {s,2s,4s,8s}.\n")
print(f"{'s':>4}{'background':>22}{'concurrency':>13}{'r_safe':>9}   "
      "flow balance of the large class by m/N")
print(f"{'':>48}   " + " ".join(f"{r:>7}" for r in RATIOS))
for s in S_VALUES:
    bg = f"{[s, 2*s, 4*s, 8*s]}"
    print(f"{s:>4}{bg:>22}{CONC[s]:>13.1f}{str(RS[s]):>9}   "
          + " ".join((f"{cell(s, r)['fb']:>7.3f}" if cell(s, r) else f"{'-':>7}")
                     for r in RATIOS))

print(f"\n{'s':>4}{'concurrency':>13}   mean JCT of the large class by m/N")
for s in S_VALUES:
    print(f"{s:>4}{CONC[s]:>13.1f}   "
          + " ".join((f"{cell(s, r)['jct_m']:>7.1f}" if cell(s, r) else f"{'-':>7}")
                     for r in RATIOS))

# the cell closest to the real cluster's operating point
s_philly = min(S_VALUES, key=lambda s: abs(CONC[s] - PHILLY_CONC))
s_e8 = min(S_VALUES, key=lambda s: abs(CONC[s] - E8_CONC))
print(f"\nclosest to Philly 11cb48 (concurrency {PHILLY_CONC}): s={s_philly} "
      f"at concurrency {CONC[s_philly]:.1f}, r_safe = {RS[s_philly]}")
print(f"closest to the EP-0006 overlap point (concurrency {E8_CONC}): "
      f"s={s_e8} at concurrency {CONC[s_e8]:.1f}, r_safe = {RS[s_e8]}")

# ------------------------------------------------------------------ grading
V = []


def rec(pid, claim, ok, detail):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail})
    print(f"{pid:>3}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")


print("\n\n=== PRED-008 grading ===")

rec("W1", "r_safe rises as concurrency falls below the previously measured range",
    RS[s_philly] is not None and RS[s_philly] > 0.625,
    f"at concurrency {CONC[s_philly]:.1f}: r_safe = {RS[s_philly]} "
    f"(EP-0006 measured 0.625 at 28.5)")

order = sorted(S_VALUES, key=lambda s: CONC[s])
seq = [(CONC[s], RS[s]) for s in order]
inv = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)
       if seq[i][1] is not None and seq[i + 1][1] is not None
       and seq[i + 1][1] > seq[i][1]]
rec("W2", "r_safe is monotone non-increasing in concurrency", not inv,
    "by concurrency: " + "  ".join(f"{c:.1f}:{r}" for c, r in seq)
    + (f"; inversions {inv}" if inv else ""))

rec("W3", "DECIDING: at Philly's operating point r_safe >= 0.75, so its ratio "
          "of 0.59 has at least 0.16 of headroom",
    RS[s_philly] is not None and RS[s_philly] >= 0.75,
    f"concurrency {CONC[s_philly]:.1f} -> r_safe {RS[s_philly]}; headroom over "
    f"Philly's {PHILLY_RATIO} = "
    f"{(RS[s_philly] - PHILLY_RATIO):.3f}" if RS[s_philly] else "undefined")

gap = (abs(RATIOS.index(RS[s_e8]) - RATIOS.index(0.625))
       if RS[s_e8] in RATIOS else None)
rec("W4", "reproduces EP-0006 where they overlap (within one grid step of 0.625)",
    gap is not None and gap <= 1,
    f"at concurrency {CONC[s_e8]:.1f}: r_safe = {RS[s_e8]} vs EP-0006's 0.625 "
    f"at 28.5; gap = {gap} grid step(s)")

full = [(s, (cell(s, 1.0) or {}).get("fb", float("nan"))) for s in S_VALUES]
rec("W5", "whole-pool jobs stay starved at every concurrency",
    all(v < STARVE_FB for _, v in full),
    "flow balance at m=N: " + "  ".join(f"s={s}:{v:.3f}" for s, v in full))

c = cell(s_philly, 0.625)
ratio6 = c["jct_m"] / c["jct_bg"] if c and c["jct_bg"] else float("nan")
rec("W6", "the harm at Philly's operating point is mild (large class < 5x the "
          "smallest background class)", ratio6 < 5,
    f"at concurrency {CONC[s_philly]:.1f}, m/N=0.625: large class JCT "
    f"{c['jct_m']:.2f} vs background {c['jct_bg']:.2f} = {ratio6:.1f}x")

n_pass = sum(v["pass"] for v in V)
print(f"\n{n_pass}/{len(V)} sealed predictions passed")
w3 = next(v for v in V if v["id"] == "W3")
print("\npre-committed consequence: " + (
    "W3 PASSED -- v6's reading is upgraded from extrapolation to measurement: "
    "Philly's riskiest virtual cluster has real headroom, and no examined "
    "production pool is near the boundary."
    if w3["pass"] else
    "W3 FAILED -- v6 is wrong about the real cluster's position. Philly's "
    "11cb48 is near the boundary; partially reverse the EP-0004/EP-0005 "
    "demotions and name the production configuration as at-risk."))
json.dump({"n_pass": n_pass, "n_total": len(V),
           "concurrency": CONC, "r_safe": RS,
           "s_closest_to_philly": s_philly, "w3_passed": w3["pass"],
           "results": V},
          open(os.path.join(HERE, "results", "E9_grading.json"), "w"),
          indent=2, default=str)
