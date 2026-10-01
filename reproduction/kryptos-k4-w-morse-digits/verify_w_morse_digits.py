"""Recompute the crib-only parts of EP-0180-0183 and compare with the record.

    python verify_w_morse_digits.py

What is rerun:
  * EP-0182: the W positions and the shift of each crib when W is skipped in the key index; the chance
    expectations of the text-key gates from the recorded setting count (26^-24, (26!/13!)/26^24, (26!/12!)/26^24).
  * EP-0183: the reversed key direction gives the same key sequences as the forward family, for every text
    length 2-60 and 97, with and without skipping W (the identity behind "forced before testing").
  * EP-0180: the logic that excludes the pure Morse mask (the operations available at each crib position).
  * EP-0181: the digit-wise addition mechanism with 30 planted controls on random digit streams.  The 22 fixed
    strings are not published; their K4 result is recorded.
The enumerator, the text-key runs (they need K1-K3 texts and the tableau), the sigma variant of the Morse mask
(22.4 million settings) and the digit run on the fixed strings are recorded, not rerun.
Standard library only, about 10 seconds.  A rerun of the author's code, not an independent replication.
"""
import json
import random
import sys
from math import factorial, isclose
from pathlib import Path

import k4_w_morse_digits as M

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "w-morse-digits-20260930.json").read_text(encoding="utf-8"))
    bad = []
    w = rec["w_null_index"]
    shifts, inside = M.crib_shifts()
    print(f"  W positions {M.WPOS}; crib shifts when W is skipped {shifts}; W inside a crib {inside}")
    if M.WPOS != w["w_positions"] or {str(k): v[0] for k, v in shifts.items()} != w["crib_shift"] or inside:
        bad.append("W index")
    g = w["text_keys"]["gates"]
    n = g["none"]["settings"]
    chance = {"none": n * 26.0 ** -24, "sigma": n * factorial(26) / factorial(13) / 26.0 ** 24,
              "tau": n * factorial(26) / factorial(12) / 26.0 ** 24}
    for k, v in chance.items():
        print(f"  text keys, gate {k:<5}: {n:,} settings, chance {v:.3g} (recorded {g[k]['chance']:.3g}), K4 {g[k]['K4']}")
        if not isclose(v, g[k]["chance"], rel_tol=0.01) or g[k]["K4"] != 0:
            bad.append("chance " + k)
    d = g["double"]
    print(f"  two-sided mask (recorded): K4 {d['K4']:,} passes vs chance about {d['chance_K4']:,} {d['chance_band']} "
          f"-> undecidable; English stage {d['english_stage']}")
    if not (abs(d["K4"] - d["chance_K4"]) <= 0.4 * d["chance_K4"]):
        bad.append("double band")
    badL = M.direction_identity(list(range(2, 61)) + [97])
    print(f"  reversed direction = forward family for text lengths 2-60 and 97: {'yes' if not badL else badL}")
    r = rec["reversed_direction"]["double_mask_passes"]
    if badL or r["rev"] != r["forward id"] or r["wskip_rev"] != r["forward wskip"]:
        bad.append("direction identity")
    adm = M.morse_admissible()
    none = [i for i, v in adm.items() if not v]
    some = {i: v for i, v in adm.items() if v}
    print(f"  Morse mask, pure form: {len(none)} of 24 crib positions admit no operation "
          f"({len(M.morse_length_mismatch())} of them by Morse length alone); admissible {some}")
    if len(none) != 22 or sorted(some) != [32, 73]:
        bad.append("Morse logic")
    rng = random.Random(181)
    streams = M.random_streams(rng)
    settings = M.digit_settings(streams)
    found = 0
    for _ in range(30):
        ct, (name, o, dr, sg, eb, db) = M.digit_plant(rng, streams)
        found += any(h[:6] == (name, o, dr, sg, eb, db) for h in M.digit_hits(ct, settings))
    dg = rec["digit_addition"]
    print(f"  digit-wise addition: planted settings recovered {found}/30 on random streams; "
          f"recorded K4 result on the 22 fixed strings {dg['K4']} of {dg['distinct_on_crib']:,} (chance {dg['chance']:.2g})")
    if found != 30:
        bad.append("digit controls")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: W-index shifts, chance values, the direction identity, the Morse logic and the digit mechanism reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
