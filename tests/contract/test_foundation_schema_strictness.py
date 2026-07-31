from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_NAMES = (
    "agent-metadata.schema.json",
    "change-provenance.schema.json",
    "contradiction-register.schema.json",
    "memory-drift-report.schema.json",
    "parallel-execution-manifest.schema.json",
    "policy-evaluation-report.schema.json",
    "policy-exception.schema.json",
    "policy-rule.schema.json",
    "project-brief.schema.json",
    "reconciliation-proposal.schema.json",
    "reconciliation-report.schema.json",
    "registry.schema.json",
    "resume-packet.schema.json",
    "runtime-capability.schema.json",
    "runtime-contract.schema.json",
    "session-brief.schema.json",
    "source-of-truth-manifest.schema.json",
)
FIXTURES = json.loads(
    (ROOT / "tests" / "fixtures" / "schema-instances.json").read_text(
        encoding="utf-8"
    )
)


def load_schema(name: str) -> dict[str, Any]:
    return json.loads(
        (ROOT / "schemas" / name).read_text(encoding="utf-8")
    )


def load_fixture(name: str) -> dict[str, Any]:
    fixture = FIXTURES[name]
    if "path" in fixture:
        return json.loads(
            (ROOT / fixture["path"]).read_text(encoding="utf-8")
        )
    return deepcopy(fixture["instance"])


def errors_for(name: str, instance: object) -> list:
    return list(Draft202012Validator(load_schema(name)).iter_errors(instance))


def at_path(instance: object, path: tuple[str | int, ...]) -> object:
    current = instance
    for part in path:
        current = current[part]  # type: ignore[index]
    return current


def set_path(
    instance: object,
    path: tuple[str | int, ...],
    value: object,
) -> None:
    parent = at_path(instance, path[:-1])
    parent[path[-1]] = value  # type: ignore[index]


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_foundation_schemas_define_closed_root_objects(
    schema_name: str,
) -> None:
    schema = load_schema(schema_name)

    assert schema["type"] == "object"
    assert schema["properties"]
    assert schema["additionalProperties"] is False


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_foundation_schemas_reject_unknown_root_fields(
    schema_name: str,
) -> None:
    instance = load_fixture(schema_name)
    instance["unexpected_field"] = True

    errors = errors_for(schema_name, instance)

    assert any(error.validator == "additionalProperties" for error in errors)


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_foundation_schemas_reject_null_required_fields(
    schema_name: str,
) -> None:
    schema = load_schema(schema_name)
    valid = load_fixture(schema_name)
    for field in schema["required"]:
        instance = deepcopy(valid)
        instance[field] = None

        errors = errors_for(schema_name, instance)

        assert any(
            list(error.path) == [field] for error in errors
        ), f"{schema_name} accepted null for {field}"


@pytest.mark.parametrize(
    ("schema_name", "field", "invalid_value"),
    (
        ("agent-metadata.schema.json", "tools", []),
        ("change-provenance.schema.json", "changes", [42]),
        ("contradiction-register.schema.json", "contradictions", [42]),
        ("memory-drift-report.schema.json", "sources_checked", [42]),
        ("parallel-execution-manifest.schema.json", "workstreams", [42]),
        ("policy-evaluation-report.schema.json", "results", [42]),
        ("policy-exception.schema.json", "compensating_controls", [42]),
        ("policy-rule.schema.json", "evidence", [42]),
        ("project-brief.schema.json", "active_work", [42]),
        ("reconciliation-proposal.schema.json", "proposed_updates", [42]),
        ("reconciliation-report.schema.json", "workstreams", [42]),
        ("registry.schema.json", "agents", [42]),
        ("resume-packet.schema.json", "memory_sources", [42]),
        ("runtime-capability.schema.json", "capabilities", [42]),
        ("runtime-contract.schema.json", "required_capabilities", [42]),
        ("session-brief.schema.json", "completed_work", [42]),
        ("source-of-truth-manifest.schema.json", "domains", []),
    ),
)
def test_foundation_schemas_reject_invalid_collection_members(
    schema_name: str,
    field: str,
    invalid_value: object,
) -> None:
    instance = load_fixture(schema_name)
    instance[field] = invalid_value

    errors = errors_for(schema_name, instance)

    assert any(list(error.path)[:1] == [field] for error in errors)


ENUM_CASES = (
    ("contradiction-register.schema.json", ("contradictions", 0, "status")),
    ("parallel-execution-manifest.schema.json", ("status",)),
    ("policy-exception.schema.json", ("status",)),
    ("policy-rule.schema.json", ("severity",)),
    ("reconciliation-proposal.schema.json", ("status",)),
    ("reconciliation-report.schema.json", ("outcome",)),
    ("runtime-capability.schema.json", ("support",)),
    (
        "source-of-truth-manifest.schema.json",
        ("domains", "framework_version", "type"),
    ),
)


@pytest.mark.parametrize(("schema_name", "path"), ENUM_CASES)
def test_foundation_schemas_enforce_closed_vocabularies(
    schema_name: str,
    path: tuple[str | int, ...],
) -> None:
    instance = load_fixture(schema_name)
    set_path(instance, path, "unknown-value")

    errors = errors_for(schema_name, instance)

    assert any(list(error.path) == list(path) for error in errors)


VALID_WORKSTREAM = {
    "workstream_id": "ws-example",
    "task_id": "task-example",
    "summary": "Example workstream",
    "runtime": "codex",
    "owner_role": "backend-engineer",
    "dependencies": [],
    "resource_claims": [],
    "validation": [],
    "reviews": [],
    "completion_criteria": ["validated"],
    "status": "planned",
}
VALID_POLICY_RESULT = {
    "policy_id": "atlas.version.consistency",
    "outcome": "passed",
    "evidence": {},
    "findings": [],
    "remediation": "Align every version-bearing source.",
    "exception_id": None,
}
VALID_PROPOSED_UPDATE = {
    "source": "VERSION",
    "finding_type": "version-drift",
    "severity": "blocking",
    "proposed_action": "Align the source with the current version.",
    "automatic": False,
}
VALID_CONFLICT = {
    "left_claim": "claim-left",
    "right_claim": "claim-right",
    "resource_left": "src/shared",
    "resource_right": "src/shared/file.py",
    "severity": "blocking",
}


NESTED_CASES = (
    ("change-provenance.schema.json", ("changes", 0)),
    ("contradiction-register.schema.json", ("contradictions", 0)),
    ("memory-drift-report.schema.json", ("summary",)),
    ("parallel-execution-manifest.schema.json", ("workstreams", 0)),
    ("policy-evaluation-report.schema.json", ("results", 0)),
    ("reconciliation-proposal.schema.json", ("proposed_updates", 0)),
    ("reconciliation-report.schema.json", ("conflicts", 0)),
    ("registry.schema.json", ("runtime_support",)),
    (
        "source-of-truth-manifest.schema.json",
        ("domains", "framework_version"),
    ),
)


def prepare_nested_case(
    schema_name: str,
    path: tuple[str | int, ...],
) -> dict[str, Any]:
    instance = load_fixture(schema_name)
    if schema_name == "parallel-execution-manifest.schema.json":
        instance["workstreams"] = [deepcopy(VALID_WORKSTREAM)]
    elif schema_name == "policy-evaluation-report.schema.json":
        instance["results"] = [deepcopy(VALID_POLICY_RESULT)]
        instance["summary"]["passed"] = 1
    elif schema_name == "reconciliation-proposal.schema.json":
        instance["proposed_updates"] = [deepcopy(VALID_PROPOSED_UPDATE)]
    elif schema_name == "reconciliation-report.schema.json":
        instance["conflicts"] = [deepcopy(VALID_CONFLICT)]
        instance["outcome"] = "blocked"
    target = at_path(instance, path)
    target["unexpected_field"] = True  # type: ignore[index]
    return instance


@pytest.mark.parametrize(("schema_name", "path"), NESTED_CASES)
def test_foundation_schemas_reject_unknown_nested_fields(
    schema_name: str,
    path: tuple[str | int, ...],
) -> None:
    instance = prepare_nested_case(schema_name, path)

    errors = errors_for(schema_name, instance)

    assert any(
        error.validator == "additionalProperties"
        and list(error.path) == list(path)
        for error in errors
    )


def test_documented_extension_points_remain_typed_and_extensible() -> None:
    policy_report = load_fixture("policy-evaluation-report.schema.json")
    result = deepcopy(VALID_POLICY_RESULT)
    result["evidence"] = {
        "command": "validate.py",
        "metrics": {"passed": 3},
    }
    policy_report["results"] = [result]
    policy_report["summary"]["passed"] = 1

    runtime_contract = load_fixture("runtime-contract.schema.json")
    runtime_contract["shared_sources"]["new_domain"] = "framework/new-domain/"

    registry = load_fixture("registry.schema.json")
    registry["automation"]["new_generator"] = "scripts/new_generator.py"

    source_manifest = load_fixture("source-of-truth-manifest.schema.json")
    source_manifest["domains"]["new_domain"] = {
        "source": "framework/new-domain/",
        "type": "directory",
        "optional": True,
    }

    assert not errors_for("policy-evaluation-report.schema.json", policy_report)
    assert not errors_for("runtime-contract.schema.json", runtime_contract)
    assert not errors_for("registry.schema.json", registry)
    assert not errors_for(
        "source-of-truth-manifest.schema.json",
        source_manifest,
    )

    registry["automation"]["invalid_generator"] = 42
    assert errors_for("registry.schema.json", registry)


def test_all_canonical_agent_metadata_instances_validate() -> None:
    schema = load_schema("agent-metadata.schema.json")
    validator = Draft202012Validator(schema)
    for path in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        metadata = yaml.safe_load(frontmatter)

        errors = list(validator.iter_errors(metadata))

        assert not errors, f"{path}: {errors}"


def test_all_canonical_policy_rules_validate() -> None:
    validator = Draft202012Validator(load_schema("policy-rule.schema.json"))
    for path in sorted((ROOT / "policies").glob("*.json")):
        instance = json.loads(path.read_text(encoding="utf-8"))

        errors = list(validator.iter_errors(instance))

        assert not errors, f"{path}: {errors}"


def test_all_supported_runtime_declarations_validate() -> None:
    validator = Draft202012Validator(
        load_schema("runtime-capability.schema.json")
    )
    for runtime in ("claude", "codex"):
        path = ROOT / "adapters" / runtime / "runtime-declaration.json"
        instance = json.loads(path.read_text(encoding="utf-8"))

        errors = list(validator.iter_errors(instance))

        assert not errors, f"{path}: {errors}"
