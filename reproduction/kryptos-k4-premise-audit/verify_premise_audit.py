"""Check the public aggregate projection only; no cipher search is rerun."""
import json
from pathlib import Path

result = json.loads((Path(__file__).parent / "results" / "premise-audit-public-20261011.json").read_text(encoding="utf-8"))
assert result["publication_scope"] == "aggregate_metadata_only"
assert result["ep0188"]["ledger_rows"] == 100
assert sum(result["ep0188"]["grade_counts"].values()) == 20
assert result["ep0188"]["double_coded_rows"] == 14
assert result["ep0188"]["mean_jaccard"] == 0.8
assert result["ep0189"]["rows"] == 62 and result["ep0189"]["salvaged_groups"] == 6
assert result["ep0190"]["groups_with_reported_zero_exact_hits"] == ["G2", "G3", "G4", "G5", "G6"]
assert result["ep0191"]["rows_coded"] == 72
assert result["ep0191"]["rows_in_ep0188_summary"] == 73
assert result["ep0191"]["multiplier_recomputed"] - result["ep0191"]["multiplier_recorded"] == 600
assert sum(result["ep0191"]["states"].values()) == 72
assert result["ep0192"]["finite_groups"] == result["ep0192"]["groups_with_zero_exact_hits"] == 6
assert result["ep0192"]["T6_settings"] == 1898208
assert result["ep0194"]["unknown_subfamily_count"] == 1
print("PASS public aggregate metadata; no search rerun; new plaintext 0")