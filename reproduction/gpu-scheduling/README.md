# GPU scheduling EP-0001 reproduction

This package is an exact public extraction of the E1 simulator and result state at source commit `6e96d5f`. It excludes later unadjudicated experiments.

## Environment

- Python 3.11+
- NumPy (pinned by the repository-level `requirements-reproduce.txt`)

## Quick evidence check

From the repository root:

```bash
python scripts/reproduce.py --quick gpu
```

This verifies the sealed prediction digest and the stored 7/10 grading.

## Full simulation rerun

```bash
cd reproduction/gpu-scheduling
python run_sweep.py
python analyze_e1.py
```

The original 320-run sweep took about 209 seconds on the source machine. Runtime varies by machine. `analyze_e1.py` rewrites `results/E1_grading.json`; compare the result to the committed file.

## Boundary

This reproduces a synthetic discrete-event simulation. It does not validate the result against a production trace.

