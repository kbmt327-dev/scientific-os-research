"""E6: where between N/2 and N does whole-pool starvation switch on?

E5 measured the real scheduling pools in the Philly trace: no virtual cluster
ever receives a job needing its whole capacity, but one VC (11cb48) runs a
128-GPU job in a 217-GPU pool, i.e. k/N = 0.59 -- inside the band EP-0003 never
tested. EP-0003 measured only k = N/2 (fed) and k = N (starved).

Design: a background of small jobs (theta=0.4 geometric shape over needs up to
N/2) plus one large class at need = m, arriving with probability p_m. Sweep m.

ServerFilling requires powers of two, so sf_srpt / sf_fcfs run only at the
power-of-two m values and are excluded from the sweep proper.

Predictions sealed in predictions/PRED-005.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N_JOBS = int(os.environ.get("N_JOBS", 30_000))
HORIZON2 = 120_000
SEEDS = [401, 402, 403, 404, 405]
P_M = 0.002
RHOS = [0.7, 0.85]
POLICIES = ["fcfs", "easy_backfill", "srpt", "srpt_np"]
SF_POLICIES = ["sf_srpt", "sf_fcfs"]
RATIOS = [0.5, 0.531, 0.563, 0.594, 0.625, 0.688, 0.75, 0.875, 1.0]
THETA_BASE = 0.4
KEEP = ["mean_jct", "p99_jct", "mean_wait", "utilization", "rho_emp",
        "util_over_rho", "mean_backlog", "preempts_per_job", "completion_frac",
        "aborted_backlog", "hit_time_limit", "jct_by_need",
        "completion_frac_by_need", "flow_balance_by_need", "n_arrivals_by_need",
        "min_flow_balance", "starving_needs"]
HERE = os.path.dirname(os.path.abspath(__file__))


def mix(n_servers, m, p_m=P_M, theta=THETA_BASE):
    """Small-job background over needs 1..N/2 plus one large class at m."""
    small = [1]
    while small[-1] * 2 <= n_servers // 2:
        small.append(small[-1] * 2)
    w = np.array([theta ** i for i in range(len(small))], dtype=float)
    w = w / w.sum() * (1.0 - p_m)
    if m in small:                      # m coincides with a background class
        probs = list(w)
        probs[small.index(m)] += p_m
        return tuple(small), tuple(probs)
    return tuple(small) + (m,), tuple(w) + (p_m,)


def one(task):
    n_servers, m, rho, pol, seed, n_jobs = task
    needs, probs = mix(n_servers, m)
    jobs, lam = make_workload(n_jobs, rho, n_servers, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, n_servers, pol, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=40_000)
    rec = {k: sim[k] for k in KEEP}
    fb = sim["flow_balance_by_need"]
    jb = sim["jct_by_need"]
    rec.update(n_servers=n_servers, m=m, ratio=round(m / n_servers, 3), rho=rho,
               policy=pol, seed=seed, n_jobs=n_jobs, lam=lam,
               fb_m=fb.get(m, fb.get(str(m))),
               jct_m=jb.get(m, jb.get(str(m))),
               jct_1=jb.get(1, jb.get("1")),
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = []
    # main sweep at N=64
    for r in RATIOS:
        m = int(round(64 * r))
        for rho in RHOS:
            for pol in POLICIES:
                for s in SEEDS:
                    tasks.append((64, m, rho, pol, s, N_JOBS))
            tasks.append((64, m, rho, POLICIES[2], 401, HORIZON2))
            tasks.append((64, m, rho, POLICIES[1], 401, HORIZON2))
    # ServerFilling only where the algorithm is applicable
    for m in (32, 64):
        for rho in RHOS:
            for pol in SF_POLICIES:
                for s in SEEDS:
                    tasks.append((64, m, rho, pol, s, N_JOBS))
    # scale check at N=128, greedy SRPT only, matched ratios
    for r in RATIOS:
        m = int(round(128 * r))
        for s in SEEDS[:3]:
            tasks.append((128, m, 0.85, "srpt", s, N_JOBS))

    print(f"{len(tasks)} runs   workers={workers}")
    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 40 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E6.json")
    json.dump({"config": {"n_jobs": N_JOBS, "horizon2": HORIZON2, "seeds": SEEDS,
                          "p_m": P_M, "ratios": RATIOS, "rhos": RHOS,
                          "policies": POLICIES, "sf_policies": SF_POLICIES,
                          "theta_base": THETA_BASE,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
