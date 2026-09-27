"""Check the arithmetic behind the procedure-enumerator Note (EP-0119, 0127, 0131, 0134).

    python verify_enumerator_counts.py

The enumerator itself reads the K1-K3 texts and the carved tableau, which this site does
not publish, so it is not rerun here.  What is checked is every number the Note derives
from the recorded counts: the total and its log2, the description length with the shape
choice, the closed-form expected false passes for the whole crib, for up to two and three
crib errors, and for each crib alone, and the capacity margin against the crib.
Standard library only, well under a second.
"""
import json
import sys
from math import comb, isclose, log2
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "enumerator-20260927.json").read_text(encoding="utf-8"))
    shapes = rec["shapes"]
    n = sum(s["procedures"] for s in shapes)
    fails = []

    def check(name, got, want, rel=0.06):
        ok = isclose(got, want, rel_tol=rel)
        print(f"  {name:<44} {got:.3g}  (recorded {want:.3g})  {'ok' if ok else 'MISMATCH'}")
        if not ok:
            fails.append(name)

    check("total procedures", n, rec["recorded_total"], rel=0.01)
    check("log2 of the total", log2(n), rec["recorded_log2"], rel=0.002)
    check("with the shape choice (bits)", log2(n) + log2(len(shapes)), 55.4, rel=0.002)
    crib_bits = rec["crib_letters"] * log2(26)
    print(f"  crib information {crib_bits:.1f} bits; margin {crib_bits - log2(n):.1f} bits")
    check("expected false passes, whole crib", n * 26.0 ** -24, rec["recorded_expected_false_passes"])
    r = rec["runs"]
    for e, key in ((2, "EP-0131 up to 2 crib errors"), (3, "EP-0131 up to 3 crib errors")):
        # the procedure must agree with at least 24 - e crib letters: choose the e letters, each wrong in 25 ways
        check(f"expected false passes, {e} crib errors", n * comb(24, e) * 25 ** e * 26.0 ** -24,
              r[key]["expected"], rel=0.1)
    check("expected false passes, crib 1 alone", n * 26.0 ** -13, r["EP-0134 crib 1 alone (13 letters)"]["expected"],
          rel=0.1)
    check("expected false passes, crib 2 alone", n * 26.0 ** -11,
          r["EP-0134 crib 2 alone (11 letters, auxiliary)"]["expected"], rel=0.1)
    diff = sum(s["procedures"] for s in shapes if s["label"] == "different method")
    var = n - diff
    print(f"  different-method part {diff:.2g} ({diff / n:.1%}), K1-K3-variant part {var:.2g}")
    check("K1-K3-variant part", var, 2.7e12, rel=0.02)
    zero = all(v.get("K4", 0) == 0 for k, v in r.items() if "K4" in v)
    if not zero:
        fails.append("recorded K4 counts")
    if fails:
        print("FAIL:", ", ".join(fails))
        return 1
    print("PASS: enumerator counts and closed-form chance values reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
