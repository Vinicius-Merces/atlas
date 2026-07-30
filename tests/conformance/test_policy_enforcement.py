from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_runtime_capabilities_include_policy_enforcement() -> None:
    required = {
        "evaluate-policies",
        "validate-version-transitions",
        "preflight-manual-deployments",
        "manage-policy-exceptions",
    }
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_policy_schemas_exist() -> None:
    for relative in [
        "schemas/policy-rule.schema.json",
        "schemas/policy-evaluation-report.schema.json",
        "schemas/policy-exception.schema.json",
        "schemas/deployment-preflight-report.schema.json",
    ]:
        assert (ROOT / relative).is_file()
