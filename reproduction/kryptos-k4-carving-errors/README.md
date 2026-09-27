# Kryptos K4: what carving errors would change (EP-0070, EP-0071, EP-0123)

Rerun package for the Open Research Lab note
*Would a few carving errors reopen the ciphers already ruled out?*

```sh
python verify_carving_errors.py   # standard library only, a few seconds
python make_figure.py out.svg     # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_carving_errors.py` | For a periodic key (Vigenère, Beaufort, variant; A–Z or KRYPTOS), the fewest crib letters that must be wrong at each period, for K4 and for shuffled K4 |
| `results/carving-errors-20260927.json` | Recorded results, including the families not rerun here |
| `verify_carving_errors.py` | Recomputes the table for periods 1–48 with 100 shuffles and prints `PASS` |
| `make_figure.py` | The Note's figure |

This package keeps the crib at its published position. The internal run also slid the crib
by up to two places in each direction (five alignments) and used eight conventions, which gives
slightly smaller counts at some periods (for example 5 rather than 7 at p = 17). A rerun of the
author's code, not an independent replication.

## Not rerun here

Quagmire, Trifid, Hill and running keys with errors (EP-0071), one-error rechecks of the text
keys (EP-0070), and the error distance of different methods (EP-0123). Their outcomes are in
`results/`.
