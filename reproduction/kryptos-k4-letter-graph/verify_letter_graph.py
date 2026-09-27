"""Recompute the crib letter graph results (EP-0101) from K4 and the public cribs.

    python verify_letter_graph.py

Standard library only, a few seconds.  A rerun of the author's code, not an independent
replication.
"""
import json
import sys
from pathlib import Path

import k4_letter_graph as G

HERE = Path(__file__).resolve().parent


def main():
    rec = json.loads((HERE / "results" / "letter-graph-20260927.json").read_text(encoding="utf-8"))
    fails = []
    comps = G.components(G.PAIRS)
    comp = "".join(sorted(comps[0]))
    print(f"  components: {len(comps)}; the crib's {len(comp)} letters {comp}")
    if comp != rec["component"] or len(comps) != rec["n_components"]:
        fails.append("component")
    for k, want in rec["largest_after_dropping"].items():
        got = G.largest_after_dropping(int(k))
        print(f"  largest component after treating the {k} most helpful crib pair(s) as errors: {got}")
        if got != want:
            fails.append(f"drop {k}")
    for name, want in rec["crossing_pairs"].items():
        got = G.crossing_pairs(G.PARTITIONS[name])
        print(f"  {name:<40} needs {got:>2} crib errors")
        if got != want:
            fails.append(name)
    for key, s in G.SEGMENTATIONS.items():
        name = f"{key[0]} + {key[1]}"
        got = {"from_start": len(G.word_restart_conflicts(s, False)),
               "from_end": len(G.word_restart_conflicts(s, True))}
        print(f"  word restart, {name:<34} conflicts from start {got['from_start']}, from end {got['from_end']}")
        if got != rec["word_restart_conflicts"][name]:
            fails.append(name)
    if [list(p) for p in G.PAIRS if p[0] == p[1]] != rec["self_encryptions"]:
        fails.append("self-encryptions")
    if fails:
        print("FAIL:", ", ".join(fails))
        return 1
    print("PASS: crib letter graph, partition error counts and word-restart conflicts reproduce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
