"""Grade PRED-001 against results/E1.json and print the phase table.

A cell is marked DIVERGED when the backlog grows over the arrival window
(utilization below the offered load, or the last backlog decile more than 3x the
first and above 50 jobs, or the backlog cap was hit). A diverged cell has no
meaningful mean JCT, so comparisons treat it as infinitely worse.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "results", "E1.json")))
rows = D["rows"]
CFG = D["config"]
NONPRE = {"fcfs", "easy_backfill"}


def diverged(r):
    grow = r["backlog_growing"]
    b0, b1 = r["backlog_first_decile"], r["backlog_last_decile"]
    ramp = (b1 > 3 * b0 and b1 > 50) if (b0 == b0 and b1 == b1) else False
    return bool(r["aborted_backlog"] or r["completion_frac"] < 0.98 or grow or ramp)


def cell(mix, pol, sigma, c_pre):
    cp = 0.0 if pol in NONPRE else c_pre
    rs = [r for r in rows if r["mix"] == mix and r["policy"] == pol
          and abs(r["sigma"] - sigma) < 1e-9 and abs(r["c_pre"] - cp) < 1e-9]
    if not rs:
        return None
    div = [diverged(r) for r in rs]
    jct = np.array([r["mean_jct"] for r in rs])
    return {
        "n": len(rs), "n_div": sum(div), "diverged": any(div),
        "jct": float(jct.mean()),
        "jct_se": float(jct.std(ddof=1) / np.sqrt(len(jct))) if len(jct) > 1 else float("nan"),
        "jct_by_seed": {r["seed"]: r["mean_jct"] for r in rs},
        "p99": float(np.mean([r["p99_jct"] for r in rs])),
        "lost": float(np.mean([r["lost_work_frac"] for r in rs])),
        "pre": float(np.mean([r["preempts_per_job"] for r in rs])),
        "util_over_rho": float(np.mean([r["util_over_rho"] for r in rs])),
    }


def ratio(mix, a, b, sigma, c_pre):
    """Paired mean JCT ratio a/b. Diverged cells give inf (a) or 0 (b)."""
    ca, cb = cell(mix, a, sigma, c_pre), cell(mix, b, sigma, c_pre)
    if ca is None or cb is None:
        return float("nan"), ca, cb
    if ca["diverged"] and not cb["diverged"]:
        return float("inf"), ca, cb
    if cb["diverged"] and not ca["diverged"]:
        return 0.0, ca, cb
    seeds = sorted(set(ca["jct_by_seed"]) & set(cb["jct_by_seed"]))
    pr = np.array([ca["jct_by_seed"][s] / cb["jct_by_seed"][s] for s in seeds])
    return float(pr.mean()), ca, cb


# ------------------------------------------------------------------ tables
for mix in ["trace_like", "gang_heavy"]:
    print(f"\n=== {mix}  (rho={CFG['rho']}, N={CFG['n_servers']}, "
          f"n_jobs={CFG['n_jobs']}, {len(CFG['seeds'])} seeds) ===")
    print("mean JCT   (D = diverged: backlog grows over the window)")
    hdr = "  ".join(f"c={c:<5}" for c in CFG["c_pres"])
    print(f"{'policy':<14}{'sigma':>6}   {hdr}")
    for pol in ["fcfs", "easy_backfill", "srpt", "sf_srpt"]:
        for sigma in CFG["sigmas"]:
            cells = []
            for c in CFG["c_pres"]:
                cc = cell(mix, pol, sigma, c)
                if cc is None:
                    cells.append("     -   ")
                elif cc["diverged"]:
                    cells.append(f"{cc['jct']:>7.1f}D")
                else:
                    cells.append(f"{cc['jct']:>7.2f} ")
            print(f"{pol:<14}{sigma:>6}   " + "  ".join(cells))

    print("\n  reversal map: mean_jct(srpt)/mean_jct(easy_backfill)  (>1 = backfill wins)")
    for sigma in CFG["sigmas"]:
        vals = []
        for c in CFG["c_pres"]:
            r, _, _ = ratio(mix, "srpt", "easy_backfill", sigma, c)
            vals.append(f"{r:>8.3f}" if np.isfinite(r) else f"{'inf':>8}")
        print(f"    sigma={sigma:<5}" + "".join(vals))
    print("  sf_srpt/srpt  (<1 = ServerFilling wins)")
    for sigma in CFG["sigmas"]:
        vals = []
        for c in CFG["c_pres"]:
            r, _, _ = ratio(mix, "sf_srpt", "srpt", sigma, c)
            vals.append(f"{r:>8.3f}" if np.isfinite(r) else f"{'inf':>8}")
        print(f"    sigma={sigma:<5}" + "".join(vals))

# -------------------------------------------------------------- grading
print("\n\n=== PRED-001 grading ===")
verdicts = []


def record(pid, claim, passed, detail):
    verdicts.append({"id": pid, "pass": bool(passed), "detail": detail})
    print(f"{pid}  {'PASS' if passed else 'FAIL':<4}  {claim}\n      {detail}")


r, _, _ = ratio("trace_like", "srpt", "easy_backfill", 1.0, 0.0)
record("P1", "trace_like sigma=1, c=0: srpt/backfill < 0.95", r < 0.95, f"ratio={r:.4f}")

r2, _, _ = ratio("trace_like", "srpt", "easy_backfill", 2.0, 0.0)
record("P2", "trace_like sigma=2, c=0: srpt still beats backfill (<1.0)", r2 < 1.0,
       f"ratio={r2:.4f}")

r3, _, _ = ratio("trace_like", "srpt", "easy_backfill", 0.0, 0.2)
record("P3", "trace_like c=0.2, sigma=0: srpt loses to backfill (>1.0)", r3 > 1.0,
       f"ratio={r3:.4f}")

r4a, _, _ = ratio("trace_like", "srpt", "easy_backfill", 0.0, 0.05)
record("P4", "crossover in c_pre strictly between 0.05 and 0.2",
       r4a < 1.0 and r3 > 1.0, f"ratio(c=0.05)={r4a:.4f}, ratio(c=0.2)={r3:.4f}")

r5, _, _ = ratio("gang_heavy", "sf_srpt", "srpt", 0.0, 0.2)
record("P5", "gang_heavy c=0.2: sf_srpt still beats srpt (<1.0)", r5 < 1.0,
       f"ratio={r5:.4f}")

p6 = []
for mix in ["trace_like", "gang_heavy"]:
    for c in [0.05, 0.2]:
        a, b = cell(mix, "sf_srpt", 0.0, c), cell(mix, "srpt", 0.0, c)
        rr = a["lost"] / b["lost"] if b["lost"] > 0 else float("inf")
        p6.append((mix, c, rr))
record("P6", "lost_work_frac(sf_srpt)/lost(srpt) > 1.5 in every c>0 cell",
       all(x[2] > 1.5 for x in p6),
       ", ".join(f"{m}/c={c}: {v:.2f}" for m, c, v in p6))

a0, a2 = cell("gang_heavy", "sf_srpt", 0.0, 0.0), cell("gang_heavy", "sf_srpt", 2.0, 0.0)
b0, b2 = cell("gang_heavy", "srpt", 0.0, 0.0), cell("gang_heavy", "srpt", 2.0, 0.0)
deg_sf, deg_srpt = a2["jct"] / a0["jct"], b2["jct"] / b0["jct"]
record("P7", "gang_heavy: sigma 0->2 degrades sf_srpt less than srpt",
       deg_sf < deg_srpt, f"sf_srpt x{deg_sf:.3f} vs srpt x{deg_srpt:.3f}")

e0, e2 = cell("trace_like", "easy_backfill", 0.0, 0.0), cell("trace_like", "easy_backfill", 2.0, 0.0)
ch = e2["jct"] / e0["jct"] - 1.0
record("P8", "trace_like: backfill JCT change from sigma 0->2 within 15%",
       abs(ch) < 0.15, f"change={ch:+.2%} ({e0['jct']:.3f} -> {e2['jct']:.3f})")

base = cell("trace_like", "fcfs", 0.0, 0.0)["jct"]
devs = [abs(cell("trace_like", "fcfs", s, 0.0)["jct"] / base - 1.0) for s in CFG["sigmas"]]
record("P9", "fcfs is untouched by the frictions (<3% across cells)",
       max(devs) < 0.03, f"max deviation={max(devs):.2%}")

gh = [cell("gang_heavy", "fcfs", s, 0.0) for s in CFG["sigmas"]]
record("P10", "gang_heavy: fcfs backlog grows in every cell",
       all(c["diverged"] for c in gh),
       f"diverged cells {sum(c['diverged'] for c in gh)}/{len(gh)}, "
       f"util/rho={np.mean([c['util_over_rho'] for c in gh]):.4f}")

n_pass = sum(v["pass"] for v in verdicts)
print(f"\n{n_pass}/{len(verdicts)} sealed predictions passed")
json.dump(verdicts, open(os.path.join(HERE, "results", "E1_grading.json"), "w"), indent=2)
