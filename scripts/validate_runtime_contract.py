from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]


def safe_path(root: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    pure = PurePosixPath(relative.replace("\\", "/"))
    if pure.is_absolute() or ".." in pure.parts:
        return None
    path = (root / Path(*pure.parts)).resolve()
    return path if path.is_relative_to(root) else None


def collect_failures(root: Path) -> list[str]:
    failures: list[str] = []
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        contract = json.loads(
            (root / "adapters/shared/runtime-contract.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Unable to load runtime contract: {exc}"]

    if contract.get("version") != version:
        failures.append(
            f"Runtime contract version {contract.get('version')!r} "
            f"does not match VERSION {version!r}"
        )
    required_value = contract.get("required_capabilities")
    if not isinstance(required_value, list) or not all(
        isinstance(item, str) and item for item in required_value
    ):
        failures.append("required_capabilities must be an array of strings")
        required: set[str] = set()
    else:
        required = set(required_value)

    for runtime in ("claude", "codex"):
        declaration_path = (
            root / "adapters" / runtime / "runtime-declaration.json"
        )
        try:
            declaration = json.loads(
                declaration_path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{runtime}: invalid declaration: {exc}")
            continue
        if declaration.get("version") != version:
            failures.append(
                f"{runtime}: declaration version does not match VERSION"
            )
        capabilities = declaration.get("capabilities")
        if not isinstance(capabilities, list):
            failures.append(f"{runtime}: capabilities must be an array")
        else:
            missing = sorted(required - set(capabilities))
            if missing:
                failures.append(
                    f"{runtime}: missing capabilities: {', '.join(missing)}"
                )
        implementation = safe_path(root, declaration.get("implementation"))
        if implementation is None or not implementation.exists():
            failures.append(f"{runtime}: implementation path is missing or unsafe")

    shared = contract.get("shared_sources")
    if not isinstance(shared, dict):
        failures.append("shared_sources must be an object")
    else:
        for name, relative in shared.items():
            path = safe_path(root, relative)
            if path is None or not path.exists():
                failures.append(f"Shared source {name!r} is missing or unsafe")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the complete ATLAS universal runtime contract."
    )
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    failures = collect_failures(root)
    if failures:
        print("Universal runtime contract validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Universal runtime contract validation passed.")


if __name__ == "__main__":
    main()
