from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker

from release_utils import canonical_release_bytes, sha256_bytes


ROOT = Path(__file__).resolve().parents[1]
RECORD_SCHEMAS = {
    "receipt_id": "manual-deployment-receipt.schema.json",
    "evidence_id": "evidence-record.schema.json",
    "checkpoint_id": "checkpoint.schema.json",
    "handoff_id": "handoff-manifest.schema.json",
}


def sha256(path: Path) -> str:
    return sha256_bytes(canonical_release_bytes(path.read_bytes()))


def safe_record_path(workspace: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    normalized = relative.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or re.match(r"^[A-Za-z]:", normalized)
    ):
        return None
    path = (workspace / Path(*pure.parts)).resolve()
    return path if path.is_relative_to(workspace) else None


def schema_errors(root: Path, schema_name: str, instance: object) -> list[str]:
    schema = json.loads(
        (root / "schemas" / schema_name).read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    return [
        error.message
        for error in sorted(
            validator.iter_errors(instance),
            key=lambda item: list(item.absolute_path),
        )
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Verify an ATLAS audit bundle, record hashes, JSON syntax, and "
            "recognized evidence schemas."
        )
    )
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--bundle")
    args = parser.parse_args()

    workspace = Path(args.root).resolve()
    bundle_path = (
        Path(args.bundle)
        if args.bundle
        else workspace / ".atlas" / "audit" / "audit-bundle.json"
    )
    if not bundle_path.is_absolute():
        bundle_path = workspace / bundle_path
    if not bundle_path.is_file():
        raise SystemExit("Run scripts/build_audit_bundle.py first")

    failures: list[str] = []
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid audit bundle JSON: {exc}") from None
    try:
        schema_root = workspace if (workspace / "schemas").is_dir() else ROOT
        bundle_errors = schema_errors(
            schema_root,
            "audit-bundle-manifest.schema.json",
            bundle,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid audit bundle schema: {exc}") from None
    failures.extend(f"Bundle schema: {error}" for error in bundle_errors)

    records = bundle.get("records", [])
    if not isinstance(records, list):
        records = []
    paths = [
        record.get("path")
        for record in records
        if isinstance(record, dict)
    ]
    duplicates = sorted(
        {
            path
            for path in paths
            if isinstance(path, str) and paths.count(path) > 1
        }
    )
    failures.extend(f"Duplicate record path: {path}" for path in duplicates)
    integrity = bundle.get("integrity", {})
    if not isinstance(integrity, dict):
        integrity = {}
    if integrity.get("algorithm") != "sha256":
        failures.append("Unsupported or missing integrity algorithm")
    if integrity.get("record_count") != len(records):
        failures.append("Record count mismatch")
    expected_records_hash = sha256_bytes(
        json.dumps(
            records,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    if (
        "records_sha256" in integrity
        and integrity.get("records_sha256") != expected_records_hash
    ):
        failures.append("Record index hash mismatch")

    for record in records:
        if not isinstance(record, dict):
            failures.append("Record index entry is not an object")
            continue
        relative = record.get("path")
        path = safe_record_path(workspace, relative)
        if path is None:
            failures.append(f"Path escapes workspace: {relative}")
            continue
        if path.is_symlink():
            failures.append(f"Evidence record is a symlink: {relative}")
            continue
        if not path.is_file():
            failures.append(f"Missing: {relative}")
            continue
        if sha256(path) != record.get("sha256"):
            failures.append(f"Hash mismatch: {relative}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"Invalid JSON: {relative}: {exc}")
            continue
        if isinstance(data, dict):
            schema_name = next(
                (
                    schema
                    for marker, schema in RECORD_SCHEMAS.items()
                    if marker in data
                ),
                None,
            )
            if schema_name:
                for error in schema_errors(schema_root, schema_name, data):
                    failures.append(
                        f"Schema mismatch ({schema_name}): {relative}: {error}"
                    )

    if failures:
        print("Evidence integrity failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print(f"Evidence integrity passed for {len(records)} records.")


if __name__ == "__main__":
    main()
