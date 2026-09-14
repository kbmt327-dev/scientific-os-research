#!/usr/bin/env python3
"""Run the two attacks that took down both headline results.

Each attack is a sweep over a quantity that was held at a single value when the
result was published. If the published claim had been robust, neither sweep
would change it.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from world import Config, discount_estimate, run  # noqa: E402

SEEDS = range(1, 9)
ESTIMATOR_SEEDS = range(1, 16)


def attack_one() -> dict:
    """Is the settling rate blind to the frontier, or pinned by a constant?

    The only route from a judgement to a non-rule is p_called_idiosyncratic.
    Sweep it. If the settling rate simply tracks 1 - p, it was never measuring
    the frontier and the published blindness is an artifact.
    """
    rows = []
    for p in (0.02, 0.05, 0.15, 0.30):
        closed = statistics.fmean(
            run(Config(discount=0.0, p_called_idiosyncratic=p), s)["settling_rate"] for s in SEEDS)
        open_ = statistics.fmean(
            run(Config(discount=0.6, p_called_idiosyncratic=p), s)["settling_rate"] for s in SEEDS)
        rows.append({"p": p, "one_minus_p": round(1 - p, 4),
                     "settling_closed": round(closed, 4), "settling_open": round(open_, 4),
                     "gap": round(open_ - closed, 4)})
    # Compare how far the constant we chose moves the metric against how far the
    # thing we claimed to be measuring moves it. An absolute tolerance on
    # "settling rate equals 1 - p" was the wrong test: the offset grows with p,
    # so a badly placed threshold hid the point. The point is the ratio.
    swept = max(row["settling_closed"] for row in rows) - min(row["settling_closed"] for row in rows)
    frontier = max(abs(row["gap"]) for row in rows)
    sign_unstable = len({row["gap"] > 0 for row in rows}) > 1
    return {"rows": rows,
            "range_moved_by_the_constant_we_chose": round(swept, 4),
            "largest_move_by_the_frontier": round(frontier, 4),
            "ratio": round(swept / frontier, 1) if frontier else None,
            "frontier_gap_sign_is_unstable": sign_unstable,
            "verdict": "retracted" if swept > 5 * frontier and sign_unstable else "survives"}


def attack_two() -> dict:
    """Is the decision line a property of sample size, or of an unobservable?

    The estimator was characterised at theta = 30 and the line published as if it
    depended on n alone. Sweep theta at a frontier that fully closes. If the null
    crosses the published line, a closing frontier gets declared open.
    """
    published_line = 0.283
    rows = []
    for theta in (5, 15, 30, 100, 300):
        values = [discount_estimate(theta, 0.0, 10000, s) for s in ESTIMATOR_SEEDS]
        mean, sd = statistics.fmean(values), statistics.pstdev(values)
        rows.append({"theta": theta, "null_mean": round(mean, 4), "null_sd": round(sd, 4),
                     "own_line": round(mean + 3 * sd, 4),
                     "clears_published_line": mean > published_line})
    open_world = statistics.fmean(discount_estimate(30, 0.3, 10000, s) for s in ESTIMATOR_SEEDS)
    confounded = [row["theta"] for row in rows if abs(row["null_mean"] - open_world) < 0.05]
    return {"published_line": published_line, "rows": rows,
            "truly_open_estimate_at_theta_30": round(open_world, 4),
            "closing_frontier_clears_the_line_at": [r["theta"] for r in rows if r["clears_published_line"]],
            "confounded_with_a_truly_open_frontier_at": confounded,
            "verdict": "retracted" if any(r["clears_published_line"] for r in rows) else "survives"}


def survivor() -> dict:
    """What was not an artifact: reuse responds to the frontier."""
    closed = statistics.fmean(run(Config(discount=0.0), s)["rule_reuse_mean"] for s in SEEDS)
    open_ = statistics.fmean(run(Config(discount=0.6), s)["rule_reuse_mean"] for s in SEEDS)
    return {"reuse_closed": round(closed, 2), "reuse_open": round(open_, 2),
            "ratio": round(open_ / closed, 4) if closed else None,
            "verdict": "survives" if open_ < 0.2 * closed else "does not survive"}


def main() -> int:
    result = {
        "package": "frontier-metrics",
        "attack_1_settling_rate_pinned_by_a_constant": attack_one(),
        "attack_2_decision_line_depends_on_an_unobservable": attack_two(),
        "survivor_reuse_responds_to_the_frontier": survivor(),
    }
    result["both_headline_results_retracted"] = (
        result["attack_1_settling_rate_pinned_by_a_constant"]["verdict"] == "retracted"
        and result["attack_2_decision_line_depends_on_an_unobservable"]["verdict"] == "retracted")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
