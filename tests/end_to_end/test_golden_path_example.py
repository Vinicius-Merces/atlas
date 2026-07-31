from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance: Path, schema_name: str) -> None:
    schema = load(ROOT / "schemas" / schema_name)
    Draft202012Validator(schema).validate(load(instance))


def test_golden_path_generates_valid_portable_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "golden-path"
    command = [
        sys.executable,
        str(ROOT / "scripts" / "build_golden_path.py"),
        "--output-dir",
        str(output),
        "--runtime",
        "codex",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    schemas = {
        "task-envelope.json": "task-envelope.schema.json",
        "context-pack.manifest.json": "context-pack-manifest.schema.json",
        "execution-plan.json": "runtime-execution-plan.schema.json",
        "checkpoint.json": "checkpoint.schema.json",
        "handoff.json": "handoff-manifest.schema.json",
        "continuation-plan.json": "continuation-plan.schema.json",
        "execution-result.json": "execution-result.schema.json",
        "evidence.json": "evidence-record.schema.json",
    }
    for artifact, schema in schemas.items():
        validate(output / artifact, schema)

    manifest = load(output / "golden-path-manifest.json")
    assert manifest["runtime"] == "codex"
    assert manifest["requires_external_execution"] is True
    assert len(manifest["artifacts"]) == 9

    repeated = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert repeated.returncode != 0
    assert "Refusing to overwrite" in repeated.stdout + repeated.stderr
