from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_policy_exceptions.py"),
            "--root",
            str(root),
        ],
        capture_output=True,
        text=True,
    )


def prepare(root: Path, expires_at: str) -> None:
    policies = root / "policies"
    exceptions = root / ".atlas" / "policy" / "exceptions"
    policies.mkdir(parents=True)
    exceptions.mkdir(parents=True)
    shutil.copy2(
        ROOT / "policies" / "framework_version_consistency.json",
        policies / "framework_version_consistency.json",
    )
    record = {
        "exception_id": "exception-test",
        "policy_id": "atlas.version.consistency",
        "scope": "test",
        "reason": "Exercise expiration handling",
        "owner": "test-owner",
        "expires_at": expires_at,
        "compensating_controls": ["isolated test workspace"],
        "status": "approved",
    }
    (exceptions / "exception.json").write_text(
        json.dumps(record), encoding="utf-8"
    )


def test_unexpired_approved_exception_passes(tmp_path: Path) -> None:
    prepare(tmp_path, "2099-01-01T00:00:00Z")
    result = run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_expired_approved_exception_blocks(tmp_path: Path) -> None:
    prepare(tmp_path, "2000-01-01T00:00:00Z")
    result = run(tmp_path)
    assert result.returncode == 1
    assert "expired" in result.stdout
