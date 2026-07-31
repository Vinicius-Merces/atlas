from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(script: str, workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / script),
            "--root",
            str(workspace),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def workspace(tmp_path: Path, content: str) -> Path:
    root = tmp_path / "workspace"
    records = root / ".atlas" / "deployments"
    records.mkdir(parents=True)
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (records / "record.json").write_text(content, encoding="utf-8")
    return root


def test_integrity_rejects_hash_valid_but_schema_invalid_receipt(
    tmp_path: Path,
) -> None:
    root = workspace(tmp_path, '{"receipt_id": "deploy-invalid"}\n')
    built = run("build_audit_bundle.py", root)
    assert built.returncode == 0, built.stdout + built.stderr

    verified = run("verify_evidence_integrity.py", root)

    assert verified.returncode == 1
    assert "Schema mismatch" in verified.stdout


def test_integrity_rejects_hash_valid_but_invalid_json(tmp_path: Path) -> None:
    root = workspace(tmp_path, "{not-json}\n")
    built = run("build_audit_bundle.py", root)
    assert built.returncode == 0, built.stdout + built.stderr

    verified = run("verify_evidence_integrity.py", root)

    assert verified.returncode == 1
    assert "Invalid JSON" in verified.stdout
