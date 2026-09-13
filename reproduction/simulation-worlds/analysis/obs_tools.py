"""Observation loading and model-free diagnostics (no access to the world truth)."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def load(path: str | Path):
    path = Path(path)
    meta = json.loads(path.with_suffix(".meta.json").read_text(encoding="utf-8"))
    raw = [l.split(",") for l in path.read_text(encoding="utf-8").strip().split("\n")]
    head, rows = raw[0], raw[1:]
    col = {name: i for i, name in enumerate(head)}

    def num(r, name):
        if name not in col:
            return math.nan
        v = r[col[name]]
        return float(v) if v else math.nan

    d = {
        "id": np.array([int(r[col["customer_id"]]) for r in rows]),
        "arr": np.array([num(r, "arrival_time") for r in rows]),
        "dep": np.array([num(r, "departure_time") for r in rows]),
    }
    d["start"] = np.array([num(r, "service_start_time") for r in rows]) if "service_start_time" in col else None
    d["server"] = np.array([r[col["server_id"]] if r[col["server_id"]] else "-1" for r in rows], dtype=object) if "server_id" in col else None
    d["reason"] = np.array([r[col["exit_reason"]] for r in rows], dtype=object) if "exit_reason" in col else None
    d["meta"] = meta
    return d


# --------------------------------------------------------------- arrivals
def arrival_diagnostics(arr: np.ndarray, t0: float, t1: float, bin_width: float = 5.0):
    n = len(arr)
    T = t1 - t0
    lam = n / T

    # exact ties -> batch signature
    uniq, counts = np.unique(np.round(arr, 6), return_counts=True)
    n_epochs = len(uniq)
    tie_frac = 1.0 - n_epochs / n
    batch_mean = n / n_epochs

    gaps = np.diff(uniq)
    gaps = gaps[gaps > 0]
    cv_epoch_gap = gaps.std() / gaps.mean() if len(gaps) > 2 else math.nan

    edges = np.arange(t0, t1 + bin_width, bin_width)
    cnt, _ = np.histogram(arr, bins=edges)
    idc = cnt.var() / cnt.mean() if cnt.mean() > 0 else math.nan  # index of dispersion (Poisson -> 1)
    ac1 = float(np.corrcoef(cnt[:-1], cnt[1:])[0, 1]) if len(cnt) > 3 else math.nan

    # epoch-count dispersion (removes batch-size effect)
    cnt_e, _ = np.histogram(uniq, bins=edges)
    idc_e = cnt_e.var() / cnt_e.mean() if cnt_e.mean() > 0 else math.nan
    ac1_e = float(np.corrcoef(cnt_e[:-1], cnt_e[1:])[0, 1]) if len(cnt_e) > 3 else math.nan

    return {"n": n, "T": T, "lambda_hat": lam, "n_epochs": n_epochs,
            "tie_fraction": tie_frac, "mean_batch_size": batch_mean,
            "cv_epoch_gap": cv_epoch_gap, "index_of_dispersion_customers": idc,
            "lag1_autocorr_customers": ac1, "index_of_dispersion_epochs": idc_e,
            "lag1_autocorr_epochs": ac1_e}


# --------------------------------------------------------------- M/M/c
def erlang_c(lam: float, mu: float, c: int):
    a = lam / mu
    rho = a / c
    if rho >= 1:
        return {"rho": rho, "stable": False}
    s = sum(a ** k / math.factorial(k) for k in range(c))
    last = a ** c / math.factorial(c) / (1 - rho)
    pw = last / (s + last)
    wq = pw / (c * mu - lam)
    lq = lam * wq
    return {"rho": rho, "stable": True, "P_wait": pw, "Wq": wq, "W": wq + 1 / mu,
            "Lq": lq, "L": lq + a,
            # sojourn-time distribution of M/M/c (FCFS): P(W>t)
            "sojourn_cv": None,
            "P_W_gt": lambda t: (1 - pw) * math.exp(-mu * t) + pw * (
                math.exp(-mu * t) - math.exp(-(c * mu - lam) * t)) / (1 - (c * mu - lam) / mu)
            if abs((c * mu - lam) / mu - 1) > 1e-9 else None}


def mmc_sojourn_moments(lam: float, mu: float, c: int):
    """Mean and CV of the FCFS sojourn time in M/M/c."""
    e = erlang_c(lam, mu, c)
    if not e["stable"]:
        return e
    pw, nu = e["P_wait"], c * mu - lam
    # Wq is a mixture: w.p. (1-pw) zero, w.p. pw Exp(nu)
    e_wq, e_wq2 = pw / nu, 2 * pw / nu ** 2
    e_s, e_s2 = 1 / mu, 2 / mu ** 2
    m1 = e_wq + e_s
    m2 = e_wq2 + 2 * e_wq * e_s + e_s2
    var = m2 - m1 ** 2
    return {**e, "W": m1, "W_cv": math.sqrt(var) / m1}


def summarize_sojourn(arr, dep, t0, t1):
    ok = ~np.isnan(dep)
    w = dep[ok] - arr[ok]
    return {"n_served": int(ok.sum()), "n_no_departure": int((~ok).sum()),
            "served_fraction": float(ok.mean()),
            "W_mean": float(w.mean()), "W_sd": float(w.std()),
            "W_cv": float(w.std() / w.mean()),
            "W_q": {q: float(np.quantile(w, q)) for q in (0.5, 0.9, 0.95, 0.99)},
            "W_max": float(w.max())}
