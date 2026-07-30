from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "compatibility" / "core-contracts.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail("Missing core contract manifest")

    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid core contract manifest: {exc}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if data.get("version") != version:
        fail(
            f"Core contract manifest version {data.get('version')} "
            f"does not match VERSION {version}"
        )

    for contract in data.get("contracts", []):
        path = ROOT / contract["path"]
        if not path.exists():
            fail(f"Missing contract file: {contract['path']}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"Empty contract file: {contract['path']}")

    for relative in data.get("canonical_paths", []):
        if not (ROOT / relative).exists():
            fail(f"Missing canonical path: {relative}")

    print(
        f"Core contracts valid: {len(data.get('contracts', []))} contracts, "
        f"{len(data.get('canonical_paths', []))} canonical paths"
    )


if __name__ == "__main__":
    main()
