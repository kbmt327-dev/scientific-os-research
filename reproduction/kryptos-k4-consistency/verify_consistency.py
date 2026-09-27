"""Recompute the K4-only consistency checks (EP-0112, EP-0113, EP-0116) and compare with the record.

    python verify_consistency.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_consistency as K

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "consistency-20260927.json").read_text(encoding="utf-8"))
    fails = []

    def check(name, got, want):
        ok = got == want
        print(f"  {name:<52} {got}  {'ok' if ok else 'MISMATCH'}")
        if not ok:
            fails.append(name)

    check("successive occurrences inside the cribs", [list(x) for x in K.successive_occurrences()],
          rec["successive_occurrences"])
    check("shift-by-count: conflicting steps", K.occurrence_shift_conflicts(K.K4), rec["occurrence_shift_conflicts"])
    check("shift-by-count: share of shuffles failing too", K.occurrence_null(2000),
          rec["occurrence_shift_null_share_failing"])
    check("ciphertext letters from two plaintext letters", K.homophone_collisions(K.K4), rec["homophone_collisions"])
    check("self-encryptions", [list(x) for x in K.self_encryptions(K.K4)], rec["self_encryptions"])
    sw = rec["switching_feasible_periods"]
    check("switching, feasible periods (A-Z)", K.switching_feasible_periods(K.K4, K.AZ)[0], sw["AZ"])
    check("switching, feasible periods (KRYPTOS)", K.switching_feasible_periods(K.K4, K.KA)[0], sw["KRYPTOS"])
    null = rec["switching_shuffle_null"]
    got = K.shuffle_null(null["n"])
    check("switching, shuffles: pass p <= 24 / fail every p", list(got),
          [null["share_passing_some_constrained_p_le_24"], null["share_failing_every_constrained_p"]])
    rates = K.per_period_shuffle_rates(null["n"])
    check("switching, shuffles: per-period feasibility", {str(p): r for p, r in rates.items()}, null["per_period_share"])
    if fails:
        print("FAIL:", ", ".join(fails))
        return 1
    print("PASS: occurrence-count, homophone, self-encryption and switching checks reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
