# FCFS fragmentation residual and state coupling (EP-0031 to EP-0034, E20 to E23)

How much of FCFS's extra delay under node fragmentation comes from slowdowns
being tied to the cluster state at placement, and which part of that state
carries it? Synthetic MSJ model: 64 GPUs in 8-GPU nodes, trace_like mix, sticky
first-fit; a gang spanning more nodes than ceil(need/8) runs at rate
1/(1 + pi * excess).

```sh
python verify_state_coupling.py
```

The verifier checks the four sealed prediction digests, reruns the sealed
analysers on the published results, and re-simulates two tasks at the 160k
window (about two minutes on one core):

| Experiment | Prediction | Published grade |
|---|---|---|
| E20 | PRED-019 | P0 PASS, P1-P5 unscorable (14 of 27 cells UNKNOWN at 40k/80k windows) |
| E21 | PRED-020 | 5/6; decision P2 PASS (state coupling a is 0.56 of T at (0.6, 0.2)); P3 FAIL |
| E22 | PRED-021 | replication on new seeds: R1 PASS (0.52), R2 PASS (pooled 12-seed lower bound 0.0006; includes E21's seeds, a precision estimate rather than an independent test), R3 FAIL (reported only) |
| E23 | PRED-022 | 6/6; decision D PASS (busy-GPU strata restore 0.77 of a at (0.55, 0.2), the only scorable decision row; strata are F's state, five coarse bins, and CO/CT were chosen after a 20k smoke run) |

Full sweeps: `python run_e20.py`, `run_e21.py`, `run_e22.py`, `run_e23.py`
(648, 648, 648 and 864 simulations; each refuses to overwrite its results
file, so move it aside first). Set `WORKERS` for the process count.

- `predictions/`: sealed before the matching experiment ran (local commits
  only, no external timestamp). E20 had one post-seal fix to the JSON writer
  only, after the first run crashed while saving; simulation and grading were
  untouched and the first run's values were not read. PRED-022's private record gives the digest of
  its CRLF working copy (`9f53e9f1...`); the committed LF file here has
  `ca8da3c9...`. The verifier checks both.
- `sim/`, `run_e20.py`: the private working repository at the E23 seal. E23
  added a read-only placement trace to `sim/cluster.py` and an opt-in C-058 mode
  to `run_e20.py`; before sealing, every field of the existing E22 arms was
  reproduced exactly on four E22 tasks with the new code. E20 and E21 were run with earlier
  versions of these two files; the verifier re-simulates one E21 FCFS task
  (BASE/F/RP/CS/CM/U) against E21's published rows.
- `run_e21.py`, `run_e22.py`, `run_e23.py`, `analyze_e2x.py`: as sealed.
- `results/`: as produced. Source episode digests: EP-0031
  `a44554b4...`, EP-0032 `96438ae0...`, EP-0033 `63f7638e...`, EP-0034
  `838a51fd...`.

Boundary: one synthetic model, pi is a knob not a measured cost, three
(rho, pi) rows, no migration, no real cluster data. The E23 decision rests on
one row because (0.6, 0.2) was UNKNOWN. That fuller clusters fragment more is
known (Tiresias, Gandiva, Philly analyses, bin packing). Novelty UNKNOWN.
