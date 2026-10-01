# Kryptos K4: Portax with a free substitution, and a free-square Playfair followed by a mask (EP-0156)

Check package for the Open Research Lab note
*Portax with a free substitution, and Playfair with a free square followed by a shift mask*

```sh
python verify_portax_playfair_mask.py   # standard library only, about 10 s
python make_figure.py out.svg
```

| File | What it does |
|---|---|
| `k4_portax.py` | The Portax table (ACA rules), the vertical pairs for a period P, and an exact backtracking decider for C = Portax(sigma(P)) on the crib |
| `results/portax-playfair-mask-20260930.json` | The author's recorded results: CP-SAT outcomes for both Portax layers at P = 1..48 with shuffles and plants, and for the free-square Playfair followed by masks m1-m4 with controls |
| `verify_portax_playfair_mask.py` | Recomputes the ACA worked example, the reciprocity and no-fixed-letter facts, the crib pairs at every period, the 'before' layer on K4 at every period (with 960 planted texts and 960 shuffles), and the W-reduced text, crib pairs and m1 / m2 setting counts of the Playfair part; checks the record; prints `PASS` |
| `make_figure.py` | The Note's figure |

## What is not rerun here

The 'after' layer (C = tau(Portax(P))) and the free-square Playfair with masks are exact proofs from a constraint
solver (OR-tools CP-SAT), up to 600 s and 120 s per problem; m3 uses a keyword list from an earlier Note and m4
uses the K1-K3 plaintext as a running key, which this site does not publish. They are recorded, not rerun here.
The stdlib decider for the 'before' layer is a second implementation of the same constraint set; a few shuffled
texts exceed its node budget and are reported as such. Planted texts here use random letters with the cribs
written in (the record used English). A rerun of the author's method, not an independent replication.
