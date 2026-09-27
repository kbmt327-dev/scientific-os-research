"""Recompute the chart-free key-source test and the width-21 phenomenon (EP-0093) and compare with the record.

    python verify_key_sources.py

Standard library only, about 20 seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import statistics as st
import sys
from pathlib import Path

import k4_key_sources as S

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "key-sources-20260927.json").read_text(encoding="utf-8"))
    lc, ws = rec["latin_chart_no_error"], rec["width_scan"]
    kw, dg = S.keyword_sources(S.KEYWORDS), S.keyword_sources(S.DIGITS)
    a, b = S.decoy_keyword_null(lc["decoy_keyword_lists"]["n"]), S.decoy_digit_null(lc["decoy_digit_lists"]["n"])
    got = {"keyword_phases": len(kw), "keyword_passes": S.pass_count(kw), "digit_phases": len(dg),
           "digit_passes": S.pass_count(dg), "periods_passing_2_48": S.period_passes(),
           "decoy_keyword_lists": {"n": len(a), "median_passes": st.median(a), "share_with_0": sum(x == 0 for x in a) / len(a)},
           "decoy_digit_lists": {"n": len(b), "median_passes": st.median(b), "share_with_0": sum(x == 0 for x in b) / len(b)}}
    r = S.width_scan(ws["permutations"])
    got_ws = {"permutations": ws["permutations"], "k4_count_width21": r["k4_counts"][21],
              "p_width21": r["p_width21"], "p_scan_widths_2_48": r["p_scan"]}
    print(f"  Latin chart, no crib error: keywords {got['keyword_passes']}/{got['keyword_phases']}, digit strings "
          f"{got['digit_passes']}/{got['digit_phases']}, periods passing {got['periods_passing_2_48']}")
    print(f"  decoy keyword lists with 0 passes: {got['decoy_keyword_lists']['share_with_0']:.0%}")
    print(f"  width 21: {got_ws['k4_count_width21']} repeated vertical bigram types; P {got_ws['p_width21']} at that "
          f"width, {got_ws['p_scan_widths_2_48']} after scanning widths 2-48")
    bad = [k for k in got if got[k] != lc[k]] + [k for k in got_ws if got_ws[k] != ws[k]]
    if bad:
        print("FAIL:", ", ".join(bad))
        return 1
    print("PASS: key-source tests and the width scan reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
