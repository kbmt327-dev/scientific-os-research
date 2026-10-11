"""Draw the Note's figure: for each family, K4's best crib mismatch count h next to the range of the best h over
shuffled K4 texts, with the pass region h <= 2 and the selection-free cover bound (standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-fixed-row-lists.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "fixed-row-lists-20261010.json").read_text(encoding="utf-8"))
r6, r7, r8, r9 = rec["ep0196"], rec["ep0197"], rec["ep0198"], rec["ep0208"]


def rng(h):
    v = [int(k) for k in h]
    return min(v), max(v)


def pct(x):
    return f"{100 * x:.1f}% of shuffles <= K4"


ROWS = [
    ("EP-0196 position in the word", f"{r6['N_all']:,} settings", rng(r6["null"]["min_all_hist"]),
     r6["k4"]["min_all"], 4, pct(r6["null"]["share_le_k4_all"])),
    ("EP-0197 phase from the fold line", f"{r7['N']:,} settings", rng(r7["null"]["min_hist"]),
     r7["k4"]["min"], 4, pct(r7["null"]["share_le_k4"])),
    ("EP-0198 letter behind the seam", f"{r8['N_main']:,} settings", rng(r8["null"]["min_hist"]),
     r8["k4"]["min"], 3, pct(r8["null"]["share_le_k4"])),
    ("EP-0198 + free column wobble", f"{r8['N_aux']:,} settings", rng(r8["null"]["min_aux_hist"]),
     r8["k4"]["min_aux"], 3, pct(r8["null"]["share_le_k4_aux"])),
    ("EP-0208 period band, layer 1", f"{r9['N']['L1']:,} settings (20 shuffles)",
     (min(r9["null"]["shuffle_mins"]["L1"]), max(r9["null"]["shuffle_mins"]["L1"])), r9["k4"]["L1"]["min"], 4,
     f"P = {r9['null']['P']['L1']:.2f}"),
    ("EP-0208 period band, layer 2", f"{r9['N']['L2']:,} settings (20 shuffles)",
     (min(r9["null"]["shuffle_mins"]["L2"]), max(r9["null"]["shuffle_mins"]["L2"])), r9["k4"]["L2"]["min"], 4,
     f"P = {r9['null']['P']['L2']:.2f}"),
]
X0, W, Y0, DY = 300, 600, 96, 46
ux = W / 24


def x(h):
    return X0 + ux * h


H = Y0 + DY * len(ROWS)
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="520" viewBox="0 0 1080 520">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}.muted{font-size:12px;fill:#566573}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Chart rows fixed to 12 word lists committed before K4: '
       'no setting reaches h &lt;= 2</text>',
       f'<rect x="{x(0):.1f}" y="{Y0 - 30}" width="{x(2) - x(0) + ux / 2:.1f}" height="{H - Y0 + 26}" fill="#fadbd8"/>',
       f'<text x="{x(0) + 4:.1f}" y="{Y0 - 36}" class="muted">pass: h &lt;= 2</text>']
for t in range(0, 25, 2):
    out.append(f'<line x1="{x(t):.1f}" y1="{Y0 - 30}" x2="{x(t):.1f}" y2="{H - 4}" class="grid"/>')
    out.append(f'<text x="{x(t):.1f}" y="{H + 12}" text-anchor="middle" class="small">{t}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{H + 32}" text-anchor="middle" class="small">best h over all settings '
           f'(crib positions out of 24 where the chart disagrees with K4)</text>')
out.append(f'<line x1="{x(4):.1f}" y1="{Y0 - 30}" x2="{x(4):.1f}" y2="{H - 4}" stroke="#7b241c" '
           f'stroke-width="1.5" stroke-dasharray="5 4"/>')
out.append(f'<text x="{x(4) + 4:.1f}" y="{Y0 - 18}" class="muted">cover bound: any row rule on these lists has h &gt;= 4 '
           f'(&gt;= 3 for EP-0198)</text>')
for k, (name, sub, (lo, hi), k4, floor, share) in enumerate(ROWS):
    y = Y0 + DY * k + 10
    out.append(f'<text x="{X0 - 12}" y="{y - 2}" text-anchor="end" class="small">{name}</text>')
    out.append(f'<text x="{X0 - 12}" y="{y + 13}" text-anchor="end" class="muted">{sub}</text>')
    out.append(f'<rect x="{x(lo) - 3:.1f}" y="{y - 6}" width="{x(hi) - x(lo) + 6:.1f}" height="12" rx="4" fill="#aeb6bf"/>')
    out.append(f'<path d="M{x(floor):.1f} {y - 9} l-5 -7 h10 z" fill="#7b241c"/>')
    out.append(f'<circle cx="{x(k4):.1f}" cy="{y}" r="6" fill="#d68910" stroke="#fffdf8" stroke-width="2"/>')
    out.append(f'<text x="{x(k4):.1f}" y="{y + 22}" text-anchor="middle" class="small">{k4}</text>')
    out.append(f'<text x="{X0 + W + 16}" y="{y + 4}" class="muted">{share}</text>')
ly = H + 58
out.append(f'<rect x="60" y="{ly - 9}" width="26" height="12" rx="4" fill="#aeb6bf"/>'
           f'<text x="94" y="{ly + 1}" class="small">shuffled K4 texts (2,000; 20 for EP-0208): range of their best h</text>')
out.append(f'<circle cx="583" cy="{ly - 3}" r="6" fill="#d68910"/>'
           f'<text x="595" y="{ly + 1}" class="small">K4: best h</text>')
out.append(f'<path d="M700 {ly - 9} l-5 -7 h10 z" transform="translate(0 10)" fill="#7b241c"/>'
           f'<text x="712" y="{ly + 1}" class="small">floor forced by the list cover</text>')
notes = [f"IC check without the crib (K4's IC {r6['ic_check']['k4_ic']:.4f} below the family's 1% quantile): "
         f"EP-0196 {r6['ic_check']['excluded']}/{r6['ic_check']['groups']} groups, EP-0197 "
         f"{r7['ic_check']['excluded']}/{r7['ic_check']['groups']}, EP-0198 {r8['ic_check']['excluded']}/"
         f"{r8['ic_check']['groups']}; not run for EP-0208.",
         "Logical refutations of the fixed-list versions only; K4 is not rarer than random. Arbitrary rows stay undecidable."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{ly + 30 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8", newline="\n")
