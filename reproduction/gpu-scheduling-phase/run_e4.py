"""E4: is whole-cluster starvation caused by the SUPPORT of the need
distribution containing N, and by the combination of size-based priority with
greedy work conservation?

E2 showed greedy SRPT starving the need=64 class at theta=0.4 (rho=0.7 already),
while EP-0001's trace-like mix -- which had a HIGHER mean need (3.26 vs 2.37)
but no need=64 class -- had greedy SRPT winning. That points at the support,
not the mean. Two factors are separated here:

  A. p64 sweep       weights over (1..32) keep the theta=0.4 shape and are
                     renormalised to 1-p64; p64 goes on need=64. So the support
                     gains N at an arbitrarily small probability.
  B. E[k]-matched    a mix with max need 32 whose mean need equals the
     control     p64=0.03 cell's. If starvation tracks E[k] rather than the
                     support, this control must starve too.

and the 2x2 of mechanism:

                      greedy fill        exact fill (ServerFilling)
  size priority       srpt               sf_srpt
  arrival priority    fcfs               sf_fcfs

plus easy_backfill (arrival priority + reservation) and srpt_np (size priority,
greedy, no preemption).

Predictions sealed in predictions/PRED-003.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload, mix_stats
from sim.cluster import simulate

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
HORIZON2 = 120_000
SEEDS = [301, 302, 303, 304, 305]
P64 = [0.0, 0.0005, 0.002, 0.008, 0.03]
RHOS = [0.7, 0.85]
POLICIES = ["fcfs", "easy_backfill", "srpt", "srpt_np", "sf_srpt", "sf_fcfs"]
SMALL = (1, 2, 4, 8, 16, 32)
THETA_BASE = 0.4
KEEP = ["mean_jct", "p99_jct", "mean_slowdown", "mean_wait", "max_wait",
        "utilization", "rho_emp", "util_over_rho", "mean_backlog",
        "preempts_per_job", "lost_work_frac", "completion_frac",
        "backlog_growing", "aborted_backlog", "hit_time_limit", "backlog_slope",
        "backlog_first_decile", "backlog_last_decile", "jct_by_need",
        "completion_frac_by_need", "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance",
        "starving_needs", "jct_spread_by_need"]
HERE = os.path.dirname(os.path.abspath(__file__))


def small_probs(theta):
    w = np.array([theta ** i for i in range(len(SMALL))], dtype=float)
    return w / w.sum()


def mix_p64(p64):
    """theta=0.4 shape over needs 1..32, renormalised to 1-p64, plus p64 on 64."""
    base = small_probs(THETA_BASE) * (1.0 - p64)
    return (SMALL + (64,)), tuple(base) + (p64,)


def mix_matched(target_e_need):
    """Max need 32, mean need matched to target by solving for theta."""
    def f(t):
        return float(np.dot(SMALL, small_probs(t))) - target_e_need
    t = brentq(f, 0.05, 20.0)
    return SMALL, tuple(small_probs(t)), t


def one(task):
    label, needs, probs, rho, pol, seed, n_jobs = task
    jobs, lam = make_workload(n_jobs, rho, N, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                 backlog_cap=40_000)
    rec = {k: m[k] for k in KEEP}
    rec.update(label=label, rho=rho, policy=pol, seed=seed, n_jobs=n_jobs,
               lam=lam, max_need=max(needs), secs=round(time.time() - t0, 1),
               **mix_stats(needs, probs, N))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))

    mixes = []
    for p in P64:
        needs, probs = mix_p64(p)
        mixes.append((f"p64={p}", needs, probs))
    e_target = mix_stats(*mix_p64(0.03), N)["e_need"]
    needs_m, probs_m, theta_m = mix_matched(e_target)
    mixes.append((f"matched_max32(E[k]={e_target:.3f},theta={theta_m:.3f})",
                  needs_m, probs_m))

    print("mixes:")
    for label, needs, probs in mixes:
        st = mix_stats(needs, probs, N)
        print(f"  {label:<44} E[k]={st['e_need']:.3f}  max_need={max(needs)}  "
              f"p(64)={st['p_full']:.4f}")

    tasks = [(label, needs, probs, rho, pol, s, N_JOBS)
             for label, needs, probs in mixes for rho in RHOS
             for pol in POLICIES for s in SEEDS]
    # horizon check on EVERY cell (one seed), so no verdict is left
    # unadjudicated: cells whose min flow balance falls below 0.995 are decided
    # by whether mean JCT scales with the horizon.
    tasks += [(label, needs, probs, rho, pol, 301, HORIZON2)
              for label, needs, probs in mixes for rho in RHOS
              for pol in POLICIES]
    print(f"\n{len(tasks)} runs   workers={workers}")

    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 30 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E4.json")
    json.dump({"config": {"n_servers": N, "n_jobs": N_JOBS, "horizon2": HORIZON2,
                          "seeds": SEEDS, "p64": P64, "rhos": RHOS,
                          "theta_base": THETA_BASE, "policies": POLICIES,
                          "mixes": [(l, list(n), list(map(float, p)))
                                    for l, n, p in mixes],
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
