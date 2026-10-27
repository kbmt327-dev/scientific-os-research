"""Grade PRED-019 against results/E20.json.

Written and sealed together with PRED-019, before E20 ran.

Labels are E19's: per (cell, seed) from the 40k/80k pair, DIVERGING if either
horizon aborted or hit the time limit or alpha >= 0.8, STABLE if alpha <= 0.2,
else UNKNOWN; a cell (policy, rho, pi, arm) is labelled only when all six seeds
agree. Values use the 80k horizon and are seed-paired.

Per seed:
  Q_p   = J_F / J_U                       (residual against the exact-work uniform arm)
  a     = log(J_F  / J_CS)                state coupling          (fcfs)
  b     = log(J_CS / J_CM)                within-class spread     (fcfs)
  c     = log(J_CM / J_U)                 between-class composition (fcfs)
  T     = log(J_F  / J_U) = a + b + c
Shares are taken on seed means of the logs.
"""
import json
import math
import os
import statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DECISION_ROWS = [(0.55, 0.2), (0.6, 0.2)]


def load():
    d = json.load(open(os.path.join(HERE, "results", "E20.json")))
    runs = defaultdict(dict)
    for r in d["rows"]:
        runs[(r["policy"], r["rho"], r["penalty"], r["arm"], r["seed"])][r["horizon"]] = r
    return d["config"], runs


def seed_label(pair):
    a, b = pair[40_000], pair[80_000]
    if a["aborted_backlog"] or b["aborted_backlog"] or a["hit_time_limit"] or b["hit_time_limit"]:
        return "DIVERGING", None
    alpha = math.log(b["mean_jct"] / a["mean_jct"]) / math.log(2)
    if alpha >= 0.8:
        return "DIVERGING", alpha
    if alpha <= 0.2:
        return "STABLE", alpha
    return "UNKNOWN", alpha


def cells(cfg, runs):
    out = {}
    for key in {k[:4] for k in runs}:
        labs, alphas, jct = [], [], []
        for s in cfg["seeds"]:
            pair = runs[key + (s,)]
            lab, al = seed_label(pair)
            labs.append(lab)
            alphas.append(al)
            jct.append(pair[80_000]["mean_jct"])
        out[key] = dict(label=labs[0] if len(set(labs)) == 1 else "UNKNOWN",
                        seed_labels=labs, alphas=alphas, jct=jct)
    return out


def stable(c, *keys):
    return all(c[k]["label"] == "STABLE" for k in keys)


def summ(xs):
    m = sum(xs) / len(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return dict(mean=m, sd=sd, se=sd / math.sqrt(len(xs)), per_seed=xs)


def row_stats(c, rho, pen):
    """Everything graded for one (rho, pi) row; None fields when unscorable."""
    f = {arm: ("fcfs", rho, pen, arm) for arm in ("BASE", "F", "RP", "CS", "CM", "U")}
    s = {arm: ("srpt", rho, pen, arm) for arm in ("BASE", "F", "U")}
    out = dict(rho=rho, penalty=pen,
               labels={f"{k[0]}:{k[3]}": c[k]["label"] for k in list(f.values()) + list(s.values())})
    if stable(c, f["F"], f["U"], s["F"], s["U"]):
        qf = [x / y for x, y in zip(c[f["F"]]["jct"], c[f["U"]]["jct"])]
        qs = [x / y for x, y in zip(c[s["F"]]["jct"], c[s["U"]]["jct"])]
        gap = [x - y for x, y in zip(qf, qs)]
        out.update(Q_fcfs=summ(qf), Q_srpt=summ(qs), Q_gap=summ(gap))
    if stable(c, f["F"], f["CS"], f["CM"], f["U"]):
        J = {a: c[f[a]]["jct"] for a in ("F", "CS", "CM", "U")}
        a = [math.log(x / y) for x, y in zip(J["F"], J["CS"])]
        b = [math.log(x / y) for x, y in zip(J["CS"], J["CM"])]
        cc = [math.log(x / y) for x, y in zip(J["CM"], J["U"])]
        T = [math.log(x / y) for x, y in zip(J["F"], J["U"])]
        out.update(a=summ(a), b=summ(b), c=summ(cc), T=summ(T))
        tm = out["T"]["mean"]
        out["shares"] = ({k: out[k]["mean"] / tm for k in ("a", "b", "c")}
                         if tm > 0 else None)
    return out


def grade(cfg, runs, c):
    g = {}
    # P0 instrument: fcfs replay reproduces F in every run
    diffs = []
    for rho, pen in cfg["rows"]:
        for s in cfg["seeds"]:
            for h in cfg["horizons"]:
                fj = runs[("fcfs", rho, pen, "F", s)][h]["mean_jct"]
                rj = runs[("fcfs", rho, pen, "RP", s)][h]["mean_jct"]
                diffs.append(abs(rj - fj) / fj)
    g["P0"] = dict(passed=max(diffs) <= 1e-9, max_rel_diff=max(diffs))

    rows = {(rho, pen): row_stats(c, rho, pen) for rho, pen in cfg["rows"]}
    g["rows"] = {f"{k[0]}|{k[1]}": v for k, v in rows.items()}

    # P1 the residual replicates against the exact-work uniform arm:
    # at (0.6, 0.2), seed-mean Q_fcfs - Q_srpt >= 0.2 and every seed > 0
    r = rows[(0.6, 0.2)]
    if "Q_gap" in r:
        gp = r["Q_gap"]
        g["P1"] = dict(scored=True, passed=gp["mean"] >= 0.2 and min(gp["per_seed"]) > 0,
                       gap=gp)
    else:
        g["P1"] = dict(scored=False, passed=False, labels=r["labels"])

    # P2 DECISION: state coupling carries at least half of the fcfs residual:
    # in every scorable decision row with T > 0, mean(a) >= 0.5 * mean(T);
    # at least one decision row scorable
    sc = [rows[k] for k in DECISION_ROWS if "T" in rows[k] and rows[k]["T"]["mean"] > 0]
    g["P2"] = dict(scored=len(sc),
                   passed=len(sc) >= 1 and all(x["a"]["mean"] >= 0.5 * x["T"]["mean"] for x in sc),
                   rows=[dict(rho=x["rho"], penalty=x["penalty"], a=x["a"]["mean"],
                              T=x["T"]["mean"], shares=x["shares"]) for x in sc])

    # P3 composition hurts fcfs: mean(c) > 0 in every scorable decision row
    sc3 = [rows[k] for k in DECISION_ROWS if "c" in rows[k]]
    g["P3"] = dict(scored=len(sc3),
                   passed=len(sc3) >= 1 and all(x["c"]["mean"] > 0 for x in sc3),
                   rows=[dict(rho=x["rho"], c=x["c"]) for x in sc3])

    # P4 within-class spread hurts fcfs (expected from known theory):
    # mean(b) >= 0 in every scorable decision row
    g["P4"] = dict(scored=len(sc3),
                   passed=len(sc3) >= 1 and all(x["b"]["mean"] >= 0 for x in sc3),
                   rows=[dict(rho=x["rho"], b=x["b"]) for x in sc3])

    # P5 the residual grows with pi: at rho 0.6, mean T(pi 0.2) > mean T(pi 0.1)
    r1, r2 = rows[(0.6, 0.1)], rows[(0.6, 0.2)]
    if "T" in r1 and "T" in r2:
        g["P5"] = dict(scored=True, passed=r2["T"]["mean"] > r1["T"]["mean"],
                       T_01=r1["T"], T_02=r2["T"])
    else:
        g["P5"] = dict(scored=False, passed=False)
    return g


if __name__ == "__main__":
    cfg, runs = load()
    c = cells(cfg, runs)
    g = grade(cfg, runs, c)
    labels = defaultdict(int)
    for v in c.values():
        labels[v["label"]] += 1
    n = sum(labels.values())
    print("cell labels:", dict(labels), f"UNKNOWN share {labels['UNKNOWN'] / n:.3f}")
    for k in ("P0", "P1", "P2", "P3", "P4", "P5"):
        v = g[k]
        print(k, "PASS" if v["passed"] else "FAIL", "" if v.get("scored", True) else "(unscorable)")
    for k, v in g["rows"].items():
        print(k, {x: (round(v[x]["mean"], 4), round(v[x]["sd"], 4))
                  for x in ("Q_fcfs", "Q_srpt", "Q_gap", "a", "b", "c", "T") if x in v},
              "shares", v.get("shares"))
    out = {"grades": g, "labels": dict(labels),
           "cells": {"|".join(map(str, k)): v for k, v in c.items()}}
    json.dump(out, open(os.path.join(HERE, "results", "E20_grading.json"), "w"),
              indent=1, default=str)
