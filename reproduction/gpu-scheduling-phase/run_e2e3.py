"""E2: gang-need-mix axis (theta) x load.  E3: noise parameterisation x sigma.

Predictions sealed in predictions/PRED-002.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload, geometric_mix, mix_stats
from sim.cluster import simulate

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
SEEDS = [201, 202, 203, 204, 205]
THETAS = [0.4, 0.6, 0.8, 1.0, 1.25, 1.6, 2.0]
RHOS = [0.7, 0.85, 0.95]
POLICIES = ["fcfs", "easy_backfill", "srpt", "sf_srpt"]
BACKLOG_CAP = 6000
KEEP = ["mean_jct", "p99_jct", "mean_slowdown", "mean_wait", "max_wait",
        "utilization", "rho_emp", "util_over_rho", "mean_backlog",
        "preempts_per_job", "lost_work_frac", "completion_frac",
        "backlog_growing", "aborted_backlog", "hit_time_limit", "backlog_slope",
        "backlog_first_decile", "backlog_last_decile", "jct_by_need",
        "completion_frac_by_need", "flow_balance_by_need", "min_flow_balance",
        "starving_needs", "jct_spread_by_need"]
HERE = os.path.dirname(os.path.abspath(__file__))


def run_e2(task):
    theta, rho, pol, seed = task
    needs, probs = geometric_mix(theta)
    jobs, lam = make_workload(N_JOBS, rho, N, seed=seed, needs=needs, need_probs=probs)
    t0 = time.time()
    m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                 backlog_cap=BACKLOG_CAP)
    rec = {k: m[k] for k in KEEP}
    rec.update(theta=theta, rho=rho, policy=pol, seed=seed, lam=lam,
               secs=round(time.time() - t0, 1), **mix_stats(needs, probs, N))
    return rec


def run_e3(task):
    mode, sigma, pol, seed = task
    needs, probs = geometric_mix(0.4)
    jobs, lam = make_workload(N_JOBS, 0.85, N, seed=seed, needs=needs,
                              need_probs=probs, sigma=sigma, est_mode=mode)
    t0 = time.time()
    m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                 backlog_cap=BACKLOG_CAP)
    rec = {k: m[k] for k in KEEP}
    rec.update(est_mode=mode, sigma=sigma, policy=pol, seed=seed,
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    t2 = [(th, rho, pol, s) for th in THETAS for rho in RHOS
          for pol in POLICIES for s in SEEDS]
    t3 = [(mode, sig, pol, s) for mode in ["mean", "median"]
          for sig in [0.0, 0.5, 1.0, 2.0, 3.0]
          for pol in ["easy_backfill", "srpt", "sf_srpt"] for s in SEEDS]
    print(f"E2: {len(t2)} runs   E3: {len(t3)} runs   workers={workers}")

    for name, tasks, fn in [("E2", t2, run_e2), ("E3", t3, run_e3)]:
        t0, rows = time.time(), []
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for i, rec in enumerate(ex.map(fn, tasks), 1):
                rows.append(rec)
                if i % 40 == 0 or i == len(tasks):
                    print(f"  {name} {i}/{len(tasks)}  ({time.time()-t0:.0f}s)", flush=True)
        out = os.path.join(HERE, "results", f"{name}.json")
        json.dump({"config": {"n_servers": N, "n_jobs": N_JOBS, "seeds": SEEDS,
                              "thetas": THETAS, "rhos": RHOS,
                              "backlog_cap": BACKLOG_CAP,
                              "pred_sha256": os.environ.get("PRED_SHA", "")},
                   "rows": rows}, open(out, "w"), indent=1)
        print(f"  wrote {out}")
