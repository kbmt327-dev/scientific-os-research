"""Recompute the YAR residuals and classes of EP-0139 from the recorded pixel measurements and
compare with the record.

    python verify_yar_photo.py

Needs numpy; under a second.  The measurements are the author's readings of two public photos
(pixel numbers only, no image is stored); rerunning the statistic does not re-measure the
photos.  A rerun of the author's code, not an independent replication.
"""
import json
import sys
from pathlib import Path

import k4_yar as Y

HERE = Path(__file__).resolve().parent


def main():
    meas = json.loads((HERE / "results" / "yar-measurements-20260927.json").read_text(encoding="utf-8"))
    rec = json.loads((HERE / "results" / "yar-result-20260927.json").read_text(encoding="utf-8"))
    bad, classes = [], []
    for ph in meas["photos"]:
        r = Y.yar(ph["cipher"])
        want = rec["photos"][ph["id"]]
        got = [round(float(r["row14_resid_P"][k]), 4) for k in sorted(r["row14_resid_P"])]
        print(f"  {ph['id']} ({ph['side']}): pitch {r['P_px']:.0f} px, sigma {r['sigma_P']:.3f} P, "
              f"threshold {r['T_P']:.2f} P -> {r['class']}")
        print("    row-14 residuals (P, columns 0-10): " + ", ".join(f"{v:+.3f}" for v in got))
        yar = [got[k] for k in Y.YAR]
        cm = [-x * r["P_px"] / want["in_plate_pitch_px"] * rec["pitch_cm"] for x in yar]
        print(f"    Y, A, R: {yar[0]:+.3f}, {yar[1]:+.3f}, {yar[2]:+.3f} P  = raised about "
              f"{min(cm):.1f}-{max(cm):.1f} cm (in-plate pitch {want['in_plate_pitch_px']} px = {rec['pitch_cm']} cm)")
        if got != want["row14_resid_P"] or r["class"] != want["class"]:
            bad.append(ph["id"])
        classes.append(r["class"])
    v = Y.verdict(classes)
    print(f"  across photos: {v}")
    if v != rec["verdict_yar"]:
        bad.append("verdict")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: residuals and classes reproduce; the two photos disagree, so the YAR shift stays undecided")
    return 0


if __name__ == "__main__":
    sys.exit(main())
