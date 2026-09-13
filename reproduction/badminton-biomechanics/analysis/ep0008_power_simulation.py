"""Monte Carlo power sensitivity for the planned balanced within-subject 2x2 study.

The simulation works on subject-level orthogonal contrasts. Participant
intercepts cancel in a balanced within-subject contrast. The remaining
uncertainty is a participant-specific random slope plus trial residual error.
This is a sensitivity analysis, not a final sample-size calculation: the
random-slope SD and minimum effect of interest still require a feasibility
pilot or an external empirical basis.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Scenario:
    contrast: str
    participants: int
    trials_per_cell: int
    effect_sd: float
    contrast_sd: float
    power: float
    monte_carlo_se: float


def simulate_power(
    *,
    rng: np.random.Generator,
    iterations: int,
    participants: int,
    trials_per_cell: int,
    effect_sd: float,
    random_slope_sd: float,
    residual_sd: float,
    residual_multiplier: float,
    alpha: float,
) -> tuple[float, float, float]:
    """Return power, Monte Carlo SE, and subject-level contrast SD."""

    contrast_variance = random_slope_sd**2 + (
        residual_multiplier * residual_sd**2 / trials_per_cell
    )
    contrast_sd = float(np.sqrt(contrast_variance))
    draws = rng.normal(
        loc=effect_sd,
        scale=contrast_sd,
        size=(iterations, participants),
    )
    means = draws.mean(axis=1)
    sample_sd = draws.std(axis=1, ddof=1)
    t_stat = means / (sample_sd / np.sqrt(participants))
    p_value = 2.0 * stats.t.sf(np.abs(t_stat), df=participants - 1)
    power = float(np.mean(p_value < alpha))
    mc_se = float(np.sqrt(power * (1.0 - power) / iterations))
    return power, mc_se, contrast_sd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20_260_913)
    args = parser.parse_args()

    if args.iterations < 1_000:
        raise SystemExit("--iterations must be at least 1000")

    participants_grid = [12, 16, 20, 24, 30, 36, 48]
    trials_grid = [4, 6, 8]
    effect_grid = [0.20, 0.30, 0.40, 0.50]
    residual_sd = 1.0
    random_slope_sd = 0.20
    familywise_alpha = 0.05
    number_of_coprimary_tests = 3
    alpha_per_test = familywise_alpha / number_of_coprimary_tests

    # A main effect averages two cell means at each factor level, so its
    # residual variance multiplier is 1. A difference-in-differences
    # interaction uses four cell means with weights +/-1, giving multiplier 4.
    contrast_specs = {
        "main_effect": 1.0,
        "interaction": 4.0,
    }

    rng = np.random.default_rng(args.seed)
    scenarios: list[Scenario] = []
    for contrast, residual_multiplier in contrast_specs.items():
        for trials_per_cell in trials_grid:
            for effect_sd in effect_grid:
                for participants in participants_grid:
                    power, mc_se, contrast_sd = simulate_power(
                        rng=rng,
                        iterations=args.iterations,
                        participants=participants,
                        trials_per_cell=trials_per_cell,
                        effect_sd=effect_sd,
                        random_slope_sd=random_slope_sd,
                        residual_sd=residual_sd,
                        residual_multiplier=residual_multiplier,
                        alpha=alpha_per_test,
                    )
                    scenarios.append(
                        Scenario(
                            contrast=contrast,
                            participants=participants,
                            trials_per_cell=trials_per_cell,
                            effect_sd=effect_sd,
                            contrast_sd=round(contrast_sd, 6),
                            power=round(power, 4),
                            monte_carlo_se=round(mc_se, 6),
                        )
                    )

    threshold_rows = []
    for contrast in contrast_specs:
        for trials_per_cell in trials_grid:
            for effect_sd in effect_grid:
                matching = [
                    row
                    for row in scenarios
                    if row.contrast == contrast
                    and row.trials_per_cell == trials_per_cell
                    and row.effect_sd == effect_sd
                    and row.power >= 0.80
                ]
                threshold_rows.append(
                    {
                        "contrast": contrast,
                        "trials_per_cell": trials_per_cell,
                        "effect_sd": effect_sd,
                        "minimum_grid_n_for_80pct": (
                            min(row.participants for row in matching)
                            if matching
                            else None
                        ),
                    }
                )

    result = {
        "schema_version": "iaa.ep0008.power-sensitivity.v1",
        "status": "sensitivity_only_not_final_sample_size",
        "seed": args.seed,
        "iterations_per_scenario": args.iterations,
        "analysis_unit": "participant-level balanced orthogonal contrast",
        "test": "two-sided one-sample t test on each participant contrast",
        "multiplicity": {
            "familywise_alpha": familywise_alpha,
            "coprimary_tests": number_of_coprimary_tests,
            "per_test_alpha_bonferroni": alpha_per_test,
        },
        "assumptions": {
            "trial_residual_sd": residual_sd,
            "participant_random_slope_sd": random_slope_sd,
            "balanced_complete_cells": True,
            "main_effect_residual_variance_multiplier": 1.0,
            "interaction_residual_variance_multiplier": 4.0,
            "effect_scale": "difference in trial-residual SD units",
        },
        "grids": {
            "participants": participants_grid,
            "trials_per_cell": trials_grid,
            "effect_sd": effect_grid,
        },
        "minimum_grid_n_for_80pct": threshold_rows,
        "scenarios": [asdict(row) for row in scenarios],
        "limitations": [
            "Random-slope SD is an explicit assumption, not an empirical estimate from the new protocol.",
            "Balanced complete cells are assumed; missing trials and unusable impacts will reduce information.",
            "The simulation does not model period, fatigue, carry-over, or heteroscedasticity.",
            "A feasibility pilot must freeze the minimum effect of interest before choosing sample size.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
