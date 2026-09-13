# GPU scheduling EP-0002 / EP-0003 / EP-0004 reproduction

This package covers the three studies that followed EP-0001: the demand-mix
phase diagram with the rebuilt stability instrument (EP-0002), the support and
mechanism experiment (EP-0003), and the real-trace measurement plus threshold
sweep that demoted EP-0003's practical claim (EP-0004).

It is a separate package from `reproduction/gpu-scheduling/`, which stays pinned
to the E1 simulator. The simulator here carries metrics that did not exist at
E1 time — per-class flow balance above all — so the two packages are not
interchangeable, and the earlier one is not superseded by this one.

## Environment

- Python 3.11+
- NumPy and SciPy (pinned by the repository-level `requirements-reproduce.txt`)

## Quick evidence check

From the repository root:

```bash
python scripts/reproduce.py --quick gpu-phase
```

This verifies both sealed prediction digests and the stored 5/10 and 7/10
gradings, including the `n_pass_asrun` field that keeps the post-hoc detector
change auditable.

## Full simulation rerun

```bash
cd reproduction/gpu-scheduling-phase
python calib/c06_flow_balance.py     # calibrate the instrument first
python run_e2e3.py                   # E2 420 runs + E3 150 runs
python adjudicate.py                 # 59 ambiguous cells, two horizons
python analyze_e2e3.py               # rewrites results/E2E3_grading.json
python run_e4.py                     # E4 432 runs
python analyze_e4.py                 # rewrites results/E4_grading.json
python run_e6.py                     # E6 463 runs, the m/N threshold sweep
python analyze_e6.py                 # rewrites results/E6_grading.json
```

`analyze_traces.py` measures the demand shape of the public traces and is
included, but the raw traces are not redistributed. Obtain them from
`msr-fiddle/philly-traces` and `alibaba/clusterdata`; `results/E5_traces.json`
holds the derived per-trace and per-virtual-cluster measurements.

On the source machine E2/E3 took about 220 seconds, the adjudication about 750
seconds, and E4 about 570 seconds, with `WORKERS=8`. Runtime varies by machine.
Set `WORKERS` to match the host. The analysis scripts rewrite their grading
JSON; compare against the committed files.

`adjudicate.py` must run before `analyze_e2e3.py`, which reads
`results/adjudication.json` and refuses to treat an unadjudicated cell as
stable.

## Reading the results

`results/E2E3_report.txt` opens with the phase diagram: 21 cells of demand mix
(theta) by load (rho) for four policies. `results/E4_report.txt` opens with the
support sweep and the E[k]-matched control, which is the decisive comparison —
two mixes with identical mean gang size and opposite outcomes.

## Instrument note

Three single-horizon stability detectors failed before the one used here. The
failures are recorded in the header of `adjudicate.py` and calibrated in
`calib/c06_flow_balance.py`, which is a pass/fail test of the instrument rather
than an experiment. Run it first: if it fails, no verdict in this package is
trustworthy.

The detector used for grading is written into `predictions/PRED-003.json` under
`detector`, sealed before E4 ran. PRED-002 did not fix the detector formula, and
four of its ten predictions turn on which detector is applied; both gradings are
therefore reported.

## What the real-trace part does and does not show

`results/E5_traces.json` carries the measurement that demoted the previous
study's practical claim: across all 11 Philly virtual clusters, the probability
that a job requires the full measured pool capacity is 0.00000, and the largest
ratio of job size to capacity is 0.59. Capacity is estimated from peak
concurrent GPU usage, which is a lower bound, so a larger true quota only makes
those ratios smaller.

Only the *shape* of demand was taken from the traces. No policy was run on a
real arrival stream; the threshold sweep fed measured ratios into the synthetic
model. The measurement is retrospective on existing public data.

## Boundary

Synthetic multi-server-job simulation, 64 servers, exponential service, no
locality constraints, no network interference, no failures. The public research
notes state the claim scope that these artifacts support.
