from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run_git(root: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def prepare(root: Path) -> Path:
    (root / "policies").mkdir(parents=True)
    shutil.copy2(
        ROOT / "policies" / "repository_cleanliness.json",
        root / "policies" / "repository_cleanliness.json",
    )
    (root / "VERSION").write_text("0.1.0-rc.1\n", encoding="utf-8")
    run_git(root, "init")
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


def test_tracked_user_editor_state_blocks_policy(tmp_path: Path) -> None:
    report = prepare(tmp_path)
    editor = tmp_path / ".vscode" / "extensions.json"
    editor.parent.mkdir()
    editor.write_text('{"recommendations": []}\n', encoding="utf-8")
    run_git(tmp_path, "add", ".vscode/extensions.json")

    result = evaluate(tmp_path, report)

    assert result.returncode == 1, result.stdout + result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["summary"]["blocked"] == 1
    findings = data["results"][0]["findings"]
    assert ".vscode/extensions.json" in findings


def test_ignored_user_editor_state_passes_policy(tmp_path: Path) -> None:
    report = prepare(tmp_path)
    (tmp_path / ".gitignore").write_text(
        ".vscode/extensions.json\n",
        encoding="utf-8",
    )
    editor = tmp_path / ".vscode" / "extensions.json"
    editor.parent.mkdir()
    editor.write_text('{"recommendations": []}\n', encoding="utf-8")

    result = evaluate(tmp_path, report)

    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["summary"]["passed"] == 1
