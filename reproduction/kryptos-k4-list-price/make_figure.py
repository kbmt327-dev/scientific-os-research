"""Draw the Note's figure from results/list-price-20260927.json (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-list-price.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "list-price-20260927.json").read_text(encoding="utf-8"))
q1 = rec["Q1_K4_letters"]
rows = [
    ("World Clock place names (146), the list EP-0011 used", q1["per_list"]["worldclock"], "#1f6f5c"),
    ("English words (2,541)", q1["per_list"]["english"], "#9aa5b1"),
    ("Words of the K1-K3 plaintexts (107)", q1["per_list"]["k123"], "#9aa5b1"),
    ("Compass points (24)", q1["per_list"]["compass"], "#9aa5b1"),
    ("Theme words (135)", q1["per_list"]["themes"], "#9aa5b1"),
    ("National capitals (207)", q1["per_list"]["capitals"], "#9aa5b1"),
    ("Union of the six lists (3,036 words)", q1["union"], "#c9a227"),
]
X0, W, MAX = 470, 520, 0.06
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="480" viewBox="0 0 1080 480">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Expected chance hits of K4\'s W-gap reading family, '
       'by target list (closed form)</text>']
for t in (0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06):
    x = X0 + W * t / MAX
    out.append(f'<line x1="{x:.1f}" y1="52" x2="{x:.1f}" y2="{52 + 36 * len(rows)}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{70 + 36 * len(rows)}" text-anchor="middle" class="small">{t:g}</text>')
for i, (label, v, col) in enumerate(rows):
    y = 58 + 36 * i
    out.append(f'<text x="{X0 - 10}" y="{y + 17}" text-anchor="end" class="small">{label}</text>')
    out.append(f'<rect x="{X0}" y="{y}" width="{max(W * v / MAX, 1):.2f}" height="24" fill="{col}"/>')
    out.append(f'<text x="{X0 + W * v / MAX + 6:.1f}" y="{y + 17}" class="small">{v:.4f}</text>')
q4 = rec["Q4_cipher_side"]
yb = 120 + 36 * len(rows)
lines = [f'World Clock share of the union: {q1["worldclock_share"]:.1%}.',
         f'Adding the other markers in K1-K4 (question marks, section boundaries, misspellings, ...): '
         f'{q4["hits"]:.0f} hit (TOKIO) against {q4["expected"]:.3f} expected, P(at least 1) = {q4["p_ge"]:.2f}.',
         'The public rerun recomputes every list except the K1-K3 words, which this site does not publish.']
for k, line in enumerate(lines):
    out.append(f'<text x="55" y="{yb + 22 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
