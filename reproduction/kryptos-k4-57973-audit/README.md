# Kryptos K4: an audit of the reverse-Gromark-57973 claim (EP-0001)

Rerun package for the Open Research Lab note
*Does primer 57973 stand out once the model's freedom is counted?*

```sh
python verify_57973_audit.py          # deterministic parts, under a minute
python verify_57973_audit.py --full   # plus the two random controls, about two minutes
```

`verify_57973_audit.py` reruns `k4_audit.py` and compares it with
`results/audit-20260919.json`. It prints `PASS` when everything matches. This is a
rerun of the author's code, not an independent replication.

## What is audited

A research handoff given to this project on 2026-09-18 argued that K4 is a Gromark
cipher with primer 57973, keystream reversed, and two arbitrary 26-letter alphabets.
It cited these numbers, all of which reproduce exactly from the public ciphertext and
the 24 crib letters:

| Claim | Reproduced |
|---|---|
| Primers compatible with the cribs, forward / reversed | 39 / 23 of 100,000 |
| 57973 forward / reversed | incompatible / compatible |
| Alphabet configurations for 57973 | 29,120 (5 components) |
| Most forced plaintext letters, and at which primers | 13, at 57928, 57973, 59346 |

It also pins down that "reversed" means: generate 97 digits forward, then reverse the
sequence. Only that reading matches all 13 mask digits the handoff states.

The three controls the handoff did not run:

1. **Uniform random 97-digit masks** pass the same crib test at 813 of 2,000,000
   (4.07 × 10⁻⁴), no less often than Gromark (3.90 × 10⁻⁴ forward, 2.30 × 10⁻⁴ reversed).
   The count measures the freedom of two arbitrary alphabets, not Gromark.
2. **The 13 forced letters need the identity route with shift 0.** Over 284
   paper-executable routes × 97 cyclic shifts × 2 directions = 55,096 choices, 482 are
   compatible and up to 21 letters are forced, a different set each time.
3. **All 40 randomly drawn primers** admit at least one compatible route.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990); public transcriptions on
  [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by
  [Elonka Dunin](https://elonka.com/kryptos/).
- Crib releases: [WIRED 2010](https://www.wired.com/2010/11/clue-kryptos/),
  [WIRED 2014](https://www.wired.com/2014/11/second-kryptos-clue/), NPR 2020
  ([transcript](https://www.kunc.org/2020-01-30/a-new-and-final-clue-to-kryptos-a-long-standing-puzzle)),
  [Elonka Dunin's archive](https://elonka.com/kryptos/) for `EAST`.
- The handoff builds on
  [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).
  Only its numeric claims are restated here.
- Gromark cipher: the American Cryptogram Association's cipher type of that name
  (keystream digit = sum of the digits five and four places back, mod 10).

## License

Code and result files: MIT (see `LICENSE`). The K4 ciphertext and crib letters are
Sanborn's and are quoted for research and commentary; they are not licensed here.
