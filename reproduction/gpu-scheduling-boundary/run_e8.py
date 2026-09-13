"""E8: is r_safe set by pool size, by background class count, or by the number
of concurrently running background jobs?

EP-0005 measured r_safe falling from 0.8125 (N=32) to 0.5 (N=512) and recorded
it as a pool-size effect. But the mix family confounds three things that all
grow with N: the pool size, the number of background classes (log N, because
the background is every power of two up to N/2), and the number of concurrent
background jobs (~N / E[k]).

Three arms, differing only in how the background sizes are chosen:

  A  background = every power of two 1..N/2   (baseline, reused from E7)
  B  background = {1, 2, 4, 8} for every N     class count fixed, concurrency ~N
  C  background = {N/64, N/32, N/16, N/8}      class count fixed AND relative
                                               size fixed, so concurrency is
                                               roughly constant in N

Arms B and C coincide at N=64 by construction (a built-in check).

Predictions sealed in predictions/PRED-007.json before this script was run.
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.workload import make_workload
from sim.cluster import simulate

N_JOBS = int(os.environ.get("N_JOBS", 30_000))
NS = [64, 128, 256, 512]
RATIOS = [0.5, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
P_M = 0.002
RHO = 0.85
POLICY = "srpt"
SEEDS_SMALL = [501, 502, 503, 504, 505]
SEEDS_BIG = [501, 502, 503]
THETA = 0.4
KEEP = ["mean_jct", "utilization", "rho_emp", "mean_backlog", "mean_running",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance"]
HERE = os.path.dirname(os.path.abspath(__file__))


def background(arm, n_servers):
    if arm == "B":
        return [1, 2, 4, 8]
    if arm == "C":
        return [max(1, n_servers // d) for d in (64, 32, 16, 8)]
    raise ValueError(arm)


def mix(arm, n_servers, m, p_m=P_M, theta=THETA):
    bg = background(arm, n_servers)
    w = np.array([theta ** i for i in range(len(bg))], dtype=float)
    w = w / w.sum() * (1.0 - p_m)
    if m in bg:
        probs = list(w)
        probs[bg.index(m)] += p_m
        return tuple(bg), tuple(probs)
    return tuple(bg) + (m,), tuple(w) + (p_m,)


def one(task):
    arm, n_servers, m, seed = task
    needs, probs = mix(arm, n_servers, m)
    jobs, lam = make_workload(N_JOBS, RHO, n_servers, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, n_servers, POLICY, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=60_000)
    rec = {k: sim[k] for k in KEEP}
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec.update(arm=arm, n_servers=n_servers, m=m,
               ratio=round(m / n_servers, 4), rho=RHO, policy=POLICY,
               seed=seed, n_jobs=N_JOBS, lam=lam, background=list(needs[:-1])
               if m not in background(arm, n_servers) else list(needs),
               n_classes=len(needs),
               fb_m=fb.get(m, fb.get(str(m))),
               jct_m=jb.get(m, jb.get(str(m))),
               secs=round(time.time() - t0, 1))
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = []
    for arm in ("B", "C"):
        for n in NS:
            seeds = SEEDS_SMALL if n <= 128 else SEEDS_BIG
            for r in RATIOS:
                m = int(round(n * r))
                for s in seeds:
                    tasks.append((arm, n, m, s))
    tasks.sort(key=lambda t: -t[1])
    print(f"{len(tasks)} runs   workers={workers}")
    for arm in ("B", "C"):
        print(f"  arm {arm}: " + "  ".join(
            f"N={n}:{background(arm, n)}" for n in NS))

    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 20 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)", flush=True)

    out = os.path.join(HERE, "results", "E8.json")
    json.dump({"config": {"n_jobs": N_JOBS, "ns": NS, "ratios": RATIOS,
                          "p_m": P_M, "rho": RHO, "policy": POLICY,
                          "theta": THETA, "arms": ["B", "C"],
                          "seeds_small": SEEDS_SMALL, "seeds_big": SEEDS_BIG,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w"), indent=1)
    print(f"  wrote {out}")
