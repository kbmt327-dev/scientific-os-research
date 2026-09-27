# Kryptos K4: the Ws as separators and 25-letter squares (EP-0110, 0115, 0120, 0125, 0126, 0128)

Rerun package for the Open Research Lab note
*If the Ws are separators, can a 5×5 square cipher produce K4?*

```sh
python verify_w_squares.py      # standard library only, about a second
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_w_squares.py` | K4 with the Ws removed (92 letters), three digraph pairings, the exact free-Four-square test with planted controls and a shuffle null, the Two-square self-encryption witnesses, and doubled ciphertext pairs |
| `results/w-squares-20260927.json` | Recorded results, including searches not rerun here |
| `verify_w_squares.py` | Recomputes the K4-only checks and prints `PASS` |
| `make_figure.py` | The Note's figure |

A rerun of the author's code, not an independent replication.

## Not rerun here

The keyword-square search (925,600 settings, with an English word list), the exact Two-square
and CM-Bifid solvers, the Bifid annealing, the Playfair-plus-mask and squares-plus-mask searches,
and the 5×5 grid searches. Their outcomes are listed in `results/`.
