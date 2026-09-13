"""E7: does the safe job-size ratio r_safe fall with pool size?

E6 measured r_safe = 0.75 at N=64 and found the only failed prediction of
PRED-005: the onset is not a pure function of m/N. N=128 was worse than N=64 at
every matched ratio, and the gap widened with the ratio.

That matters because Philly's worst real virtual cluster runs a 128-GPU job in
a 217-GPU pool (m/N = 0.59) -- a pool more than three times larger than the N
the boundary was measured at.

Same construction as E6: a small-job background (theta=0.4 geometric shape over
needs 1..N/2) plus one large class at need = m arriving with probability p_m.

Predictions sealed in predictions/PRED-006.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N_JOBS = int(os.environ.get("N_JOBS", 30_000))
NS = [32, 64, 128, 256, 512]
RATIOS = [0.5, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
P_M = 0.002
RHO = 0.85
POLICIES = ["srpt", "easy_backfill"]
SEEDS_SMALL = [401, 402, 403, 404, 405]
SEEDS_BIG = [401, 402, 403]
THETA_BASE = 0.4
KEEP = ["mean_jct", "p99_jct", "utilization", "rho_emp", "util_over_rho",
        "mean_backlog", "completion_frac", "aborted_backlog", "hit_time_limit",
        "jct_by_need", "flow_balance_by_need", "n_arrivals_by_need",
        "min_flow_balance", "starving_needs"]
HERE = os.path.dirname(os.path.abspath(__file__))


def mix(n_servers, m, p_m=P_M, theta=THETA_BASE):
    small = [1]
    while small[-1] * 2 <= n_servers // 2:
        small.append(small[-1] * 2)
    w = np.array([theta ** i for i in range(len(small))], dtype=float)
    w = w / w.sum() * (1.0 - p_m)
    if m in small:
        probs = list(w)
        probs[small.index(m)] += p_m
        return tuple(small), tuple(probs)
    return tuple(small) + (m,), tuple(w) + (p_m,)


def one(task):
    n_servers, m, pol, seed = task
    needs, probs = mix(n_servers, m)
    jobs, lam = make_workload(N_JOBS, RHO, n_servers, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, n_servers, pol, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=60_000)
    rec = {k: sim[k] for k in KEEP}
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec.update(n_servers=n_servers, m=m, ratio=round(m / n_servers, 4),
               rho=RHO, policy=pol, seed=seed, n_jobs=N_JOBS, lam=lam,
               n_classes=len(needs),
               fb_m=fb.get(m, fb.get(str(m))),
               jct_m=jb.get(m, jb.get(str(m))),
               jct_1=jb.get(1, jb.get("1")),
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = []
    for n in NS:
        seeds = SEEDS_SMALL if n <= 128 else SEEDS_BIG
        for r in RATIOS:
            m = int(round(n * r))
            for pol in POLICIES:
                for s in seeds:
                    tasks.append((n, m, pol, s))
    # biggest pools first so the long tail starts early
    tasks.sort(key=lambda t: -t[0])
    print(f"{len(tasks)} runs   workers={workers}")

    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 20 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E7.json")
    json.dump({"config": {"n_jobs": N_JOBS, "ns": NS, "ratios": RATIOS,
                          "p_m": P_M, "rho": RHO, "policies": POLICIES,
                          "seeds_small": SEEDS_SMALL, "seeds_big": SEEDS_BIG,
                          "theta_base": THETA_BASE,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
