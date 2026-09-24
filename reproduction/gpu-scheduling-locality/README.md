# Node fragmentation and policy ranking (EP-0029, E18)

Does node fragmentation reorder size-first policies (greedy SRPT,
ServerFilling-SRPT) against FCFS and EASY backfill, and does best-fit compact
placement remove the effect? Synthetic MSJ model: 64 GPUs in 8-GPU nodes, a
gang that spans more nodes than ceil(need/8) runs at rate 1/(1 + pi * excess).

```sh
python verify_locality.py
```

The verifier checks the sealed digest of `predictions/PRED-017.json`, reruns the
sealed `analyze_e18.py` on `results/E18.json`, checks the gang_heavy null, and
re-simulates eight runs (about a minute). The full sweep is `python run_e18.py`
(768 runs, about 20 minutes on 15 workers; it refuses to overwrite
`results/E18.json`).

- `predictions/PRED-017.json`: sealed before any E18 run (local commit only, no
  external timestamp).
- `run_e18.py`, `analyze_e18.py`, `sim/`: as sealed. `sim/` is the simulator
  from the private working repository at the sealing commit.
- `results/`: as produced.

Result: sealed predictions 1/6; the decision prediction P3 failed (no ranking
reversal under either placement). The test had little power. Every gang_heavy
need is a multiple of the node size, so first-fit never fragments and the
penalty never applies (a structural null). At pi = 0.6, 15 of 16 trace_like
cells diverged. Post hoc, unsealed: on trace_like, the degradation order was
srpt < sf_srpt < easy_backfill < fcfs in all eight rho x pi x placement rows.

Boundary: one synthetic model, pi is a knob not a measured cost, no migration,
no locality-aware admission, no real cluster data. That fragmentation hurts and
consolidation helps is known (Tiresias, Philly analysis, Gandiva).
