"""Verify the sealed EP-0027 lexical self-containment audit.

Rescores the baseline snapshots and the current public articles with the sealed
rubric and runner. Lexical presence only; no reader comprehension is tested.
"""
from pathlib import Path
import hashlib
import json

from public_self_containment import score, sha

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    contract = json.loads((HERE / "protocol.json").read_text(encoding="utf-8-sig"))
    seal = json.loads((HERE / "seal.json").read_text(encoding="utf-8-sig"))
    assert sha(HERE / "protocol.json") == seal["protocol_sha256"], "protocol bytes differ from seal"
    assert sha(HERE / "public_self_containment.py") == seal["runner_sha256"], "runner bytes differ from seal"
    for stage, root, articles in (
        ("baseline", HERE, {lang: f"baseline-snapshot/{lang}.md" for lang in contract["articles"]}),
        ("remediation", ROOT, contract["articles"]),
    ):
        recorded = json.loads((HERE / f"{stage}.json").read_text(encoding="utf-8"))
        fresh = score(dict(contract, articles=articles), root)
        for lang, rec in recorded["languages"].items():
            got = fresh["languages"][lang]
            digest = got["sha256"]
            if stage == "remediation":
                # Remediation was scored on LF bytes; Windows checkouts may use CRLF.
                raw = (root / articles[lang]).read_bytes().replace(b"\r\n", b"\n")
                digest = hashlib.sha256(raw).hexdigest()
            assert digest == rec["sha256"], f"{stage}/{lang}: article bytes differ from record"
            assert [c["pattern_matches"] for c in got["criteria"]] == [c["pattern_matches"] for c in rec["criteria"]], f"{stage}/{lang}: score differs"
            if stage == "baseline":
                assert rec["sha256"] == contract["baseline_sha256"][lang], f"baseline/{lang}: snapshot is not the sealed baseline"
        print(f"{stage}: " + ", ".join(f"{k} {v['passed']}/{v['total']}" for k, v in fresh["languages"].items()))
    print("self-containment: PASS; lexical audit only, no reader tested; not independent replication")


if __name__ == "__main__":
    main()
