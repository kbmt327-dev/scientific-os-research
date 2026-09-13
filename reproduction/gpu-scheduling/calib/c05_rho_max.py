"""C5: rho_max per policy per need mix, measured directly as saturated throughput.

Offer every job at t=0 and measure utilization while the queue is non-empty.
That utilization IS the policy's maximum sustainable load. Measuring rho_max
this way costs one run per cell instead of a scan over rho, and it does not
depend on an instability detector.

Then cross-check: at rho just below and just above the measured rho_max, an
open-arrival run should be stable and unstable respectively.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sim.workload import make_workload
from sim.cluster import simulate

N = 64
N_SAT = int(os.environ.get("N_SAT", 6000))
N_JOBS = int(os.environ.get("N_JOBS", 20_000))
SEEDS = [41, 42, 43]
POLICIES = ["fcfs", "easy_backfill", "srpt_np", "srpt", "sf_srpt", "sf_fcfs"]
MIXES = {
    "trace_like": ((1, 2, 4, 8, 16, 32), (0.50, 0.20, 0.15, 0.10, 0.04, 0.01)),
    "balanced": ((1, 2, 4, 8, 16, 32), (1 / 6,) * 6),
    "gang_heavy": ((8, 16, 32, 64), (0.10, 0.20, 0.30, 0.40)),
}

rho_max = {}
print("saturated throughput = rho_max")
for mix, (needs, probs) in MIXES.items():
    for pol in POLICIES:
        u = []
        for s in SEEDS:
            jobs, _ = make_workload(N_SAT, 0.9, N, seed=s, needs=needs, need_probs=probs)
            for j in jobs:
                j.arrival = 0.0
            m = simulate(jobs, N, pol, warmup_frac=0.0, t_limit_factor=1e9,
                         saturated=True)
            u.append(m["utilization"])
        rho_max[(mix, pol)] = float(np.mean(u))
        print(f"  {mix:<12} {pol:<14} rho_max={np.mean(u):.4f} (sd {np.std(u):.4f})")

print("\ncross-check with open arrivals (util/rho < 0.995 => detected unstable)")
rows = []
for mix, (needs, probs) in MIXES.items():
    for pol in POLICIES:
        rm = rho_max[(mix, pol)]
        for tag, rho in [("below", max(0.5, rm - 0.04)), ("above", min(0.999, rm + 0.03))]:
            if tag == "above" and rm > 0.985:
                continue                      # no headroom to test above
            flags, ur = [], []
            for s in SEEDS[:2]:
                jobs, _ = make_workload(N_JOBS, rho, N, seed=s,
                                        needs=needs, need_probs=probs)
                m = simulate(jobs, N, pol, t_limit_factor=2.0, backlog_cap=4000)
                flags.append(m["unstable"])
                ur.append(m["util_over_rho"])
            ok = (tag == "below" and not any(flags)) or (tag == "above" and all(flags))
            rows.append({"mix": mix, "policy": pol, "tag": tag, "rho": rho,
                         "rho_max": rm, "unstable": sum(flags), "util_over_rho": float(np.mean(ur)),
                         "as_expected": ok})
            print(f"  {mix:<12} {pol:<14} {tag:<5} rho={rho:.3f} (rho_max={rm:.3f}) "
                  f"unstable={sum(flags)}/{len(flags)} util/rho={np.mean(ur):.4f} "
                  f"{'OK' if ok else 'MISMATCH'}")

bad = [r for r in rows if not r["as_expected"]]
print(f"\nC5 {'PASS' if not bad else f'{len(bad)} mismatches'}")
json.dump({"rho_max": {f"{k[0]}|{k[1]}": v for k, v in rho_max.items()}, "rows": rows},
          open(os.path.join(os.path.dirname(__file__), "c05_rho_max.json"), "w"), indent=2)
