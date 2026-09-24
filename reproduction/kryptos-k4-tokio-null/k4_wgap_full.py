"""Pay every reading freedom at once, exactly, against the frozen place list.

EP-0010 enumerated 32 conventions but still fixed two things by choice: the
occurrence count n was restricted to {5, 6}, and the target was restricted to
five-letter names.  Neither is forced by anything external.  The lesson of
EP-0009 is that an unpaid freedom cannot be deferred, so this pays both.

The family is now every (multiplicity m present in K4) x (gap definition) x
(anchor) x (direction) x (base).  A letter of multiplicity m yields a string of
length m with an anchor and m-1 without one, so the reachable target lengths are
read off the multiplicity profile of K4 rather than chosen.  The target set is
every place name on the frozen list whose letters-only form has such a length.

Every branch is invertible, so the null probability is computed in closed form:

    E[hits] = sum over (target, m) of
              (distinct position sets of size m that yield it) * (carriers of
              multiplicity m) / C(97, m)

Usage:  python k4_wgap_full.py   (writes wgap-full-rerun.json)
"""
import collections
import json
from math import comb

# K4 ciphertext: Jim Sanborn, *Kryptos* (1990), quoted for research; not licensed here.
CT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

LEN = 97


def decode(s, base):
    lo = 1 if base == "A1" else 0
    return [ord(c) - 65 + lo for c in s]
GAPDEF = ("between", "difference")
ANCHOR = ("start", "zero", "cyclic", "none")
DIRECTION = ("forward", "reverse")
BASE = ("A1", "A0")


def preimages(seq, m, gapdef, anchor):
    """Position tuples of size m whose gaps under this convention give seq."""
    sub = 1 if gapdef == "between" else 0
    out = []
    if anchor == "none":                      # m-1 gaps, first position free
        if len(seq) != m - 1:
            return out
        for v0 in range(LEN):
            v = [v0]
            for g in seq:
                v.append(v[-1] + g + sub)
            if v[-1] < LEN and all(v[k] > v[k - 1] for k in range(1, m)):
                out.append(tuple(v))
        return out
    if len(seq) != m:
        return out
    if anchor == "cyclic":                    # the wrap constraint fixes the total
        if sum(seq) + m * sub != LEN:
            return out
        for v0 in range(LEN):
            v = [v0]
            for g in seq[1:]:
                v.append(v[-1] + g + sub)
            if v[-1] < LEN and all(v[k] > v[k - 1] for k in range(1, m)):
                out.append(tuple(v))
        return out
    pre = -1 if anchor == "start" else 0
    v = [pre + seq[0] + sub]
    for g in seq[1:]:
        v.append(v[-1] + g + sub)
    if 0 <= v[0] and v[-1] < LEN and all(v[k] > v[k - 1] for k in range(1, m)):
        out.append(tuple(v))
    return out


def family(text, mults):
    """Every in-range string the full convention family yields for one text."""
    pos = collections.defaultdict(list)
    for i, c in enumerate(text):
        pos[c].append(i)
    by_m = collections.defaultdict(dict)
    for c, v in pos.items():
        by_m[len(v)][c] = v
    out = set()
    for m in mults:
        for c, v in by_m.get(m, {}).items():
            for gapdef in GAPDEF:
                sub = 1 if gapdef == "between" else 0
                for anchor in ANCHOR:
                    if anchor == "none":
                        seq = [v[k] - v[k - 1] - sub for k in range(1, m)]
                    else:
                        pre = -1 if anchor == "start" else 0 if anchor == "zero" \
                            else v[-1] - LEN
                        seq = [v[0] - pre - sub] + \
                              [v[k] - v[k - 1] - sub for k in range(1, m)]
                    if not seq:
                        continue
                    for direction in DIRECTION:
                        s = seq[::-1] if direction == "reverse" else seq
                        for base in BASE:
                            lo, hi = (1, 26) if base == "A1" else (0, 25)
                            if all(lo <= x <= hi for x in s):
                                out.add("".join(chr(65 + x - lo) for x in s))
    return out


def main(write=True):
    d = json.load(open("data/worldclock-place-letters.json", encoding="utf-8"))
    names = sorted(set(d["letters"]))
    mult = collections.Counter(CT)
    carriers = collections.Counter(mult.values())          # multiplicity -> letters
    mults = sorted(carriers)
    lengths = sorted({m for m in mults} | {m - 1 for m in mults if m >= 2})
    targets = [n for n in names if len(n) in lengths]

    print("K4 multiplicity profile: %s" % dict(sorted(carriers.items())))
    print("reachable string lengths: %s" % lengths)
    print("frozen list: %d names, %d of a reachable length" % (len(names), len(targets)))

    fam = family(CT, mults)
    hits = sorted(fam & set(targets))

    per = {}
    total = 0.0
    for tgt in targets:
        sets = collections.defaultdict(set)
        for m in mults:
            if len(tgt) not in (m, m - 1):
                continue
            for gapdef in GAPDEF:
                for anchor in ANCHOR:
                    for direction in DIRECTION:
                        for base in BASE:
                            seq = decode(tgt, base)
                            if direction == "reverse":
                                seq = seq[::-1]
                            sets[m].update(preimages(seq, m, gapdef, anchor))
        e = sum(carriers[m] * len(s) / comb(LEN, m) for m, s in sets.items())
        if e:
            per[tgt] = e
            total += e

    print("\nreachable targets with nonzero null probability: %d" % len(per))
    for t, e in sorted(per.items(), key=lambda x: -x[1])[:12]:
        print("  %-10s %.3e%s" % (t, e, "   <- K4 produces this" if t in hits else ""))
    print("\nfully paid E[hits] = P(at least one hit) <= %.3e" % total)
    print("K4 family size: %d   hits: %s" % (len(fam), hits))

    res = {"lengths": lengths, "targets": len(targets), "nonzero": len(per),
           "expected_hits_total": total, "per_target": per,
           "k4_hits": hits, "k4_family_size": len(fam),
           "carriers": dict(sorted(carriers.items()))}
    if write:
        json.dump(res, open("wgap-full-rerun.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, sort_keys=True)
    return res


if __name__ == "__main__":
    main()
