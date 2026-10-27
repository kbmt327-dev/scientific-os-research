"""Grade PRED-022 against results/E23.json (C-058, EP-0034).

Labels and cells are analyze_e21.py's (160k/320k pair, values at 320k, a cell
is labelled only when all six seeds agree). Written and sealed with PRED-022,
before E23 ran.

Per seed, fcfs, within one (rho, pi) row:
  a    = log(J_F  / J_CS)      state coupling, as in E20-E22
  d_X  = log(J_X  / J_CS)      what the stratified shuffle X restores, X in CO, CQ, CT
  share_X = mean(d_X) / mean(a)
Placement-state correlations come from each run's own summary (320k run).
"""
import json
import math
import os
from collections import defaultdict

import analyze_e21 as base
import analyze_e22 as e22

HERE = os.path.dirname(os.path.abspath(__file__))
DECISION_ROWS = [(0.55, 0.2), (0.6, 0.2)]
CLASSES = [2, 4, 8, 16]            # needs that can span extra nodes and have >= ~1% of jobs


def log_ratios(c, rho, pen, x, y):
    return [math.log(p / q) for p, q in zip(c[("fcfs", rho, pen, x)]["jct"],
                                            c[("fcfs", rho, pen, y)]["jct"])]


def stratified(c, rho, pen):
    keys = {a: ("fcfs", rho, pen, a) for a in ("F", "CS", "CO", "CQ", "CT")}
    out = dict(labels={a: c[k]["label"] for a, k in keys.items()})
    if not base.stable(c, keys["F"], keys["CS"]):
        return out
    out["a"] = base.summ(log_ratios(c, rho, pen, "F", "CS"))
    for x in ("CO", "CQ", "CT"):
        if base.stable(c, keys[x]):
            d = base.summ(log_ratios(c, rho, pen, x, "CS"))
            out["d_" + x] = d
            out["share_" + x] = (d["mean"] / out["a"]["mean"]) if out["a"]["mean"] > 0 else None
    return out


def corr_table(runs, cfg, pol, rho, pen, arm, field):
    """per class: list over seeds of the 320k run's Spearman correlation"""
    t = {}
    for k in CLASSES:
        t[k] = [runs[(pol, rho, pen, arm, s)][base.H_LONG]["placement_state"][str(k)][field]
                for s in cfg["seeds"]]
    return t


def all_pos(t):
    return all(v is not None and v > 0 for vs in t.values() for v in vs)


def grade(cfg, runs, c):
    g = {}
    diffs = []
    for rho, pen in cfg["rows"]:
        for s in cfg["seeds"]:
            for h in cfg["horizons"]:
                fj = runs[("fcfs", rho, pen, "F", s)][h]["mean_jct"]
                rj = runs[("fcfs", rho, pen, "RP", s)][h]["mean_jct"]
                diffs.append(abs(rj - fj) / fj)
    g["P0"] = dict(passed=max(diffs) <= 1e-9, max_rel_diff=max(diffs))
    if not g["P0"]["passed"]:
        return g                         # PRED-022: P0 failure stops the episode
    # GPU-work of the shuffled arms against F (they match it only approximately)
    g["work_ratio"] = {}
    for rho, pen in cfg["rows"]:
        for x in ("CS", "CO", "CQ", "CT"):
            w = [runs[("fcfs", rho, pen, x, s)][base.H_LONG]["work_ratio_vs_F"] for s in cfg["seeds"]]
            g["work_ratio"][f"{rho}|{pen}|{x}"] = [min(w), max(w)]

    rows = {k: stratified(c, *k) for k in cfg_rows(cfg)}
    g["rows"] = {f"{k[0]}|{k[1]}": v for k, v in rows.items()}
    sc = [(k, rows[k]) for k in DECISION_ROWS
          if "a" in rows[k] and rows[k]["a"]["mean"] > 0 and "d_CO" in rows[k]]
    # D: busy-stratified shuffle restores at least half of a
    g["D"] = dict(scored=len(sc),
                  passed=len(sc) >= 1 and all(r["d_CO"]["mean"] >= 0.5 * r["a"]["mean"] for _, r in sc),
                  rows={f"{k[0]}|{k[1]}": dict(a=r["a"]["mean"], d_CO=r["d_CO"]["mean"],
                                               share_CO=r["share_CO"]) for k, r in sc})
    # S1: state beats coarse time: d_CO > d_CT
    sc1 = [(k, r) for k, r in sc if "d_CT" in r]
    g["S1"] = dict(scored=len(sc1),
                   passed=len(sc1) >= 1 and all(r["d_CO"]["mean"] > r["d_CT"]["mean"] for _, r in sc1),
                   rows={f"{k[0]}|{k[1]}": dict(d_CO=r["d_CO"]["mean"], d_CT=r["d_CT"]["mean"])
                         for k, r in sc1})
    # S2-S4: placement-time correlations at (0.6, 0.2), classes 2-16, all seeds
    rho, pen = 0.6, 0.2
    t_base = corr_table(runs, cfg, "fcfs", rho, pen, "BASE", "rho_busy")
    t_f = corr_table(runs, cfg, "fcfs", rho, pen, "F", "rho_busy")
    t_s = corr_table(runs, cfg, "srpt", rho, pen, "F", "rho_busy")
    g["S2"] = dict(passed=all_pos(t_base), table=t_base)
    g["S3"] = dict(passed=all_pos(t_f) and all_pos(t_s), fcfs=t_f, srpt=t_s)
    # S4: feedback: fcfs F places into a more fragmented cluster than BASE
    ef = [runs[("fcfs", rho, pen, "F", s)][base.H_LONG]["excess_nodes_per_placement"] for s in cfg["seeds"]]
    eb = [runs[("fcfs", rho, pen, "BASE", s)][base.H_LONG]["excess_nodes_per_placement"] for s in cfg["seeds"]]
    g["S4"] = dict(passed=all(x > y for x, y in zip(ef, eb)), F=ef, BASE=eb,
                   diff=base.summ([x - y for x, y in zip(ef, eb)]))
    # reported: queue-length and scatter correlations, CQ share, E21's statistics on these seeds
    g["reported"] = dict(
        rho_wait_fcfs_F=corr_table(runs, cfg, "fcfs", rho, pen, "F", "rho_wait"),
        rho_scatter_fcfs_F=corr_table(runs, cfg, "fcfs", rho, pen, "F", "rho_scatter"),
        rho_wait_srpt_F=corr_table(runs, cfg, "srpt", rho, pen, "F", "rho_wait"),
        e21_P2_on_these_seeds=base.grade(cfg, runs, c)["P2"])
    return g


def cfg_rows(cfg):
    return [tuple(r) for r in cfg["rows"]]


if __name__ == "__main__":
    cfg, runs = e22.load("E23.json")
    c = base.cells(cfg, runs)
    g = grade(cfg, runs, c)
    labels = defaultdict(int)
    for v in c.values():
        labels[v["label"]] += 1
    n = sum(labels.values())
    print("cell labels:", dict(labels), f"UNKNOWN share {labels['UNKNOWN'] / n:.3f}")
    if not g["P0"]["passed"]:
        print("P0 FAIL: instrument broken, episode stops", g["P0"])
        json.dump({"grades": g}, open(os.path.join(HERE, "results", "E23_grading.json"), "w"),
                  indent=1, default=str)
        raise SystemExit(1)
    for k in ("P0", "D", "S1", "S2", "S3", "S4"):
        v = g[k]
        print(k, "PASS" if v["passed"] else "FAIL", "" if v.get("scored", 1) else "(unscorable)")
    for k, v in g["rows"].items():
        print(k, v["labels"], {x: (round(v[x]["mean"], 4), round(v[x]["sd"], 4), round(v[x]["se"], 4))
                               for x in ("a", "d_CO", "d_CQ", "d_CT") if x in v},
              {x: v.get(x) and round(v[x], 3) for x in ("share_CO", "share_CQ", "share_CT")})
    print("S4 excess/placement F-BASE:", {x: round(g["S4"]["diff"][x], 4) for x in ("mean", "sd", "se")})
    for name, t in (("fcfs BASE rho_busy", g["S2"]["table"]), ("fcfs F rho_busy", g["S3"]["fcfs"]),
                    ("srpt F rho_busy", g["S3"]["srpt"]),
                    ("fcfs F rho_wait", g["reported"]["rho_wait_fcfs_F"]),
                    ("fcfs F rho_scatter", g["reported"]["rho_scatter_fcfs_F"])):
        print(name, {k: (round(min(x for x in v if x is not None), 3),
                         round(max(x for x in v if x is not None), 3),
                         sum(x is None for x in v)) if any(x is not None for x in v) else None
                     for k, v in t.items()})
    print("work ratio vs F (min, max at 320k):",
          {k: [round(x, 4) for x in v] for k, v in g["work_ratio"].items()})
    p2 = g["reported"]["e21_P2_on_these_seeds"]
    print("E21 P2 rule on E23 seeds:", "PASS" if p2["passed"] else "FAIL", p2["rows"])
    out = {"grades": g, "labels": dict(labels),
           "cells": {"|".join(map(str, k)): v for k, v in c.items()}}
    json.dump(out, open(os.path.join(HERE, "results", "E23_grading.json"), "w"),
              indent=1, default=str)
