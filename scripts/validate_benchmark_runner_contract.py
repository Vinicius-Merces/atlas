#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"Benchmark runner contract validation failed: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a frozen target runner contract")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--schema")
    parser.add_argument("--target-root")
    parser.add_argument("--github-output")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    schema_path = Path(args.schema).resolve() if args.schema else DEFAULT_SCHEMA
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda err: list(err.path))
    if errors:
        detail = "; ".join(f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors[:8])
        fail(detail)

    if args.target_root:
        target_root = Path(args.target_root).resolve()
        app_dir = (target_root / manifest["app_dir"]).resolve()
        try:
            app_dir.relative_to(target_root)
        except ValueError:
            fail("app_dir escapes target checkout")
        if not app_dir.is_dir():
            fail(f"app_dir does not exist: {manifest['app_dir']}")

    output = {
        "app_dir": manifest["app_dir"],
        "install_command": manifest["install_command"],
        "test_command": manifest["test_command"],
        "build_command": manifest["build_command"],
        "start_command": manifest["start_command"],
        "port": str(manifest["port"]),
        "health_path": manifest["health_path"],
        "origin_env": manifest["origin_env"],
        "browser_routes": ",".join(manifest["browser_routes"]),
    }
    if args.github_output:
        path = Path(args.github_output)
        with path.open("a", encoding="utf-8") as handle:
            for key, value in output.items():
                handle.write(f"{key}={value}\n")

    print(json.dumps({"manifest": str(manifest_path), **output}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
