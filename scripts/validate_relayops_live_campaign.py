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
P5 = ROOT / "benchmarks/reference-builds/campaigns/p5"
CAMPAIGN = P5 / "campaign.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"P5 RelayOps live campaign validation failed: {message}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_no_benchmark_catalog_expansion() -> None:
    """Prove P5 infrastructure changes do not also mutate capability catalogs.

    The campaign rule is a scope guard for benchmark infrastructure. It must not
    accidentally freeze normal ATLAS capability evolution forever after the P5
    branches have been isolated from their recorded base commit.
    """
    if not (ROOT / ".git").exists():
        return
    base = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if base.returncode != 0 or not base.stdout.strip():
        return
    changed = subprocess.run(
        ["git", "diff", "--name-only", f"{base.stdout.strip()}...HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if changed.returncode != 0:
        fail("cannot inspect P5 capability-catalog scope")

    changed_paths = [path for path in changed.stdout.splitlines() if path]

    # The clean-room invariant applies when a change is modifying P5 campaign
    # infrastructure itself. A later, unrelated framework/agent/skill PR must be
    # allowed to evolve ATLAS because the benchmark target branches are already
    # frozen from their recorded campaign base commit.
    p5_infrastructure_prefixes = (
        "benchmarks/reference-builds/campaigns/p5/",
        "scripts/validate_relayops_live_campaign.py",
        "scripts/validate_relayops_assurance.py",
        "tests/contract/test_relayops_live_campaign.py",
        "tests/contract/test_relayops_assurance.py",
    )
    touches_p5_infrastructure = any(
        path.startswith(p5_infrastructure_prefixes) for path in changed_paths
    )
    if not touches_p5_infrastructure:
        return

    forbidden_prefixes = (
        "agents/",
        "skills/",
        ".claude/agents/",
        ".claude/skills/",
    )
    touched = sorted(
        path for path in changed_paths
        if path.startswith(forbidden_prefixes)
    )
    if touched:
        fail("P5 infrastructure touches agent/skill catalogs: " + ", ".join(touched))


def main() -> int:
    campaign = yaml.safe_load(CAMPAIGN.read_text(encoding="utf-8"))
    if campaign.get("id") != "p5-live-saas-reference-build-campaign":
        fail("campaign id")

    fixture = campaign["fixture"]
    spec = yaml.safe_load((ROOT / fixture["spec"]).read_text(encoding="utf-8"))
    rubric = yaml.safe_load((ROOT / fixture["rubric"]).read_text(encoding="utf-8"))
    if fixture.get("id") != "multitenant-subscription-saas" or spec.get("id") != fixture.get("id"):
        fail("fixture mismatch")
    if rubric.get("version") != fixture.get("benchmark_version"):
        fail("rubric mismatch")

    policy = campaign["run_policy"]
    required_true = [
        "same_base_commit_required",
        "isolated_run_branches",
        "forbid_cross_run_branch_reads",
        "forbid_implementation_reuse",
        "preserve_exact_fixture_and_rubric",
        "record_runtime_reported_model",
        "frozen_runner_contract_required",
        "environment_capability_manifest_required",
        "portable_browser_fallback_required",
        "evidence_assurance_manifest_required",
        "saas_assurance_manifest_required",
        "evidence_reference_integrity_required",
        "browser_evidence_required",
        "deployment_evidence_manifest_required",
        "controlled_public_preview_required",
        "deployment_class_truth_required",
        "controlled_preview_cannot_satisfy_production_config",
        "claimable_production_same_provider_required",
        "deployment_evidence_required_for_claimable_result",
        "independent_review_required",
        "preserve_first_frozen_result_before_remediation",
        "compare_only_after_target_results_frozen",
        "common_environment_floor_required",
        "negative_tenant_isolation_evidence_required",
        "billing_reconciliation_evidence_required",
        "background_recovery_evidence_required",
        "privileged_admin_audit_evidence_required",
        "secret_boundary_evidence_required",
        "import_partial_failure_evidence_required",
    ]
    disabled = [key for key in required_true if policy.get(key) is not True]
    if disabled:
        fail("required policy disabled: " + ", ".join(disabled))
    if policy.get("branch_pattern") != "bench/p5-relayops-{target_id}":
        fail("branch pattern")

    targets = {row["id"]: row for row in campaign["targets"]}
    if set(targets) != {"calibration-gpt-5-6-sol", "codex", "claude-code"}:
        fail("target set")
    if targets["codex"]["model"] != "runtime-reported" or targets["claude-code"]["model"] != "runtime-reported":
        fail("target model must be runtime-reported")
    if targets["calibration-gpt-5-6-sol"]["include_in_target_comparison"] is not False:
        fail("calibration cannot enter target comparison")

    packet_markers = (
        "do not inspect",
        "saas-from-brief-delivery",
        "runner contract",
        "controlled-preview",
        "saas-production-config",
        "validate_relayops_assurance.py",
        "cross-tenant",
        "billing",
        "independent review",
    )
    for target in targets.values():
        packet = ROOT / target["packet"]
        if not packet.is_file():
            fail(f"missing packet {target['id']}")
        text = packet.read_text(encoding="utf-8").lower()
        for marker in packet_markers:
            if marker not in text:
                fail(f"packet {target['id']} missing {marker}")

    inherited = campaign["inherits"]
    inherited_paths = [
        inherited["live_campaign_model"],
        inherited["full_stack_model"],
        inherited["p4_environment_assurance"],
        inherited["p4_evidence_assurance"],
        inherited["p4_deployment_contract"],
        inherited["p4_deployment_evidence"],
    ]
    missing_inherited = [path for path in inherited_paths if not (ROOT / path).is_file()]
    if missing_inherited:
        fail("missing inherited assurance: " + ", ".join(missing_inherited))

    run_schema = load_json(P5 / "run-manifest.schema.json")
    assurance_schema = load_json(P5 / "assurance/relayops-assurance.schema.json")
    runner_schema = load_json(P5 / "runner-contract.schema.json")
    for schema in (run_schema, assurance_schema, runner_schema):
        Draft202012Validator.check_schema(schema)
    if run_schema.get("title") != "ATLAS P5 RelayOps Live SaaS Run Manifest":
        fail("run manifest schema title")
    if assurance_schema.get("title") != "ATLAS P5 RelayOps SaaS Assurance Manifest":
        fail("SaaS assurance schema title")
    if runner_schema.get("title") != "ATLAS P5 Common Target Runner Contract":
        fail("runner contract schema title")
    required = set(run_schema.get("required", []))
    if not {
        "runner_contract",
        "environment_capability_manifest",
        "evidence_assurance_manifest",
        "deployment_evidence_manifest",
        "saas_assurance_manifest",
        "isolation_attestation",
    } <= required:
        fail("run manifest missing required runner/assurance sidecars")

    floor = campaign["common_environment_floor"]
    if floor.get("execution") != "github-actions" or floor.get("public_preview_provider") != "cloudflare-quick-tunnel":
        fail("common environment execution/provider")
    if floor.get("browser_runner") != "campaign-portable" or floor.get("browser_engine") != "chromium":
        fail("common browser floor")
    if floor.get("runner_contract_schema") != "benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json":
        fail("runner contract schema pointer")
    if floor.get("runner_contract_validator") != "scripts/validate_benchmark_runner_contract.py":
        fail("runner contract validator pointer")
    if floor.get("deployment_workflow") != ".github/workflows/reference-build-controlled-deployment.yml":
        fail("common deployment workflow pointer")
    if floor.get("required_viewports") != ["phone-360", "tablet-768", "laptop-1280", "wide-1920"]:
        fail("common viewport set")
    if floor.get("historical_scores_immutable") is not True:
        fail("historical score truth")

    controlled = campaign["controlled_deployment"]
    if controlled.get("preview_provider") != "cloudflare-quick-tunnel":
        fail("controlled preview provider")
    if controlled.get("production_enabled") is not False:
        fail("claimable production must remain explicit/disabled without campaign credentials")

    domains = set(campaign["saas_assurance"]["domains"])
    expected_domains = {
        "auth_and_membership", "tenant_database", "tenant_storage", "tenant_search",
        "tenant_cache_jobs", "notifications", "billing_entitlements", "admin_audit",
        "import_export", "secret_boundary",
    }
    if domains != expected_domains:
        fail("SaaS assurance domain set")

    required_files = [
        ROOT / "scripts/validate_relayops_assurance.py",
        ROOT / "scripts/validate_benchmark_runner_contract.py",
        ROOT / ".github/workflows/reference-build-controlled-deployment.yml",
        ROOT / ".github/workflows/reference-build-browser-evidence.yml",
    ]
    missing_files = [path.relative_to(ROOT).as_posix() for path in required_files if not path.is_file()]
    if missing_files:
        fail("missing common evidence infrastructure: " + ", ".join(missing_files))

    deployment_workflow = (ROOT / ".github/workflows/reference-build-controlled-deployment.yml").read_text(encoding="utf-8")
    for marker in (
        "workflow_dispatch",
        "app_path",
        "install_command",
        "build_command",
        "start_command",
        "health_path",
        "routes",
        "cloudflare-quick-tunnel",
        "collect_portable_browser_evidence.cjs",
    ):
        if marker not in deployment_workflow:
            fail(f"common deployment workflow missing {marker}")

    validate_no_benchmark_catalog_expansion()

    with tempfile.TemporaryDirectory(prefix="p5-relayops-", dir=ROOT) as tmp:
        tmp_path = Path(tmp)
        rel = tmp_path.relative_to(ROOT).as_posix()
        app_dir = tmp_path / "site"
        app_dir.mkdir()
        runner = {
            "version": 1,
            "app_dir": f"{rel}/site",
            "install_command": "npm ci",
            "test_command": "npm test",
            "build_command": "npm run build",
            "start_command": "npm start",
            "port": 4173,
            "health_path": "/health",
            "origin_env": "RELAYOPS_ORIGIN",
            "browser_routes": ["/", "/login", "/dashboard", "/customers", "/work-orders"],
        }
        runner_path = tmp_path / "runner.json"
        runner_path.write_text(json.dumps(runner), encoding="utf-8")
        runner_run = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_benchmark_runner_contract.py"),
                "--manifest", str(runner_path),
                "--target-root", str(ROOT),
            ],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if runner_run.returncode != 0:
            fail("runner contract self-test failed: " + (runner_run.stdout + runner_run.stderr).strip())

        refs = []
        for index in range(1, 41):
            path = tmp_path / f"e{index}.txt"
            path.write_text("ok\n", encoding="utf-8")
            refs.append(f"{rel}/e{index}.txt")
        run_manifest = tmp_path / "run.json"
        run_manifest.write_text("{}\n", encoding="utf-8")

        iterator = iter(refs)
        ref = lambda: next(iterator)
        assurance = {
            "version": 1,
            "run_manifest": f"{rel}/run.json",
            "evidence_references": refs,
            "auth_and_membership": {
                "session_lifecycle_ref": ref(), "organization_membership_ref": ref(),
                "unauthenticated_denial_ref": ref(), "role_denial_ref": ref(),
            },
            "tenant_database": {"attempts": [
                {"source_tenant": "a", "target_tenant": "b", "operation": "read", "outcome": "denied", "evidence_ref": ref()},
                {"source_tenant": "a", "target_tenant": "b", "operation": "write", "outcome": "denied", "evidence_ref": ref()},
            ]},
            "tenant_storage": {"attempts": [
                {"source_tenant": "a", "target_tenant": "b", "operation": "read", "outcome": "denied", "evidence_ref": ref()},
                {"source_tenant": "a", "target_tenant": "b", "operation": "write", "outcome": "denied", "evidence_ref": ref()},
            ]},
            "tenant_search": {"attempts": [
                {"source_tenant": "a", "target_tenant": "b", "operation": "query", "outcome": "denied", "evidence_ref": ref()},
            ]},
            "tenant_cache_jobs": {
                "cache_isolation_ref": ref(), "job_context_ref": ref(), "duplicate_delivery_ref": ref(),
                "retry_recovery_ref": ref(), "stale_authorization_ref": ref(),
            },
            "notifications": {"tenant_delivery_ref": ref(), "provider_failure_ref": ref(), "recovery_ref": ref()},
            "billing_entitlements": {
                "checkout_ref": ref(), "authoritative_entitlement_ref": ref(), "duplicate_webhook_ref": ref(),
                "out_of_order_webhook_ref": ref(), "reconciliation_ref": ref(), "revocation_ref": ref(),
            },
            "admin_audit": {
                "explicit_tenant_context": True, "least_privilege_denial_ref": ref(),
                "privileged_action_ref": ref(), "audit_record_ref": ref(),
            },
            "import_export": {
                "row_validation_ref": ref(), "partial_failure_ref": ref(),
                "safe_retry_ref": ref(), "export_isolation_ref": ref(),
            },
            "secret_boundary": {
                "browser_bundle_scan_ref": ref(), "client_log_scan_ref": ref(), "exposed_privileged_secrets": 0,
            },
        }
        manifest_path = tmp_path / "assurance.json"
        manifest_path.write_text(json.dumps(assurance), encoding="utf-8")
        assurance_run = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_relayops_assurance.py"), "--manifest", str(manifest_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if assurance_run.returncode != 0:
            fail("RelayOps assurance self-test failed: " + (assurance_run.stdout + assurance_run.stderr).strip())

    print("P5 RelayOps live campaign validation passed: clean-room targets, frozen runner contracts, common environment floor, and SaaS negative-evidence gates are active.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
