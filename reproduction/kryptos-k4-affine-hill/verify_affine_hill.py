"""Recompute the position-varying affine and periodic 2x2 Hill tests (EP-0117) and compare with the record.

    python verify_affine_hill.py

Standard library only, about 40 seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_affine_hill as H

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "affine-hill-20260927.json").read_text(encoding="utf-8"))
    af, hl = rec["affine"], rec["hill_2x2_no_vector"]
    got_af = {"a_polys_invertible_everywhere": len(H.A_POLYS),
              "K4_fits": {f"{n}/{d}": len(H.affine_fits(H.K4, a, d))
                          for n, a in (("A-Z", H.AZ), ("KRYPTOS", H.KA)) for d in ("enc", "dec")},
              "planted_found": H.affine_controls(af["planted"]), "planted": af["planted"],
              "shuffles_with_a_fit": H.affine_shuffles(af["shuffles"]), "shuffles": af["shuffles"]}
    counts = H.hill_shuffle_consistent(hl["shuffles"])
    got_hl = {"settings": len(H.hill_settings()),
              "K4_consistent": [[n, o, p] for n, a, o, p in H.hill_settings() if H.hill_consistent(H.K4, a, o, p)],
              "planted_consistent": H.hill_controls(hl["planted"]), "planted": hl["planted"],
              "shuffles": hl["shuffles"], "max_shuffles_consistent_per_setting": max(counts.values())}
    print(f"  affine: {got_af['a_polys_invertible_everywhere']} multiplier polynomials; K4 fits {got_af['K4_fits']}; "
          f"plants {got_af['planted_found']}/{af['planted']}; shuffles with a fit {got_af['shuffles_with_a_fit']}")
    print(f"  Hill 2x2: K4 consistent in {len(got_hl['K4_consistent'])} of {got_hl['settings']} settings; plants "
          f"{got_hl['planted_consistent']}/{hl['planted']}; at most {got_hl['max_shuffles_consistent_per_setting']} "
          f"of {hl['shuffles']} shuffles consistent per setting")
    bad = [k for k in got_af if got_af[k] != af[k]] + [k for k in got_hl if got_hl[k] != hl[k]]
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: position-varying affine and periodic 2x2 Hill tests reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
