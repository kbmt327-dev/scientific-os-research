"""Recompute the shape-free physical-key tests (EP-0066, EP-0068) and compare with the record.

    python verify_physical_keys.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import statistics as st
import sys
from pathlib import Path

import k4_physical_keys as P

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "physical-keys-20260927.json").read_text(encoding="utf-8"))
    bad = []
    cols = {"32": list(P.place(32)), "63": list(P.place(63)), "33": list(P.place(33)), "64": list(P.place(64))}
    if cols != rec["shared_columns"]:
        bad.append("layout")
    table = P.column_table()
    for name, row in table.items():
        print(f"  {name:<18} k(32), k(63), k(33), k(64) = {row['k32_k63_k33_k64']}: horizontal-only "
              f"{'fits' if row['horizontal_only'] else 'fails'}, horizontal + vertical "
              f"{'fits' if row['horizontal_plus_vertical'] else 'fails'}")
    if table != rec["column_table"]:
        bad.append("column table")
    r = P.random_roughness(rec["roughness"]["random_n"])
    got = {"K4": P.roughness(P.K4), "random_n": len(r), "random_median": st.median(r),
           "random_share_le_9": sum(x <= 9 for x in r) / len(r), "random_share_le_10": sum(x <= 10 for x in r) / len(r)}
    print(f"  roughness S: K4 {got['K4']}; random crib keys median {got['random_median']}, "
          f"P(S <= 9) {got['random_share_le_9']:.3f}, P(S <= 10) {got['random_share_le_10']:.3f}")
    if got != rec["roughness"]:
        bad.append("roughness")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: height-free and additive physical keys fail in all 6 conventions; K4's crib keys are as rough as random")
    return 0


if __name__ == "__main__":
    sys.exit(main())
