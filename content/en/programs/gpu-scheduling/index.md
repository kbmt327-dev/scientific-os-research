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

The seven studies that followed were largely **the work of breaking this project's own numbers**. The driver was concurrency, not pool size (EP-0006). The headline — support including the whole cluster causes starvation — disappeared when only the background granularity changed (EP-0008). The flagship phase diagram's axis was confounded by a factor of 18 (EP-0009). "Decided by two numbers" was retracted (EP-0010).

Then **the detector itself turned out to be broken** (EP-0011). The flow balance used to locate the boundary is a censoring ratio — mean response time divided by the observation window — and cannot see divergence. While the mean response time grew 3.9×, the detector moved from 0.562 to 0.574. Every operational number was put on hold.

The replacement, **alpha** (the elasticity of mean response time with respect to the observation window), reads 0 where the system is stable and 1 at linear divergence, and moves the boundary by at most 0.02 when the window is multiplied by eight (EP-0012). The operational numbers are back, **now with a frequency column**.

## Current public claims

- **Three quantities to watch:** the largest job as a fraction of pool capacity, how many jobs run on that pool at once, and how often such a large job arrives.
- Rules of thumb (256 servers, rho 0.85, synthetic model, with 90% bootstrap intervals): at concurrency 10, ratio 0.92 (frequency 0.002) or 0.72 (frequency 0.02); at concurrency 30, 0.73 or 0.66.
- **Do not drop the frequency column.** Without it, the old table handed a conservative number to clusters where big jobs are rare and a dangerous one to clusters where they are common.
- To judge your own cluster, do not use a completion or attainment rate. Ask whether **mean response time grows with the observation window**: double the window, and if the mean rises by 1.4× or more, that class is diverging.
- **The real-cluster scope is extremely narrow.** Ten of Philly's 11 virtual clusters contain no job above a quarter of capacity. In the one exception, exactly **one job out of 19,100** exceeds half of capacity.

This is not yet a policy comparison on a real arrival sequence, and there are no external replications.

## Published Research Notes

1. [[en/research/gpu-scheduling/index|EP-0001 — initial comparison]]
2. [[en/research/gpu-scheduling-phase-diagram/index|EP-0002 — the starvation region]]
3. [[en/research/gpu-scheduling-starvation-mechanism/index|EP-0003 — isolating the mechanism]]
4. [[en/research/gpu-scheduling-real-traces/index|EP-0004 — checking the precondition in public traces]]
5. [[en/research/gpu-scheduling-pool-size/index|EP-0005 — dependence on pool size]]
6. [[en/research/gpu-scheduling-concurrency/index|EP-0006 — correcting the driver]]
7. [[en/research/gpu-scheduling-real-cluster-position/index|EP-0007 — measuring at the real cluster, and withdrawing a mechanism]]
8. [[en/research/gpu-scheduling-headline-broken/index|EP-0008 — breaking our own headline]]
9. [[en/research/gpu-scheduling-phase-reaxis/index|EP-0009 — the phase diagram's confounded axis]]
10. [[en/research/gpu-scheduling-third-variable/index|EP-0010 — retracting "two numbers"]]
11. [[en/research/gpu-scheduling-blind-detector/index|EP-0011 — the detector was not measuring divergence]]
12. [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012 — a boundary that stays put]]
13. **[[en/research/gpu-scheduling-one-job/index|EP-0013 — the real-cluster claim rests on one job (latest)]]**
