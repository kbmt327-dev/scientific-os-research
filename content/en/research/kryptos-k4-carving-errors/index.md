---
research_id: KRYPTOS-K4-EP-0071
title: Would a few carving errors reopen the ciphers already ruled out?
date: '2026-09-26'
lang: en
domain: Kryptos K4
type: Finding
status: One error reopens nothing; with up to five, tightly constrained families stay closed and loosely constrained ones become undecidable; for every family K4 needs as many errors as random ciphertext
evidence_level: Exact minimum-error counts and relaxed crib tests with planted controls and shuffle nulls on public ciphertext and cribs
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; relaxed crib tests, planted positive controls, shuffled-ciphertext nulls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: How the program's main rejections change if one to five crib or carving errors are allowed, for K1–K3-form families and for the different methods tested later; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0071
source_episode_sha256: be936dda3db3eaf7e377804574770f736fb55d789ceb29963f39737d09fae908
publication:
  status: publishable
tags:
- kryptos-k4
- robustness
- carving-errors
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-carving-errors/" hreflang="ja">日本語</a></p>

## Current finding

Kryptos has known carving errors in K1–K3, so K4 might have some too. Allowing one wrong crib letter reopens none of the rejected families. Allowing up to five, families that the cribs constrain heavily (periodic keys up to period 22–23, Trifid, 2×2 Hill) stay closed, while loosely constrained ones (free alphabets per residue, 3×3 Hill, English running keys) can no longer be decided. In every family K4 needs about as many errors as shuffled ciphertext does, so "a few carving errors" does not favour any family.

## Later check (2026-09-30)

The 97 ciphertext letters themselves were checked against photographs of the sculpture (EP-0147), with the judgment rule committed before looking. The photographs (viewed only, not saved) were Carol M. Highsmith's back view in the Library of Congress (item 2011631531) and three photographs by Jim Gillogly (1999-10-27). Every one of the 97 positions was read clearly in at least one photograph, and all 97 agree with the transcription used throughout this program: **0 discrepancies**. The three line breaks (after the first 4 letters and then every 31) were confirmed at the seam and the left edge. Three letters that were unclear in one photograph were read clearly in another. Limitation: the reader knew the reference transcription while reading, so a misreading cannot be fully excluded. This concerns transcription, not carving: it does not tell whether the carved letters are what the artist intended, so the counts above stand unchanged. It does mean that results that read the non-crib letters do not rest on a transcription error. The summary is in `results/transcription-check-20260930.json`; the photographs are not published.

## Key figure

![Dot-and-bar chart over periods 1 to 48: the fewest wrong crib letters a periodic key needs, K4 as dots and the range of 100 shuffles as bars; K4 needs more than 5 at every period up to 23 and lies inside the shuffle range almost everywhere](/assets/kryptos-k4-carving-errors.svg)

## What this research shows

- With one error the main rejections of the program hold, and nothing new opens (Quagmire, Trifid and Hill give no candidate).
- A periodic key needs at least 7 wrong crib letters at every period up to 23 in this package's conventions (6–10 at 18–22 with crib slips allowed internally), so a handful of carving errors cannot rescue it.
- For the different methods tested later, the fewest crib letters to drop is small for some (Two-square 1, CM-Bifid 1, Four-square 2) but random ciphertext needs just as few, so errors do not single out a family.

## What this research does not show

It does not estimate how many errors K4 actually has. It does not rescue loosely constrained families; it only shows that with enough allowed errors they cannot be decided either way.

## Research question

If some crib letters are wrong (carving errors, or a published crib that is slightly off), which of the program's rejections survive, and does allowing errors bring K4 closer to any family than random ciphertext?

## Why this matters

Every rejection in this program assumes the 24 crib letters are exact. Kryptos has documented misspellings in K1–K3, so the assumption needs a price: how many errors each conclusion tolerates.

## Method

- **Minimum errors, periodic keys.** For each period and convention (Vigenère, Beaufort, variant; A–Z or KRYPTOS), the fewest crib letters that must be wrong, computed exactly per residue class. Internally also with the crib slid up to two places each way.
- **Relaxed crib tests (EP-0070, EP-0071).** The main rejected families (periodic, free alphabets per residue with column IC, Quagmire, Trifid, Hill, Kryptos-text stride keys, World Clock keys, English running keys) rerun allowing one error, then up to five.
- **Error distance of different methods (EP-0123).** For each later family, the fewest crib letters to drop before it becomes consistent.
- **Controls.** Planted errors in planted ciphertexts; shuffled K4 as the null for every count.

## Results

| Family | Errors K4 needs | Random ciphertext | Up to 5 errors |
|---|---|---|---|
| Periodic key, p ≤ 16 | ≥ 7 | the same range | closed |
| Periodic key, p = 18–22 | 6–10 | the same range | closed |
| Periodic key, p = 17 and ≥ 23 | ≤ 5 | the same | not decidable |
| Periodic Trifid | ≥ 10 | 9–22 | closed |
| Hill 2×2 | 6+ blocks | the same | closed |
| Hill 3×3 | 3–4 blocks | the same | not decidable |
| Kryptos-text stride and World Clock keys | 14 | 14–15 | closed |
| Free alphabet per residue, p ≥ 10 | — | shuffles pass 45–100% | not decidable |
| English running key | — | shuffles almost pass | loses power |

| Different method (EP-0123) | Fewest crib letters to drop | Shuffles as low |
|---|---|---|
| Two-square | 1 | 75 of 200 |
| Four-square | 2 | 26 of 200 |
| CM-Bifid | 1 | 50 of 50 |
| Periodic Hill (decidable settings) | 1 | 10 of 10 |
| Single free rotor | 7 | 159 of 200 |
| Fixed homophones | 9 | 91.7% |

In this package's rerun, K4 is below all 100 shuffles at one period of 48 (p = 39), about what chance gives.

## What changed

The program's rejections are now stated with how many errors each tolerates. The families that become undecidable under errors are marked as such rather than as rejected.

## What failed

Scoring the many Quagmire passes that five errors allow (5.45 million lines) was computationally out of reach and was stopped; those periods are marked not decidable.

## Evidence boundary

Public K4 ciphertext and cribs. The periodic minimum-error table is rerun in the public package. The relaxed tests of the other families use texts and solvers not published here; their outcomes are recorded.

## UNKNOWN

How many errors K4's carving or published cribs contain. External independent replications: zero.

## Falsification targets

Evidence that K4 has more than five errors in the crib region would reopen the periodic families marked closed.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-carving-errors): `python verify_carving_errors.py` recomputes the fewest crib errors for periodic keys at periods 1–48 for K4 and 100 shuffles, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results including families not rerun here, and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-carving-errors). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Allowing four to seven crib errors in the procedure enumerator (running at the time of writing).

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
