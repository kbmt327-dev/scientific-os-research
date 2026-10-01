---
research_id: KRYPTOS-K4-EP-0091
title: How much key does K4 need, and what does that leave decidable?
date: '2026-09-26'
lang: en
domain: Kryptos K4
type: Finding
status: In a model that picks chart rows uniformly, a flat IC needs a row spread of about 3 bits per position, more than English redundancy (2.86 bits) -- a model-internal quantity, not a general bound; only keys with a short description can be decided from K4; position-independent maps are impossible
evidence_level: Simulation with fixed seeds and exact crib arguments on public ciphertext; not preregistered
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; English letter frequencies; simulated ciphertexts through freely chosen rows
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: A lower bound on the key freedom K4's letter statistics require, what that implies for decidability, and maps the crib forbids outright; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0091
source_episode_sha256: 5d9ff9c773580a0cfd5f0fcfbb3ad89101adc13e7881d34f342951f74ff6b2d4
publication:
  status: publishable
tags:
- kryptos-k4
- information
- structural
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-key-bound/" hreflang="ja">日本語</a></p>

## Current finding

K4's letters are almost as evenly spread as random letters (index of coincidence 0.036; English is about 0.066). Sending English through freely chosen substitution rows makes it that flat in about 5% of cases only when there are about 8 rows to choose from at each position, which in this model is **a row spread of 3 bits per position**. English carries about **2.86 bits** of redundancy per letter. So if the key were chosen freely letter by letter, K4 alone could not determine it, however clever the search. A solvable K4 must pair a short technique with a key that has a short description: a rule, a known text, a physical layout.

## Later check (2026-09-30)

An IC recheck (EP-0152) asked what the flat IC excludes on its own. Plaintext was random 97-letter windows of an English text corpus, 20,000 simulations per key model. K4's IC 0.0361 does not separate a uniform key (mean 0.0385, SD 0.0028, P(IC ≤ K4) = 0.22) from a key with English letter frequencies (independent letters: mean 0.0400, SD 0.0032, P = 0.107; English text as key: P = 0.103). A random periodic key is rejected by the IC alone only for periods up to 4 at the 1% level and up to 8 at the 5% level (period 5: P = 0.015). So the IC can prune short random periods, not running keys. The dated numbers above are unchanged; the 3-bit quantity concerns freely chosen rows, not this test. The package reruns the uniform model only (20,000 draws gave 0.219); the English-key and periodic values need the corpus and are recorded in `results/ic-recheck-20260930.json`.

## Key figure

![Line chart of the share of simulated ciphertexts as flat as K4 against bits of key per position: 0 at 1 bit, 0.8% at 2 bits, 4.6% at 3 bits, 10% at 4 bits; a dashed red line marks English redundancy at 2.86 bits](/assets/kryptos-k4-key-bound.svg)

## What this research shows

- K4's flat letter counts are rare for English through few rows (0.8% with 4 rows) and become plausible at about 8 rows (4.6%): in the uniform-row model, a row spread of at least about 3 bits per position.
- That exceeds English redundancy (2.86 bits per letter), so a freely chosen key sequence is past the point where the plaintext is determined; outside the cribs nothing could be read with confidence.
- Any map that does not depend on position is impossible without crib errors: `EAST` occurs twice in `EASTNORTHEAST` and enciphers to `FLRV` and `GKSS`. This rules out windows of up to four plaintext letters, a word-level alphabet and a fixed homophonic code.
- The one family that is a different method and decidable from K4 alone, the sculpture's own text used as the coding chart (18,624 settings), was refuted: K4 reaches at most 6 of 24 crib letters, while all 1,000 shuffles reach 6 or more.

## What this research does not show

The "3 bits per position" is a quantity inside a model that picks among m rows uniformly (the spread of row use, the entropy of its marginal distribution); it is neither a lower bound on the key's description length nor a bound for every procedure. A rule-driven row choice, such as a periodic key, can have a 3-bit spread and still be short to describe (added 2026-09-28). It does not say the key is random, only that it must look flat and be describable briefly to be recoverable. It does not rule out a hand-made chart; that family is simply not decidable from K4. The hypothesis that the key or chart was chosen by hand at each position would explain every observed feature and predicts that public data cannot decide K4; it is a hypothesis, not a finding.

## Research question

Without assuming a cipher family, how much key freedom do K4's letter statistics require, and what does that imply about which families can be decided from K4 alone?

## Why this matters

It sets the ground rules for everything else. A family with a freely chosen key at each position cannot be tested on K4, however it is framed; only short-description keys can. It also explains why the program's negative results are logical refutations of short procedures rather than measurements of how unusual K4 is.

## Method

- **Index of coincidence.** K4's IC compared with English and uniform letters.
- **Free rows.** English letters (drawn from standard frequencies; the IC depends only on letter counts) enciphered by m random substitution rows, the row picked at random at each position; the share of 97-letter ciphertexts with IC at or below K4's, 4,000 trials per m.
- **Redundancy.** English entropy 4.70 bits per letter minus 1.84 bits per letter from a character model: 2.86 bits.
- **Position-independent maps.** For every window of up to four plaintext letters, look for two crib positions with the same window and different ciphertext letters.
- **The sculpture's text as chart (EP-0089).** A look-up family fixed before running, with 12 planted controls and 1,000 whole shuffles.

## Results

| Freely chosen rows m | 2 | 4 | 6 | 8 | 12 | 16 | 26 |
|---|---|---|---|---|---|---|---|
| Key bits per position | 1 | 2 | 2.6 | 3 | 3.6 | 4 | 4.7 |
| Share with IC ≤ K4 | 0 | 0.008 | 0.026 | 0.046 | 0.075 | 0.101 | 0.130 |

| Test | Result |
|---|---|
| Window maps of 1–4 plaintext letters (10 shapes) | All 10 conflict with the crib (e.g. E→F at 21 and E→G at 30) |
| Sculpture's text as coding chart | K4 best 6/24; all 1,000 shuffles ≥ 6 (median 7); controls 12/12 |
| Word-by-word Trifid | Disfavoured: IC ≤ K4 in 3.7% of simulations; the 27th symbol absent in 7.2% |
| Fixed digraph chart | Open: aligned repeats 4 (English P 0.13, uniform P 0.09) |

## What changed

The program stopped looking for "a different method decidable from K4 alone" as if one must exist. After this result, the remaining different methods are either short-description families (testable, and tested in later Notes) or hand-made charts that need an outside source.

## What failed

The search for a decidable different method in this round found only one, and it was refuted. The published K1 and K3 worksheets were read for how a K4 chart's rows might be made; they fix nothing for K4.

## Evidence boundary

Public K4 ciphertext and cribs, English letter frequencies, and a character-level estimate of English entropy. The sculpture-text test reads the carved panel, which this site does not publish; its result is recorded.

## UNKNOWN

Where K4's key comes from. Whether the cribs contain errors. External independent replications: zero.

## Falsification targets

A demonstration that English through two or three rows often reaches K4's IC would lower the bound; a short-description key that fits the cribs would make it moot.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-key-bound): `python verify_key_bound.py` recomputes K4's IC, the free-row simulation with fixed seeds and the window conflicts, and prints `PASS`. Standard library only, a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-key-bound). MIT-licensed.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

Test key sources with a short description separately from the chart they drive (reported in later Notes).

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
- Ed Scheidt on masking the English and solving the technique first: [WIRED 2005](https://www.wired.com/2005/01/inside-info-on-kryptos-codes/).
- Unicity distance: Claude E. Shannon, "Communication Theory of Secrecy Systems", *Bell System Technical Journal* 28 (1949).
