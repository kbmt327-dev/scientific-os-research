"""EP-0057 Part D: the six W-segments as transposition blocks.

If the Ws are designer-placed (they spell TOKIO, H-11) the segments may be blocks that were
shuffled.  Model: plaintext = the six ciphertext segments (W removed) in some order pi, each
possibly reversed, optionally with one separator slot between blocks; then a periodic key on
the PLAINTEXT index (keying on the ciphertext index would make the shuffle invisible and
reduce to the drop-W test).  720 orders x 64 reversal masks x 2 separator modes.

Gate: all 24 crib letters consistent.  A pass with c = 24 - (#distinct residues) crib
constraints has chance 26^-c, so the statistic is the largest c reached by any pass;
the same search is run on 3 shuffles of K4's non-W letters (W layout kept).

Run:  python k4_w_segments.py --plants
      python k4_w_segments.py --k4 --json w-segments-20260924.json
"""
import json
import random
import sys
from itertools import permutations, product

from k4_common import K4, CRIB, AZ, KA
from k4_w_brackets import SETTINGS, kval, enc, dec

SETS = [s for s in SETTINGS if s[0] != "vbeau"]  # vbeau consistency == vig consistency
PMAX = 46


def seg_bounds(ct):
    W = [i for i, c in enumerate(ct) if c == "W"]
    return list(zip([0] + [w + 1 for w in W], W + [len(ct)]))


def arrangement_map(bounds, order, rev, sep):
    """ciphertext index -> plaintext index."""
    m, t = {}, 0
    for b in order:
        s, e = bounds[b]
        idx = list(range(s, e))
        if rev[b]:
            idx.reverse()
        for i in idx:
            m[i] = t
            t += 1
        t += sep
    return m


def search(ct, crib):
    bounds = seg_bounds(ct)
    kv = {(kind, A): {i: kval(kind, A, ct[i], p) for i, p in crib.items()} for kind, A in SETS}
    ci = sorted(crib)
    # consistency depends only on crib-index differences, so arrangements are grouped by
    # that pattern; multiplicity is kept so pass counts are counts of concrete arrangements
    groups = {}
    for order in permutations(range(len(bounds))):
        for rev in product((0, 1), repeat=len(bounds)):
            for sep in (0, 1):
                m = arrangement_map(bounds, order, rev, sep)
                pos = [m[i] for i in ci]
                rel = tuple(x - min(pos) for x in pos)
                g = groups.setdefault(rel, [0, (order, rev, sep)])
                g[0] += 1
    best, passes = [], 0
    hist = {}
    for pos, (mult, (order, rev, sep)) in groups.items():
                for p in range(1, PMAX + 1):
                    res = [x % p for x in pos]
                    c = len(ci) - len(set(res))
                    if c == 0:
                        continue
                    for (kind, A), k in kv.items():
                        seen, ok = {}, True
                        for r, i in zip(res, ci):
                            if seen.setdefault(r, k[i]) != k[i]:
                                ok = False
                                break
                        if ok:
                            passes += mult
                            hist[c] = hist.get(c, 0) + mult
                            best.append((c, p, kind, "AZ" if A == AZ else "KA", order, rev, sep, mult))
    best.sort(reverse=True)
    return {"patterns": len(groups), "passes": passes, "hist_c": dict(sorted(hist.items())),
            "top": best[:10], "all": best}


def shuffled(ct, rng):
    letters = [c for c in ct if c != "W"]
    rng.shuffle(letters)
    it = iter(letters)
    return "".join("W" if c == "W" else next(it) for c in ct)


def plant(rng):
    """encipher a crib-bearing plaintext with periodic key, cut into K4's segment lengths
    under a random arrangement, and check the search recovers it at high c."""
    bounds = seg_bounds(K4)
    kind, A = rng.choice(SETS)
    order = tuple(rng.sample(range(6), 6))
    rev = tuple(rng.randrange(2) for _ in range(6))
    sep = rng.randrange(2)
    m = arrangement_map(bounds, order, rev, sep)
    P = rng.randrange(5, 15)
    while True:  # key redrawn too: a crib letter can encipher to W under a fixed key
        key = [rng.randrange(26) for _ in range(P)]
        ct = list(K4)
        for i in m:
            p = CRIB.get(i) or rng.choice(AZ)
            ct[i] = enc(kind, A, p, key[m[i] % P])
        if "".join(ct).count("W") == 5:
            break
    r = search("".join(ct), CRIB)
    ci = sorted(CRIB)
    want = [m[i] for i in ci]
    want = tuple(x - min(want) for x in want)

    def rel(b):
        mm = arrangement_map(bounds, b[4], b[5], b[6])
        q = [mm[i] for i in ci]
        return tuple(x - min(q) for x in q)
    hit = [b for b in r["all"] if b[1] == P and rel(b) == want]
    return {"planted": (P, kind, "AZ" if A == AZ else "KA", order, rev, sep),
            "recovered_at_c": hit[0][0] if hit else None, "top_c": r["top"][0][0]}


if __name__ == "__main__":
    if "--plants" in sys.argv:
        rng = random.Random(551)
        for _ in range(3):
            print(plant(rng))
        sys.exit()
    if "--k4" in sys.argv:
        rng = random.Random(552)
        out = {"K4": search(K4, CRIB)}
        for j in range(3):
            out[f"shuffle{j}"] = search(shuffled(K4, rng), CRIB)
        for v in out.values():
            del v["all"]
        for k, v in out.items():
            print(k, v["passes"], v["hist_c"], v["top"][:3])
        if "--json" in sys.argv:
            with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
                json.dump(out, f, indent=1)
