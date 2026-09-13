"""A06: evaluate the sealed PRED-002 against OBS-003 and OBS-004."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load, mmc_sojourn_moments

pred = json.loads(Path("predictions/PRED-002.json").read_text(encoding="utf-8"))
POOL = pred["candidate_model_M3"]["server_pool"]

for entry in pred["experiments_requested"]:
    name = entry["id"]
    path = {"OBS-003": "data/OBS-003_lam1.6_c4.csv",
            "OBS-004": "data/OBS-004_lam1.2_c3.csv"}[name]
    d = load(path)
    m = d["meta"]
    c, t0, t1 = m["c"], m["warmup"], m["horizon"]
    T = t1 - t0
    arr, dep, start, srv, reason = d["arr"], d["dep"], d["start"], d["server"], d["reason"]
    served = reason == "served"
    W = dep[served] - arr[served]
    Wq = start[served] - arr[served]
    sid = srv[served].astype(int)
    S = dep[served] - start[served]

    print("=" * 78)
    print(f"{name}: lambda={m['requested_arrival_rate']} c={c}  "
          f"predicted rho={entry['predicted_rho']:.3f}")
    print(f"  exit reasons: {dict(Counter(reason.tolist()))}")

    # Q1/Q2 stability
    edges = np.quantile(arr[served], np.linspace(0, 1, 11))
    dec = [W[(arr[served] >= edges[i]) & (arr[served] <= edges[i + 1])].mean() for i in range(10)]
    slope = np.polyfit(np.arange(10), dec, 1)[0]
    print(f"  W by decile: {np.round(dec,2).tolist()}")
    print(f"  trend per decile = {slope:+.4f}  -> "
          f"{'STABLE' if abs(slope) < 0.15 * np.mean(dec) else 'GROWING'}")
    lam_hat = (arr < t1 - 50).sum() / (t1 - 50 - t0)
    print(f"  arrival rate {lam_hat:.4f}   throughput {served.sum()/T:.4f}")

    obs = {"W_mean": W.mean(), "Wq_mean": Wq.mean(),
           "P_wait": float((Wq > 1e-9).mean()),
           "W_q90": float(np.quantile(W, 0.9)), "W_q99": float(np.quantile(W, 0.99)),
           "throughput": served.sum() / T}
    print("\n  --- predictive check (95% intervals from 40 replicates of M3) ---")
    print(f"  {'stat':10s} {'observed':>10s} | "
          f"{'fastest-idle':>26s} | {'random-idle':>26s}")
    for k in ("throughput", "W_mean", "Wq_mean", "P_wait", "W_q90", "W_q99"):
        line = f"  {k:10s} {obs[k]:10.3f} | "
        for pol in ("fastest", "random"):
            r = entry["by_policy"][pol][k]
            inside = r["lo95"] <= obs[k] <= r["hi95"]
            line += f"{r['mean']:7.3f} [{r['lo95']:6.3f},{r['hi95']:6.3f}]{'OK' if inside else ' X'} | "
        print(line)

    print("\n  --- per-server utilisation (assignment-policy discriminator) ---")
    util = np.array([S[sid == i].sum() for i in range(c)]) / T
    print(f"  observed : {np.round(util,4).tolist()}")
    for pol in ("fastest", "random"):
        u = entry["by_policy"][pol]["util"]
        hit = [u["lo95"][i] <= util[i] <= u["hi95"][i] for i in range(c)]
        print(f"  {pol:8s} : {[round(x,4) for x in u['mean']]}  inside95={hit}")

    print("\n  --- Q3: per-server service rates vs the OBS-002 pool ---")
    for i in range(c):
        si = S[sid == i]
        rate = len(si) / si.sum()
        lo, hi = stats.chi2.ppf([0.025, 0.975], 2 * len(si)) / (2 * si.sum())
        ok = lo <= POOL[i] <= hi
        print(f"    server {i}: rate={rate:.4f} 95%CI[{lo:.4f},{hi:.4f}]  "
              f"pool={POOL[i]:.4f}  {'OK' if ok else 'MISMATCH'}   CV={si.std()/si.mean():.3f}")
    print(f"    capacity observed = {sum(len(S[sid==i])/S[sid==i].sum() for i in range(c)):.4f}"
          f"   predicted = {entry['fitted_capacity']:.4f}")

    print("\n  --- Q5: arrival process ---")
    ep = np.unique(np.round(arr[arr < t1 - 50], 6))
    g = np.diff(ep)
    _, cnts = np.unique(np.round(arr[arr < t1 - 50], 6), return_counts=True)
    ks = stats.kstest(g, "expon", args=(0, g.mean()))
    print(f"    mean batch={cnts.mean():.4f}  var={cnts.var():.4f}  "
          f"epoch gap CV={g.std()/g.mean():.4f}  KS(exp) p={ks.pvalue:.3f}")

    print("\n  --- Q6: dispersion index of epoch counts by bin width ---")
    for w in (20, 40, 80, 160):
        e2 = np.arange(t0, t1 + w, w)
        cnt, _ = np.histogram(ep, bins=e2)
        idc = cnt.var() / cnt.mean()
        se = np.sqrt(2.0 / (len(cnt) - 1))
        print(f"    bin={w:4d}  ID={idc:6.3f}  z={(idc-1)/se:+6.2f}")

    print("\n  --- baseline M/M/c with the nominal mu=1, for comparison ---")
    b = mmc_sojourn_moments(lam_hat, 1.0, c)
    if b.get("stable"):
        print(f"    M/M/{c} predicts W={b['W']:.3f}, P(wait)={b['P_wait']:.3f}; "
              f"observed W={obs['W_mean']:.3f}  -> factor {obs['W_mean']/b['W']:.2f}")
    else:
        print(f"    M/M/{c} says rho={b['rho']:.3f} (unstable)")
    print()
