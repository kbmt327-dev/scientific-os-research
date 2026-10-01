---
research_id: KRYPTOS-K4-EP-0179
title: Do keys that follow the plaintext (plaintext autokey, a plaintext-indexed periodic key) fit K4's cribs?
date: '2026-09-30'
lang: en
domain: Kryptos K4
type: Negative Result
status: Plaintext autokey (primer length <= 20, A-Z / KRYPTOS x three tables) needs at least 6 crib letters treated as errors in every one of 120 cells; the plaintext-indexed periodic key with shift tables fails at every period <= 23 for the 60 listed sets; logical refutation, not rarer than random; the period-24 passes and the arbitrary-row form are undecidable
evidence_level: Exact consistency tests on the public ciphertext and cribs; code for both committed before any run on K4; the extension to every set V was added while writing this Note (post hoc)
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; chain propagation along residue classes and consistency of relative key indices; shuffles of the ciphertext with the cribs kept; planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Only plaintext autokey (lag = primer length 1-20, three standard tables x two alphabets) and a periodic key whose index advances one extra step after a plaintext letter in a set V (60 sets x periods 1-24); no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0179
source_episode_sha256: cfda8298610b8adffe0f8213a30dba407128bac2caa889334729381986f91f0d
publication:
  status: publishable
tags:
- kryptos-k4
- autokey
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-plaintext-keys/" hreflang="ja">日本語</a></p>

## Research question

Do ciphers whose key changes with the plaintext history fit K4's cribs? Two forms:

1. **Plaintext autokey (EP-0150).** The first L letters are a primer; after that the plaintext L letters back is the key (k_i = P_{i−L}). Tables: Vigenère, Beaufort, variant Beaufort; alphabets A–Z and KRYPTOS.
2. **Plaintext-indexed periodic key (EP-0179).** A periodic key K[j mod p] whose index j advances one extra step after a plaintext letter in a set V (j_{i+1} = j_i + 1 + [P_i ∈ V]).

## Why this matters

This family had earlier been set aside for another reason. About K5, published in 2025, Scientific American (2025-11-12) wrote that the two messages "share some of the same coded words in the same position". Read as "K4 and K5 share ciphertext substrings", that rules out nearly every key that follows the plaintext history.

A check of the primary wording (EP-0153) found that this sentence is the reporter's own, outside quotation marks. Sanborn's letter of the same day says that K5 has the word BERLINCLOCK in the same position as K4, which is a plaintext word. No primary source says the ciphertext substrings are the same. So the ground for excluding plaintext-history keys is gone, and each such family has to be checked by computation.

Both forms are variants of the K1–K3 shifted table. They were run as a check after the exclusion lost its basis, not as a main-line hypothesis. The arbitrary-row form of EP-0179 is a different method.

## Method

- **Plaintext autokey.** No primer search is needed: the table is invertible both ways, so along each residue class mod L one known plaintext letter fixes the whole class. A class with two or more crib letters is a test. In each class the anchor with the fewest disagreements with the other crib letters is chosen, and the disagreements are summed ("conflicts"). L = 1–40 was computed; the requested range L ≤ 20 gives 120 cells (2 alphabets × 3 tables × 20 lags). L ≤ 12 was already covered by an earlier general linear test (EP-0016).
- **Plaintext-indexed key.** Inside each crib the plaintext is known, so the relative index of every crib letter is fixed. The plaintext between the cribs (34–62) is unknown, so the offset between the cribs is free (0 to p−1). With shift tables (A–Z / KRYPTOS × three tables), crib letters on the same index need the same key; with arbitrary rows, the (P, C) pairs on the same index must form a partial one-to-one map. A cell (V, p) passes if some offset gives no conflict.
- **Sets V.** 60: the 26 single letters; vowels, vowels+Y, consonants, consonants−Y; A–M and N–Z; and the letter sets of 14 words from another part of the sculpture with their complements (28). The code's docstring says 64; recounting the list gives 60.
- **Null and controls.** The crib plaintext kept and the 97 ciphertext letters shuffled (10,000 for autokey, 1,000 for the indexed key). Planted texts: random letters with the cribs written in, enciphered (24 for autokey, 40 for the indexed key). Code for both was committed before any run on K4.

## Results

**Plaintext autokey (L ≤ 20, 120 cells)**

- Every cell needs **at least 6** crib letters treated as errors; no cell fits without errors.
- The minimum 6 occurs at A–Z variant Beaufort L = 17, KRYPTOS Vigenère L = 16 and 17, KRYPTOS Beaufort L = 18. L ≤ 12 gives 10–21, reproducing EP-0016.
- Shuffled ciphertexts reach a minimum of 6 or fewer over the 120 cells in 96% of 10,000 shuffles: K4 is at the level of random ciphertext.
- Planted controls: 24/24 at 0 conflicts. With two carving errors the conflicts become 0–7, because an error propagates along its chain; with errors allowed, this statistic cannot decide.

**Plaintext-indexed key (60 sets × periods 1–24, 1,440 cells)**

| Form | K4 passes | Shuffles (1,000) | Controls |
|---|---|---|---|
| Shift tables | 14, all at period 24, V a single letter that never moves an index inside the cribs (D F G J K M P Q U V W X Y Z) | mean 20.1; ≥ K4 in 100% | 40/40 |
| Arbitrary rows | 934 (241 at periods ≤ 12) | mean 915; ≤ K4 in 61% | 40/40 |

The 14 shift-table passes are a degenerate case: V shares no letter with the cribs, so no extra step happens inside them, and the cipher is a plain period-24 key with a free offset between the cribs. Each crib is shorter than 24 and the offset is free, so almost no test across the two cribs remains; shuffles pass more often than K4.

**Every set V (a post hoc check added while writing this Note).** Inside the cribs only 12 letters move an index (those followed by another crib letter: A B C E H I L N O R S T), so V acts only through its intersection with them, and 4,096 classes cover every possible set. K4's shift-table passes over 4,096 classes × 24 periods: 6 cells — the degenerate class above (empty intersection, period 24), two sets with many crib letters at period 23, and three at period 24. Shuffled ciphertexts (50) pass 12.8 cells on average, 3.6 at periods ≤ 23, so K4 is at random level. "Closed at periods ≤ 23" therefore holds for the 60 listed sets but does not extend to every set; with V freely chosen, this test cannot decide.

## Current finding

Plaintext autokey (primer ≤ 20 letters, A–Z / KRYPTOS, three tables) is inconsistent with the cribs if there are no carving errors. The plaintext-indexed periodic key with shift tables is inconsistent at periods ≤ 23 for the 60 listed sets. These are logical refutations, not evidence that K4 is rarer than random. Period 24, the arbitrary-row form and freely chosen sets are undecidable.

## Key figure

![Bar chart: for each autokey lag L = 1 to 20, the fewest crib letters that must be treated as errors over the six table and alphabet combinations. 20 at L = 1, falling roughly with L: 12 at L = 10, 8 at L = 15, 6 at L = 16 to 18, 8 at L = 19, 10 at L = 20; no lag reaches 0. A note below says planted ciphers give 0 (24 of 24), 96% of shuffles reach a minimum of 6 or fewer, the plaintext-indexed key has no pass at periods up to 23 for the 60 listed sets, and its 14 passes at period 24 are the degenerate case](/assets/kryptos-k4-plaintext-keys.svg)

## What this research shows

- Plaintext autokey with lag = primer length 1–20 cannot reproduce the 24 crib letters without errors.
- A periodic key whose index advances one extra step after chosen plaintext letters fails with shift tables at periods ≤ 23 for the 60 listed sets.
- The earlier ground for excluding plaintext-history keys (the magazine's sentence about shared coded words in K5) is a reporter's paraphrase, not the artist's wording; these families now rest on computed negatives only.

## What this research does not show

It does not show that K4 is rarer than random: every statistic is at shuffle level. Plaintext autokey with carving errors allowed, primers longer than 20, the arbitrary-row form, period 24, and sets V outside the 60 listed are not decided. Other plaintext-history forms (combinations with ciphertext autokey, word-unit keys) were not tested.

## What changed

Families set aside because of a reporter's paraphrase about K5 have been rechecked by computation. Plaintext autokey and the plaintext-indexed periodic key (shift tables, listed sets) stay closed without that ground.

## What failed

No setting fit. Extending to every set V gives two passes at period 23; they are at shuffle level and are not evidence, but "closed for any set" can no longer be said.

## Evidence boundary

Public K4 ciphertext and cribs, and the author's code. All 240 autokey cells were recomputed and match the record. For the indexed key, the 28 sets derived from words in another part of the sculpture are not published here, so the default check uses the other 32 sets and `--full` uses the 4,096 classes that cover every set. The 1,000-shuffle null for the 60 sets is recorded.

## UNKNOWN

Plaintext autokey with carving errors allowed. The arbitrary-row form and period 24. Keys in word units of the plaintext. External independent replications: zero.

## Falsification targets

A primer and table in the stated autokey range that reproduce all 24 crib letters without errors would overturn this; so would a key and offset consistent with the cribs for one of the 60 listed sets at a period ≤ 23 (all planted controls were found: 24/24 and 40/40).

## Reproduce

[Check package](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-plaintext-keys): `python verify_plaintext_keys.py` recomputes all 240 autokey cells and compares them one by one with the record (0 differences), runs 24 planted controls and 1,000 shuffles (minimum ≤ 6 in 95.2%; the record has 96.4% over 10,000), and for the indexed key recomputes the 14 shift-table passes on 32 sets, 40 planted controls and 200 shuffles (20.3 shift-table passes on average). It prints `PASS`, standard library only, in under a minute. `--full` runs 10,000 autokey shuffles and checks every set V (a few minutes). A rerun of the author's method, not an independent replication.

## Evidence / Artifacts

[Recorded results, check script and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-plaintext-keys). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Plaintext autokey with carving errors needs a statistic other than conflict counts (an exact test with the error positions as variables). If K5's ciphertext is published, the plaintext word it shares with K4 at the same position would test directly whether the key follows the plaintext history.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); crib releases [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- K5 report: [Scientific American 2025-11-12](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/); Sanborn's open letter of 2025-11-12 (paraphrased).
