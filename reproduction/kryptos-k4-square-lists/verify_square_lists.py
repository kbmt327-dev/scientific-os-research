"""Check public inventories and recorded histogram arithmetic; no search rerun."""
import json
import math
from pathlib import Path
import k4_square_lists as sq

root = Path(__file__).parent
result = json.loads((root / "results" / "square-lists-20261011.json").read_text(encoding="utf-8"))
inv = result["inventory"]
assert len(sq.places()) == inv["worldclock_places"] == 146
assert len(sq.KEYWORDS) == inv["keyword_seeds"] == 40
assert len(sq.squares185()) == inv["unique_squares"] == 185
assert len(sq.PAIRINGS) == inv["pairings"] == 48
assert len(sq.ADJ) == inv["adjacent_modes"] == 3
assert len(sq.seg_starts()) == inv["segment_starts"] == 6
assert len(list(sq.bf_settings())) == inv["bifid_settings"] == 2765
checked = 0
for family in result["families"]:
    nulls = family["nulls"]
    if nulls is None:
        assert family["public_scan_rerun"] is False
        continue
    hist = nulls.get("minimum_mismatch_histogram", nulls.get("joint_minimum_mismatch_histogram"))
    assert sum(hist.values()) == nulls["n"]
    observed = family.get("minimum_mismatches", family.get("joint_minimum_mismatches"))
    share = sum(count for mismatch, count in hist.items() if int(mismatch) <= observed) / nulls["n"]
    assert math.isclose(share, nulls["share_at_or_below_observed"], abs_tol=1e-12)
    checked += 1
assert checked == 5
print(f"PASS inventory={len(inv)} checks; histogram_families={checked}; no scan rerun; new plaintext 0")