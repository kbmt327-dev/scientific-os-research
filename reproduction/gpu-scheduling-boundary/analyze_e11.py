"""Grade sealed PRED-010 against results/E11.json."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, "results", name), encoding="utf-8") as handle:
        return json.load(handle)


E11 = load("E11.json")
E2 = load("E2.json")
phase = [row for row in E11["rows"] if row["arm"] == "phase_remeasurement"]
controls = [row for row in E11["rows"] if row["arm"] == "equal_summary_control"]
results = []


def mean(rows, key):
    return float(np.mean([row[key] for row in rows]))


def flow64(row):
    values = row["flow_balance_by_need"]
    value = values.get("64", values.get(64))
    return float(value) if value is not None else float("nan")


def rec(pred_id, claim, passed, detail):
    results.append({"id": pred_id, "claim": claim, "pass": bool(passed), "detail": detail})
    print(f"{pred_id}: {'PASS' if passed else 'FAIL'} -- {detail}")


# Y1: exact deterministic replay, excluding newly retained mean_running.
old_index = {
    (row["theta"], row["rho"], row["policy"], row["seed"]): row
    for row in E2["rows"] if row["policy"] in {"srpt", "sf_srpt"}
}
acceptance_keys = [
    "mean_jct", "utilization", "rho_emp", "min_flow_balance",
]
max_diff = 0.0
flow_max_diff = 0.0
missing = []
for row in phase:
    key = (row["theta"], row["rho"], row["policy"], row["seed"])
    old = old_index.get(key)
    if old is None:
        missing.append(key)
        continue
    for metric in acceptance_keys:
        a, b = float(row[metric]), float(old[metric])
        if math.isnan(a) and math.isnan(b):
            diff = 0.0
        else:
            diff = abs(a - b)
        max_diff = max(max_diff, diff)
    all_needs = set(row["flow_balance_by_need"]) | set(old["flow_balance_by_need"])
    for need in all_needs:
        a = row["flow_balance_by_need"].get(need)
        b = old["flow_balance_by_need"].get(need)
        if a is None or b is None:
            flow_max_diff = float("inf")
        else:
            flow_max_diff = max(flow_max_diff, abs(float(a) - float(b)))
y1 = not missing and max(max_diff, flow_max_diff) <= 1e-12
rec(
    "Y1", "exact E2 replay reproduces the old metrics", y1,
    f"max scalar diff={max_diff:.3g}; max flow diff={flow_max_diff:.3g}; missing={len(missing)}",
)


def phase_cell(theta, rho, policy):
    return [
        row for row in phase
        if row["theta"] == theta and row["rho"] == rho and row["policy"] == policy
    ]


thetas = E11["config"]["phase_thetas"]
rhos = E11["config"]["phase_rhos"]
phase_table = {}
y2_parts = []
print("\nPhase remeasurement (mean_running):")
for rho in rhos:
    values = [mean(phase_cell(theta, rho, "sf_srpt"), "mean_running") for theta in thetas]
    endpoint_ratio = values[0] / values[-1]
    decreasing = all(a > b for a, b in zip(values, values[1:]))
    y2_parts.append(decreasing and endpoint_ratio >= 10)
    print(
        f"  rho={rho}: " + "  ".join(f"{theta}:{value:.2f}" for theta, value in zip(thetas, values))
        + f"  endpoint={endpoint_ratio:.1f}x"
    )
    for theta, value in zip(thetas, values):
        phase_table[f"{theta}|{rho}|sf_srpt"] = value
rec(
    "Y2", "theta was strongly confounded with running-job concurrency",
    all(y2_parts), f"per-rho checks={y2_parts}",
)


starved_concurrency = []
healthy_concurrency = []
cell_details = []
for rho in rhos:
    for theta in thetas:
        rows = phase_cell(theta, rho, "srpt")
        fb = float(np.nanmean([flow64(row) for row in rows]))
        concurrency = mean(rows, "mean_running")
        is_starved = fb < 0.5
        (starved_concurrency if is_starved else healthy_concurrency).append(concurrency)
        cell_details.append((theta, rho, concurrency, fb, is_starved))
y3 = bool(starved_concurrency and healthy_concurrency) and min(starved_concurrency) > max(healthy_concurrency)
rec(
    "Y3", "old greedy-SRPT class-starvation cells occupy the high-concurrency side",
    y3,
    f"starved concurrency range={min(starved_concurrency):.2f}..{max(starved_concurrency):.2f}; "
    f"healthy range={min(healthy_concurrency):.2f}..{max(healthy_concurrency):.2f}",
)


def control_cell(group, shape, policy):
    return [
        row for row in controls
        if row["group"] == group and row["shape"] == shape and row["policy"] == policy
    ]


control_summary = {}
group_checks = {}
print("\nEqual-summary controls under greedy SRPT:")
for group in ["mean4", "mean16"]:
    concurrencies, flows, classifications = [], [], []
    for shape in ["narrow", "geometric", "wide"]:
        rows = control_cell(group, shape, "srpt")
        concurrency = mean(rows, "mean_running")
        fb = float(np.nanmean([flow64(row) for row in rows]))
        jct = mean(rows, "mean_jct")
        concurrencies.append(concurrency)
        flows.append(fb)
        classifications.append(fb < 0.5)
        control_summary[f"{group}|{shape}|srpt"] = {
            "mean_running": concurrency, "fb64": fb, "mean_jct": jct,
        }
        print(f"  {group:>6} {shape:>9}: concurrency={concurrency:.3f} fb64={fb:.3f} JCT={jct:.3f}")
    relative_range = (max(concurrencies) - min(concurrencies)) / float(np.mean(concurrencies))
    flow_range = max(flows) - min(flows)
    matched = relative_range <= 0.10
    same_class = len(set(classifications)) == 1
    invariant = flow_range <= 0.15
    group_checks[group] = {
        "relative_concurrency_range": relative_range,
        "flow_range": flow_range,
        "matched": matched,
        "same_classification": same_class,
        "invariant_flow": invariant,
        "starved": classifications,
        "flows": flows,
        "concurrencies": concurrencies,
    }

y4 = all(
    check["matched"] and check["same_classification"] and check["invariant_flow"]
    for check in group_checks.values()
)
rec(
    "Y4", "two-number summary is sufficient across controlled background shapes",
    y4,
    "; ".join(
        f"{group}: conc_range={check['relative_concurrency_range']:.3f}, "
        f"flow_range={check['flow_range']:.3f}, same_class={check['same_classification']}"
        for group, check in group_checks.items()
    ),
)

y5 = all(group_checks["mean4"]["starved"]) and not any(group_checks["mean16"]["starved"])
rec(
    "Y5", "high-concurrency mean4 starves while low-concurrency mean16 does not",
    y5,
    f"mean4 starved={group_checks['mean4']['starved']}; mean16 starved={group_checks['mean16']['starved']}",
)

y6 = all(check["matched"] for check in group_checks.values())
rec(
    "Y6", "equal-summary controls match observed running-job concurrency",
    y6,
    "; ".join(
        f"{group} relative range={check['relative_concurrency_range']:.3f}"
        for group, check in group_checks.items()
    ),
)

easy_flows = {}
for group in ["mean4", "mean16"]:
    for shape in ["narrow", "geometric", "wide"]:
        rows = control_cell(group, shape, "easy_backfill")
        easy_flows[f"{group}|{shape}"] = float(np.nanmean([flow64(row) for row in rows]))
y7 = all(value >= 0.9 for value in easy_flows.values())
rec(
    "Y7", "EASY backfill remains class-healthy in every control", y7,
    ", ".join(f"{key}={value:.3f}" for key, value in easy_flows.items()),
)

if not y1:
    for item in results:
        if item["id"] in {"Y2", "Y3"}:
            item["grade_valid"] = False
            item["note"] = "sealed rule: Y1 failure blocks interpretation of phase remeasurement"

grading = {
    "detector": E11["config"],
    "n_pass": sum(item["pass"] for item in results),
    "n_total": len(results),
    "results": results,
    "phase_cells": [
        {
            "theta": theta, "rho": rho, "mean_running": concurrency,
            "fb64": fb, "class_starved": starved,
        }
        for theta, rho, concurrency, fb, starved in cell_details
    ],
    "control_summary": control_summary,
    "group_checks": group_checks,
    "easy_backfill_flows": easy_flows,
}
output = os.path.join(HERE, "results", "E11_grading.json")
with open(output, "w", encoding="utf-8") as handle:
    json.dump(grading, handle, indent=2)
print(f"\n{grading['n_pass']}/{grading['n_total']} PASS; wrote {output}")
