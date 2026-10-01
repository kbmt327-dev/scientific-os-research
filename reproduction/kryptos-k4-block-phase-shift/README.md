# Kryptos K4: one phase shift in the grouping of block ciphers (EP-0169, with EP-0177, EP-0184, EP-0178)

Check package for the Open Research Lab note
*Does one phase shift in the grouping reopen the square and Bifid ciphers?*

```sh
python verify_block_phase_shift.py   # standard library only, about ten seconds
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_block_phase_shift.py` | K4 without its Ws (92 letters), the shift settings for digraphs (b, phi0) and for Bifid blocks (p, a0, b), and the exact tests: free Four-square, the fixed digraph chart C08, and the coordinate solver for one-square Bifid and CM-Bifid |
| `results/block-phase-shift-20260930.json` | The author's recorded results, including Two-square, keyword squares, the shuffle nulls, the post hoc CM-Bifid count null, the follow-ups and the procedure notes |
| `verify_block_phase_shift.py` | Recomputes the setting counts, free Four-square on K4 with the author's 500-shuffle null (same seed), C08 on 97 and 92 letters, one-square Bifid and CM-Bifid on K4, and planted controls; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

Free Two-square (a separate exact solver), keyword squares (an English word list, 7.15 million
settings), the C08 nulls (2,000 shuffles each), the Bifid and CM-Bifid shuffle nulls (the CM-Bifid
count null takes several minutes per shuffle) and the follow-ups EP-0177 and EP-0184 (they use
fragment lists and candidate sets built from text sources; the lists are not published) and the
scorer of EP-0178 (an English 4-gram table). They are recorded, not rerun. The planted controls
here use random letters with the cribs written in; the author's controls used English text.
A rerun of the author's code, not an independent replication.
