#!/usr/bin/env python3
"""Run bounded public reproduction checks without claiming independent replication."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"failed in {cwd}: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def gpu() -> None:
    root = ROOT / "reproduction" / "gpu-scheduling"
    pred = root / "predictions" / "PRED-001.json"
    # The sealed digest was computed from the repository's LF byte stream.
    # Normalize checkout line endings so the check is stable on Windows.
    digest = hashlib.sha256(pred.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    expected = "dd977a92c0edf7472a6190d35dab7baa22743375627ca326be354d4c4eda4b01"
    assert digest == expected, (digest, expected)
    grading = json.loads((root / "results" / "E1_grading.json").read_text(encoding="utf-8"))
    assert len(grading) == 10 and sum(row["pass"] for row in grading) == 7
    print("gpu: sealed prediction hash and 7/10 grading verified")


def gpu_phase() -> None:
    root = ROOT / "reproduction" / "gpu-scheduling-phase"
    # Both digests were computed from the repository's LF byte stream.
    expected = {
        "PRED-002": "d726c5a701367f3be0bff47eba10267ee5fcd43bc4b830ec70c97a22477ed8a0",
        "PRED-003": "2f3b1808d806e9af888acaa77a7e00f7e9af86a13d58e42ac75e514a91157d05",
        "PRED-004": "7ef0f5b21d46318e6008a1be3021e9c1ffbefbe3fb23e959c3cffa7268048cbe",
        "PRED-005": "fe3e27d68d27c5c8eb9fb6633d133e17fd6c4ba09158ab80d901dc4630ccb902",
    }
    for name, want in expected.items():
        # read_text() applies universal newlines, so this is the LF byte
        # stream the digest was sealed over, whatever the checkout style.
        text = (root / "predictions" / f"{name}.json").read_text(encoding="utf-8")
        got = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert got == want, (name, got, want)
    e2e3 = json.loads((root / "results" / "E2E3_grading.json").read_text(encoding="utf-8"))
    assert e2e3["n_total"] == 10 and e2e3["n_pass"] == 5
    # The as-run detector is kept so the post-hoc detector change stays auditable.
    assert e2e3["n_pass_asrun"] == 4
    e4 = json.loads((root / "results" / "E4_grading.json").read_text(encoding="utf-8"))
    assert e4["n_total"] == 10 and e4["n_pass"] == 7
    starved = {r["id"] for r in e4["results"] if r["pass"]}
    assert {"R1", "R3", "R6"} <= starved, starved
    # Real-trace measurement. No whole-pool job appears in any Philly virtual
    # cluster, which is what demoted the practical claim of the previous study.
    traces = json.loads((root / "results" / "E5_traces.json").read_text(encoding="utf-8"))
    vcs = traces["philly_vc_capacity"]
    assert len(vcs) == 11, len(vcs)
    assert all(vc["p_ge_peak"] == 0.0 for vc in vcs), vcs
    assert max(vc["max_k_over_peak"] for vc in vcs) < 1.0
    e5 = json.loads((root / "results" / "E5_grading.json").read_text(encoding="utf-8"))
    assert e5["n_total"] == 10 and e5["n_pass"] == 5
    # The decisive prediction was named against the project's own claim, and
    # passing it is what triggered the pre-registered demotion.
    e6 = json.loads((root / "results" / "E6_grading.json").read_text(encoding="utf-8"))
    assert e6["n_total"] == 10 and e6["n_pass"] == 9
    assert e6["t4_passed"] is True
    assert e6["r_safe"] == 0.75
    print("gpu-phase: PRED-002/003/004/005 digests and 5/7/5/9 gradings verified; "
          "no whole-pool job in any measured virtual cluster")


def queue() -> None:
    root = ROOT / "reproduction" / "simulation-worlds"
    output = run([sys.executable, "analysis/a11_verify_against_truth.py"], root)
    assert output.count("MATCH") == 5
    assert "max |error| = 2.29%" in output
    print("queue: five structural matches and revealed parameter check verified")


def human() -> None:
    root = ROOT / "reproduction" / "human-model-contract"
    output = run([sys.executable, "tests/validate_contract_v0_2.py"], root)
    result = json.loads(output)
    assert result["all_passed"] is True
    assert len(result["negative_controls"]) == 7
    print("human: contract checks and seven negative controls verified")


def iaa() -> None:
    root = ROOT / "reproduction" / "badminton-biomechanics"
    output = run([sys.executable, "analysis/ep0008_power_simulation.py", "--iterations", "1000", "--seed", "20260913"], root)
    result = json.loads(output)
    assert len(result["scenarios"]) == 168
    assert result["status"] == "sensitivity_only_not_final_sample_size"
    print("iaa: 168-scenario bounded power sensitivity rerun verified")


CHECKS = {"gpu": gpu, "gpu-phase": gpu_phase, "queue": queue,
          "human": human, "iaa": iaa}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", choices=["all", *CHECKS], default="all")
    args = parser.parse_args()
    selected = CHECKS if args.quick == "all" else {args.quick: CHECKS[args.quick]}
    for check in selected.values():
        check()
    print(f"Reproduction checks passed: {len(selected)} package(s). This is not independent replication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
