from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_p4_campaign_validator_passes() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_live_reference_campaign.py")], cwd=ROOT, check=True)


def test_p4_target_runs_are_isolated_and_runtime_truthful() -> None:
    campaign = yaml.safe_load((ROOT / "benchmarks/reference-builds/campaigns/p4/campaign.yaml").read_text(encoding="utf-8"))
    policy = campaign["run_policy"]
    assert policy["same_base_commit_required"] is True
    assert policy["forbid_cross_run_branch_reads"] is True
    assert policy["forbid_implementation_reuse"] is True
    targets = {row["id"]: row for row in campaign["targets"]}
    assert targets["codex"]["model"] == "runtime-reported"
    assert targets["claude-code"]["model"] == "runtime-reported"
    assert targets["calibration-gpt-5-6-sol"]["include_in_target_comparison"] is False


def test_p4_manifest_requires_isolation_attestation() -> None:
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p4/run-manifest.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {"campaign_base_commit", "fixture_sha256", "rubric_sha256", "isolation_attestation"} <= required
