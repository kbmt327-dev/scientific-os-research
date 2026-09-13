---
title: GPU cluster scheduling
description: An overview of research into when size-based GPU scheduling helps and when it breaks.
lang: en
---

In a GPU cluster, many jobs compete for limited accelerators. This program studies when running shorter jobs first reduces average waiting time, and when the same policy makes some jobs wait much longer.

## The question

How do job size, estimation error, restart cost, and pool capacity change the comparison between size priority and reservation-based scheduling? In particular, can a good average conceal starvation in one class of jobs?

## Progress so far

Synthetic simulation isolated a failure mechanism: one job requiring the whole pool can starve when size priority is combined with greedy packing. Two public traces were then checked for that precondition. None of the 11 production pools contained a job that filled its pool.

The current public claim is that the quantity to watch is the largest job as a fraction of pool capacity. A candidate conservative boundary is 0.75; the largest measured trace ratio was 0.59. This is not yet a policy comparison on a real arrival sequence, and there are no external replications.

## Published Research Notes

1. [[en/research/gpu-scheduling/index|EP-0001 — initial comparison]]
2. [[en/research/gpu-scheduling-phase-diagram/index|EP-0002 — the starvation region]]
3. [[en/research/gpu-scheduling-starvation-mechanism/index|EP-0003 — isolating the mechanism]]
4. **[[en/research/gpu-scheduling-real-traces/index|EP-0004 — checking the precondition in public traces (latest)]]**
