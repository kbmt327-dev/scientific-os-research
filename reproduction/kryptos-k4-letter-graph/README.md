# Kryptos K4: the crib's letter graph (EP-0101)

Rerun package for the Open Research Lab note
*Which ciphers does the crib's letter graph rule out without choosing a key?*

```sh
python verify_letter_graph.py   # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_letter_graph.py` | K4, the 24 public crib letters, the plaintext-to-ciphertext letter graph, its components after treating crib pairs as errors, the exact number of crib errors a named partition needs, and the pure word-restart check |
| `results/letter-graph-20260927.json` | Recorded results |
| `verify_letter_graph.py` | Recomputes everything and prints `PASS` |
| `make_figure.py` | The Note's figure |

Everything here uses only K4 and its public cribs, so the whole result is rerunnable. It is a
rerun of the author's code, not an independent replication.

## Correction

The internal record (EP-0101) stated that pure word-restart keying fails for every crib
segmentation. Rechecking for this package showed that, counted from the end of the word, it is
compatible with the cribs when `EASTNORTHEAST` is read as one word (2 of 6 segmentations).
Counted from the start of the word it fails for all 6.
