from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

from release_utils import canonical_release_bytes, sha256_bytes


SHA256 = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    return sha256_bytes(canonical_release_bytes(path.read_bytes()))


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value.replace("\\", "/"))
    return (
        bool(value)
        and "\\" not in value
        and not path.is_absolute()
        and ".." not in path.parts
        and not re.match(r"^[A-Za-z]:", value)
    )


def listed_paths(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return set(re.findall(r"- `([^`]+)`", path.read_text(encoding="utf-8")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-root", required=True)
    parser.add_argument("--installed-root")
    parser.add_argument("--output")
    args = parser.parse_args()

    patch = Path(args.patch_root).resolve()
    manifest_path = patch / "PATCH-MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = []

    if args.installed_root:
        installed = Path(args.installed_root).resolve()
        current = (installed / "VERSION").read_text(encoding="utf-8").strip()
        checks.append({
            "check": "base-version",
            "passed": current == manifest["from_version"],
            "expected": manifest["from_version"],
            "actual": current,
        })

    missing = []
    invalid_hash = []
    invalid_mapping = []
    invalid_paths = []
    invalid_operations = []
    installed_conflicts = []
    declared_payloads: set[str] = set()
    declared_targets: set[str] = set()
    declared_targets_folded: set[str] = set()
    duplicate_targets: set[str] = set()
    duplicate_payloads: set[str] = set()
    declared_payloads_folded: set[str] = set()
    operation_paths = {"add": set(), "replace": set(), "delete": set()}

    for item in manifest.get("files", []):
        operation = item.get("operation")
        package_path = item.get("package_path", item.get("path", ""))
        target = item.get("target_path", item.get("path", ""))
        if operation not in operation_paths:
            invalid_operations.append(f"{operation}: {target}")
            continue
        target_key = target.casefold()
        if target_key in declared_targets_folded:
            duplicate_targets.add(target)
        declared_targets.add(target)
        declared_targets_folded.add(target_key)
        if not safe_relative(target):
            invalid_paths.append(f"target_path: {target}")
        if operation != "delete" and not safe_relative(package_path):
            invalid_paths.append(f"package_path: {package_path}")
        if operation != "delete":
            package_key = package_path.casefold()
            if package_key in declared_payloads_folded:
                duplicate_payloads.add(package_path)
            declared_payloads.add(package_path)
            declared_payloads_folded.add(package_key)
        operation_paths[operation].add(
            target if operation == "delete" else package_path
        )

        if operation == "delete":
            if item.get("sha256"):
                invalid_operations.append(f"delete carries sha256: {target}")
        else:
            path = (patch / package_path).resolve()
            try:
                path.relative_to(patch)
            except ValueError:
                invalid_paths.append(f"package escapes patch root: {package_path}")
                continue
            if path.is_symlink():
                invalid_paths.append(f"package symlink: {package_path}")
                continue
            if not path.is_file():
                missing.append(package_path)
                continue
            if sha256(path) != item.get("sha256"):
                invalid_hash.append(package_path)
            if target.startswith(".claude/") and not package_path.startswith(
                "CLAUDE-DIRECTORY/"
            ):
                invalid_mapping.append(f"{package_path} -> {target}")
            if package_path.startswith(
                "CLAUDE-DIRECTORY/"
            ) and not target.startswith(".claude/"):
                invalid_mapping.append(f"{package_path} -> {target}")

        base_hash = item.get("base_sha256")
        if operation in {"replace", "delete"} and not (
            isinstance(base_hash, str) and SHA256.fullmatch(base_hash)
        ):
            invalid_operations.append(f"{operation} missing base_sha256: {target}")
        if operation == "add" and base_hash is not None:
            invalid_operations.append(f"add carries base_sha256: {target}")

        if args.installed_root and safe_relative(target):
            installed_target = (installed / Path(*PurePosixPath(
                target.replace("\\", "/")
            ).parts)).resolve()
            try:
                installed_target.relative_to(installed)
            except ValueError:
                invalid_paths.append(f"target escapes installed root: {target}")
                continue
            if installed_target.is_symlink():
                installed_conflicts.append(f"symlink target: {target}")
            elif operation == "add" and installed_target.exists():
                installed_conflicts.append(f"add target already exists: {target}")
            elif operation in {"replace", "delete"}:
                if not installed_target.is_file():
                    installed_conflicts.append(
                        f"{operation} target is missing or not a file: {target}"
                    )
                elif isinstance(base_hash, str) and sha256(
                    installed_target
                ) != base_hash:
                    installed_conflicts.append(
                        f"{operation} target differs from declared base: {target}"
                    )

    visible_root = patch / "CLAUDE-DIRECTORY"
    visible_payloads = {
        path.relative_to(patch).as_posix()
        for path in visible_root.rglob("*")
        if path.is_file()
    } if visible_root.exists() else set()
    declared_visible = {
        path for path in declared_payloads if path.startswith("CLAUDE-DIRECTORY/")
    }
    package_only_visible = sorted(visible_payloads - declared_visible)
    missing_visible = sorted(declared_visible - visible_payloads)

    list_mismatches = []
    for operation, filename in [
        ("add", "FILES-TO-ADD.md"),
        ("replace", "FILES-TO-REPLACE.md"),
        ("delete", "FILES-TO-DELETE.md"),
    ]:
        listed = listed_paths(patch / filename)
        if listed != operation_paths[operation]:
            list_mismatches.append(
                {
                    "operation": operation,
                    "manifest": sorted(operation_paths[operation]),
                    "list": sorted(listed),
                }
            )

    checks.extend([
        {"check": "package-files", "passed": not missing, "findings": missing},
        {"check": "hashes", "passed": not invalid_hash, "findings": invalid_hash},
        {
            "check": "claude-directory-mapping",
            "passed": not invalid_mapping,
            "findings": invalid_mapping,
        },
        {"check": "safe-paths", "passed": not invalid_paths, "findings": invalid_paths},
        {
            "check": "operations",
            "passed": (
                not invalid_operations
                and not duplicate_targets
                and not duplicate_payloads
            ),
            "findings": {
                "invalid": invalid_operations,
                "duplicate_targets": sorted(duplicate_targets),
                "duplicate_payloads": sorted(duplicate_payloads),
            },
        },
        {
            "check": "installed-state",
            "passed": not installed_conflicts,
            "findings": installed_conflicts,
        },
        {
            "check": "visible-payload-only",
            "passed": not package_only_visible and not missing_visible,
            "findings": {
                "package_only": package_only_visible,
                "missing": missing_visible,
            },
        },
        {
            "check": "explicit-operation-lists",
            "passed": not list_mismatches,
            "findings": list_mismatches,
        },
    ])

    outcome = "passed" if all(item["passed"] for item in checks) else "blocked"
    report = {
        "from_version": manifest["from_version"],
        "to_version": manifest["to_version"],
        "package": patch.as_posix(),
        "checks": checks,
        "outcome": outcome,
    }
    output = Path(args.output) if args.output else patch / "DEPLOY-PREFLIGHT-REPORT.json"
    if not output.is_absolute():
        output = patch / output
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output)
    if outcome == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
