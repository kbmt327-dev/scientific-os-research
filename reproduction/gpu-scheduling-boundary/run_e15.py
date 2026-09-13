"""E15: how often do big-relative jobs actually arrive in the Philly VCs?

Predictions and grading rules are sealed in predictions/PRED-014.json before
this script is run.  No simulation: this reads the trace and places 11cb48 on
the frequency axis of the EP-0012 alpha table.

The capacity and concurrency sweep is the same event walk measure_vc_concurrency
uses, so K0 can check the recount against what EP-0004 and EP-0006 recorded.
"""
import json
import os
from collections import defaultdict
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FMT = "%Y-%m-%d %H:%M:%S"
QS = [0.25, 0.40, 0.50, 0.59, 0.75, 1.00]
MIN_JOBS = 500
# EP-0012 alpha table at concurrency ~10 (N=256, rho=0.85)
ALPHA_TABLE = {0.002: 0.9182, 0.02: 0.7215}


def timeavg(events):
    """Time-average over non-empty periods, and the peak. Identical walk to
    measure_vc_concurrency.py so the recount is comparable."""
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
    mean_busy = float((v[v > 0] * w[v > 0]).sum() / busy) if busy > 0 else \
        float("nan")
    return mean_busy, float(v.max())


def main():
    jobs = json.load(open(os.path.join(HERE, "data", "trace-data",
                                       "cluster_job_log"), encoding="utf-8"))
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

    rows = []
    for vc in sorted(ev_jobs, key=lambda v: -len(ks[v])):
        if len(ks[vc]) < MIN_JOBS:
            continue
        mc, pk = timeavg(list(ev_jobs[vc]))
        mg, capacity = timeavg(list(ev_gpus[vc]))
        k = np.asarray(ks[vc])
        freq = {str(q): float((k >= q * capacity).mean()) for q in QS}
        rows.append({
            "vc": vc, "n_jobs": int(len(k)),
            "mean_concurrent_jobs": mc, "peak_concurrent_jobs": pk,
            "capacity_gpus": capacity, "mean_gpus": mg,
            "max_k": int(k.max()), "ratio_max": float(k.max() / capacity),
            "freq": freq,
            "n_at_059": int((k >= 0.59 * capacity).sum()),
        })

    print("Philly virtual clusters: size relative to the pool, and how often\n")
    print(f"{'vc':>8}{'jobs':>9}{'conc':>8}{'cap':>7}{'max k':>7}{'ratio':>8}"
          + "".join(f"{f'P(>={q})':>12}" for q in QS))
    for r in rows:
        print(f"{r['vc']:>8}{r['n_jobs']:>9,}{r['mean_concurrent_jobs']:>8.1f}"
              f"{r['capacity_gpus']:>7.0f}{r['max_k']:>7}{r['ratio_max']:>8.2f}"
              + "".join(f"{r['freq'][str(q)]:>12.6f}" for q in QS))

    target = next((r for r in rows if r["vc"] == "11cb48"), None)
    if target:
        f059 = target["freq"]["0.59"]
        near = min(ALPHA_TABLE, key=lambda p: abs(np.log(max(p, 1e-9))
                                                  - np.log(max(f059, 1e-9))))
        print(f"\n11cb48: concurrency {target['mean_concurrent_jobs']:.1f}, "
              f"ratio {target['ratio_max']:.2f}, "
              f"P(need >= 0.59*capacity) = {f059:.6f} "
              f"({target['n_at_059']} of {target['n_jobs']:,} jobs)")
        print(f"  nearest alpha-table frequency row: {near} "
              f"-> r_alpha = {ALPHA_TABLE[near]:.4f}")
        print(f"  margin at that row = {ALPHA_TABLE[near] - target['ratio_max']:.4f}")

    out = os.path.join(HERE, "results", "E15.json")
    json.dump({"config": {"qs": QS, "min_jobs": MIN_JOBS,
                          "alpha_table_conc10": ALPHA_TABLE,
                          "pred_sha256": os.environ.get("PRED_SHA", "")},
               "rows": rows}, open(out, "w", encoding="utf-8"), indent=1)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
