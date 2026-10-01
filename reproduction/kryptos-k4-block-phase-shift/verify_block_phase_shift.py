"""Recompute the exact tests of the block phase-shift Note (EP-0169) that need only K4 and the cribs,
and compare with the record.

    python verify_block_phase_shift.py

Rerun here: the setting counts (186 raw digraph shifts -> 24 crib pairings, 40 plain squares; Bifid
7,176 -> 2,765 block lists, 78 unshifted); free Four-square on K4 (960 settings) and the same 500-shuffle
null as the author (same seed); C08 on 97 and 92 letters; one-square Bifid and CM-Bifid on K4 (2,765
each, exact solver); planted controls for each.  Not rerun: free Two-square, keyword squares, the
CM-Bifid count null and the follow-ups EP-0177 / EP-0184 / EP-0178 (they need other solvers, word
lists or English text, or are long).  Standard library only, about ten seconds.
A rerun of the author's code, not an independent replication.
"""
import json
import random
import sys
from pathlib import Path

import k4_block_phase_shift as B

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "block-phase-shift-20260930.json").read_text(encoding="utf-8"))
    st, ep = rec["settings"], rec["EP-0169"]
    bad = []

    def check(name, ok):
        print(f"  {name:<70} {'ok' if ok else 'MISMATCH'}")
        if not ok:
            bad.append(name)

    # settings
    cs, pq = B.crib_settings(), B.plain_squares()
    new = sum(not B.is_global(v, B.N92) for v in cs.values())
    bs = B.bf_settings()
    unsh = [k for k, v in bs.items() if any(b == B.N92 for _, _, b in v)]
    print(f"  digraph shifts {len(B.raw_settings(B.N92))} -> crib pairings {len(cs)} ({new} new); plain squares {len(pq)}; "
          f"Bifid {sum(len(v) for v in bs.values())} -> {len(bs)} ({len(unsh)} unshifted)")
    check("setting counts", (len(B.raw_settings(B.N92)), len(cs), new, len(pq), sum(len(v) for v in bs.values()), len(bs), len(unsh))
          == (st["digraph_raw"], st["digraph_crib_distinct"], st["digraph_new_by_shift"], st["plain_squares"],
              st["bifid_raw"], st["bifid_crib_distinct"], st["bifid_unshifted"]))

    # free Four-square
    k4fs = sum(B.fs_consistent(B.RED, q, k) for q in pq for k in cs)
    rng = random.Random(16903)                       # the author's null seed
    allbad = 0
    for _ in range(500):
        sh = "".join(rng.sample(B.RED, 92))
        allbad += not any(B.fs_consistent(sh, q, k) for q in pq for k in cs)
    print(f"  free Four-square: K4 consistent {k4fs}/{len(pq) * len(cs)}; shuffles inconsistent everywhere {allbad}/500")
    fs = ep["free Four-square"]
    check("free Four-square K4 0/960, null 473/500",
          (k4fs, len(pq) * len(cs), allbad) == (fs["K4_consistent"], fs["settings"], fs["shuffles_inconsistent_everywhere"][0]))
    rng = random.Random(16911)
    ok = 0
    for _ in range(50):
        b, phi = rng.randrange(B.N92 + 1), rng.randrange(2)
        pairs = B.shift_pairs(b, phi, B.N92)
        enc = B.four_square_enc("".join(rng.sample(B.A25, 25)), "".join(rng.sample(B.A25, 25)))
        P = B.plant92(rng)
        C = [rng.choice(B.A25) for _ in P]
        for i, j in pairs:
            C[i], C[j] = enc(P[i], P[j])
        ok += B.fs_consistent("".join(C), B.square(""), tuple(p for p in pairs if p[0] in B.CR and p[1] in B.CR))
    print(f"  planted Four-square with a shift found: {ok}/50")
    check("Four-square planted 50/50", ok == 50)

    # C08
    res = {}
    for name, text, known in (("97", B.K4, B.CRIB), ("92", B.RED, B.CR)):
        fsx = B.full_settings(len(text))
        conf = {k: B.c08_conflicts(text, known, k) for k in fsx}
        badb = sorted(fsx[k][0][0] for k, c in conf.items() if c)
        glob = [c for k, c in conf.items() if B.is_global(fsx[k], len(text))]
        res[name] = (len(fsx), sum(c == 0 for c in conf.values()), badb, glob)
        print(f"  C08 {name} letters: consistent {res[name][1]}/{res[name][0]}; inconsistent at b = {badb}; unshifted conflicts {glob}")
    check("C08 97: 88/97, inconsistent only for b in 23..31 (inside EASTNORTHEAST)",
          res["97"][:2] == (97, 88) and [res["97"][2][0], res["97"][2][-1]] == ep["C08, 97 letters"]["K4_inconsistent_b"]
          and res["97"][3] == [0, 0])
    check("C08 92: 83/92", res["92"][:2] == (92, ep["C08, 92 letters"]["K4_consistent"]))

    # Bifid and CM-Bifid
    r1 = {k: B.bf_consistent(B.RED, B.CR, k, True) for k in bs}
    r2 = {k: B.bf_consistent(B.RED, B.CR, k, False) for k in bs}
    n1, n2 = sum(v is True for v in r1.values()), sum(v is True for v in r2.values())
    und = sum(v is None for v in list(r1.values()) + list(r2.values()))
    periods = sorted({bs[k][0][0] for k, v in r2.items() if v})
    whole = sorted(bs[k][0][2] for k, v in r2.items() if v and bs[k][0][0] == 0)
    unsh_cons = sum(bool(r2[k]) for k in unsh)
    print(f"  Bifid one square: K4 consistent {n1}/{len(bs)}; CM-Bifid: {n2}/{len(bs)}; undetermined {und}")
    print(f"  CM-Bifid consistent: periods {periods} (0 = whole text split at b = {whole}); unshifted consistent {unsh_cons}")
    check("one-square Bifid 0/2,765", n1 == ep["Bifid, one free square"]["K4_consistent"])
    check("CM-Bifid 27/2,765, 0 undetermined, none unshifted (EP-0120 stands without a shift)",
          n2 == ep["CM-Bifid, two free squares"]["K4_consistent"] and und == 0 and unsh_cons == 0
          and periods == ep["CM-Bifid, two free squares"]["K4_consistent_periods"])
    rng = random.Random(16912)
    found = {True: 0, False: 0}
    keys = list(bs)
    for t in range(20):
        one = t % 2 == 0
        p = rng.choice([0] + list(range(2, 13)))
        a0 = rng.randrange(p) if p else 0
        b = rng.randrange(1, B.N92 + 1)
        blks = B.bf_blocks(p, a0, b)
        q1 = "".join(rng.sample(B.A25, 25))
        q2 = q1 if one else "".join(rng.sample(B.A25, 25))
        C = B.bf_encrypt(B.plant92(rng), q1, q2, blks)
        key = tuple(x for x in blks if any(i in B.CR for i in range(*x)))
        found[one] += B.bf_consistent(C, B.CR, key, one) is True and key in bs
    print(f"  planted Bifid with a shift found: one square {found[True]}/10, CM-Bifid {found[False]}/10")
    check("Bifid planted 10/10 and 10/10", found[True] == 10 and found[False] == 10)

    cn = ep["CM-Bifid, two free squares"]["post_hoc_count_null"]
    print(f"  recorded post hoc CM-Bifid null: median {cn['median']}, p05 {cn['p05']}, P(count <= 27) = {cn['P_le_K4']}")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: the shift settings, free Four-square, C08, Bifid and CM-Bifid results reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
