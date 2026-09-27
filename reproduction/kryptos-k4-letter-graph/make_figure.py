"""Draw the Note's figure: the crib letter graph (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-letter-graph.svg
"""
import math
import sys
from pathlib import Path

import k4_letter_graph as G

letters = sorted({x for p in G.PAIRS for x in p})
cx, cy, r = 300, 250, 190
pos = {ch: (cx + r * math.cos(2 * math.pi * k / len(letters) - math.pi / 2),
            cy + r * math.sin(2 * math.pi * k / len(letters) - math.pi / 2)) for k, ch in enumerate(letters)}
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="500" viewBox="0 0 1080 500">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.node{font-size:15px;font-weight:600}</style>',
       '<text x="540" y="28" text-anchor="middle" class="title">The 24 crib pairs as edges (plaintext letter to '
       'ciphertext letter): all 21 letters form one component</text>',
       '<defs><marker id="a" viewBox="0 0 10 10" refX="17" refY="5" markerWidth="6" markerHeight="6" '
       'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1f6f5c"/></marker></defs>']
for p, c in G.PAIRS:
    if p == c:
        x, y = pos[p]
        dx, dy = (x - cx) / r, (y - cy) / r
        out.append(f'<circle cx="{x + 20 * dx:.1f}" cy="{y + 20 * dy:.1f}" r="12" fill="none" stroke="#b03a2e" '
                   f'stroke-width="2"/>')
        continue
    (x1, y1), (x2, y2) = pos[p], pos[c]
    out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1f6f5c" '
               f'stroke-width="1.6" marker-end="url(#a)"/>')
for ch, (x, y) in pos.items():
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#fffdf8" stroke="#17202a"/>')
    out.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" class="node">{ch}</text>')
lines = ["Red loops: S to S (position 32) and K to K (position 73).",
         "",
         "A cipher whose every per-position map keeps a fixed",
         "partition of the alphabet must put this whole component",
         "in one block. Blocks under 21 letters are therefore",
         "impossible without crib errors.",
         "",
         "Treating the most helpful crib pairs as errors, the",
         "largest component shrinks to 12 letters (1 error),",
         "9 (2 errors) and 7 (3 errors).",
         "",
         "Named partitions need many errors: vowels/consonants 7,",
         "A-Z halves 8, QWERTY rows 12, Morse-length classes 18,",
         "5x5 Polybius rows 19."]
for k, line in enumerate(lines):
    out.append(f'<text x="580" y="{90 + 24 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
