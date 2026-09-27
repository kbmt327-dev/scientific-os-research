"""The classical families closed from the crib's keystream (EP-0032) and from K4's letter counts (EP-0018-0020).

Fix an alphabet and a form, and the 24 crib letters give 24 exact keystream values (Vigenere and variant both fix
c - p, Beaufort fixes c + p).  Four alphabets (A-Z and the keyed KRYPTOS, PALIMPSEST, ABSCISSA) x two forms = 8
settings.  From these values alone:
  * any periodic key: positions congruent mod p must carry equal values -- decided for every p at once;
  * progressive / Gromark-type keys: first differences periodic -- the same check on differences;
  * a running key of English text: the 24 values judged against English letter frequencies.
And any transposition alone keeps K4's letter counts, which are far flatter than English.
Standard library only.
"""
import random
from math import log

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, .00153, .00772, .04025, .02406,
           .06749, .07507, .01929, .00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074]


def keyed(word):
    seen = []
    for ch in word + AZ:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


ALPHABETS = {"A-Z": AZ, "KRYPTOS": keyed("KRYPTOS"), "PALIMPSEST": keyed("PALIMPSEST"), "ABSCISSA": keyed("ABSCISSA")}
FORMS = ("c-p", "c+p")


def keystream(alph, form, ct=K4):
    n = {ch: k for k, ch in enumerate(alph)}
    sign = -1 if form == "c-p" else 1
    return {i: (n[ct[i]] + sign * n[CRIB[i]]) % 26 for i in POS}


def keystream_text(alph, form):
    k = keystream(alph, form)
    return "".join(alph[k[i]] for i in POS[:13]), "".join(alph[k[i]] for i in POS[13:])


def testable_periods(max_p=96):
    return [p for p in range(1, max_p + 1) if len({i % p for i in POS}) < len(POS)]


def periodic_survivors(k, max_p=96):
    out = []
    for p in testable_periods(max_p):
        vals = {}
        if all(vals.setdefault(i % p, k[i]) == k[i] for i in POS):
            out.append(p)
    return out


def difference_survivors(k, max_q=96):
    """first differences d_i = k_(i+1) - k_i (both in the crib) must be periodic with period q"""
    d = {i: (k[i + 1] - k[i]) % 26 for i in POS if i + 1 in k}
    out = []
    for q in range(1, max_q + 1):
        if len({i % q for i in d}) == len(d):
            continue
        vals = {}
        if all(vals.setdefault(i % q, d[i]) == d[i] for i in d):
            out.append(q)
    return out


def english_loglik(values):
    return sum(log(ENGLISH[v]) for v in values)


def english_running_key_p(k, alph, n, seed=320):
    """share of 24-letter keys drawn from English frequencies (read in this alphabet) whose likelihood is as low
    as K4's"""
    idx = [AZ.index(alph[v]) for v in (k[i] for i in POS)]
    target = english_loglik(idx)
    rng = random.Random(seed)
    low = sum(english_loglik(rng.choices(range(26), weights=ENGLISH, k=24)) <= target for _ in range(n))
    return low / n


def ic(s):
    m = len(s)
    return sum(s.count(c) * (s.count(c) - 1) for c in set(s)) / (m * (m - 1))


def transposition_p(n, seed=321):
    """share of 97-letter English samples (independent letters) as flat as K4; a transposition keeps K4's counts"""
    rng = random.Random(seed)
    t = ic(K4)
    return sum(ic("".join(rng.choices(AZ, weights=ENGLISH, k=97))) <= t for _ in range(n)) / n
