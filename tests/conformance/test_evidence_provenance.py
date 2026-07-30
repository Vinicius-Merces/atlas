from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_runtime_capabilities_include_evidence_and_provenance() -> None:
    required = {
        "create-evidence-records",
        "map-change-provenance",
        "record-manual-deployments",
        "build-audit-bundles",
        "verify-evidence-integrity",
    }
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_evidence_schemas_exist() -> None:
    for relative in [
        "schemas/evidence-record.schema.json",
        "schemas/change-provenance.schema.json",
        "schemas/manual-deployment-receipt.schema.json",
        "schemas/audit-bundle-manifest.schema.json",
    ]:
        assert (ROOT / relative).is_file()
