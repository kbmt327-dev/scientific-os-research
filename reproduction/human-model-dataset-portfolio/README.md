# Human Model dataset portfolio reproduction

This bounded package checks the public EP-0005 dataset decision: distinct development, external-validation, and internal-load roles; the frozen Carter participant split; source and archive-index hashes; leakage guards; and the list of work that has not been performed.

~~~bash
python scripts/reproduce.py --quick human-dataset
~~~

Or from this directory:

~~~bash
python tests/validate_dataset_portfolio.py
~~~

Expected: `human_dataset_portfolio: PASS` with 30 development, 10 validation, and 10 test participants.

## Boundary

The check is an internal-consistency reproduction over the published manifest. It does not download Carter, OpenCap, Knee Grand Challenge, AMASS, or HuMoD; inspect B3D numerical frames; fit a model; select performance thresholds; or evaluate any holdout. It is not an independent replication.
