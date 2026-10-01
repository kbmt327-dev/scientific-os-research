"""Draw the Note's figure: status of each block family with one phase shift, and what the later
constraints did to the 27 CM-Bifid settings (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-block-phase-shift.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "block-phase-shift-20260930.json").read_text(encoding="utf-8"))
ep = rec["EP-0169"]
ROWS = [
    ("Four-square, free cipher squares (960)", "closed", "K4 0; 94.6% of shuffles also fail everywhere"),
    ("Two-square, free squares (576)", "closed", "K4 0; 78.5% of shuffles also fail everywhere"),
    ("Keyword squares (7.15 million, 22.8 bit)", "closed", "K4 0 hits; shuffles 0/100"),
    ("Bifid, one free square (2,765)", "closed*", "K4 0; every shuffle fails too: no power"),
    ("CM-Bifid, two free squares (2,765)", "open", "K4 27 consistent; shuffle median 90 (post hoc)"),
    ("Fixed digraph chart C08 (97 / 92)", "open", "K4 88 / 83 consistent, like shuffles"),
]
COL = {"closed": "#1f6f5c", "closed*": "#6fa596", "open": "#c9a227"}
TXT = {"closed": "closed (logical)", "closed*": "closed, no power", "open": "undecidable"}
H = 500
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{H}" viewBox="0 0 1080 {H}">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.badge{font-size:12px;fill:#fffdf8;font-weight:600}'
       '.big{font-size:22px;font-weight:600}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Block ciphers on K4 without W, '
       'with one phase shift in the grouping</text>']
for k, (fam, st, note) in enumerate(ROWS):
    y = 50 + 32 * k
    out.append(f'<text x="30" y="{y + 17}" class="small">{fam}</text>')
    out.append(f'<rect x="340" y="{y + 2}" width="140" height="22" rx="4" fill="{COL[st]}"/>')
    out.append(f'<text x="410" y="{y + 17}" text-anchor="middle" class="badge">{TXT[st]}</text>')
    out.append(f'<text x="495" y="{y + 17}" class="small">{note}</text>')
# lower panel: CM-Bifid settings through later constraints
Y = 290
out.append(f'<text x="30" y="{Y}" class="small" font-weight="600">The 27 CM-Bifid settings under later '
           f'plaintext constraints</text>')
boxes = [
    (60, "27", "consistent with the cribs", ("shuffles: median 90", "P(count <= 27) = 0.12, post hoc")),
    (400, "6", "remain with word fragments (10.95 bit)", ("K4 survival 0.22, shuffles median 0.43", "2 of 20 shuffles at or below K4")),
    (740, "0", "remain with candidate sets (20.34 bit)", ("shuffles also lose every setting", "in 153 of 159")),
]
for i, (x, n, l1, l2) in enumerate(boxes):
    out.append(f'<rect x="{x}" y="{Y + 16}" width="290" height="112" rx="6" fill="none" stroke="#c9a227" stroke-width="2"/>')
    out.append(f'<text x="{x + 145}" y="{Y + 46}" text-anchor="middle" class="big">{n}</text>')
    out.append(f'<text x="{x + 145}" y="{Y + 70}" text-anchor="middle" class="small">{l1}</text>')
    for r, line in enumerate(l2):
        out.append(f'<text x="{x + 145}" y="{Y + 92 + 16 * r}" text-anchor="middle" class="small" fill="#5d6d7e">{line}</text>')
    if i < 2:
        out.append(f'<line x1="{x + 296}" y1="{Y + 64}" x2="{x + 334}" y2="{Y + 64}" stroke="#17202a" stroke-width="2"/>')
        out.append(f'<path d="M{x + 334},{Y + 58} L{x + 340},{Y + 64} L{x + 334},{Y + 70} Z" fill="#17202a"/>')
notes = ["Neither step separates K4 from shuffled ciphertexts significantly, so neither is evidence about K4.",
         "The last step is closed only if the candidate sets are assumed. Four free Four-square settings on the O-segment",
         "pairings stay untouched (4/4 remain with the fragments; the candidate sets cannot reach them)."]
for k, line in enumerate(notes):
    out.append(f'<text x="30" y="{Y + 160 + 18 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
