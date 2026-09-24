# Kryptos K4: the Ws that bracket both cribs (EP-0057)

Rerun package for the Open Research Lab note
*Do the Ws that bracket both K4 cribs carry structure?*

```sh
python verify_w_brackets.py          # standard library only, a few seconds
```

`verify_w_brackets.py` reruns every K4-facing computation and compares it with
`results/*.json`. It prints `PASS` when everything matches. This is a rerun of the
author's code, not an independent replication.

| File | What it does |
|---|---|
| `k4_common.py` | K4 ciphertext, the 24 public crib letters, additive tableau arithmetic |
| `k4_w_brackets.py` | Part A: exact nulls for the observation. Part B: Ws as inserted nulls (92 letters) with periodic, progressive and autokey keys. Part C: key restarting at each W |
| `k4_w_segments.py` | Part D: the six W-segments as shuffled or reversed blocks, then a periodic key |
| `k4_w_alpha25.py` | Part E: W passes through and the other letters use a 25-letter cipher |

Each probe script also has `--plants` (positive controls that never read K4). In the
author's working repository the probe code was committed before it was run on K4.
Those commit hashes are private, so treat that ordering as the author's claim.

## Result

No reading produced a candidate decryption and no new plaintext letter.

- Periodic, progressive and autokey keys on the 92 non-W letters are compatible only at
  periods where no two crib positions share a residue (25, 26).
- A key that restarts at each W should give both cribs the same keystream, because both
  lie in 15-letter "O" segments. At the 9 shared offsets the additive keys agree at 1–2
  of 9.
- Shuffling or reversing the six segments (92,160 arrangements, 208 distinct crib
  patterns) with a periodic key of period ≤ 46 gives 0 passes.
- Playfair with any square is impossible even if W passes through, because K4 has a
  crib letter enciphered to itself at positions 32 (S) and 73 (K).

Families with a free alphabet per residue or per offset are **not distinguishable**
by the cribs; they are not refuted.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990), CIA headquarters, Langley, Virginia.
  Public transcriptions: [Wikipedia, "Kryptos"](https://en.wikipedia.org/wiki/Kryptos);
  [Elonka Dunin's Kryptos page](https://elonka.com/kryptos/).
- Cribs: `BERLIN` — [WIRED, 2010-11-21](https://www.wired.com/2010/11/clue-kryptos/);
  `CLOCK` — [WIRED, 2014-11-20](https://www.wired.com/2014/11/second-kryptos-clue/);
  `NORTHEAST` — NPR *All Things Considered*, 2020-01-30
  ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle));
  `EAST` — confirmed by Sanborn in August 2020, as recorded in
  [Elonka Dunin's archive](https://elonka.com/kryptos/).
- `BERLINCLOCK` refers to the Berlin World Clock:
  [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
- The W-gap reading `20,15,11,9,15 → TOKIO`:
  [matbalez, *Kryptos K4: comprehensive research handoff and restart plan* (GitHub gist, 2026-07-18)](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).

## License

Code and result files: MIT (see `LICENSE`). The K4 ciphertext and crib letters are
Sanborn's and are quoted for research and commentary; they are not licensed here.
