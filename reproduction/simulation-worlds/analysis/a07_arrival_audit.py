"""A07: audit of the Q6 'over-dispersion' finding.

A06 binned with np.arange(t0, t1+w, w) while the data stopped short of t1.  A
ragged final bin inflates the dispersion index by roughly (mean count)/(n bins),
which is large exactly at the wide bins where the 'effect' appeared.  This
script redoes the test with complete bins only and calibrates it against an
empirical homogeneous-Poisson null instead of the asymptotic formula.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from obs_tools import load

FILES = [("OBS-002", "data/OBS-002_level3.csv"),
         ("OBS-003", "data/OBS-003_lam1.6_c4.csv"),
         ("OBS-004", "data/OBS-004_lam1.2_c3.csv")]

rng = np.random.default_rng(20260913)


def dispersion(ep, t0, t_end, w):
    n_bins = int((t_end - t0) // w)
    if n_bins < 8:
        return None, 0
    edges = t0 + w * np.arange(n_bins + 1)
    cnt, _ = np.histogram(ep, bins=edges)
    return cnt.var() / cnt.mean(), n_bins


for name, path in FILES:
    d = load(path)
    m = d["meta"]
    t0 = m["warmup"]
    arr = d["arr"]
    ep = np.unique(np.round(arr, 6))
    t_end = ep.max()
    rate = len(ep) / (t_end - t0)
    print("=" * 70)
    print(f"{name}: epochs={len(ep)}  window=[{t0:.0f},{t_end:.1f}]  epoch rate={rate:.4f}")
    print(f"  {'bin':>5s} {'n_bins':>7s} {'ID':>7s} {'null mean':>10s} {'null 95%':>16s} {'emp p':>8s}")
    for w in (5, 10, 20, 40, 80, 160, 320):
        idc, nb = dispersion(ep, t0, t_end, w)
        if idc is None:
            continue
        # empirical null: homogeneous Poisson with the same epoch rate and window
        null = []
        for _ in range(400):
            n = rng.poisson(rate * (t_end - t0))
            sim = rng.uniform(t0, t_end, n)
            v, _ = dispersion(sim, t0, t_end, w)
            null.append(v)
        null = np.array(null)
        p = float((null >= idc).mean())
        print(f"  {w:5d} {nb:7d} {idc:7.3f} {null.mean():10.3f} "
              f"[{np.quantile(null,0.025):6.3f},{np.quantile(null,0.975):6.3f}] {p:8.3f}")

    # ragged-bin demonstration on the same data
    t1 = m["horizon"]
    w = 160
    nb_full = int((t_end - t0) // w)
    edges_bad = np.arange(t0, t1 + w, w)
    cnt_bad, _ = np.histogram(ep, bins=edges_bad)
    idc_bad = cnt_bad.var() / cnt_bad.mean()
    idc_good, _ = dispersion(ep, t0, t_end, w)
    print(f"  [artifact check w=160] ragged-bin ID={idc_bad:.3f} "
          f"(last bins hold {cnt_bad[-2:].tolist()} vs mean {cnt_bad.mean():.1f})"
          f"   complete-bin ID={idc_good:.3f}")
