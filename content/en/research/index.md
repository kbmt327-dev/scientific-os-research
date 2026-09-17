---
title: Research
description: Research areas, what each currently claims, and what kind of evidence backs it.
lang: en
aliases: [/research/index]
---

<p class="site-lede">Grouped by research area. Each entry says what can be claimed right now and what kind of evidence supports it. <a href="/ja/research/" hreflang="ja">日本語</a></p>

Notes are grouped by what they contribute, not by how confident they sound. A **Finding** reports an observed result, a **Method** defines a research interface, and a **Protocol** freezes a future test before confirmatory data exists.

<!-- GENERATED: research-current:START -->
## GPU cluster scheduling

**Question:** When does size-first scheduling break, and how far can its capacity boundary be resolved?

**Current state:** In a synthetic MSJ model, largest-job share, concurrency and large-job frequency affect policy rankings and class starvation. Earlier boundary values remain conditional on unaudited alpha=0.5. Saturated throughput and stored bisection capacity are not validated.

Following the EP-0017 alpha/queue disagreement, EP-0018 identified a midpoint queue miss at known overload rho=1.05 in a full-gang M/M/1 control. EP-0019 used independent exponential inputs, all input work and known unit capacity to form a load CI. It resolved holdout0.99/1.01/0.995, but 1.005 remained UNKNOWN at the maximum 320k window; execution stopped there. This is known-model input classification, not validation of a general MSJ detector. **U-31, mixed-need capacity and real-cluster transfer remain UNKNOWN; validated general detectors remain zero.**

The public Philly count of one job above half-capacity in 19,100 arrivals survives as a frequency measurement. Derived margins use a synthetic model and unaudited threshold; no scheduler was run on the real trace.

**Evidence boundary:** Limited to synthetic known-model controls and public Philly arrival counts. Public artifacts check aggregates, sufficient statistics, F quantiles, CI arithmetic and stopping. Exponentiality/independence and true-work observability are assumptions; raw job sequences, simulator source, external independent replication and prospective real-cluster validation are absent.

**[Read the current Research Note (EP-0019) →](/en/research/gpu-scheduling-drift-uncertainty/)** — Negative Result

[See the current state and revision history →](/en/programs/gpu-scheduling/)

## Queueing system identification

**Question:** Given a queueing world whose mechanism is hidden, how much of it can external records alone recover?

**Current state:** Within a disclosed family of candidate mechanisms, one hidden instance was identified correctly and all five structural components matched the withheld truth.

**Evidence boundary:** This tests selection from given options, not discovery from an open hypothesis space, and transfer to a real system has not been tested.

**[Read the current Research Note (EP-0001) →](/en/research/simulation-worlds/)** — Finding

[See the current state and revision history →](/en/programs/queueing-system-identification/)

## Human movement model interfaces

**Question:** Before measured human motion reaches a model, can explicit contracts and dataset boundaries stop coordinate mix-ups, target leakage, and false external validation?

**Current state:** The interface contract rejects seven deliberately broken variants. The dataset gate splits Carter into 30 development, 10 validation, and 10 test participants; reserves OpenCap laboratory data for external validation; and reserves Knee Grand Challenge for internal-load stress testing. B3D is a source-adapter format, the internal representation is NumPy plus explicit semantics, and Nimble is not mandatory.

**Evidence boundary:** No model has been fitted and no holdout has been read.

**[Read the current Research Note (EP-0005) →](/en/research/human-model-dataset-portfolio/)** — Dataset

[See the current state and revision history →](/en/programs/human-model-interface/)

## Badminton biomechanics

**Question:** In the smash, can the effect of short preparation time be separated from the effect of backward centre of mass?

**Current state:** Only the experimental design and power sensitivity are public; no observations exist. Detecting the interaction requires substantially more participants than detecting the main effects, so the sample size remains undecided.

**Evidence boundary:** Instrument feasibility and ethics remain unresolved, so the protocol is not sealed and data collection is not authorized.

**[Read the current Research Note (EP-0008) →](/en/research/badminton-biomechanics/)** — Protocol

[See the current state and revision history →](/en/programs/badminton-biomechanics/)

## The instrument in domains that require acting

**Question:** What can a seal-and-score apparatus measure when the predictor is also the actor, and where does the observational contract break?

**Current state:** The observational prediction contract breaks in five places: a miss cannot be split into a wrong model and nobody acting, the predictor can go and make its own prediction false, the scoring date is not theirs to choose, waiting becomes a stall, and success moves the distribution being measured.

Each breach is answered by **an invariant that refuses the record**. Scoring runs only through a four-point joint — threshold, decision, execution, result — and a prediction whose decision never opened can be neither supported nor refuted. Self-interference is settled by a stance declared at seal time; counting an intervention as its own success was declined, because it would stop the ledger separating a good model from a good operator.

**Evidence boundary:** Contract validation only. No prediction sealed in this grammar has reached a scoring date, and there is no guarantee that five is the complete set of breaches.

**[Read the current Research Note (EP-0001) →](/en/research/intervention-grammar/)** — Method

[See the current state and revision history →](/en/programs/intervention-instrument/)

## What a measurement design sees, and what it does not

**Question:** Where does a measurement-design result obtained on a world of your own making give way under a sweep?

**Current state:** **Both headline results are currently withdrawn.** A synthetic world flatters its author, and the flattery turned out to have forms.

The first was fixing the only thing that drives the quantity being measured. That constant moves the metric by 0.209; the thing we claimed to measure moves it by at most 0.027, with an unstable sign — **a factor of 7.9**. The second was pinning an unobservable nuisance at one value and publishing a decision line as a function of sample size. Sweep the nuisance and a frontier that fully closes clears the published line.

Only the weaker form survives: **reuse and the settling rate are different quantities, and only reuse responds.** That one is not an artifact of a constant.

**Evidence boundary:** Synthetic, and the mechanism family is ours. No real data of any kind was used and no claim about any application field is made. This is a self-review, so an attack we did not think of is by construction not in it.

**[Read the current Research Note (FRONTIER-METRICS-REVIEW-0001) →](/en/research/retracted-frontier-metrics/)** — Negative Result

[See the current state and revision history →](/en/programs/measurement-design/)

[Browse all published Research Notes by date →](/en/research-notes/)
<!-- GENERATED: research-current:END -->

---

Future records may include Replication, Negative Result, Dataset, and Benchmark without changing existing research identities.
