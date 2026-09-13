"""E13: audit the detector the whole domain's operational numbers rest on.

Predictions and grading rules are sealed in predictions/PRED-012.json before
this script is run.

The boundary statistic has been flow balance of the largest class, measured in
one 30000-job window and thresholded at 0.9.  EP-0002 showed for this same
domain that flow-balance LEVELS are horizon dependent; the r_safe pipeline
never received that calibration.  Arm H sweeps the horizon.  The threshold and
past-result arms need no new runs and live in analyze_e13.py.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.cluster import simulate
from sim.workload import make_workload, mix_stats

N = 256
RHO = 0.85
HERE = os.path.dirname(os.path.abspath(__file__))

RATIOS = [0.5, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
E_TARGETS = {
    "C10": 12 * 2.952 / 1.624,
    "C15": 8 * 2.952 / 1.624,
    "C28": 4 * 2.952 / 1.624,
}
P_LEVELS = [0.002, 0.02]
HORIZONS = [30_000, 60_000, 120_000]
SEEDS = [901, 902, 903, 904, 905]
EASY_RATIOS = [0.5, 1.0]
EASY_P = 0.002
EASY_HORIZON = 120_000
EASY_SEEDS = [901, 902, 903]

GEOM_SUPPORT = (1, 2, 4, 8, 16, 32, 64)
KEEP = ["mean_jct", "utilization", "rho_emp", "mean_backlog", "mean_running",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance",
        "starving_needs"]


def fit_geometric(target_mean, support=GEOM_SUPPORT):
    lo, hi = 0.0, 80.0
    for _ in range(300):
        mid = (lo + hi) / 2
        w = np.asarray([mid ** i for i in range(len(support))], dtype=float)
        if float(np.dot(support, w / w.sum())) < target_mean:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    w = np.asarray([theta ** i for i in range(len(support))], dtype=float)
    return theta, tuple(w / w.sum())


def factorial_mix(e_target, ratio, p):
    """Identical construction to run_e12.py."""
    m = int(round(N * ratio))
    bg_mean = (e_target - p * m) / (1 - p)
    assert bg_mean >= 1.05, f"infeasible cell: bg_mean={bg_mean}"
    theta, bg_probs = fit_geometric(bg_mean)
    assert max(GEOM_SUPPORT) < m
    needs = GEOM_SUPPORT + (m,)
    probs = tuple((1 - p) * np.asarray(bg_probs)) + (p,)
    assert abs(float(np.dot(needs, probs)) - e_target) < 1e-9
    return needs, probs, m, bg_mean, theta


def one(task):
    arm, e_label, ratio, p, n_jobs, seed, policy = task
    e_target = E_TARGETS[e_label]
    needs, probs, m, bg_mean, theta = factorial_mix(e_target, ratio, p)
    jobs, lam = make_workload(n_jobs, RHO, N, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, N, policy, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=2 * n_jobs)
    rec = {k: sim[k] for k in KEEP}
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec.update(arm=arm, e_label=e_label, e_target=e_target, ratio=ratio, m=m,
               p=p, n_jobs=n_jobs, seed=seed, policy=policy, lam=lam,
               bg_mean=bg_mean, bg_theta=theta,
               work_share_max=p * m / e_target,
               predicted_conc=RHO * N / e_target,
               fb_m=fb.get(m, fb.get(str(m))),
               jct_m=jb.get(m, jb.get(str(m))),
               n_arr_m=sim["n_arrivals_by_need"].get(
                   m, sim["n_arrivals_by_need"].get(str(m))),
               secs=round(time.time() - t0, 1),
               **mix_stats(needs, probs, N))
    return rec


def build_tasks():
    tasks = []
    for e_label in E_TARGETS:
        for ratio in RATIOS:
            for p in P_LEVELS:
                for n_jobs in HORIZONS:
                    for seed in SEEDS:
                        tasks.append(("H", e_label, ratio, p, n_jobs, seed,
                                      "srpt"))
    for e_label in E_TARGETS:
        for ratio in EASY_RATIOS:
            for seed in EASY_SEEDS:
                tasks.append(("E", e_label, ratio, EASY_P, EASY_HORIZON, seed,
                              "easy_backfill"))
    # longest runs first so the tail does not serialise
    tasks.sort(key=lambda t: -t[4])
    return tasks


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = build_tasks()
    by_arm = {}
    for t in tasks:
        by_arm[t[0]] = by_arm.get(t[0], 0) + 1
    print(f"E13: {len(tasks)} runs {by_arm}  workers={workers}  N={N}")
    print(f"  horizons={HORIZONS}  p={P_LEVELS}  ratios={RATIOS}")
    for e_label, e in E_TARGETS.items():
        print(f"  {e_label}: E[need]={e:.4f}  "
              f"Little concurrency={RHO * N / e:.2f}")

    rows, t0 = [], time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 40 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)",
                      flush=True)

    out = os.path.join(HERE, "results", "E13.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump({"config": {
            "n_servers": N, "rho": RHO, "ratios": RATIOS,
            "e_targets": E_TARGETS, "p_levels": P_LEVELS,
            "horizons": HORIZONS, "seeds": SEEDS,
            "easy_ratios": EASY_RATIOS, "easy_p": EASY_P,
            "easy_horizon": EASY_HORIZON, "easy_seeds": EASY_SEEDS,
            "geom_support": list(GEOM_SUPPORT),
            "pred_sha256": os.environ.get("PRED_SHA", ""),
        }, "rows": rows}, handle, indent=1)
    print(f"  wrote {out}")
