"""Recompute the masked linear-key and periodic-key tests (EP-0072-0075) and compare with the record.

    python verify_masks.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_masks as M

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "masks-20260927.json").read_text(encoding="utf-8"))
    power = M.periodic_power(200)
    k4 = set(M.periodic_survivors(M.K4))
    dec = {s: [p for p in range(1, 49) if power[(s, p)] <= 0.05] for s in ("before", "after")}
    lin_null, per_null = M.shuffle_null(200)
    pl, pp = M.planted(40)
    got_lin = {"K4_survivors": [list(x) for x in M.linear_survivors(M.K4)], "shuffle_share_with_a_survivor": lin_null,
               "planted_found": pl, "planted": 40}
    got_per = {"decidable_periods": dec,
               "K4_passes_at_decidable": {s: [p for p in dec[s] if (s, p) in k4] for s in dec},
               "shuffle_share_passing_some_p_le_24": per_null, "planted_consistent": pp, "planted": 40,
               "power_rule": rec["periodic_keys"]["power_rule"]}
    print(f"  linear keys under a free mask: K4 survivors {got_lin['K4_survivors'] or 'none'}; plants {pl}/40")
    for s in dec:
        print(f"  periodic key, mask {s}: decidable periods {dec[s]}; K4 passes at {got_per['K4_passes_at_decidable'][s]}")
    print(f"  shuffles passing some period <= 24: {per_null:.1%}; plants consistent {pp}/40")
    bad = [k for k in got_lin if got_lin[k] != rec["linear_keys"][k]]
    bad += [k for k in got_per if got_per[k] != rec["periodic_keys"][k]]
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: masked linear and periodic key tests reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
