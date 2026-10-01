"""Portax with one free substitution layer (EP-0156, finishing EP-0116): the table, the vertical pairs, and a
small exact decider for the 'before' layer (the 'after' layer needs a constraint solver; recorded only).  Standard library only.

Portax (ACA rules): the text is written in rows of the period P; letters i and i+P of each block of 2P form a
vertical pair (the last partial block is split in half); each column has a key letter, and only key // 2 matters
(13 slides).  Upper rows A-M / N-Z (the second shifted by the slide), lower rows ACE..Y / BDF..Z (both shifted);
the two letters are rectangle corners, the upper one first; in the same column, the other two letters of that column.

  before  C = Portax_key(sigma(P))     sigma a free substitution
  after   C = tau(Portax_key(P))       tau a free substitution
"""
K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
N = 97
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def portax(x):
    """encipher function of slide x (0..12) on letter indices"""
    up = [list(range(13)), [13 + ((j + x) % 13) for j in range(13)]]
    lo = [[2 * ((j + x) % 13) for j in range(13)], [2 * ((j + x) % 13) + 1 for j in range(13)]]
    upos = {v: (r, j) for r in (0, 1) for j, v in enumerate(up[r])}
    lpos = {v: (r, j) for r in (0, 1) for j, v in enumerate(lo[r])}

    def enc(p1, p2):
        (u, a), (v, b) = upos[p1], lpos[p2]
        if a != b:
            return up[u][b], lo[v][a]
        return up[1 - u][a], lo[1 - v][a]
    return enc


PX_ENC = [{(a, b): portax(x)(a, b) for a in range(26) for b in range(26)} for x in range(13)]
PX_DEC = [{v: k for k, v in d.items()} for d in PX_ENC]


def pairs(P, n=N):
    """(i, j, column) for the vertical pairs of a text of length n written in rows of P"""
    out = []
    for b0 in range(0, n, 2 * P):
        r = min(2 * P, n - b0)
        h = P if r == 2 * P else r // 2
        out += [(b0 + c, b0 + h + c, c) for c in range(h)]
    return out


def encipher(key, pt):
    out = list(pt)
    for i, j, c in pairs(len(key), len(pt)):
        out[i], out[j] = PX_ENC[key[c] // 2][(pt[i], pt[j])]
    return out


def crib_pairs(P):
    """pairs with at least one crib letter"""
    return [(i, j, c) for i, j, c in pairs(P) if i in CRIB or j in CRIB]


def before_consistent(P, ct, budget=None):
    """Exact test of C = Portax(sigma(P)) on the crib: is there a slide per column and an injective sigma on the
    crib letters with (sigma(P_i), sigma(P_j)) = Dec(C_i, C_j) on the crib side(s) of every pair touching the
    crib?  Backtracking over the key columns, the column with the fewest compatible slides first.
    Returns True / False, or None if more than `budget` nodes were needed."""
    ps = crib_pairs(P)
    bycol = {}
    for i, j, c in ps:
        bycol.setdefault(c, []).append((i, j))
    cols = sorted(bycol, key=lambda c: -sum((i in CRIB) + (j in CRIB) for i, j in bycol[c]))
    opts = {}
    for c in cols:
        lst = []
        for x in range(13):
            items, ok, loc = [], True, {}
            for i, j in bycol[c]:
                v0, v1 = PX_DEC[x][(ct[i], ct[j])]
                for q, v in ((i, v0), (j, v1)):
                    if q in CRIB:
                        L = CRIB[q]
                        if loc.get(L, v) != v:
                            ok = False
                        loc[L] = v
            if ok and len(set(loc.values())) == len(loc):
                lst.append(loc)
        opts[c] = lst
    sig, used = {}, {}
    nodes = [0]

    class Budget(Exception):
        pass

    def fits(loc):
        return all(sig[L] == v if L in sig else v not in used for L, v in loc.items())

    def rec(left):
        nodes[0] += 1
        if budget is not None and nodes[0] > budget:
            raise Budget
        if not left:
            return True
        # dynamic ordering: the column with the fewest options compatible with sigma so far
        best = None
        for c in left:
            fit = [loc for loc in opts[c] if fits(loc)]
            if best is None or len(fit) < len(best[1]):
                best = (c, fit)
                if not fit:
                    return False
        c, fit = best
        rest = [d for d in left if d != c]
        for loc in fit:
            new = [L for L in loc if L not in sig]
            for L in new:
                sig[L] = loc[L]
                used[loc[L]] = L
            if rec(rest):
                return True
            for L in new:
                del used[sig[L]]
                del sig[L]
        return False
    try:
        return rec(cols)
    except Budget:
        return None


def plant(rng, P, layer):
    """random letters with the cribs written in, random key and substitution"""
    pt = [AZ.index(CRIB[i]) if i in CRIB else rng.randrange(26) for i in range(N)]
    key = [rng.randrange(26) for _ in range(P)]
    perm = list(range(26))
    rng.shuffle(perm)
    if layer == "before":
        return encipher(key, [perm[x] for x in pt])
    return [perm[x] for x in encipher(key, pt)]
