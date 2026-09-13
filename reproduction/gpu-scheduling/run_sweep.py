"""Experiment E1: sigma (estimate error) x c_pre (preemption cost) x need mix.

Predictions were sealed in predictions/PRED-001.json
(sha256 dd977a92c0edf7472a6190d35dab7baa22743375627ca326be354d4c4eda4b01)
before this script was run. Do not edit that file.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N = 64
RHO = float(os.environ.get("RHO", 0.85))
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
SEEDS = [int(x) for x in os.environ.get("SEEDS", "101,102,103,104,105").split(",")]
SIGMAS = [0.0, 0.5, 1.0, 2.0]
C_PRES = [0.0, 0.05, 0.2]
BACKLOG_CAP = 6000
MIXES = {
    "trace_like": ((1, 2, 4, 8, 16, 32), (0.50, 0.20, 0.15, 0.10, 0.04, 0.01)),
    "gang_heavy": ((8, 16, 32, 64), (0.10, 0.20, 0.30, 0.40)),
}
PREEMPTIVE = {"srpt": True, "sf_srpt": True, "fcfs": False, "easy_backfill": False}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "E1.json")


def one(task):
    mix, pol, sigma, c_pre, seed = task
    needs, probs = MIXES[mix]
    jobs, lam = make_workload(N_JOBS, RHO, N, seed=seed, needs=needs,
                              need_probs=probs, sigma=sigma)
    t0 = time.time()
    m = simulate(jobs, N, pol, c_pre=c_pre, dur_mean=1.0,
                 t_limit_factor=2.0, backlog_cap=BACKLOG_CAP)
    keep = ["mean_jct", "p99_jct", "mean_slowdown", "p99_jct", "mean_wait",
            "max_wait", "utilization", "rho_emp", "util_over_rho", "mean_backlog",
            "preempts_per_job", "lost_work_frac", "completion_frac",
            "backlog_growing", "aborted_backlog", "hit_time_limit",
            "backlog_slope", "backlog_first_decile", "backlog_last_decile",
            "jct_by_need", "completion_frac_by_need"]
    rec = {k: m[k] for k in keep}
    rec.update(mix=mix, policy=pol, sigma=sigma, c_pre=c_pre, seed=seed,
               lam=lam, secs=round(time.time() - t0, 1))
    return rec


def build_tasks():
    tasks = []
    for mix in MIXES:
        for pol, pre in PREEMPTIVE.items():
            for sigma in SIGMAS:
                for c_pre in (C_PRES if pre else [0.0]):
                    for seed in SEEDS:
                        tasks.append((mix, pol, sigma, c_pre, seed))
    return tasks


if __name__ == "__main__":
    tasks = build_tasks()
    print(f"{len(tasks)} runs, rho={RHO}, n_jobs={N_JOBS}, seeds={SEEDS}")
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=int(os.environ.get("WORKERS", 8))) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 20 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time()-t0:.0f}s elapsed)")
    json.dump({"config": {"rho": RHO, "n_jobs": N_JOBS, "seeds": SEEDS,
                          "sigmas": SIGMAS, "c_pres": C_PRES, "n_servers": N,
                          "backlog_cap": BACKLOG_CAP,
                          "pred_sha256": "dd977a92c0edf7472a6190d35dab7baa22743375627ca326be354d4c4eda4b01"},
               "rows": rows}, open(OUT, "w"), indent=1)
    print(f"wrote {OUT} in {time.time()-t0:.0f}s")
