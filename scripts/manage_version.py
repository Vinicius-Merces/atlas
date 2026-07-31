from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(
    r"^\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\.\d+)?$"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def nested_value(data: dict[str, Any], field: str) -> Any:
    value: Any = data
    for part in field.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(field)
        value = value[part]
    return value


def set_nested_value(data: dict[str, Any], field: str, value: str) -> None:
    target: Any = data
    parts = field.split(".")
    for part in parts[:-1]:
        if not isinstance(target, dict) or part not in target:
            raise KeyError(field)
        target = target[part]
    if not isinstance(target, dict) or parts[-1] not in target:
        raise KeyError(field)
    target[parts[-1]] = value


def recursive_versions(value: Any) -> list[str]:
    versions: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "version":
                versions.append(item)
            versions.extend(recursive_versions(item))
    elif isinstance(value, list):
        for item in value:
            versions.extend(recursive_versions(item))
    return versions


def replace_recursive_versions(value: Any, version: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "version":
                value[key] = version
            else:
                replace_recursive_versions(item, version)
    elif isinstance(value, list):
        for item in value:
            replace_recursive_versions(item, version)


def configured_paths(root: Path, config: dict[str, Any]) -> list[Path]:
    paths = [root / item["path"] for item in config["json_fields"]]
    paths.extend(root / item["path"] for item in config["line_fields"])
    for pattern in config["recursive_json_version_globs"]:
        paths.extend(sorted(root.glob(pattern)))
    return sorted(set(paths))


def historical_paths(root: Path, config: dict[str, Any]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in config["historical_globs"]:
        paths.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(paths)


def validate_configuration(root: Path, config: dict[str, Any]) -> None:
    managed = set(configured_paths(root, config))
    historical = set(historical_paths(root, config))
    overlap = managed & historical
    if overlap:
        names = ", ".join(path.relative_to(root).as_posix() for path in overlap)
        raise ValueError(f"Managed paths overlap protected history: {names}")
    missing = [path for path in managed if not path.is_file()]
    if missing:
        names = ", ".join(path.relative_to(root).as_posix() for path in missing)
        raise ValueError(f"Managed version paths are missing: {names}")


def find_mismatches(
    root: Path, config: dict[str, Any], expected: str
) -> list[str]:
    mismatches: list[str] = []

    for item in config["json_fields"]:
        path = root / item["path"]
        try:
            actual = nested_value(read_json(path), item["field"])
        except (KeyError, json.JSONDecodeError) as exc:
            mismatches.append(f"{item['path']}:{item['field']} is invalid: {exc}")
            continue
        if actual != expected:
            mismatches.append(
                f"{item['path']}:{item['field']}={actual!r}, expected {expected!r}"
            )

    for pattern in config["recursive_json_version_globs"]:
        for path in sorted(root.glob(pattern)):
            versions = recursive_versions(read_json(path))
            relative = path.relative_to(root).as_posix()
            if not versions:
                mismatches.append(f"{relative} contains no version fields")
            for actual in versions:
                if actual != expected:
                    mismatches.append(
                        f"{relative}:version={actual!r}, expected {expected!r}"
                    )

    for item in config["line_fields"]:
        path = root / item["path"]
        pattern = re.compile(item["pattern"], re.MULTILINE)
        matches = pattern.findall(path.read_text(encoding="utf-8"))
        expected_line = item["replacement"].format(version=expected)
        if len(matches) != 1:
            mismatches.append(
                f"{item['path']} expected one version line, found {len(matches)}"
            )
        elif matches[0] != expected_line:
            mismatches.append(
                f"{item['path']} version line is stale, expected {expected_line!r}"
            )

    return mismatches


def update_versions(
    root: Path, config: dict[str, Any], target: str
) -> list[str]:
    before = {
        path: sha256(path)
        for path in configured_paths(root, config)
        if path.is_file()
    }
    protected_before = {
        path: sha256(path) for path in historical_paths(root, config)
    }

    for item in config["json_fields"]:
        path = root / item["path"]
        data = read_json(path)
        set_nested_value(data, item["field"], target)
        write_json(path, data)

    for pattern in config["recursive_json_version_globs"]:
        for path in sorted(root.glob(pattern)):
            data = read_json(path)
            replace_recursive_versions(data, target)
            write_json(path, data)

    for item in config["line_fields"]:
        path = root / item["path"]
        text = path.read_text(encoding="utf-8")
        replacement = item["replacement"].format(version=target)
        updated, count = re.subn(
            item["pattern"], replacement, text, flags=re.MULTILINE
        )
        if count != 1:
            raise ValueError(
                f"{item['path']} expected one version line, found {count}"
            )
        path.write_text(updated, encoding="utf-8")

    (root / config["source"]).write_text(target + "\n", encoding="utf-8")

    protected_after = {
        path: sha256(path) for path in historical_paths(root, config)
    }
    if protected_after != protected_before:
        raise ValueError("A protected historical release file was modified")

    changed = [
        path.relative_to(root).as_posix()
        for path in configured_paths(root, config)
        if before.get(path) != sha256(path)
    ]
    source = root / config["source"]
    if source not in before:
        changed.append(source.relative_to(root).as_posix())
    return sorted(set(changed))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate or update controlled ATLAS version surfaces."
    )
    parser.add_argument("--root", default=str(ROOT))
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--check",
        action="store_true",
        help="Explicitly validate all managed surfaces against VERSION.",
    )
    action.add_argument("--set", dest="target_version")
    parser.add_argument("--report")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = root / "release" / "version-sources.json"
    config = read_json(config_path)
    validate_configuration(root, config)

    source_path = root / config["source"]
    current = source_path.read_text(encoding="utf-8").strip()
    target = args.target_version or current
    if not VERSION_PATTERN.fullmatch(target):
        raise SystemExit(f"Invalid semantic version: {target}")

    if args.target_version:
        changed = update_versions(root, config, target)
        mismatches = find_mismatches(root, config, target)
        if mismatches:
            for mismatch in mismatches:
                print(f"ERROR: {mismatch}")
            raise SystemExit(1)

        report = {
            "from_version": current,
            "to_version": target,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "changed_files": changed,
            "protected_history": [
                path.relative_to(root).as_posix()
                for path in historical_paths(root, config)
            ],
        }
        report_path = (
            Path(args.report)
            if args.report
            else root / "reports" / f"version-update-{target}.json"
        )
        if not report_path.is_absolute():
            report_path = root / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(report_path, report)
        print(f"Version surfaces updated: {current} -> {target}")
        print(f"Changed files: {len(changed)}")
        print(report_path)
        return

    mismatches = find_mismatches(root, config, current)
    if mismatches:
        print("Version consistency validation failed:")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        raise SystemExit(1)
    print(f"Version consistency passed: {current}")


if __name__ == "__main__":
    main()
