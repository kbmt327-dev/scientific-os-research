"""Recompute the selection-free cover of three public row lists (EP-0114) and compare with the record.

    python verify_chosen_rows.py

Standard library only, about 10 seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_chosen_rows as C

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "chosen-rows-20260927.json").read_text(encoding="utf-8"))["cover"]
    wc = json.loads((HERE / "data" / "worldclock-places.json").read_text(encoding="utf-8"))["letters"]
    lists = dict(C.LISTS, worldclock=[w for w in wc if w])
    bad = []
    for name, words in lists.items():
        rows = C.rows_of(words)
        c = C.cover_all(rows, C.K4)
        got = {"rows": len(rows), "cover_m1_m4": [c[k] for k in ("m1", "m2", "m3", "m4")],
               "best_cover": max(c.values()), "best_convention": max(c, key=c.get), "null": C.null_share(rows, 200)}
        print(f"  {name:<10} {got['rows']:>3} rows: at most {got['best_cover']}/24 crib letters explainable by any "
              f"row ({got['best_convention']}); shuffles reach as many in {got['null']['share_ge_k4']:.0%}")
        if got != rec[name]:
            bad.append(name)
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: no rule for choosing rows from these lists can produce the crib")
    return 0


if __name__ == "__main__":
    sys.exit(main())
