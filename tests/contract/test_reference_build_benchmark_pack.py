from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_reference_build_benchmark_pack_validator() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_reference_build_benchmark_pack.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "3 reference builds" in result.stdout
    assert "128 skills reused" in result.stdout


def test_p3_reuses_agents_and_skills() -> None:
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert len(registry["agents"]) + 1 == 87
    assert len(registry["skills"]) == 128
    assert "reference-build-benchmark" in registry["workflows"]
    assert "reference-build-benchmark-review" in registry["reviews"]


def test_harness_smoke_is_never_claimable() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_reference_build_benchmark.py"), "--suite-smoke"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["count"] == 3
    assert all(row["outcome"] == "harness-only" for row in data["results"])


def test_blocking_check_overrides_numeric_score(tmp_path: Path) -> None:
    spec = ROOT / "benchmarks" / "reference-builds" / "specs" / "premium-marketing-site.yaml"
    source = ROOT / "benchmarks" / "reference-builds" / "examples" / "premium-marketing-site.harness-smoke.yaml"
    submission = yaml.safe_load(source.read_text(encoding="utf-8"))
    blocking_id = "marketing-browser-primary-flow"
    for row in submission["checks"]:
        if row["id"] == blocking_id:
            row["status"] = "fail"
            row["evidence"] = []
            row["notes"] = "Synthetic blocking failure."
            break
    changed = tmp_path / "submission.yaml"
    changed.write_text(yaml.safe_dump(submission, sort_keys=False), encoding="utf-8")
    output = tmp_path / "result.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_reference_build_benchmark.py"),
            "--spec", str(spec),
            "--submission", str(changed),
            "--output", str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    scored = json.loads(output.read_text(encoding="utf-8"))
    assert blocking_id in scored["blocking_failures"]
    assert scored["outcome"] == "blocked"
    assert scored["claimable"] is False
    assert scored["score"] < 100
