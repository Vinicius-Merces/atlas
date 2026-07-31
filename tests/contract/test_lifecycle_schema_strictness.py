from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_NAMES = (
    "task-envelope.schema.json",
    "execution-result.schema.json",
    "checkpoint.schema.json",
    "handoff-manifest.schema.json",
    "continuation-plan.schema.json",
    "workstream.schema.json",
    "resource-claim.schema.json",
    "evidence-record.schema.json",
)


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_lifecycle_schemas_reject_null_required_fields(schema_name: str) -> None:
    schema = load_schema(schema_name)
    invalid = {field: None for field in schema["required"]}

    errors = list(Draft202012Validator(schema).iter_errors(invalid))

    assert errors, f"{schema_name} accepted null-valued required fields"


@pytest.mark.parametrize(
    ("schema_name", "field", "invalid_value"),
    (
        ("task-envelope.schema.json", "state", "unknown"),
        ("execution-result.schema.json", "status", "unknown"),
        ("checkpoint.schema.json", "state", "unknown"),
        ("workstream.schema.json", "status", "unknown"),
        ("resource-claim.schema.json", "mode", "unknown"),
        ("evidence-record.schema.json", "status", "unknown"),
    ),
)
def test_lifecycle_schemas_enforce_declared_enums(
    schema_name: str,
    field: str,
    invalid_value: str,
) -> None:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors({field: invalid_value}))

    assert any(list(error.path) == [field] for error in errors)


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_lifecycle_schemas_reject_unknown_fields(schema_name: str) -> None:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors({"unexpected_field": True}))

    assert any(error.validator == "additionalProperties" for error in errors)


@pytest.mark.parametrize(
    ("schema_name", "field"),
    (
        ("task-envelope.schema.json", "reviews"),
        ("execution-result.schema.json", "changed_files"),
        ("checkpoint.schema.json", "completed_steps"),
        ("handoff-manifest.schema.json", "pending_steps"),
        ("continuation-plan.schema.json", "next_steps"),
        ("workstream.schema.json", "dependencies"),
        ("resource-claim.schema.json", "resources"),
        ("evidence-record.schema.json", "validation"),
    ),
)
def test_lifecycle_schemas_reject_non_string_array_items(
    schema_name: str,
    field: str,
) -> None:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors({field: [{"not": "a string"}]}))

    assert any(list(error.path)[:1] == [field] for error in errors)
