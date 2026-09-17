# GPU U-31 known controls and input-drift uncertainty

Editorial aggregate projections of EP-0018, EP-0019 and EP-0020. EP-0018 exposes control scores and the first known-overload miss. EP-0019 exposes pooled synthetic input-work/time sufficient statistics, F quantiles, intervals and the ordered stopping branch.

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

The verifier needs SciPy (`requirements-reproduce.txt`) and recalculates the conditional F quantiles, interval arithmetic and stop branches. It does not regenerate jobs, rerun the simulator, validate exponentiality or independence, audit the omitted source, establish repeated-sampling coverage, or provide independent replication. Raw job sequences, simulator source, private work state and local paths are excluded.

The 5% family error budget is a theorem conditional on iid independent exponential inputs and known full-gang capacity. It is not an observed real-cluster error rate. True required work of unfinished jobs is available in this synthetic control; real-world availability is unverified. UNKNOWN at the maximum window is an abstention, not a stable label.

## EP-0020: fixed-need M/M/4 transfer

```bash
python reproduction/gpu-scheduling-u31-controls/verify_mmc_summary.py
```

The projection includes pooled input sufficient statistics, conditional F intervals, ordered adaptive stopping and four native/oracle alignment summaries. Capacity is four service-time slots: normalized load is B/(4T). Six known-control cells resolved correctly over 30 workloads and 10 looks, with a separate 5% / 24-look budget. The failed initial persistence attempt and previously observed recovery controls are disclosed. Holdouts had not run in that attempt.

The verifier checks arithmetic and recorded alignment/stopping claims; it cannot rerun or independently verify omitted generator/engine code, coverage or distribution assumptions. Information tier W requires true work of unfinished jobs. Output-only tier O and future-drained JCT tier D have different information/end times. No diagnostic-superiority comparison, new theorem, mixed-need capacity, manuscript novelty or real-cluster validation is established.
