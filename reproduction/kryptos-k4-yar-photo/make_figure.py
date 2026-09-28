"""Draw the Note's figure: height residuals of the 11 measured letters of carved row 14 in two
public photos, with the pre-registered threshold (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-yar-photo.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "yar-result-20260927.json").read_text(encoding="utf-8"))
LABEL = {3: "Y", 4: "A", 5: "H", 6: "R"}
X0, Y0, W, H = 120, 70, 860, 240
LO, HI = -0.16, 0.10


def ypos(v):
    return Y0 + H * (HI - v) / (HI - LO)


out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="420" viewBox="0 0 1080 420">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">How far each letter of carved row 14 sits from its '
       'row line (negative = raised), two public photos</text>']
for t in (-0.15, -0.10, -0.05, 0.0, 0.05, 0.10):
    out.append(f'<line x1="{X0}" y1="{ypos(t):.1f}" x2="{X0 + W}" y2="{ypos(t):.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{ypos(t) + 4:.1f}" text-anchor="end" class="small">{t:+.2f}</text>')
for t in (-0.08, 0.08):
    out.append(f'<line x1="{X0}" y1="{ypos(t):.1f}" x2="{X0 + W}" y2="{ypos(t):.1f}" stroke="#b03a2e" '
               f'stroke-dasharray="6 4"/>')
out.append(f'<text x="{X0 + W - 4}" y="{ypos(-0.08) - 6:.1f}" text-anchor="end" class="small" fill="#b03a2e">'
           f'threshold 0.08 of the row pitch</text>')
step = W / 11
styles = [("highsmith-LOC-2011631531", "#1f6f5c", "Highsmith (back, larger image): class 'intended'"),
          ("gillogly-ciphermidleft", "#9aa5b1", "Gillogly (front): same direction, below threshold")]
for j, (pid, col, label) in enumerate(styles):
    vals = rec["photos"][pid]["row14_resid_P"]
    for k, v in enumerate(vals):
        x = X0 + step * (k + 0.5) + (j * 2 - 1) * 7
        out.append(f'<circle cx="{x:.1f}" cy="{ypos(v):.1f}" r="6" fill="{col}"/>')
    out.append(f'<circle cx="{X0 + 10 + 430 * j}" cy="{Y0 + H + 58}" r="6" fill="{col}"/>')
    out.append(f'<text x="{X0 + 22 + 430 * j}" y="{Y0 + H + 63}" class="small">{label}</text>')
for k in range(11):
    x = X0 + step * (k + 0.5)
    lab = LABEL.get(k, "")
    out.append(f'<text x="{x:.1f}" y="{Y0 + H + 22}" text-anchor="middle" class="small">col {k}'
               f'{" " + lab if lab else ""}</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 92}" class="small">Only Y, A and R are raised (about 1.5-1.9 cm in the '
           f'larger photo); H between them and the rows above and below do not move.</text>')
out.append(f'<text x="{X0}" y="{Y0 + H + 112}" class="small">The two photos give different pre-registered classes, '
           f'so the verdict is undecided.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
