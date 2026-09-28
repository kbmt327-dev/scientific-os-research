# Kryptos K4: letters reordered inside each word (EP-0137)

Check package for the Open Research Lab note
*Does reordering the letters inside each word, before or after the substitution, open a procedure that fits K4?*

```sh
python verify_word_reordering.py   # standard library only, under a second
python make_figure.py out.svg      # redraws the Note's figure
```

| File | What it does |
|---|---|
| `k4_word_reordering.py` | The three segmentations of the cribs into words, the 8 fixed reordering rules, the count of within-word orders, the word-restart (J03) conflict count and the near-key count |
| `results/word-reordering-20260928.json` | The author's recorded counts and the outcome of every run (K4, two shuffles, planted controls) |
| `verify_word_reordering.py` | Recomputes the orders and their bits (S1 37.5, S2 31.5, S3 50.2), the capacity against the crib, the 21 distinct fixed-rule crib assignments and their chance value (1.1 × 10⁻¹⁷), the word-restart conflicts and the near keys; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The search runs every EP-0119 procedure on the reordered cribs (on a GPU, 3–8 minutes per
run). Those procedures are built partly from the K1–K3 texts and the carved tableau, which
this site does not publish, so the search is not part of this package. The package checks
the counts and the crib-only arguments. It is not an independent replication.

## Result

- Reorder then substitute (J01) and substitute then reorder (J01'): 0 procedures fit K4 under
  every segmentation, for the fixed rules and for any order inside the words; two shuffles 0;
  planted controls 76/76.
- Logical refutation only: the chance of a false pass is at most 7 × 10⁻⁶, so random
  ciphertexts give 0 too.
