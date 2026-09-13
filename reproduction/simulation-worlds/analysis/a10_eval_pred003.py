"""A10: evaluate PRED-003."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load

pred = json.loads(Path("predictions/PRED-003.json").read_text(encoding="utf-8"))
POOL = pred["model"]["server_pool"]

print("=== R1: eight fresh replications at lambda=1.6, c=4 ===")
Ws, Wqs = [], []
for s in range(101, 109):
    d = load(f"data/OBS-rep{s}.csv")
    served = d["reason"] == "served"
    W = d["dep"][served] - d["arr"][served]
    Wq = d["start"][served] - d["arr"][served]
    Ws.append(W.mean()); Wqs.append(Wq.mean())
    print(f"  seed {s}: W_mean={W.mean():7.3f}  Wq_mean={Wq.mean():7.3f}  n={served.sum()}")
Ws, Wqs = np.array(Ws), np.array(Wqs)
r1 = pred["predictions"][0]
lo, hi = r1["interval"]
loq, hiq = r1["interval_Wq"]
print(f"\n  mean of W_mean  = {Ws.mean():.4f}   predicted interval [{lo:.3f},{hi:.3f}]  "
      f"-> {'PASS' if lo <= Ws.mean() <= hi else 'FAIL'}")
print(f"  mean of Wq_mean = {Wqs.mean():.4f}   predicted interval [{loq:.3f},{hiq:.3f}]  "
      f"-> {'PASS' if loq <= Wqs.mean() <= hiq else 'FAIL'}")
print(f"  (OBS-003 gave W_mean=3.370; the replicate spread is sd={Ws.std(ddof=1):.3f}, "
      f"range [{Ws.min():.3f},{Ws.max():.3f}])")

print("\n=== R2: c = 6 ===")
d = load("data/OBS-013_c6.csv")
m = d["meta"]
c, T = m["c"], m["horizon"] - m["warmup"]
served = d["reason"] == "served"
S = d["dep"][served] - d["start"][served]
sid = d["server"][served].astype(int)
print(f"  exit reasons: {sorted(set(d['reason'].tolist()))}")
caps = []
for i in range(c):
    si = S[sid == i]
    rate = len(si) / si.sum()
    lo_, hi_ = stats.chi2.ppf([0.025, 0.975], 2 * len(si)) / (2 * si.sum())
    caps.append(rate)
    known = f"pool={POOL[i]:.4f} {'OK' if lo_ <= POOL[i] <= hi_ else 'MISMATCH'}" if i < 4 \
        else "declared UNKNOWN in advance"
    print(f"    server {i}: rate={rate:.4f} 95%CI[{lo_:.4f},{hi_:.4f}] "
          f"CV={si.std()/si.mean():.3f}  n={len(si):5d}  {known}")
print(f"  capacity(c=6) observed = {sum(caps):.4f}  "
      f"(known part {sum(caps[:4]):.4f} + newly measured {sum(caps[4:]):.4f})")
cvs = [S[sid == i].std() / S[sid == i].mean() for i in (4, 5)]
print(f"  new-server CVs {np.round(cvs,3).tolist()} -> "
      f"{'PASS' if all(0.92 <= x <= 1.08 for x in cvs) else 'FAIL'} (predicted [0.92,1.08])")

Wc6 = d["dep"][served] - d["arr"][served]
print(f"  observed W_mean at c=6 = {Wc6.mean():.3f}; rho = {2.0/sum(caps):.3f}")
