"""EP-0057 Part E: W passes through, everything else is a 25-letter cipher.

EP-0052 closed every 25-symbol method because K4 uses all 26 letters.  That closure assumes
the ciphertext alphabet is the whole text's.  If W is a pass-through plaintext separator, the
other 92 letters only need 25 symbols -- and K4's non-W letters are exactly the other 25.

  Playfair (any square without W)  a letter never enciphers to itself; K4 has ct == crib at
                                   32 (S) and 73 (K) -> rejected for every square.
  mod-25 periodic / progressive / autokey, alphabets A-Z minus W and KRYPTOS minus W,
  key index on the 92 non-W letters (W does not advance) or on all 97 (W advances).

Run:  python k4_w_alpha25.py --plants
      python k4_w_alpha25.py --k4 --json w-alpha25-20260924.json
"""
import json
import random
import sys

from k4_common import K4, CRIB, AZ, KA
from k4_w_brackets import drop_w, trivial_periods

A25 = {"AZ-W": AZ.replace("W", ""), "KA-W": KA.replace("W", "")}
KINDS = ("vig", "beau")  # vbeau consistency == vig consistency for numeric keys


def kv(kind, A, c, p):
    return (A.index(c) - A.index(p)) % 25 if kind == "vig" else (A.index(c) + A.index(p)) % 25


def enc(kind, A, p, k):
    return A[(A.index(p) + k) % 25] if kind == "vig" else A[(k - A.index(p)) % 25]


def dec(kind, A, c, k):
    return A[(A.index(c) - k) % 25] if kind == "vig" else A[(k - A.index(c)) % 25]


def gate(t, cr, pos_of, kind, A):
    """t: letters (W never looked up), cr: crib by index into t, pos_of: key index."""
    n = len(t)
    out = {"periodic": [], "progressive": [], "ct-autokey": []}
    idx = sorted(cr)
    kval = {i: kv(kind, A, t[i], cr[i]) for i in idx}
    triv = trivial_periods({pos_of[i]: 0 for i in idx}, n // 2)
    for p in range(1, n // 2 + 1):
        if p in triv:
            continue
        seen = {}
        if all(seen.setdefault(pos_of[i] % p, kval[i]) == kval[i] for i in idx):
            out["periodic"].append(p)
        for s in range(1, 25):
            if p > 26:
                break
            seen = {}
            if all(seen.setdefault(pos_of[i] % p, (kval[i] - s * (pos_of[i] // p)) % 25)
                   == (kval[i] - s * (pos_of[i] // p)) % 25 for i in idx):
                out["progressive"].append((p, s))
    # autokey over the non-W stream only (W is not part of the 25-letter stream)
    for L in range(1, 31):
        if all(i - L < 0 or t[i - L] == "W" or kval[i] == A.index(t[i - L]) for i in idx):
            out["ct-autokey"].append(L)
    return out


def run(ct, crib):
    res = {}
    t92, cr92 = drop_w(ct, crib)
    pos92 = {i: i for i in cr92}
    pos97 = {i: i for i in crib}
    for aname, A in A25.items():
        for kind in KINDS:
            res[f"{kind}-{aname} dropW(92)"] = gate(t92, cr92, pos92, kind, A)
            res[f"{kind}-{aname} keepW(97)"] = gate(ct, crib, pos97, kind, A)
    res["playfair_self_encryption_positions"] = [i for i, p in crib.items() if ct[i] == p]
    return res


def plant(rng, aname, kind, P, mode):
    A = A25[aname]
    Wpos = [20, 36, 48, 58, 74]
    while True:
        key = [rng.randrange(25) for _ in range(P)]
        ct, j = [], 0
        for i in range(97):
            if i in Wpos:
                ct.append("W")
                continue
            p = CRIB.get(i) or rng.choice(A)
            ki = j if mode == "dropW(92)" else i
            ct.append(enc(kind, A, p, key[ki % P]))
            j += 1
        return "".join(ct)


if __name__ == "__main__":
    if "--plants" in sys.argv:
        rng = random.Random(557)
        for aname in A25:
            for kind in KINDS:
                for mode, P in (("dropW(92)", 7), ("keepW(97)", 11)):
                    r = run(plant(rng, aname, kind, P, mode), CRIB)
                    print(aname, kind, mode, P, P in r[f"{kind}-{aname} {mode}"]["periodic"])
        sys.exit()
    if "--k4" in sys.argv:
        r = run(K4, CRIB)
        for k, v in r.items():
            print(k, v)
        if "--json" in sys.argv:
            with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
                json.dump(r, f, indent=1)
