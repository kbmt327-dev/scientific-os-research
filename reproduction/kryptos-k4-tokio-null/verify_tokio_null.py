"""Recompute the exact null for the W-gap -> place-name reading and compare it with the
recorded result.

    python verify_tokio_null.py

Standard library only; well under a minute.  A rerun of the author's code, not an
independent replication.
"""
import io
import json
import sys
from contextlib import redirect_stdout
from math import isclose
from pathlib import Path

import k4_wgap_full

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "wgap-full-20260919.json").read_text(encoding="utf-8"))
    with redirect_stdout(io.StringIO()):
        got = json.loads(json.dumps(k4_wgap_full.main(write=False)))
    fails = [k for k in ("lengths", "targets", "nonzero", "k4_hits", "k4_family_size", "carriers")
             if got[k] != rec[k]]
    if set(got["per_target"]) != set(rec["per_target"]) or not all(
            isclose(got["per_target"][t], rec["per_target"][t], rel_tol=1e-12) for t in rec["per_target"]):
        fails.append("per_target")
    if not isclose(got["expected_hits_total"], rec["expected_hits_total"], rel_tol=1e-12):
        fails.append("expected_hits_total")
    total, rom = got["expected_hits_total"], got["per_target"].get("ROM", 0.0)
    print(f"K4 strings from the full reading family: {got['k4_family_size']}; place names hit: {got['k4_hits']}")
    print(f"exact P(at least one hit) <= {total:.3e}; ROM alone {rom:.3e} ({rom / total:.0%}); "
          f"without OSLO (added 1997) {total - got['per_target'].get('OSLO', 0.0):.3e}")
    if fails:
        print("MISMATCH:", ", ".join(fails))
        return 1
    print("PASS: recorded exact null reproduced (author rerun, not independent replication)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
