"""C3: the sharp known results — stability region and heavy-traffic ordering.

Theory (Grosof et al.): in the MSJ model FCFS wastes capacity, so its stability
region is strictly smaller than rho < 1, while ServerFilling-SRPT is
heavy-traffic optimal for mean response time. So as rho -> 1 we must see
  (a) FCFS destabilise at some rho_max < 1 while ServerFilling stays stable, and
  (b) ServerFilling-SRPT overtake greedy SRPT in mean JCT.
If (b) never happens, either the implementation is wrong or the effect is
distribution-dependent; that distinction has to be settled before any sweep.

No friction here: sigma = 0, c_pre = 0.
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload
from sim.cluster import simulate

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
SEEDS = [int(x) for x in os.environ.get("SEEDS", "21,22,23").split(",")]
POLICIES = os.environ.get("POLICIES", "fcfs,easy_backfill,srpt,sf_srpt,sf_fcfs").split(",")
RHOS = [float(x) for x in os.environ.get("RHOS", "0.90,0.94,0.96,0.97,0.98,0.99").split(",")]
BACKLOG_CAP = 3000

rows = []
for rho in RHOS:
    for pol in POLICIES:
        res, t0 = [], time.time()
        for s in SEEDS:
            jobs, lam = make_workload(N_JOBS, rho, N, seed=s)
            m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0,
                         t_limit_factor=2.0, backlog_cap=BACKLOG_CAP)
            res.append(m)
        n_unstable = sum(r["unstable"] for r in res)
        stable = [r for r in res if not r["unstable"]]
        row = {
            "rho": rho, "policy": pol, "n_unstable": n_unstable, "n_seeds": len(res),
            "mean_jct": float(np.mean([r["mean_jct"] for r in stable])) if stable else float("nan"),
            "jct_se": float(np.std([r["mean_jct"] for r in stable], ddof=1) / np.sqrt(len(stable)))
                      if len(stable) > 1 else float("nan"),
            "p99_jct": float(np.mean([r["p99_jct"] for r in stable])) if stable else float("nan"),
            "mean_backlog": float(np.mean([r["mean_backlog"] for r in stable])) if stable else float("nan"),
            "drift": float(np.mean([r["drift_ratio"] for r in res])),
            "completion_frac": float(np.mean([r["completion_frac"] for r in res])),
            "preempts_per_job": float(np.mean([r["preempts_per_job"] for r in res])),
            "jct_k32": float(np.mean([r["jct_by_need"].get(32, np.nan) for r in stable])) if stable else float("nan"),
            "jct_k1": float(np.mean([r["jct_by_need"].get(1, np.nan) for r in stable])) if stable else float("nan"),
            "secs": round(time.time() - t0, 1),
        }
        rows.append(row)
        print(f"rho={rho:.2f} {pol:<14} unstable={n_unstable}/{len(res)} "
              f"E[T]={row['mean_jct']:>8.3f} P99={row['p99_jct']:>8.2f} "
              f"k1={row['jct_k1']:>7.3f} k32={row['jct_k32']:>8.3f} "
              f"L={row['mean_backlog']:>7.1f} done={row['completion_frac']:.3f} "
              f"pre/job={row['preempts_per_job']:.2f} ({row['secs']}s)")

print("\nrho_max (largest rho with every seed stable):")
for pol in POLICIES:
    ok = [r["rho"] for r in rows if r["policy"] == pol and r["n_unstable"] == 0]
    print(f"  {pol:<14} {max(ok) if ok else 'none':}")

print("\nsf_srpt vs srpt (mean JCT ratio, <1 means ServerFilling wins):")
for rho in RHOS:
    a = next((r for r in rows if r["policy"] == "sf_srpt" and r["rho"] == rho), None)
    b = next((r for r in rows if r["policy"] == "srpt" and r["rho"] == rho), None)
    if a and b and a["mean_jct"] == a["mean_jct"] and b["mean_jct"] == b["mean_jct"]:
        print(f"  rho={rho:.2f}  ratio={a['mean_jct']/b['mean_jct']:.3f}")

json.dump(rows, open(os.path.join(os.path.dirname(__file__), "c03_heavy.json"), "w"), indent=2)
