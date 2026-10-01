---
research_id: KRYPTOS-K4-EP-0169
title: Does one phase shift in the grouping reopen the square and Bifid ciphers?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Finding
status: With one shift in the grouping, free Four-square (0/960), free Two-square (0/576), keyword squares (0/7.15 million) and one-square Bifid (0/2,765) stay closed; CM-Bifid with two free squares reopens (27 of 2,765 settings consistent, post hoc null P = 0.12), which corrects the earlier closure and makes it undecidable; later plaintext constraints did not decide it; C08 stays undecidable
evidence_level: Exact consistency tests on the public ciphertext and cribs with planted controls and shuffled nulls; decision rules committed before any run on K4, but the controls were run before that commit, the keyword-square null was enlarged after seeing K4, and the CM-Bifid null was added after the result (post hoc)
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext without its Ws and the 24 public crib letters; exact square and coordinate solvers, shuffled-ciphertext nulls, planted controls; follow-ups with word-fragment sets and plaintext candidate sets fixed before K4 (EP-0177, EP-0184) and a typo-tolerant scorer (EP-0178)
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One phase shift (b, phi0) in the digraph grouping, or one restart of the Bifid block alignment, on the 92 non-W letters (C08 also on 97); the families of the W-squares Note; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0169
source_episode_sha256: ccdfdc7b15c8139d0f5275489d5aea852a22b9f46bd1794eacfe1b6297df4fcd
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- correction
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-block-phase-shift/" hreflang="ja">日本語</a></p>

## Research question

The [W-squares Note](/en/research/kryptos-k4-w-squares/) removed K4's five Ws as separators and closed the 5×5 square ciphers on the remaining 92 letters, pairing letters from the first or the second letter throughout. An encipherer working by hand could lose one letter of the grouping somewhere and continue out of step. If the grouping shifts once, do the square ciphers and Bifid become consistent with the cribs?

## Why this matters

A one-letter slip in the grouping is a small and plausible error, and it costs about 8 bit (97 positions × 2 phases). If a closed family reopens with it, the earlier closure was fragile and must say so. There is no source hint for this shift; it is a robustness test of earlier negatives.

## Method

- **Digraph shift.** A setting (b, φ0) pairs letters from phase φ0 before position b and from the other phase from b on; one letter at the shift stays unpaired and unconstrained. On 92 letters this gives 186 settings, which reduce to 24 distinct sets of crib pairs (22 of them new).
- **Bifid shift.** Period p = 2–12 or the whole text, a first alignment a0, and the alignment restarts at b. 7,176 settings reduce to 2,765 distinct crib-touching block lists (78 of them without a shift, as in EP-0120).
- **Exact tests (from the W-squares Note).** Free Four-square: each crib digraph fixes one cell of each cipher square, with the standard or one of 39 keyword plain squares (960 settings). Free Two-square: 24 variants × 24 (576). Keyword squares: 7,154,160 settings (22.8 bit). C08, a fixed arbitrary digraph chart, on 97 and on 92 letters. One-square Bifid and CM-Bifid (two free squares): an exact solver on square coordinates.
- **Controls and nulls.** Planted texts enciphered with a random shift for every family (200, 200, 30, 200, 40, 40). Nulls: shuffles of the ciphertext with the crib positions kept.
- **What was fixed before K4, and what was not.**
  - The decision rules were committed before any run on K4. The planted controls do not use K4, but they were run before that commit and included in it.
  - The keyword-square null was first run with 5 shuffles. After K4's 0 hits had been seen, it was increased to 100 and rerun.
  - The CM-Bifid count null (100 shuffles) was added after the K4 result. Its P value is post hoc.

## Results

| Family | Settings | K4 | Shuffles | Planted | Verdict |
|---|---|---|---|---|---|
| Four-square, free cipher squares | 960 | 0 consistent | 94.6% inconsistent everywhere (473/500) | 200/200 | closed (logical) |
| Two-square, free squares | 576 | 0 consistent, 0 undetermined | 78.5% (157/200) | 199/200 (1 hit the node cap) | closed (logical) |
| Keyword squares | 7,154,160 | 0 hits | 0 of 100 with hits | 30/30 | closed |
| C08, 97 letters | 97 | 88 consistent | 2 of 2,000 inconsistent everywhere | 200/200 | undecidable |
| C08, 92 letters | 92 | 83 consistent | 3 of 2,000 | 200/200 | undecidable |
| Bifid, one free square | 2,765 | 0 consistent | 200/200 inconsistent everywhere | 40/40 | closed, but no power |
| CM-Bifid, two free squares | 2,765 | **27 consistent**, 0 undetermined | post hoc: median 90, 5% point 17, P(≤ 27) = 0.12 | 40/40 | **reopened, undecidable** |

In C08 every setting where K4 contradicts has b inside EASTNORTHEAST; the two unshifted phases give no contradiction. The 27 CM-Bifid settings are whole-text splits into two blocks at b = 22, 28 and 30, and restarted alignments with periods 5, 6 and 8–12. None of the 78 unshifted settings is consistent, so the EP-0120 result itself stands; the closure fails only once one shift is allowed.

**Later constraints on the open settings.** Three follow-ups tried to decide what stayed open. FSfree below means the four free Four-square settings on other pairings of the two O-segments (folded and neighbouring pairs), left undecidable by an internal follow-up (EP-0157) to the [O-pairs Note](/en/research/kryptos-k4-o-pairs/). EP-0177 read the Ws as phrase breaks and required the two letters after EASTNORTHEAST to end a phrase and the four letters before BERLINCLOCK to begin one, with two-letter and four-letter word sets fixed by rule from a book corpus before K4 (10.95 bit). CM-Bifid went from 27 to 6 and FSfree kept 4/4. K4 kept 0.22 of its settings against a shuffle median of 0.43; 2 of 20 shuffles were at or below K4, not significant. EP-0184 fixed plaintext candidate sets by rule before K4 for positions 0–19 (phrases from the sculpture's Morse section) and 75–96 (spelled times, dates, coordinates and compass words), 20.34 bit in all. All 6 CM-Bifid settings were eliminated, but shuffles lost every crib-consistent setting in 153 of 159 cases, so the elimination is what any ciphertext would show; it holds only if those candidate sets are assumed. FSfree was untouched, because its pairs never reach positions 0–19 or 75–96: the result was forced before testing. EP-0178 built a scorer for English that tolerates up to two misspellings, like those in K1–K3; it is a tool and was not applied to K4. At length 97 the original 4-gram scorer already separates English from shuffles completely (AUC 1.000 with 0–2 substitutions), and the tolerant score helps only in windows of about 30 letters (d′ 5.59 → 5.98).

## Current finding

One shift in the grouping leaves free Four-square, free Two-square, keyword squares and one-square Bifid closed; each is a logical refutation, and shuffles mostly fail too. CM-Bifid with two free squares does not stay closed: 27 shifted settings are consistent with the cribs. This corrects the earlier closure of CM-Bifid in the [W-squares Note](/en/research/kryptos-k4-w-squares/) (EP-0120): with one shift allowed, CM-Bifid is undecidable by the cribs alone, and K4's count of 27 is not unusual among shuffles (post hoc P = 0.12). Word-fragment and candidate-set constraints did not decide it either. C08 remains undecidable.

## Key figure

![Upper panel: six rows. Four-square with free cipher squares (960) closed, K4 0, 94.6% of shuffles also fail everywhere; Two-square with free squares (576) closed, 78.5%; keyword squares (7.15 million, 22.8 bit) closed, 0 hits, shuffles 0/100; Bifid with one free square (2,765) closed but with no power, every shuffle fails too; CM-Bifid with two free squares (2,765) undecidable, K4 27 consistent, shuffle median 90 (post hoc); fixed digraph chart C08 (97 / 92) undecidable, K4 88 / 83 consistent like shuffles. Lower panel: three boxes joined by arrows for the CM-Bifid settings: 27 consistent with the cribs (shuffles median 90, P = 0.12, post hoc); 6 remain with word fragments at 10.95 bit (K4 survival 0.22, shuffles median 0.43, 2 of 20 shuffles at or below K4); 0 remain with candidate sets at 20.34 bit (shuffles also lose every setting in 153 of 159). A note says neither step separates K4 from shuffles significantly, that the last step holds only if the candidate sets are assumed, and that four free Four-square settings on the O-segment pairings stay untouched](/assets/kryptos-k4-block-phase-shift.svg)

## What this research shows

- One shift in the grouping does not reopen free Four-square, free Two-square, keyword squares or one-square Bifid.
- CM-Bifid with two free squares reopens: 27 of 2,765 shifted settings are consistent, so the earlier "closed" holds only without a shift.
- Two later plaintext constraints did not decide the reopened settings in a way that separates K4 from random ciphertext.

## What this research does not show

It does not show that K4 is a CM-Bifid: 27 consistent settings is typical of shuffles (post hoc P = 0.12), and no English stage was run on them. It does not show that K4 is rarer than random for the closed families. The elimination of the last 6 CM-Bifid settings depends on assumed candidate sets and happens to 96% of shuffles. Two or more shifts, a shift inside the per-segment pairing of the W-squares Note, and Two-square or C08 with the fragment constraints were not tested.

## What changed

The CM-Bifid row of the W-squares Note changes from "closed" to "undecidable when one shift is allowed". The other square families gain robustness to one shift. The four FSfree settings remain open, and the candidate-set test could never have reached them.

## What failed

The earlier closure of CM-Bifid did not survive one shift. Both later constraints were too weak or too strong to be informative: the fragments removed no more than random, and the candidate sets removed almost everything from any ciphertext. Some procedure steps were not as preregistered: the controls ran before the commit, the keyword-square null was enlarged after K4 was seen, and the CM-Bifid null was added afterwards.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. The public package reruns the setting counts, free Four-square with the author's 500-shuffle null, C08, one-square Bifid and CM-Bifid on K4, and planted controls. Two-square, keyword squares, the other nulls and the follow-ups are recorded, not rerun. The fragment lists and candidate sets are not published.

## UNKNOWN

Whether an English stage on the 27 (or 6) CM-Bifid settings would separate K4 from shuffles. Whether the four FSfree settings can be decided by any constraint that reaches their pairs. External independent replications: zero.

## Falsification targets

A shifted setting of Four-square, Two-square, keyword squares or one-square Bifid consistent with all 24 crib letters would overturn the closed rows; an error in the exact solvers would too (planted controls 200/200, 199/200, 30/30, 40/40). For CM-Bifid, an exact proof that the 27 settings are inconsistent would restore the closure; an English stage that ranks K4 above size-matched shuffles would make it a candidate.

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-block-phase-shift): `python verify_block_phase_shift.py` recomputes the setting counts (186 → 24 digraph settings, 40 plain squares, 7,176 → 2,765 Bifid block lists), free Four-square on K4 (0/960) and the author's 500-shuffle null (473/500, same seed), C08 on 97 and 92 letters (88/97, 83/92), one-square Bifid (0/2,765) and CM-Bifid (27/2,765) on K4, and planted controls, and prints `PASS`. Standard library only, about ten seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-block-phase-shift). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

An English stage on the 27 CM-Bifid settings with a preregistered threshold, planted controls and size-matched shuffles; for long texts the original 4-gram scorer is enough. A constraint that reaches the FSfree pairs inside the O-segments.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
