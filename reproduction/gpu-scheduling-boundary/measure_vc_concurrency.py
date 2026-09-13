"""Locate the real Philly virtual clusters on the axis E8 identified: the
time-average number of CONCURRENTLY RUNNING jobs competing for the pool.

E8 showed r_safe is set by that count, not by the pool's size in servers, so
this is the coordinate the real trace has to be placed on.
"""
import json, os
from collections import defaultdict
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FMT = "%Y-%m-%d %H:%M:%S"
jobs = json.load(open(os.path.join(HERE, "data", "trace-data", "cluster_job_log")))

ev_jobs, ev_gpus, ks = defaultdict(list), defaultdict(list), defaultdict(list)
for j in jobs:
    att = [a for a in j.get("attempts", []) if a.get("detail")]
    if not att:
        continue
    a = att[0]
    k = sum(len(d.get("gpus", [])) for d in a["detail"])
    if k <= 0:
        continue
    try:
        t0 = datetime.strptime(a["start_time"], FMT).timestamp()
        t1 = datetime.strptime(a["end_time"], FMT).timestamp()
    except (TypeError, ValueError):
        continue
    if t1 < t0:
        continue
    vc = j.get("vc")
    ev_jobs[vc] += [(t0, 1), (t1, -1)]
    ev_gpus[vc] += [(t0, k), (t1, -k)]
    ks[vc].append(k)


def timeavg(events):
    events.sort()
    cur, vals, durs, prev = 0, [], [], events[0][0]
    for t, d in events:
        if t > prev:
            vals.append(cur)
            durs.append(t - prev)
            prev = t
        cur += d
    if not vals:
        return float("nan"), float("nan")
    v = np.asarray(vals, float)
    w = np.asarray(durs, float)
    busy = w[v > 0].sum()
    mean_busy = float((v[v > 0] * w[v > 0]).sum() / busy) if busy > 0 else float("nan")
    return mean_busy, float(v.max())


print("Philly virtual clusters placed on the concurrency axis")
print("(mean concurrent jobs is averaged over times when the VC is non-empty)\n")
print(f"{'vc':>8}{'jobs':>9}{'mean concurrent':>17}{'peak':>7}"
      f"{'peak GPUs':>11}{'max k':>7}{'max k/peak':>12}")
rows = []
for vc in sorted(ev_jobs, key=lambda v: -len(ks[v])):
    if len(ks[vc]) < 500:
        continue
    mc, pk = timeavg(list(ev_jobs[vc]))
    mg, pg = timeavg(list(ev_gpus[vc]))
    a = np.asarray(ks[vc])
    rows.append({"vc": vc, "n_jobs": len(a), "mean_concurrent_jobs": mc,
                 "peak_concurrent_jobs": pk, "peak_gpus": pg,
                 "max_k": int(a.max()), "max_k_over_peak": float(a.max() / pg)})
    print(f"{vc:>8}{len(a):>9,}{mc:>17.1f}{pk:>7.0f}{pg:>11.0f}"
          f"{a.max():>7}{a.max() / pg:>12.2f}")

json.dump(rows, open(os.path.join(HERE, "results", "E8_philly_concurrency.json"),
                     "w"), indent=1)
mc = [r["mean_concurrent_jobs"] for r in rows]
print(f"\nrange of mean concurrent jobs across VCs: {min(mc):.1f} - {max(mc):.1f}")
print("E8 measured r_safe = 0.625 at a concurrency of 28.5 running jobs and")
print("r_safe = 0.5 once concurrency reached ~170.")
