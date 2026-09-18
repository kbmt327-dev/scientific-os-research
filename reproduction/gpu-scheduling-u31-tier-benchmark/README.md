# GPU U-31 information-tier benchmark (EP-0021)

A re-executable projection of the sealed benchmark that scores three stability
diagnostics against a known synthetic label under one common observation window.

```bash
python reproduction/gpu-scheduling-u31-tier-benchmark/rerun_tier_benchmark.py --seeds 10
```

Unlike the earlier GPU projections in this repository, this one is not an
arithmetic verifier over recorded summaries. `rerun_tier_benchmark.py` carries
its own workload generator, its own first-come first-served M/M/4 oracle and all
three diagnostics, and regenerates every number it prints from the seed alone.
It reads no recorded trace, no private path and no work state. Running the full
sealed grid takes `--seeds 100 --horizons 20000 80000 320000`; the default is a
short subset so the script finishes in about a minute.

## What is being compared

The model is 64 identical servers where every job needs exactly 16 of them and
is never preempted, so four jobs run at once and the system is an M/M/4 queue
with load `rho`. The label is therefore known without asking any diagnostic:
`rho < 1` is subcritical, `rho > 1` is overloaded, and `rho = 1` is excluded.

Every method sees the same window, from time zero to the arrival of the h-th
job, but they are given deliberately different information.

| tier | information | output |
|---|---|---|
| O | arrivals and departures inside the window only | stable or unstable, never abstains |
| W | true required service of every offered job, all arrival gaps, known capacity | subcritical, overloaded or UNKNOWN |
| D | completion times of the same arrival cohort after it has drained, which happens after the cutoff | stable or unstable, never abstains |

Tier O is Algorithm AB of Wieland, Pasupathy and Schmeiser, *Queueing-Network
Stability: Simulation-Based Checking*, Proceedings of the 2003 Winter Simulation
Conference, 520-527, section 6.1. Its authors present it as an illustrative
example with no performance claim, so outscoring it is not a contribution. Two
points of that published specification are under-determined: the printed Step 3
variance formula squares the Step 2 difference and can be negative, and the
Step 4 statistic and the Section 6.2 p-value disagree by a factor. The script
uses the sample variance of the batch observations, reports the literal reading
alongside, and never uses the literal one for a label.

Tier W is the input load confidence interval used by the earlier episodes in
this project. Tier D is this project's own window-elasticity diagnostic at its
historical threshold 0.5, which had never been scored against a known label.

## The critical load

Passing `--rhos 1.0` runs the load the benchmark otherwise excludes, and the script
scores nothing there. At `rho = 1` the queue is null recurrent: the expected number
in the network grows like the square root of time, so its time average is infinite
and the model is unstable under the definition the primary source gives in its
section 1.5. At the same time the arrival and departure rates are equal, so the
asymptotic growth slope is exactly zero, which is the null hypothesis the O-tier
test checks. The sentence in section 3.3 that an unstable network has a positive
slope does not hold here. None of that is new queueing theory; the script just
lets you watch the two readings disagree on one model.

The same square-root growth puts the D-tier elasticity at exactly 0.5, which is the
threshold this project has used since its first experiments. The script prints the
declaration mix instead of a score, so you can see how each tier behaves when there
is no side to be on.

## How to read the output

The unit of replication is a seed. The three looks of one seed are nested
prefixes of the same run, so the horizons are not independent estimates of each
other and a look is not a replication. The `future work share` column is the
fraction of offered work still unfinished at the cutoff: it is information that
tier W must be handed and tier O cannot see, which is why a difference between
the tiers is a statement about cost, not a ranking.

## Limits

This is a re-execution, not an independent replication: the reader runs the same
design and the same generator logic on the same synthetic model. It establishes
no repeated-sampling coverage, no mixed-need capacity result, no general
stability detector, no scheduler comparison and nothing about real clusters. A
tier that abstains is not thereby correct, and a wrong-side count of zero in a
cell is bounded by the number of seeds, not by the method.
