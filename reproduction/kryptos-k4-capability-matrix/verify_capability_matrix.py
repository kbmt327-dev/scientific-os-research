"""Recompute the coverage views of the capability-matrix Note (EP-0142) from the recorded rows
and compare with the summary.

    python verify_capability_matrix.py

Standard library only, under a second.  No K4 data is read and no K4 test is run: the rows are
the author's transcription of which capabilities each recorded test covered.  A rerun of the
author's code, not an independent replication.
"""
import json
import sys
from math import isclose
from pathlib import Path

import k4_capability_matrix as M

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "capability-matrix-summary-20260928.json").read_text(encoding="utf-8"))
    bad = []
    rs = M.rows()
    print(f"  rows: {len(rs)}")
    if len(rs) != rec["rows"] or len({d['id'] for d in rs}) != len(rs):
        bad.append("rows")
    cov, part = M.cube(rs)
    for u in M.UNITS:
        print(f"  unit {M.EN[u]}:")
        for s in M.STATES:
            cells = ["closed" if cov.get((u, s, y)) else ("touched" if part.get((u, s, y)) else "EMPTY")
                     for y in M.SYNCS]
            print(f"    {M.EN[s]:<19} " + "  ".join(f"{M.EN[y]}={c}" for y, c in zip(M.SYNCS, cells)))
    empty = [[s, y] for s in M.STATES for y in M.SYNCS if not cov.get(("文字", s, y))]
    if empty != rec["empty_letter_cells"]:
        bad.append("letter cells")
    blk = sum(1 for s in ("平文履歴", "暗号文履歴", "外の状態") for y in M.SYNCS if cov.get(("塊", s, y)))
    if blk != rec["block_history_states_closed"]:
        bad.append("block cells")
    for col in ("chrono", "origin"):
        t = dict(M.tallies(rs, col))
        print(f"  {col}: {t}")
        if t != rec["chronology" if col == "chrono" else "origin"]:
            bad.append(col)
    p = M.two_slips_inside_both_cribs()
    print(f"  two random slips falling one inside each crib: {p:.3f}")
    if not isclose(p, rec["two_slips_inside_both_cribs"], abs_tol=0.0005):
        bad.append("two slips")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: the covered region and the empty letter cells reproduce from the recorded rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
