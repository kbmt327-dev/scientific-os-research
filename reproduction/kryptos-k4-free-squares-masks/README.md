# Free-square mask audits

This package projects the recorded outcomes for EP-0195, EP-0204, EP-0212, EP-0213, EP-0223, EP-0229, and EP-0235. The public inputs are the K4 ciphertext, the 24 public crib letters, and the existing free-square mask implementation.

Run the bounded verifier from the repository root:

    python reproduction/kryptos-k4-free-squares-masks/verify_free_squares_masks.py

The verifier checks public input dimensions and the recorded result projection. It does not rerun the registered searches or shuffle nulls. See results.json for the finite scopes and retained compatible outcomes. In particular, EP-0213's two-square logic-only column retains 24 compatible labels in 12 classes, and EP-0229 refutes one of four surviving non-bijective classes while three remain compatible.

No K4 plaintext is published. New plaintext characters: 0. Independent replications: 0. The registered finite outcomes do not exclude free-square models outside the tested settings or decision rules.