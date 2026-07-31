from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/plan_project_adoption.py", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_adoption_plan_never_overwrites_target_and_flags_collisions(
    tmp_path: Path,
) -> None:
    framework = tmp_path / "framework"
    target = tmp_path / "project"
    framework.mkdir()
    target.mkdir()
    (framework / "VERSION").write_text("1.2.3\n", encoding="utf-8")
    (framework / "README.md").write_text("ATLAS\n", encoding="utf-8")
    (framework / "framework").mkdir()
    (framework / "framework" / "model.md").write_text(
        "model\n", encoding="utf-8"
    )
    (target / "README.md").write_text("Product\n", encoding="utf-8")
    before = (target / "README.md").read_bytes()
    report = tmp_path / "adoption.json"

    result = run(
        "--framework-root",
        str(framework),
        "--target-root",
        str(target),
        "--output",
        str(report),
    )

    assert result.returncode == 2
    assert (target / "README.md").read_bytes() == before
    assert not (target / "framework" / "model.md").exists()
    data = json.loads(report.read_text(encoding="utf-8"))
    actions = {item["path"]: item["action"] for item in data["operations"]}
    assert actions["README.md"] == "merge-required"
    assert actions["framework/model.md"] == "copy"


def test_adoption_plan_passes_for_identical_target(tmp_path: Path) -> None:
    framework = tmp_path / "framework"
    target = tmp_path / "project"
    framework.mkdir()
    target.mkdir()
    for root in (framework, target):
        (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
        (root / "README.md").write_text("same\n", encoding="utf-8")

    result = run(
        "--framework-root",
        str(framework),
        "--target-root",
        str(target),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["summary"]["identical"] == 2
    assert report["summary"]["merge-required"] == 0
    assert report["summary"]["review-required"] == 0
