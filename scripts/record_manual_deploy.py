from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_STATUSES = {"applied", "simulated"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Record a manual deployment receipt. Applied or simulated status "
            "requires a passed preflight report and concrete validation."
        )
    )
    result.add_argument("--from-version", required=True)
    result.add_argument("--to-version", required=True)
    result.add_argument("--patch", default="")
    result.add_argument("--patch-root")
    result.add_argument("--preflight-report")
    result.add_argument(
        "--status",
        choices=("pending", "applied", "simulated", "failed", "rolled-back"),
        default="pending",
    )
    result.add_argument("--validation", action="append", default=[])
    result.add_argument("--operator-note", action="append", default=[])
    result.add_argument("--source-commit", default="")
    result.add_argument("--release-url", default="")
    result.add_argument("--output")
    return result


def load_patch(
    patch_root: Path | None,
    from_version: str,
    to_version: str,
) -> tuple[list[str], list[str], list[str], str]:
    if patch_root is None:
        return [], [], [], ""
    manifest_path = patch_root / "PATCH-MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid patch manifest: {exc}") from None
    if manifest.get("from_version") != from_version:
        raise SystemExit("Patch manifest from_version does not match the receipt")
    if manifest.get("to_version") != to_version:
        raise SystemExit("Patch manifest to_version does not match the receipt")

    operations = {"add": [], "replace": [], "delete": []}
    for item in manifest.get("files", []):
        operation = item.get("operation")
        target = item.get("target_path")
        if operation not in operations or not isinstance(target, str):
            raise SystemExit("Patch manifest contains an invalid operation")
        operations[operation].append(target)
    return (
        sorted(operations["add"]),
        sorted(operations["replace"]),
        sorted(operations["delete"]),
        sha256(manifest_path),
    )


def load_preflight(
    path: Path | None,
    *,
    from_version: str,
    to_version: str,
) -> tuple[str, dict | None]:
    if path is None:
        return "", None
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid preflight report: {exc}") from None
    if report.get("from_version") != from_version:
        raise SystemExit("Preflight from_version does not match the receipt")
    if report.get("to_version") != to_version:
        raise SystemExit("Preflight to_version does not match the receipt")
    return sha256(path), report


def main() -> None:
    args = parser().parse_args()
    patch_root = Path(args.patch_root).resolve() if args.patch_root else None
    preflight_path = (
        Path(args.preflight_report).resolve()
        if args.preflight_report
        else None
    )
    added, replaced, deleted, patch_manifest_hash = load_patch(
        patch_root,
        args.from_version,
        args.to_version,
    )
    preflight_hash, preflight = load_preflight(
        preflight_path,
        from_version=args.from_version,
        to_version=args.to_version,
    )
    if args.status in FINAL_STATUSES:
        if preflight is None or preflight.get("outcome") != "passed":
            raise SystemExit(
                f"Status {args.status} requires a passed --preflight-report"
            )
        if not args.validation:
            raise SystemExit(
                f"Status {args.status} requires at least one --validation"
            )

    receipt = {
        "receipt_id": f"deploy-{uuid.uuid4().hex[:12]}",
        "from_version": args.from_version,
        "to_version": args.to_version,
        "patch": args.patch,
        "patch_manifest_sha256": patch_manifest_hash,
        "preflight_report": (
            preflight_path.as_posix() if preflight_path is not None else ""
        ),
        "preflight_sha256": preflight_hash,
        "source_commit": args.source_commit,
        "release_url": args.release_url,
        "applied_at": (
            datetime.now(timezone.utc).isoformat()
            if args.status in FINAL_STATUSES
            else ""
        ),
        "files_added": added,
        "files_replaced": replaced,
        "files_deleted": deleted,
        "validation": list(dict.fromkeys(args.validation)),
        "operator_notes": list(dict.fromkeys(args.operator_note)),
        "status": args.status,
    }

    output = (
        Path(args.output).resolve()
        if args.output
        else ROOT / ".atlas" / "deployments" / f"{receipt['receipt_id']}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
