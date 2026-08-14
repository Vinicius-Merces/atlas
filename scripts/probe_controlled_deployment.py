#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def flatten_name(value) -> str | None:
    if not value:
        return None
    parts: list[str] = []
    for group in value:
        for key, item in group:
            parts.append(f"{key}={item}")
    return ", ".join(parts) or None


def tls_probe(hostname: str, port: int = 443) -> dict:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=15) as raw:
        with context.wrap_socket(raw, server_hostname=hostname) as wrapped:
            cert = wrapped.getpeercert()
            return {
                "verified": True,
                "hostname": hostname,
                "protocol": wrapped.version() or "unknown",
                "certificate_subject": flatten_name(cert.get("subject")),
                "certificate_issuer": flatten_name(cert.get("issuer")),
                "not_after": cert.get("notAfter"),
            }


def http_probe(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ATLAS-P4.2-controlled-deployment-probe/1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        return {
            "status": int(response.status),
            "final_url": response.geturl(),
            "headers": {str(k).lower(): str(v) for k, v in response.headers.items()},
            "body_sha256": hashlib.sha256(body).hexdigest(),
        }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Probe and record ATLAS controlled public deployment evidence.")
    result.add_argument("--url", required=True)
    result.add_argument("--source-ref", required=True)
    result.add_argument("--source-commit", required=True)
    result.add_argument("--provider", required=True)
    result.add_argument("--deployment-class", choices=("controlled-preview", "claimable-production"), required=True)
    result.add_argument("--health-path", default="/")
    result.add_argument("--output", required=True)
    result.add_argument("--persistent-configuration-ref")
    result.add_argument("--environment-configuration-ref")
    result.add_argument("--browser-evidence-ref")
    result.add_argument("--started-at")
    return result


def main() -> int:
    args = parser().parse_args()
    started_at = args.started_at or now()
    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise SystemExit("Controlled deployment probe requires an https:// URL with a hostname")

    target = args.url.rstrip("/") + args.health_path
    http = http_probe(target)
    tls = tls_probe(parsed.hostname, parsed.port or 443)
    controlled_preview = args.deployment_class == "controlled-preview"

    data = {
        "version": 1,
        "deployment_class": args.deployment_class,
        "provider": args.provider,
        "source_ref": args.source_ref,
        "source_commit": args.source_commit,
        "url": args.url.rstrip("/"),
        "started_at": started_at,
        "finished_at": now(),
        "health_path": args.health_path,
        "tls": tls,
        "http": http,
        "lifecycle": {
            "ephemeral": controlled_preview,
            "cleanup_policy": "process termination at workflow completion" if controlled_preview else "provider-managed persistent deployment",
            "expires_with_job": controlled_preview,
        },
        "claimable_production": not controlled_preview,
        "persistent_configuration_ref": args.persistent_configuration_ref,
        "environment_configuration_ref": args.environment_configuration_ref,
        "browser_evidence_ref": args.browser_evidence_ref,
        "notes": (
            "Campaign-owned controlled preview. Public HTTPS/browser/SEO evidence only; not a production-domain pass."
            if controlled_preview
            else "Campaign-owned persistent production deployment evidence."
        ),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"url": data["url"], "status": http["status"], "tls": tls["protocol"], "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
