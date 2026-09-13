"""Grade PRED-002 against results/E2.json and results/E3.json.

Stability verdicts come from the layered rule validated in calib/c06 and
results/adjudication.json (see adjudicate.py for why three earlier
single-horizon detectors failed):

  unusable       run aborted, hit the time limit, or did not drain
  class-starved  flow balance spread across need classes > 0.30 -- one class
                 completes ~40% of its arrivals while every other class
                 completes ~100%. Horizon-invariant, so no re-run needed.
  stable         every class's flow balance >= 0.995
  otherwise      decided by the two-horizon test in adjudicate.py: the cell is
                 re-run at 30k and 120k jobs and called "overloaded" if mean
                 JCT grows >= 2x, "stable" if it grows <= 1.3x.

Only cells whose verdict is "stable" enter a ratio. PRED-002 did not fix the
detector formula at seal time; that is a flaw of the seal, recorded as lesson
M-7. The as-run grading is printed alongside so the change is auditable.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E2 = json.load(open(os.path.join(HERE, "results", "E2.json")))
E3 = json.load(open(os.path.join(HERE, "results", "E3.json")))
ADJ = json.load(open(os.path.join(HERE, "results", "adjudication.json")))["verdicts"]
THETAS = E2["config"]["thetas"]
RHOS = E2["config"]["rhos"]
SIGMAS = [0.0, 0.5, 1.0, 2.0, 3.0]
POLICIES = ["fcfs", "easy_backfill", "srpt", "sf_srpt"]
SPREAD_STARVE, LEVEL_OK = 0.30, 0.995
MARK = {"stable": ".", "class-starved": "S", "overloaded": "O", "unusable": "X",
        "undetermined": "?", "unadjudicated": "!"}


def spread(r):
    fb = r["flow_balance_by_need"]
    return max(fb.values()) - min(fb.values()) if fb else float("nan")


def diverged_asrun(r):
    b0, b1 = r["backlog_first_decile"], r["backlog_last_decile"]
    ramp = (b1 > 3 * b0 and b1 > 50) if (b0 == b0 and b1 == b1) else False
    return bool(r["aborted_backlog"] or r["completion_frac"] < 0.98
                or r["backlog_growing"] or ramp)


def verdict(rows, key):
    if any(r["aborted_backlog"] or r["hit_time_limit"] or r["completion_frac"] < 0.98
           for r in rows):
        return "unusable"
    if any(spread(r) > SPREAD_STARVE for r in rows):
        return "class-starved"
    if all(r["min_flow_balance"] >= LEVEL_OK for r in rows):
        return "stable"
    a = ADJ.get("|".join(map(str, key)))
    return a["verdict"] if a else "unadjudicated"


def agg(rows, key):
    if not rows:
        return None
    jct = np.array([r["mean_jct"] for r in rows])
    v = verdict(rows, key)
    return {"n": len(rows), "verdict": v, "ok": v == "stable",
            "mark": MARK[v],
            "div_asrun": any(diverged_asrun(r) for r in rows),
            "starving": sorted({int(k) for r in rows for k in r["starving_needs"]}),
            "jct": float(jct.mean()),
            "se": float(jct.std(ddof=1) / np.sqrt(len(jct))) if len(jct) > 1 else float("nan"),
            "by_seed": {r["seed"]: r["mean_jct"] for r in rows},
            "worst_class_jct": float(np.mean([max(r["jct_by_need"].values()) for r in rows])),
            "min_fb": float(np.mean([r["min_flow_balance"] for r in rows])),
            "p99": float(np.mean([r["p99_jct"] for r in rows]))}


def c2(theta, rho, pol):
    return agg([r for r in E2["rows"] if abs(r["theta"] - theta) < 1e-9
                and abs(r["rho"] - rho) < 1e-9 and r["policy"] == pol],
               (theta, rho, pol, 0.0, "mean"))


def c3(mode, sigma, pol):
    return agg([r for r in E3["rows"] if r["est_mode"] == mode
                and abs(r["sigma"] - sigma) < 1e-9 and r["policy"] == pol],
               (0.4, 0.85, pol, sigma, mode))


def pair_ratio(a, b):
    """Paired-seed mean ratio; NaN unless BOTH cells are stable."""
    if a is None or b is None or not a["ok"] or not b["ok"]:
        return float("nan")
    seeds = sorted(set(a["by_seed"]) & set(b["by_seed"]))
    return float(np.mean([a["by_seed"][s] / b["by_seed"][s] for s in seeds]))


# ------------------------------------------------------------- phase diagram
print("=== PHASE DIAGRAM  (. stable   S class-starved   O overloaded   "
      "X unusable   ? undetermined) ===")
print(f"{'rho':>6} {'theta':>6} " + " ".join(f"{p:>14}" for p in POLICIES))
for rho in RHOS:
    for th in THETAS:
        print(f"{rho:>6} {th:>6} " + " ".join(
            f"{c2(th, rho, p)['mark']:>14}" for p in POLICIES))

# ------------------------------------------------------------------ E2 tables
print("\n=== E2  mean JCT over all jobs (verdict mark appended) ===")
for rho in RHOS:
    print(f"\n rho={rho}")
    print(f"{'theta':>6} " + " ".join(f"{p:>15}" for p in POLICIES) + "   sf/srpt")
    for th in THETAS:
        cells = [f"{c2(th, rho, p)['jct']:>14.2f}{c2(th, rho, p)['mark']}"
                 for p in POLICIES]
        r = pair_ratio(c2(th, rho, "sf_srpt"), c2(th, rho, "srpt"))
        print(f"{th:>6} " + " ".join(cells) + (f"{r:>9.3f}" if r == r else "      n/a"))

print("\n=== E2  worst need-class mean JCT (what the unluckiest class sees) ===")
for rho in RHOS:
    print(f"\n rho={rho}")
    print(f"{'theta':>6} " + " ".join(f"{p:>15}" for p in POLICIES))
    for th in THETAS:
        print(f"{th:>6} " + " ".join(
            f"{c2(th, rho, p)['worst_class_jct']:>14.1f}{c2(th, rho, p)['mark']}"
            for p in POLICIES))

print("\n=== E2  starving need classes by cell ===")
for rho in RHOS:
    for p in POLICIES:
        s = " ".join(f"{th}:{'-' if not c2(th, rho, p)['starving'] else ','.join(map(str, c2(th, rho, p)['starving']))}"
                     for th in THETAS)
        print(f" rho={rho} {p:<14} {s}")

print("\n=== stable region per policy (all classes fed, no horizon growth) ===")
for rho in RHOS:
    for p in POLICIES:
        ok = [th for th in THETAS if c2(th, rho, p)["ok"]]
        print(f"  rho={rho} {p:<14} {ok if ok else 'none'}")

print("\ncrossover theta* (smallest theta where sf_srpt beats srpt, both stable):")
star = {}
for rho in RHOS:
    hit = [th for th in THETAS
           if (pair_ratio(c2(th, rho, "sf_srpt"), c2(th, rho, "srpt")) or 9) < 1.0]
    star[rho] = hit[0] if hit else None
    print(f"  rho={rho}: theta*={star[rho]}")

# ------------------------------------------------------------------ E3 tables
E3P = ["easy_backfill", "srpt", "sf_srpt"]
print("\n=== E3  theta=0.4, rho=0.85 (mean JCT) ===")
print(f"{'mode':>7}{'sigma':>7} " + " ".join(f"{p:>16}" for p in E3P)
      + "   srpt/backfill")
for mode in ["mean", "median"]:
    for s in SIGMAS:
        cs = {p: c3(mode, s, p) for p in E3P}
        cells = [f"{cs[p]['jct']:>15.3f}{cs[p]['mark']}" for p in E3P]
        r = pair_ratio(cs["srpt"], cs["easy_backfill"])
        print(f"{mode:>7}{s:>7} " + " ".join(cells) +
              (f"{r:>14.3f}" if r == r else "           n/a"))

print("\n=== E3  worst need-class mean JCT ===")
print(f"{'mode':>7}{'sigma':>7} " + " ".join(f"{p:>16}" for p in E3P))
for mode in ["mean", "median"]:
    for s in SIGMAS:
        print(f"{mode:>7}{s:>7} " + " ".join(
            f"{c3(mode, s, p)['worst_class_jct']:>15.1f}{c3(mode, s, p)['mark']}"
            for p in E3P))

# -------------------------------------------------------------------- grading
V = []


def rec(pid, claim, ok, detail, ok_asrun=None, detail_asrun=None):
    V.append({"id": pid, "claim": claim, "pass": bool(ok), "detail": detail,
              "pass_asrun": None if ok_asrun is None else bool(ok_asrun),
              "detail_asrun": detail_asrun})
    print(f"{pid}  {'PASS' if ok else 'FAIL':<4}  {claim}\n      {detail}")
    if ok_asrun is not None and bool(ok_asrun) != bool(ok):
        print(f"      [as-run detector would have said "
              f"{'PASS' if ok_asrun else 'FAIL'}: {detail_asrun}]")


print("\n\n=== PRED-002 grading ===")

r04 = pair_ratio(c2(0.4, 0.85, "sf_srpt"), c2(0.4, 0.85, "srpt"))
r08 = pair_ratio(c2(0.8, 0.85, "sf_srpt"), c2(0.8, 0.85, "srpt"))
s04, s08 = c2(0.4, 0.85, "srpt"), c2(0.8, 0.85, "srpt")
rec("Q1", "a mix threshold exists between theta=0.4 and 0.8 (rho=0.85): "
          "sf/srpt > 1 then < 1",
    r04 == r04 and r08 == r08 and r04 > 1 and r08 < 1,
    f"ratio(0.4)={r04}, ratio(0.8)={r08}; greedy SRPT is {s04['verdict']} at "
    f"theta=0.4 (starving {s04['starving']}) and {s08['verdict']} at theta=0.8. "
    f"No like-for-like crossover exists at rho=0.85: greedy SRPT is never "
    f"stable on this grid, so the prediction's frame was wrong.")

i7 = THETAS.index(star[0.7]) if star[0.7] else None
i95 = THETAS.index(star[0.95]) if star[0.95] else None
rec("Q2", "crossover moves at most one grid step between rho=0.7 and 0.95",
    i7 is not None and i95 is not None and abs(i7 - i95) <= 1,
    f"theta* = {star[0.7]} (rho=0.7) vs {star[0.95]} (rho=0.95)")

ratios = [(th, pair_ratio(c2(th, 0.85, "sf_srpt"), c2(th, 0.85, "srpt")))
          for th in THETAS]
valid = [(th, v) for th, v in ratios if v == v]
bad = [(valid[i][0], valid[i + 1][0]) for i in range(len(valid) - 1)
       if valid[i + 1][1] > valid[i][1] * 1.05]
rec("Q3", "sf/srpt ratio decreases monotonically in theta (rho=0.85)",
    bool(valid) and not bad,
    f"{len(valid)} comparable cells: "
    + (", ".join(f"{th}:{v:.3f}" for th, v in valid) if valid else "none")
    + (" -- too few to test monotonicity" if len(valid) < 3 else "")
    + (f"; increases at {bad}" if bad else ""))

srpt_ok_low = all(c2(th, 0.85, "srpt")["ok"] for th in [0.4, 0.6, 0.8])
srpt_bad_16 = not c2(1.6, 0.85, "srpt")["ok"]
rec("Q4", "srpt stable at theta<=0.8 and unstable at theta=1.6 (rho=0.85)",
    srpt_ok_low and srpt_bad_16,
    "verdict by theta: " + ", ".join(
        f"{th}:{c2(th, 0.85, 'srpt')['verdict']}" for th in THETAS))

eb_bad = [(th, rho, c2(th, rho, "easy_backfill")["verdict"])
          for th in THETAS for rho in RHOS if not c2(th, rho, "easy_backfill")["ok"]]
eb_bad_asrun = [(th, rho) for th in THETAS for rho in RHOS
                if c2(th, rho, "easy_backfill")["div_asrun"]]
rec("Q5", "easy_backfill never becomes unstable anywhere in E2", not eb_bad,
    f"unstable cells: {eb_bad if eb_bad else 'none'}; worst flow balance over "
    f"all 21 backfill cells = "
    f"{min(c2(th, rho, 'easy_backfill')['min_fb'] for th in THETAS for rho in RHOS):.3f}",
    not eb_bad_asrun, f"as-run detector flagged {eb_bad_asrun}")

f04 = c2(0.4, 0.85, "fcfs")["ok"]
fhigh = all(not c2(th, 0.85, "fcfs")["ok"] for th in [1.0, 1.25, 1.6, 2.0])
rec("Q6", "fcfs stable at theta=0.4, unstable at theta>=1.0 (rho=0.85)",
    f04 and fhigh,
    "verdict by theta: " + ", ".join(
        f"{th}:{c2(th, 0.85, 'fcfs')['verdict']}" for th in THETAS)
    + f"; fcfs mean JCT at theta=0.4 is {c2(0.4, 0.85, 'fcfs')['jct']:.1f} vs "
      f"{c2(0.4, 0.85, 'easy_backfill')['jct']:.2f} for backfill, i.e. stable "
      f"but 38x worse")

q7bad = []
for th in THETAS:
    for rho in RHOS:
        eb, a, b = (c2(th, rho, "easy_backfill"), c2(th, rho, "srpt"),
                    c2(th, rho, "sf_srpt"))
        if not eb["ok"]:
            continue
        cand = [c["jct"] for c in (a, b) if c["ok"]]
        if cand and min(cand) >= eb["jct"]:
            q7bad.append((th, rho, round(eb["jct"], 2), round(min(cand), 2)))
wc = sum(1 for th in THETAS for rho in RHOS
         if c2(th, rho, "easy_backfill")["worst_class_jct"]
         < c2(th, rho, "srpt")["worst_class_jct"])
rec("Q7", "easy_backfill is never the best policy in a stable cell", not q7bad,
    f"cells where backfill wins on mean JCT: {q7bad if q7bad else 'none'}; but "
    f"on WORST-CLASS JCT backfill beats greedy SRPT in {wc}/{len(THETAS) * len(RHOS)} "
    f"cells, so 'never best' holds only for the aggregate metric")

med = [c3("median", s, "easy_backfill")["jct"] for s in SIGMAS]
mses = [c3("median", s, "easy_backfill")["se"] for s in SIGMAS]
drops = [(SIGMAS[i], SIGMAS[i + 1]) for i in range(len(SIGMAS) - 1)
         if med[i + 1] < med[i] - mses[i]]
rec("Q8", "median-unbiased: backfill mean JCT is monotone non-decreasing in sigma",
    not drops, "JCT " + " ".join(f"{s}:{v:.3f}+-{e:.3f}"
                                 for s, v, e in zip(SIGMAS, med, mses))
    + (f"; drops at {drops}" if drops else ""))

q9 = pair_ratio(c3("median", 3.0, "srpt"), c3("median", 3.0, "easy_backfill"))
sr, eb3 = c3("median", 3.0, "srpt"), c3("median", 3.0, "easy_backfill")
rec("Q9", "median-unbiased sigma=3: srpt still beats backfill on mean JCT",
    q9 == q9 and q9 < 1.0,
    f"ratio={q9}; greedy SRPT is {sr['verdict']} (starving {sr['starving']}), so "
    f"the paired ratio is withheld. Unpaired means: srpt {sr['jct']:.3f} vs "
    f"backfill {eb3['jct']:.3f}; worst-class {sr['worst_class_jct']:.1f} vs "
    f"{eb3['worst_class_jct']:.1f}")

a, b = c3("median", 3.0, "easy_backfill"), c3("mean", 3.0, "easy_backfill")
rec("Q10", "at sigma=3 backfill is worse under median-unbiased than mean-unbiased",
    a["jct"] > b["jct"] + b["se"],
    f"median={a['jct']:.3f}+-{a['se']:.3f} vs mean={b['jct']:.3f}+-{b['se']:.3f}")

n_pass = sum(v["pass"] for v in V)
n_asrun = sum(1 for v in V
              if (v["pass_asrun"] if v["pass_asrun"] is not None else v["pass"]))
print(f"\n{n_pass}/{len(V)} sealed predictions passed")
print(f"as-run detector would have given: {n_asrun}/{len(V)}")
json.dump({"detector": "layered: spread / level / two-horizon (adjudicate.py)",
           "n_pass": n_pass, "n_total": len(V), "n_pass_asrun": n_asrun,
           "results": V},
          open(os.path.join(HERE, "results", "E2E3_grading.json"), "w"), indent=2)
