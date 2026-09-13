"""E12: is the frequency of the largest class a third variable?

Predictions and grading rules are sealed in predictions/PRED-011.json before
this script is run.

Four arms:
  R  replay E9 exactly (code-drift gate)
  A  factorial  r x E[need] target x p, fully crossed
  B  p extension to 0.05 where the workload algebra allows it
  C  EASY backfill reference cells

The construction sets the maximum-job ratio, the frequency of that class and
the target concurrency independently.  E[need] pins concurrency through
Little's law (every job is in service for E[S]=1, so the mean number running is
rho*N/E[need] while all classes are served).  The background geometric ratio is
fitted so that the background mean absorbs whatever p*m takes.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.cluster import simulate
from sim.workload import make_workload, mix_stats

N = 256
RHO = 0.85
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
HERE = os.path.dirname(os.path.abspath(__file__))

RATIOS = [0.5, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
# exactly the background means of E9's s=12, s=8 and s=4 rows
E_TARGETS = {
    "C10": 12 * 2.952 / 1.624,
    "C15": 8 * 2.952 / 1.624,
    "C28": 4 * 2.952 / 1.624,
}
P_LEVELS = [0.002, 0.005, 0.02]
P_EXTENSION = {"C10": 0.05, "C15": 0.05}      # infeasible at C28
SEEDS = [901, 902, 903, 904, 905]
REPLAY_S = [12, 8, 4]
REPLAY_SEEDS = [601, 602, 603, 604]
REPLAY_P_M = 0.002
REPLAY_THETA = 0.4
REF_RATIOS = [0.5, 0.75, 1.0]
REF_P = 0.005
REF_SEEDS = [901, 902, 903]

GEOM_SUPPORT = (1, 2, 4, 8, 16, 32, 64)
KEEP = ["mean_jct", "utilization", "rho_emp", "mean_backlog", "mean_running",
        "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
        "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance",
        "starving_needs"]


def fit_geometric(target_mean, support=GEOM_SUPPORT):
    """Geometric weights over `support` whose mean equals target_mean."""
    lo, hi = 0.0, 80.0
    for _ in range(300):
        mid = (lo + hi) / 2
        w = np.asarray([mid ** i for i in range(len(support))], dtype=float)
        if float(np.dot(support, w / w.sum())) < target_mean:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    w = np.asarray([theta ** i for i in range(len(support))], dtype=float)
    probs = w / w.sum()
    return theta, tuple(probs), float(np.dot(support, probs))


def factorial_mix(e_target, ratio, p):
    """Need distribution with P(need=m)=p and E[need]=e_target exactly."""
    m = int(round(N * ratio))
    bg_mean = (e_target - p * m) / (1 - p)
    assert bg_mean >= 1.05, f"infeasible cell: bg_mean={bg_mean}"
    theta, bg_probs, achieved_bg = fit_geometric(bg_mean)
    assert max(GEOM_SUPPORT) < m, "background support must stay below m"
    needs = GEOM_SUPPORT + (m,)
    probs = tuple((1 - p) * np.asarray(bg_probs)) + (p,)
    e_need = float(np.dot(needs, probs))
    assert abs(sum(probs) - 1.0) < 1e-12
    assert abs(e_need - e_target) < 1e-9, (e_need, e_target)
    return needs, probs, m, bg_mean, theta


def replay_mix(s, m, p_m=REPLAY_P_M, theta=REPLAY_THETA):
    """Byte-identical reproduction of run_e9.py's mix()."""
    bg = [s, 2 * s, 4 * s, 8 * s]
    w = np.array([theta ** i for i in range(len(bg))], dtype=float)
    w = w / w.sum() * (1.0 - p_m)
    if m in bg:
        probs = list(w)
        probs[bg.index(m)] += p_m
        return tuple(bg), tuple(probs)
    return tuple(bg) + (m,), tuple(w) + (p_m,)


def _run(needs, probs, seed, policy):
    jobs, lam = make_workload(N_JOBS, RHO, N, seed=seed, needs=needs,
                              need_probs=probs)
    t0 = time.time()
    sim = simulate(jobs, N, policy, c_pre=0.0, dur_mean=1.0,
                   t_limit_factor=2.0, backlog_cap=60_000)
    rec = {k: sim[k] for k in KEEP}
    rec["secs"] = round(time.time() - t0, 1)
    rec["lam"] = lam
    return rec, sim


def one(task):
    arm = task[0]
    if arm == "R":
        _, s, ratio, seed = task
        m = int(round(N * ratio))
        needs, probs = replay_mix(s, m)
        rec, sim = _run(needs, probs, seed, "srpt")
        rec.update(arm=arm, s=s, ratio=ratio, m=m, seed=seed, policy="srpt",
                   p=REPLAY_P_M)
    else:
        _, e_label, ratio, p, seed, policy = task
        e_target = E_TARGETS[e_label]
        needs, probs, m, bg_mean, theta = factorial_mix(e_target, ratio, p)
        rec, sim = _run(needs, probs, seed, policy)
        rec.update(arm=arm, e_label=e_label, e_target=e_target, ratio=ratio,
                   m=m, p=p, seed=seed, policy=policy, bg_mean=bg_mean,
                   bg_theta=theta, work_share_max=p * m / e_target,
                   predicted_conc=RHO * N / e_target,
                   **mix_stats(needs, probs, N))
    fb, jb = sim["flow_balance_by_need"], sim["jct_by_need"]
    rec["fb_m"] = fb.get(rec["m"], fb.get(str(rec["m"])))
    rec["jct_m"] = jb.get(rec["m"], jb.get(str(rec["m"])))
    rec["n_arr_m"] = sim["n_arrivals_by_need"].get(
        rec["m"], sim["n_arrivals_by_need"].get(str(rec["m"])))
    return rec


def build_tasks():
    tasks = []
    for s in REPLAY_S:
        for ratio in RATIOS:
            for seed in REPLAY_SEEDS:
                tasks.append(("R", s, ratio, seed))
    for e_label in E_TARGETS:
        for ratio in RATIOS:
            for p in P_LEVELS:
                for seed in SEEDS:
                    tasks.append(("A", e_label, ratio, p, seed, "srpt"))
    for e_label, p in P_EXTENSION.items():
        for ratio in RATIOS:
            for seed in SEEDS:
                tasks.append(("B", e_label, ratio, p, seed, "srpt"))
    for e_label in E_TARGETS:
        for ratio in REF_RATIOS:
            for seed in REF_SEEDS:
                tasks.append(("C", e_label, ratio, REF_P, seed,
                              "easy_backfill"))
    return tasks


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    tasks = build_tasks()
    by_arm = {}
    for t in tasks:
        by_arm[t[0]] = by_arm.get(t[0], 0) + 1
    print(f"E12: {len(tasks)} runs {by_arm}  workers={workers}  N={N}")
    for e_label, e in E_TARGETS.items():
        print(f"  {e_label}: E[need]={e:.4f}  predicted concurrency="
              f"{RHO * N / e:.2f}")
        for p in P_LEVELS + [P_EXTENSION.get(e_label)]:
            if p is None:
                continue
            cells = []
            for ratio in (0.5, 1.0):
                _, _, m, bg, th = factorial_mix(e, ratio, p)
                cells.append(f"r={ratio} bg={bg:.2f} theta={th:.3f} "
                             f"w_max={p * m / e:.3f}")
            print(f"    p={p:<6} " + " | ".join(cells))

    rows, t0 = [], time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, rec in enumerate(ex.map(one, tasks), 1):
            rows.append(rec)
            if i % 40 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ({time.time() - t0:.0f}s)",
                      flush=True)

    out = os.path.join(HERE, "results", "E12.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump({"config": {
            "n_servers": N, "rho": RHO, "n_jobs": N_JOBS, "ratios": RATIOS,
            "e_targets": E_TARGETS, "p_levels": P_LEVELS,
            "p_extension": P_EXTENSION, "seeds": SEEDS,
            "replay_s": REPLAY_S, "replay_seeds": REPLAY_SEEDS,
            "replay_p_m": REPLAY_P_M, "replay_theta": REPLAY_THETA,
            "ref_ratios": REF_RATIOS, "ref_p": REF_P, "ref_seeds": REF_SEEDS,
            "geom_support": list(GEOM_SUPPORT),
            "pred_sha256": os.environ.get("PRED_SHA", ""),
        }, "rows": rows}, handle, indent=1)
    print(f"  wrote {out}")
