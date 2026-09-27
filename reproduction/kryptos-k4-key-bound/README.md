# Kryptos K4: how much key K4 needs (EP-0089, EP-0091)

Rerun package for the Open Research Lab note
*How much key does K4 need, and what does that leave decidable?*

```sh
python verify_key_bound.py      # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_key_bound.py` | K4's index of coincidence; English letters through m freely chosen rows (share of simulations as flat as K4); window maps of up to four plaintext letters against the crib |
| `results/key-bound-20260927.json` | Recorded results, including the tests not rerun here |
| `verify_key_bound.py` | Recomputes the simulation (fixed seeds) and the window conflicts, and prints `PASS` |
| `make_figure.py` | The Note's figure |

The simulation draws plaintext letters independently from standard English letter frequencies;
the index of coincidence depends only on letter counts, so this is enough. The internal run used
English text and gave 0.009, 0.027, 0.050 and 0.107 for m = 4, 6, 8 and 16. A rerun of the
author's code, not an independent replication.

## Not rerun here

The sculpture's own text as the coding chart (EP-0089) reads the carved panel, which this site
does not publish. Its outcome is in `results/`.
