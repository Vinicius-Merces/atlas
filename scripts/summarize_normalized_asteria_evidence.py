#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize P4.3 normalized Asteria evidence.")
    p.add_argument("--target", required=True)
    p.add_argument("--browser", required=True)
    p.add_argument("--deployment", required=True)
    p.add_argument("--source-commit", required=True)
    p.add_argument("--campaign-commit", required=True)
    p.add_argument("--historical-score", required=True, type=float)
    p.add_argument("--output", required=True)
    return p.parse_args()


def lower_robots(values: list[str]) -> list[str]:
    return [str(v).lower().replace(" ", "") for v in values]


def is_campaign_provider_url(url: str) -> bool:
    parsed = urlparse(url or "")
    return parsed.path.startswith("/cdn-cgi/")


def is_expected_rsc_prefetch_abort(row: dict) -> bool:
    url = str(row.get("url") or "")
    error = str(row.get("error") or "")
    parsed = urlparse(url)
    return (
        row.get("resourceType") in (None, "fetch")
        and "_rsc" in parse_qs(parsed.query)
        and "ERR_ABORTED" in error
    )


def console_status(message: str) -> int | None:
    match = re.search(r"status of (\d{3})", message)
    return int(match.group(1)) if match else None


def classify_browser_noise(rows: list[dict]) -> dict:
    raw_console: list[dict] = []
    raw_failed_requests: list[dict] = []
    raw_error_responses: list[dict] = []
    infrastructure_console: list[dict] = []
    prefetch_cancellations: list[dict] = []
    infrastructure_error_responses: list[dict] = []
    target_console: list[dict] = []
    target_failed_requests: list[dict] = []
    target_error_responses: list[dict] = []

    for row in rows:
        context = {
            "route": row.get("route"),
            "viewport": row.get("viewport", {}).get("name"),
        }
        error_responses = [{**context, **item} for item in row.get("errorResponses", [])]
        raw_error_responses.extend(error_responses)
        provider_status_budget = Counter()
        for item in error_responses:
            if is_campaign_provider_url(str(item.get("url") or "")):
                infrastructure_error_responses.append(item)
                provider_status_budget[int(item.get("status") or 0)] += 1
            else:
                target_error_responses.append(item)

        for message in row.get("consoleErrors", []):
            item = {**context, "message": message}
            raw_console.append(item)
            if "/cdn-cgi/" in message:
                infrastructure_console.append(item)
                continue
            status = console_status(message)
            if status is not None and provider_status_budget[status] > 0:
                provider_status_budget[status] -= 1
                infrastructure_console.append(item)
                continue
            target_console.append(item)

        for failure in row.get("failedRequests", []):
            item = {**context, **failure}
            raw_failed_requests.append(item)
            if is_expected_rsc_prefetch_abort(failure):
                prefetch_cancellations.append(item)
            elif is_campaign_provider_url(str(failure.get("url") or "")):
                infrastructure_console.append({**context, "message": f"requestfailed:{failure.get('url')}"})
            else:
                target_failed_requests.append(item)

    return {
        "raw_console_errors": raw_console,
        "raw_failed_requests": raw_failed_requests,
        "raw_error_responses": raw_error_responses,
        "deployment_infrastructure_console_errors": infrastructure_console,
        "deployment_infrastructure_error_responses": infrastructure_error_responses,
        "expected_rsc_prefetch_cancellations": prefetch_cancellations,
        "target_attributable_console_errors": target_console,
        "target_attributable_failed_requests": target_failed_requests,
        "target_attributable_error_responses": target_error_responses,
    }


def main() -> int:
    args = parse_args()
    browser = json.loads(Path(args.browser).read_text(encoding="utf-8"))
    deployment = json.loads(Path(args.deployment).read_text(encoding="utf-8"))
    rows = browser.get("results", [])

    route_status_failures = [r for r in rows if not isinstance(r.get("status"), int) or not 200 <= r["status"] < 400]
    overflow = [r for r in rows if int(r.get("horizontalOverflow") or 0) > 0]
    page_errors = sum(len(r.get("pageErrors", [])) for r in rows)
    classified = classify_browser_noise(rows)

    unlabeled = []
    for row in rows:
        for control in row.get("formControls", []):
            if control.get("tag") == "button":
                continue
            if not control.get("label") and not control.get("ariaLabel"):
                unlabeled.append({
                    "route": row.get("route"),
                    "viewport": row.get("viewport", {}).get("name"),
                    "tag": control.get("tag"),
                    "id": control.get("id"),
                })

    missing = browser.get("seo_not_found", {})
    directives = lower_robots(missing.get("robots", []))
    missing_noindex = any("noindex" in value for value in directives)
    conflicting_index = any(value.startswith("index") or ",index" in value for value in directives)
    missing_canonical = missing.get("canonical")
    missing_truth = (
        missing.get("status") == 404
        and missing_noindex
        and not conflicting_index
        and missing_canonical in (None, "")
    )

    dep_url = deployment.get("url", "")
    dep_host = urlparse(dep_url).hostname
    public_https = dep_url.startswith("https://") and bool(dep_host)
    tls_verified = deployment.get("tls", {}).get("verified") is True
    controlled_preview_truth = (
        deployment.get("deployment_class") == "controlled-preview"
        and deployment.get("claimable_production") is False
    )

    unique_routes = sorted({r.get("route") for r in rows if r.get("route")})
    viewports = sorted({r.get("viewport", {}).get("name") for r in rows if r.get("viewport", {}).get("name")})
    screenshot_count = sum(1 for r in rows if r.get("screenshot"))

    checks = {
        "public_https": public_https,
        "tls_verified": tls_verified,
        "controlled_preview_truth": controlled_preview_truth,
        "required_surface_http": not route_status_failures,
        "no_horizontal_overflow": not overflow,
        "no_target_console_errors": not classified["target_attributable_console_errors"],
        "no_page_errors": page_errors == 0,
        "no_target_failed_requests": not classified["target_attributable_failed_requests"],
        "no_target_http_error_responses": not classified["target_attributable_error_responses"],
        "form_fields_labeled": not unlabeled,
        "not_found_seo_truth": missing_truth,
    }

    observations = {
        "route_status_failures": len(route_status_failures),
        "overflow_cases": len(overflow),
        "max_horizontal_overflow": max([int(r.get("horizontalOverflow") or 0) for r in rows] or [0]),
        "raw_console_errors": len(classified["raw_console_errors"]),
        "raw_failed_requests": len(classified["raw_failed_requests"]),
        "raw_http_error_responses": len(classified["raw_error_responses"]),
        "deployment_infrastructure_console_errors": len(classified["deployment_infrastructure_console_errors"]),
        "deployment_infrastructure_http_error_responses": len(classified["deployment_infrastructure_error_responses"]),
        "expected_rsc_prefetch_cancellations": len(classified["expected_rsc_prefetch_cancellations"]),
        "target_attributable_console_errors": len(classified["target_attributable_console_errors"]),
        "target_attributable_failed_requests": len(classified["target_attributable_failed_requests"]),
        "target_attributable_http_error_responses": len(classified["target_attributable_error_responses"]),
        "target_error_response_samples": classified["target_attributable_error_responses"][:20],
        "target_console_error_samples": classified["target_attributable_console_errors"][:20],
        "target_failed_request_samples": classified["target_attributable_failed_requests"][:20],
        "page_errors": page_errors,
        "unlabeled_form_fields": len(unlabeled),
        "unlabeled_samples": unlabeled[:10],
        "not_found_status": missing.get("status"),
        "not_found_robots": missing.get("robots", []),
        "not_found_canonical": missing_canonical,
        "tls_protocol": deployment.get("tls", {}).get("protocol"),
    }

    summary = {
        "version": 2,
        "target": args.target,
        "source_commit": args.source_commit,
        "campaign_commit": args.campaign_commit,
        "historical_score": args.historical_score,
        "evidence_source": "campaign-portable",
        "deployment_class": deployment.get("deployment_class"),
        "public_url": dep_url,
        "routes": unique_routes,
        "viewports": viewports,
        "browser_result_count": len(rows),
        "screenshot_count": screenshot_count,
        "checks": checks,
        "normalized_floor_pass": all(checks.values()),
        "observations": observations,
        "classification_policy": {
            "raw_evidence_preserved": True,
            "deployment_infrastructure_noise": "Only identifiable /cdn-cgi/ responses/messages from the common Cloudflare preview are excluded from target-attributable counts.",
            "prefetch_cancellation_noise": "Only failed requests containing an _rsc query and net::ERR_ABORTED are classified as expected Next.js prefetch/page-close cancellations.",
            "all_other_http_4xx_5xx": "Target-attributable unless the URL is campaign-provider /cdn-cgi/ infrastructure.",
        },
        "truth_note": "Normalized evidence floor only. Historical benchmark score remains immutable; this summary is not a model-quality rescore.",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
