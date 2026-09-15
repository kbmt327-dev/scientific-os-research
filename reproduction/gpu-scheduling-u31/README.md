# GPU Scheduling U-31: bounded public artifact

`results/u31-v3-summary.json` is an editorial projection of the private EP-0017 audit. It exposes the fixed control/grid, aggregate alpha and queue scores, threshold rule, stop position, and evidence boundary. It contains no private work state, local paths, raw run traces, or company data.

Run `python verify_summary.py` to recompute the control midpoint, compare the two labels on the executed grid, and confirm that execution stopped at the first disagreement. This check does **not** rerun the synthetic simulator or independently reproduce the research. The simulator source and raw runs are not included in this package. The internal Episode and result SHA-256 values identify the source records but do not establish scientific validity.
