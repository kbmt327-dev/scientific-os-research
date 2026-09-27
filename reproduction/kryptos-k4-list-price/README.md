# Kryptos K4: the TOKIO reading once the choice of target list is paid (EP-0135)

Rerun package for the Open Research Lab note
*What is the TOKIO reading worth once the choice of target list is paid?*

```sh
python verify_list_price.py     # standard library only, a few seconds
python make_figure.py out.svg   # redraws the Note's figure from results/
```

`verify_list_price.py` prints `PASS` when every check matches the recorded result. This is a
rerun of the author's code, not an independent replication.

| File | What it does |
|---|---|
| `k4_list_price.py` | K4 ciphertext, the W-gap reading family generalised to a text of length n, the closed-form count of position sets, expected hits per word list |
| `data/target-lists-public.json` | Five of the six target lists frozen before any gap was read, and the SHA-256 of the frozen file that also holds the sixth |
| `results/list-price-20260927.json` | The author's recorded results (Q1 per list and union, Q4 totals, Q2 counts) |
| `verify_list_price.py` | Brute-force check of the closed form; recomputes the five public lists; brackets the recorded union; checks that K4 yields only `TOKIO` |
| `make_figure.py` | The Note's figure |

## What is withheld

The sixth list (107 distinct words of the K1–K3 plaintexts) and the marker texts of Q4
(the carved panel, the tableau, the K1–K3 plaintexts) are not published, because this site
does not publish the sculpture's text beyond K4. The verifier therefore checks that the
recorded union (0.0539) lies between the union of the public lists (0.0343) and that value
plus the withheld list's own price (0.0205).

The Q2 runs (the procedure enumerator on the 92 non-W letters, ciphertext autokey,
Chaocipher and the walking cursor with the five W letters unknown) are recorded in
`results/` but are not rerun here: they need the enumerator's full code and about 30 minutes
of parallel computation.

## Result

- K4's reading family against the union of the six lists: E = 0.054; the World Clock share is 3.7%.
- Every marker in K1–K4, cipher side: 1 hit (`TOKIO`) against 0.211 expected, p = 0.19.
- Ws as inserted or overwritten marks: 0 in every family, controls all found.
