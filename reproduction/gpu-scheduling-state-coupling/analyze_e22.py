"""Grade PRED-021 against results/E22.json (and, for the pooled estimate, E21.json).

Labels, cells, row statistics and P0-P5 are analyze_e21.py's functions,
unchanged; only the input file differs. Written and sealed together with
PRED-021, before E22 ran.

Added for the replication (R1-R3 in PRED-021):
  margin m = a - 0.5 * T per seed, in each decision row
  R1  P2 as sealed in PRED-020, re-graded on seeds 2201-2206 (DECISION)
  R2  pooled 12 seeds (2101-2106 from E21, 2201-2206 from E22) at (0.6, 0.2):
      one-sided 95% lower bound of mean m, t with 11 df, > 0
  R3  E22 alone: same lower bound with 5 df (reported, not a decision)
"""
import json
import math
import os
from collections import defaultdict

import analyze_e21 as base

HERE = os.path.dirname(os.path.abspath(__file__))
T95 = {5: 2.015048, 11: 1.795885}   # one-sided 95% t quantiles


def load(name):
    d = json.load(open(os.path.join(HERE, "results", name)))
    runs = defaultdict(dict)
    for r in d["rows"]:
        runs[(r["policy"], r["rho"], r["penalty"], r["arm"], r["seed"])][r["horizon"]] = r
    return d["config"], runs


def margins(row):
    if "a" not in row:
        return None
    return [x - 0.5 * t for x, t in zip(row["a"]["per_seed"], row["T"]["per_seed"])]


def lower(xs):
    s = base.summ(xs)
    return dict(s, lower95=s["mean"] - T95[len(xs) - 1] * s["se"])


if __name__ == "__main__":
    cfg, runs = load("E22.json")
    c = base.cells(cfg, runs)
    g = base.grade(cfg, runs, c)
    labels = defaultdict(int)
    for v in c.values():
        labels[v["label"]] += 1
    n = sum(labels.values())
    print("cell labels:", dict(labels), f"UNKNOWN share {labels['UNKNOWN'] / n:.3f}")
    for k in ("P0", "P1", "P2", "P3", "P4", "P5"):
        v = g[k]
        print(k, "PASS" if v["passed"] else "FAIL", "" if v.get("scored", True) else "(unscorable)")
    for k, v in g["rows"].items():
        print(k, {x: (round(v[x]["mean"], 4), round(v[x]["sd"], 4), round(v[x]["se"], 4))
                  for x in ("Q_fcfs", "Q_srpt", "Q_gap", "a", "b", "c", "T") if x in v},
              "shares", v.get("shares"))

    rep = {"R1": dict(scored=g["P2"]["scored"], passed=g["P2"]["passed"])}
    m22 = margins(g["rows"]["0.6|0.2"])
    cfg21, runs21 = load("E21.json")
    g21 = base.grade(cfg21, runs21, base.cells(cfg21, runs21))
    m21 = margins(g21["rows"]["0.6|0.2"])
    if m22 is not None and m21 is not None:
        rep["R2"] = dict(scored=True, **lower(m21 + m22))
        rep["R2"]["passed"] = rep["R2"]["lower95"] > 0
        rep["R3"] = dict(scored=True, **lower(m22))
        rep["R3"]["passed"] = rep["R3"]["lower95"] > 0
    else:
        rep["R2"] = rep["R3"] = dict(scored=False, passed=False)
    rep["margins_0.55|0.2"] = margins(g["rows"]["0.55|0.2"])
    for k in ("R1", "R2", "R3"):
        v = rep[k]
        print(k, "PASS" if v["passed"] else "FAIL", "" if v["scored"] else "(unscorable)",
              {x: round(v[x], 5) for x in ("mean", "sd", "se", "lower95") if x in v})
    print("margins (0.6, 0.2) E22:", None if m22 is None else [round(x, 4) for x in m22])
    out = {"grades": g, "replication": rep, "labels": dict(labels),
           "cells": {"|".join(map(str, k)): v for k, v in c.items()}}
    json.dump(out, open(os.path.join(HERE, "results", "E22_grading.json"), "w"),
              indent=1, default=str)
