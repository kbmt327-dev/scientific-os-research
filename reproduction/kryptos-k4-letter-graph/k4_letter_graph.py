"""The crib's letter graph (EP-0101): one edge plaintext letter -> ciphertext letter for each
of K4's 24 public crib pairs.  If every per-position map of a cipher keeps a fixed partition
of the alphabet (each block to itself), every connected component of this graph must lie
inside one block.  Standard library only.
"""
from itertools import combinations

K4 = ("OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYP"
      "VTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR")
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
CRIB = {s + k: ch for s, w in CRIBS.items() for k, ch in enumerate(w)}
PAIRS = [(CRIB[i], K4[i]) for i in sorted(CRIB)]


def components(pairs):
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            x = parent[x]
        return x
    for p, c in pairs:
        parent[find(p)] = find(c)
    out = {}
    for x in list(parent):
        out.setdefault(find(x), set()).add(x)
    return sorted(out.values(), key=len, reverse=True)


def largest_after_dropping(k):
    """the smallest possible largest component once the k most helpful crib pairs are treated as errors"""
    return min(len(components([p for j, p in enumerate(PAIRS) if j not in drop])[0])
               for drop in combinations(range(len(PAIRS)), k))


def crossing_pairs(blocks):
    """crib pairs whose two letters fall in different blocks: the exact number of crib errors a fixed partition needs"""
    where = {ch: b for b, block in enumerate(blocks) for ch in block}
    return sum(1 for p, c in PAIRS if where.get(p) != where.get(c))


MORSE_LEN = {1: "ET", 2: "AIMN", 3: "DGKORSUW", 4: "BCFHJLPQVXYZ"}
PARTITIONS = {
    "Morse length classes": [MORSE_LEN[k] for k in (1, 2, 3, 4)],
    "Vowels (AEIOUY) / consonants": ["AEIOUY", "BCDFGHJKLMNPQRSTVWXZ"],
    "QWERTY rows": ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"],
    "A-Z halves": ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"],
    "A-Z parity": ["ACEGIKMOQSUWY", "BDFHJLNPRTVXZ"],
    "KRYPTOS alphabet halves": ["KRYPTOSABCDEF", "GHIJLMNQUVWXZ"],
    "Rows of a 5x5 Polybius square (I=J)": ["ABCDE", "FGHIK", "LMNOP", "QRSTU", "VWXYZ"],
}
# Named systems whose block sizes are known but whose letter assignment is free
SIZES_ONLY = {"3x3x3 cube, cubies by type (corner 8 / edge 12 / centre 6)": 12}


def word_restart_conflicts(segmentation, from_end):
    """pure word-restart keying: the row (any bijection) depends only on the position j inside the word.  Within
    one j, equal plaintext letters must give equal ciphertext letters and different ones different letters."""
    rows, bad = {}, []
    for start, words in segmentation:
        pos = start
        for w in words:
            for k, ch in enumerate(w):
                j = len(w) - 1 - k if from_end else k
                row = rows.setdefault(j, {})
                for p2, (c2, pos2) in row.items():
                    if (p2 == ch) != (c2 == K4[pos]):
                        bad.append((pos2, pos))
                row.setdefault(ch, (K4[pos], pos))
                pos += 1
    return bad


SEGMENTATIONS = {
    (a, b): [(21, ea), (63, bc)]
    for a, ea in {"EAST|NORTHEAST": ["EAST", "NORTHEAST"], "EASTNORTHEAST": ["EASTNORTHEAST"],
                  "EAST|NORTH|EAST": ["EAST", "NORTH", "EAST"]}.items()
    for b, bc in {"BERLIN|CLOCK": ["BERLIN", "CLOCK"], "BERLINCLOCK": ["BERLINCLOCK"]}.items()
}
