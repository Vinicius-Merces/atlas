from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_environment_capture_produces_schema_valid_manifest(tmp_path: Path) -> None:
    output = tmp_path / "environment.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/capture_benchmark_environment.py"),
            "--runtime", "contract-test",
            "--model", "contract-model",
            "--output", str(output),
            "--browser-source", "campaign-portable",
            "--portable-browser-eligible",
            "--network-mode", "restricted",
            "--independent-review",
        ],
        cwd=ROOT,
        check=True,
    )
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p4/assurance/environment-capability.schema.json").read_text(encoding="utf-8"))
    data = json.loads(output.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(data))
    assert not errors, [error.message for error in errors]
    assert data["runtime"] == "contract-test"
    assert data["capabilities"]["browser"]["source"] == "campaign-portable"
    assert data["capabilities"]["browser"]["portable_fallback_eligible"] is True
