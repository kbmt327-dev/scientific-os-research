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

**Question:** Under which information and observation windows can size-first conditions and capacity boundaries be established? Is the cost of fragmentation explained by added work alone?

**Current state:** In the synthetic model at (ρ, π) = (0.6, 0.2), about half (0.52–0.56) of FCFS's extra fragmentation delay is state coupling (the part that disappears when slowdowns are shuffled within need class). The decision prediction also passed a sealed replication on new seeds, but the margin is thin; the pooled 12-seed lower bound, which includes E21 and is not an independent test, is 0.0006. In EP-0034, shuffling slowdowns only within busy-GPU strata at placement restored 77% of state coupling, against 6% for coarse arrival-order blocks (one decision row, (0.55, 0.2), was scorable). The mechanism candidate within the model is "fragmentation concentrates when the cluster is busy, and FCFS pays for it then". Real clusters and novelty remain UNKNOWN.

**Evidence boundary:** One synthetic MSJ model, 64 GPUs in 8-GPU nodes, trace_like, first-fit, exponential service, sticky placement and no migration, three rows. Local-commit seals only. Public checks verify sealed digests, rerun the grading and re-simulate two tasks; they are not independent replication.

**[Read the current Research Note (EP-0034) →](/en/research/gpu-scheduling-occupancy-strata/)** — Finding

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

## Kryptos K4

**Question:** Which mechanisms can the 97 ciphertext letters and 24 crib letters rule out, and which apparent patterns survive once the freedom used to find them is counted?

**Current state:** No decryption and no new plaintext letter (2026-10-11). Rounds 10–15 tested fixed row lists, listed public machines, squares and masks, printed Hill and classical procedures, mixed two-stage constructions and listed layout permutations. Decidable columns in the registered finite families gave no pass. These are logical negatives within the stated settings and error allowances, not refutations of ciphers in general or evidence that K4 is rarer than random. Insufficient coding agreement in premise audits, free charts and long-period masks, and 228 compatible free-square/within-word settings remain explicitly undecided. Twelve two-square classes in EP-0213 and three nonbijective Four-square classes remain compatible; settings outside the sixteen-square subset and the stopped branch in EP-0222 remain untested. Public packages verify bounded counts, instruments and saved summaries; they do not collectively rerun the original full searches. Recent tests of crib gaps and errors, free-cube Trifid, two systems scored per crib, two stages with one printed cube fixed, and Hill with square ciphers also gave no registered pass. One Hill/square column uses nulls for a 26-square subset rather than the entire space. Tests with preliminary K4 exposure or post-exposure diagnostic choices are not independent confirmation. EP-0224 also completed PH200, SPF2 and eight conditional sets of 20 controls: no K4 pass at registered thresholds, no UNKNOWN, and registered P=1. The conclusion is confined to the registered finite family, with SPF confirmation-control power of 25/60 retained as a limitation.

**Evidence boundary:** Exploratory computation on public ciphertext and 24 crib letters. Many later tests were fixed by local commits before K4 execution, without external preregistration; preliminary trials and instrument corrections are disclosed. Public internal verification is not independent replication. External independent replications and cryptographer reviews remain zero. Ground truth exists but is withheld.

**[Read the current Research Note (EP-0241) →](/en/research/kryptos-k4-two-stage-and-errors/)** — Negative Result

[See the current state and revision history →](/en/programs/kryptos-k4/)

[Browse all published Research Notes by date →](/en/research-notes/)
<!-- GENERATED: research-current:END -->

---

Future records may include Replication, Negative Result, Dataset, and Benchmark without changing existing research identities.
