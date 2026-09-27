"""Consistency checks on K4's cribs that need no key search (EP-0112, EP-0113, EP-0116).

Standard library only.
"""
import random
from collections import defaultdict

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def successive_occurrences():
    """pairs (earlier position, later position) of the same plaintext letter with no occurrence of that letter
    in between, both inside one crib (so every letter between them is known)"""
    out = []
    for start, word in CRIBS.items():
        last = {}
        for k, ch in enumerate(word):
            if ch in last:
                out.append((ch, last[ch], start + k))
            last[ch] = start + k
    return out


def occurrence_shift_conflicts(ct):
    """shift-by-count form C = tau(sigma(x) + d*n_x + b): for successive occurrences of a letter the ciphertext
    moves by the same d under tau^-1.  So the step map (earlier ciphertext letter -> later one) must be a partial
    injective function: one letter cannot step to two letters, and two letters cannot step to one."""
    fwd, back = defaultdict(set), defaultdict(set)
    for ch, a, b in successive_occurrences():
        fwd[ct[a]].add(ct[b])
        back[ct[b]].add(ct[a])
    out = {f"{s}->": sorted(d) for s, d in fwd.items() if len(d) > 1}
    out.update({f"->{t}": sorted(d) for t, d in back.items() if len(d) > 1})
    return out


def occurrence_null(n, seed=1120):
    """share of shuffled K4 texts on which the same check already fails"""
    rng = random.Random(seed)
    letters = list(K4)
    bad = 0
    for _ in range(n):
        rng.shuffle(letters)
        bad += bool(occurrence_shift_conflicts("".join(letters)))
    return bad / n


def homophone_collisions(ct):
    """ciphertext letters that come from two different plaintext letters inside the crib"""
    src = defaultdict(set)
    for i, p in CRIB.items():
        src[ct[i]].add(p)
    return {c: "".join(sorted(ps)) for c, ps in sorted(src.items()) if len(ps) > 1}


def self_encryptions(ct):
    return [(i, CRIB[i]) for i in sorted(CRIB) if ct[i] == CRIB[i]]


def switching_feasible_periods(ct, alphabet, periods=range(1, 53)):
    """Vigenere / Beaufort / variant Beaufort chosen freely at each position, key periodic with period p:
    feasible iff every residue class of crib positions shares a key value that some type allows at each position"""
    idx = {ch: n for n, ch in enumerate(alphabet)}
    need = {}
    for i, p in CRIB.items():
        x, y = idx[p], idx[ct[i]]
        need[i] = {(y - x) % 26, (y + x) % 26, (x - y) % 26}
    feasible, constrained = [], []
    for p in periods:
        classes = defaultdict(list)
        for i in CRIB:
            classes[i % p].append(i)
        if all(len(v) < 2 for v in classes.values()):
            feasible.append(p)
            continue
        constrained.append(p)
        if all(set.intersection(*(need[i] for i in v)) for v in classes.values()):
            feasible.append(p)
    return feasible, constrained


def shuffle_null(n, seed=1130):
    """share of shuffled K4 texts that pass some constrained p <= 24, and share that fail every constrained p"""
    rng = random.Random(seed)
    letters = list(K4)
    pass_small = fail_all = 0
    for _ in range(n):
        rng.shuffle(letters)
        ct = "".join(letters)
        ok_small = fail = True
        any_small = False
        for alph in (AZ, KA):
            feas, cons = switching_feasible_periods(ct, alph)
            if any(p in feas and p <= 24 for p in cons):
                any_small = True
            if any(p in feas for p in cons):
                fail = False
        pass_small += any_small
        fail_all += fail
    return pass_small / n, fail_all / n


def per_period_shuffle_rates(n, seed=1131):
    """for each period, the share of shuffled K4 texts for which free switching with a periodic key is feasible
    (either alphabet)"""
    rng = random.Random(seed)
    letters = list(K4)
    hits = defaultdict(int)
    for _ in range(n):
        rng.shuffle(letters)
        ct = "".join(letters)
        feas = set(switching_feasible_periods(ct, AZ)[0]) | set(switching_feasible_periods(ct, KA)[0])
        for p in feas:
            hits[p] += 1
    return {p: hits[p] / n for p in range(1, 53)}
