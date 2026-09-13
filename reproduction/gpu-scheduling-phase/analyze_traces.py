"""E5: measure the need distribution of real GPU cluster traces and grade PRED-004.

The question EP-0003 leaves open is not "are real jobs big" but "is there a
scheduling pool size at which whole-pool jobs arrive at least as often as the
rate that produced starvation in the synthetic model" (p >= 0.0005).

Two traces:
  Alibaba PAI v2020   100K-job sample shipped with the cluster trace's simulator.
                      Gang size k = ceil(num_inst * num_gpu); num_gpu < 1 is
                      GPU sharing, so the product is the simultaneous demand.
  Microsoft Philly    cluster_job_log from msr-fiddle/philly-traces. Gang size
                      is the number of GPUs held in the job's attempt. Philly
                      also records a virtual cluster (vc) per job, which is the
                      real scheduling pool, so the pool-size question can be
                      asked directly rather than over a hypothetical grid.

Predictions sealed in predictions/PRED-004.json before any of this was run.
"""
import json, math, os, sys
from collections import Counter, defaultdict
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
THRESH = 0.0005                      # the rate that starved the class in E4
POOLS = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
FMT = "%Y-%m-%d %H:%M:%S"


def pow2(k):
    return k >= 1 and (int(k) & (int(k) - 1)) == 0


def tail(ks, n):
    ks = np.asarray(ks)
    return float((ks >= n).mean())


def critical_pool(ks):
    """Largest candidate pool size at which whole-pool jobs reach THRESH."""
    hit = [n for n in POOLS if tail(ks, n) >= THRESH]
    return max(hit) if hit else None


def geometric_tail(e_need, needs=(1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)):
    """p(k >= 64) for the synthetic geometric family matched to the same mean."""
    from scipy.optimize import brentq
    needs = np.asarray(needs, dtype=float)

    def mean_of(t):
        w = np.array([t ** i for i in range(len(needs))], dtype=float)
        return float(np.dot(needs, w / w.sum()))

    if not (mean_of(1e-3) < e_need < mean_of(50)):
        return None, None
    t = brentq(lambda x: mean_of(x) - e_need, 1e-3, 50)
    w = np.array([t ** i for i in range(len(needs))], dtype=float)
    p = w / w.sum()
    return float(p[needs >= 64].sum()), float(t)


def describe(name, ks, work, extra=None):
    ks = np.asarray(ks, dtype=float)
    work = np.asarray(work, dtype=float)
    n = len(ks)
    out = {"trace": name, "n_gpu_jobs": n, "e_need": float(ks.mean()),
           "median": float(np.median(ks)), "max": float(ks.max()),
           "p_k1": float((ks == 1).mean()),
           "p_pow2": float(np.mean([pow2(k) for k in ks])),
           "tails": {n_: tail(ks, n_) for n_ in POOLS},
           "critical_pool": critical_pool(ks)}
    big = ks >= 64
    cs = float(big.mean())
    ws = float(work[big].sum() / work.sum()) if work.sum() > 0 else float("nan")
    out["count_share_ge64"] = cs
    out["work_share_ge64"] = ws
    out["work_over_count_ge64"] = (ws / cs) if cs > 0 else float("nan")
    g64, theta = geometric_tail(out["e_need"])
    out["geom_p64_matched"] = g64
    out["geom_theta_matched"] = theta
    if extra:
        out.update(extra)

    print(f"\n=== {name} ===")
    print(f"  GPU jobs {n:,}   E[k]={out['e_need']:.3f}   median={out['median']:.0f}"
          f"   max={out['max']:.0f}")
    print(f"  P(k=1)={out['p_k1']:.4f}   P(k is power of 2)={out['p_pow2']:.4f}")
    print("  tail  " + "  ".join(f"N={n_}:{out['tails'][n_]:.5f}" for n_ in POOLS))
    print(f"  critical pool size N* = {out['critical_pool']}"
          f"   (largest N with p_N >= {THRESH})")
    print(f"  k>=64: count share {cs:.5f}, work share {ws:.4f},"
          f" ratio {out['work_over_count_ge64']:.1f}x")
    print(f"  geometric family matched to E[k]: theta={theta:.4f}"
          if theta else "  geometric family: mean out of range")
    if g64 is not None:
        print(f"  p(k>=64): real {out['tails'][64]:.5f}  vs geometric {g64:.5f}"
              f"  -> real is {'HEAVIER' if out['tails'][64] > g64 else 'lighter'}")
    return out


# ------------------------------------------------------------------ Alibaba PAI
def load_pai():
    import csv
    ks, work, n_rows, n_cpu_only = [], [], 0, 0
    with open(os.path.join(DATA, "pai_100k.csv"), newline="") as f:
        for row in csv.DictReader(f):
            n_rows += 1
            g = float(row["num_gpu"])
            if g <= 0:
                n_cpu_only += 1
                continue
            k = max(1, math.ceil(float(row["num_inst"]) * g))
            ks.append(k)
            work.append(k * float(row["duration"]))
    return ks, work, {"n_rows": n_rows, "cpu_only_share": n_cpu_only / n_rows}


# ---------------------------------------------------------------------- Philly
def load_philly():
    path = os.path.join(DATA, "trace-data", "cluster_job_log")
    jobs = json.load(open(path))
    ks, work, vc_of, n_no_attempt = [], [], [], 0
    vc_jobs = defaultdict(list)
    vc_events = defaultdict(list)
    for j in jobs:
        att = [a for a in j.get("attempts", []) if a.get("detail")]
        if not att:
            n_no_attempt += 1
            continue
        a = att[0]
        k = sum(len(d.get("gpus", [])) for d in a["detail"])
        if k <= 0:
            continue
        try:
            dur = (datetime.strptime(a["end_time"], FMT)
                   - datetime.strptime(a["start_time"], FMT)).total_seconds()
        except (TypeError, ValueError):
            dur = 0.0
        dur = max(dur, 0.0)
        ks.append(k)
        work.append(k * dur)
        vc_of.append(j.get("vc"))
        vc_jobs[j.get("vc")].append(k)
        try:
            t0 = datetime.strptime(a["start_time"], FMT).timestamp()
            vc_events[j.get("vc")].append((t0, k))
            vc_events[j.get("vc")].append((t0 + dur, -k))
        except (TypeError, ValueError):
            pass
    return ks, work, vc_of, vc_jobs, vc_events, {"n_jobs_total": len(jobs),
                                                 "n_without_attempt": n_no_attempt}


if __name__ == "__main__":
    results = {}

    pk, pw, pex = load_pai()
    results["alibaba_pai_v2020"] = describe("Alibaba PAI v2020 (100K sample)",
                                            pk, pw, pex)
    print(f"  CPU-only rows excluded: {pex['cpu_only_share']:.3f} of "
          f"{pex['n_rows']:,}")

    hk, hw, vc_of, vc_jobs, vc_events, hex_ = load_philly()
    results["philly"] = describe("Microsoft Philly (cluster_job_log)", hk, hw, hex_)
    print(f"  jobs with no attempt detail: {hex_['n_without_attempt']:,} of "
          f"{hex_['n_jobs_total']:,}")

    # ---- Philly virtual clusters: the real scheduling pools -----------------
    print("\n=== Philly virtual clusters (the actual scheduling pools) ===")
    print("pool size proxy = the largest gang ever run in that VC is a LOWER "
          "bound on its size;\nwe use the 99.9th percentile of concurrent GPU "
          "demand as an upper-ish proxy and report both.")
    print(f"\n{'vc':>8}{'jobs':>9}{'max k':>8}{'p(k>=32)':>10}{'p(k>=64)':>10}"
          f"{'p(k>=128)':>11}{'N*':>7}")
    vcs = []
    for vc, ks in sorted(vc_jobs.items(), key=lambda kv: -len(kv[1])):
        if len(ks) < 500:
            continue
        a = np.asarray(ks)
        row = {"vc": vc, "n": len(ks), "max_k": int(a.max()),
               "p32": tail(a, 32), "p64": tail(a, 64), "p128": tail(a, 128),
               "critical_pool": critical_pool(a), "e_need": float(a.mean())}
        vcs.append(row)
        print(f"{vc:>8}{row['n']:>9,}{row['max_k']:>8}{row['p32']:>10.5f}"
              f"{row['p64']:>10.5f}{row['p128']:>11.5f}"
              f"{str(row['critical_pool']):>7}")
    results["philly_vcs"] = vcs
    binding = [v for v in vcs if v["critical_pool"] and v["critical_pool"] >= 64]
    print(f"\n{len(binding)}/{len(vcs)} virtual clusters have N* >= 64")

    # ---- measured VC capacity, instead of a hypothetical pool size ---------
    # Sweep each VC's attempt intervals to get concurrent GPU occupancy. The
    # peak (and the 99th percentile) of that is a direct measurement of how big
    # the scheduling pool actually is, so "does this pool receive jobs that need
    # the whole pool" stops being hypothetical.
    print("\n=== measured VC capacity vs whole-pool job rate ===")
    print(f"{'vc':>8}{'jobs':>9}{'peak GPUs':>11}{'p99 GPUs':>10}"
          f"{'max k':>8}{'k/peak':>9}{'p(k>=peak)':>12}{'p(k>=p99)':>11}")
    cap_rows = []
    for vc, _ in sorted(vc_jobs.items(), key=lambda kv: -len(kv[1])):
        ev = vc_events.get(vc)
        if not ev or len(vc_jobs[vc]) < 500:
            continue
        ev.sort()
        cur, occ, durs = 0, [], []
        prev = ev[0][0]
        for tstamp, delta in ev:
            if tstamp > prev:
                occ.append(cur)
                durs.append(tstamp - prev)
                prev = tstamp
            cur += delta
        if not occ:
            continue
        occ = np.asarray(occ, dtype=float)
        durs = np.asarray(durs, dtype=float)
        order = np.argsort(occ)
        w = np.cumsum(durs[order]) / durs.sum()
        p99 = float(occ[order][np.searchsorted(w, 0.99)])
        peak = float(occ.max())
        a = np.asarray(vc_jobs[vc])
        row = {"vc": vc, "n": len(a), "peak_gpus": peak, "p99_gpus": p99,
               "max_k": int(a.max()), "max_k_over_peak": float(a.max() / peak),
               "p_ge_peak": tail(a, peak), "p_ge_p99": tail(a, p99)}
        cap_rows.append(row)
        print(f"{vc:>8}{row['n']:>9,}{peak:>11.0f}{p99:>10.0f}{row['max_k']:>8}"
              f"{row['max_k_over_peak']:>9.2f}{row['p_ge_peak']:>12.5f}"
              f"{row['p_ge_p99']:>11.5f}")
    results["philly_vc_capacity"] = cap_rows
    hot = [r for r in cap_rows if r["p_ge_p99"] >= THRESH]
    print(f"\n{len(hot)}/{len(cap_rows)} VCs receive jobs needing their whole "
          f"typical capacity at a rate >= {THRESH}")

    json.dump(results, open(os.path.join(HERE, "results", "E5_traces.json"), "w"),
              indent=1, default=str)
    print("\nwrote results/E5_traces.json")
