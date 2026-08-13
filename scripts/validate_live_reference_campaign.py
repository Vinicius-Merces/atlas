#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "benchmarks/reference-builds/campaigns/p4/campaign.yaml"

def fail(message: str) -> None:
    raise SystemExit(f"P4 live reference campaign validation failed: {message}")

def main() -> int:
    campaign = yaml.safe_load(CAMPAIGN.read_text(encoding="utf-8"))
    if campaign.get("id") != "p4-live-reference-build-campaign": fail("campaign id")
    fixture = campaign["fixture"]
    spec = yaml.safe_load((ROOT / fixture["spec"]).read_text(encoding="utf-8"))
    rubric = yaml.safe_load((ROOT / fixture["rubric"]).read_text(encoding="utf-8"))
    if spec.get("id") != fixture.get("id"): fail("fixture mismatch")
    if rubric.get("version") != fixture.get("benchmark_version"): fail("rubric mismatch")
    policy = campaign["run_policy"]
    required_true = ["same_base_commit_required", "isolated_run_branches", "forbid_cross_run_branch_reads", "forbid_implementation_reuse", "preserve_exact_fixture_and_rubric", "record_runtime_reported_model", "browser_evidence_required", "deployment_evidence_required_for_claimable_result", "independent_review_required", "preserve_first_frozen_result_before_remediation", "compare_only_after_target_results_frozen"]
    if any(policy.get(key) is not True for key in required_true): fail("required policy disabled")
    targets = {row["id"]: row for row in campaign["targets"]}
    if set(targets) != {"calibration-gpt-5-6-sol", "codex", "claude-code"}: fail("target set")
    if targets["codex"]["model"] != "runtime-reported" or targets["claude-code"]["model"] != "runtime-reported": fail("target model must be runtime-reported")
    for target in targets.values():
        packet = ROOT / target["packet"]
        text = packet.read_text(encoding="utf-8").lower()
        for marker in ("do not inspect", "site-from-brief-delivery", "independent review"):
            if marker not in text: fail(f"packet {target['id']} missing {marker}")
    schema = json.loads((ROOT / "benchmarks/reference-builds/campaigns/p4/run-manifest.schema.json").read_text(encoding="utf-8"))
    if schema.get("title") != "ATLAS P4 Live Reference Build Run Manifest": fail("manifest schema")
    registry = json.loads((ROOT / ".claude/registry.json").read_text(encoding="utf-8"))
    if registry.get("assurance", {}).get("live_reference_build_campaign_model") != "framework/live-reference-build-campaign-model.md": fail("registry model pointer")
    print("P4 live reference campaign validation passed: isolated calibration, Codex, and Claude Code targets.")
    return 0
if __name__ == "__main__": raise SystemExit(main())
