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


CHECKS = {"gpu": gpu, "queue": queue, "human": human, "iaa": iaa}


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
