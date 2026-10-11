"""Public machines for the K4 Note on published wirings and disks (EP-0193 T2, EP-0203, EP-0206, EP-0207,
EP-0209, EP-0215).  Standard library + numpy.  No sculpture text other than the K4 ciphertext.

Wirings: Crypto Museum, "Enigma wiring" (the values the author's code used).
  commercial (EP-0132): Enigma D/K, Swiss-K, Railway; rotors I-III and their reflector (UKW)
  Enigma I  (EP-0193):  rotors I-V, reflectors A, B, C; the 30 machines are each 3-subset of I-V x one reflector

Machine (EP-0132's simulator, no plugboard).  Letter index x, entry-wheel table E (contact of each letter):
  y = E[x]; through R, M, L at offsets (c, b, a): y -> W[(y + o) mod 26] - o; reflector at position uq;
  back through L, M, R with the inverse wirings; output = the letter whose contact is y.
  Stepping before every letter (lever/pawl, middle-rotor double step):
      atR = (phR + sR) % 26 == 0, atM = (phM + sM) % 26 == 0;  if atM: M and L step  elif atR: M steps;  R steps.
  Offsets: a = oL + sL, b = oM + sM, c = oR + sR (window minus ring).  The turnover phases phR, phM (26^2) absorb
  the notch letters and the ring settings.
Entry wheel readings of the commercial QWERTZ wheel (EP-0203, EP-0209):
  QW   contact = QWERTZ.index(letter)            (key Q at contact A)
  QWi  contact = AZ.index(QWERTZ[letter])        (the reading EP-0132 and EP-0193 used)
  id   contact = letter index

With a free substitution sigma before the machine, C_i = E_i(sigma(P_i)) and E_i is an involution, so
sigma(P_i) = E_i(C_i): the 24 values must be equal for equal crib letters and different for different ones.
"""
import itertools
import math
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "kryptos-k4-layout-transposition"))
import k4_layout_pi as LP                                           # noqa: E402  (the Pi set of EP-0185 / EP-0186)

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
N = 97
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
POS = sorted(CRIB)
PT = [CRIB[i] for i in POS]
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
QWERTZ = "QWERTZUIOASDFGHJKPYXCVBNML"
PI_DIGEST = "493992dde23a3fb132a3d197cf95db77016e130283fbbcd95826b9140b029a40"

COMMERCIAL = {
    "DK": ("LPGSZMHAEOQKVXRFYBUTNICJDW", "SLVGBTFXJQOHEWIRZYAMKPCNDU", "CJGDPSHKTURAWZXFMYNQOBVLIE",
           "IMETCGFRAYSQBZXWLHKDVUPOJN"),
    "SWISSK": ("PEZUOHXSCVFMTBGLRINQJWAYDK", "ZOUESYDKFWPCIQXHMVBLGNJRAT", "EHRVXGAOBQUSIMZFLYNWKTPDJC",
               "IMETCGFRAYSQBZXWLHKDVUPOJN"),
    "RAIL": ("JGDQOXUSCAMIFRVTPNEWKBLZYH", "NTZPSFBOKMWRCJDIVLAEYUXHGQ", "JVIUBHTCDYAKEQZPOSGXNRMWFL",
             "QYHOGNECVPUZTFDJAXWMKISRBL"),
}
ENIGMA1_ROTORS = {"I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
                  "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
                  "V": "VZBRGITYUPSDNHLXAWMJQOFECK"}
ENIGMA1_UKW = {"A": "EJMZALYXVBWFCRQUONTSPIKHGD", "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
               "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}
ENIGMA1_NOTCH = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z"}   # window letter at which the next rotor turns

MACHINES = dict(COMMERCIAL)
for _trio in itertools.combinations(ENIGMA1_ROTORS, 3):
    for _u in ENIGMA1_UKW:
        MACHINES["EnigmaI %s-%s-%s/%s" % (_trio + (_u,))] = tuple(ENIGMA1_ROTORS[r] for r in _trio) + (ENIGMA1_UKW[_u],)
ORDERS = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]       # (left, middle, right)
PUBLIC_WIRINGS = [w for m in ("DK", "SWISSK", "RAIL") for w in COMMERCIAL[m][:3]] + list(ENIGMA1_ROTORS.values())


def perm(s):
    return np.array([AZ.index(c) for c in s], dtype=np.int64)


READINGS = {"QW": np.array([QWERTZ.index(c) for c in AZ], dtype=np.int64),
            "QWi": np.array([AZ.index(QWERTZ[x]) for x in range(26)], dtype=np.int64),
            "id": np.arange(26, dtype=np.int64)}


class Machine:
    def __init__(self, name, order, reading):
        m = MACHINES[name]
        trio = [perm(m[k]) for k in range(3)]
        self.W = [trio[order[0]], trio[order[1]], trio[order[2]]]          # left, middle, right
        self.Wi = [np.argsort(w) for w in self.W]
        self.U = perm(m[3])
        self.E = READINGS[reading]
        self.Ei = np.argsort(self.E)

    def letter(self, x, a, b, c, uq):
        """one letter through entry, R, M, L, reflector, L^-1, M^-1, R^-1, entry^-1 (offsets may be arrays)"""
        WL, WM, WR = self.W
        y = self.E[x]
        y = (WR[(y + c) % 26] - c) % 26
        y = (WM[(y + b) % 26] - b) % 26
        y = (WL[(y + a) % 26] - a) % 26
        y = (self.U[(y + uq) % 26] - uq) % 26
        y = (self.Wi[0][(y + a) % 26] - a) % 26
        y = (self.Wi[1][(y + b) % 26] - b) % 26
        y = (self.Wi[2][(y + c) % 26] - c) % 26
        return self.Ei[y]


def steps(phR, phM, n):
    """(sL, sM, sR) after the stepping before each letter 0..n-1 (EP-0132)"""
    sL = sM = sR = 0
    out = []
    for _ in range(n):
        atR = (phR + sR) % 26 == 0
        atM = (phM + sM) % 26 == 0
        if atM:
            sM += 1
            sL += 1
        elif atR:
            sM += 1
        sR += 1
        out.append((sL, sM, sR))
    return out


def real_steps(win, notch, n):
    """an independent real-machine model: windows (L, M, R) and notch letters (M, R) as letter indices; before every
    key press the pawls act on the current windows; returns the window positions (L, M, R) for each letter"""
    L_, M_, R_ = win
    out = []
    for _ in range(n):
        m_at = M_ == notch[0]
        r_at = R_ == notch[1]
        if m_at:
            M_ = (M_ + 1) % 26
            L_ = (L_ + 1) % 26
        elif r_at:
            M_ = (M_ + 1) % 26
        R_ = (R_ + 1) % 26
        out.append((L_, M_, R_))
    return out


def encipher(mach, text_idx, oL, oM, oR, uq, phR, phM):
    st = steps(phR, phM, len(text_idx))
    return [int(mach.letter(x, (oL + sL) % 26, (oM + sM) % 26, (oR + sR) % 26, uq))
            for x, (sL, sM, sR) in zip(text_idx, st)]


def test_vectors():
    """Enigma I, rotors I-II-III, reflector B, rings A, no plugboard: AAA + AAAAA -> BDZGO, ADU + AAAA -> EQIB.
    Run twice: through the abstract stepping (phases from the windows) and through real_steps."""
    mach = Machine("EnigmaI I-II-III/B", (0, 1, 2), "id")
    out = []
    for pos, text in (("AAA", "AAAAA"), ("ADU", "AAAA")):
        w = [AZ.index(c) for c in pos]
        phR = (w[2] - AZ.index(ENIGMA1_NOTCH["III"])) % 26
        phM = (w[1] - AZ.index(ENIGMA1_NOTCH["II"])) % 26
        a = "".join(AZ[y] for y in encipher(mach, [AZ.index(c) for c in text], w[0], w[1], w[2], 0, phR, phM))
        wins = real_steps(w, (AZ.index(ENIGMA1_NOTCH["II"]), AZ.index(ENIGMA1_NOTCH["III"])), len(text))
        b = "".join(AZ[int(mach.letter(AZ.index(ch), L_, M_, R_, 0))] for ch, (L_, M_, R_) in zip(text, wins))
        out.append((a, b))
    return out


# ------------------------------------------------------------------ the exact sigma test (EP-0132)
GROUP = [sorted(set(PT)).index(c) for c in PT]                       # crib letter -> group 0..12


def sigma_consistent(vals):
    """vals[j] = E_t(C_j) at crib position j; True if letter -> value is a consistent injection"""
    seen, used = {}, {}
    for g, v in zip(GROUP, vals):
        if g in seen:
            if seen[g] != v:
                return False
        else:
            if v in used:
                return False
            seen[g] = v
            used[v] = g
    return True


def slice_scan(mach, ct, phR, phM, oL0=None, times=None):
    """the settings of one (machine, order, reading, phR, phM): every (oL, oM, oR, uq) = 26^4, or every
    (oM, oR, uq) = 26^3 when oL is fixed to oL0.  Returns the number of sigma passes and the passing settings.
    times[j] = machine time of crib position j (default: the position itself)."""
    times = POS if times is None else times
    st = steps(phR, phM, max(times) + 1)
    if oL0 is None:
        g = np.indices((26, 26, 26, 26)).reshape(4, -1)
    else:
        g3 = np.indices((26, 26, 26)).reshape(3, -1)
        g = np.vstack([np.full(g3.shape[1], oL0), g3])
    oL, oM, oR, uq = g
    vals = []
    for j, t in enumerate(times):
        sL, sM, sR = st[t]
        vals.append(mach.letter(AZ.index(ct[POS[j]]), (oL + sL) % 26, (oM + sM) % 26, (oR + sR) % 26, uq))
    V = np.stack(vals)                                                # 24 x 26^4
    ok = np.ones(V.shape[1], dtype=bool)
    rep = {}
    for j, gr in enumerate(GROUP):
        if gr in rep:
            ok &= V[j] == V[rep[gr]]
        else:
            rep[gr] = j
    R = np.sort(V[list(rep.values())], axis=0)                       # 13 representatives must be distinct
    ok &= np.all(R[1:] != R[:-1], axis=0)
    idx = np.flatnonzero(ok)
    return len(idx), [tuple(int(x) for x in g[:, k]) for k in idx]


# ------------------------------------------------------------------ closed forms
def crib_multiplicities():
    return {c: PT.count(c) for c in sorted(set(PT))}


def p_sigma_uniform(drop=()):
    """P(the remaining crib positions admit a consistent injection | values uniform on 26) (EP-0132 / EP-0192 T3)"""
    rem = [j for j in range(24) if j not in drop]
    k = len({GROUP[j] for j in rem})
    q = Fraction(1, 26 ** (len(rem) - k))
    for i in range(k):
        q *= Fraction(26 - i, 26)
    return q


def p_sigma_le(h):
    """union bound used in the records: sum over drop sets D, |D| <= h, of P(the rest is consistent)"""
    return sum(p_sigma_uniform(D) for k in range(h + 1) for D in itertools.combinations(range(24), k))


def p_mismatch_le(k, n=24, p=Fraction(1, 26)):
    """P(h <= k) for a machine without a free part: each crib position matches with probability 1/26"""
    return sum(math.comb(n, h) * (1 - p) ** h * p ** (n - h) for h in range(k + 1))


# ------------------------------------------------------------------ Pi (EP-0186) and forced positions
def pis():
    ps = LP.pi_set()
    assert len(ps) == 104 and LP.digest(ps) == PI_DIGEST
    return ps


def forced(ct, src):
    """crib positions whose aligned cipher letter equals the crib letter (src = None: identity).  A machine that never
    maps a letter to itself (reflector Enigma without sigma; M-94 with read-off g != 0) must mismatch there.  The
    same for order A (C = Pi(M(P))) and order B (C = M(Pi(P))): the cipher letter is C[inv[i]] in both."""
    inv = list(range(N)) if src is None else LP.inverse(list(src))
    return [i for i in POS if ct[inv[i]] == CRIB[i]]


def m94_count(src, order, slist):
    """EP-0207: sum over phases s of 25^L * 25!/(25-R)!, L = 25-letter lines and R = residues the crib touches"""
    inv = LP.inverse(list(src))
    tot = 0
    for s in slist:
        ts = [i if order == "A" else inv[i] for i in POS]
        L = len({(t - s) // 25 for t in ts})
        R = len({(t - s) % 25 for t in ts})
        tot += 25 ** L * (math.factorial(25) // math.factorial(25 - R))
    return tot
