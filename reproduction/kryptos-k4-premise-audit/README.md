# Kryptos K4 premise audit

This package publishes a bounded projection of the premise and audit records for EP-0188, EP-0189, EP-0190, EP-0191, EP-0192, and EP-0194. It is an audit of how assumptions, classifications, and finite search records were documented; it is not a K4 solution or an independent cryptanalysis.

The public projection reports aggregate counts only. It records 100 ledger rows across 20 premises; 14 double-coded rows had mean Jaccard agreement 0.80. A later coding record contains 72 rows while its cited summary says 73. It also records a multiplier of 172501 where the displayed rule recomputes to 173101, a difference of 600. These discrepancies remain visible rather than being silently repaired.

The source record reports zero exact hits in five named finite groups in EP-0190 and all six finite groups in EP-0192. That is limited to those recorded families. EP-0194 leaves one subfamily UNKNOWN. These figures do not establish that other methods fail, and they do not establish that the source records have been independently reproduced.

Run the lightweight metadata check from this directory with: python -B verify_premise_audit.py

The check validates only the public aggregate projection and arithmetic. It does not rerun any cipher search. No plaintext, crib strings, ciphertext, local paths, or personal information are included.