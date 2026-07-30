from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_supported_runtimes_include_handoff_capabilities() -> None:
    required = {"create-checkpoints", "handoff-tasks", "resume-execution"}
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_handoff_schemas_exist() -> None:
    for relative in [
        "schemas/checkpoint.schema.json",
        "schemas/handoff-manifest.schema.json",
        "schemas/continuation-plan.schema.json",
    ]:
        assert (ROOT / relative).is_file()
