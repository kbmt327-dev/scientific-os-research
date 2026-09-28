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
    # EP-0145: an independent third photo, a rubbing (auxiliary) and Antipodes (one-sided)
    e = rec["ep0145"]
    third = json.loads((HERE / "results" / "yar-measurements-third-photo-20260928.json").read_text(encoding="utf-8"))
    for ph in third["photos"]:
        r = Y.yar(ph["cipher"])
        if ph["id"] == e["third_photo"]["id"]:
            got = [round(float(r["row14_resid_P"][k]), 3) for k in sorted(r["row14_resid_P"])]
            print(f"  third photo {ph['id']}: {r['class']} (read as 'none'); Y, A, R "
                  f"{got[1]:+.3f}, {got[2]:+.3f}, {got[4]:+.3f} P; in-plate pitch about "
                  f"{e['third_photo']['in_plate_pitch_px']} px < 100 -> combined verdict stays undecided")
            if r["class"] != e["third_photo"]["class"] or got != e["third_photo"]["row14_resid_P"]:
                bad.append("third photo")
        else:
            print(f"    sensitivity {ph['id']}: {r['class']}")
            if r["class"] != e["third_photo"]["sensitivity"][ph["id"]]:
                bad.append(ph["id"])
    ndy = json.loads((HERE / "results" / "yar-rubbing-ndy-20260928.json").read_text(encoding="utf-8"))
    c = ndy["centres14"]
    (x1, y1), (x2, y2), (x3, y3) = c["1"], c["2"], c["3"]
    res = (y3 - (y1 + (y2 - y1) * (x3 - x1) / (x2 - x1))) / ndy["pitch_px"]
    print(f"  rubbing NDY (auxiliary): Y {res:+.3f} P against the line through N and D (up)")
    if round(res, 3) != e["rubbing_ndy"]["Y_resid_P"]:
        bad.append("rubbing")
    ant = json.loads((HERE / "results" / "yar-measurements-antipodes-20260928.json").read_text(encoding="utf-8"))
    r = Y.yar(ant["photos"][0]["cipher"])
    yar_a = [round(float(r["row14_resid_P"][k]), 3) for k in Y.YAR]
    print(f"  Antipodes: {r['class']}; Y, A, R {yar_a} P (no lift; says nothing about Kryptos)")
    if r["class"] != e["antipodes"]["class"] or yar_a != e["antipodes"]["YAR_resid_P"]:
        bad.append("Antipodes")
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: residuals and classes reproduce; with the third photo the YAR shift is still undecided (direction up)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
