# Two-stage fractionation audits

This package projects EP-0202, EP-0219, EP-0220, EP-0221, EP-0222, and EP-0239. The recorded outcomes cover finite, specified two-stage compositions and parameter sets. EP-0222 tested only its preregistered fixed bank of 16 squares: its two decisionable columns had no pass, while R3-3 stopped after a failed specificity control and was not run.

Run from the repository root:

    python reproduction/kryptos-k4-two-stage-fractionation/verify_two_stage_fractionation.py

The bounded verifier checks public input dimensions and the recorded scope boundaries. It does not rerun the large searches or nulls. No statement here closes the full 2,622-square bank or every two-stage composition.

No K4 plaintext is published. New plaintext characters: 0. Independent replications: 0.