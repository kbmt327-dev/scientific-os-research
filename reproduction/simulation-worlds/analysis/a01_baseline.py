"""A01: model-free diagnostics of OBS-001 and the M/M/c baseline prediction."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load, arrival_diagnostics, mmc_sojourn_moments, summarize_sojourn

d = load(sys.argv[1] if len(sys.argv) > 1 else "data/OBS-001_baseline.csv")
m = d["meta"]
t0, t1 = m["warmup"], m["horizon"]
c = m["c"]
MU = 1.0  # nominal service rate stated by the operator

arr, dep = d["arr"], d["dep"]
inside = arr < t1 - 50  # drop the right edge: those may be censored by the horizon

print("=== observation ===")
print(json.dumps({k: m[k] for k in ("observation_level", "c", "horizon", "warmup",
                                    "requested_arrival_rate", "n_rows")}, indent=2))

print("\n=== arrival process (model-free) ===")
ad = arrival_diagnostics(arr[inside], t0, t1 - 50)
print(json.dumps(ad, indent=2))

print("\n=== sojourn times of served customers ===")
so = summarize_sojourn(arr[inside], dep[inside], t0, t1)
print(json.dumps(so, indent=2))

lam = ad["lambda_hat"]
print("\n=== M/M/c baseline prediction (lambda_hat, mu=1, c=%d) ===" % c)
pred = mmc_sojourn_moments(lam, MU, c)
print(json.dumps({k: v for k, v in pred.items() if not callable(v) and v is not None}, indent=2))

if pred.get("stable"):
    print("\n--- prediction vs observation ---")
    print(f"  W   predicted {pred['W']:.3f}   observed {so['W_mean']:.3f}   ratio {so['W_mean']/pred['W']:.2f}")
    print(f"  CV  predicted {pred['W_cv']:.3f}   observed {so['W_cv']:.3f}")

print("\n=== stationarity: sojourn mean by time decile ===")
ok = inside & ~np.isnan(dep)
w = dep[ok] - arr[ok]
a = arr[ok]
edges = np.quantile(a, np.linspace(0, 1, 11))
for i in range(10):
    sel = (a >= edges[i]) & (a < edges[i + 1] if i < 9 else a <= edges[i + 1])
    print(f"  t in [{edges[i]:7.1f},{edges[i+1]:7.1f})  n={sel.sum():5d}  mean W={w[sel].mean():7.3f}")

print("\n=== throughput balance ===")
served = int((~np.isnan(dep[inside])).sum())
print(f"  arrivals in window        : {inside.sum()}")
print(f"  with recorded departure   : {served}")
print(f"  without departure         : {inside.sum() - served}")
print(f"  arrival rate              : {lam:.4f}")
print(f"  completion rate           : {served/(t1-50-t0):.4f}")
print(f"  offered load a=lam/mu     : {lam/MU:.4f}  (c={c}, nominal rho={lam/(c*MU):.4f})")
print(f"  implied busy servers (L.L): {served/(t1-50-t0)/MU:.4f}")
