"""A03: evaluate PRED-001 against OBS-002 (level 3, same run)."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load

d = load("data/OBS-002_level3.csv")
m = d["meta"]
c = m["c"]
arr, dep, start, srv, reason = d["arr"], d["dep"], d["start"], d["server"], d["reason"]
served = reason == "served"

print("=== P1: exit reasons ===")
print(" ", dict(Counter(reason.tolist())))

S = dep[served] - start[served]
print(f"\n=== P2: mean service duration = {S.mean():.4f}  (predicted 1.6435 +/- 0.05) ===")
print(f"  pooled service CV = {S.std()/S.mean():.4f}   median = {np.median(S):.4f}")

print("\n=== P3: per-server work ===")
sid = srv[served].astype(int)
T = m["horizon"] - m["warmup"]
rows = []
for i in range(c):
    sel = sid == i
    si = S[sel]
    rows.append((i, sel.sum(), sel.sum() / T, si.mean(), si.std() / si.mean()))
    print(f"  server {i}: n={sel.sum():6d}  rate={sel.sum()/T:7.4f}  "
          f"mean S={si.mean():7.4f}  CV={si.std()/si.mean():6.3f}")
counts = np.array([r[1] for r in rows], float)
chi = ((counts - counts.mean()) ** 2 / counts.mean()).sum()
p = 1 - stats.chi2.cdf(chi, c - 1)
rates = np.array([r[2] for r in rows])
print(f"  chi-square (equal servers) = {chi:.1f}, df={c-1}, p={p:.3e}")
print(f"  max/min rate ratio = {rates.max()/rates.min():.3f}")
print(f"  sum of per-server rates = {rates.sum():.4f}")

print("\n=== P4/P6: occupancy ===")
q = np.loadtxt("data/OBS-002_level3_qsamples.csv", delimiter=",", skiprows=1)
t, nw, nb = q[:, 0], q[:, 1], q[:, 2]
late = t > 1000
print(f"  n_busy == c fraction (t>1000): {(nb[late] == c).mean():.4f}")
print(f"  any sample with n_waiting>0 and n_busy<c: {int(((nw > 0) & (nb < c)).sum())}")
print(f"  final n_waiting = {nw[-1]:.0f}   max = {nw.max():.0f}")
busy_frac = []
for i in range(c):
    sel = sid == i
    busy_frac.append(S[sel].sum() / T)
print("  per-server busy fraction:", np.round(busy_frac, 4))

print("\n=== P5: service-time law, per server ===")
for i in range(c):
    si = S[sid == i]
    mu_i = 1 / si.mean()
    # exponential goodness of fit via KS on the fitted exponential
    ks = stats.kstest(si, "expon", args=(0, si.mean()))
    print(f"  server {i}: mean={si.mean():.4f} rate={mu_i:.4f} CV={si.std()/si.mean():.4f} "
          f"skew={stats.skew(si):.3f}  KS(exp) D={ks.statistic:.4f} p={ks.pvalue:.2e}")

print("\n=== extra: is service duration related to congestion at start? ===")
# queue length at each service start, from the qsample series
idx = np.searchsorted(t, start[served]) - 1
idx = np.clip(idx, 0, len(t) - 1)
qs = nw[idx]
lo, hi = qs < np.median(qs), qs >= np.median(qs)
print(f"  mean S | low backlog  = {S[lo].mean():.4f}  (n={lo.sum()})")
print(f"  mean S | high backlog = {S[hi].mean():.4f}  (n={hi.sum()})")
print(f"  Spearman(S, backlog)  = {stats.spearmanr(S, qs).statistic:+.4f}")

print("\n=== extra: normalised service times pooled across servers ===")
Z = np.concatenate([S[sid == i] / S[sid == i].mean() for i in range(c)])
print(f"  pooled normalised CV = {Z.std():.4f}  skew = {stats.skew(Z):.3f}")
ks = stats.kstest(Z, "expon", args=(0, 1.0))
print(f"  KS vs Exp(1): D={ks.statistic:.4f} p={ks.pvalue:.3e}")
for k_ in (2, 3, 4, 6):
    ksg = stats.kstest(Z, "gamma", args=(k_, 0, 1.0 / k_))
    print(f"  KS vs Erlang(k={k_}): D={ksg.statistic:.4f} p={ksg.pvalue:.3e}")
