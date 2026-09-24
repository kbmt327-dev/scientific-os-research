"""Experiment E18: node locality (fragmentation) x placement x policy x mix.

RQ-1 names four frictions. E1 measured size-estimate error and preemption cost,
E17 server heterogeneity. Gang/locality was never measured. This sweep does it.

Locality model: 8-GPU nodes; a gang that spans more nodes than
ceil(need / 8) runs at rate 1 / (1 + pi * excess_nodes) (penalty_mode="excess").
Job sizes are read as measured under ideal placement, so pi is the cost of
fragmentation alone and ideal placement leaves the offered load at rho.

Loads 0.6 and 0.7 sit below every c12 capacity lower bound for these policies
and mixes (smallest: gang_heavy fcfs 0.789), so the comparison does not depend
on locating a capacity boundary. Fragmentation can still push a cell over;
that is read by alpha on the 40k/80k pair and labelled three-way in
analyze_e18.py.

Predictions were sealed in predictions/PRED-017.json before this script ran.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.cluster import simulate
from sim.workload import make_workload

N = 64
NODE = 8
HORIZONS = [40_000, 80_000]
SEEDS = [1801, 1802, 1803]
RHOS = [0.6, 0.7]
PENALTIES = [0.0, 0.1, 0.3, 0.6]
PLACEMENTS = ["first_fit", "compact"]
POLICIES = ["fcfs", "easy_backfill", "srpt", "sf_srpt"]
MIXES = {
    "trace_like": ((1, 2, 4, 8, 16, 32), (0.50, 0.20, 0.15, 0.10, 0.04, 0.01)),
    "gang_heavy": ((8, 16, 32, 64), (0.10, 0.20, 0.30, 0.40)),
}
BACKLOG_CAP = 6000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "E18.json")
KEEP = ["mean_jct", "p99_jct", "mean_wait", "utilization", "rho_emp",
        "preempts_per_job", "completion_frac", "aborted_backlog",
        "hit_time_limit", "jct_by_need", "mean_gang_rate", "gang_rate_by_need",
        "n_placements", "excess_nodes_per_placement"]


def one(task):
    mix, pol, rho, pen, place, seed, horizon = task
    needs, probs = MIXES[mix]
    jobs, lam = make_workload(horizon, rho, N, seed=seed, needs=needs,
                              need_probs=probs, sigma=0.0)
    t0 = time.time()
    m = simulate(jobs, N, pol, dur_mean=1.0, t_limit_factor=2.0,
                 backlog_cap=BACKLOG_CAP, node_size=NODE,
                 cross_node_penalty=pen, placement=place,
                 penalty_mode="excess")
    rec = {k: m.get(k) for k in KEEP}
    rec.update(mix=mix, policy=pol, rho=rho, penalty=pen, placement=place,
               seed=seed, horizon=horizon, lam=lam,
               secs=round(time.time() - t0, 1))
    return rec


def build_tasks():
    return [(mix, pol, rho, pen, place, seed, h)
            for mix in MIXES for pol in POLICIES for rho in RHOS
            for pen in PENALTIES for place in PLACEMENTS
            for seed in SEEDS for h in HORIZONS]


if __name__ == "__main__":
    if os.path.exists(OUT):
        raise FileExistsError(OUT)
    tasks = build_tasks()
    # longest first so the pool does not idle on a straggler at the end
    tasks.sort(key=lambda t: (t[0] != "gang_heavy", t[1] not in ("srpt", "sf_srpt"), -t[6]))
    print(f"{len(tasks)} runs")
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=int(os.environ.get("WORKERS", 15))) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 50 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)} ({time.time() - t0:.0f}s)", flush=True)
    json.dump({"config": {"n_servers": N, "node_size": NODE, "horizons": HORIZONS,
                          "seeds": SEEDS, "rhos": RHOS, "penalties": PENALTIES,
                          "placements": PLACEMENTS, "policies": POLICIES,
                          "mixes": {k: [list(v[0]), list(v[1])] for k, v in MIXES.items()},
                          "penalty_mode": "excess", "backlog_cap": BACKLOG_CAP,
                          "pred": "PRED-017"},
               "rows": rows}, open(OUT, "w"), indent=1)
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
