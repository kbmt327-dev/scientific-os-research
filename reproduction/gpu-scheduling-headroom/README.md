# GPU Scheduling Headroom (EP-0030)

This bounded checker re-grades selected saved E19 grading fields. The compact fixture stores per-row policy degradation values and the FCFS/SRPT load-matched values needed to check the sealed P0-P5 criteria.

Run with Python 3:

    python verify_e19_projection.py

The fixture records hashes identifying the source episode, PRED-018, E19.json, and E19_grading.json. It does not bundle those files, verify hashes against copies, include raw run records, rerun the simulator, or provide an independent replication. The 912-run count and 152-cell labels are checked as reported design and grading totals. This is a deterministic arithmetic check of the published projection only.

The experiment used one synthetic model: 64 GPUs in 8-GPU nodes, exponential service, sigma 0, sticky placement, and no migration. The load-matched arm is approximate: fragmentation raises work only for gangs spanning nodes, while the control increases work uniformly across arrivals. P5 does not identify a causal decomposition or establish behavior on real clusters.

The source episode summary reports a 66–100% P5 range. Recomputing from the saved row-level grading fields gives 63.78–99.96%; this package reports the recomputed range (about 64–100%). The aggregation or rounding difference is unresolved and does not change the four computable rows passing the sealed P5 criterion.
