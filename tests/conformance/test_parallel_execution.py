from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_runtime_capabilities_include_parallel_execution() -> None:
    required = {
        "decompose-workstreams",
        "claim-resources",
        "detect-workstream-conflicts",
        "reconcile-results",
    }
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_parallel_schemas_exist() -> None:
    for relative in [
        "schemas/workstream.schema.json",
        "schemas/resource-claim.schema.json",
        "schemas/parallel-execution-manifest.schema.json",
        "schemas/reconciliation-report.schema.json",
    ]:
        assert (ROOT / relative).is_file()
