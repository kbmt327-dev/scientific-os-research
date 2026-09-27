"""Recompute the free-wiring single-rotor test (EP-0083) and compare with the record.

    python verify_rotor.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_rotor as R

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "rotors-20260927.json").read_text(encoding="utf-8"))["single_rotor_free_wiring"]
    got = {"K4_passing": R.passing_settings(R.K4), "planted_found": R.planted_controls(rec["planted"]),
           "shuffles_with_a_pass": R.shuffle_null(rec["shuffles"])}
    print(f"  K4 settings with a consistent wiring: {got['K4_passing']}")
    print(f"  planted rotors found: {got['planted_found']}/{rec['planted']}")
    print(f"  shuffles with any consistent setting: {got['shuffles_with_a_pass']}/{rec['shuffles']}")
    bad = [k for k in got if got[k] != rec[k]]
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: no free wiring fits K4 for any step or numbering; planted rotors all found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
