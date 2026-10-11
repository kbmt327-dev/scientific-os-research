# Kryptos K4: two-stage and errors

Public projection of recorded results from EP-0227, EP-0236, EP-0238, EP-0240, and EP-0241. The aggregate contains counts, thresholds, histograms, and disclosure flags; it contains no plaintext.

From the repository root, run:

    python reproduction/kryptos-k4-two-stage-and-errors/verify_two_stage_and_errors.py

The verifier reads only the packaged aggregate JSON. It checks histogram totals, sample fractions, registered-pass counts, and scope boundaries. It does not rerun candidate searches, generate null samples, or validate every source row. EP-0240 rank numerators are integer equivalents of the recorded aggregate fractions; the check confirms their arithmetic.

P denotes the observed fraction of a recorded null sample at or below the specified K4 threshold, not a confirmatory p-value. EP-0236 and EP-0241 disclose pre-registration K4 exposure and resulting family or metric/subset selection. EP-0241 r27 nulls cover only 26 registered settings (1% of q1). No full-q1 null evaluation is complete, and the full-q1 K4 search is also incomplete. EP-0240 B/C fractions are undefined because the K4 minimum h is unavailable.

This is an author-maintained aggregate consistency check, not an independent replication. Only Python's standard library is required.
