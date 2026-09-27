"""Recompute the K4-only square checks (EP-0110, EP-0125) and compare with the record.

    python verify_w_squares.py

Standard library only, about a second.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_w_squares as S

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "w-squares-20260927.json").read_text(encoding="utf-8"))
    fails = []

    def check(name, got, want):
        ok = got == want
        print(f"  {name:<58} {'ok' if ok else 'MISMATCH'}")
        if not ok:
            fails.append(name)

    check("92 letters after removing W", len(S.RED), rec["reduced_length"])
    for m in S.PAIR_MODES:
        fs = rec["foursquare_free"][m]
        check(f"free Four-square inconsistent, pairing {m}", S.foursquare_consistent(S.RED, S.square(), m),
              fs["standard_plain"])
        check(f"  with keyword plain squares, pairing {m}",
              sum(S.foursquare_consistent(S.RED, S.square(w), m) for w in S.KEYWORDS), fs["keyword_plain_consistent"])
        std, swp = S.twosquare_witnesses(m)
        check(f"Two-square witnesses, pairing {m}", {"standard": [list(x) for x in std],
                                                     "swapped": [list(x) for x in swp]},
              rec["twosquare_witnesses"][m])
        check(f"doubled ciphertext pairs, pairing {m}", [list(x) for x in S.doubled_ciphertext_pairs(m)],
              rec["doubled_ciphertext_pairs"][m])
    check("Four-square planted controls consistent", S.planted_controls(200), rec["foursquare_plants_consistent"])
    check("Four-square shuffles consistent", S.shuffle_null(2000), rec["foursquare_shuffle_consistent_share"])
    if fails:
        print("FAIL:", ", ".join(fails))
        return 1
    print("PASS: free Four-square, Two-square witnesses and doubled pairs reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
