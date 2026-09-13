"""A04: is the arrival epoch process homogeneous Poisson on long timescales?
       and: how many distinct server rates does the data actually require?"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load

d = load("data/OBS-002_level3.csv")
m = d["meta"]
t0, t1 = m["warmup"], m["horizon"]
arr = d["arr"]
epochs = np.unique(np.round(arr, 6))

print("=== epoch-count index of dispersion vs bin width ===")
print("  (homogeneous Poisson -> 1 at every width; a slow rate cycle or an")
print("   MMPP inflates it as the bin approaches the modulation timescale)")
for w in (2, 5, 10, 20, 40, 80, 160, 320):
    edges = np.arange(t0, t1 + w, w)
    cnt, _ = np.histogram(epochs, bins=edges)
    if len(cnt) < 8:
        continue
    idc = cnt.var() / cnt.mean()
    se = np.sqrt(2.0 / (len(cnt) - 1))  # sd of the dispersion index under Poisson
    print(f"  bin={w:4d}  n_bins={len(cnt):5d}  ID={idc:6.3f}  "
          f"z=({idc-1:+.3f})/{se:.3f} = {(idc-1)/se:+6.2f}")

print("\n=== epoch inter-arrival times vs Exponential ===")
g = np.diff(epochs)
print(f"  n={len(g)} mean={g.mean():.4f} CV={g.std()/g.mean():.4f}")
ks = stats.kstest(g, "expon", args=(0, g.mean()))
print(f"  KS vs Exp: D={ks.statistic:.4f} p={ks.pvalue:.3f}")
print(f"  lag-1 autocorr of gaps = {np.corrcoef(g[:-1], g[1:])[0,1]:+.4f}")

print("\n=== periodogram of epoch counts (bin=4) for a hidden arrival cycle ===")
w = 4.0
edges = np.arange(t0, t1 + w, w)
cnt, _ = np.histogram(epochs, bins=edges)
x = cnt - cnt.mean()
P = np.abs(np.fft.rfft(x)) ** 2 / len(x)
freq = np.fft.rfftfreq(len(x), d=w)
top = np.argsort(P[1:])[-6:][::-1] + 1
print("  strongest components (period, power / mean power):")
for i in top:
    print(f"    period={1/freq[i]:9.1f}  ratio={P[i]/P[1:].mean():6.2f}")
print("  white noise -> ratios around 1-10 for the top of ~700 bins")

print("\n=== how many distinct server rates? ===")
srv, dep, start, reason = d["server"], d["dep"], d["start"], d["reason"]
served = reason == "served"
S = dep[served] - start[served]
sid = srv[served].astype(int)
c = m["c"]
n = np.array([(sid == i).sum() for i in range(c)])
tot = np.array([S[sid == i].sum() for i in range(c)])  # busy time
rate = n / tot                                          # MLE of mu_i (exp service)
print("  MLE rate_i = completions_i / busy_time_i")
for i in range(c):
    lo, hi = stats.chi2.ppf([0.025, 0.975], 2 * n[i]) / (2 * tot[i])
    print(f"    server {i}: rate={rate[i]:.4f}  95% CI [{lo:.4f}, {hi:.4f}]  n={n[i]}")


def loglik(rates_by_server):
    """exponential service log-likelihood, given each server's assigned rate"""
    return sum(n[i] * np.log(rates_by_server[i]) - rates_by_server[i] * tot[i] for i in range(c))


full = loglik(rate)
# pooled model (all servers equal)
r_pool = n.sum() / tot.sum()
pooled = loglik([r_pool] * c)
# servers 1 and 2 share a rate, 0 and 3 free
r12 = (n[1] + n[2]) / (tot[1] + tot[2])
tied = loglik([rate[0], r12, r12, rate[3]])
for name, ll, k in (("4 free rates", full, 4), ("mu1 = mu2 (3 rates)", tied, 3),
                    ("all equal (1 rate)", pooled, 1)):
    aic = -2 * ll + 2 * k
    print(f"  {name:22s} loglik={ll:12.2f}  k={k}  AIC={aic:12.2f}")
print(f"  LR test mu1=mu2 : chi2={2*(full-tied):.3f}, df=1, p={1-stats.chi2.cdf(2*(full-tied),1):.3f}")
print(f"  LR test all equal: chi2={2*(full-pooled):.1f}, df=3, p={1-stats.chi2.cdf(2*(full-pooled),3):.3e}")
