"""Recompute the parts of the layout-transposition Note (EP-0186) that need only K4's length,
the crib positions and the recorded counts, and compare with the record.

    python verify_layout_transposition.py

What is rerun: the set Pi of layout transpositions (176 items, 104 distinct non-identity,
counts per family, its sha256 as committed before any run on K4), the capacity 7.70 bit of
208 settings, the closed-form chance values of the three stages, where the crib positions go
under order B, and a round-trip control for every Pi.  The enumerator runs (GPU) and the
confirmation statistic (English letter frequencies) are recorded in results/, not rerun.
Standard library only, under a second.  A rerun of the author's code, not an independent replication.
"""
import json
import sys
from collections import Counter
from math import comb, exp, isclose, log2
from pathlib import Path

import k4_layout_pi as L

HERE = Path(__file__).resolve().parent
CRIB_POS = list(range(21, 34)) + list(range(63, 74))


def chance(n, settings, e):
    return settings * n * sum(comb(24, j) * 25 ** j for j in range(e + 1)) * 26.0 ** -24


def main():
    rec = json.loads((HERE / "results" / "layout-transposition-20261001.json").read_text(encoding="utf-8"))
    bad = []

    def check(name, got, want, rel=0.06):
        ok = isclose(got, want, rel_tol=rel)
        print(f"  {name:<44} {got:.3g}  (recorded {want:.3g})  {'ok' if ok else 'MISMATCH'}")
        if not ok:
            bad.append(name)

    raw, ps = L.build(), L.pi_set()
    fam = dict(Counter(f for _, f in ps))
    print(f"  Pi: {len(raw)} items, {len(ps)} distinct non-identity, by family {fam}")
    r = rec["pi"]
    if (len(raw), len(ps), fam) != (r["raw_items"], r["distinct_non_identity"], r["by_family"]):
        bad.append("Pi counts")
    h = L.digest(ps)
    print(f"  sha256 of Pi {h[:12]}...{h[-5:]} ({'matches' if h == r['sha256'] else 'DIFFERS FROM'} the committed set)")
    if h != r["sha256"]:
        bad.append("Pi digest")
    check("log2 |Pi|", log2(len(ps)), r["log2"], rel=0.002)
    settings = 2 * len(ps)
    check("settings (104 x 2 orders)", settings, rec["settings"], rel=0)
    check("capacity of the setting choice (bit)", log2(settings), rec["capacity_bits"], rel=0.002)
    n = rec["enumerator_procedures"]
    st = rec["stages"]
    t1 = 2 * fam["T1"]
    check("S1 chance, e <= 4, 208 settings", chance(n, settings, 4), st["S1"]["chance"])
    check("S2 chance, e <= 7, T1 48 settings", chance(n, t1, 7), st["S2"]["chance"])
    check("S3 chance, e <= 7, 160 settings", chance(n, settings - t1, 7), st["S3"]["chance"])
    total = chance(n, t1, 7) + chance(n, settings - t1, 7)
    print(f"  expected chance hits at e <= 7 over S2 + S3: {total:.2f} (P(at least one) {1 - exp(-total):.2f}); "
          f"recorded non-identity hits {st['S2']['K4_non_identity_hits'] + st['S3']['K4_non_identity_hits']}")
    # order B: how far the crib positions move
    stay = sum(all(L.inverse(list(s))[i] == i for i in CRIB_POS) for s, _ in ps)
    spread = Counter(len({L.inverse(list(s))[i] - i for i in CRIB_POS}) == 1 for s, _ in ps)
    print(f"  order B: Pi leaving all 24 crib positions in place: {stay}; moving them by one common offset: "
          f"{spread[True]} of {len(ps)}")
    ok = sum(L.planted_roundtrip(list(s), k) for k, (s, _) in enumerate(ps))
    print(f"  round trip (transpose then undo) recovers a random text for {ok}/{len(ps)} Pi")
    if ok != len(ps):
        bad.append("round trip")
    if st["S1"]["K4_non_identity_hits"] or st["S3"]["K4_non_identity_hits"] or st["S2"]["K4_non_identity_hits"] != 1:
        bad.append("recorded hits")
    print(f"  recorded: S1 0, S2 1 (not confirmed, p = 0.81), S3 0; identities 0 in every stage")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: Pi, its capacity and the chance values reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
