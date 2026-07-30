from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_runtime_capabilities_include_memory_governance() -> None:
    required = {
        "audit-memory-drift",
        "validate-sources-of-truth",
        "build-reconciliation-proposals",
        "refresh-continuity-artifacts",
    }
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_memory_governance_schemas_exist() -> None:
    for relative in [
        "schemas/memory-drift-report.schema.json",
        "schemas/contradiction-register.schema.json",
        "schemas/reconciliation-proposal.schema.json",
        "schemas/source-of-truth-manifest.schema.json",
    ]:
        assert (ROOT / relative).is_file()

def test_source_of_truth_manifest_matches_version() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = load("adapters/shared/source-of-truth-manifest.json")
    assert manifest["framework_version"] == version
