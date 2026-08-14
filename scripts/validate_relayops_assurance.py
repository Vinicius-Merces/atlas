#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "benchmarks/reference-builds/campaigns/p5/assurance/relayops-assurance.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"RelayOps assurance validation failed: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")


def resolve_repo_ref(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        fail(f"absolute evidence paths are forbidden: {value}")
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"evidence path escapes repository: {value}")
    return resolved


def collect_domain_refs(value: Any, *, key: str | None = None) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            refs.update(collect_domain_refs(child_value, key=child_key))
    elif isinstance(value, list):
        for child in value:
            refs.update(collect_domain_refs(child, key=key))
    elif isinstance(value, str) and key and key.endswith("_ref"):
        refs.add(value)
    return refs


def validate_denial_attempts(manifest: dict[str, Any]) -> int:
    count = 0
    for domain in ("tenant_database", "tenant_storage", "tenant_search"):
        for attempt in manifest[domain]["attempts"]:
            count += 1
            if attempt["source_tenant"] == attempt["target_tenant"]:
                fail(f"{domain} attempt does not cross tenant boundary")
            if attempt["outcome"] != "denied":
                fail(f"{domain} attempt is not denied")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate P5 RelayOps SaaS assurance evidence")
    parser.add_argument("--manifest", required=True, help="Repo-relative or absolute path to assurance manifest")
    parser.add_argument("--schema", help="Override schema path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (ROOT / manifest_path).resolve()
    schema_path = Path(args.schema).resolve() if args.schema else DEFAULT_SCHEMA

    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    manifest = load_json(manifest_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda err: list(err.path))
    if errors:
        detail = "; ".join(f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors[:8])
        fail(detail)

    evidence_refs = set(manifest["evidence_references"])
    domain_refs = collect_domain_refs({
        key: value
        for key, value in manifest.items()
        if key not in {"evidence_references", "run_manifest", "notes"}
    })
    missing_from_index = sorted(domain_refs - evidence_refs)
    if missing_from_index:
        fail("domain refs missing from evidence_references: " + ", ".join(missing_from_index))

    all_refs = set(evidence_refs)
    all_refs.add(manifest["run_manifest"])
    missing_files = sorted(ref for ref in all_refs if not resolve_repo_ref(ref).is_file())
    if missing_files:
        fail("referenced evidence files do not exist: " + ", ".join(missing_files))

    denial_count = validate_denial_attempts(manifest)
    if manifest["secret_boundary"]["exposed_privileged_secrets"] != 0:
        fail("privileged/provider secrets exposed to browser-visible surface")
    if manifest["admin_audit"]["explicit_tenant_context"] is not True:
        fail("privileged admin evidence lacks explicit tenant context")

    print(
        "RelayOps SaaS assurance valid: "
        f"{denial_count} direct cross-tenant denials, "
        f"{len(evidence_refs)} indexed evidence refs, billing/recovery/admin/import/secret gates present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
