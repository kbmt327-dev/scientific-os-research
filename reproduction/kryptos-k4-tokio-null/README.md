# Kryptos K4: what the TOKIO reading costs once every freedom is paid (EP-0011)

Rerun package for the Open Research Lab note
*How much is the TOKIO reading of K4's Ws worth?*

```sh
python verify_tokio_null.py        # standard library only, under a second
```

It recomputes the exact null and compares it with `results/wgap-full-20260919.json`.
It prints `PASS` when they match. This is a rerun of the author's code, not an
independent replication.

## What is computed

Take any letter that occurs m times in K4, read the gaps between its occurrences as
letters, and ask whether the result is a place name engraved on Berlin's World Clock.
The family of readings covers every multiplicity K4 actually has, two gap definitions,
four anchors, two directions and two alphabet bases (A=1 or A=0). K4 yields 69 strings;
one is a place name, `TOKIO`.

Under the null, the positions of a letter with m occurrences are a uniform m-subset of
the 97 cells. Every reading can be inverted, so the expected number of place-name hits
has a closed form with no sampling:

    P(at least one hit) <= E[hits] = 1.48e-3

`ROM` alone contributes 70% of that. Removing `OSLO`, which a 1997 newspaper report
says was added that year, gives 1.44e-3.

| File | What it is |
|---|---|
| `k4_wgap_full.py` | The reading family and the closed-form null |
| `data/worldclock-place-letters.json` | Letters-only forms of the 146 place names |
| `results/wgap-full-20260919.json` | The recorded result |

## Limits

- The place list is the post-1997 list of 146 names. Kryptos (1988–1990) corresponds to
  the 1985–1997 list of 134 names, which has not been enumerated.
- The choice of the World Clock as the target list was made after the cribs pointed to
  it. That choice is not paid for, so the value is exploratory, not confirmatory.
- The reading gives no key, route or plaintext letter.

## Sources

- K4 ciphertext: Jim Sanborn, *Kryptos* (1990); public transcriptions on
  [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) and by
  [Elonka Dunin](https://elonka.com/kryptos/).
- The W-gap reading `20, 15, 11, 9, 15 → TOKIO`:
  [matbalez, *Kryptos K4: comprehensive research handoff and restart plan*, GitHub gist, 2026](https://gist.github.com/matbalez/8300cb067a5cda55c3b44ef382d517c0).
- `BERLINCLOCK` refers to Berlin's World Clock:
  [Scientific American, 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/).
- Place names: the list on the official site of the clock's designer, Erich John,
  [weltzeituhr-berlin.de](https://weltzeituhr-berlin.de/en/places-worldtimeclock),
  captured through the
  [Internet Archive (12 Aug 2020)](https://web.archive.org/web/20200812142431/https://weltzeituhr-berlin.de/en/places-worldtimeclock).
  Only the letter strings are included here; the author's full frozen copy has SHA-256
  `68b7f888daf72604e4a95a96dc8ba7228813290116851b9d03f5e746dc020578`.
- `OSLO` added in 1997: *Berliner Zeitung*, 12 Dec 1997.

## License

Code and result files: MIT (see `LICENSE`). The K4 ciphertext is Sanborn's and the place
names are factual data from the source above; neither is licensed here.
