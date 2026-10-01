"""Recompute the fold crossings of chart #3 and the restart test of EP-0167, and compare with the record.

    python verify_chart3_folds.py

What is rerun: the K4 positions and the number of K3 cells on the fold columns (cell geometry only), the
same-phase crib pairs, the key disagreements under six shift-table conventions, the conflicts for arbitrary
rows, and the 100,000-shuffle null in the author's random order (about 15 seconds).  Added for this Note: the
share of shuffles that, like K4, disagree at every same-phase pair (20,000 shuffles, seed 1).
The inventory of the chart image, the 2025 materials and the NOVA stills are records, not rerun here.
Standard library only.  A rerun of the author's code, not an independent replication.
"""
import json
import random
import sys
from pathlib import Path

import k4_chart3_folds as F

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "chart3-folds-20260930.json").read_text(encoding="utf-8"))
    bad = []
    k4, k3 = F.fold_crossings()
    print(f"  fold columns {F.FOLD_COLUMNS}: K4 positions {k4}, K3 cells {k3}")
    if k4 != rec["chart3_image"]["k4_positions_crossed"] or k3 != rec["chart3_image"]["k3_cells_crossed"]:
        bad.append("crossings")
    got = F.run()
    for name, r in got.items():
        want = rec["restart_test"][name]
        fd = set(r["fixed_disagreements"].values())
        print(f"  {name}: same-phase pairs {r['same_phase_groups']}")
        print(f"    shift table: disagreements {sorted(fd)} in all 6 conventions (shuffles <= K4: {r['fixed_shuffles_le']})")
        print(f"    arbitrary rows: conflicts {r['rows_conflicts']} (shuffles <= K4: {r['rows_shuffles_le']})")
        if (r["same_phase_groups"] != want["same_phase_groups"] or fd != {want["fixed_disagreements_every_convention"]}
                or r["fixed_shuffles_le"] != want["fixed_shuffles_le"] or r["rows_conflicts"] != want["rows_conflicts"]
                or r["rows_shuffles_le"] != want["rows_shuffles_le"]):
            bad.append(name)
        if fd != {len(r["same_phase_groups"])}:
            bad.append(name + ": not every pair disagrees")
    rng = random.Random(1)
    for name, cols in F.CASES.items():
        G = F.groups(F.segment_starts(cols))
        full = 0
        for _ in range(20000):
            s = list(F.K4)
            rng.shuffle(s)
            full += min(F.fixed_fail("".join(s), G).values()) == len(G)
        print(f"  {name}: shuffles that also disagree at every pair under the best convention {full / 20000:.3f}")
        if full == 0:
            bad.append("shuffle share")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: K4 disagrees at every same-phase crib pair under a shift table; arbitrary rows stay undecidable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
