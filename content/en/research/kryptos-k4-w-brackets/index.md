---
research_id: KRYPTOS-K4-EP-0057
title: Do the Ws that bracket both K4 cribs carry structure?
date: '2026-09-24'
lang: en
domain: Kryptos K4
type: Finding
status: Observation reproduced; significance downgraded; four readings gave no candidate
evidence_level: Exploratory computation on public ciphertext; not preregistered
peer_reviewed: false
independent_replications: 0
evidence:
  class: exploratory-computation
  source: Public K4 ciphertext and the 24 public crib letters; exact nulls, shuffled-text controls and planted positive controls
review:
  editorial_reviewed: true
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
claim_scope: One post hoc observation about W positions in K4 and four cipher families
  built from it; no decryption and no new plaintext letter
replication:
  independent: 0
  failed: 0
source_episode: KRYPTOS-K4/EP-0057
source_episode_sha256: 0b4f31e6f22ce59f2d590e59e5bf5b5033808acd5df70a98b9fba8382bcfb09a
publication:
  status: publishable
tags:
- kryptos-k4
- cryptanalysis
- negative-result
- en
---

<p class="research-area"><b>Kryptos K4</b><a href="/ja/research/kryptos-k4-w-brackets/" hreflang="ja">日本語</a></p>

## Current finding

K4 has five Ws, at 0-indexed positions 20, 36, 48, 58 and 74. The W at 20 sits just before `EASTNORTHEAST` (21–33) and the W at 74 just after `BERLINCLOCK` (63–73). Both cribs lie inside the two 15-letter gaps between Ws. This is reproduced exactly. But the Ws were chosen after looking. If the letter is left free, the chance that cells 20 and 74 hold the same letter is 0.036, not 0.004. The observation also does not add independent evidence for the known `TOKIO` reading of the W gaps. Four ciphers built on "the Ws are structure" gave no candidate decryption and no new plaintext letter.

## Key figure

![K4 as 97 cells: five Ws, six gaps of length 20, 15, 11, 9, 15, 22, and the two cribs inside the 15-letter gaps](/assets/kryptos-k4-w-brackets.svg)

Each cell is one ciphertext letter. The gap lengths read as letters (A=1) give T O K I O V.

## What this research shows

- The stated facts are correct. Each crib is bracketed on one side only: two letters follow `NORTHEAST` and four precede `BERLIN` before the next W.
- The stated chance of 0.004 is the exact chance that cells 20 and 74, or 34 and 62, both hold W (0.0043). For 20 and 74 alone it is 0.0021. For "at least two of the four cells next to the cribs are W" it is 0.012, not 0.02.
- Choosing the letter W is itself a choice made after looking. Without it, the chance is 0.036 (same letter at 20 and 74) or 0.071 (same letter on both outer sides or on both inner sides).
- If the `TOKIO` reading is right, the gap lengths already fix every W position. So this observation is about where the published cribs fall, and cannot be multiplied with the `TOKIO` evidence.
- Four readings of the Ws as structure were rejected in the families tested (see Results).

## What this research does not show

It does not show that the Ws are random. It does not rule out cipher families that allow a free substitution alphabet for each key position; the 24 crib letters cannot tell those apart. It does not decrypt anything.

## Research question

An observation was submitted to the project: the Ws bracket both public cribs. Is it reproducible and how surprising is it? If the Ws are structure placed by the designer, which simple ciphers follow, and do they survive the cribs?

## Why this matters

K4 attracts many post hoc patterns. The work here shows the three prices one pays before trusting one: the freedom to choose the letter, the dependence on an earlier reading of the same positions, and whether any cipher built on the pattern survives the known plaintext.

## Method

- **Exact nulls.** Five Ws are placed uniformly among 97 cells. Letter-free versions use K4's own letter counts.
- **B. Ws as inserted nulls.** Drop the Ws (92 letters). Test periodic, progressive and ciphertext- or plaintext-autokey keys under Vigenère, Beaufort and variant Beaufort, with the A–Z and the KRYPTOS alphabets.
- **C. The key restarts at each W.** Both cribs lie in "O" gaps. A key that depends only on the gap's letter and the offset within the gap gives both cribs the same keystream. Test the 9 shared offsets.
- **D. The six gaps are blocks.** All 720 orders × 64 reversal patterns × with or without a separator slot. Then a periodic key of period ≤ 46 on the plaintext index. Three shuffles of K4's non-W letters serve as controls.
- **E. W passes through and the rest is a 25-letter cipher.** Mod-25 periodic, progressive and ciphertext-autokey keys with the A–Z and KRYPTOS alphabets minus W. For Playfair, use the rule that no letter enciphers to itself.

Every probe has planted positive controls that never read K4. In the author's working repository the code was committed before it was run on K4 (private history; treat this as the author's claim). Nothing was preregistered.

## Results

| Reading | K4 | Controls | Verdict |
|---|---|---|---|
| B. Ws as inserted nulls | Only periods where no two crib positions share a residue (25, 26) | Planted 18/18 recovered | Rejected |
| B′. Free alphabet per residue | 26 periods compatible | — | Not distinguishable |
| C. Key restarts at each W | Additive keys agree at 1–2 of 9 shared offsets (chance level ≈ 0.35) | Planted 6/6 at 9/9 | Rejected |
| C′. Free substitution per offset | No violation, but only 1 informative offset | — | Not distinguishable |
| D. Gaps as shuffled blocks | 0 passes over 92,160 arrangements | Planted 3/3; shuffles pass only with a single crib constraint | Rejected |
| E. W pass-through, 25-letter cipher | Mod-25 keys: 0 (one progressive pass per setting rests on a single constraint, positions 21 and 73). Playfair: K4 has crib letters enciphered to themselves at 32 (S) and 73 (K), so no square works | Planted 8/8 | Rejected |

One step does real work. Any scheme that shifts the key by the gap's letter (T, O, K, I, O, V) gives both cribs the same shift, because both lie in "O" gaps. On the cribs it therefore reduces to a plain periodic key, which is already dead.

## What changed

The observation is recorded as provisional, not promoted to a hypothesis. An earlier closure in this project ("K4 uses all 26 letters, so every 25-symbol cipher is impossible") had a gap: if W passes through, the other 92 letters need only 25 symbols, and they are exactly the other 25. Playfair is now closed through that gap too.

## What failed

The stated chance for "two or more of four boundary cells" (0.02) does not reproduce; the exact value is 0.012. The first two probe commits were labelled with an episode number already used by a parallel session and were renumbered afterwards.

## Evidence boundary

Public ciphertext and 24 crib letters only. The cribs are Sanborn's choice of which words to release, so their positions are not a random sample. All tests are exploratory and exact within the stated families.

## UNKNOWN

Whether the Ws were placed on purpose. Whether 5×5 Bifid, Two-square or Four-square with W passing through survive the cribs. Whether transposition inside each gap, combined with block moves, does. External independent replications: zero.

## Falsification targets

A cipher in any rejected family that turns K4 into the published cribs would refute the rejection; the rerun below would then show a mismatch. A principled reason to prefer W over other letters, fixed before looking, would restore part of the 0.004.

## Reproduce

[Public code](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-brackets): `python verify_w_brackets.py` reruns every K4-facing computation with the standard library in a few seconds and compares it with the recorded results. It prints `PASS`. It is a rerun of the author's code, not an independent replication.

## Evidence / Artifacts

[Probe scripts, recorded results and positive controls](https://github.com/kbmt327-dev/scientific-os-research/tree/main/reproduction/kryptos-k4-w-brackets). Code and results are MIT-licensed; the ciphertext and cribs are quoted, not licensed.

## External audit

External independent replications: zero. No cryptographer has reviewed this note.

## Next experiment

Bifid, Two-square and Four-square with W passing through, and block moves combined with transposition inside each gap.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990), CIA headquarters, Langley, Virginia. Public transcriptions: [Wikipedia, "Kryptos"](https://en.wikipedia.org/wiki/Kryptos); [Elonka Dunin's Kryptos page](https://elonka.com/kryptos/).
- Cribs: `BERLIN` — [WIRED, 21 Nov 2010](https://www.wired.com/2010/11/clue-kryptos/); `CLOCK` — [WIRED, 20 Nov 2014](https://www.wired.com/2014/11/second-kryptos-clue/); `NORTHEAST` — NPR *All Things Considered*, 30 Jan 2020 ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)); `EAST` — confirmed by Sanborn in August 2020, as recorded in [Elonka Dunin's archive](https://elonka.com/kryptos/).
- `BERLINCLOCK` refers to Berlin's World Clock: [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
- The W-gap reading `20, 15, 11, 9, 15 → TOKIO`: [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).
- The bracketing observation was submitted to the project after inspection of the ciphertext; its original wording is kept in the internal record.
