# Kryptos K4: keys that follow the plaintext (EP-0150, EP-0179)

Check package for the Open Research Lab note
*Do keys that follow the plaintext fit K4's cribs?*

```sh
python verify_plaintext_keys.py          # standard library only, under a minute
python verify_plaintext_keys.py --full   # 10,000 autokey shuffles and every possible set V, a few minutes
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_plaintext_keys.py` | Plaintext autokey with lag L (chain propagation along residue classes, no primer search); the plaintext-indexed periodic key (shift tables and arbitrary rows); planted ciphers |
| `results/plaintext-keys-20260930.json` | The author's recorded results: all 240 autokey cells with their shuffle P, the 14 shift-table passes, the arbitrary-row counts, shuffle nulls and controls; and the every-V check added while writing the Note |
| `verify_plaintext_keys.py` | Recomputes every autokey cell and compares cell by cell, 24 planted controls and a shuffle null; recomputes the shift-table and arbitrary-row tests on the 32 sets V that need no other text, 40 planted controls and a shuffle null; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The record's 60 sets V include 28 letter sets taken from another part of the sculpture (14 words and their
complements). That text is not published here, so the default check uses the other 32 sets; `--full` instead
tests every possible V (inside the cribs only V's intersection with 12 crib letters matters, so 4,096 classes
cover all sets). The record's 1,000-shuffle null for the 60 sets is recorded. Planted texts here use random
letters with the cribs written in. A rerun of the author's method, not an independent replication.
