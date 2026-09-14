---
research_id: GPU-SCHED-EP-0008
title: Changing only the granularity of the background made the headline result disappear
date: 2026-09-13
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Exploratory
evidence_level: Synthetic simulation
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-simulation
  source: one sealed prediction (PRED-009, 5 of 5) and a 30-run experiment changing only the granularity of the background
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: 64-server synthetic multiserver-job model, rho 0.7, exponential service, no restart cost. EP-0003's original setting is held fixed and only the background demand granularity varies
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0008
source_episode_sha256: 5b305fc7b433ae222efcd035c2760a6f5640d24b4f7497097729b9b65a0c93d7
publication:
  status: publishable
tags: [finding, scheduling, simulation, retraction]
---

<p class="research-area"><b>GPU cluster scheduling</b><span>Finding the conditions under which size-first scheduling breaks</span><a href="/ja/research/gpu-scheduling-headline-broken/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic simulation</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

Since [[en/research/gpu-scheduling-starvation-mechanism/index|EP-0003]], this project's central result had been:

> If the support of the demand distribution — the set of gang sizes that can occur — includes the whole pool, that class starves. Fifteen such jobs out of 30,000 (probability 0.0005) is enough, and it happens even at a load of rho 0.7.

**We went after it, and it broke.**

Holding the pool size, the load, the scheduling policy and the whole-pool job probability of 0.0005 all fixed, and **coarsening only the granularity of the background jobs**, the whole-pool class's flow goes from 0.307 to **0.997**. Its mean response time falls from 400.9 to **39.9**. The starvation disappears.

What changed is how many jobs compete for the pool at once. EP-0003's original setting ran at a concurrency of 23.2. Coarsening the background takes it to 4.3 — a factor of 5.37.

So **support — whether whole-pool jobs exist at all — was a proxy.** The cause is whether a job is too large *relative to the number of competitors present at that moment*. The headline result was not wrong; it was **a claim conditioned on concurrency.**

## Key figure

<div class="ratio-figure" aria-label="background granularity against starvation"><div class="ratio-track"><i style="left:30.7%"></i><i style="left:99.7%"></i></div><div class="ratio-labels"><span style="left:30.7%"><b>0.307</b> fine background<br>concurrency 23.2 · starved</span><span style="left:99.7%"><b>0.997</b> coarse background<br>concurrency 4.3 · healthy</span></div></div>

The axis is the whole-pool class's flow balance — how well it keeps up with its own arrivals; 1.0 means it does. The only thing changed between the two points is the granularity of the background. Pool size, load and the whole-pool job probability are identical.

## What this research shows

- At identical probability, pool size, load and policy, **starvation appears and disappears with the granularity of the background alone**: flow 0.307 against 0.997.
- Starvation is conditioned on how many jobs are competing at once, not on the support of the demand distribution as such.
- Reservation-based EASY backfill is insensitive to the manipulation (flow 1.000 at every background).

## What this research does not show

- It does not establish that concurrency is the *only* second variable. Coarsening the background moves other quantities too; later studies find frequency and background family as further factors.
- The flow-balance statistic used to judge starvation was later shown to be invalid. The gap here (0.307 against 0.997) is extreme enough that the conclusion does not depend on where the line is drawn.
- No scheduling policy was run on a real arrival stream.

## Why this matters

The result broken here was **this project's strongest and most-cited own finding**. It had been handed to operators in the form "check whether whole-cluster jobs exist".

A claim published without its condition gets used outside that condition. Read as "whole-pool jobs are dangerous by their existence", it produces an operational rule that bans such jobs. In fact, when few jobs run at once, they get through.

**Build the experiment that attacks your own headline.** If it survives, it is stronger; if it breaks, you have found the condition. Here it was the latter.

## Research question

Can this domain's headline result be broken along a single axis — the granularity of the background?

## Method

Hold EP-0003's original setting completely fixed: 64 servers, rho 0.7, whole-pool job probability 0.0005, greedy SRPT. Vary **only the granularity** of the background gang-size distribution: fine (1, 2, 4 …), intermediate, coarse (8, 16, 32 …). 30,000 jobs per run, 30 runs.

Sealed as PRED-009; the digest is at `predictions/PRED-009.sha256` in the reproduction package, committed while no corresponding result file existed.

The deciding prediction X2 — "coarsening the background alone makes the starvation disappear" — was named **on the side that demotes this project's own headline**. The sealed text states the demotion it triggers.

## Results

| Background granularity | Fine | Intermediate | Coarse |
|---|---|---|---|
| Concurrency | 23.2 | — | 4.3 |
| Flow of the whole-pool class | **0.307** | 0.868 | **0.997** |
| Mean response time of that class | **400.9** | — | **39.9** |
| EASY backfill flow | 1.000 | 1.000 | 1.000 |

Flow is monotone in granularity. The concurrency difference is a factor of 5.37.

## What changed

- "Support includes the whole pool ⇒ that class starves" was rewritten as **a claim conditioned on concurrency**.
- "Support" was demoted from cause to proxy. The cause is whether a job is too large relative to the number of competitors present.
- A correction band was added to the published EP-0003 note.

## What failed

**PRED-009 scored 5 of 5.** Every prediction passed.

The failure is not in the predictions but in **having published this conclusion unconditioned across three studies.** That EP-0003's original setting sat at the specific point of concurrency 23.2 was never measured until EP-0006 found the axis.

**When a new axis is found, every past conclusion has to be placed back onto it.** At the moment EP-0006 identified the driver, where each earlier study sat on that axis was unknown. Placing them back reversed the headline.

## Evidence boundary

**Supported:** inside this synthetic model, whole-pool starvation appears and disappears with the granularity of the background alone, and EP-0003's headline was conditioned on concurrency.

**Not supported:** that concurrency is the only second variable; the validity of the statistic used to judge starvation (later invalidated, though the gap here is extreme enough that this conclusion is unaffected); any behaviour on a real trace.

## UNKNOWN

- Whether EP-0002's 21-cell phase diagram carries the same confound. Varying its demand-mix parameter should move concurrency too.
- Whether concurrency and maximum job ratio really are sufficient.
- What else moves when the background granularity changes.

## Falsification targets

- Hold concurrency and maximum job ratio fixed, change the background shape, and find the starvation verdict changes.
- Use a different statistic and find starvation persists even at the coarse background.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick gpu-boundary
```

Full rerun:

```bash
cd reproduction/gpu-scheduling-boundary
python run_e10.py
```

## Evidence / Artifacts

- [Public reproduction package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-boundary)
- [Sealed PRED-009, including the deciding prediction and the demotion it triggers](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/predictions/PRED-009.json)
- [E10 grading](https://github.com/kbmt327-dev/scientific-os-research/blob/main/reproduction/gpu-scheduling-boundary/results/E10_grading.json)
- Internal source Episode hash: `5b305fc7b433ae222efcd035c2760a6f5640d24b4f7497097729b9b65a0c93d7`

## External audit

- Independent replications: 0
- Failed replications: 0
- Bugs confirmed after publication: 0
- Open critiques: 0

## Next experiment

Place [[en/research/gpu-scheduling-phase-diagram/index|EP-0002]]'s 21-cell phase diagram back onto the same axis. It is this project's flagship result, and varying its demand-mix parameter should move concurrency too — so the axis itself may be confounded.

## How this was reached

<div class="revision-chain vertical" aria-label="revision history of the GPU cluster scheduling research">
  <a href="/en/research/gpu-scheduling/"><b>EP-0001</b><span>Estimate error and restart cost swap which policy is best.</span></a>
  <a href="/en/research/gpu-scheduling-phase-diagram/"><b>EP-0002</b><span>Good averages hide a job class that never finishes. Three stability detectors broke.</span></a>
  <a href="/en/research/gpu-scheduling-starvation-mechanism/"><b>EP-0003</b><span>Starvation is set by whether whole-cluster jobs exist, not by mean gang size.</span></a>
  <a href="/en/research/gpu-scheduling-real-traces/"><b>EP-0004</b><span>Measured pools never meet that condition; the harm is a multiple, not starvation.</span></a>
  <a href="/en/research/gpu-scheduling-pool-size/"><b>EP-0005</b><span>The safe ratio falls as the pool grows; the harm at real scale was underestimated.</span></a>
  <a href="/en/research/gpu-scheduling-concurrency/"><b>EP-0006</b><span>The driver was never pool size. It is how many jobs compete at once.</span></a>
  <a href="/en/research/gpu-scheduling-real-cluster-position/"><b>EP-0007</b><span>Measured at the real cluster's position, and corrected a mechanism claim carried for four studies.</span></a>
  <a class="current" href="/en/research/gpu-scheduling-headline-broken/"><b>EP-0008 · current</b><span>Changing only the granularity of the background made the headline result disappear.</span></a>
  <a href="/en/research/gpu-scheduling-phase-reaxis/"><b>EP-0009</b><span>The axis of the flagship phase diagram was confounded by a factor of 18.</span></a>
  <a href="/en/research/gpu-scheduling-third-variable/"><b>EP-0010</b><span>Retracted \"two numbers decide this\". Frequency is a third variable.</span></a>
  <a href="/en/research/gpu-scheduling-blind-detector/"><b>EP-0011</b><span>The detector was not measuring divergence. It divided by the window, so it never moved.</span></a>
  <a href="/en/research/gpu-scheduling-alpha-boundary/"><b>EP-0012</b><span>Replaced it with a statistic whose boundary stays put, and restored the numbers.</span></a>
  <a href="/en/research/gpu-scheduling-one-job/"><b>EP-0013</b><span>The real-cluster claim rests on one job out of 19,100.</span></a>
</div>
