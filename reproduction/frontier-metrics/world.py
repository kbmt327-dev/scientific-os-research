"""A standalone copy of the world whose two headline results were retracted.

Transactions arrive carrying a judgement type. A type that already has a rule is
handled by machine; a type without one joins a judgement queue, where a person
either turns it into a reusable rule or records it as a one-off.

Types come from a two-parameter Chinese restaurant process. Its discount `d` is
the frontier:

    d = 0    distinct types grow like log(n). The frontier closes; given enough
             time every transaction is a repeat and automation can finish.
    d > 0    distinct types grow like n^d. Novel types keep arriving forever,
             however many rules exist.

Standard library only. No real data of any kind is used or included.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass
class Config:
    weeks: int = 260
    arrivals_per_week: float = 400.0
    theta: float = 30.0
    discount: float = 0.0
    capacity_ratio: float = 4.0
    p_called_idiosyncratic: float = 0.05
    warmup_weeks: int = 60


class Restaurant:
    """Two-parameter Chinese restaurant process over transaction types."""

    def __init__(self, theta: float, discount: float, rng: random.Random) -> None:
        self.theta, self.discount, self.rng = theta, discount, rng
        self.past: list[int] = []
        self.counts: dict[int, int] = {}
        self.n_types = 0

    def draw(self) -> int:
        n = len(self.past)
        novel_mass = self.theta + self.discount * self.n_types
        if n == 0 or self.rng.random() < novel_mass / (self.theta + n):
            type_id = self.n_types
            self.n_types += 1
            self.counts[type_id] = 1
            self.past.append(type_id)
            return type_id
        while True:
            type_id = self.past[self.rng.randrange(n)]
            count = self.counts[type_id]
            if self.discount == 0.0 or self.rng.random() < (count - self.discount) / count:
                self.counts[type_id] = count + 1
                self.past.append(type_id)
                return type_id


def _poisson(rng: random.Random, mean: float) -> int:
    if mean > 30:
        return max(0, int(round(rng.gauss(mean, math.sqrt(mean)))))
    limit, count, product = math.exp(-mean), 0, 1.0
    while True:
        product *= rng.random()
        if product <= limit:
            return count
        count += 1


def run(config: Config, seed: int) -> dict:
    """Returns the settling rate and the mean reuse of the rules that were made."""
    rng = random.Random(seed)
    restaurant = Restaurant(config.theta, config.discount, rng)
    ruled: dict[int, int] = {}          # type -> transactions handled after its rule existed
    first_seen: dict[int, int] = {}
    queue: list[tuple[int, int]] = []
    processed = settled = 0
    tokens = 0.0
    recent: list[int] = []
    measured = max(1, config.weeks - config.warmup_weeks)

    for week in range(config.weeks):
        measuring = week >= config.warmup_weeks
        week_inflow = 0
        for _ in range(_poisson(rng, config.arrivals_per_week)):
            type_id = restaurant.draw()
            first_seen.setdefault(type_id, week)
            if type_id in ruled:
                ruled[type_id] += 1
                continue
            queue.append((type_id, week))
            week_inflow += 1

        recent.append(week_inflow)
        trailing = sum(recent[-12:]) / len(recent[-12:])
        tokens += config.capacity_ratio * trailing
        capacity = int(tokens)
        tokens -= capacity

        for _ in range(min(capacity, len(queue))):
            type_id, enqueued = queue.pop(0)
            if measuring:
                processed += 1
            if type_id in ruled:
                continue
            # The ONLY route from a judgement to a non-rule in this world.
            one_off = rng.random() < config.p_called_idiosyncratic and first_seen[type_id] == enqueued
            if not one_off:
                ruled[type_id] = 0
                if measuring:
                    settled += 1

    reuse = list(ruled.values())
    return {
        "settling_rate": settled / processed if processed else 0.0,
        "rule_reuse_mean": sum(reuse) / len(reuse) if reuse else 0.0,
        "distinct_types": restaurant.n_types,
    }


def discount_estimate(theta: float, discount: float, n: int, seed: int) -> float:
    """Slope of log K(n) against log n over the last decade of the growth curve."""
    import statistics

    rng = random.Random(seed)
    restaurant = Restaurant(theta, discount, rng)
    marks = sorted({int(n * frac) for frac in (0.10, 0.28, 0.46, 0.64, 0.82, 1.0)})
    points: list[tuple[int, int]] = []
    wanted = set(marks)
    for index in range(1, n + 1):
        restaurant.draw()
        if index in wanted and restaurant.n_types > 1:
            points.append((index, restaurant.n_types))
    xs = [math.log(a) for a, _ in points]
    ys = [math.log(b) for _, b in points]
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom if denom else 0.0
