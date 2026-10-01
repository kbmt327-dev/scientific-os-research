"""Recompute the key lower bound and the window conflicts (EP-0091) and compare with the record.
Later check (EP-0152): the share of uniform 97-letter strings with an IC at or below K4's (20,000 draws).

    python verify_key_bound.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from math import isclose
from pathlib import Path

import k4_key_bound as K

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "key-bound-20260927.json").read_text(encoding="utf-8"))
    fails = []
    if not isclose(K.ic(K.K4), rec["k4_ic"]):
        fails.append("IC")
    print(f"  K4 index of coincidence {K.ic(K.K4):.4f} (English about 0.066, uniform 0.038)")
    for m, want in rec["share_ic_at_or_below_k4"].items():
        got = K.free_rows_share(int(m), rec["trials_per_m"])
        print(f"  m = {int(m):>2} rows ({K.log2(int(m)):.2f} bits): share with IC <= K4 {got:.4f}")
        if got != want:
            fails.append(f"m={m}")
    wc = {k: list(v) for k, v in K.window_conflicts().items()}
    print(f"  window shapes with a crib conflict: {sum(v is not None for v in wc.values())} of {len(wc)}")
    if wc != rec["window_conflicts"]:
        fails.append("windows")
    # later check (EP-0152, 2026-09-30): only the uniform model needs no English text, so only it is rerun
    ic2 = json.loads((HERE / "results" / "ic-recheck-20260930.json").read_text(encoding="utf-8"))
    u = K.uniform_share(20000)
    want = ic2["models"]["uniform letters (uniform key)"]["p_ic_le_k4"]
    print(f"  uniform 97-letter strings with IC <= K4: {u:.4f} (recorded {want}; English-key models recorded: "
          f"{ic2['models']['English + English text as key (running key)']['p_ic_le_k4']}, not rerun)")
    if abs(u - want) > 0.01:
        fails.append("uniform IC")
    if fails:
        print("FAIL:", ", ".join(fails))
        return 1
    print("PASS: a flat IC needs about 8 free rows (3 bits per position); every window map <= 4 conflicts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
