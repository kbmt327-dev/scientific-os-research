# Kryptos K4 fixed row lists

This package covers EP-0196, EP-0197, EP-0198, and EP-0208. The recorded family contains 12 fixed lists with 662 rows total. Eight lists (336 rows) are included in the public subset.

The existing verifier reruns the K4 crib checks for EP-0196, EP-0197, and EP-0208 on those eight published lists and checks arithmetic derived from list sizes and stored summaries. It does not rerun the withheld lists, EP-0198, null generation, planted controls, or the recorded index-of-coincidence analyses. The source record gives a selection-free cover bound of at least 3 mismatches across the registered 12-list family; that bounded statement does not imply that other lists or methods fail. The verifier also found an EP-0208 prose discrepancy: 11 qualifying list-period pairs are stated, while the input sizes yield 9; the recorded excluded-setting count agrees with 9.

Run from this directory with: python -B verify_fixed_row_lists.py

A passing check is an author-code partial reproduction, not an independent replication. It emits aggregate checks only. Four source-derived lists are omitted from this public subset; the omitted source-derived rows are not included.