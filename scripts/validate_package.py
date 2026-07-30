from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    version_path = ROOT / "VERSION"
    changelog_path = ROOT / "CHANGELOG.md"
    registry_path = ROOT / ".claude" / "registry.json"

    required_paths = [
        ROOT / "README.md",
        version_path,
        changelog_path,
        ROOT / "LICENSE",
        registry_path,
        ROOT / "framework",
        ROOT / ".claude" / "agents",
        ROOT / ".claude" / "contracts",
        ROOT / ".claude" / "workflows",
    ]

    for path in required_paths:
        if not path.exists():
            errors.append(f"Missing required path: {path.relative_to(ROOT)}")

    version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else ""

    if changelog_path.exists() and version and version not in changelog_path.read_text(encoding="utf-8"):
        errors.append(f"Version {version} is missing from CHANGELOG.md")

    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            if registry.get("version") != version:
                errors.append(
                    f"Registry version {registry.get('version')} does not match VERSION {version}"
                )
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid registry JSON: {exc}")

    markdown_files = list(ROOT.rglob("*.md"))
    empty_markdown = [p for p in markdown_files if not p.read_text(encoding="utf-8").strip()]
    for path in empty_markdown:
        warnings.append(f"Empty markdown file: {path.relative_to(ROOT)}")

    print(f"ATLAS package version: {version or 'unknown'}")
    print(f"Files inspected: {sum(1 for p in ROOT.rglob('*') if p.is_file())}")

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("Package validation passed.")


if __name__ == "__main__":
    main()
