"""A02: discriminating tests that need no new observation (level-1 data only).

T1  Are the customers without a departure a FCFS backlog tail, or scattered
    abandonments?
T2  Is the completion (departure) rate constant in time, or does it fall as the
    backlog grows?  A congestion-dependent slowdown predicts a falling rate.
T3  What is the batch-size distribution at an arrival epoch?
T4  Is the backlog growth rate equal to lambda - completion rate?
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load

d = load(sys.argv[1] if len(sys.argv) > 1 else "data/OBS-001_baseline.csv")
m = d["meta"]
t0, t1 = m["warmup"], m["horizon"]
arr, dep = d["arr"], d["dep"]
missing = np.isnan(dep)

print("=== T1: where do the no-departure customers arrive? ===")
print(f"  n missing = {missing.sum()}  of {len(arr)}")
print(f"  arrival-time quantiles of MISSING : "
      f"{np.round(np.quantile(arr[missing], [0, .1, .5, .9, 1]), 1)}")
print(f"  arrival-time quantiles of SERVED  : "
      f"{np.round(np.quantile(arr[~missing], [0, .1, .5, .9, 1]), 1)}")
order = np.argsort(arr)
is_miss_sorted = missing[order]
k = is_miss_sorted.sum()
tail_purity = is_miss_sorted[-k:].mean()
print(f"  fraction of the last {k} arrivals that are missing = {tail_purity:.3f}")
print("  -> ~1.0 means a pure FCFS backlog (no abandonment); "
      "well below 1 means customers left from mid-queue.")

print("\n=== T2: completion rate over time (tests congestion-dependent slowdown) ===")
dep_ok = dep[~missing]
edges = np.arange(t0, t1 + 1e-9, (t1 - t0) / 10)
cnt, _ = np.histogram(dep_ok, bins=edges)
width = edges[1] - edges[0]
for i in range(len(cnt)):
    print(f"  depart in [{edges[i]:7.1f},{edges[i+1]:7.1f})  rate = {cnt[i]/width:6.3f}")
rates = cnt / width
sl = np.polyfit(np.arange(len(rates)), rates, 1)[0]
print(f"  linear trend per decile = {sl:+.4f}  (flat => capacity independent of backlog)")

print("\n=== T3: batch size distribution at an arrival epoch ===")
uniq, counts = np.unique(np.round(arr, 6), return_counts=True)
cc = Counter(counts.tolist())
tot = sum(cc.values())
mean_b = counts.mean()
p = 1.0 / mean_b
print(f"  epochs={tot}  mean batch={mean_b:.4f}  var={counts.var():.4f}  "
      f"(geometric on 1,2,... predicts var={(1-p)/p**2:.4f})")
print("   k   observed     geometric(p=1/mean)")
for k_ in range(1, 9):
    obs = cc.get(k_, 0) / tot
    geo = (1 - p) ** (k_ - 1) * p
    print(f"  {k_:2d}   {obs:8.4f}   {geo:8.4f}")

print("\n=== T4: backlog growth vs (lambda - completion rate) ===")
Tw = t1 - t0
lam = len(arr) / Tw
comp = (~missing).sum() / Tw
print(f"  lambda={lam:.4f}  completion rate={comp:.4f}  difference={lam-comp:.4f}")
print(f"  backlog at horizon (missing count)/T = {missing.sum()/Tw:.4f}")
print(f"  implied per-server effective service rate under saturation "
      f"= {comp/m['c']:.4f}  (nominal 1.0)")
print(f"  implied effective mean service time = {m['c']/comp:.4f}")
