from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_runtime_capabilities_include_portable_memory() -> None:
    required = {
        "build-project-briefs",
        "create-session-briefs",
        "audit-memory-freshness",
        "build-resume-packets",
    }
    for runtime in ["claude", "codex"]:
        declaration = load(f"adapters/{runtime}/runtime-declaration.json")
        assert required <= set(declaration["capabilities"])

def test_portable_memory_schemas_exist() -> None:
    for relative in [
        "schemas/project-brief.schema.json",
        "schemas/session-brief.schema.json",
        "schemas/resume-packet.schema.json",
    ]:
        assert (ROOT / relative).is_file()
