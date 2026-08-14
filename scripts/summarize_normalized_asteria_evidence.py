#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


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


def main() -> int:
    args = parse_args()
    browser = json.loads(Path(args.browser).read_text(encoding="utf-8"))
    deployment = json.loads(Path(args.deployment).read_text(encoding="utf-8"))
    rows = browser.get("results", [])

    route_status_failures = [r for r in rows if not isinstance(r.get("status"), int) or not 200 <= r["status"] < 400]
    overflow = [r for r in rows if int(r.get("horizontalOverflow") or 0) > 0]
    console_errors = sum(len(r.get("consoleErrors", [])) for r in rows)
    page_errors = sum(len(r.get("pageErrors", [])) for r in rows)
    request_failures = sum(len(r.get("failedRequests", [])) for r in rows)

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
        "no_console_errors": console_errors == 0,
        "no_page_errors": page_errors == 0,
        "no_request_failures": request_failures == 0,
        "form_fields_labeled": not unlabeled,
        "not_found_seo_truth": missing_truth,
    }

    summary = {
        "version": 1,
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
        "observations": {
            "route_status_failures": len(route_status_failures),
            "overflow_cases": len(overflow),
            "max_horizontal_overflow": max([int(r.get("horizontalOverflow") or 0) for r in rows] or [0]),
            "console_errors": console_errors,
            "page_errors": page_errors,
            "request_failures": request_failures,
            "unlabeled_form_fields": len(unlabeled),
            "unlabeled_samples": unlabeled[:10],
            "not_found_status": missing.get("status"),
            "not_found_robots": missing.get("robots", []),
            "not_found_canonical": missing_canonical,
            "tls_protocol": deployment.get("tls", {}).get("protocol"),
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
