"""Draw the Note's figure: for each operator fixed by the carved layout, the number of crib pairs
that fall in one class and the share of 20,000 shuffles that are consistent (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-construction-ledger.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "construction-ledger-20260928.json").read_text(encoding="utf-8"))
ops = rec["operators"]
X0, W, Y0 = 430, 520, 64
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{Y0 + 36 * len(ops) + 110}" '
       f'viewBox="0 0 1080 {Y0 + 36 * len(ops) + 110}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">One arbitrary table per class fixed by the carved layout: '
       'K4 against 20,000 shuffles</text>']
yend = Y0 + 36 * len(ops)
for t in range(0, 101, 20):
    x = X0 + W * t / 100
    out.append(f'<line x1="{x:.1f}" y1="{Y0 - 8}" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">{t}%</text>')
for i, (name, r) in enumerate(ops.items()):
    y = Y0 + 36 * i
    share = r["null_consistent_fraction"]
    out.append(f'<text x="{X0 - 10}" y="{y + 16}" text-anchor="end" class="small">{name} '
               f'[{r["within_class_crib_pairs"]} pairs]</text>')
    out.append(f'<rect x="{X0}" y="{y + 2}" width="{max(W * share, 1.5):.1f}" height="22" fill="#9aa5b1"/>')
    k4 = "K4 fits" if r["consistent"] else "K4 fails"
    col = "#1f6f5c" if r["consistent"] else "#b03a2e"
    out.append(f'<text x="{X0 + W * share + 8:.1f}" y="{y + 18}" class="small">{share:.1%}  '
               f'<tspan fill="{col}">{k4}</tspan></text>')
notes = ["Grey bar: share of shuffled ciphertexts consistent with the cribs. [n pairs]: crib pairs that share a class,",
         "the only places a table can be broken. The row table fails at the first crib (E->F and E->G in one row); the",
         "column and fold tables fit, but so do 74-96% of shuffles: consistent, and uninformative (capacity)."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{yend + 50 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
