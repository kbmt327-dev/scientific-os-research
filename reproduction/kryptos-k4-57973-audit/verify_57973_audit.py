"""Rerun the audit of the reverse-Gromark-57973 claim and compare with the recorded result.

    python verify_57973_audit.py          # deterministic parts, a few minutes
    python verify_57973_audit.py --full   # also the two random controls (much longer)

Standard library only.  A rerun of the author's code, not an independent replication.
"""
import json
import random
import sys
from pathlib import Path

import k4_audit as a

HERE = Path(__file__).resolve().parent


def main():
    full = "--full" in sys.argv
    rec = json.loads((HERE / "results" / "audit-20260919.json").read_text(encoding="utf-8"))
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append(name)

    fwd, rev = [], []
    for n in range(100000):
        p = [int(c) for c in "%05d" % n]
        d = a.gromark(p)
        if a.sat(a.CT_CODES, d):
            fwd.append("%05d" % n)
        if a.sat(a.CT_CODES, d[::-1]):
            rev.append("%05d" % n)
    check("forward_compatible", fwd, rec["forward_compatible"]["primers"])
    check("reverse_compatible", rev, rec["reverse_compatible"]["primers"])

    tbl = {p: len(a.forced(a.CT_CODES, a.gromark([int(x) for x in p])[::-1])) for p in rev}
    check("max_forced", max(tbl.values()), rec["max_forced"])
    check("primers_at_max", sorted(p for p, v in tbl.items() if v == max(tbl.values())),
          rec["primers_at_max"])
    mask = a.gromark([5, 7, 9, 7, 3])[::-1]
    check("p57973_skeleton", a.skeleton(a.forced(a.CT_CODES, mask)), rec["p57973_skeleton"])
    check("p57973_config_count", list(a.config_count(a.CT_CODES, mask)),
          [rec["p57973_config_count"], rec["p57973_components"]])

    rc_map = {k: [a.CT_CODES[i] for i in v] for k, v in a.routes().items()}
    sat_n, best = 0, 0
    for base in (mask, a.gromark([5, 7, 9, 7, 3])):
        for sh in range(97):
            m = base[sh:] + base[:sh]
            for rc in rc_map.values():
                f = a.forced(rc, m)
                if f is not None:
                    sat_n += 1
                    best = max(best, len(f))
    rs = rec["route_sweep_57973"]
    check("route_sweep", [len(rc_map), sat_n, best],
          [rec["route_family_size"], rs["sat"], rs["max_forced_under_route_freedom"]])

    print(f"primers compatible: forward {len(fwd)}, reverse {len(rev)} of 100,000; "
          f"57973 reverse-compatible: {'57973' in rev}; max forced letters {max(tbl.values())}")
    print(f"route freedom for 57973: {sat_n} of {2 * 97 * len(rc_map)} (route, shift, direction) "
          f"combinations compatible; max forced letters {best}")

    if full:
        random.seed(0)
        n = rec["null_random_mask"]["trials"]
        hits = sum(1 for _ in range(n) if a.sat(a.CT_CODES, [random.randrange(10) for _ in range(97)]))
        check("null_random_mask", hits, rec["null_random_mask"]["compatible"])
        print(f"uniform random masks compatible: {hits} of {n} ({hits / n:.2e})")
        random.seed(1)

        def any_sat(p):
            dd = a.gromark(p)
            for base in (dd[::-1], dd):
                for sh in range(97):
                    m = base[sh:] + base[:sh]
                    if any(a.sat(rc, m) for rc in rc_map.values()):
                        return True
            return False
        k = rec["null_random_primer_admits_route"]["primers"]
        ok = sum(1 for _ in range(k) if any_sat([random.randrange(10) for _ in range(5)]))
        check("null_random_primer_admits_route", ok, rec["null_random_primer_admits_route"]["admitting"])
        print(f"random primers admitting a compatible route: {ok} of {k}")
    else:
        r = rec["null_random_mask"]
        print(f"(recorded, not rerun without --full) uniform random masks: {r['compatible']} of {r['trials']}; "
              f"random primers admitting a route: {rec['null_random_primer_admits_route']['admitting']} of "
              f"{rec['null_random_primer_admits_route']['primers']}")

    if fails:
        print("MISMATCH:", ", ".join(fails))
        return 1
    print("PASS: recorded audit reproduced (author rerun, not independent replication)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
