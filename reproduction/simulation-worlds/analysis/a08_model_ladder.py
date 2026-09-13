"""A08: parsimony ladder.

All parameters are fitted on OBS-001/002 only (lambda=2.8, c=4).  OBS-003
(lambda=1.6, c=4) and OBS-004 (lambda=1.2, c=3) are out-of-sample for every
model on the ladder.

  M0  M/M/c, nominal mu = 1                       0 fitted parameters
  M1  M/M/c, fitted homogeneous mu = 0.6085       1
  M2  M^[X]/M/c, homogeneous mu, geometric batch  2
  M3t M^[X]/M/c, heterogeneous, mu_1 = mu_2       4
  M3  M^[X]/M/c, heterogeneous, 4 free rates      5
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load
from fitted_model import predictive

MU_HOM = 0.6085                              # OBS-002 throughput / c
POOL_T = [0.6930, 0.3625, 0.3625, 1.0275]    # tied
POOL_F = [0.6930, 0.3611, 0.3639, 1.0275]    # four free
BATCH = 1.9810
REPS = 60

MODELS = {
    "M0 M/M/c nominal":        dict(rates=lambda c: [1.0] * c,      batch=1.0,   k=0),
    "M1 M/M/c fitted mu":      dict(rates=lambda c: [MU_HOM] * c,   batch=1.0,   k=1),
    "M2 M^X/M/c homogeneous":  dict(rates=lambda c: [MU_HOM] * c,   batch=BATCH, k=2),
    "M3t M^X/M/c het (tied)":  dict(rates=lambda c: POOL_T[:c],     batch=BATCH, k=4),
    "M3 M^X/M/c het (4 free)": dict(rates=lambda c: POOL_F[:c],     batch=BATCH, k=5),
}

CASES = [("OBS-003", "data/OBS-003_lam1.6_c4.csv", 1.6, 4),
         ("OBS-004", "data/OBS-004_lam1.2_c3.csv", 1.2, 3)]

STATS = ["W_mean", "Wq_mean", "P_wait", "W_q90", "throughput"]

obs_all = {}
for name, path, lam, c in CASES:
    d = load(path)
    m = d["meta"]
    T = m["horizon"] - m["warmup"]
    served = d["reason"] == "served"
    W = d["dep"][served] - d["arr"][served]
    Wq = d["start"][served] - d["arr"][served]
    obs_all[name] = {"W_mean": W.mean(), "Wq_mean": Wq.mean(),
                     "P_wait": float((Wq > 1e-9).mean()),
                     "W_q90": float(np.quantile(W, 0.9)),
                     "throughput": served.sum() / T}

score = {k: {"hits": 0, "tot": 0, "relerr": []} for k in MODELS}
for name, path, lam, c in CASES:
    print("=" * 96)
    print(f"{name}: lambda={lam}, c={c}   observed: "
          + "  ".join(f"{s}={obs_all[name][s]:.3f}" for s in STATS))
    for mname, spec in MODELS.items():
        r = predictive(lam, c, spec["rates"](c), spec["batch"], 6000, 300,
                       "fastest", reps=REPS, seed0=5000)
        line = f"  {mname:26s} k={spec['k']} "
        for s in STATS:
            o = obs_all[name][s]
            pr = r[s]
            inside = pr["lo95"] <= o <= pr["hi95"]
            score[mname]["tot"] += 1
            score[mname]["hits"] += int(inside)
            score[mname]["relerr"].append(abs(pr["mean"] - o) / max(abs(o), 1e-9))
            line += f" | {s}={pr['mean']:7.3f}{'*' if inside else ' '}"
        print(line)

print("=" * 96)
print("out-of-sample summary (10 statistic-by-dataset checks per model)")
print(f"  {'model':26s} {'k':>2s} {'inside 95%':>11s} {'median |rel err|':>17s}")
for mname, spec in MODELS.items():
    s = score[mname]
    print(f"  {mname:26s} {spec['k']:2d} {s['hits']:5d}/{s['tot']:<5d} "
          f"{np.median(s['relerr']):17.3f}")
