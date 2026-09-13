# GPU scheduling EP-0005 … EP-0013 reproduction

This package covers the arc in which the project's own boundary statistic was
found to be measuring the wrong thing, and was replaced.

| Study | What it did |
|---|---|
| EP-0005 | swept the safe ratio against pool size, and found it falls |
| EP-0006 | separated the confound it had declared: the driver is not pool size but the number of jobs concurrently competing for the pool |
| EP-0007 | measured the safe ratio where the real cluster actually sits, and corrected a mechanism claim carried for four studies |
| EP-0008 | broke the project's own headline result by changing only the granularity of the background |
| EP-0009 | re-placed the EP-0002 phase diagram on the concurrency axis |
| EP-0010 | full factorial: the frequency of the largest class is a third variable, and the background family is a fourth |
| EP-0011 | audited the detector itself and found it blind to divergence |
| EP-0012 | sealed and validated the replacement statistic, and restored the operational numbers |
| EP-0013 | measured the real trace's frequency axis, with no simulation |

It is a separate package from `reproduction/gpu-scheduling-phase/`, which stays
pinned to the E2–E6 simulator and analyses. Nothing here supersedes that one:
the earlier package is the record of what was believed at the time, which is
precisely what EP-0011 revised.

## The result this package exists for

`flow_balance` — completions inside the measurement window divided by arrivals
inside it — was the statistic behind every operational number this project
published between EP-0004 and EP-0010. EP-0011 showed it is a right-censoring
ratio. With stationary arrivals over a window of length `W`,

```
1 - flow_balance = E[min(T, W)] / W
```

with no free parameter. `W` is proportional to the horizon, and so is the mean
response time `T` of a diverging class, so the ratio does not move. Over a 4×
horizon the largest class's mean response time grew 3.9× while its flow balance
moved from 0.562 to 0.574.

**A statistic normalised by the observation window being insensitive to the
horizon is not evidence that it is robust.**

The replacement is `alpha`, the elasticity of the class's mean response time
with respect to the observation window:

```
alpha = d log E[T] / d log horizon        0 = converged,  1 = linear divergence
```

EP-0012 measured it over four horizons (30k…240k jobs) and eight seeds. It reads
−0.05…+0.03 where the system is plainly stable, 0.90…0.98 where it plainly is
not, moves the boundary by at most 0.02 when the horizon is multiplied by eight,
and gives a 90% bootstrap interval of ±0.02.

## Environment

- Python 3.11+
- NumPy and SciPy (pinned by the repository-level `requirements-reproduce.txt`)

## Quick evidence check

From the repository root:

```bash
python scripts/reproduce.py --quick gpu-boundary
```

This verifies the nine sealed prediction digests against the `.sha256` files
committed before each sweep ran, then re-derives the three load-bearing facts
from the stored results: that flow balance stayed flat across a 3.9× divergence,
that `alpha` reads 0 at a half-pool class and 1 at a whole-pool class in every
condition while its boundary survives the horizon extension, and that exactly
one job in 19,100 carries the real-cluster claim.

## Full rerun

```bash
cd reproduction/gpu-scheduling-boundary
python run_e12.py      # EP-0010, 496 runs, ~2 min on 8 workers
python analyze_e12.py
python run_e13.py      # EP-0011, 648 runs, ~11 min
python analyze_e13.py
python run_e14.py      # EP-0012, 1440 runs, ~57 min
python analyze_e14.py
```

`run_e15.py` (EP-0013) reads the Philly trace and runs no simulation. The raw
trace is not redistributed here; fetch it from `msr-fiddle/philly-traces` and
place `cluster_job_log` at `data/trace-data/`. The derived per-virtual-cluster
measurements it produced are committed at `results/E15.json`.

Each `run_e*.py` writes `results/E*.json`; each `analyze_e*.py` grades the
sealed prediction and writes `results/E*_grading.json`. The analysis scripts for
E12, E13 and E14 were committed in the same commit as their prediction file,
before the corresponding result file existed. The one for E15 was not — that
lapse is recorded in `results/E15_grading.json` as
`grading_script_not_sealed: true`.

## Instrument calibration

```bash
python calib/c07_detector_registry.py
python calib/c07_detector_registry.py --selftest
```

`c07` is the remedy this arc produced. Three times a detector rather than the
physics decided a published conclusion, and writing the lesson down was not
enough — nor was moving it into code, because nobody enumerated the places the
lesson applied. `c07` is that enumeration, and it fails when the enumeration
goes stale. Its four checks:

- **A** every detector marked validated carries both a horizon audit and a
  threshold audit;
- **B** every (statistic, numeric threshold) pair in the analysis code is
  registered or explicitly attributed to a sealed prediction — a new constant in
  a new `analyze_*.py` fails this until someone writes down what it is;
- **C** a window-normalised statistic may not be marked validated on the
  strength of horizon-insensitivity, which is the exact inference EP-0011 showed
  to be wrong;
- **D** a filter that returns zero items while the maximum observed value grazes
  the cut is a threshold artifact, not a result. This one was added because
  EP-0013 rounded a measured ratio of 0.5899 to "0.59", and the cut excluded the
  single job that produced the ratio.

`--selftest` proves each check can fire. A first version of check D scanned the
sealed prediction files for numbers appearing as both a threshold and a
measurement; it fired 46 times, almost all on grid values, and was replaced.
A check that fires on everything gets ignored, which is the failure mode the
file exists to prevent.

## What is in here

```
predictions/   PRED-006 … PRED-014 and their digests, each committed before its
               sweep ran
results/       raw sweep output and the grading file for each study
run_e*.py      the sweeps
analyze_e*.py  the graders, written against the sealed criteria
sim/           the multiserver-job simulator, policies and analytic checks
calib/         instrument calibration, including the detector registry
measure_vc_concurrency.py
               places the Philly virtual clusters on the concurrency axis
adjudicate.py  the two-horizon stability adjudication from EP-0002
```

## What this package is not

It is a rerun of the authors' own pipeline. Reproducing these numbers here is
not independent replication, and the scripts share the simulator whose
assumptions are the main thing a critic should attack. Everything measured here
except EP-0013 is a synthetic multiserver-job model; no scheduling policy has
been run on a real arrival stream.
