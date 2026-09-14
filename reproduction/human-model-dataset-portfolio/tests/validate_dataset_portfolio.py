"""Validate the public EP-0005 dataset decision without downloading source data."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence" / "dataset-portfolio.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PARTICIPANT = re.compile(r"^P[0-9]{3}$")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["schema_version"] == "human-model-dataset-decision.v1"
    assert data["promotion_eligible"] is False
    assert data["prediction_registered"] is False

    decision = data["decision"]
    roles = {
        decision["development_dataset"],
        decision["external_validation_dataset"],
        decision["internal_load_stress_test"],
    }
    assert len(roles) == 3
    assert decision["canonical_representation"].startswith("NumPy arrays")
    assert "not a Human Model dependency" in decision["b3d_role"]

    manifest = data["participant_manifest"]
    partitions = {name: manifest[name] for name in ("development", "validation", "test")}
    assert {name: len(ids) for name, ids in partitions.items()} == {
        "development": 30,
        "validation": 10,
        "test": 10,
    }
    all_ids = [item for ids in partitions.values() for item in ids]
    assert len(all_ids) == len(set(all_ids)) == 50
    assert all(PARTICIPANT.fullmatch(item) for item in all_ids)
    assert manifest["upstream_test_participant_preserved"] == "P010"
    assert "P010" in partitions["test"]
    counts = manifest["source_label_counts_per_split"]
    assert counts == {
        "development": {"female": 15, "male": 15},
        "validation": {"female": 5, "male": 5},
        "test": {"female": 5, "male": 5},
    }
    assert manifest["source_size_bytes"] == 1554
    assert SHA256.fullmatch(manifest["source_sha256"])

    archive = data["bounded_archive_inspection"]
    assert archive["full_archive_downloaded"] is False
    assert archive["reused_tail_size_bytes"] == 1024 * 1024
    assert SHA256.fullmatch(archive["reused_tail_sha256"])
    assert archive["nonempty_carter_b3d_files"] == 610
    seed = archive["development_seed_candidate"]
    assert "/P008_split2/" in seed["member"]
    assert seed["downloaded"] is False
    assert re.fullmatch(r"[0-9a-f]{8}", seed["crc32"])

    required_guards = ("validation and test", "same raw source", "by participant")
    rules = "\n".join(data["leakage_rules"])
    assert all(guard in rules for guard in required_guards)
    not_executed = set(data["not_executed"])
    assert "model fitting" in not_executed
    assert "internal or external holdout evaluation" in not_executed

    print("human_dataset_portfolio: PASS; development=30 validation=10 test=10; no model or holdout result claimed")


if __name__ == "__main__":
    main()
