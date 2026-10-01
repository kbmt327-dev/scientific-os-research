"""Draw the Note's figure: for each autokey lag L = 1..20, the fewest crib letters K4 must treat as errors over the
six tables (planted ciphers: 0).  Standard library only.

    python make_figure.py ../../content/assets/kryptos-k4-plaintext-keys.svg
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "plaintext-keys-20260930.json").read_text(encoding="utf-8"))
a = rec["ep0150_plaintext_autokey"]
best = {L: min(v["conflicts"] for k, v in a["cells"].items() if int(k.split()[2]) == L) for L in range(1, 21)}
X0, Y0, W, H = 90, 70, 900, 220
bw = W / 20
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="440" viewBox="0 0 1080 440">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Plaintext autokey with lag L: no cell fits the cribs '
       'without errors (best: 6 conflicting crib letters)</text>']
for t in range(0, 25, 5):
    y = Y0 + H - H * t / 24
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X0 + W}" y2="{y:.1f}" class="grid"/>')
    out.append(f'<text x="{X0 - 8}" y="{y + 4:.1f}" text-anchor="end" class="small">{t}</text>')
for L, v in best.items():
    x = X0 + bw * (L - 1)
    h = H * v / 24
    out.append(f'<rect x="{x + 6:.1f}" y="{Y0 + H - h:.1f}" width="{bw - 12:.1f}" height="{h:.1f}" fill="#5d6d7e"/>')
    out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H - h - 5:.1f}" text-anchor="middle" class="small">{v}</text>')
    out.append(f'<text x="{x + bw / 2:.1f}" y="{Y0 + H + 18}" text-anchor="middle" class="small">{L}</text>')
out.append(f'<text x="{X0 + W / 2}" y="{Y0 + H + 38}" text-anchor="middle" class="small">lag L (primer length)</text>')
out.append(f'<text x="{X0 - 60}" y="{Y0 - 14}" class="small">fewest conflicting crib letters over A-Z / KRYPTOS x '
           f'Vigenere / Beaufort / variant Beaufort</text>')
notes = [f"Planted autokey ciphers: 0 conflicts (24/24). Shuffled ciphertexts reach a minimum of 6 or fewer over the "
         f"120 cells in {a['P_shuffle_min_le_K4_min']:.0%} of {a['shuffles']:,} shuffles,",
         "so this is a logical refutation without carving errors, not evidence that K4 is further from autokey than random.",
         "Plaintext-indexed periodic key (EP-0179), shift tables: no pass at p <= 23 for the 60 listed sets; the 14 passes at p = 24 are",
         "the degenerate case with no extra step inside the cribs (shuffles: 20 on average). Arbitrary rows: at shuffle level."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{Y0 + H + 72 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
