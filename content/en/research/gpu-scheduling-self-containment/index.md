---
research_id: GPU-SCHED-EP-0027
title: Did the public article carry the facts needed not to misread its own claim?
date: '2026-09-24'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: Lexical document audit; reader comprehension UNKNOWN
evidence_level: Sealed document-content rubric
peer_reviewed: false
independent_replications: 0
evidence:
  class: document-content-audit
  source: Sealed 12-item lexical rubric scored on the EP-0026 public articles
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Presence of predeclared facts in two public articles; no reader recruited;
  no comprehension, usability or novelty claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0027
source_episode_sha256: f2942bad6a89de109b28064272123d1ad31416785fecdcf901340b62d2699af0
publication:
  status: publishable
tags:
- gpu-scheduling
- reporting-audit
- reproducibility
- en
aliases:
- /research/gpu-scheduling-self-containment/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-self-containment/" hreflang="ja">日本語</a></p>

## Current finding

A 12-item lexical rubric, sealed after publication but before scoring, found both EP-0026 public articles at 8/12. One of the four misses was a numeric error: the reproduction step said the runner regenerates 24 looks; the public runner regenerates 72.

## Key figure

![Per-criterion pass/fail before and after correction under the sealed rubric](/assets/gpu-scheduling-self-containment.svg)

Filled: criterion present. Hollow: missing or wrong. The rubric was not changed between stages.

## What this research shows

A public article that had passed page-load checks, hash checks and CI still omitted facts needed to read its claim boundary and carried a wrong number in its reproduction step. Hashes do not check whether content is correct.

## What this research does not show

No reader was recruited. Reader comprehension, usability, novelty, demand and external independent replication are not shown. The corrected 12/12 was written against the rubric, so it is nearly guaranteed by the correction itself.

## Research question

Do the EP-0026 articles state the eventual-tail estimand versus finite-window state, the truthful-provenance prerequisite, no undeclared-drift detection, the headline counts, repetition-unit dependence, model structure, replication and detector counts, the label's primary source, and the reproduction command with its look count?

## Why this matters

Before testing outside readers, the article must contain the needed facts; otherwise a reader's misreading cannot be separated from a missing statement.

## Method

Twelve regex criteria per language, three predictions and a stop rule were sealed before baseline scoring (local hash only, no external timestamp). The rubric was designed after reading the article, so this is not blinded. After baseline the rubric was frozen; only text the same rubric requires was added or corrected.

## Results

| Criterion | Baseline | Cause | Correction |
|---|---|---|---|
| C06 service improvement at 320k | missing in both | Fact present; the pattern measured word order (unpredicted) | Reordered; stated all other transitions were correct at 320k |
| C07 common seeds and dependence | missing in both | Repetition-unit dependence not stated | Stated cells are not 120 independent seeds |
| C11 label primary source | missing in both | Theorem named without a link | Linked Grosof et al. |
| C12 regenerated look count | wrong in both | Said 24 | 72 (2 seeds x 2 models x 6 scenarios x 3 looks) |

Sealed predictions: 2/3. P1 (baseline 9/12 per language) failed at 8/12; P2 (12/12 after correction) and P3 (24 to 72; 360 recorded looks unchanged) held.

## What changed

The EP-0026 articles were corrected. Readers of the earlier version should read the regenerated look count as 72.

## What failed

P1 failed. The C06 miss was not missing content: the rubric pattern measured word order rather than presence of the fact. The baseline failure is kept.

## Evidence boundary

Two articles x 12 criteria = 24 records. The baseline snapshot is stored as the bytes matching the sealed hash. This is lexical matching, not a judgment of meaning.

## UNKNOWN

Whether an outside reader can explain and rerun the truthful/false declaration difference and the eventual-tail label without author help is UNKNOWN. External independent replications: zero. General detectors: zero.

## Falsification targets

If the 12 criteria miss the main causes of reader misreading, the articles can pass 12/12 and still fail a comprehension test. Lexical presence does not guarantee correct interpretation.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-self-containment): `python verify_self_containment.py` checks the sealed hashes and rescores the baseline snapshot at 8/12 and the current articles at 12/12.

## Evidence / Artifacts

[Protocol, seal, runner, baseline and corrected scores, baseline snapshot](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-self-containment). Protocol, seal and runner are the sealed bytes.

## External audit

External independent replications: zero. Readers: zero. This is a rescoring by the same author, not third-party verification.

## Next experiment

Specify a test in which readers other than the author receive only the public page and answer presealed questions on comprehension and rerun. If AI readers are used, report them separately from human outside readers.

[[en/research/gpu-scheduling-transition-refusal/index|EP-0026]] → EP-0027
