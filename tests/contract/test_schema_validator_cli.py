from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from scripts import (
    build_project_brief,
    build_resume_packet,
    refresh_continuity_artifacts,
    validate_execution_result,
    validate_handoff,
    validate_task_envelope,
)


ROOT = Path(__file__).resolve().parents[2]
VALID_INSTANCES = {
    "validate_task_envelope.py": {
        "id": "task-cli-validation",
        "task_type": "feature",
        "summary": "Validate a task envelope",
        "primary_role": "orchestrator",
        "workflow": "default",
        "reviews": [],
        "validation": [],
    },
    "validate_execution_result.py": {
        "task_id": "task-cli-validation",
        "runtime": "codex",
        "status": "completed",
        "summary": "Validation completed",
        "changed_files": [],
        "validation": [],
        "reviews": [],
        "assumptions": [],
        "remaining_risks": [],
    },
    "validate_handoff.py": {
        "handoff_id": "handoff-cli-validation",
        "task_id": "task-cli-validation",
        "from_runtime": "codex",
        "to_runtime": "claude-code",
        "checkpoint": "checkpoint-cli-validation.json",
        "context_pack": "",
        "completed_steps": [],
        "pending_steps": ["continue"],
        "validation": [],
        "reviews": [],
        "assumptions": [],
        "remaining_risks": [],
    },
}


def run_script(
    script: str,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("script", sorted(VALID_INSTANCES))
def test_schema_validator_accepts_valid_instance(
    script: str,
    tmp_path: Path,
) -> None:
    instance = tmp_path / f"{Path(script).stem}.json"
    instance.write_text(
        json.dumps(VALID_INSTANCES[script]) + "\n",
        encoding="utf-8",
    )

    result = run_script(script, str(instance))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Valid " in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize(
    ("script", "field", "invalid_value", "expected_location"),
    (
        ("validate_task_envelope.py", "reviews", "not-an-array", "$.reviews"),
        ("validate_execution_result.py", "status", "unknown", "$.status"),
        ("validate_handoff.py", "pending_steps", [1], "$.pending_steps[0]"),
    ),
)
def test_schema_validator_rejects_schema_violation_with_friendly_error(
    script: str,
    field: str,
    invalid_value: object,
    expected_location: str,
    tmp_path: Path,
) -> None:
    data = deepcopy(VALID_INSTANCES[script])
    data[field] = invalid_value
    instance = tmp_path / f"invalid-{Path(script).stem}.json"
    instance.write_text(json.dumps(data) + "\n", encoding="utf-8")

    result = run_script(script, str(instance))

    assert result.returncode == 1
    assert "validation failed:" in result.stderr.lower()
    assert expected_location in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("script", sorted(VALID_INSTANCES))
def test_schema_validator_reports_invalid_json(
    script: str,
    tmp_path: Path,
) -> None:
    instance = tmp_path / f"broken-{Path(script).stem}.json"
    instance.write_text("{\n", encoding="utf-8")

    result = run_script(script, str(instance))

    assert result.returncode == 1
    assert "invalid JSON" in result.stderr
    assert "line 2, column 1" in result.stderr
    assert result.stdout == ""


def test_handoff_validator_preserves_cross_runtime_invariant(
    tmp_path: Path,
) -> None:
    data = deepcopy(VALID_INSTANCES["validate_handoff.py"])
    data["to_runtime"] = data["from_runtime"]
    instance = tmp_path / "same-runtime-handoff.json"
    instance.write_text(json.dumps(data) + "\n", encoding="utf-8")

    result = run_script("validate_handoff.py", str(instance))

    assert result.returncode == 1
    assert "$.to_runtime: must differ from $.from_runtime" in result.stderr


@pytest.mark.parametrize(
    "module",
    (
        validate_task_envelope,
        validate_execution_result,
        validate_handoff,
        build_project_brief,
        build_resume_packet,
        refresh_continuity_artifacts,
    ),
)
def test_help_is_read_only(
    module,
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(module, "ROOT", tmp_path)

    with pytest.raises(SystemExit) as error:
        module.main(["--help"])

    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_continuity_generators_preserve_no_argument_behavior(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (tmp_path / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    monkeypatch.setattr(build_project_brief, "ROOT", tmp_path)
    monkeypatch.setattr(build_resume_packet, "ROOT", tmp_path)

    build_project_brief.main([])
    build_resume_packet.main([])

    continuity = tmp_path / ".atlas" / "continuity"
    assert (continuity / "project-brief.json").is_file()
    assert (continuity / "resume-packet.json").is_file()


def test_continuity_refresh_preserves_no_argument_sequence(
    monkeypatch,
) -> None:
    calls = []
    monkeypatch.setattr(
        refresh_continuity_artifacts,
        "run",
        lambda script, *args: calls.append((script, args)),
    )

    refresh_continuity_artifacts.main([])

    assert calls == [
        ("build_project_brief.py", ()),
        ("build_resume_packet.py", ()),
        ("audit_memory_drift.py", ()),
    ]
