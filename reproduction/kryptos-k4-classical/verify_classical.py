"""Recompute the keystream closures (EP-0032) and the letter-count argument, and compare with the record.

    python verify_classical.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_classical as C

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "classical-20260927.json").read_text(encoding="utf-8"))
    bad = []
    tp = C.testable_periods()
    print(f"  periods 1-96 that the crib can test: {len(tp)} (untestable: 27-29 and 53-96)")
    if tp != rec["testable_periods"]:
        bad.append("testable periods")
    for name, want in rec["settings"].items():
        a, f = name.split(" ")
        al = C.ALPHABETS[a]
        k = C.keystream(al, f)
        got = {"keystream": list(C.keystream_text(al, f)), "periodic_survivors": C.periodic_survivors(k),
               "difference_survivors": C.difference_survivors(k),
               "english_running_key_share": C.english_running_key_p(k, al, 20000)}
        print(f"  {name:<16} keystream {got['keystream'][0]} | {got['keystream'][1]}; periodic survivors "
              f"{got['periodic_survivors'] or 'none'}; English-key share {got['english_running_key_share']}")
        if got != want:
            bad.append(name)
    t = C.transposition_p(20000)
    print(f"  English samples as flat as K4 (a transposition keeps the counts): {t}")
    if t != rec["transposition_share_as_flat_as_k4"] or len(set(C.K4)) != rec["k4_distinct_letters"]:
        bad.append("letter counts")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: every testable period fails in all 8 settings; keystream table and letter-count test reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
