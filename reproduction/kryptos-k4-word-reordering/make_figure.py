"""Draw the Note's figure: search size in bits for each reordering test, against the crib
(standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-word-reordering.svg
"""
import json
import sys
from math import log2
from pathlib import Path

import k4_word_reordering as W

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "word-reordering-20260928.json").read_text(encoding="utf-8"))
base = log2(rec["procedures"])
rows = [("Procedures alone (EP-0119)", base, "#9aa5b1"),
        ("+ 8 fixed rules (21 crib assignments)", base + log2(rec["fixed_rule_assignments"]), "#1f6f5c"),
        ("+ any order inside words, S2 (NORTH split)", base + log2(W.arrangements("S2")), "#1f6f5c"),
        ("+ any order inside words, S1 (hint spans)", base + log2(W.arrangements("S1")), "#1f6f5c"),
        ("+ any order inside words, S3 (crib = word)", base + log2(W.arrangements("S3")), "#1f6f5c")]
X0, W_, MAX = 330, 660, 120.0
yend = 52 + 30 * len(rows)
h = yend + 100
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{h}" viewBox="0 0 1080 {h}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Letters reordered inside each word, then substituted: '
       'size of each test (log2)</text>']
for t in range(0, 121, 20):
    x = X0 + W_ * t / MAX
    out.append(f'<line x1="{x:.1f}" y1="48" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">{t}</text>')
for i, (label, v, col) in enumerate(rows):
    y = 52 + 30 * i
    out.append(f'<text x="{X0 - 10}" y="{y + 16}" text-anchor="end" class="small">{label}</text>')
    out.append(f'<rect x="{X0}" y="{y}" width="{W_ * v / MAX:.2f}" height="20" fill="{col}"/>')
    out.append(f'<text x="{X0 + W_ * v / MAX + 6:.1f}" y="{y + 15}" class="small">{v:.1f}</text>')
xc = X0 + W_ * W.CRIB_BITS / MAX
out.append(f'<line x1="{xc:.1f}" y1="44" x2="{xc:.1f}" y2="{yend}" stroke="#b03a2e" stroke-width="2"/>')
out.append(f'<text x="{xc - 6:.1f}" y="{yend + 36}" text-anchor="end" class="small" fill="#b03a2e">'
           f'crib: 24 letters = {W.CRIB_BITS:.1f} bits</text>')
out.append(f'<text x="55" y="{yend + 60}" class="small">Every test stays below the crib, so a true procedure would '
           f'stand out. K4 gave 0 in all of them, in both orders (reorder then substitute, and the reverse);</text>')
out.append(f'<text x="55" y="{yend + 80}" class="small">two shuffled ciphertexts gave 0 as well; planted controls '
           f'76/76 were found.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
