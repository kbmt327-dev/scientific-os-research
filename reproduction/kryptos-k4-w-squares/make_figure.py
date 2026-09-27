"""Draw the Note's figure: status of each square family (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-w-squares.svg
"""
import sys
from pathlib import Path

ROWS = [
    ("Keyword squares: Four-square, Two-square, Bifid (925,600)", "closed", "0 settings fit; shuffles 0"),
    ("Four-square, two free cipher squares", "closed", "inconsistent in every pairing; shuffles 0/2,000"),
    ("Two-square, free squares (72 settings)", "closed", "one crib digraph kills each convention"),
    ("Bifid, one free square", "closed*", "finds 96-100% of plants; K4 at shuffle level"),
    ("CM-Bifid, two free squares (79 block settings)", "closed", "inconsistent; 14% of shuffles also fail"),
    ("Playfair, then a shift mask", "closed", "0 settings; chance ≤ 6.6e-10"),
    ("Shift mask, then Playfair", "closed", "doubled ciphertext pairs (5 / 2 / 3)"),
    ("Keyword squares with a shift mask before or after", "closed", "0; expected false hits 0.00015"),
    ("2-D shifts, rotations, mirrors on a free 5x5 grid", "closed", "where decidable; long periods open"),
    ("Two free squares with long periods, free per-position symmetries", "open", "not decidable from the cribs"),
]
COL = {"closed": "#1f6f5c", "closed*": "#6fa596", "open": "#c9a227"}
TXT = {"closed": "closed (logical)", "closed*": "closed (with power)", "open": "not decidable"}
h = 80 + 34 * len(ROWS) + 40
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{h}" viewBox="0 0 1080 {h}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.badge{font-size:12px;fill:#fffdf8;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">K4 with the Ws removed (92 letters, 25 types), '
       'enciphered with 5x5 squares</text>']
for k, (fam, st, note) in enumerate(ROWS):
    y = 60 + 34 * k
    out.append(f'<text x="30" y="{y + 17}" class="small">{fam}</text>')
    out.append(f'<rect x="560" y="{y + 2}" width="150" height="22" rx="4" fill="{COL[st]}"/>')
    out.append(f'<text x="635" y="{y + 17}" text-anchor="middle" class="badge">{TXT[st]}</text>')
    out.append(f'<text x="725" y="{y + 17}" class="small">{note}</text>')
out.append(f'<text x="30" y="{h - 16}" class="small">"Logical" means no setting reproduces the cribs; random ciphertext '
           f'usually fails the same way, so K4 is not shown to be rarer than random.</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
