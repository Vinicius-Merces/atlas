from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts import validate_contracts


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "compatibility" / "contract-conformance-baseline.json"


def run_validator(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/validate_contracts.py", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_contract_check_reports_full_conformance() -> None:
    result = run_validator()

    assert result.returncode == 0, result.stdout + result.stderr
    assert "fully_conformant=true" in result.stdout
    assert "0 known violations" in result.stdout


def test_strict_contract_mode_accepts_complete_catalog() -> None:
    result = run_validator("--mode", "strict")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "fully_conformant=true" in result.stdout


def test_report_mode_confirms_empty_violation_set(tmp_path: Path) -> None:
    output = tmp_path / "contract-report.json"
    result = run_validator("--mode", "report", "--output", str(output))

    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["summary"]["fully_conformant"] is True
    assert report["summary"]["violations"] == 0
    assert report["violations"] == []


def test_baseline_fingerprint_detects_changed_nonconforming_asset() -> None:
    original = validate_contracts.Violation(
        id="agent-contract:.claude/agents/example.md:identity.authority",
        contract="agent-contract",
        collection="agents",
        artifact=".claude/agents/example.md",
        artifact_sha256="a" * 64,
        requirement="identity.authority",
        expected="authority level",
    )
    changed = validate_contracts.Violation(
        **{
            **original.__dict__,
            "artifact_sha256": "b" * 64,
        }
    )
    expected = validate_contracts.baseline_candidate("0.1.0", [original])
    actual = validate_contracts.baseline_candidate("0.1.0", [changed])

    findings = validate_contracts.compare_baseline(expected, actual)

    assert any("nonconforming_assets_sha256" in item for item in findings)


def test_contract_baseline_is_machine_readable_and_versioned() -> None:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    assert baseline["baseline_version"] == 1
    assert baseline["framework_version"] == (
        ROOT / "VERSION"
    ).read_text(encoding="utf-8").strip()
    assert baseline["known_violation_count"] == 0
    assert baseline["counts_by_contract"] == {}
