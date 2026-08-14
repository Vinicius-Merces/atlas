#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ASSURANCE_DIR = ROOT / "benchmarks/reference-builds/campaigns/p4/assurance"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate P4.1 benchmark evidence assurance sidecar.")
    p.add_argument("--manifest", required=True)
    p.add_argument("--repo-root", default=str(ROOT))
    return p


def main() -> int:
    args = parser().parse_args()
    repo = Path(args.repo_root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo / manifest_path
    failures: list[str] = []
    warnings: list[str] = []

    schema = load_json(ASSURANCE_DIR / "evidence-assurance.schema.json")
    data = load_json(manifest_path)
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        failures.append("schema: " + error.message)

    def require_path(value: str | None, label: str) -> None:
        if not value:
            failures.append(f"{label}: missing path")
            return
        path = Path(value)
        if not path.is_absolute():
            path = repo / path
        try:
            path.relative_to(repo)
        except ValueError:
            failures.append(f"{label}: path escapes repository: {value}")
            return
        if not path.exists():
            failures.append(f"{label}: evidence path does not exist: {value}")

    env_ref = data.get("environment_manifest")
    require_path(env_ref, "environment_manifest")
    if env_ref:
        env_path = repo / env_ref
        if env_path.is_file():
            env_schema = load_json(ASSURANCE_DIR / "environment-capability.schema.json")
            env_data = load_json(env_path)
            for error in sorted(Draft202012Validator(env_schema).iter_errors(env_data), key=lambda e: list(e.path)):
                failures.append("environment schema: " + error.message)

    for idx, ref in enumerate(data.get("evidence_references", [])):
        require_path(ref, f"evidence_references[{idx}]")

    browser = data.get("browser", {})
    if browser.get("source") != "unavailable":
        require_path(browser.get("summary"), "browser.summary")
        for idx, ref in enumerate(browser.get("screenshots", [])):
            require_path(ref, f"browser.screenshots[{idx}]")
    else:
        warnings.append("browser evidence unavailable; browser-dependent benchmark checks must remain unverified")

    contrast = data.get("non_text_contrast", {})
    minimum = float(contrast.get("minimum_required", 3.0))
    for sample in contrast.get("samples", []):
        if sample.get("essential") and float(sample.get("ratio", 0)) < minimum:
            failures.append(f"non-text contrast below {minimum:.2f}: {sample.get('selector')}={sample.get('ratio')}")
        if sample.get("evidence_ref"):
            require_path(sample["evidence_ref"], f"contrast:{sample.get('selector')}")

    for row in data.get("seo_not_found", []):
        route = row.get("route")
        if row.get("status") != 404:
            failures.append(f"404 SEO route {route} returned {row.get('status')}")
        directives = [str(value).lower().replace(" ", "") for value in row.get("robots", [])]
        if not any("noindex" in value for value in directives):
            failures.append(f"404 SEO route {route} lacks noindex")
        if any(value.startswith("index") or ",index" in value for value in directives):
            failures.append(f"404 SEO route {route} has conflicting index directive")
        if row.get("canonical") not in (None, ""):
            failures.append(f"404 SEO route {route} must not canonicalise to another document")
        if row.get("evidence_ref"):
            require_path(row["evidence_ref"], f"seo_not_found:{route}")

    visual = data.get("visual_regression", {})
    mode = visual.get("mode")
    if mode == "baseline-diff":
        require_path(visual.get("baseline_root"), "visual_regression.baseline_root")
        require_path(visual.get("diff_report"), "visual_regression.diff_report")
    elif mode == "capture-only":
        warnings.append("visual evidence is capture-only; do not claim automated visual regression")
    else:
        warnings.append("visual regression unavailable")

    for row in data.get("recovery_claims", []):
        if row.get("advertised"):
            require_path(row.get("implementation_ref"), f"recovery claim implementation: {row.get('claim')}")
            require_path(row.get("evidence_ref"), f"recovery claim evidence: {row.get('claim')}")

    for row in data.get("mutable_cache", []):
        if row.get("shared") and int(row.get("max_age_seconds", 0)) > int(row.get("freshness_budget_seconds", 0)):
            failures.append(f"mutable cache exceeds freshness budget for {row.get('route')}: {row.get('max_age_seconds')} > {row.get('freshness_budget_seconds')}")
        if row.get("evidence_ref"):
            require_path(row["evidence_ref"], f"mutable_cache:{row.get('route')}")

    deployment = data.get("deployment", {})
    if deployment.get("status") == "public-https":
        url = deployment.get("url") or ""
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            failures.append("public deployment must use a valid https URL")
        require_path(deployment.get("evidence_ref"), "deployment.evidence_ref")
    else:
        warnings.append("public HTTPS deployment unavailable; production-domain blocker cannot pass")

    if failures:
        print("Benchmark evidence assurance validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Benchmark evidence assurance valid.")
    for item in warnings:
        print(f"WARNING: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
