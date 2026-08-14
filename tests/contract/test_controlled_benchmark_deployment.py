from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CONTROLLED = ROOT / "benchmarks/reference-builds/campaigns/p4/controlled-deployment"


def valid_preview() -> dict:
    return {
        "version": 1,
        "deployment_class": "controlled-preview",
        "provider": "cloudflare-quick-tunnel",
        "source_ref": "bench/test",
        "source_commit": "a" * 40,
        "url": "https://example.trycloudflare.com",
        "started_at": "2026-08-13T00:00:00Z",
        "finished_at": "2026-08-13T00:01:00Z",
        "health_path": "/healthz",
        "tls": {
            "verified": True,
            "hostname": "example.trycloudflare.com",
            "protocol": "TLSv1.3",
            "certificate_subject": None,
            "certificate_issuer": None,
            "not_after": None,
        },
        "http": {
            "status": 200,
            "final_url": "https://example.trycloudflare.com/healthz",
            "headers": {"content-type": "text/plain"},
            "body_sha256": "b" * 64,
        },
        "lifecycle": {
            "ephemeral": True,
            "cleanup_policy": "process termination at workflow completion",
            "expires_with_job": True,
        },
        "claimable_production": False,
        "persistent_configuration_ref": None,
        "environment_configuration_ref": None,
        "browser_evidence_ref": None,
        "notes": "contract fixture",
    }


def test_p42_deployment_evidence_schema_accepts_controlled_preview() -> None:
    schema = json.loads((CONTROLLED / "deployment-evidence.schema.json").read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(valid_preview()))
    assert errors == []


def test_p42_controlled_preview_cannot_claim_production() -> None:
    data = valid_preview()
    data["claimable_production"] = True
    schema = json.loads((CONTROLLED / "deployment-evidence.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(data))


def test_p42_validator_rejects_quick_tunnel_as_claimable_production() -> None:
    data = valid_preview()
    data["deployment_class"] = "claimable-production"
    data["claimable_production"] = True
    data["lifecycle"]["ephemeral"] = False
    data["lifecycle"]["expires_with_job"] = False
    data["persistent_configuration_ref"] = "missing/provider.json"
    data["environment_configuration_ref"] = "missing/env.json"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "deployment.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        run = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_controlled_deployment_evidence.py"), "--manifest", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    assert run.returncode != 0
    assert "Quick Tunnel may only be recorded as controlled-preview" in run.stdout


def test_p42_workflow_pins_tunnel_binary_and_runs_external_smoke() -> None:
    text = (ROOT / ".github/workflows/reference-build-controlled-deployment.yml").read_text(encoding="utf-8")
    assert 'CLOUDFLARED_VERSION: "2026.5.2"' in text
    assert "5286698547f03df745adb2355f04c12dde52ef425491e81f433642d695521886" in text
    assert "adapter-smoke:" in text
    assert "trycloudflare.com" in text
    assert "probe_controlled_deployment.py" in text
    assert "collect_portable_browser_evidence.cjs" in text
