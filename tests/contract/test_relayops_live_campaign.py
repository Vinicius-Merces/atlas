from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_p5_campaign_validator_passes() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_relayops_live_campaign.py")], cwd=ROOT, check=True)


def test_p5_uses_common_environment_and_clean_room_targets() -> None:
    campaign = yaml.safe_load((ROOT / "benchmarks/reference-builds/campaigns/p5/campaign.yaml").read_text(encoding="utf-8"))
    policy = campaign["run_policy"]
    assert policy["same_base_commit_required"] is True
    assert policy["forbid_cross_run_branch_reads"] is True
    assert policy["forbid_implementation_reuse"] is True
    assert policy["frozen_runner_contract_required"] is True
    assert policy["common_environment_floor_required"] is True
    assert policy["controlled_preview_cannot_satisfy_production_config"] is True
    assert policy["negative_tenant_isolation_evidence_required"] is True
    assert policy["billing_reconciliation_evidence_required"] is True
    floor = campaign["common_environment_floor"]
    assert floor["public_preview_provider"] == "cloudflare-quick-tunnel"
    assert floor["browser_runner"] == "campaign-portable"
    assert floor["runner_contract_schema"] == "benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json"
    assert floor["deployment_workflow"] == ".github/workflows/reference-build-controlled-deployment.yml"
    assert floor["required_viewports"] == ["phone-360", "tablet-768", "laptop-1280", "wide-1920"]


def test_p5_manifest_requires_runner_and_assurance_sidecars() -> None:
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p5/run-manifest.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {
        "campaign_base_commit",
        "fixture_sha256",
        "rubric_sha256",
        "runner_contract",
        "environment_capability_manifest",
        "evidence_assurance_manifest",
        "deployment_evidence_manifest",
        "saas_assurance_manifest",
        "isolation_attestation",
    } <= required
    assert schema["properties"]["fixture_id"]["const"] == "multitenant-subscription-saas"


def test_p5_runner_contract_normalizes_adapter_inputs() -> None:
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {
        "app_dir",
        "install_command",
        "test_command",
        "build_command",
        "start_command",
        "port",
        "health_path",
        "origin_env",
        "browser_routes",
    } <= required
    assert schema["properties"]["port"]["const"] == 4173
    assert schema["properties"]["browser_routes"]["minItems"] == 5


def test_p5_assurance_requires_direct_tenant_and_billing_evidence() -> None:
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p5/assurance/relayops-assurance.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {
        "tenant_database",
        "tenant_storage",
        "tenant_search",
        "tenant_cache_jobs",
        "billing_entitlements",
        "admin_audit",
        "import_export",
        "secret_boundary",
    } <= required
    assert schema["$defs"]["denialAttempt"]["properties"]["outcome"]["const"] == "denied"
    assert schema["properties"]["secret_boundary"]["properties"]["exposed_privileged_secrets"]["const"] == 0
