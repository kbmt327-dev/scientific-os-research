"""A prediction contract for domains where the predictor also acts.

Standalone reference implementation: no dependencies beyond the standard
library, and no connection to the private research runtime.  It exists so a
reader can run the invariants rather than take our word for them.

The observational form of a sealed prediction assumes the world does not move
because we predicted it.  Five of its assumptions stop holding once the
prediction is attached to an action:

  B1  attribution   a miss no longer separates "the model was wrong" from
                    "nobody acted"
  B2  reflexivity   the predictor can go and make its own prediction false
  B3  exogenous due the scoring date is not ours to choose
  B4  waiting       "wait" is a legitimate ending under observation and a
                    stall under intervention
  B5  non-stationarity  success moves the distribution being measured

Each is answered below by a field plus an invariant that refuses the record
rather than by a convention someone has to remember.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


class ContractError(ValueError):
    """A record that the contract refuses to accept."""


def _time(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:  # pragma: no cover - message only
        raise ContractError(f"{name} is not a timestamp: {value!r}") from exc
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


DIRECTIONS = ("increase", "decrease", "unchanged")
DUE_KINDS = ("endogenous", "exogenous")
STANCES = ("commitment", "non_interference")
OUTCOME_STATUSES = ("supported", "falsified", "unresolved", "insufficient_evidence", "not_due", "out_of_scope")
SCORED = ("supported", "falsified")


@dataclass(frozen=True)
class InterventionSpec:
    """What is being done, by whom, against which baseline, and by when."""

    action: str
    actor: str
    channel: str
    direction: str
    decided_at: str
    expected_at: str
    baseline_as_of: str
    due_kind: str = "endogenous"
    predictor_is_actor: bool = True
    stance: str = "commitment"
    side_effects: tuple[str, ...] = ()
    not_taken: tuple[str, ...] = ()
    resume_deadline: str | None = None

    def __post_init__(self) -> None:
        for name, allowed in (("direction", DIRECTIONS), ("due_kind", DUE_KINDS), ("stance", STANCES)):
            if getattr(self, name) not in allowed:
                raise ContractError(f"{name} must be one of {allowed}")
        for name in ("action", "actor", "channel"):
            if not str(getattr(self, name)).strip():
                raise ContractError(f"{name} must not be empty")
        # B5: a baseline measured after we decided to act is not a baseline.
        if _time(self.baseline_as_of, "baseline_as_of") > _time(self.decided_at, "decided_at"):
            raise ContractError("baseline_as_of must not be after decided_at")
        if _time(self.decided_at, "decided_at") > _time(self.expected_at, "expected_at"):
            raise ContractError("decided_at must not be after expected_at")
        # B2: pledging not to interfere is empty unless we are the ones who could.
        if self.stance == "non_interference" and not self.predictor_is_actor:
            raise ContractError("stance='non_interference' requires predictor_is_actor")
        # B3/B4: if the due date is not ours, the waiting still needs an end.
        if self.due_kind == "exogenous" and self.resume_deadline is None:
            raise ContractError("due_kind='exogenous' requires resume_deadline")
        if self.resume_deadline is not None and _time(self.resume_deadline, "resume_deadline") < _time(self.expected_at, "expected_at"):
            raise ContractError("resume_deadline must not be before expected_at")


@dataclass(frozen=True)
class Attribution:
    """The four-point joint without which an acting prediction cannot be scored."""

    threshold_crossed: bool | None = None
    decision_opened: bool | None = None
    action_executed: bool | None = None
    pledge_held: bool | None = None
    baseline_as_of: str | None = None

    def __post_init__(self) -> None:
        if self.action_executed and self.decision_opened is False:
            raise ContractError("action_executed cannot be true while decision_opened is false")


@dataclass(frozen=True)
class SealedPrediction:
    id: str
    target: str
    direction: str
    registered_at: str
    intervention: InterventionSpec | None = None

    def __post_init__(self) -> None:
        if self.intervention is None:
            return
        # B2: the expectation is stamped when we commit, never afterwards.
        if _time(self.intervention.decided_at, "decided_at") > _time(self.registered_at, "registered_at"):
            raise ContractError("decided_at cannot be after the prediction was registered")


@dataclass(frozen=True)
class Outcome:
    id: str
    prediction_id: str
    status: str
    attribution: Attribution | None = None
    metrics: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in OUTCOME_STATUSES:
            raise ContractError(f"status must be one of {OUTCOME_STATUSES}")
        if self.attribution is None:
            return
        # B1: a decision that never opened never put the model on trial.
        if self.attribution.decision_opened is False and self.status in SCORED:
            raise ContractError("cannot claim supported/falsified when decision_opened is false")
        # B2: breaking a non-interference pledge makes the reading uninterpretable.
        if self.attribution.pledge_held is False and self.status != "unresolved":
            raise ContractError("outcome must be unresolved when a non-interference pledge was broken")

    @property
    def counts_toward_scoring(self) -> bool:
        """A scoring date that never arrived is a recorded result, not a score."""
        return self.status in SCORED


def check_episode(predictions, outcomes) -> None:
    """An acting prediction cannot be resolved without its four-point joint."""
    acting = {row.id: row.intervention for row in predictions if row.intervention is not None}
    for outcome in outcomes:
        spec = acting.get(outcome.prediction_id)
        if spec is None:
            continue
        if outcome.attribution is None:
            raise ContractError(f"outcome {outcome.id} resolves an acting prediction and requires attribution")
        if spec.stance == "non_interference" and outcome.attribution.pledge_held is None:
            raise ContractError(f"outcome {outcome.id} must record whether the pledge held")
        if spec.stance == "commitment" and outcome.attribution.action_executed is None:
            raise ContractError(f"outcome {outcome.id} must record whether the action was executed")
