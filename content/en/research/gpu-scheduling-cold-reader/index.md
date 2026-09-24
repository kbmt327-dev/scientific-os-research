---
research_id: GPU-SCHED-EP-0028
title: Do fresh AI readers read the transition-refusal note correctly?
date: '2026-09-24'
lang: en
domain: GPU Cluster Scheduling
type: Finding
status: AI-reader pilot; human comprehension UNKNOWN
evidence_level: Sealed AI-reader pilot, author-scored
peer_reviewed: false
independent_replications: 0
evidence:
  class: ai-reader-pilot
  source: Six fresh AI reader sessions answering sealed questions on the EP-0026 note
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Same-family AI readers, three per arm, self-reported isolation, author
  scoring; no human or external reader claim
replication:
  independent: 0
  failed: 0
source_episode: GPU-SCHEDULING/EP-0028
source_episode_sha256: 51a1db0ed4244ecfba421ae58ee5daaa30d83f4b560edc857e7582ced3dc5a2f
publication:
  status: publishable
tags:
- gpu-scheduling
- reporting-audit
- reader-test
- en
aliases:
- /research/gpu-scheduling-cold-reader/index
---

<p class="research-area"><b>GPU cluster scheduling</b><a href="/ja/research/gpu-scheduling-cold-reader/" hreflang="ja">日本語</a></p>

## Current finding

Six fresh AI readers answered nine sealed questions using only the EP-0026 note. Three read it as first published and three read it after the EP-0027 correction. The two versions differed only on the two facts EP-0027 corrected: seed dependence (0/3 vs 3/3) and the regenerated look count (0/3 vs 3/3). All six readers answered the main claims correctly, including the eventual-tail versus finite-window distinction.

## Key figure

![Correct answers per question in each arm under the sealed key](/assets/gpu-scheduling-cold-reader.svg)

Three readers per arm. Q9 is determined by the text itself and serves as a manipulation check.

## What this research shows

Without an explicit statement, none of the three readers inferred that the cells share seeds and are dependent, even though the note listed two models and ten seeds. The added sentence changed that. Two of three readers reran the reproduction command from the public repository without help and got the stated PASS line with 72 looks.

## What this research does not show

Human comprehension, outside readers, independent replication, novelty or demand. The readers are the same model family as the author, they self-reported their isolation, and the author scored them without blinding.

## Research question

Can a reader with no author context answer presealed questions on the note's claim boundary and rerun it, and do the EP-0027 corrections change the answers?

## Why this matters

A note can contain every required fact and still be misread. Before recruiting human readers, a cheap pilot can show which statements are not picked up.

## Method

The questions, answer key, five predictions and stop rule were sealed before the first reader started (local hash only). Readers were fresh Claude Code subagent sessions on sonnet; the author model is opus. Each reader received the note text with frontmatter removed and was asked to answer without tools, then to clone the public repository and run the stated command (corrected arm only).

## Results

Sealed per-reader totals: first-published 6, 6, 5; corrected 6, 7, 8 out of 9. Sealed predictions 3/5. P1 (every corrected-arm reader at least 8/9) failed. P5 (3/3 rerun PASS) failed at 2/3: in the third session, the harness's permission check blocked running cloned code, so the failure was not caused by the artifact.

Seven of the 13 misses came from the key rather than the note. On Q4 the key required stating that refusal depends on truthful provenance; five readers answered "No, it cannot detect a lying manifest from data" and scored 0. On Q7 the key also required "not estimated from observed data", which neither version of the note states. A post-hoc substance score, which is not the sealed result, is 7, 7, 7 versus 8, 9, 9.

## What changed

Nothing in the EP-0026 note changed in this step. The pilot identified one addition for Q7 (state that the label is not estimated from the observed data). Q4 needs no change because the note already states the dependence under Falsification targets.

## What failed

P1 and P5 failed. The key repeated the EP-0027 rubric's flaw of measuring phrasing instead of whether the fact was grasped. One reader's final report omitted its answers, which were recovered with one follow-up message whose fidelity cannot be verified.

## Evidence boundary

Six AI readers, one note, nine questions. Raw answers are published verbatim except that local paths are replaced by `<SCRATCH>`, so anyone can rescore them.

## UNKNOWN

Whether human researchers who are not the author read the note correctly; whether notes with harder content are read correctly by AI readers. External independent replications: zero. General detectors: zero.

## Falsification targets

If human readers misread the eventual-tail label or the provenance prerequisite, the 6/6 AI result does not transfer. If blinded rescoring of the raw answers changes the arm difference on Q6, the finding weakens.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-cold-reader): `python verify_cold_reader.py` checks the sealed bytes, rebuilds all six prompts from the sealed template and materials, and recomputes totals and prediction grades. It does not rerun the readers.

## Evidence / Artifacts

[Protocol, seal, materials, prompts, raw answers and scores](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/gpu-scheduling-cold-reader). Protocol, seal and materials are the sealed bytes; prompts and answers have local paths redacted.

## External audit

External independent replications: zero. Human readers: zero. Scoring was done by the author.

## Next experiment

A small test with human readers who are not the author, or an AI-reader test on a note that is more likely to be misread. Write the key as the facts to be grasped and include blinded or second-scorer scoring in the seal.

[[en/research/gpu-scheduling-self-containment/index|EP-0027]] → EP-0028
