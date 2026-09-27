"""Draw the Note's figure: periods 1-96, testable and failed vs untestable (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-classical.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "classical-20260927.json").read_text(encoding="utf-8"))
testable = set(rec["testable_periods"])
cell, X0, Y0 = 40, 60, 70
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="470" viewBox="0 0 1080 470">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:11px}'
       '.title{font-size:17px;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Any periodic key, periods 1-96: what the 24 crib '
       'letters decide (8 alphabet and form settings)</text>']
for p in range(1, 97):
    r, c = divmod(p - 1, 24)
    x, y = X0 + c * cell, Y0 + r * (cell + 6)
    col = "#b03a2e" if p in testable else "#d9dde2"
    txt = "#fffdf8" if p in testable else "#17202a"
    out.append(f'<rect x="{x}" y="{y}" width="{cell - 4}" height="{cell - 4}" rx="4" fill="{col}"/>')
    out.append(f'<text x="{x + (cell - 4) / 2}" y="{y + 23}" text-anchor="middle" class="tiny" fill="{txt}">{p}</text>')
legend = [("#b03a2e", f"testable ({len(testable)} periods): two crib positions share a residue; "
                      f"the key fails in all 8 settings"),
          ("#d9dde2", f"not testable ({96 - len(testable)} periods): no two crib positions share a residue, "
                      f"so 24 letters decide nothing")]
for k, (col, text) in enumerate(legend):
    y = Y0 + 4 * (cell + 6) + 24 + 26 * k
    out.append(f'<rect x="{X0}" y="{y - 12}" width="16" height="16" rx="3" fill="{col}"/>')
    out.append(f'<text x="{X0 + 26}" y="{y + 1}" class="small">{text}</text>')
out.append(f'<text x="{X0}" y="{Y0 + 4 * (cell + 6) + 90}" class="small">Keys whose first differences are periodic '
           f'(progressive, Gromark type) also fail in every setting.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
