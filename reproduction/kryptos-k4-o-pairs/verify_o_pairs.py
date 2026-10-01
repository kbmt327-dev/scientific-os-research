"""Recompute the crib-only facts and the 2x2 Hill search of the O-pairs Note (EP-0138) and
compare with the record.

    python verify_o_pairs.py

The square-cipher results are exact CP-SAT proofs run with OR-tools; they are recorded in
results/ and not rerun here.  What is rerun: the 15 pairs and which letters are known, the
absence of repeated input digraphs (so no fixed digraph table can be refuted), Playfair's
repeated-letter input, the contradiction under the mirror pairing, and the 2x2 Hill search
(linear and affine, four alphabets, both directions) with 10 planted controls.  Later check (EP-0157): the pair
counts, the equation count of the mixed-alphabet Hill and the mirror contradiction on the other pairings, and the
recorded square results there.  Standard library only, a few seconds.
A rerun of the author's code, not an independent replication.
"""
import json
import sys
from pathlib import Path

import k4_o_pairs as O

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "o-pairs-20260928.json").read_text(encoding="utf-8"))
    bad = []
    ps = O.pairs()
    both = O.both_known(ps)
    one = [x for x in ps if (x[1][0] is None) != (x[1][1] is None)]
    print(f"  pairs (21+o, 59+o): {len(both)} with both letters known, {len(one)} with one")
    if (len(both), len(one)) != (rec["pairs_both_known"], rec["pairs_one_known"]):
        bad.append("pairs")
    clash, same = O.repeated_inputs(ps)
    print(f"  repeated input digraphs: {len(clash) + len(same)} -> any fixed digraph table is consistent (undecidable)")
    if clash or same:
        bad.append("repeated inputs")
    rr = [p for p, c in both if p[0] == p[1]]
    print(f"  input digraphs with a doubled letter: {rr} -> Playfair cannot encipher them on this pairing")
    if not rr:
        bad.append("Playfair")
    mclash, _ = O.repeated_inputs(O.pairs(mirror=True))
    print(f"  mirror pairing (21+o, 73-o): {mclash} -> every fixed digraph table contradicts")
    if not mclash:
        bad.append("mirror")
    fixed_first = [(p, c) for p, c in both if p[0] == c[0] and p[1] != c[1]]
    print(f"  first letter unchanged, second changed: {fixed_first}")
    total = 0
    for name, al in O.ALPHABETS.items():
        for affine in (False, True):
            for rev in (False, True):
                r = O.hill_rows(al, affine, rev)
                total += sum(r)
                print(f"  2x2 Hill {name:<13} {'affine' if affine else 'linear':<6} {'rev' if rev else 'fwd'}: "
                      f"solutions per row {r}")
    # planted control: 9 random pairs under a random affine map must be solved
    import random
    rng = random.Random(1380)
    found = 0
    for _ in range(10):
        n = rng.choice((25, 26))
        m = [[rng.randrange(n) for _ in range(2)] for _ in range(2)]
        b = [rng.randrange(n), rng.randrange(n)]
        eqs = []
        for _ in range(9):
            pv = [rng.randrange(n), rng.randrange(n)]
            eqs.append((pv, [(m[r][0] * pv[0] + m[r][1] * pv[1] + b[r]) % n for r in range(2)]))
        found += all(k >= 1 for k in O.solve_rows(eqs, n, True))
    print(f"  planted affine 2x2 maps recovered: {found}/10")
    if found != 10:
        bad.append("Hill control")
    if total != rec["hill_2x2_solutions_per_row"]:
        bad.append("Hill")
    if any(v["K4"] != "inconsistent" for v in rec["free_square_settings"].values()) or rec["keyed_squares"]["K4"]:
        bad.append("recorded square results")
    # later check (EP-0157): other pairings; the square results are recorded CP-SAT proofs
    more = json.loads((HERE / "results" / "o-pairs-more-20260930.json").read_text(encoding="utf-8"))
    cnt = more["mixed_alphabet_hill"]["count"]
    for nm, pp in O.other_pairings().items():
        full, half, eq, unk, clash = O.hill_count(pp)
        print(f"  later check, {nm:<6}: pairs both/one known {full}/{half}, mixed-alphabet Hill equations {eq} "
              f"vs unknowns {unk}; same input with two outputs: {[c[0] for c in clash]}")
        if [full, half, eq, unk] != cnt[nm] or bool(clash) != (nm == "mirror"):
            bad.append("later check " + nm)
    print(f"  later check, recorded squares on the new pairings: K4 inconsistent in {more['K4_UNSAT']} of "
          f"{more['square_settings']}; consistent in {more['K4_SAT_settings']}")
    if more["K4_UNSAT"] + more["K4_SAT"] != 224 or             sum(v["K4"] == "UNSAT" for v in more["settings"].values()) != more["K4_UNSAT"]:
        bad.append("later check record")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: pair facts reproduce and the 2x2 Hill has no solution on these pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
