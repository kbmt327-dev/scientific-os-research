"""Draw the Note's figure: the 14 x 31 cells of chart #3 (K3, '?', K4; no letters), the two fold lines and the
six K4 cells they cross (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-chart3-folds.svg
"""
import json
import sys
from pathlib import Path

import k4_chart3_folds as F

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "chart3-folds-20260930.json").read_text(encoding="utf-8"))
S, X0, Y0 = 24, 150, 62
k4x, _ = F.fold_crossings()
cross = {F.k4_cell(i): i for i in k4x}
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="560" viewBox="0 0 1080 560">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.tiny{font-size:10px}'
       '.title{font-size:17px;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Chart #3 (14 x 31 cells): the two fold lines cross '
       'six K4 cells and 22 K3 cells</text>']
for k in range(F.ROWS * F.COLS):
    r, c = F.cell(k)
    x, y = X0 + (c - 1) * S, Y0 + (r - 1) * S
    if k < F.NK3:
        fill = "#d5dbe1"
    elif k == F.NK3:
        fill = "#ffffff"
    else:
        fill = "#f6d7a7"
    out.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{fill}" stroke="#ffffff" stroke-width="1"/>')
    if k == F.NK3:
        out.append(f'<text x="{x + S / 2}" y="{y + 16}" text-anchor="middle" class="small">?</text>')
    if (r, c) in cross:
        out.append(f'<rect x="{x + 2}" y="{y + 2}" width="{S - 4}" height="{S - 4}" fill="none" stroke="#b03a2e" stroke-width="2.5"/>')
        out.append(f'<text x="{x + S + 4}" y="{y + 16}" class="tiny" fill="#b03a2e">{cross[(r, c)]}</text>')
for r in range(1, F.ROWS + 1):
    out.append(f'<text x="{X0 - 8}" y="{Y0 + (r - 1) * S + 16}" text-anchor="end" class="tiny">{r}</text>')
for c in F.FOLD_COLUMNS:
    x = X0 + (c - 0.5) * S
    out.append(f'<line x1="{x}" y1="{Y0 - 10}" x2="{x}" y2="{Y0 + F.ROWS * S + 10}" stroke="#b03a2e" '
               f'stroke-width="2" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{x}" y="{Y0 + F.ROWS * S + 26}" text-anchor="middle" class="small" fill="#b03a2e">'
               f'fold, column {c}</text>')
lx = X0 + F.COLS * S + 30
for k, (fill, label) in enumerate((("#d5dbe1", "K3 (336 cells)"), ("#f6d7a7", "K4 (97 cells)"))):
    out.append(f'<rect x="{lx}" y="{Y0 + 30 * k}" width="18" height="18" fill="{fill}"/>')
    out.append(f'<text x="{lx + 26}" y="{Y0 + 30 * k + 14}" class="small">{label}</text>')
out.append(f'<rect x="{lx}" y="{Y0 + 60}" width="18" height="18" fill="none" stroke="#b03a2e" stroke-width="2.5"/>')
out.append(f'<text x="{lx + 26}" y="{Y0 + 74}" class="small">K4 cell on a fold</text>')
out.append(f'<text x="{lx + 26}" y="{Y0 + 92}" class="small">(0-based K4 position)</text>')
t = rec["restart_test"]["all six crossings"]
notes = ["Restarting one key at the six crossings puts five crib pairs at the same phase: "
         + ", ".join(f"{a}/{b}" for a, b in t["same_phase_groups"]) + ".",
         "A shift table (6 conventions) needs equal keys in each pair: K4 disagrees in all 5 (closed, for any key generator).",
         f"Arbitrary rows by phase: K4 has 0 conflicts, but so do {t['rows_shuffles_le']:.0%} of 100,000 shuffled "
         "ciphertexts (undecidable).",
         "Cell layout only; the public image is a typeset reconstruction, and every other mark lies outside the grid."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{Y0 + F.ROWS * S + 62 + 22 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
