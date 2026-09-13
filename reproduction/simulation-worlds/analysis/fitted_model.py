"""Independent simulator of the FITTED candidate model.

Candidate M3:  M^[X]/M/c with heterogeneous exponential servers
  - arrival epochs: homogeneous Poisson at rate lambda_customers / E[B]
  - batch size    : Geometric on {1,2,...} with mean E[B]
  - service       : exponential, server i has its own rate mu_i
  - discipline    : FCFS, infinite queue, no abandonment, no balking, no vacation
  - assignment    : selectable, because OBS-001/002 were saturated and cannot
                    identify it (every server is always busy under saturation)

This file contains no knowledge of the world's internals; it is built only from
the estimates in analysis/a03 and a04.
"""
from __future__ import annotations

import heapq

import numpy as np


def simulate(lam_customers, c, rates, mean_batch, horizon, warmup, policy="fastest", seed=0):
    rng = np.random.default_rng(seed)
    rates = np.asarray(rates, float)[:c]
    epoch_rate = lam_customers / mean_batch
    ev = []
    seq = 0

    def push(t, kind, data):
        nonlocal seq
        seq += 1
        heapq.heappush(ev, (t, seq, kind, data))

    ARR, DEP = 0, 1
    push(rng.exponential(1 / epoch_rate), ARR, None)
    busy = np.zeros(c, bool)
    cust_of = [None] * c
    idle_since = np.zeros(c)
    queue = []
    recs = []          # (arrival, start, departure, server)
    busy_time = np.zeros(c)
    area_q = 0.0
    last_t = 0.0
    n_arr = 0

    def start(i, arrt, t):
        busy[i] = True
        s = rng.exponential(1 / rates[i])
        cust_of[i] = (arrt, t)
        busy_time[i] += s
        push(t + s, DEP, i)

    while ev:
        t, _, kind, data = heapq.heappop(ev)
        if t > horizon:
            break
        area_q += len(queue) * (t - last_t)
        last_t = t
        if kind == ARR:
            n = int(rng.geometric(1.0 / mean_batch))
            for _ in range(n):
                n_arr += 1
                free = np.flatnonzero(~busy)
                if len(free):
                    if policy == "fastest":
                        i = int(free[np.argmax(rates[free])])
                    elif policy == "random":
                        i = int(rng.choice(free))
                    elif policy == "longest_idle":
                        i = int(free[np.argmin(idle_since[free])])
                    else:
                        i = int(free[0])
                    start(i, t, t)
                else:
                    queue.append(t)
            push(t + rng.exponential(1 / epoch_rate), ARR, None)
        else:
            i = data
            arrt, st = cust_of[i]
            recs.append((arrt, st, t, i))
            busy[i] = False
            idle_since[i] = t
            if queue:
                start(i, queue.pop(0), t)

    r = np.array([x for x in recs if x[0] >= warmup])
    if len(r) == 0:
        return None
    W = r[:, 2] - r[:, 0]
    Wq = r[:, 1] - r[:, 0]
    T = horizon - warmup
    util = np.array([np.sum((r[:, 3] == i) * (r[:, 2] - r[:, 1])) for i in range(c)]) / T
    return {
        "n_served": len(r), "n_arrivals": n_arr,
        "throughput": len(r) / T,
        "W_mean": W.mean(), "W_sd": W.std(),
        "Wq_mean": Wq.mean(), "P_wait": float((Wq > 1e-9).mean()),
        "W_q90": float(np.quantile(W, 0.9)), "W_q99": float(np.quantile(W, 0.99)),
        "Lq": area_q / horizon,
        "util": util, "backlog_end": len(queue),
    }


def predictive(lam, c, rates, mean_batch, horizon, warmup, policy, reps=40, seed0=1000):
    out = [simulate(lam, c, rates, mean_batch, horizon, warmup, policy, seed0 + k)
           for k in range(reps)]
    out = [o for o in out if o]
    keys = ["throughput", "W_mean", "Wq_mean", "P_wait", "W_q90", "W_q99", "Lq"]
    res = {}
    for k in keys:
        v = np.array([o[k] for o in out])
        res[k] = {"mean": float(v.mean()), "sd": float(v.std(ddof=1)),
                  "lo95": float(np.quantile(v, 0.025)), "hi95": float(np.quantile(v, 0.975))}
    U = np.array([o["util"] for o in out])
    res["util"] = {"mean": U.mean(0).tolist(),
                   "lo95": np.quantile(U, 0.025, axis=0).tolist(),
                   "hi95": np.quantile(U, 0.975, axis=0).tolist()}
    return res
