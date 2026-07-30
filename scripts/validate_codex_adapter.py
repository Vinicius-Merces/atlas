from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "adapters" / "codex"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    required = [
        CODEX / "README.md",
        CODEX / "runtime-map.yaml",
        CODEX / "runtime-manifest.json",
        CODEX / "agents",
        CODEX / "commands",
        CODEX / "skills",
        CODEX / "workflows",
        CODEX / "reviews",
    ]

    for path in required:
        if not path.exists():
            fail(f"Missing Codex adapter path: {path.relative_to(ROOT)}")

    data = json.loads((CODEX / "runtime-manifest.json").read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    if data.get("version") != version:
        fail(
            f"Codex manifest version {data.get('version')} "
            f"does not match framework version {version}"
        )

    if data.get("support") != "beta-supported":
        fail("Codex adapter is not marked beta-supported")

    for name, relative in data.get("collections", {}).items():
        path = CODEX / relative
        if not path.exists():
            fail(f"Missing Codex collection '{name}': {path.relative_to(ROOT)}")

    print("Codex adapter validation passed.")


if __name__ == "__main__":
    main()
