from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as exc:
    raise SystemExit(
        "jsonschema is required; install requirements-test.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schema-instances.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    fixture_map = load(FIXTURES)
    schemas = {path.name: path for path in sorted(SCHEMAS.glob("*.schema.json"))}

    missing = sorted(set(schemas) - set(fixture_map))
    unknown = sorted(set(fixture_map) - set(schemas))
    if missing or unknown:
        if missing:
            print(f"Missing schema fixtures: {', '.join(missing)}")
        if unknown:
            print(f"Unknown schema fixtures: {', '.join(unknown)}")
        raise SystemExit(1)

    failures: list[str] = []
    for name, schema_path in schemas.items():
        schema = load(schema_path)
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            failures.append(f"{name}: invalid schema: {exc.message}")
            continue

        fixture = fixture_map[name]
        if set(fixture) == {"path"}:
            instance_path = ROOT / fixture["path"]
            if not instance_path.is_file():
                failures.append(f"{name}: fixture path missing: {fixture['path']}")
                continue
            instance = load(instance_path)
            label = fixture["path"]
        elif set(fixture) == {"instance"}:
            instance = fixture["instance"]
            label = "inline fixture"
        else:
            failures.append(f"{name}: fixture must declare exactly path or instance")
            continue

        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{name} ({label}) {location}: {error.message}")

    if failures:
        print("Schema validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(f"Schema validation passed: {len(schemas)} schemas and fixtures")


if __name__ == "__main__":
    main()
