#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
P43 = ROOT / "benchmarks/reference-builds/campaigns/p4/normalized-reevaluation"
CAMPAIGN = P43 / "campaign.yaml"
WORKFLOW = ROOT / ".github/workflows/p4-3-normalized-asteria-reevaluation.yml"


def fail(message: str) -> None:
    raise SystemExit(f"P4.3 normalized Asteria validation failed: {message}")


def main() -> int:
    campaign = yaml.safe_load(CAMPAIGN.read_text(encoding="utf-8"))
    if campaign.get("id") != "p4-3-normalized-asteria-reevaluation":
        fail("campaign id")

    policy = campaign.get("policy", {})
    required_true = [
        "frozen_implementation_only",
        "implementation_mutation_forbidden",
        "same_public_https_adapter",
        "same_chromium_runner",
        "same_viewports",
        "same_required_surface_count",
        "campaign_infrastructure_checkout_separate_from_target",
        "native_runtime_evidence_not_required_for_normalized_floor",
        "historical_scores_immutable",
        "no_model_quality_rescore_from_portable_floor_alone",
        "controlled_preview_not_claimable_production",
        "results_must_record_source_commit",
        "results_must_record_campaign_commit",
    ]
    disabled = [key for key in required_true if policy.get(key) is not True]
    if disabled:
        fail("required policy disabled: " + ", ".join(disabled))

    fixture = campaign.get("fixture", {})
    if fixture.get("id") != "premium-marketing-site":
        fail("fixture id")
    baseline = json.loads((ROOT / campaign["historical_comparison"]).read_text(encoding="utf-8"))
    if baseline.get("fixture_sha256") != fixture.get("fixture_sha256"):
        fail("fixture hash drift from historical P4 comparison")
    if baseline.get("rubric_sha256") != fixture.get("rubric_sha256"):
        fail("rubric hash drift from historical P4 comparison")

    expected = {
        "codex": {
            "model": "GPT-5",
            "score": 53.15,
            "commit": "a1751e8558beddee8e8c57d2b3f47de86e1c5860",
        },
        "claude-code": {
            "model": "claude-opus-5",
            "score": 86.40,
            "commit": "bff32598806c7ea9b6cd4c2218ee7d5eac2d0816",
        },
    }
    baseline_runs = {row.get("target"): row for row in baseline.get("runs", [])}
    targets = campaign.get("targets", {})
    if set(targets) != set(expected):
        fail("target set")

    for target, truth in expected.items():
        row = targets[target]
        if row.get("model") != truth["model"]:
            fail(f"{target} model drift")
        if float(row.get("historical_score")) != truth["score"]:
            fail(f"{target} historical score drift")
        commit = row.get("frozen_commit", "")
        if commit != truth["commit"] or not re.fullmatch(r"[a-f0-9]{40}", commit):
            fail(f"{target} frozen commit drift")
        baseline_row = baseline_runs.get(target, {})
        baseline_commit = baseline_row.get("frozen_commit") or baseline_row.get("frozen_implementation_commit")
        if baseline_commit != commit:
            fail(f"{target} frozen commit does not match historical comparison")
        if float(baseline_row.get("score")) != truth["score"]:
            fail(f"{target} score does not match historical comparison")
        routes = row.get("routes", [])
        if len(routes) != len(campaign.get("normalized_floor", {}).get("required_surfaces", [])):
            fail(f"{target} route count differs from normalized required surface count")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "Check out campaign infrastructure",
        "Check out exact frozen target implementation",
        "Prove checkout separation and immutable target SHA",
        "Open common campaign-owned HTTPS ingress",
        "Collect identical portable Chromium evidence floor",
        "summarize_normalized_asteria_evidence.py",
        "compare_normalized_asteria_evidence.py",
        "historical_score",
    ):
        if marker not in workflow:
            fail(f"workflow missing {marker}")
    for target, truth in expected.items():
        if truth["commit"] not in workflow:
            fail(f"workflow missing frozen commit for {target}")

    with tempfile.TemporaryDirectory(prefix="p43-normalized-", dir=ROOT) as tmp:
        d = Path(tmp)
        browser = {
            "results": [
                {
                    "route": "/",
                    "viewport": {"name": "phone-360", "width": 360, "height": 800},
                    "status": 200,
                    "horizontalOverflow": 0,
                    "consoleErrors": [],
                    "pageErrors": [],
                    "failedRequests": [],
                    "formControls": [{"tag": "input", "id": "email", "label": "Email", "ariaLabel": None}],
                    "screenshot": "screenshots/home.png",
                }
            ],
            "seo_not_found": {"route": "/missing", "status": 404, "robots": ["noindex, follow"], "canonical": None},
        }
        deployment = {
            "deployment_class": "controlled-preview",
            "claimable_production": False,
            "url": "https://example.trycloudflare.com",
            "tls": {"verified": True, "protocol": "TLSv1.3"},
        }
        (d / "browser.json").write_text(json.dumps(browser), encoding="utf-8")
        (d / "deployment.json").write_text(json.dumps(deployment), encoding="utf-8")
        summary = d / "summary.json"
        run = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/summarize_normalized_asteria_evidence.py"),
                "--target", "codex",
                "--browser", str(d / "browser.json"),
                "--deployment", str(d / "deployment.json"),
                "--source-commit", "a" * 40,
                "--campaign-commit", "b" * 40,
                "--historical-score", "53.15",
                "--output", str(summary),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if run.returncode != 0:
            fail("summary self-test failed: " + (run.stdout + run.stderr).strip())
        result = json.loads(summary.read_text(encoding="utf-8"))
        if result.get("normalized_floor_pass") is not True:
            fail("summary self-test did not pass normalized floor")

    print("P4.3 normalized Asteria re-evaluation validation passed: frozen implementations, common public HTTPS, common Chromium, immutable historical scores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
