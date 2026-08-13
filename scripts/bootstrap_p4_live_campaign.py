#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "benchmarks/reference-builds/campaigns/p4/campaign.yaml": '''version: 1
id: p4-live-reference-build-campaign
title: P4 Live Reference Build Campaign - Asteria Residences
fixture:
  id: premium-marketing-site
  spec: benchmarks/reference-builds/specs/premium-marketing-site.yaml
  rubric: benchmarks/reference-builds/scoring-rubric.yaml
  benchmark_version: 1
run_policy:
  base_ref: main
  same_base_commit_required: true
  isolated_run_branches: true
  branch_pattern: bench/p4-asteria-{target_id}
  forbid_cross_run_branch_reads: true
  forbid_implementation_reuse: true
  preserve_exact_fixture_and_rubric: true
  record_runtime_reported_model: true
  browser_evidence_required: true
  deployment_evidence_required_for_claimable_result: true
  independent_review_required: true
  preserve_first_frozen_result_before_remediation: true
  compare_only_after_target_results_frozen: true
targets:
- id: calibration-gpt-5-6-sol
  role: calibration
  runtime: chatgpt
  model: GPT-5.6 Sol
  packet: benchmarks/reference-builds/campaigns/p4/runtime-packets/calibration-gpt-5-6-sol.md
  include_in_target_comparison: false
- id: codex
  role: target
  runtime: codex
  model: runtime-reported
  packet: benchmarks/reference-builds/campaigns/p4/runtime-packets/codex-asteria.md
  include_in_target_comparison: true
- id: claude-code
  role: target
  runtime: claude-code
  model: runtime-reported
  packet: benchmarks/reference-builds/campaigns/p4/runtime-packets/claude-code-asteria.md
  include_in_target_comparison: true
completion:
- campaign infrastructure merged to main
- calibration live path exercised and frozen
- codex target run frozen
- claude-code target run frozen
- exact-fixture comparison generated
- evidence-led remediation backlog recorded
''',
    "benchmarks/reference-builds/campaigns/p4/README.md": '''# P4 Live Reference Build Campaign

P4 runs the `premium-marketing-site` fixture as a controlled live campaign.

Implementation code is not merged into `main` before target results are frozen. Every runtime starts from the same recorded base commit and works on an isolated `bench/p4-asteria-{target_id}` branch.

Targets are a diagnostic GPT-5.6 Sol calibration plus Codex and Claude Code comparison targets. The calibration validates the live path but is never relabeled as either target runtime.

Protocol: freeze base commit; create isolated run branch; record manifest; build from the canonical fixture; collect browser/deployment/security/performance evidence; freeze implementation and evidence; obtain independent review; score with P3; preserve the first result before remediation; compare target runs only after both are frozen.
''',
    "benchmarks/reference-builds/campaigns/p4/runtime-packets/calibration-gpt-5-6-sol.md": '''# P4 Asteria Calibration Packet - GPT-5.6 Sol

This is a diagnostic calibration, not a Codex or Claude Code result.

Use only the recorded campaign base commit, the canonical `premium-marketing-site` fixture, ATLAS framework surfaces from that base, and this packet. Do not inspect any other `bench/p4-asteria-*` branch or prior Asteria implementation/evidence/result.

Follow `site-from-brief-delivery` and all applicable Frontend Craft, browser, accessibility, responsive, SEO, structured-data, analytics/conversion, supply-chain, production, and benchmark gates.

Record runtime exactly as `chatgpt` and model exactly as `GPT-5.6 Sol`. Freeze the first result before remediation. Independent review cannot be performed by the implementer in this same session; report that limitation honestly.
''',
    "benchmarks/reference-builds/campaigns/p4/runtime-packets/codex-asteria.md": '''# P4 Asteria Target Packet - Codex

Execute the canonical `premium-marketing-site` fixture as an isolated Codex target run from the exact campaign base commit.

Do not inspect, fetch, diff, or reuse implementation/evidence/results from any other `bench/p4-asteria-*` branch. Do not search repository history for an Asteria solution.

Follow `site-from-brief-delivery` and inherited Frontend Craft, browser, accessibility, responsive, SEO, structured-data, analytics/conversion, supply-chain, production, and independent review gates.

Record runtime as `codex` and the model string exactly as Codex reports it at run time. Freeze the first result before remediation. Independent review must be performed by a reviewer that did not implement the build.
''',
    "benchmarks/reference-builds/campaigns/p4/runtime-packets/claude-code-asteria.md": '''# P4 Asteria Target Packet - Claude Code

Execute the canonical `premium-marketing-site` fixture as an isolated Claude Code target run from the exact campaign base commit.

Do not inspect, fetch, diff, or reuse implementation/evidence/results from any other `bench/p4-asteria-*` branch. Do not search repository history for an Asteria solution.

Follow `site-from-brief-delivery` and inherited Frontend Craft, browser, accessibility, responsive, SEO, structured-data, analytics/conversion, supply-chain, production, and independent review gates.

Record runtime as `claude-code` and the model string exactly as Claude Code reports it at run time. Freeze the first result before remediation. Independent review must be performed by a reviewer that did not implement the build.
''',
    "benchmarks/reference-builds/campaigns/p4/run-manifest.schema.json": '''{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ATLAS P4 Live Reference Build Run Manifest",
  "type": "object",
  "additionalProperties": false,
  "required": ["campaign_id", "target_id", "role", "runtime", "model", "fixture_id", "campaign_base_commit", "run_branch", "fixture_sha256", "rubric_sha256", "isolation_attestation"],
  "properties": {
    "campaign_id": {"type": "string", "const": "p4-live-reference-build-campaign"},
    "target_id": {"type": "string", "minLength": 1},
    "role": {"type": "string", "enum": ["calibration", "target"]},
    "runtime": {"type": "string", "minLength": 1},
    "model": {"type": "string", "minLength": 1},
    "fixture_id": {"type": "string", "const": "premium-marketing-site"},
    "campaign_base_commit": {"type": "string", "minLength": 7},
    "run_branch": {"type": "string", "pattern": "^bench/p4-asteria-[a-z0-9-]+$"},
    "fixture_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "rubric_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "started_at": {"type": "string"},
    "finished_at": {"type": "string"},
    "tool_permissions": {"type": "array", "items": {"type": "string"}},
    "isolation_attestation": {
      "type": "object",
      "additionalProperties": false,
      "required": ["same_base_commit", "no_cross_run_branch_reads", "no_implementation_reuse"],
      "properties": {
        "same_base_commit": {"type": "boolean", "const": true},
        "no_cross_run_branch_reads": {"type": "boolean", "const": true},
        "no_implementation_reuse": {"type": "boolean", "const": true}
      }
    },
    "notes": {"type": "string"}
  }
}
''',
    ".claude/memory/capabilities/live-reference-build-campaign.md": '''# Live Reference Build Campaign

P4 adds execution discipline around the P3 benchmark without adding an agent or skill.

Canonical model: `framework/live-reference-build-campaign-model.md`.
Campaign: `benchmarks/reference-builds/campaigns/p4/campaign.yaml`.

Target runs start from the same frozen base commit. Implementations remain isolated until first results are frozen. Calibration may not impersonate Codex or Claude Code. Runtime/model identity is reported, not guessed. Independent review cannot be performed by the implementer. Frontend Craft remains mandatory for the premium marketing fixture.
''',
    "tests/contract/test_live_reference_campaign.py": '''from __future__ import annotations

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
''',
}

VALIDATOR = '''#!/usr/bin/env python3
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
'''


def write_files() -> None:
    for relative, content in FILES.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    validator = ROOT / "scripts/validate_live_reference_campaign.py"
    validator.write_text(VALIDATOR, encoding="utf-8")


def integrate() -> None:
    registry_path = ROOT / ".claude/registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry.setdefault("assurance", {})["live_reference_build_campaign_model"] = "framework/live-reference-build-campaign-model.md"
    registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    validate = ROOT / "scripts/validate_all.py"
    text = validate.read_text(encoding="utf-8")
    if '"live-reference-build-campaign"' not in text:
        marker = '        _python_step(\n            root,\n            "reference-build-benchmark-pack",\n            "Validate P3 reference build benchmark pack",\n            "validate_reference_build_benchmark_pack.py",\n        ),\n'
        addition = marker + '        _python_step(\n            root,\n            "live-reference-build-campaign",\n            "Validate P4 live reference build campaign",\n            "validate_live_reference_campaign.py",\n        ),\n'
        if marker not in text: raise SystemExit("P3 validator marker not found")
        validate.write_text(text.replace(marker, addition, 1), encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if "## Live Reference Build Campaign P4" not in text:
        section = '''\n## Live Reference Build Campaign P4\n\nP4 turns P3 into an isolated live-build campaign. Asteria is executed from one frozen base commit in separate calibration, Codex, and Claude Code branches. Implementations stay isolated until first target results are frozen, preventing one runtime from inheriting another runtime's solution.\n\nP4 adds no agents or skills. It requires truthful runtime/model identity, browser/deployment evidence, preserved first results, independent review, and exact-fixture comparison. Canonical protocol: `framework/live-reference-build-campaign-model.md` and `benchmarks/reference-builds/campaigns/p4/`.\n\n'''
        marker = "## Discovery descriptions and hover surfaces"
        if marker not in text: raise SystemExit("README marker not found")
        readme.write_text(text.replace(marker, section + marker, 1), encoding="utf-8")

    memory = ROOT / ".claude/memory/index.md"
    if memory.is_file():
        text = memory.read_text(encoding="utf-8")
        entry = "- [Live Reference Build Campaign](capabilities/live-reference-build-campaign.md) - P4 isolated live benchmark protocol."
        if entry not in text:
            memory.write_text(text.rstrip() + "\n" + entry + "\n", encoding="utf-8")

    research = ROOT / "docs/research/agent-skill-landscape-2026.md"
    if research.is_file():
        text = research.read_text(encoding="utf-8")
        if "## P4 Live Reference Build Campaign" not in text:
            text = text.rstrip() + "\n\n## P4 Live Reference Build Campaign\n\nP4 freezes catalog growth again and executes Asteria through isolated live runs. Campaign order: diagnostic calibration, Codex target, Claude Code target, exact-fixture comparison, then evidence-led remediation. New capabilities should be justified by repeated live evidence rather than speculation.\n"
            research.write_text(text, encoding="utf-8")


def main() -> None:
    write_files()
    integrate()
    print("P4 live reference campaign bootstrapped")

if __name__ == "__main__": main()
