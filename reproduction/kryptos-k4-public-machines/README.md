# Kryptos K4 public machine families

This package gathers bounded machine-family records from EP-0193 T2, EP-0203, EP-0206, EP-0207, EP-0209, and EP-0215. The source records include finite negative results: zero registered exact passes for the stated settings in EP-0193 T2, EP-0203, EP-0206, EP-0209, and EP-0215. EP-0206 also records looser h<=12 clusters, and EP-0207 has a post-hoc sensitivity observation that was not confirmed (recorded p=0.415). These findings apply only to the stated finite families.

Run from this directory with: python -B verify_public_machines.py

The lightweight verifier checks machine test vectors, wiring/stepping invariants, entry readings, small planted/K4 slices, and setting-count/chance arithmetic. The full CPU/GPU sweeps, null generation, and confirmation statistic remain source-record results and are not rerun here. A pass is an author-code partial reproduction, not an independent replication. The package publishes aggregate counts and statistics; it contains no K4 plaintext or planted text.