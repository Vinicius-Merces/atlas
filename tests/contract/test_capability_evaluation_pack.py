from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], cwd=ROOT, text=True, capture_output=True, check=False)


def test_capability_evaluation_pack_validator() -> None:
    result = run("validate_capability_evaluation_pack.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_skill_quality_measures_full_registry(tmp_path: Path) -> None:
    output = tmp_path / "quality.json"
    result = run("evaluate_skill_quality.py", "--json", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert report["skill_count"] == len(registry["skills"])


def test_skill_routing_measures_full_registry(tmp_path: Path) -> None:
    output = tmp_path / "routing.json"
    result = run("evaluate_skill_routing.py", "--json", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert report["skill_count"] == len(registry["skills"])
    assert report["fixtures"]["count"] >= 20


def test_agent_overlap_measures_full_agent_surface(tmp_path: Path) -> None:
    output = tmp_path / "agents.json"
    result = run("analyze_agent_overlap.py", "--json", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert report["agent_count"] == 1 + len(registry["agents"])
