# Free-square mask audits

This package projects the recorded outcomes for EP-0195, EP-0204, EP-0212, EP-0213, EP-0223, EP-0224, EP-0229, and EP-0235. The public inputs are the K4 ciphertext, the 24 public crib letters, and the existing free-square mask implementation.

Run the bounded verifier from the repository root:

    python reproduction/kryptos-k4-free-squares-masks/verify_free_squares_masks.py

The verifier checks public input dimensions and the recorded result projection. It does not rerun the registered searches or shuffle nulls. See results.json for the finite scopes and retained compatible outcomes. In particular, EP-0213's two-square logic-only column retains 24 compatible labels in 12 classes, EP-0224 records zero registered K4 passes and zero UNKNOWN across four PH and six SPF columns, and EP-0229 refutes one of four surviving non-bijective classes while three remain compatible.

EP-0224 follow-up source: KRYPTOS-K4/EP-0224, SHA-256 `f91c1f43e6ffaaab900d71fbc37a0040f1763513d46174f3afac47f3c3274099`.

For EP-0224, PH-main nulls use the h≤1 cutoff: h=1 occurred 0/200 in PH1-main and 1/200 in PH2-main. PH-sensitivity nulls use the h=0 cutoff only; h=1 was not evaluated. Reported P=1.0 values are PH-main P0/P1, PH-sensitivity P0, and SPF P0. The PH-main capacity-E values are approximate combined totals across both main columns; see results.json for values and assumptions.

No K4 plaintext is published. New plaintext characters: 0. Independent replications: 0. The registered finite outcomes do not exclude free-square models outside the tested settings or decision rules.
