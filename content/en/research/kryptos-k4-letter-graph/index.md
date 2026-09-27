---
research_id: KRYPTOS-K4-EP-0101
title: Which ciphers does the crib's letter graph rule out without choosing a key?
date: '2026-09-26'
lang: en
domain: Kryptos K4
type: Finding
status: All 21 crib letters form one component; every cipher that keeps a fixed partition of the alphabet with blocks under 21 letters is impossible without crib errors
evidence_level: Exact combinatorial argument on public ciphertext and cribs; fully rerunnable
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters only
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: Ciphers whose per-position maps each keep one fixed partition of the alphabet, and pure word-restart keying; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0101
source_episode_sha256: 19ae4896562c109279caadc34716d00d1afdbe0a9cf0bd02c2a38da43b28284f
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- structural
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-letter-graph/" hreflang="ja">日本語</a></p>

## Current finding

Draw each of K4's 24 crib pairs as an edge from the plaintext letter to the ciphertext letter. All 21 letters that appear in the cribs join into **one connected component**. So any cipher in which every position's substitution keeps a fixed grouping of the alphabet (each group mapped to itself) needs a group of at least 21 letters. Groupings such as vowels and consonants, halves of the alphabet, keyboard rows, Morse-length classes, Polybius rows or cube positions are impossible without crib errors, whatever the key. Named groupings need 7 to 19 wrong crib letters.

## Key figure

![A circle of 21 letters joined by arrows into a single connected graph, with loops at S and K for the two self-encryptions; text beside it lists the largest component after 1, 2 and 3 crib errors (12, 9, 7) and the errors named partitions need](/assets/kryptos-k4-letter-graph.svg)

## What this research shows

- The crib's letter graph is connected on all 21 crib letters, and S→S (position 32) and K→K (position 73) encrypt to themselves.
- A cipher whose maps keep a fixed partition must put the whole component in one block. Any partition whose largest block has fewer than 21 letters is impossible with no crib error; under 12 letters, also with one error; under 9, with two; under 7, with three.
- For specific partitions, the exact number of crib pairs that cross between blocks is the number of crib errors needed: vowels (with Y) and consonants 7, A–Z halves 8, A–Z parity 8, KRYPTOS-alphabet halves 8, QWERTY rows 12, Morse-length classes 18, rows of a 5×5 Polybius square 19.
- Swapping two fixed halves at every position (Porta type) is impossible because of the two self-encryptions.
- Pure word-restart keying (each position's row, any bijection, set only by its place in its word) fails for every segmentation of the cribs when counted from the start of the word.

## What this research does not show

It says nothing about ciphers whose per-position maps mix the whole alphabet, which is most ciphers. It does not rule out a partition cipher if the cribs contain many errors. Word-restart keying counted from the end of the word survives when `EASTNORTHEAST` is one word, and mixed rules (word position with word number) pass at the rate of random segmentations; neither is evidence for them.

## Research question

Without choosing any key, alphabet or table, what does the pattern of which crib letters encrypt to which rule out?

## Why this matters

Most tests in this program fix a family and search its keys. This one needs no key at all: it rules out whole classes of design, including unusual "solid" or grouped systems that would be hard to enumerate, from a property of the 24 crib pairs alone. It also sets how many crib errors each class would need, so a reader can judge how much the conclusion depends on the cribs being exact.

## Method

- **Graph.** One edge per crib pair, plaintext letter to ciphertext letter; components by union–find.
- **Errors.** For k = 1, 2, 3, every choice of k crib pairs is removed and the smallest possible largest component is recorded.
- **Named partitions.** The number of crib pairs whose two letters fall in different blocks, which is exactly the number of crib errors that partition needs.
- **Word restart.** Six segmentations of the cribs (`EAST|NORTHEAST`, `EASTNORTHEAST`, `EAST|NORTH|EAST` with `BERLIN|CLOCK` or `BERLINCLOCK`); position in the word counted from the start or the end; two positions with the same word position conflict if equal plaintext letters give different ciphertext letters, or different ones give equal letters.

## Results

| After treating k crib pairs as errors | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Largest component (letters) | 21 | 12 | 9 | 7 |

| Partition | Largest block | Crib errors needed |
|---|---|---|
| Vowels (AEIOUY) / consonants | 20 | 7 |
| A–Z halves; A–Z parity; KRYPTOS-alphabet halves | 13 | 8 each |
| QWERTY rows | 10 | 12 |
| Morse-length classes | 12 | 18 |
| Rows of a 5×5 Polybius square | 5 | 19 |
| 3×3×3 cube by cubie type (8 / 12 / 6) | 12 | ≥ 1 for any assignment |

| Segmentation | Word position from start | From end |
|---|---|---|
| `EAST\|NORTHEAST` + either | conflicts | conflicts |
| `EASTNORTHEAST` + either | conflicts | **compatible** |
| `EAST\|NORTH\|EAST` + either | conflicts | conflicts |

## What changed

Grouped and "solid" designs no longer need to be enumerated one by one. The internal record had stated that pure word-restart keying fails for every segmentation; rechecking for this Note found that the from-the-end form is compatible when `EASTNORTHEAST` is one word, and the record was corrected.

## What failed

The stated word-restart result did not survive the recheck in full, as described above.

## Evidence boundary

Public K4 ciphertext and the 24 public crib letters. The argument is exact; the only assumption is that the cribs are right, and the tables give how many errors each conclusion tolerates.

## UNKNOWN

Whether any real design of the period used a fixed partition. Whether the cribs contain errors. External independent replications: zero.

## Falsification targets

A published correction to the cribs that splits the component, or evidence of several crib errors, would reopen partition ciphers with small blocks.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-letter-graph): `python verify_letter_graph.py` rebuilds the graph from K4 and the cribs, recomputes the component sizes after 1–3 errors, the error counts for each named partition and the word-restart conflicts, and prints `PASS`. It uses only K4 and the cribs and runs in a few seconds. A rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Code, recorded results and figure script](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-letter-graph). MIT-licensed; the ciphertext and cribs are quoted.

## External audit

No external independent replication. No review by a cryptographer.

## Next experiment

None for partition ciphers. The surviving word-restart form is a hand-made-chart family and cannot be decided from K4 alone.

## Sources

- K4 ciphertext and cribs: Jim Sanborn, *Kryptos* (1990); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin](https://elonka.com/kryptos/); [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/), [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020.
