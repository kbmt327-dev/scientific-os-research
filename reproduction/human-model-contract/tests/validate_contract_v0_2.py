"""Validate the Human Model Commons Contract v0.2 bundle.

This is a contract/reference validator. It does not read B3D numerical frames or
execute Nimble/OpenSim. Run from any working directory with Python 3.11+ and
jsonschema installed.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "model_schema": ROOT / "contracts" / "human-model-spec.schema.json",
    "observation_schema": ROOT / "contracts" / "observation-spec.v0.2.schema.json",
    "adapter_schema": ROOT / "contracts" / "adapter-spec.v0.2.schema.json",
    "validation_schema": ROOT / "contracts" / "validation-case.v0.2.schema.json",
    "model": ROOT / "examples" / "iaa-limited-human-model-spec.example.json",
    "observation": ROOT / "examples" / "addbiomechanics-subject40-observation-spec.v0.2.json",
    "adapter": ROOT / "examples" / "subject40-to-iaa-adapter-spec.v0.2.json",
    "validation": ROOT / "examples" / "addbiomechanics-subject40-validation-case.v0.2.json",
}


class ContractError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        return json.load(stream)


def assert_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ContractError(f"duplicate {label}")


def validate_schema(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        location = "/".join(str(part) for part in errors[0].absolute_path) or "<root>"
        raise ContractError(f"{label} schema error at {location}: {errors[0].message}")


def validate_bundle(bundle: dict[str, dict[str, Any]]) -> list[str]:
    model = bundle["model"]
    observation = bundle["observation"]
    adapter = bundle["adapter"]
    case = bundle["validation"]

    validate_schema(model, bundle["model_schema"], "model")
    validate_schema(observation, bundle["observation_schema"], "observation")
    validate_schema(adapter, bundle["adapter_schema"], "adapter")
    validate_schema(case, bundle["validation_schema"], "validation")

    coordinate_spaces = {
        item["coordinate_space_id"] for item in observation["coordinate_spaces"]
    }
    coordinate_space_ids = [
        item["coordinate_space_id"] for item in observation["coordinate_spaces"]
    ]
    channel_ids = [item["channel_id"] for item in observation["channels"]]
    pass_ids = [item["processing_pass_id"] for item in observation["processing_passes"]]
    frame_ids = [item["frame_id"] for item in model["coordinate_frames"]]
    blocks = model["dynamics_interface"]["input_blocks"] + model["dynamics_interface"]["output_blocks"]
    block_ids = [item["block_id"] for item in blocks]

    assert_unique(coordinate_space_ids, "coordinate_space_id")
    assert_unique(channel_ids, "channel_id")
    assert_unique(pass_ids, "processing_pass_id")
    assert_unique(frame_ids, "model frame_id")
    assert_unique(block_ids, "model block_id")

    for channel in observation["channels"]:
        if channel["coordinate_space_id"] not in coordinate_spaces:
            raise ContractError(f"unknown coordinate space: {channel['coordinate_space_id']}")
        if channel["processing_pass_id"] not in pass_ids:
            raise ContractError(f"unknown processing pass: {channel['processing_pass_id']}")

    expected_observation_ref = "examples/addbiomechanics-subject40-observation-spec.v0.2.json"
    expected_model_ref = "examples/iaa-limited-human-model-spec.example.json"
    expected_adapter_ref = "examples/subject40-to-iaa-adapter-spec.v0.2.json"
    if case["observation_ref"] != expected_observation_ref:
        raise ContractError("ValidationCase observation_ref does not resolve to bundle observation")
    if case["model_ref"] != expected_model_ref:
        raise ContractError("ValidationCase model_ref does not resolve to bundle model")
    if case["adapter_ref"] != expected_adapter_ref:
        raise ContractError("ValidationCase adapter_ref does not resolve to bundle adapter")
    if adapter["source_observation_ref"] != case["observation_ref"]:
        raise ContractError("AdapterSpec source_observation_ref differs from ValidationCase")
    if adapter["target_model_ref"] != case["model_ref"]:
        raise ContractError("AdapterSpec target_model_ref differs from ValidationCase")

    for channel_id in case["inputs"] + case["targets"]:
        if channel_id not in channel_ids:
            raise ContractError(f"ValidationCase channel does not resolve: {channel_id}")

    for mapping in adapter["mappings"]:
        if mapping["source_channel_id"] not in channel_ids:
            raise ContractError(f"adapter source channel does not resolve: {mapping['source_channel_id']}")
        source_channel = next(
            item for item in observation["channels"]
            if item["channel_id"] == mapping["source_channel_id"]
        )
        if mapping["source_coordinate_space_id"] not in coordinate_spaces:
            raise ContractError(
                f"adapter coordinate space does not resolve: {mapping['source_coordinate_space_id']}"
            )
        if mapping["source_coordinate_space_id"] != source_channel["coordinate_space_id"]:
            raise ContractError("adapter coordinate space differs from source channel")
        missing_blocks = set(mapping["target_block_ids"]) - set(block_ids)
        if missing_blocks:
            raise ContractError(f"adapter target blocks do not resolve: {sorted(missing_blocks)}")
        missing_frames = set(mapping["target_frame_ids"]) - set(frame_ids)
        if missing_frames:
            raise ContractError(f"adapter target frames do not resolve: {sorted(missing_frames)}")

    check_ids = [item["check_id"] for item in observation["source_consistency_checks"]]
    warning_ids = [item["warning_id"] for item in observation["source_consistency_warnings"]]
    assert_unique(check_ids, "source consistency check_id")
    assert_unique(warning_ids, "source warning_id")
    warnings = set(warning_ids)
    required_warning_ids = {
        item["warning_id"]
        for item in observation["source_consistency_checks"]
        if not item["consistent"]
    }
    if not required_warning_ids <= warnings:
        raise ContractError("an inconsistent source check lacks a structured warning")
    reviewed_warnings = set(adapter["source_consistency_handling"]["warning_ids_reviewed"])
    if not required_warning_ids <= reviewed_warnings:
        raise ContractError("adapter did not review every source inconsistency warning")

    forbidden_input_tags = {
        rule["forbidden_tag"]
        for rule in case["leakage_rules"]
        if rule["applies_to"] in {"inputs", "all"}
    }
    input_channels = [item for item in observation["channels"] if item["channel_id"] in case["inputs"]]
    leaked = {
        tag
        for channel in input_channels
        for tag in channel["leakage_tags"]
        if tag in forbidden_input_tags
    }
    if leaked:
        raise ContractError(f"forbidden leakage tags in inputs: {sorted(leaked)}")

    unresolved = any(mapping["status"] == "unresolved" for mapping in adapter["mappings"])
    if case["status"] == "ready" and (adapter["status"] != "validated" or unresolved):
        raise ContractError("ready ValidationCase requires a validated adapter with no unresolved mappings")

    return [
        "schemas",
        "unique_identifiers",
        "coordinate_space_references",
        "processing_pass_references",
        "cross_document_references",
        "adapter_target_references",
        "source_consistency_warnings",
        "leakage_guard",
        "ready_state_fail_closed",
    ]


def expect_rejection(
    baseline: dict[str, dict[str, Any]],
    name: str,
    mutate: Any,
) -> dict[str, str]:
    candidate = copy.deepcopy(baseline)
    mutate(candidate)
    try:
        validate_bundle(candidate)
    except ContractError as error:
        return {"name": name, "result": "PASS", "rejected_by": str(error)}
    raise AssertionError(f"negative control was accepted: {name}")


def main() -> None:
    bundle = {name: load_json(path) for name, path in PATHS.items()}
    checks = validate_bundle(bundle)

    mutations = [
        expect_rejection(
            bundle,
            "missing_coordinate_spaces",
            lambda candidate: candidate["observation"].pop("coordinate_spaces"),
        ),
        expect_rejection(
            bundle,
            "unknown_channel_coordinate_space",
            lambda candidate: candidate["observation"]["channels"][0].update(
                coordinate_space_id="nonexistent-space"
            ),
        ),
        expect_rejection(
            bundle,
            "missing_adapter_ref",
            lambda candidate: candidate["validation"].pop("adapter_ref"),
        ),
        expect_rejection(
            bundle,
            "adapter_observation_mismatch",
            lambda candidate: candidate["adapter"].update(
                source_observation_ref="examples/other-observation.json"
            ),
        ),
        expect_rejection(
            bundle,
            "unreported_source_inconsistency",
            lambda candidate: candidate["observation"].update(
                source_consistency_warnings=[]
            ),
        ),
        expect_rejection(
            bundle,
            "ready_with_unresolved_adapter",
            lambda candidate: candidate["validation"].update(status="ready"),
        ),
        expect_rejection(
            bundle,
            "dynamics_target_leakage_as_input",
            lambda candidate: candidate["validation"].update(
                inputs=["dynamics_pass.joint_torques"]
            ),
        ),
    ]

    result = {
        "schema_version": "human-model-contract-validation.v0.2",
        "all_passed": True,
        "positive_checks": checks,
        "negative_controls": mutations,
        "boundaries": [
            "Nimble/OpenSim not executed",
            "B3D numerical frame transform not validated",
            "Subject40-to-IAA adapter remains blocked",
            "no prediction or model promotion evidence"
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
