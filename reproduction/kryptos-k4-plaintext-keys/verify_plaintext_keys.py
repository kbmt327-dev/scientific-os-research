"""Recompute the plaintext-key Note (EP-0150, EP-0179) from the K4 ciphertext and the cribs, and compare with the
record.

    python verify_plaintext_keys.py            # about 20 s
    python verify_plaintext_keys.py --full     # 10,000 autokey shuffles as in the record, and every possible V

EP-0150 (plaintext autokey, lag L = 1..40, A-Z / KRYPTOS x three tables): all 240 K4 cells are recomputed and
compared cell by cell with the record; 24 planted controls; a shuffle null (1,000 shuffles here, 10,000 with --full).
EP-0179 (plaintext-indexed periodic key): the shift-table and arbitrary-row tests on the 32 sets V that need no
other text, 40 planted controls, and a shuffle null on those sets (200 shuffles).  The record's 28 further sets come
from another part of the sculpture and are not printed; --full instead checks every possible V (only V's
intersection with the 12 crib letters that move an index matters, so 2^12 classes cover all sets).
Standard library only.  A rerun of the author's method, not an independent replication.
"""
import json
import random
import sys
from pathlib import Path

import k4_plaintext_keys as M

HERE = Path(__file__).resolve().parent


def autokey(rec, full, bad):
    r = rec["ep0150_plaintext_autokey"]
    k4 = {(an, d, L): M.autokey_conflicts(M.K4, A, d, L) for an, A in M.ALPHABETS for d in M.DIRS
          for L in range(1, 41)}
    diff = [k for k, v in k4.items() if r["cells"][f"{k[0]} {k[1]} {k[2]}"]["conflicts"] != v[0]
            or r["cells"][f"{k[0]} {k[1]} {k[2]}"]["checks"] != v[1]]
    k4min = min(t for k, (t, c) in k4.items() if k[2] <= 20)
    arg = [f"{a} {d} {L}" for (a, d, L), (t, c) in k4.items() if L <= 20 and t == k4min]
    low = [t for k, (t, c) in k4.items() if k[2] <= 12]
    print(f"EP-0150 plaintext autokey: 240 K4 cells recomputed, {len(diff)} differ from the record")
    print(f"  L <= 20 (120 cells): every cell has >= {k4min} conflicting crib letters; minimum at {arg}")
    print(f"  L <= 12: conflicts {min(low)}..{max(low)}")
    if diff or k4min != r["min_conflicts_L_le_20"] or sorted(arg) != sorted(r["argmin_L_le_20"]) \
            or [min(low), max(low)] != r["conflicts_L_le_12"]:
        bad.append("autokey K4 cells")
    rng = random.Random(1500)
    ok = 0
    for an, A in M.ALPHABETS:
        for d in M.DIRS:
            for L in (3, 7, 13, 20):
                ok += M.autokey_conflicts(M.autokey_plant(rng, A, d, L), A, d, L)[0] == 0
    print(f"  planted controls with 0 conflicts: {ok}/24")
    if ok != 24:
        bad.append("autokey controls")
    S = 10000 if full else 1000
    le = 0
    for _ in range(S):
        s = list(M.K4)
        rng.shuffle(s)
        s = "".join(s)
        m = min(M.autokey_conflicts(s, A, d, L)[0] for an, A in M.ALPHABETS for d in M.DIRS for L in range(1, 21))
        le += m <= k4min
    print(f"  shuffles {S}: share whose minimum over the 120 cells is <= {k4min}: {le / S:.3f} "
          f"(record {r['P_shuffle_min_le_K4_min']} with {r['shuffles']})")
    if abs(le / S - r["P_shuffle_min_le_K4_min"]) > (0.02 if full else 0.04):
        bad.append("autokey null")


def indexed(rec, full, bad):
    r = rec["ep0179_plaintext_indexed_key"]
    kk = M.crib_keys(M.K4)
    f = [(n, p) for n, V in M.PUBLIC_SETS for p in range(1, 25) if M.fixed_ok(M.K4, V, p, kk)]
    rows = [(n, p) for n, V in M.PUBLIC_SETS for p in range(1, 25) if M.rows_ok(M.K4, V, p)]
    cells = len(M.PUBLIC_SETS) * 24
    print(f"EP-0179 plaintext-indexed key, {len(M.PUBLIC_SETS)} sets x p 1..24 = {cells} cells")
    print(f"  shift tables: {len(f)} passing cells: {[f'{n} {p}' for n, p in f]}")
    print(f"  arbitrary rows: {len(rows)} passing cells (p <= 12: {sum(p <= 12 for _, p in rows)})")
    disjoint = [n for n, V in M.PUBLIC_SETS if not V & set(M.RELEVANT)]
    print(f"  sets disjoint from the index-moving crib letters {M.RELEVANT}: {disjoint}")
    if sorted(f"{n} {p}" for n, p in f) != sorted(r["fixed_table_pass_cells"]) or any(p != 24 for _, p in f) \
            or sorted(n for n, _ in f) != sorted(disjoint):
        bad.append("indexed K4")
    rng = random.Random(1790)
    ok = 0
    for _ in range(40):
        n, V = rng.choice(M.PUBLIC_SETS)
        p = rng.randint(2, 24)
        an, A = rng.choice(M.ALPHABETS)
        d = rng.choice(M.DIRS)
        ct = M.indexed_plant(rng, V, p, A, d)
        ok += M.fixed_ok(ct, V, p) and M.rows_ok(ct, V, p)
    print(f"  planted controls passing at their (V, p) in both tests: {ok}/40")
    if ok != 40:
        bad.append("indexed controls")
    S = 200
    nf, nr = [], []
    for _ in range(S):
        s = list(M.K4)
        rng.shuffle(s)
        s = "".join(s)
        ks = M.crib_keys(s)
        nf.append(sum(M.fixed_ok(s, V, p, ks) for _, V in M.PUBLIC_SETS for p in range(1, 25)))
        nr.append(sum(M.rows_ok(s, V, p) for _, V in M.PUBLIC_SETS for p in range(1, 25)))
    print(f"  shuffles {S}: shift-table passes mean {sum(nf) / S:.1f} (K4 {len(f)}), "
          f"share >= K4 {sum(x >= len(f) for x in nf) / S:.2f}; arbitrary rows mean {sum(nr) / S:.1f} "
          f"(K4 {len(rows)}), share <= K4 {sum(x <= len(rows) for x in nr) / S:.2f}")
    if sum(x >= len(f) for x in nf) / S < 0.5:
        bad.append("indexed null")
    if full:
        allv = rec["all_V_check"]
        got = sorted(f"{''.join(sorted(V)) or '(none)'} {p}" for V in M.all_relevant_subsets() for p in range(1, 25)
                     if M.fixed_ok(M.K4, V, p, kk))
        print(f"  every possible V ({2 ** len(M.RELEVANT)} classes x 24 periods): shift-table passes {got}")
        if got != sorted(allv["K4_pass_cells"]):
            bad.append("all-V check")


def main():
    full = "--full" in sys.argv
    rec = json.loads((HERE / "results" / "plaintext-keys-20260930.json").read_text(encoding="utf-8"))
    bad = []
    autokey(rec, full, bad)
    indexed(rec, full, bad)
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: the autokey cells, the shift-table passes and the controls reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
