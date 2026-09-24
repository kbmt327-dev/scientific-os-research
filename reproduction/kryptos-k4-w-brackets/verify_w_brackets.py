"""Rerun every K4-facing computation of EP-0057 and compare it with the recorded results.

    python verify_w_brackets.py

Needs only the Python standard library.  Takes a few seconds.  This is a rerun of the
author's code, not an independent replication.
"""
import json
import sys
from pathlib import Path

import k4_w_alpha25 as alpha25
import k4_w_brackets as brackets
import k4_w_segments as segments
from k4_common import K4, CRIB

HERE = Path(__file__).resolve().parent


def norm(x):
    return json.loads(json.dumps(x))


def main():
    rec = {n: json.loads((HERE / "results" / f"{n}-20260924.json").read_text(encoding="utf-8"))
           for n in ("w-brackets", "w-segments", "w-alpha25")}
    fails = []

    got = {"A": brackets.part_a(K4), "B": brackets.part_b(K4, CRIB), "C": brackets.part_c(K4, CRIB)}
    for part in "ABC":
        if norm(got[part]) != rec["w-brackets"][part]:
            fails.append(f"w-brackets part {part}")

    import random
    rng = random.Random(552)
    seg = {"K4": segments.search(K4, CRIB)}
    for j in range(3):
        seg[f"shuffle{j}"] = segments.search(segments.shuffled(K4, rng), CRIB)
    for v in seg.values():
        del v["all"]
    if norm(seg) != rec["w-segments"]:
        fails.append("w-segments")

    if norm(alpha25.run(K4, CRIB)) != rec["w-alpha25"]:
        fails.append("w-alpha25")

    a = got["A"]
    print(f"P(W at 20 and 74) = {a['P_W_at_20_and_74']:.4f}; "
          f"either orientation = {a['P_W_at_20_74_or_34_62']:.4f}; "
          f"any letter at 20 and 74 = {a['P_same_letter_20_74_any_letter']:.4f}")
    print(f"segment shuffle: K4 passes = {seg['K4']['passes']} over {seg['K4']['patterns']} crib patterns")
    if fails:
        print("MISMATCH:", ", ".join(fails))
        return 1
    print("PASS: EP-0057 recorded results reproduced (author rerun, not independent replication)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
