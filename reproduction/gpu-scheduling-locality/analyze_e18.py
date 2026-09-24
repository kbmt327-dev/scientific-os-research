"""Grade PRED-017 against results/E18.json.

Written and sealed together with PRED-017, before E18 ran.

Stability label per (cell, seed), from the 40k/80k horizon pair:
  DIVERGING  if either horizon aborted on the backlog cap or hit the time limit,
             or alpha >= 0.8
  STABLE     if alpha <= 0.2
  UNKNOWN    otherwise
alpha = log(mean_jct_80k / mean_jct_40k) / log 2. A cell takes a label only
when all three seeds agree; otherwise it is UNKNOWN. Comparisons use the 80k
horizon, seed-paired: ratio = mean over seeds of J_A / J_B.
"""
import json
import math
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
POLICIES = ["fcfs", "easy_backfill", "srpt", "sf_srpt"]


def load():
    d = json.load(open(os.path.join(HERE, "results", "E18.json")))
    runs = defaultdict(dict)
    for r in d["rows"]:
        key = (r["mix"], r["policy"], r["rho"], r["penalty"], r["placement"], r["seed"])
        runs[key][r["horizon"]] = r
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
    for mix in cfg["mixes"]:
        for pol in POLICIES:
            for rho in cfg["rhos"]:
                for pen in cfg["penalties"]:
                    for place in cfg["placements"]:
                        labs, alphas, jct, exc, worst = [], [], [], [], []
                        for s in cfg["seeds"]:
                            pair = runs[(mix, pol, rho, pen, place, s)]
                            lab, al = seed_label(pair)
                            labs.append(lab)
                            alphas.append(al)
                            r = pair[80_000]
                            jct.append(r["mean_jct"])
                            exc.append(r["excess_nodes_per_placement"])
                            worst.append(max(r["jct_by_need"].values()) if r["jct_by_need"] else None)
                        label = labs[0] if len(set(labs)) == 1 else "UNKNOWN"
                        out[(mix, pol, rho, pen, place)] = dict(
                            label=label, seed_labels=labs, alphas=alphas,
                            jct=jct, excess=exc, worst=worst)
    return out


def ratio(c, a, b):
    """Seed-paired mean of J_a / J_b."""
    return sum(x / y for x, y in zip(c[a]["jct"], c[b]["jct"])) / len(c[a]["jct"])


def better(c, a, b):
    """+1 if a strictly better than b, -1 if b strictly better, 0 otherwise.
    Strict: both STABLE and ratio < 0.95 (or > 1.05), or one STABLE and the
    other DIVERGING."""
    la, lb = c[a]["label"], c[b]["label"]
    if la == "STABLE" and lb == "STABLE":
        r = ratio(c, a, b)
        return 1 if r < 0.95 else (-1 if r > 1.05 else 0)
    if la == "STABLE" and lb == "DIVERGING":
        return 1
    if la == "DIVERGING" and lb == "STABLE":
        return -1
    return 0


def reversals(c, cfg, place):
    found = []
    for mix in cfg["mixes"]:
        for rho in cfg["rhos"]:
            for i, a in enumerate(POLICIES):
                for b in POLICIES[i + 1:]:
                    k0a, k0b = (mix, a, rho, 0.0, place), (mix, b, rho, 0.0, place)
                    k6a, k6b = (mix, a, rho, 0.6, place), (mix, b, rho, 0.6, place)
                    s0, s6 = better(c, k0a, k0b), better(c, k6a, k6b)
                    if s0 != 0 and s6 == -s0:
                        found.append((mix, rho, a, b, s0, s6))
    return found


def degradation(c, mix, pol, rho, place, pen):
    base, hit = c[(mix, pol, rho, 0.0, place)], c[(mix, pol, rho, pen, place)]
    if base["label"] != "STABLE" or hit["label"] != "STABLE":
        return None
    return sum(h / b for h, b in zip(hit["jct"], base["jct"])) / len(base["jct"])


def grade(cfg, runs, c):
    g = {}
    # P0 control: at pi = 0 placement cannot change anything
    diffs = [abs(runs[(m, p, r, 0.0, "first_fit", s)][h]["mean_jct"]
                 - runs[(m, p, r, 0.0, "compact", s)][h]["mean_jct"])
             for m in cfg["mixes"] for p in POLICIES for r in cfg["rhos"]
             for s in cfg["seeds"] for h in cfg["horizons"]]
    g["P0"] = dict(passed=max(diffs) == 0.0, max_abs_diff=max(diffs))

    # P1 compact spans fewer excess nodes than first_fit at pi = 0.3 everywhere,
    # and at most 0.05 excess nodes per placement on gang_heavy
    rows, ok = [], True
    for m in cfg["mixes"]:
        for p in POLICIES:
            for r in cfg["rhos"]:
                ff = sum(c[(m, p, r, 0.3, "first_fit")]["excess"]) / 3
                cp = sum(c[(m, p, r, 0.3, "compact")]["excess"]) / 3
                cond = cp < ff and (m != "gang_heavy" or cp <= 0.05)
                ok &= cond
                rows.append(dict(mix=m, policy=p, rho=r, first_fit=ff, compact=cp, ok=cond))
    g["P1"] = dict(passed=ok, rows=rows)

    # P2 first_fit, rho 0.7, pi 0.3: degradation larger on gang_heavy than
    # trace_like for every policy STABLE in all four cells involved
    rows, ok, n = [], True, 0
    for p in POLICIES:
        dg = degradation(c, "gang_heavy", p, 0.7, "first_fit", 0.3)
        dt = degradation(c, "trace_like", p, 0.7, "first_fit", 0.3)
        if dg is None or dt is None:
            rows.append(dict(policy=p, gang_heavy=dg, trace_like=dt, scored=False))
            continue
        n += 1
        ok &= dg > dt
        rows.append(dict(policy=p, gang_heavy=dg, trace_like=dt, scored=True, ok=dg > dt))
    g["P2"] = dict(passed=ok and n > 0, scored=n, rows=rows)

    # P3 decision: >= 1 reversal pi 0 -> 0.6 under first_fit, none under compact
    rf, rc = reversals(c, cfg, "first_fit"), reversals(c, cfg, "compact")
    g["P3"] = dict(passed=len(rf) >= 1 and len(rc) == 0, first_fit=rf, compact=rc)

    # P4 trace_like first_fit pi 0 -> 0.6: easy_backfill smallest degradation
    # among policies STABLE at both ends, at both loads
    rows, ok = [], True
    for r in cfg["rhos"]:
        d = {p: degradation(c, "trace_like", p, r, "first_fit", 0.6) for p in POLICIES}
        scored = {p: v for p, v in d.items() if v is not None}
        cond = "easy_backfill" in scored and min(scored, key=scored.get) == "easy_backfill"
        ok &= cond
        rows.append(dict(rho=r, degradation=d, ok=cond))
    g["P4"] = dict(passed=ok, rows=rows)

    # P5 gang_heavy first_fit rho 0.7 pi 0.6: sf_srpt degrades more than
    # easy_backfill (DIVERGING sf_srpt with STABLE easy_backfill counts as more)
    sf, eb = c[("gang_heavy", "sf_srpt", 0.7, 0.6, "first_fit")], c[("gang_heavy", "easy_backfill", 0.7, 0.6, "first_fit")]
    dsf = degradation(c, "gang_heavy", "sf_srpt", 0.7, "first_fit", 0.6)
    deb = degradation(c, "gang_heavy", "easy_backfill", 0.7, "first_fit", 0.6)
    if sf["label"] == "DIVERGING" and eb["label"] == "STABLE":
        p5 = True
    elif dsf is not None and deb is not None:
        p5 = dsf > deb
    else:
        p5 = None
    g["P5"] = dict(passed=p5, sf_srpt=dsf, easy_backfill=deb,
                   labels=(sf["label"], eb["label"]))
    return g


if __name__ == "__main__":
    cfg, runs = load()
    c = cells(cfg, runs)
    g = grade(cfg, runs, c)
    for k, v in g.items():
        print(k, "PASS" if v["passed"] is True else ("UNSCORABLE" if v["passed"] is None else "FAIL"))
    labels = defaultdict(int)
    for v in c.values():
        labels[v["label"]] += 1
    print("cell labels:", dict(labels))
    out = {"grades": g, "labels": dict(labels),
           "cells": {"|".join(map(str, k)): v for k, v in c.items()}}
    json.dump(out, open(os.path.join(HERE, "results", "E18_grading.json"), "w"), indent=1, default=str)
