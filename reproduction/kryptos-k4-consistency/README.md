# Kryptos K4: ciphers the cribs refute by consistency alone (EP-0112, EP-0113, EP-0116)

Rerun package for the Open Research Lab note
*Which ciphers can K4's cribs refute without searching any key?*

```sh
python verify_consistency.py    # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_consistency.py` | K4 and its public cribs; the shift-by-occurrence-count check, the homophone collision count, the self-encryptions, and free Vigenère/Beaufort/variant switching with a periodic key, with shuffled-ciphertext nulls |
| `results/consistency-20260927.json` | Recorded results, including the outcomes of searches that are not rerun here |
| `verify_consistency.py` | Recomputes everything above and prints `PASS` |
| `make_figure.py` | The Note's figure |

Everything rerun here uses only K4 and its public cribs. It is a rerun of the author's code,
not an independent replication.

## Not rerun here

- EP-0113 stage 1 (keys fixed at every position, including running keys over the K1–K3 texts
  and Carter & Mace) reads texts this site does not publish.
- EP-0116: the Portax and Doppelkasten solvers (exact backtracking over free squares and
  substitutions, hours of computation). Their outcomes are listed in `results/`.

The internal shift-by-count check used every successive-occurrence constraint; the check here
uses only the requirement that the step map be one-to-one, so it fails on 80% of shuffles
rather than the 86.5% recorded internally. Both fail on K4.
