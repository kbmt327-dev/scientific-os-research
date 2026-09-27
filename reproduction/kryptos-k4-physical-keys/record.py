"""Write results/physical-keys-20260927.json (the author's recorded run for this package)."""
import json
import statistics as st

import k4_physical_keys as P

r = P.random_roughness(2000)
rec = {
    "source": "rechecked 2026-09-27 for the Note; internal records EP-0059-0069 (2026-09-24/25)",
    "shared_columns": {"32": P.place(32), "63": P.place(63), "33": P.place(33), "64": P.place(64)},
    "column_table": P.column_table(),
    "roughness": {"K4": P.roughness(P.K4), "random_n": 2000, "random_median": st.median(r),
                  "random_share_le_9": sum(x <= 9 for x in r) / 2000, "random_share_le_10": sum(x <= 10 for x in r) / 2000},
    "recorded_not_rerun": {
        "EP-0068 smooth keys from the 3D model v0.4": {"sight-line overlap, S >= 10": "0 of 828 standing points",
                                                        "shadow-edge clock, gain <= 13 steps per letter, S >= 10": "<= 2.3%"},
        "EP-0068 sunlight through the holes": "no moment in the year when all 24 crib letters are lit together (at most 14 and 16)",
        "EP-0065 copper screen wrapped around the trunk (circumference 19-25 columns)": "no candidate; K4 below the null median",
        "EP-0060 reading along wave bands; sine-wave intensity as key": "no candidate",
        "EP-0067 fractionated Morse (24 separator variants); Berlin clock odometer key; seam folds and mirrors; reading from the back": "no candidate",
        "EP-0069 3D model v0.5 over the shape range (27-81 variants): letter behind each hole, shadow timing, distance from a fixed point": "no setting fits; best scores equal to shuffles",
        "EP-0062 wheel and strip devices (M-94, M-138-A)": "impossible if positions coincide (S->S, K->K)",
        "EP-0063 Hagelin M-209 without a mask": "fits the cribs but the rest never becomes English; crib-feasible cage count p = 0.06",
        "EP-0064 HC-9; CX-52 regular stepping": "HC-9 impossible; CX-52 not distinguishable in the sample",
        "EP-0059 periodic key then two 7x7 turning grilles (2.09e10)": "no candidate"}}
with open("results/physical-keys-20260927.json", "w", encoding="utf-8") as fh:
    json.dump(rec, fh, indent=1)
