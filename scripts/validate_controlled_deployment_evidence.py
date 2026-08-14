#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "benchmarks/reference-builds/campaigns/p4/controlled-deployment/deployment-evidence.schema.json"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Validate ATLAS controlled benchmark deployment evidence.")
    result.add_argument("--manifest", required=True)
    return result


def fail(items: list[str]) -> int:
    print("Controlled deployment evidence validation failed:")
    for item in items:
        print(f"- {item}")
    return 1


def repo_ref_exists(value: str | None) -> bool:
    if value is None:
        return False
    path = ROOT / value
    return path.exists()


def main() -> int:
    args = parser().parse_args()
    path = Path(args.manifest)
    data = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    failures = [error.message for error in validator.iter_errors(data)]

    url = data.get("url", "")
    parsed = urlparse(url)
    deployment_class = data.get("deployment_class")
    provider = data.get("provider")
    http = data.get("http", {})
    tls = data.get("tls", {})

    if parsed.scheme != "https" or not parsed.hostname:
        failures.append("deployment URL must be public HTTPS")
    if not tls.get("verified"):
        failures.append("TLS verification is not true")
    status = http.get("status")
    if not isinstance(status, int) or not 200 <= status < 400:
        failures.append(f"public health response must be 2xx/3xx, got {status!r}")
    final_url = http.get("final_url", "")
    if not isinstance(final_url, str) or not final_url.startswith("https://"):
        failures.append("final HTTP URL is not HTTPS")

    if provider == "cloudflare-quick-tunnel":
        if deployment_class != "controlled-preview":
            failures.append("Cloudflare Quick Tunnel may only be recorded as controlled-preview")
        if parsed.hostname and not parsed.hostname.endswith(".trycloudflare.com"):
            failures.append("Cloudflare Quick Tunnel hostname must end in .trycloudflare.com")
        if data.get("claimable_production") is not False:
            failures.append("Cloudflare Quick Tunnel cannot be claimable production")

    if deployment_class == "controlled-preview":
        lifecycle = data.get("lifecycle", {})
        if lifecycle.get("ephemeral") is not True or lifecycle.get("expires_with_job") is not True:
            failures.append("controlled preview must be ephemeral and expire with the workflow job")
        if data.get("claimable_production") is not False:
            failures.append("controlled preview cannot satisfy production-domain evidence")

    if deployment_class == "claimable-production":
        if data.get("claimable_production") is not True:
            failures.append("claimable production must set claimable_production=true")
        for key in ("persistent_configuration_ref", "environment_configuration_ref"):
            value = data.get(key)
            if not repo_ref_exists(value):
                failures.append(f"claimable production requires existing repository evidence at {key}: {value!r}")

    if failures:
        return fail(failures)

    print(
        "Controlled deployment evidence valid: "
        f"{deployment_class}, provider={provider}, url={url}, status={status}, tls={tls.get('protocol')}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
