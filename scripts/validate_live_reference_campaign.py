#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P4 = ROOT / "benchmarks/reference-builds/campaigns/p4"
CAMPAIGN = P4 / "campaign.yaml"
ASSURANCE = P4 / "assurance"
CONTROLLED = P4 / "controlled-deployment"
P4_SKILL_CATALOG_BASELINE = 128


def fail(message: str) -> None:
    raise SystemExit(f"P4 live reference campaign validation failed: {message}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    campaign = yaml.safe_load(CAMPAIGN.read_text(encoding="utf-8"))
    if campaign.get("id") != "p4-live-reference-build-campaign":
        fail("campaign id")
    fixture = campaign["fixture"]
    spec = yaml.safe_load((ROOT / fixture["spec"]).read_text(encoding="utf-8"))
    rubric = yaml.safe_load((ROOT / fixture["rubric"]).read_text(encoding="utf-8"))
    if spec.get("id") != fixture.get("id"):
        fail("fixture mismatch")
    if rubric.get("version") != fixture.get("benchmark_version"):
        fail("rubric mismatch")

    policy = campaign["run_policy"]
    required_true = [
        "same_base_commit_required", "isolated_run_branches", "forbid_cross_run_branch_reads",
        "forbid_implementation_reuse", "preserve_exact_fixture_and_rubric",
        "record_runtime_reported_model", "environment_capability_manifest_required",
        "portable_browser_fallback_required", "evidence_assurance_manifest_required",
        "evidence_reference_integrity_required", "visual_regression_mode_required",
        "recovery_claim_evidence_required", "mutable_cache_freshness_required",
        "browser_evidence_required", "deployment_evidence_manifest_required",
        "controlled_public_preview_required", "deployment_class_truth_required",
        "controlled_preview_cannot_satisfy_production_domain",
        "claimable_production_same_provider_required",
        "deployment_evidence_required_for_claimable_result",
        "independent_review_required", "preserve_first_frozen_result_before_remediation",
        "compare_only_after_target_results_frozen",
    ]
    disabled = [key for key in required_true if policy.get(key) is not True]
    if disabled:
        fail("required policy disabled: " + ", ".join(disabled))

    targets = {row["id"]: row for row in campaign["targets"]}
    if set(targets) != {"calibration-gpt-5-6-sol", "codex", "claude-code"}:
        fail("target set")
    if targets["codex"]["model"] != "runtime-reported" or targets["claude-code"]["model"] != "runtime-reported":
        fail("target model must be runtime-reported")
    for target in targets.values():
        packet = ROOT / target["packet"]
        text = packet.read_text(encoding="utf-8").lower()
        for marker in ("do not inspect", "site-from-brief-delivery", "controlled-preview", "production-domain"):
            if marker not in text:
                fail(f"packet {target['id']} missing {marker}")

    required_files = [
        ASSURANCE / "README.md",
        ASSURANCE / "environment-capability.schema.json",
        ASSURANCE / "evidence-assurance.schema.json",
        ASSURANCE / "deployment-adapter.contract.yaml",
        CONTROLLED / "README.md",
        CONTROLLED / "deployment-evidence.schema.json",
        ROOT / "scripts/capture_benchmark_environment.py",
        ROOT / "scripts/validate_benchmark_evidence_assurance.py",
        ROOT / "scripts/collect_portable_browser_evidence.cjs",
        ROOT / "scripts/probe_controlled_deployment.py",
        ROOT / "scripts/validate_controlled_deployment_evidence.py",
        ROOT / "scripts/controlled_deployment_smoke_server.py",
        ROOT / ".github/workflows/reference-build-browser-evidence.yml",
        ROOT / ".github/workflows/reference-build-controlled-deployment.yml",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing:
        fail("missing P4.1/P4.2 artifacts: " + ", ".join(missing))

    env_schema = load_json(ASSURANCE / "environment-capability.schema.json")
    evidence_schema = load_json(ASSURANCE / "evidence-assurance.schema.json")
    deployment_schema = load_json(CONTROLLED / "deployment-evidence.schema.json")
    if env_schema.get("title") != "ATLAS Benchmark Environment Capability Manifest":
        fail("environment schema title")
    if evidence_schema.get("title") != "ATLAS Benchmark Evidence Assurance Manifest":
        fail("evidence assurance schema title")
    if evidence_schema.get("properties", {}).get("version", {}).get("const") != 2:
        fail("evidence assurance schema must be version 2 after P4.2")
    if deployment_schema.get("title") != "ATLAS Controlled Benchmark Deployment Evidence":
        fail("deployment evidence schema title")
    Draft202012Validator.check_schema(env_schema)
    Draft202012Validator.check_schema(evidence_schema)
    Draft202012Validator.check_schema(deployment_schema)

    run_schema = load_json(P4 / "run-manifest.schema.json")
    if run_schema.get("title") != "ATLAS P4 Live Reference Build Run Manifest":
        fail("manifest schema")
    required = set(run_schema.get("required", []))
    if not {"environment_capability_manifest", "evidence_assurance_manifest", "deployment_evidence_manifest"} <= required:
        fail("run manifest must require P4.1/P4.2 sidecar paths")

    adapter = yaml.safe_load((ASSURANCE / "deployment-adapter.contract.yaml").read_text(encoding="utf-8"))
    if adapter.get("version") != 2 or adapter.get("status") != "controlled-preview-active":
        fail("deployment adapter version/status")
    preview = adapter.get("controlled_preview", {})
    if preview.get("enabled") is not True or preview.get("provider") != "cloudflare-quick-tunnel":
        fail("controlled preview adapter")
    if preview.get("execution") != "github-actions" or preview.get("requires_credentials") is not False:
        fail("controlled preview execution/credential policy")
    production = adapter.get("claimable_production", {})
    if production.get("provider") != "vercel" or production.get("enabled") is not False:
        fail("claimable production must remain explicit and disabled until campaign credentials exist")

    controlled = campaign.get("controlled_deployment", {})
    if controlled.get("preview_provider") != "cloudflare-quick-tunnel":
        fail("campaign controlled preview provider")
    if controlled.get("production_provider") != "vercel" or controlled.get("production_enabled") is not False:
        fail("campaign claimable production state")

    model = (ROOT / "framework/live-reference-build-campaign-model.md").read_text(encoding="utf-8")
    for marker in (
        "## Environment normalization", "## Browser evidence fallback", "## Assurance truth checks",
        "## Controlled public deployment", "## Claimable production separation",
        "## P4.1 completion", "## P4.2 completion",
    ):
        if marker not in model:
            fail(f"campaign model missing {marker}")

    browser_workflow = (ROOT / ".github/workflows/reference-build-browser-evidence.yml").read_text(encoding="utf-8")
    for marker in ("workflow_dispatch", "collect_portable_browser_evidence.cjs", "campaign-owned Chromium runner", "upload-artifact"):
        if marker not in browser_workflow:
            fail(f"portable browser workflow missing {marker}")

    deployment_workflow = (ROOT / ".github/workflows/reference-build-controlled-deployment.yml").read_text(encoding="utf-8")
    for marker in (
        "cloudflare-quick-tunnel", "CLOUDFLARED_VERSION", "CLOUDFLARED_LINUX_AMD64_SHA256",
        "probe_controlled_deployment.py", "validate_controlled_deployment_evidence.py",
        "collect_portable_browser_evidence.cjs", "upload-artifact",
    ):
        if marker not in deployment_workflow:
            fail(f"controlled deployment workflow missing {marker}")

    registry = load_json(ROOT / ".claude/registry.json")
    if registry.get("assurance", {}).get("live_reference_build_campaign_model") != "framework/live-reference-build-campaign-model.md":
        fail("registry model pointer")
    current_skill_count = len(registry.get("skills", []))
    if current_skill_count < P4_SKILL_CATALOG_BASELINE:
        fail(
            f"skill catalog regressed below P4.2 baseline: {current_skill_count} < {P4_SKILL_CATALOG_BASELINE}"
        )

    with tempfile.TemporaryDirectory(prefix="p42-assurance-", dir=ROOT) as tmp:
        tmp_path = Path(tmp)
        rel = tmp_path.relative_to(ROOT).as_posix()
        for name in ("evidence.txt", "browser.json", "shot.png", "diff.json", "impl.txt", "recovery.txt", "cache.txt", "deployment.json"):
            (tmp_path / name).write_text("ok\n", encoding="utf-8")
        (tmp_path / "baseline").mkdir()
        env = {
            "version": 1, "captured_at": "2026-08-13T00:00:00Z", "runtime": "test-runtime", "model": "test-model",
            "capabilities": {
                "browser": {"native_available": False, "portable_fallback_eligible": True, "source": "campaign-portable"},
                "deployment": {"native_available": False, "campaign_adapter_available": True},
                "network": {"mode": "restricted"}, "independent_review": {"available": True}, "commands": {}
            }
        }
        (tmp_path / "environment.json").write_text(json.dumps(env), encoding="utf-8")
        evidence = {
            "version": 2,
            "environment_manifest": f"{rel}/environment.json",
            "evidence_references": [f"{rel}/evidence.txt"],
            "browser": {"source": "campaign-portable", "summary": f"{rel}/browser.json", "screenshots": [f"{rel}/shot.png"]},
            "non_text_contrast": {"minimum_required": 3.0, "samples": [{"selector": "input", "ratio": 3.4, "essential": True, "evidence_ref": f"{rel}/evidence.txt"}]},
            "seo_not_found": [{"route": "/missing", "status": 404, "robots": ["noindex, follow"], "canonical": None, "evidence_ref": f"{rel}/browser.json"}],
            "visual_regression": {"mode": "baseline-diff", "baseline_root": f"{rel}/baseline", "diff_report": f"{rel}/diff.json"},
            "recovery_claims": [{"claim": "automatic retry", "advertised": True, "implementation_ref": f"{rel}/impl.txt", "evidence_ref": f"{rel}/recovery.txt"}],
            "mutable_cache": [{"route": "/inventory", "shared": True, "max_age_seconds": 60, "freshness_budget_seconds": 300, "evidence_ref": f"{rel}/cache.txt"}],
            "deployment": {
                "status": "public-https", "deployment_class": "controlled-preview", "claimable_production": False,
                "url": "https://example.trycloudflare.com", "evidence_ref": f"{rel}/deployment.json"
            }
        }
        evidence_path = tmp_path / "assurance.json"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        assurance_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_benchmark_evidence_assurance.py"), "--manifest", str(evidence_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if assurance_run.returncode != 0:
            fail("evidence assurance self-test failed: " + (assurance_run.stdout + assurance_run.stderr).strip())

        deployment = {
            "version": 1,
            "deployment_class": "controlled-preview",
            "provider": "cloudflare-quick-tunnel",
            "source_ref": "bench/test",
            "source_commit": "a" * 40,
            "url": "https://example.trycloudflare.com",
            "started_at": "2026-08-13T00:00:00Z",
            "finished_at": "2026-08-13T00:01:00Z",
            "health_path": "/healthz",
            "tls": {"verified": True, "hostname": "example.trycloudflare.com", "protocol": "TLSv1.3", "certificate_subject": None, "certificate_issuer": None, "not_after": None},
            "http": {"status": 200, "final_url": "https://example.trycloudflare.com/healthz", "headers": {"content-type": "text/plain"}, "body_sha256": "b" * 64},
            "lifecycle": {"ephemeral": True, "cleanup_policy": "process termination at workflow completion", "expires_with_job": True},
            "claimable_production": False,
            "persistent_configuration_ref": None,
            "environment_configuration_ref": None,
            "browser_evidence_ref": None,
            "notes": "synthetic contract self-test"
        }
        deployment_path = tmp_path / "controlled-deployment.json"
        deployment_path.write_text(json.dumps(deployment), encoding="utf-8")
        deployment_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_controlled_deployment_evidence.py"), "--manifest", str(deployment_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if deployment_run.returncode != 0:
            fail("controlled deployment self-test failed: " + (deployment_run.stdout + deployment_run.stderr).strip())

    print("P4/P4.1/P4.2 live reference campaign validation passed: isolated targets, normalized evidence, and controlled public deployment truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
