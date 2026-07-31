from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def prepare(root: Path, deletion_list: str) -> Path:
    (root / "policies").mkdir(parents=True)
    shutil.copy2(
        ROOT / "policies" / "deletion_safety.json",
        root / "policies" / "deletion_safety.json",
    )
    (root / "VERSION").write_text("0.1.0-rc.1\n", encoding="utf-8")
    manifest = {
        "from_version": "0.1.0-beta.11",
        "to_version": "0.1.0-rc.1",
        "files": [
            {
                "path": "legacy.txt",
                "target_path": "legacy.txt",
                "package_path": "",
                "operation": "delete",
            }
        ],
    }
    (root / "PATCH-MANIFEST.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (root / "FILES-TO-DELETE.md").write_text(deletion_list, encoding="utf-8")
    return root / "policy-report.json"


def evaluate(root: Path, report: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evaluate_policies.py"),
            "--root",
            str(root),
            "--output",
            str(report),
        ],
        capture_output=True,
        text=True,
    )


def test_blocking_policy_returns_nonzero(tmp_path: Path) -> None:
    report = prepare(tmp_path, "# Files to delete\n\n")
    result = evaluate(tmp_path, report)
    assert result.returncode == 1, result.stdout + result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["summary"]["blocked"] == 1


def test_explicit_deletion_satisfies_policy(tmp_path: Path) -> None:
    report = prepare(tmp_path, "# Files to delete\n\n- `legacy.txt`\n")
    result = evaluate(tmp_path, report)
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["summary"]["passed"] == 1
