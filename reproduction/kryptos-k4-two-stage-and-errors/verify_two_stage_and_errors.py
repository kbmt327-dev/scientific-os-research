from pathlib import Path
import json, math

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "results" / "two-stage-and-errors-20261011.json").read_text(encoding="utf-8"))

def require(condition, label):
    if not condition:
        raise SystemExit("FAIL: " + label)

def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)

e = DATA["experiments"]
x = e["EP-0227"]
require((x["null_targets"], x["null_rows"]) == (22, 88), "EP-0227 scope")
require(x["k4_registered_passes"] == 0 and x["null_registered_pass_targets"] == 0, "EP-0227 passes")
require(x["registered_rule_requires_nonidentity"] and x["null_identity_hits"] == 1 and not x["identity_hit_eligible"], "EP-0227 identity eligibility")

x = e["EP-0236"]
hist = x["null_min_dstar_histogram"]
require(sum(hist.values()) == x["null_count"] == 20, "EP-0236 histogram")
rank = sum(n for value, n in hist.items() if int(value) <= x["k4_min_dstar"])
require(rank == 20 and close(rank / x["null_count"], x["recorded_null_min_le_k4_fraction"]), "EP-0236 rank fraction")
require((x["k4_settings"], x["k4_timeouts"], x["k4_unknown"], x["k4_registered_passes"]) == (466, 0, 0, 0), "EP-0236 K4 scope")

x = e["EP-0238"]
require(sum(x["null_min_max_histogram"].values()) == x["null_count"] == 200, "EP-0238 max histogram")
require(sum(x["null_min_sum_histogram"].values()) == x["null_count"], "EP-0238 sum histogram")
nmax = sum(n for value, n in x["null_min_max_histogram"].items() if int(value) <= x["k4_joint_min_max"])
nsum = sum(n for value, n in x["null_min_sum_histogram"].items() if int(value) <= x["k4_joint_min_sum"])
require(close(nmax / x["null_count"], x["recorded_fraction_max_le_k4"]), "EP-0238 max fraction")
require(close(nsum / x["null_count"], x["recorded_fraction_sum_le_k4"]), "EP-0238 sum fraction")
require(x["null_registered_passes"] == 0 and x["row_null_registered_passes"] == 0, "EP-0238 passes")

x = e["EP-0240"]
require(x["main_null_targets_per_column"] == 200 and x["auxiliary_null_targets"] == 10, "EP-0240 null scope")
require(x["k4_registered_passes"] == x["main_null_registered_passes"] == x["auxiliary_null_registered_passes"] == 0, "EP-0240 passes")
for name, col in x["columns"].items():
    if col["k4_min_h"] is None:
        require(col["rank_numerator"] is None and col["source_recorded_fraction"] is None, "EP-0240 " + name + " undefined")
    else:
        require(col["rank_denominator"] == 200 and close(col["rank_numerator"] / col["rank_denominator"], col["source_recorded_fraction"]), "EP-0240 " + name + " fraction")

x = e["EP-0241"]
for name, fam in x["other_registered_families"].items():
    require(fam["k4_registered_passes"] == 0 and fam["null_count"] == 1000 and fam["null_texts_with_pass"] == 0, "EP-0241 " + name)
r = x["r27"]
require(r["registered_q1_settings"] == 26 and close(r["q1_fraction"], 0.01), "EP-0241 r27 subset")
require(r["null_count"] == 100 and r["nulls_complete_for_registered_subset"] and not r["full_q1_k4_search_completed"] and not r["full_q1_null_evaluation_completed"], "EP-0241 r27 boundary")
require(r["k4_registered_passes"] == 0 and r["null_texts_with_pass"] == 0, "EP-0241 r27 passes")
require(x["preregistration_k4_exposure"] and x["metric_and_subset_selection_after_exposure"], "EP-0241 exposure")
require(x["registered_rules_threshold_settings_and_column_split_unchanged_after_exposure"] and not x["per_run_code_hash_verified"], "EP-0241 disclosure")
require(DATA["independent_replications"] == 0 and DATA["new_k4_plaintext"] == 0, "overall scope")
print("PASS: five episode aggregates, counts, fractions, and scope boundaries; no search rerun.")
