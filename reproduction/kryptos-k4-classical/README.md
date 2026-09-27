# Kryptos K4: the classical families (EP-0032, EP-0018-0020, EP-0051-0056)

Rerun package for the Open Research Lab note
*Which classical ciphers do K4's crib and letter counts rule out?*

```sh
python verify_classical.py      # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_classical.py` | The 24 keystream values in 8 settings (A–Z and keyed KRYPTOS, PALIMPSEST, ABSCISSA alphabets × two forms); periodic and difference-periodic closure for every period at once; the English-unigram running-key test; the letter-count test for transpositions |
| `results/classical-20260927.json` | Recorded results (written by `record.py`), including the families not rerun here |
| `verify_classical.py` | Recomputes everything above and prints `PASS` |
| `make_figure.py` | The Note's figure |

Everything rerun here uses only K4, its public cribs and English letter frequencies. A rerun of
the author's code, not an independent replication.

## Not rerun here

Free alphabets per residue with column statistics, transposition followed by English running
keys, keyed columnar and K3-style rotation, Hill with transposition, Trifid, two keyword layers,
turning grilles. Their outcomes are in `results/`.
