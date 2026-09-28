# Kryptos K4: the procedure enumerator (EP-0119, 0127, 0131, 0134, 0136)

Check package for the Open Research Lab note
*Does any fully specified procedure built from a grammar of parts fit K4?*

```sh
python verify_enumerator_counts.py   # standard library only, under a second
python make_figure.py out.svg        # redraws the Note's figure from results/
```

| File | What it does |
|---|---|
| `results/enumerator-20260927.json` | The author's recorded counts: selector families, tables and procedures per shape, and the outcome of every run (K4, two shuffles, planted controls) |
| `verify_enumerator_counts.py` | Recomputes the total, its log2, the description length with the shape choice, the closed-form expected false passes (whole crib, up to two, three, four, seven and eight crib errors, each crib alone), the coverage of scattered hand alterations and the split into different-method and K1–K3-variant parts |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The enumerator builds selectors and chart rows from the K1–K3 ciphertexts and plaintexts,
the carved tableau and the text of Carter & Mace (1923). This site does not publish the
sculpture's text beyond K4, so the search is not part of this package; a full run also
takes about 33 minutes (and the stacked-mask stage a GPU). The package checks the
arithmetic that turns the recorded counts into the Note's claims. It is not a rerun of the
search and not an independent replication.

## Result

- 4.7 × 10¹⁵ procedures (log2 52.1; 99.9% different-method shapes): 0 fit K4; two shuffles 0; planted controls 18/18.
- Expected chance passes: 5 × 10⁻¹⁹ for the whole crib, 9 × 10⁻¹⁴ and 1.6 × 10⁻¹¹ with up to two or three crib errors, 2.2 × 10⁻⁹, 1.1 × 10⁻³ and 0.059 with up to four, seven and eight (EP-0136, all 0 hits), 0.0019 for crib 1 alone.
- Seven crib errors cover 20 scattered alterations with probability 0.93, 28 with 0.62, 35 with 0.29.
