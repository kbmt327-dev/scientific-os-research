"""E11: re-axis EP-0002 and challenge the two-number explanation.

Predictions and grading rules are sealed in predictions/PRED-010.json before
this script is run.  The first arm exactly replays the srpt/sf_srpt half of E2
while retaining mean_running.  The second arm holds E[need], p64, rho, N and
arrival rate fixed while changing only the background need distribution.
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim.cluster import simulate
from sim.workload import geometric_mix, make_workload, mix_stats

N = 64
N_JOBS = int(os.environ.get("N_JOBS", 30_000))
THETAS = [0.4, 0.6, 0.8, 1.0, 1.25, 1.6, 2.0]
RHOS = [0.7, 0.85, 0.95]
PHASE_POLICIES = ["srpt", "sf_srpt"]
PHASE_SEEDS = [201, 202, 203, 204, 205]
CONTROL_POLICIES = ["srpt", "sf_srpt", "easy_backfill"]
CONTROL_SEEDS = [801, 802, 803, 804, 805]
HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = [
    "mean_jct", "mean_running", "mean_backlog", "utilization", "rho_emp",
    "completion_frac", "aborted_backlog", "hit_time_limit", "jct_by_need",
    "flow_balance_by_need", "n_arrivals_by_need", "min_flow_balance",
    "starving_needs",
]


def fitted_geometric_background(target_mean):
    needs = (1, 2, 4, 8, 16, 32)
    lo, hi = 0.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        w = np.asarray([mid ** i for i in range(len(needs))], dtype=float)
        mean = float(np.dot(needs, w / w.sum()))
        if mean < target_mean:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    w = np.asarray([theta ** i for i in range(len(needs))], dtype=float)
    return needs, tuple(w / w.sum()), theta


def two_point_background(low, high, target_mean):
    p_high = (target_mean - low) / (high - low)
    assert 0 <= p_high <= 1
    return (low, high), (1 - p_high, p_high)


def make_control_group(label, target_mean, p64, narrow_support, wide_support):
    bg_mean = (target_mean - p64 * N) / (1 - p64)
    narrow_n, narrow_p = two_point_background(*narrow_support, bg_mean)
    wide_n, wide_p = two_point_background(*wide_support, bg_mean)
    geom_n, geom_p, theta = fitted_geometric_background(bg_mean)
    shapes = {
        "narrow": (narrow_n, narrow_p),
        "geometric": (geom_n, geom_p),
        "wide": (wide_n, wide_p),
    }
    out = {}
    for shape, (needs, probs) in shapes.items():
        full_needs = tuple(needs) + (N,)
        full_probs = tuple((1 - p64) * np.asarray(probs)) + (p64,)
        actual_mean = float(np.dot(full_needs, full_probs))
        assert abs(sum(full_probs) - 1) < 1e-12
        assert abs(actual_mean - target_mean) < 1e-10
        out[shape] = {
            "needs": full_needs,
            "probs": full_probs,
            "background_mean": bg_mean,
            "fitted_theta": theta if shape == "geometric" else None,
        }
    return label, out


CONTROL_GROUPS = dict([
    make_control_group("mean4", 4.0, 0.02, (2, 4), (1, 8)),
    make_control_group("mean16", 16.0, 0.10, (8, 16), (1, 32)),
])


def phase_one(task):
    theta, rho, policy, seed = task
    needs, probs = geometric_mix(theta)
    jobs, lam = make_workload(
        N_JOBS, rho, N, seed=seed, needs=needs, need_probs=probs
    )
    t0 = time.time()
    result = simulate(
        jobs, N, policy, c_pre=0.0, dur_mean=1.0,
        t_limit_factor=2.0, backlog_cap=6000,
    )
    rec = {key: result[key] for key in KEEP}
    rec.update(
        arm="phase_remeasurement", theta=theta, rho=rho, policy=policy,
        seed=seed, lam=lam, secs=round(time.time() - t0, 2),
        **mix_stats(needs, probs, N),
    )
    return rec


def control_one(task):
    group, shape, policy, seed = task
    spec = CONTROL_GROUPS[group][shape]
    needs, probs = spec["needs"], spec["probs"]
    jobs, lam = make_workload(
        N_JOBS, 0.85, N, seed=seed, needs=needs, need_probs=probs
    )
    t0 = time.time()
    result = simulate(
        jobs, N, policy, c_pre=0.0, dur_mean=1.0,
        t_limit_factor=2.0, backlog_cap=60_000,
    )
    rec = {key: result[key] for key in KEEP}
    rec.update(
        arm="equal_summary_control", group=group, shape=shape,
        policy=policy, seed=seed, rho=0.85, lam=lam,
        needs=list(needs), probs=list(probs),
        fitted_theta=spec["fitted_theta"],
        secs=round(time.time() - t0, 2),
        **mix_stats(needs, probs, N),
    )
    return rec


if __name__ == "__main__":
    workers = int(os.environ.get("WORKERS", 8))
    phase_tasks = [
        (theta, rho, policy, seed)
        for theta in THETAS for rho in RHOS
        for policy in PHASE_POLICIES for seed in PHASE_SEEDS
    ]
    control_tasks = [
        (group, shape, policy, seed)
        for group in CONTROL_GROUPS for shape in CONTROL_GROUPS[group]
        for policy in CONTROL_POLICIES for seed in CONTROL_SEEDS
    ]
    print(
        f"E11: {len(phase_tasks)} phase reruns + "
        f"{len(control_tasks)} controls; workers={workers}"
    )
    for group, shapes in CONTROL_GROUPS.items():
        print(f"  {group}")
        for shape, spec in shapes.items():
            print(
                f"    {shape:>9}: needs={spec['needs']} "
                f"E[k]={np.dot(spec['needs'], spec['probs']):.12f} "
                f"p64={spec['probs'][-1]:.4f}"
            )

    rows = []
    t0 = time.time()
    for label, tasks, fn in [
        ("phase", phase_tasks, phase_one),
        ("control", control_tasks, control_one),
    ]:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for index, rec in enumerate(executor.map(fn, tasks), 1):
                rows.append(rec)
                if index % 30 == 0 or index == len(tasks):
                    print(
                        f"  {label} {index}/{len(tasks)} "
                        f"({time.time() - t0:.0f}s)", flush=True
                    )

    serial_groups = {
        group: {
            shape: {
                **spec,
                "needs": list(spec["needs"]),
                "probs": list(spec["probs"]),
            }
            for shape, spec in shapes.items()
        }
        for group, shapes in CONTROL_GROUPS.items()
    }
    output = os.path.join(HERE, "results", "E11.json")
    with open(output, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "config": {
                    "n_servers": N,
                    "n_jobs": N_JOBS,
                    "phase_thetas": THETAS,
                    "phase_rhos": RHOS,
                    "phase_policies": PHASE_POLICIES,
                    "phase_seeds": PHASE_SEEDS,
                    "control_rho": 0.85,
                    "control_policies": CONTROL_POLICIES,
                    "control_seeds": CONTROL_SEEDS,
                    "control_groups": serial_groups,
                    "pred_sha256": os.environ.get("PRED_SHA", ""),
                },
                "rows": rows,
            },
            handle,
            indent=1,
        )
    print(f"  wrote {output}")
