"""C1: with every job needing exactly one server, FCFS must reproduce M/M/c.

This checks the event engine, the load calibration and the metric definitions
against a closed form before anything else is claimed.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload
from sim.cluster import simulate
from sim.analytic import mmc

C = 8
N_JOBS = 200_000
SEEDS = [1, 2, 3, 4, 5]

rows = []
for rho in [0.5, 0.7, 0.9]:
    ana = mmc(lam=rho * C, mu=1.0, c=C)
    jct, wait, util = [], [], []
    for s in SEEDS:
        jobs, lam = make_workload(N_JOBS, rho, C, seed=s,
                                  needs=(1,), need_probs=(1.0,))
        m = simulate(jobs, C, "fcfs", dur_mean=1.0)
        jct.append(m["mean_jct"]); wait.append(m["mean_wait"]); util.append(m["utilization"])
    jct = np.array(jct); wait = np.array(wait)
    se = jct.std(ddof=1) / np.sqrt(len(jct))
    rows.append({
        "rho": rho,
        "analytic_jct": ana["mean_jct"],
        "sim_jct": jct.mean(),
        "sim_jct_se": se,
        "rel_err_jct": jct.mean() / ana["mean_jct"] - 1.0,
        "analytic_wait": ana["mean_wait"],
        "sim_wait": wait.mean(),
        "rel_err_wait": wait.mean() / ana["mean_wait"] - 1.0,
        "sim_util": float(np.mean(util)),
        "z_jct": (jct.mean() - ana["mean_jct"]) / se if se > 0 else float("nan"),
    })

print(f"{'rho':>5} {'analytic E[T]':>14} {'sim E[T]':>10} {'rel err':>9} "
      f"{'z':>7} {'analytic E[W]':>14} {'sim E[W]':>10} {'rel err':>9} {'util':>7}")
for r in rows:
    print(f"{r['rho']:>5.2f} {r['analytic_jct']:>14.4f} {r['sim_jct']:>10.4f} "
          f"{r['rel_err_jct']:>+9.2%} {r['z_jct']:>+7.2f} {r['analytic_wait']:>14.4f} "
          f"{r['sim_wait']:>10.4f} {r['rel_err_wait']:>+9.2%} {r['sim_util']:>7.4f}")

ok = all(abs(r["rel_err_jct"]) < 0.01 and abs(r["z_jct"]) < 3.5 for r in rows)
print("\nC1", "PASS" if ok else "FAIL")
json.dump(rows, open(os.path.join(os.path.dirname(__file__), "c01_mmc.json"), "w"), indent=2)
