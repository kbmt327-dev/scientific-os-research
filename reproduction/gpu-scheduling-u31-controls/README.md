# GPU U-31 known controls and input-drift uncertainty

Editorial aggregate projections of EP-0018 and EP-0019. EP-0018 exposes control scores and the first known-overload miss. EP-0019 exposes pooled synthetic input-work/time sufficient statistics, F quantiles, intervals and the ordered stopping branch.

```bash
python reproduction/gpu-scheduling-u31-controls/verify_summary.py
```

The verifier needs SciPy (`requirements-reproduce.txt`) and recalculates the conditional F quantiles, interval arithmetic and stop branches. It does not regenerate jobs, rerun the simulator, validate exponentiality or independence, audit the omitted source, establish repeated-sampling coverage, or provide independent replication. Raw job sequences, simulator source, private work state and local paths are excluded.

The 5% family error budget is a theorem conditional on iid independent exponential inputs and known full-gang capacity. It is not an observed real-cluster error rate. True required work of unfinished jobs is available in this synthetic control; real-world availability is unverified. UNKNOWN at the maximum window is an abstention, not a stable label.
