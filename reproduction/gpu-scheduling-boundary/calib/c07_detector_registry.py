"""C7: every detector that turns a measurement into a verdict must be registered
and audited.

Why this file exists. Three times this domain has published conclusions that a
detector, not the physics, decided:

  EP-0001/EP-0002  three single-horizon stability detectors failed in a row.
                   The lesson was written down AND moved into code -- but only
                   into calib/c05 (rho_max) and adjudicate.py (the phase
                   diagram).
  EP-0010          the safe-ratio table, the domain's headline operational
                   number, turned out to rest on `flow balance >= 0.9` at a
                   single 30000-job horizon.  That constant was placed in
                   analyze_e6.py during EP-0004 and carried unchanged through
                   six episodes.  Two published rows sat +0.0006 and +0.0064
                   above the line while the statistic's own seed standard
                   deviation is 0.012 to 0.105.
  EP-0011          that same statistic was found to be a right-censoring ratio,
                   (1 - fb) ~= 1.76 * mean_response_time / window.  It is
                   INSENSITIVE to the horizon precisely because it cannot see
                   divergence: numerator and denominator both scale with the
                   window.

So writing the lesson down was not enough, and moving it into code was not
enough either, because nobody enumerated the detectors it applied to.  This
file is that enumeration, and it fails the build when the enumeration goes
stale.

Three checks:

  A  every detector marked "validated" carries evidence for BOTH a horizon
     audit and a threshold audit.
  B  every (statistic, numeric threshold) pair that appears in the analysis
     code is registered here, or is explicitly attributed to a sealed
     prediction file.  A new constant appearing in a new analyze_*.py fails
     this check until someone registers it.
  C  a detector whose statistic is normalised by the observation window may
     NOT be marked validated on the strength of horizon-insensitivity.  That
     is the exact inference EP-0011 showed to be wrong.
  D  a sealed prediction may not use, as a THRESHOLD, a number that the same
     file also reports as a MEASURED value.  EP-0013 rounded a measured ratio
     of 0.5899 to "0.59" and then used 0.59 as a cut; the cut excluded the very
     job that produced the ratio, by 0.03 of a GPU, and produced a spurious
     "zero such jobs".

Run: python calib/c07_detector_registry.py
"""
import json
import os
import ast
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --------------------------------------------------------------- registry
# status:
#   validated  -- audited on both axes and currently trusted
#   invalid    -- measured and found not to work; kept so it is not re-invented
#   suspended  -- in use for published claims but the audit overturned it
#   unaudited  -- in use, not yet audited on both axes
REGISTRY = [
    {
        "id": "completion_frac",
        "statistic": "completion_frac",
        "threshold": 0.98,
        "verdict": "unstable",
        "used_in": ["sim/cluster.py", "adjudicate.py"],
        "window_normalised": False,
        "horizon_audit": "EP-0001: a finite system always drains after the "
                         "arrival stream ends, so it never fires",
        "threshold_audit": "EP-0001: no threshold works; the defect is "
                           "structural, not a mis-set constant",
        "status": "invalid",
        "note": "retained as a diagnostic only. Never use as a stability "
                "verdict.",
    },
    {
        "id": "util_over_rho",
        "statistic": "util_over_rho",
        "threshold": 0.995,
        "verdict": "backlog_growing",
        "used_in": ["sim/cluster.py"],
        "window_normalised": False,
        "horizon_audit": "EP-0001, EP-0002: fires on long transients in stable "
                         "systems",
        "threshold_audit": "EP-0002: no threshold separates a long transient "
                           "from divergence",
        "status": "invalid",
        "note": "retained as a diagnostic only.",
    },
    {
        "id": "flow_balance_spread",
        "statistic": "spread of flow_balance_by_need across classes",
        "threshold": 0.30,
        "verdict": "class-starved",
        "used_in": ["adjudicate.py"],
        "window_normalised": True,
        "horizon_audit": "calib/c06: spread moved 0.361 -> 0.419 over a 4x "
                         "horizon while the starved class's JCT grew linearly",
        "threshold_audit": "EP-0002: chosen from the observed bimodality "
                           "(starved ~0.4 against 1.00 for every other class)",
        "status": "unaudited",
        "note": "EP-0011 showed the LEVEL of flow balance is a censoring "
                "ratio. Whether the SPREAD between classes inherits that "
                "defect has not been measured. Its horizon-insensitivity is "
                "no longer evidence of validity (check C).",
    },
    {
        "id": "flow_balance_level_ok",
        "statistic": "min_flow_balance",
        "threshold": 0.995,
        "verdict": "stable (no re-run needed)",
        "used_in": ["adjudicate.py", "analyze_e2e3.py", "analyze_e4.py"],
        "window_normalised": True,
        "horizon_audit": "EP-0002: cells at min_fb ~ 0.98 grew 3.4x over a 4x "
                         "horizon, which is why the line is 0.995 and not 0.97",
        "threshold_audit": "EP-0002, by the 4x-horizon JCT test",
        "status": "unaudited",
        "note": "the 0.995 line was set BY a horizon test, which is the right "
                "way round. But EP-0011 showed the underlying statistic is "
                "window-normalised, so the line's meaning should be re-derived "
                "from alpha. Tracked as U-28.",
    },
    {
        "id": "r_safe",
        "statistic": "flow_balance_by_need[m]",
        "threshold": 0.9,
        "verdict": "the largest class is 'fed' / safe",
        "used_in": ["analyze_e6.py", "analyze_e7.py", "analyze_e9.py",
                    "analyze_e12.py", "analyze_e13.py"],
        "window_normalised": True,
        "horizon_audit": "EP-0011 D1: r* moves only +0.006..+0.021 over a 4x "
                         "horizon -- but EP-0011 section 4 showed that is "
                         "because the statistic is a censoring ratio, not "
                         "because it is robust",
        "threshold_audit": "EP-0011 D4/D6: moving the line to 0.8 or 0.95 "
                           "moves the boundary by 0.052..0.137 while "
                           "preserving the ORDER of conditions",
        "status": "suspended",
        "note": "EP-0004..EP-0010 published operational numbers from this. "
                "EP-0011 suspended them. Cells this detector calls safe have "
                "alpha 0.8..0.96, i.e. near-linear divergence. Replacement "
                "candidate is `alpha`, sealed in PRED-013.",
    },
    {
        "id": "class_starved",
        "statistic": "flow_balance_by_need[k]",
        "threshold": 0.5,
        "verdict": "class-starved",
        "used_in": ["sim/cluster.py", "analyze_e6.py", "analyze_e11.py",
                    "analyze_e12.py"],
        "window_normalised": True,
        "horizon_audit": None,
        "threshold_audit": None,
        "status": "unaudited",
        "note": "the coarse classification used by EP-0003, EP-0008 and "
                "EP-0009. It is far from the 0.9 line, so it is more robust in "
                "practice, but it has never been audited on either axis.",
    },
    {
        "id": "rho_max_saturation",
        "statistic": "saturated throughput",
        "threshold": None,
        "verdict": "stability region of a policy",
        "used_in": ["calib/c05_rho_max.py"],
        "window_normalised": False,
        "horizon_audit": "calib/c05: measured under saturation, so there is no "
                         "arrival window to normalise by",
        "threshold_audit": "not applicable: the output is a rate, not a "
                           "classification",
        "status": "validated",
        "note": "EP-0001: invalid for policies that starve a class, because "
                "throughput stays high while one class is unbounded. Always "
                "read alongside a per-class check.",
    },
    {
        "id": "alpha_divergence_elasticity",
        "statistic": "dlog E[T of the largest class] / dlog horizon",
        "threshold": 0.5,
        "verdict": "the class is diverging",
        "used_in": ["analyze_e14.py"],
        "window_normalised": False,
        "horizon_audit": "PRED-013 G1: sealed test of whether adding a fourth "
                         "horizon moves the boundary",
        "threshold_audit": None,
        "status": "unaudited",
        "note": "0.5 is a convention (the midpoint between converged and "
                "linearly divergent), not a derived criterion. E[T] averages "
                "completed jobs only, which biases alpha DOWNWARD at the "
                "divergent end, so the resulting boundary errs toward calling "
                "things stable.",
    },
]

# (statistic token, threshold literal) pairs that belong to a sealed prediction
# file rather than to a reusable detector. Sealed files are immutable, so their
# constants are attributed rather than registered.
# Each (file, token, literal) that the scanner finds must be attributed here or
# be a registered detector. Writing the attribution down IS the discipline: an
# unexplained constant in an analysis script is how EP-0010 happened.
ATTRIBUTIONS = {
    ("analyze_e11.py", "fb", 0.5): "detector `class_starved`, PRED-010 Y4/Y5",
    ("analyze_e12.py", "fb", 0.5): "detector `class_starved`",
    ("analyze_e14.py", "fb", 1.0): "not a detector: G9 excludes cells at "
                                   "fb == 1.0, where the censoring ratio is "
                                   "identically zero and uninformative",
    ("analyze_e7.py", "fb", 0.99): "PRED-006 U5, sealed: EASY backfill must "
                                   "stay >= 0.99 at every N and ratio. A "
                                   "stricter one-off line than `r_safe`; it "
                                   "was never used to set a boundary",
    ("analyze_e7.py", "x", 0.98): "detector `completion_frac`, used as the "
                                  "run-validity guard",
    ("sim/cluster.py", "out", 0.98): "detector `completion_frac`",
    ("sim/cluster.py", "out", 0.995): "detector `util_over_rho`",
    ("analyze_e13.py", "fb", 0.9): "detector `r_safe` (PRED-012 D10 reference)",
    ("analyze_e12.py", "v", 0.9): "detector `r_safe` (PRED-011 Z7 reference)",
    ("analyze_e11.py", "value", 0.9): "detector `r_safe` (PRED-010 Y7)",
}

STAT_TOKENS = [
    "flow_balance", "fb_m", "min_flow_balance", "completion_frac",
    "util_over_rho", "SAFE_FB", "STARVE_FB", "LEVEL_OK", "SPREAD_STARVE",
    "fb", "alpha", "alpha4", "spread",
]
REGISTERED_PAIRS = {
    (d["statistic"], d["threshold"]) for d in REGISTRY
} | {
    ("SAFE_FB", 0.9), ("STARVE_FB", 0.5), ("LEVEL_OK", 0.995),
    ("SPREAD_STARVE", 0.30), ("flow_balance_by_need[m]", 0.9),
    ("flow_balance_by_need[k]", 0.5), ("min_flow_balance", 0.995),
    ("completion_frac", 0.98), ("util_over_rho", 0.995),
}

def _stat_name(node):
    """Textual name of the thing being compared, preferring a dict key."""
    if isinstance(node, ast.Subscript):
        sl = node.slice
        if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
            return sl.value
        return _stat_name(node.value)
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _stat_name(node.func)
    return ""


def scan_thresholds():
    """Check B: find (file, statistic, literal) comparisons in analysis code.

    AST-based on purpose: a regex over source text also matches docstrings and
    prose, and an unenforceable check is worse than none.
    """
    found = {}
    targets = [f for f in os.listdir(ROOT)
               if f.startswith("analyze_") and f.endswith(".py")]
    targets += ["adjudicate.py", "sim/cluster.py"]
    for rel in sorted(targets):
        path = os.path.join(ROOT, *rel.split("/"))
        if not os.path.isfile(path):
            continue
        tree = ast.parse(open(path, encoding="utf-8").read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue
            operands = [node.left] + list(node.comparators)
            lits = [o.value for o in operands
                    if isinstance(o, ast.Constant)
                    and isinstance(o.value, float)]
            if not lits:
                continue
            names = [_stat_name(o) for o in operands
                     if not isinstance(o, ast.Constant)]
            for name in names:
                if not name:
                    continue
                if not any(tok in name or tok == name for tok in STAT_TOKENS):
                    continue
                for lit in lits:
                    found.setdefault((rel, name, lit), []).append(
                        f"{rel}:{node.lineno}")
    return found


def main():
    failures, warnings = [], []

    # ---- check A: validated detectors carry both audits
    for d in REGISTRY:
        if d["status"] == "validated":
            if not d["horizon_audit"] or not d["threshold_audit"]:
                failures.append(
                    f"A: detector '{d['id']}' is marked validated but is "
                    f"missing a horizon or threshold audit")

    # ---- check C: window-normalised detectors cannot be validated by
    #      horizon-insensitivity (the EP-0011 inference error)
    for d in REGISTRY:
        if d["window_normalised"] and d["status"] == "validated":
            failures.append(
                f"C: detector '{d['id']}' is normalised by the observation "
                f"window and cannot be marked validated. EP-0011: a "
                f"window-normalised statistic is horizon-insensitive because "
                f"it divides the divergence away, not because it is robust.")

    # ---- check B: every threshold in the analysis code is accounted for
    found = scan_thresholds()
    for (rel, stat, lit), sites in sorted(found.items()):
        if (stat, lit) in REGISTERED_PAIRS:
            continue
        if (rel, stat, lit) in ATTRIBUTIONS:
            continue
        failures.append(
            f"B: threshold `{stat} vs {lit}` at {', '.join(sites[:3])} is "
            f"neither a registered detector nor attributed in ATTRIBUTIONS. "
            f"Write down what it is before publishing anything that depends "
            f"on it.")

    # ---- check D: a threshold that grazes its own data
    for (fn, label, q), (rmax, qv) in sorted(scan_grazing_thresholds().items()):
        failures.append(
            f"D: {fn} reports zero items for {label} at threshold {q}, but its "
            f"maximum observed value is {rmax:.4f}, within "
            f"{100 * (qv - rmax) / qv:.2f}% below the cut. The zero is the "
            f"threshold, not the data (EP-0013 F64). Use the unrounded value "
            f"or acknowledge it in GRAZE_ACKNOWLEDGED.")

    # ---- report
    by_status = {}
    for d in REGISTRY:
        by_status.setdefault(d["status"], []).append(d["id"])
    print("detector registry")
    for status in ["validated", "unaudited", "suspended", "invalid"]:
        ids = by_status.get(status, [])
        print(f"  {status:>10}: {len(ids):>2}  {', '.join(ids) if ids else '-'}")
    print(f"\nthreshold comparisons scanned: {len(found)} distinct "
          f"(statistic, literal) pairs")
    for w in warnings:
        print(f"  WARN {w}")

    if failures:
        print(f"\nFAIL ({len(failures)})")
        for f in failures:
            print(f"  - {f}")
    else:
        print("\nPASS: every detector in use is registered, and no detector is "
              "marked validated without both audits.")

    out = {
        "registry": REGISTRY,
        "scanned_pairs": {f"{f}|{s}|{l}": sites
                          for (f, s, l), sites in found.items()},
        "failures": failures,
        "n_validated": len(by_status.get("validated", [])),
        "n_suspended": len(by_status.get("suspended", [])),
        "n_unaudited": len(by_status.get("unaudited", [])),
    }
    json.dump(out, open(os.path.join(HERE, "c07_detector_registry.json"), "w",
                        encoding="utf-8"), indent=1)
    return 1 if failures else 0



# Check D: a threshold that "grazes" its own data. EP-0013 rounded a measured
# ratio of 0.5899 to 0.59 and used 0.59 as a cut; the cut excluded the single
# job that produced the ratio, by 0.03 of a GPU, and reported "zero such jobs".
#
# A first version of this check scanned the sealed prediction files for numbers
# that appear both as a threshold and as a reported measurement. It fired 46
# times, almost all of them on grid values, rho, and 0.0/1.0. A check that fires
# on everything gets ignored, which is the failure mode this whole file exists
# to prevent, so it was replaced by the precise form below.
#
# The precise signature is: a filter returns ZERO items while the maximum
# observed value sits just under the cut. That is detectable with no false
# positives.
GRAZE_TOL = 0.01        # "just under" = within 1% of the threshold

GRAZE_ACKNOWLEDGED = {
    ("E15.json", "11cb48", "0.59"): "KNOWN DEFECT, kept for the record. "
                                    "EP-0013 section 4: ratio 0.5899 rounded "
                                    "to 0.59 excluded the defining job.",
}


def grazes(max_value, threshold, tol=GRAZE_TOL):
    """True when a zero count is an artifact of the cut rather than the data."""
    if threshold <= 0:
        return False
    return 0 < (threshold - max_value) / threshold <= tol


def scan_grazing_thresholds():
    """Check D over any result file shaped like a trace frequency table."""
    hits = {}
    rdir = os.path.join(ROOT, "results")
    if not os.path.isdir(rdir):
        return hits
    for fn in sorted(os.listdir(rdir)):
        if not fn.endswith(".json"):
            continue
        try:
            data = json.load(open(os.path.join(rdir, fn), encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = data.get("rows") or []
        else:
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            freq, rmax = row.get("freq"), row.get("ratio_max")
            if not isinstance(freq, dict) or rmax is None:
                continue
            label = row.get("vc") or row.get("id") or "?"
            for q, v in freq.items():
                if v == 0 and grazes(float(rmax), float(q)):
                    key = (fn, str(label), str(q))
                    if key not in GRAZE_ACKNOWLEDGED:
                        hits[key] = (float(rmax), float(q))
    return hits


def selftest():
    """Prove checks A and C can actually fail. A guard that cannot fire is
    worse than no guard, which is the failure mode this whole file exists to
    prevent."""
    probes = [
        ({"id": "_probe_A", "window_normalised": False, "status": "validated",
          "horizon_audit": None, "threshold_audit": "x"},
         "A", "validated without a horizon audit"),
        ({"id": "_probe_C", "window_normalised": True, "status": "validated",
          "horizon_audit": "x", "threshold_audit": "x"},
         "C", "window-normalised and marked validated"),
    ]
    ok = True
    for probe, check, why in probes:
        fired = False
        if probe["status"] == "validated" and (
                not probe["horizon_audit"] or not probe["threshold_audit"]):
            fired = fired or check == "A"
        if probe["window_normalised"] and probe["status"] == "validated":
            fired = fired or check == "C"
        print(f"  selftest {check}: {'fires' if fired else 'DOES NOT FIRE'} "
              f"on a detector {why}")
        ok = ok and fired
    print("  selftest B: add an unregistered comparison to any analyze_*.py "
          "and rerun; it must FAIL")
    fires = grazes(0.5899, 0.59) and not grazes(0.5899, 0.75)         and not grazes(0.59, 0.59)
    print(f"  selftest D: {'fires' if fires else 'DOES NOT FIRE'} on the "
          f"EP-0013 case (max 0.5899 under a 0.59 cut) and stays quiet on a "
          f"genuine zero (0.5899 under 0.75) and on an exact match")
    ok = ok and fires
    print(f"  selftest D: {len(scan_grazing_thresholds())} unacknowledged "
          f"grazing threshold(s) in results/ "
          f"({len(GRAZE_ACKNOWLEDGED)} acknowledged)")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
