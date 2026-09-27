"""A free substitution (mask) before or after a shift key (EP-0072-0075), exact tests on the cribs.

  mask before:  C_i = sigma(P_i) + k_i        mask after:  C_i = tau(P_i + k_i)      (A-Z numbers, mod 26)
sigma and tau are completely free.  Two key families are decided exactly:
  * linear keys k_i = a*i + b: b folds into the mask, so the test runs over a = 0..25;
  * periodic keys with free values: a weighted union-find over the unknowns sigma(letter) / tau^-1(letter) and
    the p key values, which fails on a contradiction or when two letters are forced to the same value.
Standard library only.
"""
import random

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = {ch: k for k, ch in enumerate(AZ)}


def linear_ok(ct, a, side):
    """mask before: P_i = P_j <=> C_i - a*i = C_j - a*j ; mask after: C_i = C_j <=> P_i + a*i = P_j + a*j"""
    fwd, back = {}, {}
    for i in POS:
        if side == "before":
            u, v = CRIB[i], (N[ct[i]] - a * i) % 26
        else:
            u, v = (N[CRIB[i]] + a * i) % 26, ct[i]
        if fwd.setdefault(u, v) != v or back.setdefault(v, u) != u:
            return False
    return True


def linear_survivors(ct):
    return [(side, a) for side in ("before", "after") for a in range(26) if linear_ok(ct, a, side)]


class Offsets:
    """union-find with offsets mod 26: value(x) = value(root) + off(x)"""

    def __init__(self):
        self.parent, self.off = {}, {}

    def find(self, x):
        self.parent.setdefault(x, x)
        self.off.setdefault(x, 0)
        if self.parent[x] == x:
            return x, 0
        r, o = self.find(self.parent[x])
        self.parent[x], self.off[x] = r, (self.off[x] + o) % 26
        return r, self.off[x]

    def relate(self, x, y, d):
        """impose value(x) - value(y) = d; False on contradiction"""
        (rx, ox), (ry, oy) = self.find(x), self.find(y)
        if rx == ry:
            return (ox - oy) % 26 == d % 26
        self.parent[rx], self.off[rx] = ry, (d + oy - ox) % 26
        return True


def periodic_ok(ct, p, side):
    uf = Offsets()
    for i in POS:
        k = ("k", i % p)
        if side == "before":                                   # sigma(P) + k = C
            if not uf.relate(("s", CRIB[i]), k, N[ct[i]]):
                return False
        else:                                                  # tau^-1(C) - k = P
            if not uf.relate(("t", ct[i]), k, N[CRIB[i]]):
                return False
    letters = {("s", CRIB[i]) if side == "before" else ("t", ct[i]) for i in POS}
    seen = {}
    for x in letters:
        key = uf.find(x)
        if key in seen and seen[key] != x:
            return False                                        # two letters forced to the same value
        seen[key] = x
    return True


def periodic_survivors(ct, periods=range(1, 49)):
    return [(side, p) for side in ("before", "after") for p in periods if periodic_ok(ct, p, side)]


def shuffle_null(n, seed=720):
    rng = random.Random(seed)
    letters = list(K4)
    lin = per = 0
    for _ in range(n):
        rng.shuffle(letters)
        ct = "".join(letters)
        lin += bool(linear_survivors(ct))
        per += bool([x for x in periodic_survivors(ct, range(1, 25))])
    return lin / n, per / n


def planted(n, seed=721):
    rng = random.Random(seed)
    ok_lin = ok_per = 0
    for t in range(n):
        pt = [rng.choice(AZ) for _ in range(97)]
        for i, ch in CRIB.items():
            pt[i] = ch
        mask = list(AZ)
        rng.shuffle(mask)
        side = ("before", "after")[t % 2]
        a, b = rng.randrange(26), rng.randrange(26)
        p = rng.randrange(1, 25)
        keys = [rng.randrange(26) for _ in range(p)]

        def enc(key):
            out = []
            for i, ch in enumerate(pt):
                if side == "before":
                    out.append(AZ[(N[mask[N[ch]]] + key(i)) % 26])
                else:
                    out.append(mask[(N[ch] + key(i)) % 26])
            return "".join(out)
        ok_lin += (side, a) in linear_survivors(enc(lambda i: a * i + b))
        ok_per += periodic_ok(enc(lambda i: keys[i % p]), p, side)
    return ok_lin, ok_per


def periodic_power(n, seed=722, periods=range(1, 49)):
    """per side and period, the share of shuffled K4 texts that pass (the test decides only where this is small)"""
    rng = random.Random(seed)
    letters = list(K4)
    counts = {(s, p): 0 for s in ("before", "after") for p in periods}
    for _ in range(n):
        rng.shuffle(letters)
        ct = "".join(letters)
        for s, p in counts:
            counts[(s, p)] += periodic_ok(ct, p, s)
    return {k: v / n for k, v in counts.items()}
