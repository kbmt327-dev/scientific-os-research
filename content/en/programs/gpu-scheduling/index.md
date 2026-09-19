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

<!-- GENERATED: program-current:START -->
## Current public state

EP-0026 audits one permanent parameter transition. A truthful manifest refuses240/240 transition looks before inference. A false stationary declaration yields80/80 wrong at100k; service improvement remains scheduled20/20 wrong at320k. The gate does not detect undeclared drift from data. General U31/real-GPU/time-varying theory, novelty and peer review remain UNKNOWN; general detectors0.

**Evidence boundary:** Known two-block exponential strict-FCFS, one permanent change, eventual-tail label and truthful provenance manifest only. Same-design execution is not external independent replication.

**[Read the current Research Note (EP-0026) →](/en/research/gpu-scheduling-transition-refusal/)**
<!-- GENERATED: program-current:END -->

<!-- GENERATED: program-history:START -->
## Published Research Notes

1. [[en/research/gpu-scheduling/index|EP-0001 — Estimation error and restart cost reverse which GPU scheduler wins]]
2. [[en/research/gpu-scheduling-phase-diagram/index|EP-0002 — A good average, a job class that never finishes, and three broken stability detectors]]
3. [[en/research/gpu-scheduling-starvation-mechanism/index|EP-0003 — Whole-cluster jobs, not mean gang size, decide when size-based scheduling breaks]]
4. [[en/research/gpu-scheduling-real-traces/index|EP-0004 — Real GPU clusters never received a job that filled the pool]]
5. [[en/research/gpu-scheduling-pool-size/index|EP-0005 — The safe ratio falls as the pool grows]]
6. [[en/research/gpu-scheduling-concurrency/index|EP-0006 — The driver was never pool size. It is how many jobs compete at once]]
7. [[en/research/gpu-scheduling-real-cluster-position/index|EP-0007 — Measured at the real cluster's position, and withdrew an explanation carried for four studies]]
8. [[en/research/gpu-scheduling-headline-broken/index|EP-0008 — Changing only the granularity of the background made the headline result disappear]]
9. [[en/research/gpu-scheduling-phase-reaxis/index|EP-0009 — The axis of the flagship phase diagram was confounded by a factor of 18]]
10. [[en/research/gpu-scheduling-third-variable/index|EP-0010 — Retracting "this is decided by two numbers"]]
11. [[en/research/gpu-scheduling-blind-detector/index|EP-0011 — The detector was not measuring divergence. It divided by the window, so it never moved]]
12. [[en/research/gpu-scheduling-alpha-boundary/index|EP-0012 — Replaced it with a statistic whose boundary stays put, and restored the numbers]]
13. [[en/research/gpu-scheduling-one-job/index|EP-0013 — The real-cluster claim rests on one job out of 19,100]]
14. [[en/research/gpu-scheduling-u31-calibration/index|EP-0017 — Independent calibration still left two capacity detectors in disagreement]]
15. [[en/research/gpu-scheduling-known-controls/index|EP-0018 — A midpoint queue threshold missed a known overload]]
16. [[en/research/gpu-scheduling-drift-uncertainty/index|EP-0019 — A small overload remained unresolved within a finite window]]
17. [[en/research/gpu-scheduling-mmc-transfer/index|EP-0020 — Input confidence intervals transferred to a fixed-need four-slot control]]
18. [[en/research/gpu-scheduling-information-tiers/index|EP-0021 — One window, different information, different errors]]
19. [[en/research/gpu-scheduling-critical-loss/index|EP-0022 — The price of abstention and the critical-load definition]]
20. [[en/research/gpu-scheduling-two-class-control/index|EP-0023 — Two-class FCFS overload below nominal resource load one]]
21. [[en/research/gpu-scheduling-past-only-learning/index|EP-0024 — Learning capacity from past completions without population parameters]]
22. [[en/research/gpu-scheduling-exposure-checkpoints/index|EP-0025 — Fixed completion-exposure checkpoints: reporting scope and abstention]]
23. **[[en/research/gpu-scheduling-transition-refusal/index|EP-0026 — When should a stationary diagnostic refuse a permanent parameter transition?]] (latest)**
<!-- GENERATED: program-history:END -->
