"""Standalone re-execution of the GPU U-31 information-tier benchmark.

This file contains its own workload generator, its own M/M/4 first-come
first-served oracle and all three diagnostics. It imports nothing from the
private research tree, reads no private path, and needs no recorded trace: it
regenerates every number it prints from the seed alone.

    python rerun_tier_benchmark.py --seeds 10
    python rerun_tier_benchmark.py --seeds 100 --horizons 20000 80000 320000

What it is: a re-execution of the sealed protocol on the same synthetic model,
so a reader can obtain the wrong-side, UNKNOWN and cost numbers independently
of the recorded run artifact.

What it is not: an independent replication (the reader runs the same design and
the same generator logic), a real-cluster measurement, a coverage estimate, or
evidence that any of the three diagnostics generalises beyond fixed-need
synthetic M/M/4 labels. The tiers are given deliberately different information,
so a difference between them is a cost statement, not a ranking.

Requires numpy and scipy.
"""
from __future__ import annotations

import argparse
import heapq
import json
import math

import numpy as np
from scipy.stats import f as f_dist, t as student_t

N_SERVERS = 64
NEED = 16
SLOTS = N_SERVERS // NEED
MEAN_SERVICE = 1.0
BATCHES = 10
TEST_ALPHA = 0.05
PER_DECISION_ERROR = 0.05
ELASTICITY_RATIO = 4
ELASTICITY_WARMUP = 0.2
ELASTICITY_THRESHOLD = 0.5


def generate(n_jobs: int, rho: float, seed: int):
    """Poisson arrivals and exponential service for a fixed gang need.

    The draw order reproduces the private generator exactly, including the
    categorical draw for the job need. That draw is degenerate here because
    every job needs the same number of servers, but it still advances the
    bit generator, so removing it would change every later value.
    """
    rng = np.random.default_rng(seed)
    lam = rho * N_SERVERS / (NEED * MEAN_SERVICE)
    gaps = rng.exponential(1.0 / lam, n_jobs)
    arrival = np.cumsum(gaps)
    rng.choice((NEED,), size=n_jobs, p=(1.0,))
    size = rng.exponential(MEAN_SERVICE, n_jobs)
    return arrival, size


def oracle(arrival, size, slots=SLOTS):
    """Each job takes the slot that frees up first; arrival order is kept."""
    available = [0.0] * slots
    dep = np.empty(len(arrival))
    for i in range(len(arrival)):
        dep[i] = max(heapq.heappop(available), arrival[i]) + size[i]
        heapq.heappush(available, dep[i])
    return dep


def occupancy_integral(arrival, dep, t0, t1):
    return float(np.maximum(0.0, np.minimum(dep, t1) - np.maximum(arrival, t0)).sum())


def algorithm_ab(arrival, dep, tau, batches=BATCHES, alpha=TEST_ALPHA):
    """Algorithm AB of Wieland, Pasupathy and Schmeiser (WSC 2003), section 6.1.

    Tier O: only arrivals and departures inside the observation window are used.
    The printed Step 3 variance formula cannot be a variance, because the symbol
    it squares is the Step 2 difference; the sample variance of the b-1 batch
    observations is used instead and the literal reading is reported alongside.
    """
    width = tau / batches
    obs = np.array([occupancy_integral(arrival, dep, (j - 1) * width, j * width) / width
                    for j in range(2, batches + 1)])
    growth = float(obs[-1] - obs[0])
    variance = float(np.sum((obs - obs.mean()) ** 2) / (batches - 2))
    literal = float((np.sum(obs ** 2) - batches * growth ** 2) / (batches - 2))
    critical = float(student_t.ppf(1 - alpha, batches - 2))
    if not variance > 0:
        return dict(label='overloaded' if growth > 0 else 'subcritical', growth=growth,
                    statistic=None, literal_variance=literal, degenerate=True)
    statistic = growth / (math.sqrt(2) * math.sqrt(variance))
    return dict(label='overloaded' if statistic > critical else 'subcritical', growth=growth,
                statistic=statistic, literal_variance=literal, degenerate=False)


def input_confidence(work, elapsed, count, error=PER_DECISION_ERROR, slots=SLOTS):
    """Tier W: needs the true service of every offered job, finished or not."""
    qlow, qhigh = f_dist.ppf([error / 2, 1 - error / 2], 2 * count, 2 * count)
    ratio = work / (slots * elapsed)
    low, high = ratio / qhigh, ratio / qlow
    return dict(label='overloaded' if low > 1 else ('subcritical' if high < 1 else 'UNKNOWN'),
                load_estimate=float(ratio), ci_low=float(low), ci_high=float(high))


def window_elasticity(arrival, dep, horizon, threshold=ELASTICITY_THRESHOLD):
    """Tier D: needs the same arrival cohort to have drained, which happens after the cutoff."""
    def cohort_mean(k):
        start = int(ELASTICITY_WARMUP * k)
        return float(np.mean(dep[start:k] - arrival[start:k]))
    small = cohort_mean(max(2, int(horizon / ELASTICITY_RATIO)))
    large = cohort_mean(horizon)
    alpha = (math.log(large) - math.log(small)) / math.log(ELASTICITY_RATIO)
    return dict(label='overloaded' if alpha >= threshold else 'subcritical', alpha=float(alpha))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--rhos', type=float, nargs='+', default=[0.8, 0.95, 0.99, 1.01, 1.05, 1.2])
    p.add_argument('--horizons', type=int, nargs='+', default=[20000, 80000])
    p.add_argument('--seeds', type=int, default=10, help='number of seeds, starting at --first-seed')
    p.add_argument('--first-seed', type=int, default=5001)
    p.add_argument('--generated-horizon', type=int, default=320000,
                   help='arrivals drawn per seed. The sealed run drew 320000 and read shorter '
                        'looks as prefixes of it. Lowering this draws a different stream, so the '
                        'numbers will no longer match the recorded ones.')
    p.add_argument('--out', default='')
    args = p.parse_args()

    seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    generated = max(args.generated_horizon, max(args.horizons))
    if generated != 320000:
        print('note: drawing %d arrivals per seed instead of the sealed 320000, so these numbers '
              'are a different sample, not a reproduction of the recorded run.\n' % generated)
    rows = []
    critical_rows = []
    print('rho    look     truth        AB wrong  FCI wrong  FCI UNKNOWN  ALPHA wrong  future work share')
    for rho in args.rhos:
        critical = rho == 1.0
        truth = 'critical' if critical else ('subcritical' if rho < 1 else 'overloaded')
        tally = {h: dict(AB=0, FCIw=0, FCIu=0, ALPHA=0, share=[], mix={}, alphas=[]) for h in args.horizons}
        for h in args.horizons:
            tally[h]['mix'] = {n: dict(subcritical=0, overloaded=0, UNKNOWN=0)
                               for n in ('AB', 'FCI', 'ALPHA')}
        for seed in seeds:
            arrival, size = generate(generated, rho, seed)
            dep = oracle(arrival, size)
            for h in args.horizons:
                tau = float(arrival[h - 1])
                ab = algorithm_ab(arrival[:h], dep[:h], tau)
                fci = input_confidence(float(size[:h].sum()), tau, h)
                el = window_elasticity(arrival, dep, h)
                incomplete = dep[:h] > tau
                share = float(size[:h][incomplete].sum() / size[:h].sum())
                for name, label in (('AB', ab['label']), ('FCI', fci['label']), ('ALPHA', el['label'])):
                    tally[h]['mix'][name][label] += 1
                if not critical:
                    tally[h]['AB'] += ab['label'] != truth
                    tally[h]['FCIw'] += fci['label'] not in (truth, 'UNKNOWN')
                    tally[h]['ALPHA'] += el['label'] != truth
                tally[h]['FCIu'] += fci['label'] == 'UNKNOWN'
                tally[h]['share'].append(share)
                tally[h]['alphas'].append(el['alpha'])
                rows.append(dict(rho=rho, horizon=h, seed=seed, truth=truth, tau=tau,
                                 future_work_share=share, ab=ab, fci=fci, alpha=el))
        for h in args.horizons:
            t = tally[h]
            if critical:
                # No declaration is scored here: the published definition calls this load
                # unstable, while the criterion the O-tier test uses is satisfied by it.
                print('%-6s %-8d %-12s %-9s %-10s %-12d %-12s %.5f'
                      % (rho, h, truth, '-', '-', t['FCIu'], '-', float(np.median(t['share']))))
                critical_rows.append((h, t['mix'], float(np.median(t['alphas']))))
            else:
                print('%-6s %-8d %-12s %-9d %-10d %-12d %-12d %.5f'
                      % (rho, h, truth, t['AB'], t['FCIw'], t['FCIu'], t['ALPHA'],
                         float(np.median(t['share']))))

    if critical_rows:
        print('\ncritical load rho=1: declaration mix (no answer is scored correct here)')
        print('look     method  subcritical  overloaded  UNKNOWN   median elasticity')
        for h, mix, med in critical_rows:
            for name in ('AB', 'FCI', 'ALPHA'):
                print('%-8d %-7s %-12d %-11d %-9d %.4f'
                      % (h, name, mix[name]['subcritical'], mix[name]['overloaded'],
                         mix[name]['UNKNOWN'], med))
        print('At this load the queue is null recurrent: the time-average expected number in the '
              'network is infinite, so the model is unstable under the definition, while arrival '
              'and departure rates are equal, so the growth slope the O-tier test checks is zero.')

    print('\nseeds per cell: %d (the unit of replication). Looks of one seed are nested prefixes'
          ' of one run and are not independent.' % len(seeds))
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as handle:
            json.dump(rows, handle, ensure_ascii=False, indent=1)
        print('wrote %s' % args.out)


if __name__ == '__main__':
    main()
