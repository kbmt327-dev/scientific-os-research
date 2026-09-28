# Kryptos K4: the two O-segments paired as digraphs (EP-0138)

Check package for the Open Research Lab note
*Can the two O-segments, paired letter by letter, be a digraph cipher?*

```sh
python verify_o_pairs.py   # standard library only, a few seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_o_pairs.py` | The pairs (21+o, 59+o) and the mirror pairing, repeated-input checks, and a brute-force 2x2 Hill solver |
| `results/o-pairs-20260928.json` | The author's recorded results: CP-SAT proofs for the 56 free-square settings, shuffle consistency, keyed squares, controls and the minimal contradicting sets |
| `verify_o_pairs.py` | Recomputes the pair facts (no repeated inputs, Playfair's (R,R), the mirror contradiction) and the 2x2 Hill search in four alphabets with planted controls; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The free-square results are exact proofs from a constraint solver (OR-tools CP-SAT), one model
per setting, up to 120 s each, 1,000 shuffles per setting; the keyed squares use word lists
from an earlier Note. They are recorded, not rerun here. A rerun of the author's code, not an
independent replication.
