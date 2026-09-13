"""Adjudicate ambiguous stability verdicts with an explicit two-horizon test.

Why this file exists. Three single-horizon detectors have now failed:

  1. completion_frac < threshold   -- a finite system always drains after
     arrivals stop, so it never fires (EP-0001).
  2. util_over_rho < 0.995         -- fires on long transients in stable
     systems (EP-0001, and again on E2 easy_backfill).
  3. min per-class flow balance    -- horizon-dependent in level: FCFS at
     theta=0.4 rho=0.85 reads 0.80 at 30k jobs and 0.95 at 120k while its mean
     JCT FALLS (x0.65), i.e. stable; FCFS at theta=2.0 reads a HIGHER 0.87 yet
     its mean JCT grows x3.22, i.e. divergent.

What survived validation (calib/c06) is the *spread* of flow balance across
need classes: a starving class sits near 0.4 while every other class sits at
1.00, and that signature is horizon-invariant (0.361 -> 0.419 over a 4x
horizon) while the starved class's JCT grows linearly with the horizon.

So the rule is:
  spread > SPREAD_STARVE            -> class-starved   (no re-run needed)
  min_fb >= LEVEL_OK                -> stable          (no re-run needed)
                                       LEVEL_OK is 0.995, not 0.97: cells with
                                       min_fb ~ 0.98 turned out to grow 3.4x
                                       over a 4x horizon, because a 2% per-job
                                       deficit accumulates linearly.
  otherwise                         -> ambiguous, decided by re-running the
                                       cell at 30k and 120k jobs and asking
                                       whether mean JCT scales with horizon.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload, geometric_mix
from sim.cluster import simulate

HERE = os.path.dirname(os.path.abspath(__file__))
N = 64
SPREAD_STARVE = 0.30
LEVEL_OK = 0.995
GROW_DIVERGE = 2.0     # mean JCT grows at least 2x over a 4x horizon
GROW_STABLE = 1.30
HORIZONS = (30_000, 120_000)
ADJ_SEEDS = (201, 202)


def spread(r):
    fb = r["flow_balance_by_need"]
    return max(fb.values()) - min(fb.values()) if fb else float("nan")


def single_horizon_class(r):
    """Verdict from one horizon: 'unusable', 'class-starved', 'stable', or
    'ambiguous' (needs the two-horizon test)."""
    if r["aborted_backlog"] or r["hit_time_limit"] or r["completion_frac"] < 0.98:
        return "unusable"
    if spread(r) > SPREAD_STARVE:
        return "class-starved"
    if r["min_flow_balance"] >= LEVEL_OK:
        return "stable"
    return "ambiguous"


def _one(task):
    theta, rho, pol, sigma, mode, n_jobs, seed = task
    needs, probs = geometric_mix(theta)
    jobs, _ = make_workload(n_jobs, rho, N, seed=seed, needs=needs,
                            need_probs=probs, sigma=sigma, est_mode=mode)
    m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                 backlog_cap=40_000)
    return (theta, rho, pol, sigma, mode, n_jobs, seed,
            m["mean_jct"], m["min_flow_balance"], spread(m),
            bool(m["hit_time_limit"] or m["aborted_backlog"]))


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    E2 = json.load(open(os.path.join(HERE, "results", "E2.json")))
    E3 = json.load(open(os.path.join(HERE, "results", "E3.json")))

    amb = {}
    for r in E2["rows"]:
        if single_horizon_class(r) == "ambiguous":
            amb[(r["theta"], r["rho"], r["policy"], 0.0, "mean")] = True
    for r in E3["rows"]:
        if single_horizon_class(r) == "ambiguous":
            amb[(0.4, 0.85, r["policy"], r["sigma"], r["est_mode"])] = True
    keys = sorted(amb)
    print(f"{len(keys)} ambiguous cells to adjudicate "
          f"x {len(HORIZONS)} horizons x {len(ADJ_SEEDS)} seeds "
          f"= {len(keys) * len(HORIZONS) * len(ADJ_SEEDS)} runs")
    for k in keys:
        print("   ", k)

    tasks = [k + (n, s) for k in keys for n in HORIZONS for s in ADJ_SEEDS]
    t0, out = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(_one, tasks), 1):
            out.append(rec)
            if i % 8 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    verdicts = {}
    print(f"\n{'cell':<46}{'jct@30k':>10}{'jct@120k':>10}{'growth':>8}  verdict")
    for k in keys:
        got = {n: [r[7] for r in out if r[:5] == k and r[5] == n] for n in HORIZONS}
        bad = any(r[10] for r in out if r[:5] == k)
        a, b = np.mean(got[HORIZONS[0]]), np.mean(got[HORIZONS[1]])
        g = b / a
        v = ("unusable" if bad else
             "overloaded" if g >= GROW_DIVERGE else
             "stable" if g <= GROW_STABLE else "undetermined")
        verdicts["|".join(map(str, k))] = {"jct_30k": float(a), "jct_120k": float(b),
                                           "growth": float(g), "verdict": v}
        print(f"{str(k):<46}{a:>10.2f}{b:>10.2f}{g:>8.2f}  {v}")

    json.dump({"rule": {"spread_starve": SPREAD_STARVE, "level_ok": LEVEL_OK,
                        "grow_diverge": GROW_DIVERGE, "grow_stable": GROW_STABLE,
                        "horizons": list(HORIZONS), "seeds": list(ADJ_SEEDS)},
               "verdicts": verdicts},
              open(os.path.join(HERE, "results", "adjudication.json"), "w"), indent=1)
    print("\nwrote results/adjudication.json")
