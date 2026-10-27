"""Experiment E20: where does the fcfs fragmentation residual come from?

E19 (PRED-018) left one residual: on trace_like at rho 0.6, pi 0.2, first_fit,
fcfs degraded by R = 1.66 beyond a load-matched control against 1.15 for srpt.
E19's control was approximate in two ways: it scaled every arrival instead of
the jobs fragmentation actually slowed, and it interpolated J between load
points without the slower service itself.

E20 replaces it with a ladder of pi = 0 arms that carry EXACTLY the work the
fragmented run (F) did, differing only in how that extra work is distributed:

  RP  replay: each job runs size / rate_j, rate_j its realised rate in F.
      For fcfs (non-preemptive, admission by free count only) this must
      reproduce F; it is the instrument check.
  CS  class-shuffled: the slowdowns 1/rate_j are permuted among jobs of the
      same need class. Same multiset per class, no link to the cluster state
      at placement time.
  CM  class-mean: every job of a class gets the size-weighted mean slowdown of
      its class. Same work per class, no within-class spread.
  U   uniform: every job gets the GPU-work-weighted mean slowdown over all
      jobs. Same total GPU-work, no composition. (srpt gets this arm too; for
      srpt, which re-places preempted jobs, the job's final rate stands in for
      its realised rate, so srpt's U carries F's work only approximately.)

So log(J_F / J_U) splits into state coupling log(J_F / J_CS), within-class
spread log(J_CS / J_CM) and between-class composition log(J_CM / J_U).

Predictions were sealed in predictions/PRED-019.json before this script ran.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.cluster import simulate
from sim.workload import make_workload

N = 64
NODE = 8
HORIZONS = [40_000, 80_000]
SEEDS = [2001, 2002, 2003, 2004, 2005, 2006]
ROWS = [(0.55, 0.2), (0.6, 0.2), (0.6, 0.1)]          # (rho, pi), first_fit
POLICIES = ["fcfs", "srpt"]
ARMS = {"fcfs": ["RP", "CS", "CM", "U"], "srpt": ["U"]}
MIX = ((1, 2, 4, 8, 16, 32), (0.50, 0.20, 0.15, 0.10, 0.04, 0.01))   # trace_like
BACKLOG_CAP = 6000
SHUFFLE_SEED_OFFSET = 7_000_000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "E20.json")
KEEP = ["mean_jct", "p99_jct", "mean_wait", "utilization", "rho_emp", "util_over_rho",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "mean_gang_rate", "gang_rate_by_need", "excess_nodes_per_placement"]


def workload(rho, seed, horizon):
    return make_workload(horizon, rho, N, seed=seed, needs=MIX[0],
                         need_probs=MIX[1], sigma=0.0)


def sim(jobs, pol, pen, trace=None):
    return simulate(jobs, N, pol, dur_mean=1.0, t_limit_factor=2.0,
                    backlog_cap=BACKLOG_CAP, node_size=NODE,
                    cross_node_penalty=pen, placement="first_fit",
                    penalty_mode="excess", trace=trace)


def slowdowns(arm, size, need, slow, seed):
    """Per-job duration multipliers for an arm, from F's realised slowdowns.
    Means are weighted by GPU-work need * size, so CM and U carry exactly the
    GPU-work F did (within a class need is constant, so size weights suffice)."""
    if arm == "RP":
        return slow.copy()
    out = np.empty_like(slow)
    if arm == "U":
        w = need * size
        out[:] = np.dot(w, slow) / w.sum()
        return out
    rng = np.random.default_rng(seed + SHUFFLE_SEED_OFFSET)
    for k in np.unique(need):
        idx = np.flatnonzero(need == k)
        if arm == "CS":
            out[idx] = slow[rng.permutation(idx)]
        else:  # CM
            out[idx] = np.dot(size[idx], slow[idx]) / size[idx].sum()
    return out


C058_ARMS = ["CQ", "CO", "CT"]
STRATA = 5
TRACE_COLS = ("jid", "t", "need", "excess", "rate", "busy", "n_waiting", "n_free",
              "free_nodes_any", "free_nodes_full")
BUSY_BINS = [0.5, 0.75, 0.9]          # busy / N: [0,.5) [.5,.75) [.75,.9) [.9,1]
WAIT_BINS = [1, 4, 16]                # n_waiting: 0, 1-3, 4-15, 16+


def strata(arm, need, jid, state):
    """C-058 strata for the stratified shuffles: within need class, five bins of
    F's placement-time queue length (CQ) or busy servers (CO), cut at value
    quantiles so ties stay together, or five equal-count arrival-order blocks
    (CT, over placed jobs). Jobs F never placed get their own stratum -1."""
    out = np.full(len(need), -1, dtype=np.int64)
    for k in np.unique(need):
        idx = np.flatnonzero(need == k)
        if arm == "CT":
            placed = idx[np.array([jid[i] in state for i in idx], dtype=bool)]
            if len(placed):                                  # jobs are in jid order
                out[placed] = np.arange(len(placed)) * STRATA // len(placed)
            continue
        col = 1 if arm == "CQ" else 0
        v = np.array([state[jid[i]][col] if jid[i] in state else np.nan for i in idx])
        ok = ~np.isnan(v)
        if ok.any():
            edges = np.unique(np.quantile(v[ok], np.arange(1, STRATA) / STRATA))
            out[idx[ok]] = np.searchsorted(edges, v[ok], side="right")
    return out


def shuffle_within(groups, slow, seed, offset):
    rng = np.random.default_rng(seed + SHUFFLE_SEED_OFFSET + offset)
    out = slow.copy()
    for g in np.unique(groups):
        idx = np.flatnonzero(groups == g)
        out[idx] = slow[rng.permutation(idx)]
    return out


def spearman(x, y):
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    from scipy.stats import spearmanr
    return float(spearmanr(x, y)[0])


def summarise_trace(trace, warm_jid):
    """Per need class, over measured placements (jid >= warm_jid): placement
    count, mean excess, Spearman correlation of excess with busy servers,
    queue length and free-GPU scatter, and mean excess by busy / queue bins.
    scatter = nodes holding free GPUs beyond the fewest that could hold them."""
    a = np.array(trace, dtype=float)
    a = a[a[:, 0] >= warm_jid]
    col = {c: a[:, i] for i, c in enumerate(TRACE_COLS)}
    scatter = col["free_nodes_any"] - np.ceil(col["n_free"] / NODE)
    bfrac = col["busy"] / N
    out = {}
    for k in np.unique(col["need"]):
        m = col["need"] == k
        ex = col["excess"][m]
        bb = np.searchsorted(BUSY_BINS, bfrac[m], side="right")
        wb = np.searchsorted(WAIT_BINS, col["n_waiting"][m], side="right")
        out[int(k)] = dict(
            n=int(m.sum()), mean_excess=float(ex.mean()),
            frac_excess_pos=float((ex > 0).mean()),
            mean_busy=float(bfrac[m].mean()), mean_waiting=float(col["n_waiting"][m].mean()),
            rho_busy=spearman(ex, col["busy"][m]),
            rho_wait=spearman(ex, col["n_waiting"][m]),
            rho_scatter=spearman(ex, scatter[m]),
            excess_by_busy_bin={int(b): [int((bb == b).sum()), float(ex[bb == b].mean())]
                                for b in np.unique(bb)},
            excess_by_wait_bin={int(b): [int((wb == b).sum()), float(ex[wb == b].mean())]
                                for b in np.unique(wb)})
    return out


def one(task):
    """One (policy, rho, pi, seed, horizon): base (pi 0), F, and the pi = 0
    arms built from F's realised rates. Every arm reuses the same arrivals,
    needs and sizes.

    An optional sixth task element {"c058": True} adds C-058 (E23): BASE and F
    record every placement's cluster state (sim trace=) and return a per-class
    summary, and fcfs gets three more pi = 0 arms that shuffle F's slowdowns
    within need class AND a stratum -- CQ (F's queue length at placement), CO
    (F's busy servers at placement), CT (arrival-order block). Without it the
    output is E20's, unchanged."""
    pol, rho, pen, seed, h = task[:5]
    c058 = len(task) > 5 and task[5].get("c058", False)
    t0 = time.time()
    recs = []

    def rec(arm, m, extra=None):
        r = {k: m.get(k) for k in KEEP}
        r.update(policy=pol, rho=rho, penalty=pen, seed=seed, horizon=h, arm=arm)
        if extra:
            r.update(extra)
        recs.append(r)

    jobs, _ = workload(rho, seed, h)
    warm = int(len(jobs) * 0.2)          # simulate()'s warmup_frac default
    tr_base = [] if c058 else None
    rec("BASE", sim(jobs, pol, 0.0, tr_base),
        dict(placement_state=summarise_trace(tr_base, warm)) if c058 else None)
    jobs, _ = workload(rho, seed, h)
    tr_f = [] if c058 else None
    rec("F", sim(jobs, pol, pen, tr_f),
        dict(placement_state=summarise_trace(tr_f, warm)) if c058 else None)
    size = np.array([j.size for j in jobs])
    need = np.array([j.need for j in jobs])
    jid = np.array([j.jid for j in jobs])
    slow = np.array([1.0 / j.rate for j in jobs])   # final rate; exact for fcfs
    arms = list(ARMS[pol])
    if c058 and pol == "fcfs":
        arms += C058_ARMS
        state = {}
        for row in tr_f:                 # fcfs places each job once
            state[row[0]] = (row[5], row[6])   # (busy, n_waiting)
    for arm in arms:
        if arm in C058_ARMS:
            g = strata(arm, need, jid, state)
            groups = need.astype(np.int64) * 100 + g
            mult = shuffle_within(groups, slow, seed, 1 + C058_ARMS.index(arm))
        else:
            mult = slowdowns(arm, size, need, slow, seed)
        jobs, _ = workload(rho, seed, h)
        for j, s in zip(jobs, mult):
            j.size = j.size * s
            j.remaining = j.size
            j.est_total = j.size
        w = need * size
        work_ratio = float(np.dot(w, mult) / np.dot(w, slow))
        rec(arm, sim(jobs, pol, 0.0), dict(work_ratio_vs_F=work_ratio))
    for r in recs:
        r["secs"] = round(time.time() - t0, 1)
    return recs


def build_tasks():
    return [(pol, rho, pen, s, h) for pol in POLICIES for rho, pen in ROWS
            for s in SEEDS for h in HORIZONS]


if __name__ == "__main__":
    if os.path.exists(OUT):
        raise FileExistsError(OUT)
    tasks = build_tasks()
    tasks.sort(key=lambda t: (t[0] != "fcfs", -t[4]))
    print(f"{len(tasks)} tasks")
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=int(os.environ.get("WORKERS", 14))) as ex:
        for i, recs in enumerate(ex.map(one, tasks), 1):
            rows.extend(recs)
            if i % 10 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)} ({time.time() - t0:.0f}s)", flush=True)
    json.dump({"config": {"n_servers": N, "node_size": NODE, "horizons": HORIZONS,
                          "seeds": SEEDS, "rows": ROWS, "policies": POLICIES,
                          "arms": ARMS, "mix": [list(MIX[0]), list(MIX[1])],
                          "penalty_mode": "excess", "placement": "first_fit",
                          "backlog_cap": BACKLOG_CAP, "pred": "PRED-019"},
               "rows": rows}, open(OUT, "w"), indent=1,
              # POST-SEAL FIX (serialization only): arm durations are numpy
              # floats, so some metrics come back as numpy bool/float and the
              # first run crashed here after all simulations had finished.
              default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
