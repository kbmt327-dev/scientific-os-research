---
research_id: SIM-WORLD-EP-0001
lang: en
aliases: [/research/simulation-worlds/index]
title: How much of a hidden queueing mechanism can observation alone recover?
date: 2026-09-13
domain: Sim World / Queueing
type: Finding
status: Exploratory
evidence_level: Synthetic blind benchmark
peer_reviewed: false
independent_replications: 0
evidence:
  class: synthetic-blind-benchmark
  source: Public hidden-world generator, observations, sealed predictions, fitted simulator, and reveal
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: One hidden instance inside a disclosed finite mechanism family
source_episode: SIM-WORLD/EP-0001
source_episode_sha256: 0c632eb5cad1431953bcbfbe3a067925fea3d7caac6bb21547ce53cb03a7931f
publication:
  status: publishable
tags: [finding, queueing, blind-benchmark, model-selection]
---

<p class="research-area"><b>Queueing system identification</b><span>How far observation alone can recover a mechanism</span><a href="/ja/research/simulation-worlds/" hreflang="ja">日本語</a></p>

<div class="evidence-strip"><span>Finding</span><span>Synthetic blind benchmark</span><span>Exploratory</span><span>Not peer reviewed</span><span>0 external replications</span></div>

## Current finding

Inside a disclosed finite mechanism family, a blind queueing instance was identified as geometric batch arrivals plus heterogeneous exponential servers. The parsimonious model placed 8 of 10 out-of-sample statistics inside 95% predictive intervals and matched all five structural components after reveal.

A hidden queueing world presented an apparent M/M/c baseline whose observed mean sojourn time was 234 times the analytic prediction and grew over time. Cheap tests identified simultaneous geometric batches; a sealed request for server-level observations then separated heterogeneous service rates from a globally wrong nominal rate. A parsimonious batched-arrival, exponential-service, tied-rate heterogeneous-server model put 8 of 10 out-of-sample statistics inside 95% predictive intervals and matched the final hidden-world reveal. The benchmark tested identification inside a known mechanism family, not discovery of an unknown hypothesis space.

## Key figure

```mermaid
flowchart LR
  O[Large mismatch] --> T[Cheap alternative tests]
  T --> Q[Seal a request for richer observations]
  Q --> L[Compare a model ladder]
  L --> P[Seal out-of-sample predictions]
  P --> R[Reveal: 5/5 structural matches]
```

## What this research shows

- A bounded observe–predict–request–replicate loop recovered this one hidden instance within its supplied family.
- Replication prevented a one-run residual from becoming an unnecessary new mechanism.

## What this research does not show

- It does not demonstrate open-world mechanism discovery, real-queue performance, or generalization across seeds.
- The benchmark designer and researcher were not independent.

## Research question

Can prediction mismatch, requested observation, sealed out-of-sample tests, replication, and a model ladder identify the smallest queueing model that explains a hidden simulated world?

## Why this matters

Adding complexity after a mismatch is easy. This benchmark instead required cheaper alternative explanations to be eliminated, new observation channels to be justified, and residuals to be replicated before expanding the model.

## Competing hypotheses

The candidate family included alternative arrival processes, service laws, server structures, and customer behavior. The active alternatives were: abandonment or balking; congestion-dependent slowdown; batch arrival; a wrong common service rate; heterogeneous server rates; and non-exponential service.

## Predictions

- **PRED-001:** sealed before elevating one existing run from observation level 1 to level 3; all six predictions were supported, including strong server-rate heterogeneity.
- **PRED-002:** sealed before two out-of-sample conditions; 8/10 reported statistics fell inside 95% predictive intervals.
- **PRED-003:** sealed before eight same-condition replications to decide whether one residual required a new mechanism; the replicate mean returned inside the interval.
- **FINAL-MODEL:** sealed before revealing the hidden world.

## Method

The world drew a 16-byte seed at runtime and stored only the seed plus a SHA-256 commitment. Mechanisms and parameters were derived from the seed. Observation levels exposed progressively richer fields. Analysis began with arrivals and departures, then requested service start, server ID, exit reason, and queue-length samples only after the request and six predictions were sealed.

A model ladder compared nominal M/M/c, fitted-rate M/M/c, homogeneous batched arrival, and heterogeneous batched-arrival models. The chosen model tied two statistically indistinguishable server rates and used one fewer parameter than the full heterogeneous model.

## Results

- Baseline M/M/4 predicted mean sojourn `W=1.335`; observed `W=311.8` with linear growth.
- 49.5% of arrivals shared an exact timestamp; batch sizes closely matched a geometric distribution.
- Server rates were approximately `0.693 / 0.361 / 0.364 / 1.028`; a homogeneous-rate explanation was rejected.
- The parsimonious heterogeneous model achieved 8/10 predictive-interval hits and median relative error 0.102.
- Revealed structure matched all five declared structural components. Estimated mean batch size differed by 0.53%, maximum server-rate error was 2.29%, and capacity errors for `c=3,4,6` were below 0.3%.

## What changed

- Observation escalation was narrowed to one justified channel upgrade after cheap tests eliminated abandonment and slowdown.
- A one-run waiting-time residual triggered replication rather than a new mechanism.
- Two near-equal rates were represented as an economical tie, not claimed to be exactly equal.

## What failed

An analysis initially reported over-dispersed arrival epochs because it included a partial terminal time bin. Complete bins and an empirical Poisson null removed the apparent effect. Without that correction, the model would have added an unnecessary modulated or periodic arrival process.

The family of possible mechanisms and an assignment rule were supplied in advance. The hidden instance was blind; the hypothesis space was not.

## Evidence boundary

**Supported:** One hidden synthetic instance was identified within a declared finite family, and the final structure/parameters matched its reveal after sealed predictions and out-of-sample checks.

**Not supported:** Open-world mechanism discovery, performance on real queues, generality across hidden seeds, or independence of the benchmark designer and researcher.

## UNKNOWN

- Whether the same procedure succeeds when the mechanism family is expanded independently.
- Detection power with observation windows one tenth as long.
- Identifiability under interacting deviations such as heterogeneous servers plus congestion-dependent slowdown.
- Generalization across new hidden seeds and independent researchers.

## Falsification targets

- New sealed seeds from the same family repeatedly select a wrong structure.
- Higher-load conditions produce capacity inconsistent with the fitted sum of rates.
- Permuting server identity breaks predicted rate tracking.
- Independent reanalysis finds leakage from the seed or reveal into predictions.

## Reproduce

```bash
python -m pip install -r requirements-reproduce.txt
python scripts/reproduce.py --quick queue
```

For a full fresh blind run, generate a new seal and keep `reveal` unavailable to the analyst until the final model is sealed. The bundled completed run can reproduce every published calculation but is no longer blind because the reveal is now public.

## Evidence / Artifacts

- [World generator and observation data](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds)
- [Sealed predictions](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds/predictions)
- [Analysis ladder](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/simulation-worlds/analysis)
- Hidden-world commitment: `7c4e47709de366e295aec26be7fac462100d1c6bf3d49fcd9ec03e40930b663a`
- Internal source Episode digest: `0c632eb5cad1431953bcbfbe3a067925fea3d7caac6bb21547ce53cb03a7931f`

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs after publication: 0
- Open critiques: 0

## Next experiment

Have an independent process expand the mechanism family, generate multiple sealed instances, and evaluate structure recovery without sharing truth or family-construction logic with the analyst.
