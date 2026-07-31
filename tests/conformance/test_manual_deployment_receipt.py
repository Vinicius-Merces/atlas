from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "record_manual_deploy.py"),
            *arguments,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def prepare(tmp_path: Path) -> tuple[Path, Path]:
    patch = tmp_path / "patch"
    patch.mkdir()
    manifest = {
        "from_version": "0.1.0",
        "to_version": "0.1.1",
        "files": [],
    }
    (patch / "PATCH-MANIFEST.json").write_text(
        json.dumps(manifest) + "\n",
        encoding="utf-8",
    )
    preflight = tmp_path / "preflight.json"
    preflight.write_text(
        json.dumps(
            {
                "from_version": "0.1.0",
                "to_version": "0.1.1",
                "package": patch.as_posix(),
                "checks": [],
                "outcome": "passed",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return patch, preflight


def test_receipt_defaults_to_pending_without_claiming_application(
    tmp_path: Path,
) -> None:
    patch, _ = prepare(tmp_path)
    output = tmp_path / "pending.json"

    result = run(
        "--from-version",
        "0.1.0",
        "--to-version",
        "0.1.1",
        "--patch-root",
        str(patch),
        "--output",
        str(output),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["status"] == "pending"
    assert receipt["applied_at"] == ""


def test_applied_receipt_requires_passed_preflight_and_validation(
    tmp_path: Path,
) -> None:
    patch, preflight = prepare(tmp_path)
    output = tmp_path / "applied.json"

    missing = run(
        "--from-version",
        "0.1.0",
        "--to-version",
        "0.1.1",
        "--patch-root",
        str(patch),
        "--status",
        "applied",
        "--output",
        str(output),
    )
    assert missing.returncode != 0
    assert "requires a passed" in missing.stdout + missing.stderr

    result = run(
        "--from-version",
        "0.1.0",
        "--to-version",
        "0.1.1",
        "--patch",
        "atlas-framework-0.1.1-incremental.zip",
        "--patch-root",
        str(patch),
        "--preflight-report",
        str(preflight),
        "--status",
        "applied",
        "--validation",
        "target VERSION and full validation profile passed",
        "--output",
        str(output),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads(output.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schemas" / "manual-deployment-receipt.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(
        receipt
    )
    assert receipt["status"] == "applied"
    assert len(receipt["patch_manifest_sha256"]) == 64
    assert len(receipt["preflight_sha256"]) == 64
    assert receipt["validation"]
