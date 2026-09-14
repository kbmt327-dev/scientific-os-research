#!/usr/bin/env python3
"""Run the contract's invariants, and a negative control for each one.

A negative control here is a record the contract must refuse.  If a control
stops failing, the invariant it guards has quietly stopped working.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from contract import (  # noqa: E402
    Attribution,
    ContractError,
    InterventionSpec,
    Outcome,
    SealedPrediction,
    check_episode,
)

BASE = dict(
    action="route undecided items to a review queue",
    actor="operator",
    channel="share of items closed without a rule",
    direction="decrease",
    baseline_as_of="2026-09-01T00:00:00Z",
    decided_at="2026-09-14T00:00:00Z",
    expected_at="2026-12-01T00:00:00Z",
)


def spec(**overrides):
    return InterventionSpec(**{**BASE, **overrides})


def refuses(breach: str, label: str, call):
    try:
        call()
    except ContractError as exc:
        return {"breach": breach, "control": label, "refused": True, "reason": str(exc)}
    return {"breach": breach, "control": label, "refused": False, "reason": "accepted a record it must refuse"}


def main() -> int:
    controls = [
        refuses("B1", "an acting prediction resolved without the four-point joint", lambda: check_episode(
            [SealedPrediction(id="p1", target="Y", direction="decrease", registered_at="2026-09-14T00:00:00Z", intervention=spec())],
            [Outcome(id="o1", prediction_id="p1", status="supported")])),
        refuses("B1", "a decision that never opened used to refute the model", lambda: Outcome(
            id="o1", prediction_id="p1", status="falsified",
            attribution=Attribution(decision_opened=False, action_executed=False))),
        refuses("B1", "an action recorded as run without a decision", lambda: Attribution(
            decision_opened=False, action_executed=True)),
        refuses("B2", "the commitment stamped after the prediction was registered", lambda: SealedPrediction(
            id="p1", target="Y", direction="decrease", registered_at="2026-09-13T00:00:00Z", intervention=spec())),
        refuses("B2", "a pledge not to interfere made by someone who cannot", lambda: spec(
            stance="non_interference", predictor_is_actor=False)),
        refuses("B2", "a broken pledge scored as a result", lambda: Outcome(
            id="o1", prediction_id="p1", status="supported",
            attribution=Attribution(pledge_held=False, decision_opened=True))),
        refuses("B3", "an exogenous scoring date with no end to the waiting", lambda: spec(due_kind="exogenous")),
        refuses("B4", "a resume deadline that falls before the effect is expected", lambda: spec(
            due_kind="exogenous", resume_deadline="2026-10-01T00:00:00Z")),
        refuses("B5", "a baseline measured after the decision to act", lambda: spec(
            baseline_as_of="2026-09-20T00:00:00Z")),
    ]

    acting = SealedPrediction(id="p1", target="Y", direction="decrease",
                              registered_at="2026-09-14T00:00:00Z", intervention=spec())
    undue = Outcome(id="o1", prediction_id="p1", status="not_due",
                    attribution=Attribution(decision_opened=True, action_executed=False))
    check_episode([acting], [undue])

    observational = SealedPrediction(id="p2", target="Y", direction="increase",
                                     registered_at="2026-09-14T00:00:00Z")
    plain = Outcome(id="o2", prediction_id="p2", status="supported")
    check_episode([observational], [plain])

    positives = {
        "a scoring date that never came is recorded and does not score": undue.status == "not_due" and not undue.counts_toward_scoring,
        "an executed commitment that missed still scores": Outcome(
            id="o3", prediction_id="p1", status="falsified",
            attribution=Attribution(threshold_crossed=True, decision_opened=True, action_executed=True),
        ).counts_toward_scoring,
        "observational predictions need no attribution": plain.counts_toward_scoring,
    }

    result = {
        "package": "intervention-grammar",
        "all_passed": all(row["refused"] for row in controls) and all(positives.values()),
        "negative_controls": controls,
        "positive_checks": positives,
        "breaches_covered": sorted({row["breach"] for row in controls}),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
