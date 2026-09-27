"""Recompute the public part of EP-0135 Q1 and compare it with the recorded result.

    python verify_list_price.py

Checks: (1) the closed-form count against brute force on small random texts; (2) the
expected hits of K4's reading family for each public target list; (3) the union of the
public lists, bracketed against the recorded union that also contains the withheld K1-K3
word list; (4) that the only list word K4 produces is TOKIO, from the letter W.
Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import random
import sys
from itertools import combinations
from math import isclose
from pathlib import Path

import k4_list_price as P

HERE = Path(__file__).resolve().parent


def brute_force_check():
    rng = random.Random(7)
    for _ in range(120):
        n, m = rng.randrange(8, 30), rng.randrange(3, 6)
        seq = [rng.randrange(0, 10) for _ in range(rng.choice((m, m - 1)))]
        for gd in P.GAPDEF:
            sub = 1 if gd == "between" else 0
            for an in P.ANCHOR:
                bf = 0
                for v in combinations(range(n), m):
                    if an == "none":
                        g = [v[k] - v[k - 1] - sub for k in range(1, m)]
                    else:
                        pre = -1 if an == "start" else 0 if an == "zero" else v[-1] - n
                        g = [v[0] - pre - sub] + [v[k] - v[k - 1] - sub for k in range(1, m)]
                    bf += g == seq
                if bf != P.count_sets(seq, m, n, gd, an):
                    return False
    return True


def main():
    data = json.loads((HERE / "data" / "target-lists-public.json").read_text(encoding="utf-8"))
    rec = json.loads((HERE / "results" / "list-price-20260927.json").read_text(encoding="utf-8"))["Q1_K4_letters"]
    lists = {k: set(v) for k, v in data["lists"].items()}
    car = P.k4_carriers()
    fails = []
    if not brute_force_check():
        fails.append("closed form vs brute force")
    for name, words in lists.items():
        got = P.expected(sorted(words), car, 97)[0]
        if not isclose(got, rec["per_list"][name], rel_tol=1e-9):
            fails.append(f"per_list {name}: {got} vs {rec['per_list'][name]}")
        print(f"  {name:<10} {len(words):>5} words  E[hits] = {got:.4f}")
    union_pub = P.expected(sorted(set().union(*lists.values())), car, 97)[0]
    k123 = rec["per_list"]["k123"]
    print(f"  union of public lists E = {union_pub:.4f}; recorded union with the K1-K3 words E = "
          f"{rec['union']:.4f} (must lie in [{union_pub:.4f}, {union_pub + k123:.4f}])")
    if not union_pub <= rec["union"] <= union_pub + k123 + 1e-12:
        fails.append("union bracket")
    share = rec["per_list"]["worldclock"] / rec["union"]
    if not isclose(share, rec["worldclock_share"], rel_tol=1e-9):
        fails.append("worldclock share")
    hits = P.k4_hits(lists)
    print("  K4 hits:", sorted({(h[0], h[1], h[2]) for h in hits}))
    if sorted({(h[0], h[1]) for h in hits}) != [("W", "TOKIO")]:
        fails.append("K4 hits")
    if fails:
        print("FAIL:", "; ".join(fails))
        return 1
    print(f"PASS: EP-0135 Q1 public lists reproduce (World Clock share of the union {share:.1%})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
