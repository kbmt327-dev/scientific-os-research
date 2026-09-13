---
id: GPU-SCHED-EP-0002
title: A demand-mix phase diagram, and three stability detectors that failed
date: 2026-09-13
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: Public simulator, instrument calibration, two-horizon adjudication, sealed prediction, and E2/E3 outputs
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: One-parameter synthetic demand-mix family, 64 servers, exponential service, rho 0.7 to 0.95, zero preemption cost, and a sigma grid to 3.0
source_episode: GPU-SCHEDULING/EP-0002
source_episode_sha256: 656775b68fee9214ef5490de02441111ac1451b4f24cab4d00556716c52649f4
publication:
  status: publishable
tags: [finding, scheduling, simulation, falsification, instrument]
---

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

Follows [[research/gpu-scheduling/index|Scheduling principles reverse under workload mix and preemption friction]], whose declared next experiment this study carries out.

## Summary

We swept GPU demand mix as a continuous axis to locate the threshold where ServerFilling-SRPT overtakes greedy SRPT, and re-ran the estimation-error axis under a corrected noise model. Both sealed expectations were wrong in instructive ways. There is no low-mix crossover, because greedy SRPT is not stable anywhere on the grid at rho 0.85 or above; the ranking reversal sits at the *opposite* end, where gang sizes are homogeneous and greedy SRPT wins by 7 to 17 percent. The corrected noise model overturned EP-0001's estimation-error conclusion for the one policy that reserves capacity.

The larger result is about measurement, not scheduling. Three single-horizon detectors for "stable or divergent" failed in succession, and the second failure was a detector this project had already recorded as invalid, revived inside the next analysis script. Ten predictions graded 5/10 under the corrected instrument and 4/10 under the one actually carried into the run.

## Research question

Along a continuous demand-mix axis, where does ServerFilling-SRPT overtake greedy SRPT, and does that threshold move with load? Separately: was EP-0001's finding that size-estimation error barely matters an artifact of a mean-unbiased lognormal error model, which shrinks the median estimate as sigma grows?

## Why this matters

Scheduling work is usually ranked by mean job completion time. If a policy can hold a healthy mean while one demand class never finishes, that ranking is not measuring what operators care about. A phase diagram that labels each cell by *stability* rather than by mean response time is a different object from a speedup table, and it is the object a practitioner needs before adopting a principle.

The instrument half matters for any simulation study of a queueing system: the quantity being claimed — stability — is a statement about the infinite horizon, and every finite-window proxy for it we tried was either silent or wrong.

## Method

Demand mix was parameterized as a one-parameter family, `P(need = 2^i)` proportional to `theta^i` over needs 1 to 64 on a 64-server cluster. `theta = 0.4` is small-job-heavy, with mean gang size 2.37 and about 60 percent single-GPU jobs. It was chosen to resemble the shapes reported for production traces; no production trace data were used anywhere in this study; `theta = 2.0` is gang-dominated, with mean gang size 43.

- **E2**: 7 mixes x 3 loads (rho 0.7, 0.85, 0.95) x 4 policies x 5 seeds, 30,000 jobs each. 420 runs.
- **E3**: mean-unbiased versus median-unbiased error, sigma in {0, 0.5, 1, 2, 3}, 3 policies, 5 seeds, at `theta = 0.4`, rho 0.85. 150 runs.
- **Adjudication**: 59 cells whose verdict was not settled by the single-horizon rule were re-run at 30,000 and 120,000 jobs. 236 runs.

Predictions were sealed with SHA-256 `d726c5a701367f3be0bff47eba10267ee5fcd43bc4b830ec70c97a22477ed8a0` and committed before any result file existed.

## Results

Phase diagram, 21 cells. `.` stable, `S` one demand class starves, `O` whole-system overload, `X` unusable, `?` undetermined.

| rho | theta | FCFS | EASY backfill | greedy SRPT | ServerFilling-SRPT |
|---|---|---|---|---|---|
| 0.70 | 0.4 | . | . | **S** | . |
| 0.70 | 0.8 | X | . | O | . |
| 0.70 | 1.25 | O | . | . | . |
| 0.70 | 2.0 | . | . | . | . |
| 0.85 | 0.4 | . | . | **S** | . |
| 0.85 | 0.8 | X | . | O | . |
| 0.85 | 1.6 | O | . | O | . |
| 0.85 | 2.0 | O | . | ? | . |
| 0.95 | 0.4 | X | . | **S** | . |
| 0.95 | 1.0 | X | . | O | . |
| 0.95 | 2.0 | O | . | O | . |

ServerFilling-SRPT and EASY backfill are stable in all 21 cells. Greedy SRPT is stable in 3, all at rho 0.7 with homogeneous large gangs. The full grid is in `results/E2E3_report.txt`.

**The aggregate metric hides the failure.** At `theta = 0.4`, rho 0.85, greedy SRPT's mean JCT is 2.06 against EASY backfill's 2.11 — a ratio of 0.98, which reads as a slightly better ordinary policy. In the same runs the 64-GPU class waits 366 against backfill's 7.1, a factor of 52.

**The reversal runs the other way.** At rho 0.7 the ServerFilling/greedy ratio is 0.248 at `theta = 1.25`, then 1.070 at 1.6 and 1.169 at 2.0. ServerFilling's advantage comes from *heterogeneity* of gang sizes, not from large gangs being common: when every job is the same size there is no packing freedom for exact filling to exploit.

**Unfairness reverses direction with the policy.** At rho 0.85, worst-class mean JCT under greedy SRPT falls from 366 to 84 across the theta axis while ServerFilling's rises from 1.6 to 26.7. EASY backfill stays flat, 7.1 to 13.6, and is best on worst-class JCT in 19 of 21 cells.

**Estimation error, corrected model.** Under median-unbiased noise, where sigma is pure spread, EASY backfill's mean JCT rises from 2.107 to 7.019 as sigma goes 0 to 3, a factor of 3.3, and its worst-class JCT rises 7.1 to 43.9. ServerFilling-SRPT moves 18 percent and greedy SRPT 27 percent over the same range.

Under the mean-unbiased model the backfill curve is non-monotone, peaking at 9.602 for sigma 1 and then *improving* to 3.887 at sigma 3. That is arithmetic, not scheduling: at sigma 3 the median estimate is `exp(-4.5) = 0.011` of true size, so 77 percent of jobs look nearly instantaneous, the head-of-line reservation collapses to the present moment, and EASY backfill degenerates into "start whatever fits". On a small-job-heavy mix that degeneration happens to help.

## What changed

Three claims from EP-0001 are revised.

| EP-0001 claim | Revision |
|---|---|
| Greedy SRPT leads on a small-job-heavy mix | Holds only when the demand distribution excludes whole-cluster jobs. With them present, ServerFilling-SRPT leads on both mean and worst-class JCT |
| Size-estimation error barely matters | Wrong for reservation-based policies. EASY backfill degrades 3.3x under pure spread. Priority-based policies are the insensitive ones |
| The ranking reverses as large-gang share rises | Direction inverted. The reversal is at the homogeneous end, and favors greedy SRPT |

This study also closes two UNKNOWNs that EP-0001 declared, and hits one of its own stated falsification targets: a corrected median-unbiased error model did reverse the inference about estimation error within the tested range.

## What failed

Five of ten sealed predictions failed.

| Prediction | Criterion | Result |
|---|---|---|
| Q1 | A mix threshold sits between theta 0.4 and 0.8 | **Failed.** No like-for-like crossover exists: greedy SRPT is never stable at rho 0.85 |
| Q2 | The threshold moves at most one grid step with load | **Failed.** Defined only at rho 0.7 |
| Q3 | The ratio falls monotonically in theta | **Failed.** Zero comparable cells at rho 0.85; vacuous |
| Q4 | Greedy SRPT is stable for theta <= 0.8 | **Failed.** One class starves from theta 0.4 |
| Q5 | EASY backfill never becomes unstable | Supported. 21 of 21 stable, worst flow balance 0.984 |
| Q6 | FCFS stable at theta 0.4, unstable above 1.0 | Supported, though its mean JCT at 0.4 is 38x backfill's |
| Q7 | EASY backfill is never the best policy | Supported on mean JCT only; it is best on worst-class JCT in 19 of 21 cells |
| Q8 | Median-unbiased backfill JCT is monotone in sigma | Supported |
| Q9 | Greedy SRPT still beats backfill at sigma 3 | **Failed.** Withheld: greedy SRPT is class-starved, so the paired ratio is undefined |
| Q10 | Backfill is worse under median-unbiased noise at sigma 3 | Supported. 7.019 against 3.887 |

Q1 through Q4 failed for one reason: the sealed frame assumed both policies would be stable somewhere and trade places. They do not. That frame came from over-generalizing EP-0001's result.

**Three instruments failed, and one failure was a repeat.**

| Detector | How it broke | Caught in |
|---|---|---|
| Completion fraction below a threshold | A finite system always drains once arrivals stop, so it never fires | EP-0001 |
| Utilization below offered load | Fires on long transients in stable systems. EP-0001 recorded this as invalid; it was nevertheless reinstated inside the E2 analysis script | EP-0002 |
| Level of per-class flow balance | Horizon-dependent. FCFS at theta 0.4 reads 0.80 at 30k jobs and 0.95 at 120k while its mean JCT *falls* by a third, i.e. stable. At theta 2.0 it reads a higher 0.87 while mean JCT grows 3.22x, i.e. divergent | EP-0002 |

What survived calibration is the *spread* of flow balance across demand classes: a starving class sits near 0.4 while every other class sits at 1.00, and that signature is horizon-invariant, while the starved class's own JCT grows linearly with the horizon. Level questions are settled by re-running at two horizons.

**Disclosure.** The detector was changed after results were seen. PRED-002 required both cells to be stable but did not fix the formula for stability. Under the detector carried into the run the grade is 4/10; under the corrected one it is 5/10, and the grading of Q1, Q2, Q3, and Q9 depends on which is used. Those four carry reduced evidential weight. Both gradings are stored in `results/E2E3_grading.json` under `pass` and `pass_asrun`. PRED-003 writes the detector into the sealed file to prevent a repeat.

## Evidence boundary

**Supported:** Under this simulator, mix family, load grid, and seeds, policy *stability* — not merely ranking — depends on demand mix; greedy SRPT starves the whole-cluster class across the low-mix region; the aggregate mean hides that starvation; and the estimation-error conclusion of EP-0001 depends on the noise parameterization.

**Not supported:** No production-cluster claim, no universal threshold, no result for non-exponential service, no fairness-acceptability judgment, and no real trace. Preemption cost was zero throughout this study.

## UNKNOWN

- Behavior above sigma 3.
- Whether the mix-dependent crossover persists with non-zero preemption cost.
- Whether the reversal contour survives heavy-tailed service times.
- The greedy SRPT cell at theta 2.0, rho 0.85 remains undetermined; it grew 1.46x over a 4x horizon, between the stable and divergent bands.
- Real-trace validation, which remains the highest-priority open item.

## Falsification targets

- An independent simulator at the same parameters does not reproduce the stable/starved/overloaded labels.
- A starved class's JCT stops growing with the horizon under a longer run.
- A third horizon moves cells currently labeled stable into the overloaded band.
- A reservation-based policy other than EASY backfill proves insensitive to median-unbiased error, which would confine the estimation-error revision to one implementation rather than to the reservation mechanism.

## Reproduce

### Quick artifact and grading check

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-phase
```

### Full rerun

```bash
cd reproduction/gpu-scheduling-phase
python calib/c06_flow_balance.py
python run_e2e3.py
python adjudicate.py
python analyze_e2e3.py
```

Calibrate the instrument first. If `c06` fails, no verdict in the package is trustworthy. `adjudicate.py` must run before `analyze_e2e3.py`, which refuses to treat an unadjudicated cell as stable.

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-phase)
- [Sealed PRED-002](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/predictions/PRED-002.json)
- [E2/E3 grading, with the as-run detector retained](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/E2E3_grading.json)
- [Two-horizon adjudication of 59 cells](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/results/adjudication.json)
- [Instrument calibration](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-phase/calib/c06_flow_balance.py)

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs: 0
- Open critiques: 0

## Next experiment

Separate the two candidate causes of the starvation: does it track the *support* of the demand distribution containing the full cluster size, or the mean gang size? That is [[research/gpu-scheduling-starvation-mechanism/index|EP-0003]], which holds mean gang size fixed and moves only the support.
