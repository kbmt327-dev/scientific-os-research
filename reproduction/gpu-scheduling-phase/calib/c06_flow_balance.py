"""C06: validate the per-class flow-balance instrument.

The detector used in EP-0001 (util < offered load) cannot tell a diverging
system from a long transient, and it fired on cells whose every class clearly
finished on time. Flow balance is the replacement: inside the arrival window,
a class whose queue grows completes fewer jobs than arrive.

Three checks:
  (a) a known-stable cell has min_flow_balance ~ 1 for every class
  (b) a cell where greedy SRPT starves the 64-GPU class is caught, and the
      starved class's JCT scales with the horizon while the others do not
  (c) the verdict is horizon-insensitive (same at 30k and 120k jobs)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload, geometric_mix
from sim.cluster import simulate

N = 64
FAIL = []


def run(theta, rho, pol, n_jobs, seed=201):
    needs, probs = geometric_mix(theta)
    jobs, _ = make_workload(n_jobs, rho, N, seed=seed, needs=needs, need_probs=probs)
    return simulate(jobs, N, pol, c_pre=0.0, dur_mean=1.0, t_limit_factor=2.0,
                    backlog_cap=20000)


print("horizon  policy          min_fb  starving   jct_1   jct_64  util/rho")
res = {}
for n_jobs in (30_000, 120_000):
    for pol in ("sf_srpt", "easy_backfill", "srpt"):
        m = run(0.4, 0.7, pol, n_jobs)
        res[(n_jobs, pol)] = m
        print(f"{n_jobs:>7}  {pol:<14}{m['min_flow_balance']:>7.3f}  "
              f"{str(m['starving_needs']):<10}"
              f"{m['jct_by_need'][1]:>7.2f} {m['jct_by_need'][64]:>8.1f}"
              f"{m['util_over_rho']:>10.4f}")

# (a) stable policies show flow balance ~1 and no starving class
for pol in ("sf_srpt", "easy_backfill"):
    for n_jobs in (30_000, 120_000):
        m = res[(n_jobs, pol)]
        if m["starving_needs"] or m["min_flow_balance"] < 0.85:
            FAIL.append(f"(a) {pol}@{n_jobs}: fb={m['min_flow_balance']:.3f} "
                        f"starving={m['starving_needs']}")

# (b) greedy SRPT's 64-class is caught, and its JCT scales with the horizon
for n_jobs in (30_000, 120_000):
    if 64 not in res[(n_jobs, 'srpt')]["starving_needs"]:
        FAIL.append(f"(b) srpt@{n_jobs}: 64-need class not flagged")
g = res[(120_000, 'srpt')]["jct_by_need"][64] / res[(30_000, 'srpt')]["jct_by_need"][64]
g1 = res[(120_000, 'srpt')]["jct_by_need"][1] / res[(30_000, 'srpt')]["jct_by_need"][1]
print(f"\nhorizon x4: srpt jct_64 grows {g:.2f}x, jct_1 grows {g1:.2f}x")
if g < 2.0:
    FAIL.append(f"(b) srpt jct_64 grew only {g:.2f}x over a 4x horizon")
if g1 > 1.2:
    FAIL.append(f"(b) srpt jct_1 grew {g1:.2f}x; the small class should be stable")

# (c) verdict identical at both horizons for every policy
for pol in ("sf_srpt", "easy_backfill", "srpt"):
    a = bool(res[(30_000, pol)]["starving_needs"])
    b = bool(res[(120_000, pol)]["starving_needs"])
    if a != b:
        FAIL.append(f"(c) {pol}: verdict changed with horizon ({a} -> {b})")

print("\nC06 " + ("FAIL\n  " + "\n  ".join(FAIL) if FAIL else "PASS"))
sys.exit(1 if FAIL else 0)
