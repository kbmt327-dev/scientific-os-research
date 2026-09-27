"""Draw the Note's figure from results/enumerator-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-procedure-enumerator.svg
"""
import json
import sys
from math import log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "enumerator-20260927.json").read_text(encoding="utf-8"))
shapes = rec["shapes"]
total = sum(s["procedures"] for s in shapes)
crib = rec["crib_letters"] * log2(26)
X0, W, MAX = 330, 660, 120.0
rows = [(f'{s["shape"]}', log2(s["procedures"]), "#1f6f5c" if s["label"] == "different method" else "#9aa5b1")
        for s in shapes]
rows.append(("All shapes (EP-0119)", log2(total), "#c9a227"))
rows.append(("With a stacked shift mask (EP-0127)", 107.6, "#c9a227"))
h = 110 + 30 * len(rows) + 80
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{h}" viewBox="0 0 1080 {h}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Procedures in each part of the grammar (log2), '
       'against the 24 crib letters</text>']
yend = 52 + 30 * len(rows)
for t in range(0, 121, 20):
    x = X0 + W * t / MAX
    out.append(f'<line x1="{x:.1f}" y1="48" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">{t}</text>')
for i, (label, v, col) in enumerate(rows):
    y = 52 + 30 * i
    out.append(f'<text x="{X0 - 10}" y="{y + 16}" text-anchor="end" class="small">{label}</text>')
    out.append(f'<rect x="{X0}" y="{y}" width="{W * v / MAX:.2f}" height="20" fill="{col}"/>')
    out.append(f'<text x="{X0 + W * v / MAX + 6:.1f}" y="{y + 15}" class="small">{v:.1f}</text>')
xc = X0 + W * crib / MAX
out.append(f'<line x1="{xc:.1f}" y1="44" x2="{xc:.1f}" y2="{yend}" stroke="#b03a2e" stroke-width="2"/>')
out.append(f'<text x="{xc - 6:.1f}" y="{yend + 36}" text-anchor="end" class="small" fill="#b03a2e">'
           f'crib: 24 letters = {crib:.1f} bits</text>')
out.append(f'<text x="55" y="{yend + 58}" class="small">Green: different methods (not one shifted chart). '
           f'Grey: K1-K3 variants.</text>')
out.append(f'<text x="55" y="{yend + 78}" class="small">Every part gave 0 procedures that fit K4; '
           f'shuffled ciphertexts also gave 0.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
