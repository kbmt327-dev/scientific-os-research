"""Draw the Note's figure: letters per carved row against the row's mean letter width (Arial as
a stand-in), with K4's four rows marked (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-production-traces.svg
"""
import json
import sys
from pathlib import Path

import k4_production_traces as T

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "production-traces-20260928.json").read_text(encoding="utf-8"))
n = rec["row_lengths"]
m = rec["row_mean_advance_width"]["arial"]
X0, Y0, W, H = 110, 60, 820, 260
mlo, mhi = min(m) - 5, max(m) + 5
nlo, nhi = 28.5, 33.5


def px(v):
    return X0 + W * (v - mlo) / (mhi - mlo)


def py(v):
    return Y0 + H * (nhi - v) / (nhi - nlo)


rho = T.spearman(n, m)
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 0 1080 440">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Rows with wider letters hold fewer letters: '
       'the 28 carved cipher rows</text>']
for v in range(29, 34):
    out.append(f'<line x1="{X0}" y1="{py(v):.1f}" x2="{X0 + W}" y2="{py(v):.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 10}" y="{py(v) + 4:.1f}" text-anchor="end" class="small">{v}</text>')
t = int(mlo // 10 * 10 + 10)
while t < mhi:
    out.append(f'<line x1="{px(t):.1f}" y1="{Y0}" x2="{px(t):.1f}" y2="{Y0 + H}" class="grid"/>')
    out.append(f'<text x="{px(t):.1f}" y="{Y0 + H + 18}" text-anchor="middle" class="small">{t}</text>')
    t += 10
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 40}" text-anchor="middle" class="small">mean letter width in the row '
           f'(Arial advance, 1/1000 em)</text>')
out.append(f'<text x="30" y="{Y0 + H / 2}" class="small" transform="rotate(-90 30 {Y0 + H / 2})" '
           f'text-anchor="middle">letters in the row</text>')
for i, (a, b) in enumerate(zip(m, n)):
    k4 = i >= 24
    col = "#b03a2e" if k4 else ("#1f6f5c" if i < 14 else "#9aa5b1")
    out.append(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="{7 if k4 else 6}" fill="{col}" fill-opacity="0.85"/>')
leg = [("#1f6f5c", "upper plate (K1, K2)"), ("#9aa5b1", "lower plate (K3)"), ("#b03a2e", "rows holding K4 (24-27)")]
for k, (col, lab) in enumerate(leg):
    out.append(f'<circle cx="{X0 + 10 + 250 * k}" cy="{Y0 + H + 66}" r="6" fill="{col}"/>')
    out.append(f'<text x="{X0 + 22 + 250 * k}" y="{Y0 + H + 71}" class="small">{lab}</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 98}" class="small">Spearman rho = {rho:.2f} (re-breaking the same text at '
           f'random: mean -0.02, P &lt;= 1e-5). K4\'s rows sit on the same trend: the layout follows letter widths,</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 118}" class="small">not plaintext words or a cipher grid, even in K1-K3 where '
           f'the methods are known.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
