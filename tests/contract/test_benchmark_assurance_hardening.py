from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate_benchmark_evidence_assurance.py"


def write_fixture(tmp_path: Path, *, ratio: float = 3.5, robots: list[str] | None = None, canonical=None, cache_age: int = 60, recovery_evidence: bool = True) -> Path:
    robots = robots or ["noindex, follow"]
    for name in ("evidence.txt", "browser.json", "impl.txt", "recovery.txt", "cache.txt"):
        (tmp_path / name).write_text("ok\n", encoding="utf-8")
    env = {
        "version": 1,
        "captured_at": "2026-08-13T00:00:00Z",
        "runtime": "test-runtime",
        "model": "test-model",
        "capabilities": {
            "browser": {"native_available": False, "portable_fallback_eligible": True, "source": "campaign-portable"},
            "deployment": {"native_available": False, "campaign_adapter_available": False},
            "network": {"mode": "restricted"},
            "independent_review": {"available": True},
            "commands": {},
        },
    }
    (tmp_path / "environment.json").write_text(json.dumps(env), encoding="utf-8")
    data = {
        "version": 1,
        "environment_manifest": "environment.json",
        "evidence_references": ["evidence.txt"],
        "browser": {"source": "campaign-portable", "summary": "browser.json", "screenshots": []},
        "non_text_contrast": {"minimum_required": 3.0, "samples": [{"selector": "input", "ratio": ratio, "essential": True, "evidence_ref": "evidence.txt"}]},
        "seo_not_found": [{"route": "/missing", "status": 404, "robots": robots, "canonical": canonical, "evidence_ref": "browser.json"}],
        "visual_regression": {"mode": "capture-only", "baseline_root": None, "diff_report": None},
        "recovery_claims": [{"claim": "automatic retry", "advertised": True, "implementation_ref": "impl.txt", "evidence_ref": "recovery.txt" if recovery_evidence else "missing-recovery.txt"}],
        "mutable_cache": [{"route": "/inventory", "shared": True, "max_age_seconds": cache_age, "freshness_budget_seconds": 300, "evidence_ref": "cache.txt"}],
        "deployment": {"status": "unavailable", "url": None, "evidence_ref": None},
    }
    path = tmp_path / "assurance.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def run_validator(tmp_path: Path, manifest: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--manifest", str(manifest), "--repo-root", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_p41_assurance_manifest_accepts_honest_capture_only_run(tmp_path: Path) -> None:
    result = run_validator(tmp_path, write_fixture(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "capture-only" in result.stdout
    assert "production-domain blocker" in result.stdout


def test_p41_rejects_non_text_contrast_below_three_to_one(tmp_path: Path) -> None:
    result = run_validator(tmp_path, write_fixture(tmp_path, ratio=2.47))
    assert result.returncode == 1
    assert "non-text contrast below 3.00" in result.stdout


def test_p41_rejects_conflicting_404_robots_and_canonical(tmp_path: Path) -> None:
    result = run_validator(tmp_path, write_fixture(tmp_path, robots=["noindex", "index, follow"], canonical="https://example.test/"))
    assert result.returncode == 1
    assert "conflicting index directive" in result.stdout
    assert "must not canonicalise" in result.stdout


def test_p41_rejects_unproven_recovery_claim_and_stale_mutable_cache(tmp_path: Path) -> None:
    result = run_validator(tmp_path, write_fixture(tmp_path, recovery_evidence=False, cache_age=31536000))
    assert result.returncode == 1
    assert "recovery claim evidence" in result.stdout
    assert "mutable cache exceeds freshness budget" in result.stdout
