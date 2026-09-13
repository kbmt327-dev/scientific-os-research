"""E10: place EP-0003's configuration on the concurrency axis EP-0007 found.

EP-0003 concluded that a need distribution whose support contains N starves
that class "structurally". EP-0007 showed that starvation of the m=N class is
itself a function of how many jobs compete for the pool. This re-runs EP-0003's
setting with only the background granularity changed.

Predictions sealed in predictions/PRED-009.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
RHO, P64, THETA = 0.85, 0.002, 0.4
SEEDS = [701, 702, 703, 704, 705]
POLICIES = ["srpt", "easy_backfill"]
BACKGROUNDS = {"fine": [1, 2, 4, 8, 16, 32],
               "mid": [4, 8, 16, 32],
               "coarse": [8, 16, 32]}
KEEP = ["mean_jct", "mean_running", "mean_backlog", "utilization", "rho_emp",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance"]
HERE = os.path.dirname(os.path.abspath(__file__))


def mix(bg):
    w = np.array([THETA ** i for i in range(len(bg))], dtype=float)
    w = w / w.sum() * (1.0 - P64)
    return tuple(bg) + (N,), tuple(w) + (P64,)


def one(task):
    name, pol, seed = task
    bg = BACKGROUNDS[name]
    needs, probs = mix(bg)
    jobs, lam = make_workload(N_JOBS, RHO, N, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                   backlog_cap=60_000)
    rec = {k: sim[k] for k in KEEP}
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec.update(background=name, needs=list(bg), policy=pol, seed=seed,
               n_servers=N, rho=RHO, p64=P64, lam=lam,
               fb_64=fb.get(64, fb.get("64")),
               jct_64=jb.get(64, jb.get("64")),
               jct_small=jb.get(bg[0], jb.get(str(bg[0]))),
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = [(name, pol, s) for name in BACKGROUNDS for pol in POLICIES
             for s in SEEDS]
    print(f"{len(tasks)} runs   N={N}  rho={RHO}  p64={P64}")
    for name, bg in BACKGROUNDS.items():
        w = np.array([THETA ** i for i in range(len(bg))])
        w = w / w.sum()
        print(f"  {name:>7}: {bg}  E[k_bg]={float(np.dot(bg, w)):.2f}")

    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 10 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E10.json")
    json.dump({"config": {"n_servers": N, "n_jobs": N_JOBS, "rho": RHO,
                          "p64": P64, "theta": THETA, "seeds": SEEDS,
                          "policies": POLICIES, "backgrounds": BACKGROUNDS,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
