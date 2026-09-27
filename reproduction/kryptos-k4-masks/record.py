"""Write results/masks-20260927.json (the author's recorded run for this package)."""
import json

import k4_masks as M

power = M.periodic_power(200)
k4_periodic = set(M.periodic_survivors(M.K4))
decidable = {s: [p for p in range(1, 49) if power[(s, p)] <= 0.05] for s in ("before", "after")}
lin_null, per_null = M.shuffle_null(200)
plants_lin, plants_per = M.planted(40)
rec = {
    "source": "rechecked 2026-09-27 for the Note; internal records EP-0072-0077, EP-0084-0086, EP-0088 (2026-09-26)",
    "linear_keys": {"K4_survivors": [list(x) for x in M.linear_survivors(M.K4)], "shuffle_share_with_a_survivor": lin_null,
                    "planted_found": plants_lin, "planted": 40},
    "periodic_keys": {"decidable_periods": decidable,
                      "K4_passes_at_decidable": {s: [p for p in decidable[s] if (s, p) in k4_periodic] for s in decidable},
                      "shuffle_share_passing_some_p_le_24": per_null, "planted_consistent": plants_per, "planted": 40,
                      "power_rule": "a period counts as decidable when at most 5% of 200 shuffles pass"},
    "recorded_not_rerun": {
        "EP-0072/0073 Kryptos-text stride keys, World Clock keys, anchor distances with sigma or tau (61.7M and 0.93M)": {"K4": 0},
        "EP-0074/0075 M-94 with fixed disk orders, autokeys, under sigma or tau": {"K4": 0},
        "EP-0074/0075 M-94 with a free disk order under a mask": "not decidable (about 79 bits against about 52)",
        "EP-0076/0077 stride running keys with masks on both sides (15.4M)": {"crib_survivors": 6889, "best_score": -238.8, "shuffle_best": -243.1, "power": "about 0.65"},
        "EP-0084 Carter & Mace vol. 1 running key": {"no_or_one_mask": "0 with up to 2 crib errors (controls 60/60)", "both_masks": "291 survivors, none English (K4 rank 3 of 11)"},
        "EP-0085 Hagelin M-209 / CX-52 under a mask": "not decidable: freedom exceeds crib + English by tens to 200 bits",
        "EP-0086 ROLL keys and aperture windows (96 readings, 4,081 keys)": "0 with no mask or one mask; no English with both",
        "EP-0088 hand-chosen English running key with one mask": "not decidable with the present search (0/8 plants recovered with the mask unknown); not refuted"}}
with open("results/masks-20260927.json", "w", encoding="utf-8") as fh:
    json.dump(rec, fh, indent=1)
