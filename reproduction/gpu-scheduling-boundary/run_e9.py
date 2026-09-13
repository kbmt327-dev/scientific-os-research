"""E9: measure r_safe at the concurrency where the real cluster actually sits.

EP-0006 showed r_safe is set by the number of concurrently running jobs and
measured it at 28.5, 54.2, 99.0, 168.5. Philly's 11cb48 -- the one real virtual
cluster whose largest job is a big fraction of its pool (0.59) -- runs at a
concurrency of 10.2, below everything measured. v6 places it on the safe side
by extrapolation. This turns that into a measurement.

Pool fixed at N=256; concurrency is swept by coarsening the background:
background = {s, 2s, 4s, 8s} with theta=0.4 weights.

Predictions sealed in predictions/PRED-008.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N = 256
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
S_VALUES = [1, 2, 4, 8, 12, 16]
RATIOS = [0.5, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
P_M = 0.002
RHO = 0.85
POLICY = "srpt"
SEEDS = [601, 602, 603, 604]
THETA = 0.4
KEEP = ["mean_jct", "utilization", "rho_emp", "mean_backlog", "mean_running",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance"]
HERE = os.path.dirname(os.path.abspath(__file__))


def mix(s, m, p_m=P_M, theta=THETA):
    bg = [s, 2 * s, 4 * s, 8 * s]
    w = np.array([theta ** i for i in range(len(bg))], dtype=float)
    w = w / w.sum() * (1.0 - p_m)
    if m in bg:
        probs = list(w)
        probs[bg.index(m)] += p_m
        return tuple(bg), tuple(probs)
    return tuple(bg) + (m,), tuple(w) + (p_m,)


def one(task):
    s, m, seed = task
    needs, probs = mix(s, m)
    jobs, lam = make_workload(N_JOBS, RHO, N, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, N, POLICY, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=60_000)
    rec = {k: sim[k] for k in KEEP}
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec.update(s=s, n_servers=N, m=m, ratio=round(m / N, 4), rho=RHO,
               policy=POLICY, seed=seed, n_jobs=N_JOBS, lam=lam,
               background=[s, 2 * s, 4 * s, 8 * s],
               fb_m=fb.get(m, fb.get(str(m))),
               jct_m=jb.get(m, jb.get(str(m))),
               jct_bg_small=jb.get(s, jb.get(str(s))),
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = [(s, int(round(N * r)), seed)
             for s in S_VALUES for r in RATIOS for seed in SEEDS]
    print(f"{len(tasks)} runs   workers={workers}   N={N}")
    for s in S_VALUES:
        bg = [s, 2 * s, 4 * s, 8 * s]
        w = np.array([THETA ** i for i in range(4)])
        w = w / w.sum()
        ek = float(np.dot(bg, w))
        print(f"  s={s:>3}  background={bg}  E[k_bg]={ek:5.1f}  "
              f"expected concurrency ~{RHO * N / ek:5.1f}")

    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 20 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E9.json")
    json.dump({"config": {"n_servers": N, "n_jobs": N_JOBS, "s_values": S_VALUES,
                          "ratios": RATIOS, "p_m": P_M, "rho": RHO,
                          "policy": POLICY, "seeds": SEEDS, "theta": THETA,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
