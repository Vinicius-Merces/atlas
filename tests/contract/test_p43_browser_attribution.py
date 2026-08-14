from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARIZER = ROOT / "scripts/summarize_normalized_asteria_evidence.py"


def run_summary(tmp_path: Path, browser: dict) -> dict:
    deployment = {
        "deployment_class": "controlled-preview",
        "claimable_production": False,
        "url": "https://example.trycloudflare.com",
        "tls": {"verified": True, "protocol": "TLSv1.3"},
    }
    browser_path = tmp_path / "browser.json"
    deployment_path = tmp_path / "deployment.json"
    output_path = tmp_path / "summary.json"
    browser_path.write_text(json.dumps(browser), encoding="utf-8")
    deployment_path.write_text(json.dumps(deployment), encoding="utf-8")
    run = subprocess.run(
        [
            sys.executable,
            str(SUMMARIZER),
            "--target", "claude-code",
            "--browser", str(browser_path),
            "--deployment", str(deployment_path),
            "--source-commit", "a" * 40,
            "--campaign-commit", "b" * 40,
            "--historical-score", "86.40",
            "--output", str(output_path),
        ],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    return json.loads(output_path.read_text(encoding="utf-8"))


def base_row() -> dict:
    return {
        "route": "/enquire",
        "viewport": {"name": "wide-1920", "width": 1920, "height": 1080},
        "status": 200,
        "horizontalOverflow": 0,
        "consoleErrors": [],
        "pageErrors": [],
        "failedRequests": [],
        "errorResponses": [],
        "formControls": [{"tag": "input", "id": "email", "label": "Email", "ariaLabel": None}],
        "screenshot": "screenshots/enquire.png",
    }


def browser_with(row: dict) -> dict:
    return {
        "version": 2,
        "results": [row],
        "seo_not_found": {"status": 404, "robots": ["noindex"], "canonical": None},
    }


def test_p43_provider_cdn_cgi_noise_is_preserved_but_not_target_attributable(tmp_path: Path) -> None:
    row = base_row()
    row["consoleErrors"] = [
        "Failed to load resource: the server responded with a status of 404 ()"
    ]
    row["errorResponses"] = [
        {
            "url": "https://example.trycloudflare.com/cdn-cgi/scripts/email-decode.min.js",
            "status": 404,
            "statusText": "Not Found",
            "resourceType": "script",
            "method": "GET",
        }
    ]
    result = run_summary(tmp_path, browser_with(row))
    obs = result["observations"]
    assert obs["raw_console_errors"] == 1
    assert obs["raw_http_error_responses"] == 1
    assert obs["deployment_infrastructure_console_errors"] == 1
    assert obs["deployment_infrastructure_http_error_responses"] == 1
    assert obs["target_attributable_console_errors"] == 0
    assert obs["target_attributable_http_error_responses"] == 0
    assert result["checks"]["no_target_console_errors"] is True
    assert result["checks"]["no_target_http_error_responses"] is True


def test_p43_next_rsc_abort_is_preserved_as_expected_prefetch_cancellation(tmp_path: Path) -> None:
    row = base_row()
    row["failedRequests"] = [
        {
            "url": "https://example.trycloudflare.com/residences?_rsc=abc123",
            "resourceType": "fetch",
            "error": "net::ERR_ABORTED",
        }
    ]
    result = run_summary(tmp_path, browser_with(row))
    obs = result["observations"]
    assert obs["raw_failed_requests"] == 1
    assert obs["expected_rsc_prefetch_cancellations"] == 1
    assert obs["target_attributable_failed_requests"] == 0
    assert result["checks"]["no_target_failed_requests"] is True


def test_p43_target_api_429_remains_target_attributable(tmp_path: Path) -> None:
    row = base_row()
    row["consoleErrors"] = [
        "Failed to load resource: the server responded with a status of 429 ()"
    ]
    row["errorResponses"] = [
        {
            "url": "https://example.trycloudflare.com/api/events",
            "status": 429,
            "statusText": "",
            "resourceType": "ping",
            "method": "POST",
        }
    ]
    result = run_summary(tmp_path, browser_with(row))
    obs = result["observations"]
    assert obs["target_attributable_console_errors"] == 1
    assert obs["target_attributable_http_error_responses"] == 1
    assert obs["target_error_response_samples"][0]["url"].endswith("/api/events")
    assert result["checks"]["no_target_console_errors"] is False
    assert result["checks"]["no_target_http_error_responses"] is False
    assert result["normalized_floor_pass"] is False
