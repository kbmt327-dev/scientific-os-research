"""Verify the sealed EP-0028 AI cold-reader pilot record.

Checks sealed bytes, rebuilds the six reader prompts from the sealed template and
materials, and recomputes totals and prediction outcomes from the recorded scores.
It does not rerun the readers and does not rescore the free-text answers.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORKDIR = "<SCRATCH>/readers/{rid}"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    seal = json.loads((HERE / "seal.json").read_text(encoding="utf-8"))
    assert sha((HERE / "protocol.json").read_bytes()) == seal["protocol_sha256"], "protocol bytes differ from seal"
    contract = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    materials = {}
    for arm, rec in seal["materials"].items():
        raw = (HERE / "materials" / f"{arm}.md").read_bytes()
        assert sha(raw) == rec["prepared_sha256"], f"{arm}: material differs from seal"
        materials[arm] = raw.decode("utf-8")

    template = contract["reader_prompt"]
    b, c = template.index("PART B."), template.index("PART C.")
    for arm in ("BASE", "CURR"):
        for k in (1, 2, 3):
            rid = f"{arm}-{k}"
            text = template if arm == "CURR" else template[:b] + "PART B. Skip.\n\n" + template[c:]
            text = text.replace("{workdir}", WORKDIR.format(rid=rid)).replace("{material}", materials[arm])
            assert (HERE / "prompts" / f"{rid}.prompt.md").read_text(encoding="utf-8") == text, f"{rid}: prompt differs"
            assert (HERE / "answers" / f"{rid}.md").exists(), f"{rid}: answer missing"

    scores = json.loads((HERE / "scores.json").read_text(encoding="utf-8"))
    sealed = scores["sealed"]
    qs = [f"Q{i}" for i in range(1, 10)]
    for rid, row in sealed.items():
        assert sum(row[q] for q in qs) == row["total"], f"{rid}: total mismatch"
    col = lambda arm, q: sum(sealed[f"{arm}-{k}"][q] for k in (1, 2, 3))
    for arm in ("BASE", "CURR"):
        assert {q: col(arm, q) for q in qs} == scores["per_question_sealed"][arm], f"{arm}: per-question mismatch"
    outcome = {
        "P1": all(sealed[f"CURR-{k}"]["total"] >= 8 for k in (1, 2, 3)),
        "P2": col("BASE", "Q9") == 0 and col("CURR", "Q9") == 3,
        "P3": col("BASE", "Q6") <= 1 and col("CURR", "Q6") == 3,
        "P4": col("CURR", "Q3") >= 2,
        "P5": all(sealed[f"CURR-{k}"]["partB"] == "pass" for k in (1, 2, 3)),
    }
    for p, ok in outcome.items():
        assert scores["predictions"][p]["result"] == ("PASS" if ok else "FAIL"), f"{p}: recorded grade differs"
    print("sealed totals: " + ", ".join(f"{r} {v['total']}/9" for r, v in sealed.items()))
    print(f"predictions: {sum(outcome.values())}/5")
    print("cold-reader: PASS; record consistent; AI readers, author-scored, not human or independent")


if __name__ == "__main__":
    main()
