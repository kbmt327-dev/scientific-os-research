"""Recompute the fewest crib errors a periodic key needs (EP-0071), for K4 and 100 shuffles.

    python verify_carving_errors.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_carving_errors as E

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "carving-errors-20260927.json").read_text(encoding="utf-8"))["periodic_min_errors"]
    t = E.table(range(1, 49), rec["shuffles"])
    got = {str(p): {"K4": v["K4"], "shuffle_min": v["shuffles"][0], "shuffle_median": v["shuffles"][50],
                    "shuffle_max": v["shuffles"][-1]} for p, v in t.items()}
    closed5 = [int(p) for p, v in got.items() if v["K4"] > 5]
    print(f"  periods that still need more than 5 crib errors: {closed5}")
    far = [p for p, v in got.items() if v["K4"] < v["shuffle_min"]]
    print(f"  periods where K4 needs fewer errors than all {rec['shuffles']} shuffles: {far or 'none'} "
          f"(one of 48 periods; expected about 0.5 by chance)")
    if got != rec["by_period"]:
        print("FAIL: periodic minimum errors differ from the record")
        return 1
    print("PASS: fewest crib errors for periodic keys reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
