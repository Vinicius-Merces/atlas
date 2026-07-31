from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "task-envelope.schema.json"


def fail(message: str) -> None:
    print(f"Task envelope validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path, label: str) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{label} not found: {path}")
    except json.JSONDecodeError as exc:
        fail(
            f"invalid JSON in {label.lower()} {path}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
    except OSError as exc:
        fail(f"cannot read {label.lower()} {path}: {exc}")


def error_location(path: list[object]) -> str:
    location = "$"
    for part in path:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate an ATLAS task envelope against its JSON Schema."
    )
    parser.add_argument("task_envelope", type=Path, help="Task envelope JSON file")
    args = parser.parse_args(argv)

    data = load_json(args.task_envelope, "Task envelope")
    schema = load_json(SCHEMA, "Task envelope schema")
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    except SchemaError as exc:
        fail(f"invalid JSON Schema {SCHEMA}: {exc.message}")

    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )
    if errors:
        details = "; ".join(
            f"{error_location(list(error.absolute_path))}: {error.message}"
            for error in errors
        )
        fail(details)

    print(f"Valid task envelope: {data['id']}")


if __name__ == "__main__":
    main()
