from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
P43 = ROOT / "benchmarks/reference-builds/campaigns/p4/normalized-reevaluation"


def test_p43_validator_passes() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_normalized_asteria_reevaluation.py")],
        cwd=ROOT,
        check=True,
    )


def test_p43_uses_exact_historical_frozen_implementations() -> None:
    campaign = yaml.safe_load((P43 / "campaign.yaml").read_text(encoding="utf-8"))
    targets = campaign["targets"]
    assert targets["codex"]["frozen_commit"] == "a1751e8558beddee8e8c57d2b3f47de86e1c5860"
    assert targets["claude-code"]["frozen_commit"] == "bff32598806c7ea9b6cd4c2218ee7d5eac2d0816"
    assert float(targets["codex"]["historical_score"]) == 53.15
    assert float(targets["claude-code"]["historical_score"]) == 86.40
    assert campaign["policy"]["historical_scores_immutable"] is True
    assert campaign["policy"]["implementation_mutation_forbidden"] is True
    assert campaign["policy"]["no_model_quality_rescore_from_portable_floor_alone"] is True


def test_p43_common_evidence_floor_is_equal_by_contract() -> None:
    campaign = yaml.safe_load((P43 / "campaign.yaml").read_text(encoding="utf-8"))
    policy = campaign["policy"]
    assert policy["same_public_https_adapter"] is True
    assert policy["same_chromium_runner"] is True
    assert policy["same_viewports"] is True
    assert policy["same_required_surface_count"] is True
    assert policy["campaign_infrastructure_checkout_separate_from_target"] is True
    assert policy["controlled_preview_not_claimable_production"] is True
    required_count = len(campaign["normalized_floor"]["required_surfaces"])
    assert len(campaign["targets"]["codex"]["routes"]) == required_count
    assert len(campaign["targets"]["claude-code"]["routes"]) == required_count


def test_p43_comparator_preserves_scores_instead_of_rewriting_them(tmp_path: Path) -> None:
    common = {
        "version": 1,
        "source_commit": "a" * 40,
        "campaign_commit": "c" * 40,
        "evidence_source": "campaign-portable",
        "deployment_class": "controlled-preview",
        "normalized_floor_pass": True,
        "checks": {"public_https": True, "tls_verified": True},
        "observations": {"console_errors": 0},
    }
    codex = {**common, "target": "codex", "historical_score": 53.15}
    claude = {**common, "target": "claude-code", "historical_score": 86.40, "source_commit": "b" * 40}
    (tmp_path / "codex.json").write_text(json.dumps(codex), encoding="utf-8")
    (tmp_path / "claude.json").write_text(json.dumps(claude), encoding="utf-8")
    output = tmp_path / "comparison.json"
    run = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/compare_normalized_asteria_evidence.py"),
            "--codex", str(tmp_path / "codex.json"),
            "--claude", str(tmp_path / "claude.json"),
            "--output", str(output),
        ],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["historical_scores_immutable"] == {"codex": 53.15, "claude-code": 86.40}
    assert "does not replace the historical benchmark scores" in result["interpretation"]
