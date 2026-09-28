"""Recompute the counts and crib checks of the word-reordering Note (EP-0137) and compare with
the record.

    python verify_word_reordering.py

The search itself runs the EP-0119 enumerator, which reads text this site does not publish,
so it is not rerun here.  What is rerun: the number of within-word orders for each
segmentation and its bits, the capacity against the crib, the 21 distinct crib assignments of
the 8 fixed rules, the closed-form chance for the fixed rules, the word-restart (J03) conflict
counts and the near-key counts.  Standard library only, well under a second.  A rerun of the
author's code, not an independent replication.
"""
import json
import sys
from math import isclose, log2
from pathlib import Path

import k4_word_reordering as W

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "word-reordering-20260928.json").read_text(encoding="utf-8"))
    bad = []
    for s in W.SEGS:
        n = W.arrangements(s)
        tot = rec["procedures_log2"] + log2(n)
        print(f"  {s}: {n:.3g} orders ({log2(n):.1f} bits); with the procedures {tot:.1f} bits "
              f"< crib {W.CRIB_BITS:.1f}")
        if n != rec["arrangements"][s] or round(log2(n), 1) != rec["arrangement_bits"][s] or tot >= W.CRIB_BITS:
            bad.append(f"arrangements {s}")
    ra = W.rule_assignments()
    print(f"  fixed rules: {len(ra)} distinct crib assignments (incl. identity)")
    if len(ra) != rec["fixed_rule_assignments"]:
        bad.append("fixed rules")
    chance = rec["procedures"] * len(ra) * 26.0 ** -24
    print(f"  expected false passes, fixed rules: {chance:.2g}")
    if not isclose(chance, rec["expected_false_passes"]["fixed rules"], rel_tol=0.1):
        bad.append("fixed-rule chance")
    got = {s: [W.word_restart_conflicts(ws, e) for e in (False, True)] for s, ws in W.J03_SEGS.items()}
    for s, v in got.items():
        print(f"  word restart {s:<28} conflicts from start {v[0]}, from end {v[1]}")
    if got != rec["word_restart_conflicts"]:
        bad.append("word restart")
    near = {"identity": W.near_keys(W.CRIB)}
    near.update({s: W.near_keys(W.reversed_assignment(s)) for s in W.SEGS})
    print(f"  crib keys within +-3 on A-Z: {near}")
    if near != rec["near_keys_pm3"]:
        bad.append("near keys")
    if any(v["K4"] for v in rec["runs"].values()):
        bad.append("recorded K4 counts")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: reordering counts, fixed-rule chance, word-restart conflicts and near keys reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
