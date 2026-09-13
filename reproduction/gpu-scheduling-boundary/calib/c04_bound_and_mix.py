"""C4: three decisive instrument checks.

(a) No MSJ policy may beat the resource-pooled SRPT lower bound. If one does,
    the engine or the metrics are wrong.
(b) FCFS saturated throughput: offer a huge burst and measure the utilization
    while the queue is non-empty. That number is FCFS's rho_max, and it explains
    whether FCFS's stability region is really below 1 for this need mix.
(c) Need-mix flip test: ServerFilling's advantage is that it never wastes
    servers. With a need mix dominated by 1-GPU jobs, greedy skipping wastes
    almost nothing, so the advantage should vanish. Shift the mix toward large
    gangs and ServerFilling-SRPT should overtake greedy SRPT. If it never does,
    the ServerFilling implementation is suspect.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload, Job
from sim.cluster import simulate
from sim.pooled import simulate_pooled

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 20_000))
SEEDS = [31, 32]
out = {}

# ---------------------------------------------------------------- (a) bound
print("(a) resource-pooled SRPT lower bound vs MSJ policies")
bound_rows = []
for rho in [0.90, 0.97]:
    for s in SEEDS:
        jobs, _ = make_workload(N_JOBS, rho, N, seed=s)
        lb = simulate_pooled(jobs, N)
        rec = {"rho": rho, "seed": s, "pooled_srpt": lb["mean_jct"]}
        for pol in ["fcfs", "easy_backfill", "srpt", "sf_srpt"]:
            jobs, _ = make_workload(N_JOBS, rho, N, seed=s)
            rec[pol] = simulate(jobs, N, pol, t_limit_factor=2.0,
                                backlog_cap=3000)["mean_jct"]
        bound_rows.append(rec)
        pols = " ".join(f"{p}={rec[p]:.3f}" for p in
                        ["fcfs", "easy_backfill", "srpt", "sf_srpt"])
        print(f"  rho={rho} seed={s} pooled_LB={rec['pooled_srpt']:.3f} | {pols}")
viol = [(r["rho"], r["seed"], p) for r in bound_rows
        for p in ["fcfs", "easy_backfill", "srpt", "sf_srpt"]
        if r[p] < r["pooled_srpt"] * 0.999]
print(f"  bound violations: {viol if viol else 'none'}  ->",
      "PASS" if not viol else "FAIL")
out["bound_rows"] = bound_rows
out["bound_violations"] = [list(v) for v in viol]

# ------------------------------------------------------ (b) saturated FCFS
print("\n(b) saturated throughput (all jobs present at t=0)")
sat = {}
for pol in ["fcfs", "easy_backfill", "srpt", "sf_srpt", "sf_fcfs"]:
    utils = []
    for s in SEEDS:
        jobs, _ = make_workload(4000, 0.9, N, seed=s)
        for j in jobs:            # collapse all arrivals to time 0
            j.arrival = 0.0
        m = simulate(jobs, N, pol, warmup_frac=0.0, t_limit_factor=1e9)
        # utilization over the saturated span (queue non-empty nearly throughout)
        utils.append(m["utilization"])
    sat[pol] = float(np.mean(utils))
    print(f"  {pol:<14} saturated utilization = {sat[pol]:.4f}")
out["saturated_utilization"] = sat

# ----------------------------------------------------------- (c) need mix
print("\n(c) need-mix flip test (srpt vs sf_srpt, mean JCT ratio; <1 = SF wins)")
MIXES = {
    "trace_like  1..32 (0.5,0.2,0.15,0.1,0.04,0.01)":
        ((1, 2, 4, 8, 16, 32), (0.50, 0.20, 0.15, 0.10, 0.04, 0.01)),
    "balanced    1..32 uniform":
        ((1, 2, 4, 8, 16, 32), (1 / 6,) * 6),
    "gang_heavy  8..64 (0.1,0.2,0.3,0.4)":
        ((8, 16, 32, 64), (0.10, 0.20, 0.30, 0.40)),
    "all_full    64 only":
        ((64,), (1.0,)),
}
mix_rows = []
for name, (needs, probs) in MIXES.items():
    for rho in [0.90, 0.97]:
        r = {}
        for pol in ["srpt", "sf_srpt", "fcfs"]:
            vals = []
            for s in SEEDS:
                jobs, _ = make_workload(N_JOBS, rho, N, seed=s,
                                        needs=needs, need_probs=probs)
                m = simulate(jobs, N, pol, t_limit_factor=2.0, backlog_cap=3000)
                vals.append(m["mean_jct"] if not m["unstable"] else np.nan)
            r[pol] = float(np.nanmean(vals)) if not all(np.isnan(vals)) else float("nan")
        ratio = r["sf_srpt"] / r["srpt"]
        mix_rows.append({"mix": name, "rho": rho, **r, "sf_over_srpt": ratio})
        print(f"  {name:<46} rho={rho}  srpt={r['srpt']:>8.3f} "
              f"sf_srpt={r['sf_srpt']:>8.3f} ratio={ratio:.3f} fcfs={r['fcfs']:>9.3f}")
out["mix_rows"] = mix_rows
flips = [m for m in mix_rows if m["sf_over_srpt"] < 1.0]
print(f"\n  ServerFilling wins in {len(flips)}/{len(mix_rows)} cells ->",
      "PASS (mechanism reachable)" if flips else "FAIL (never wins: implementation suspect)")

json.dump(out, open(os.path.join(os.path.dirname(__file__), "c04.json"), "w"), indent=2)
