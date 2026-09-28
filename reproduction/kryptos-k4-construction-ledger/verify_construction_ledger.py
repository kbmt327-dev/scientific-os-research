"""Rerun the row and column operators of EP-0140 from K4's coordinates on the panel and compare
with the record.

    python verify_construction_ledger.py

Standard library only, about a second.  Draws random numbers in the same order as the author's
run, so the shuffle fractions match exactly.  The fold operators (G1-G3) need carved text this
site does not publish and are recorded only.  A rerun of the author's code, not an
independent replication.
"""
import json
import sys
from math import isclose
from pathlib import Path

import k4_layout_ledger as L

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "construction-ledger-20260928.json").read_text(encoding="utf-8"))
    bad = []
    got = L.run(rec["shuffles"], rec["seed"])
    for name, r in got.items():
        want = rec["operators"][name]
        conf = r["first_conflict"]
        extra = (f"; first conflict {conf[0]} {L.CRIB[conf[0]]}->{L.K4[conf[0]]} and {conf[1]} "
                 f"{L.CRIB[conf[1]]}->{L.K4[conf[1]]} in the same class") if conf else ""
        print(f"  {name}: within-class crib pairs {r['within_class_crib_pairs']}, K4 "
              f"{'consistent' if r['consistent'] else 'inconsistent'}{extra}")
        print(f"    shuffles consistent {r['null_consistent_fraction']:.5f}, plants {r['plants_consistent']}")
        if any(r[k] != want[k] for k in r):
            bad.append(name)
    stop = [f["id"] for f in rec["ledger"] if f["fixes_operator"].startswith("STOP")]
    print(f"  ledger: {len(rec['ledger'])} facts, STOP for {len(stop)} ({', '.join(stop)})")
    ch = L.last_rows_all_31()
    print(f"  chance that the last four of 28 rows are all 31 when 15 are: {ch:.3f}")
    if not isclose(ch, rec["last_four_rows_all_31_chance"], abs_tol=0.0005):
        bad.append("row chance")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: a table per carved row fails at the first crib; a table per column fits, as do 93% of shuffles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
