from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "adapters/shared/source-of-truth-manifest.json"

def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    failures = []

    if data["framework_version"] != version:
        failures.append("Source-of-truth manifest version mismatch")

    for domain, spec in data["domains"].items():
        path = ROOT / spec["source"]
        if path.exists() or spec.get("optional"):
            continue
        fallback_found = any((ROOT / item).exists() for item in spec.get("fallbacks", []))
        if not fallback_found:
            failures.append(f"Missing source for {domain}: {spec['source']}")

    if failures:
        print("Source-of-truth validation failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print("Source-of-truth validation passed.")

if __name__ == "__main__":
    main()
