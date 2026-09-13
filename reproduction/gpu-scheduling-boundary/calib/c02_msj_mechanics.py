"""C2: MSJ mechanics under no friction (sigma = 0, c_pre = 0).

Checks that are actually valid in a stable system:
  (a) Little's law: mean_backlog ~= lam * E[T], per policy.
  (b) Work conservation: utilization equals the EMPIRICAL offered load and is
      the same for every stable policy. (An earlier version of this file checked
      "FCFS shows lower utilization than rho", which is wrong: in a stable
      system every policy consumes the same server-time. FCFS's capacity waste
      shows up in the stability region, not in utilization. See c03.)
  (c) Per-need-class response time, to expose starvation of large gang jobs.
The no-friction ordering of mean JCT is reported as an observation, not as a
pass/fail check: theory only claims heavy-traffic optimality (see c03).
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload, expected_need
from sim.cluster import simulate

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 40_000))
SEEDS = [11, 12, 13]
POLICIES = ["fcfs", "easy_backfill", "srpt_np", "srpt", "sf_srpt", "sf_fcfs"]
RHOS = [float(x) for x in os.environ.get("RHOS", "0.7,0.9").split(",")]

rows = []
for rho in RHOS:
    for pol in POLICIES:
        res = []
        t0 = time.time()
        for s in SEEDS:
            jobs, lam = make_workload(N_JOBS, rho, N, seed=s)
            m = simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0)
            # empirical offered load of the measured window
            meas = [j for j in jobs if j.jid >= int(len(jobs) * 0.2)]
            work = sum(j.need * j.size for j in meas)
            span = jobs[-1].arrival - meas[0].arrival
            m["rho_emp"] = work / (N * span)
            m["util_over_rho_emp"] = m["utilization"] / m["rho_emp"]
            m["little_ratio"] = m["mean_backlog"] / (lam * m["mean_jct"])
            res.append(m)
        agg = {k: float(np.mean([r[k] for r in res]))
               for k in ["mean_jct", "p99_jct", "mean_slowdown", "utilization",
                         "rho_emp", "util_over_rho_emp", "completion_frac",
                         "min_flow_balance", "preempts_per_job",
                         "little_ratio"]}
        agg["jct_se"] = float(np.std([r["mean_jct"] for r in res], ddof=1) / np.sqrt(len(res)))
        agg["unstable"] = any(r["unstable"] for r in res)
        agg["jct_by_need"] = {k: float(np.mean([r["jct_by_need"].get(k, np.nan) for r in res]))
                              for k in res[0]["jct_by_need"]}
        agg.update(rho=rho, policy=pol, secs=round(time.time() - t0, 1))
        rows.append(agg)
        need_str = " ".join(f"k{k}:{v:.2f}" for k, v in agg["jct_by_need"].items())
        print(f"rho={rho} {pol:<14} E[T]={agg['mean_jct']:>8.3f}+-{agg['jct_se']:.3f} "
              f"P99={agg['p99_jct']:>8.2f} util/rho_emp={agg['util_over_rho_emp']:.4f} "
              f"little={agg['little_ratio']:.3f} pre/job={agg['preempts_per_job']:.2f} "
              f"unst={agg['unstable']:d} ({agg['secs']}s)\n{'':>21}{need_str}")

print(f"\nE[need]={expected_need():.3f}  N={N}  n_jobs={N_JOBS}")
checks = {}
for rho in RHOS:
    sub = {r["policy"]: r for r in rows if r["rho"] == rho}
    stable = [r for r in sub.values() if not r["unstable"]]
    checks[f"little_{rho}"] = all(abs(r["little_ratio"] - 1.0) < 0.03 for r in stable)
    checks[f"work_cons_{rho}"] = all(abs(r["util_over_rho_emp"] - 1.0) < 0.01 for r in stable)
    u = [r["utilization"] for r in stable]
    checks[f"util_equal_{rho}"] = (max(u) - min(u)) < 0.005
for k, v in checks.items():
    print(f"  {k:<20} {'PASS' if v else 'FAIL'}")
print("\nC2", "PASS" if all(checks.values()) else "CHECK FAILURES ABOVE")
json.dump({"rows": rows, "checks": checks},
          open(os.path.join(os.path.dirname(__file__), "c02_msj.json"), "w"), indent=2)
