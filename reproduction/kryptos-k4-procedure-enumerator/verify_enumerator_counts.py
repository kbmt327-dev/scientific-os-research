"""Check the arithmetic behind the procedure-enumerator Note (EP-0119, 0127, 0131, 0134, 0136, 0143).

    python verify_enumerator_counts.py

The enumerator itself reads the K1-K3 texts and the carved tableau, which this site does
not publish, so it is not rerun here.  What is checked is every number the Note derives
from the recorded counts: the total and its log2, the description length with the shape
choice, the closed-form expected false passes for the whole crib, for up to two, three,
four, seven and eight crib errors, and for each crib alone, the capacity margin against the
crib, how many scattered hand alterations an e-error run covers (hypergeometric), and for the
fixed-origin features (EP-0143) the chance values, the 79 auxiliary origins, and the identity
of (i + 337) div 31 with K4's carved row.
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
    for e in (4, 7, 8):
        key = next(k for k in r if k.startswith(f"EP-0136 up to {e} crib errors"))
        # cumulative: agree with at least 24 - e crib letters
        got = n * sum(comb(24, j) * 25 ** j for j in range(e + 1)) * 26.0 ** -24
        check(f"expected false passes, <= {e} crib errors", got, r[key]["expected"], rel=0.1)

    def cover(k, e):
        # k altered letters scattered over 97 positions; P(at most e of them fall on the 24 crib positions)
        return sum(comb(k, j) * comb(97 - k, 24 - j) for j in range(min(e, k) + 1)) / comb(97, 24)

    ks = (10, 15, 20, 25, 28, 30, 35, 40)
    print("  coverage of k scattered alterations:  k = " + ", ".join(map(str, ks)))
    for e in (4, 7, 8):
        print(f"    e = {e}: " + ", ".join(f"{cover(k, e):.3f}" for k in ks))
    for (k, e), want in {(20, 7): 0.93, (28, 7): 0.62, (35, 7): 0.29, (35, 8): 0.47}.items():
        check(f"coverage k = {k}, e = {e}", cover(k, e), want, rel=0.01)
    check("expected false passes, crib 1 alone", n * 26.0 ** -13, r["EP-0134 crib 1 alone (13 letters)"]["expected"],
          rel=0.1)
    check("expected false passes, crib 2 alone", n * 26.0 ** -11,
          r["EP-0134 crib 2 alone (11 letters, auxiliary)"]["expected"], rel=0.1)
    diff = sum(s["procedures"] for s in shapes if s["label"] == "different method")
    var = n - diff
    print(f"  different-method part {diff:.2g} ({diff / n:.1%}), K1-K3-variant part {var:.2g}")
    check("K1-K3-variant part", var, 2.7e12, rel=0.02)
    # EP-0143: fixed-origin features
    o = rec["ep0143"]
    r43 = r["EP-0143 fixed-origin features, whole crib"]
    nn = r43["new_procedures"]
    check("EP-0143 chance, whole crib", nn * 26.0 ** -24, r43["expected"], rel=0.1)
    check("EP-0143 chance, crib 1 alone", nn * 26.0 ** -13, r["EP-0143 fixed-origin features, crib 1 alone"]["expected"],
          rel=0.1)
    check("EP-0143 chance, crib 2 alone", nn * 26.0 ** -11,
          r["EP-0143 fixed-origin features, crib 2 alone (auxiliary)"]["expected"], rel=0.1)
    check("grammar total after EP-0143", n + nn, o["grammar_total_after"], rel=0.01)
    for e in (4, 7, 8):
        key = next(k for k in r if k.startswith(f"EP-0143 fixed-origin main features, up to {e} crib errors"))
        nm = r[key]["main_procedures"]
        got = nm * sum(comb(24, j) * 25 ** j for j in range(e + 1)) * 26.0 ** -24
        check(f"EP-0143 main, <= {e} crib errors", got, r[key]["expected"], rel=0.1)
    aux = sum(o["aux_moduli"])
    print(f"  EP-0143 auxiliary origins: every o = 0..m-1 for m in {o['aux_moduli']} -> {aux} features")
    if aux != o["aux_features"]:
        fails.append("aux origins")
    # (i + o) div m changes only by a constant when o moves by m, so o mod m covers every origin
    for m in o["aux_moduli"]:
        for oo in range(m):
            dif = {(i + oo + m) // m - (i + oo) // m for i in range(97)}
            if dif != {1}:
                fails.append(f"origin shift m={m}")
    # K4's carved row: positions 0-3 are row 24, then rows 25-27 of 31 letters
    row = [24 if i < 4 else 25 + (i - 4) // 31 for i in range(97)]
    diff = {(i + 337) // 31 - row[i] for i in range(97)}
    print(f"  (i + 337) div 31 minus K4's carved row: {sorted(diff)} (a constant, so m = 31 from the K3 head is the carved row)")
    if len(diff) != 1:
        fails.append("carved row identity")
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
