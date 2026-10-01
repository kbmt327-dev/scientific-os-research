"""Draw the Note's figure: for each test, the expected number of chance passes (log scale) and what K4 gave
(standard library only).

    python make_figure.py ../../content/assets/kryptos-k4-w-morse-digits.svg
"""
import json
import sys
from math import log10
from pathlib import Path

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "results" / "w-morse-digits-20260930.json").read_text(encoding="utf-8"))
w, g = rec["w_null_index"], rec["w_null_index"]["text_keys"]["gates"]
rows = [("W skipped: procedure enumerator, up to 2 errors", w["enumerator_e2"]["chance_total"], "K4 0", "closed"),
        ("W skipped: text key, shift table", g["none"]["chance"], "K4 0", "closed"),
        ("W skipped: text key + mask on plaintext", g["sigma"]["chance"], "K4 0", "closed"),
        ("W skipped: text key + mask on ciphertext", g["tau"]["chance"], "K4 0", "closed"),
        ("W skipped: text key + masks on both sides", g["double"]["chance_K4"], f"K4 {g['double']['K4']:,}", "undecidable"),
        ("Morse mask + free substitution", rec["morse_mask"]["sigma_variant"]["chance"], "K4 0", "closed"),
        ("Digit-wise addition, 22 fixed strings", rec["digit_addition"]["chance"], "K4 0", "closed")]
LO, HI = -32, 5
X0, W, Y0, H = 350, 540, 70, 40


def xs(v):
    return X0 + W * (log10(v) - LO) / (HI - LO)


out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="480" viewBox="0 0 1080 480">',
       '<rect width="100%" height="100%" fill="#fffdf8"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#17202a}.small{font-size:13px}'
       '.title{font-size:17px;font-weight:600}.grid{stroke:#d9dde2;stroke-width:1}</style>',
       '<text x="540" y="30" text-anchor="middle" class="title">Expected chance passes for each test, and what K4 gave</text>']
yend = Y0 + H * len(rows)
for t in range(LO, HI + 1, 4):
    x = xs(10.0 ** t)
    out.append(f'<line x1="{x:.1f}" y1="{Y0 - 8}" x2="{x:.1f}" y2="{yend}" class="grid"/>')
    out.append(f'<text x="{x:.1f}" y="{yend + 18}" text-anchor="middle" class="small">1e{t}</text>')
x1 = xs(1.0)
out.append(f'<line x1="{x1:.1f}" y1="{Y0 - 8}" x2="{x1:.1f}" y2="{yend}" stroke="#7d8a96" stroke-dasharray="4,3"/>')
out.append(f'<text x="{x1:.1f}" y="{Y0 - 14}" text-anchor="middle" class="small">1 expected pass</text>')
for i, (name, v, k4, verdict) in enumerate(rows):
    y = Y0 + H * i + H / 2
    col = "#b03a2e" if verdict == "undecidable" else "#2e5c8a"
    out.append(f'<text x="{X0 - 12}" y="{y + 4}" text-anchor="end" class="small">{name}</text>')
    out.append(f'<line x1="{X0}" y1="{y}" x2="{xs(v):.1f}" y2="{y}" stroke="#c9d1d9" stroke-width="2"/>')
    out.append(f'<circle cx="{xs(v):.1f}" cy="{y}" r="6" fill="{col}"/>')
    out.append(f'<text x="{X0 + W + 14}" y="{y + 4}" class="small" fill="{col}">{k4}: {verdict}</text>')
notes = ["Dot: expected number of settings that pass the crib by chance (closed form; for the two-sided mask, the",
         "ciphertext's own random-key pass rate). Every test far left of 1 gave K4 0, as did its shuffles, so those",
         "are logical refutations, not evidence that K4 is rarer than random. The two-sided mask passes about as many",
         "settings as chance; its English stage was not run. The pure Morse mask needs no search (excluded by logic)."]
for k, line in enumerate(notes):
    out.append(f'<text x="60" y="{yend + 50 + 20 * k}" class="small">{line}</text>')
out.append('</svg>')
Path(sys.argv[1]).write_text("".join(out), encoding="utf-8")
