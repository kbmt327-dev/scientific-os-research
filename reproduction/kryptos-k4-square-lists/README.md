# Kryptos K4 square-list families

This package publishes a compact aggregate projection for EP-0193 T1, EP-0199, EP-0200, EP-0201, EP-0205, and EP-0228. The source records report zero exact or registered passes in the stated finite families. Their minima and null summaries are shown in results/square-lists-20261011.json.

The null shares are descriptive fractions from the recorded finite samples. They are not independent p-values. Sample sizes vary, including 10 and 20 draws for several families. EP-0193 T1 is source-record-only because its package scan is not present. The source scans for the other episodes are also not rerun by this lightweight public check.

Run from this directory with: python -B verify_square_lists.py

The check rebuilds public inventory counts from the package code and verifies histogram totals and shares. It does not enumerate candidate squares against K4 or regenerate nulls. A pass validates this projection only; it is not an independent replication. No decoded text or grid data is included.