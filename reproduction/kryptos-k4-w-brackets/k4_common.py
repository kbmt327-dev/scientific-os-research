"""Shared inputs for the EP-0057 package: the public K4 ciphertext, the 24 public crib
letters, and additive tableau arithmetic.

K4 ciphertext: the 97-letter fourth section of Jim Sanborn's sculpture *Kryptos* (1990),
as transcribed publicly (Wikipedia "Kryptos"; Elonka Dunin, https://elonka.com/kryptos/).
It is quoted for research and commentary and is not covered by this package's license.

Cribs (0-indexed): EASTNORTHEAST at 21-33, BERLINCLOCK at 63-73, released by Sanborn in
2010 (BERLIN), 2014 (CLOCK) and 2020 (NORTHEAST, then EAST).
"""
K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")},
        **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
N = 97


def key_of(kind, alpha, c, p):
    ix = alpha.index
    return (ix(c) - ix(p)) % 26 if kind == "vig" else (ix(c) + ix(p)) % 26


def plain_of(kind, alpha, c, k):
    ix = alpha.index
    return alpha[(ix(c) - k) % 26] if kind == "vig" else alpha[(k - ix(c)) % 26]


def encrypt_plain(kind, alpha, pch, k):
    ix = alpha.index
    return alpha[(ix(pch) + k) % 26] if kind == "vig" else alpha[(k - ix(pch)) % 26]
