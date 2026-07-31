from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "adapters" / "codex"
REGISTRY = ROOT / ".claude" / "registry.json"
MAP_NAMES = {
    "agents": "agent-map.json",
    "commands": "command-map.json",
    "skills": "skill-map.json",
    "workflows": "workflow-map.json",
    "reviews": "review-map.json",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    required = [
        CODEX / "README.md",
        CODEX / "runtime-map.yaml",
        CODEX / "runtime-manifest.json",
        CODEX / "runtime-declaration.json",
        CODEX / "catalogs",
        CODEX / "generated",
        CODEX / "agents",
        CODEX / "commands",
        CODEX / "skills",
        CODEX / "workflows",
        CODEX / "reviews",
        ROOT / "AGENTS.md",
        ROOT / ".agents" / "skills",
    ]

    for path in required:
        if not path.exists():
            fail(f"Missing Codex adapter path: {path.relative_to(ROOT)}")

    data = json.loads((CODEX / "runtime-manifest.json").read_text(encoding="utf-8"))
    declaration = json.loads(
        (CODEX / "runtime-declaration.json").read_text(encoding="utf-8")
    )
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    expected_support = "supported" if "-" not in version else "beta-supported"

    if data.get("version") != version:
        fail(
            f"Codex manifest version {data.get('version')} "
            f"does not match framework version {version}"
        )

    if data.get("support") != expected_support:
        fail(f"Codex adapter is not marked {expected_support}")

    if declaration.get("version") != version:
        fail("Codex runtime declaration version does not match VERSION")
    if declaration.get("support") != expected_support:
        fail(f"Codex runtime declaration is not {expected_support}")
    if declaration.get("canonical") is not False:
        fail("Codex runtime declaration must not claim canonical status")

    for name, relative in data.get("collections", {}).items():
        path = CODEX / relative
        if not path.exists():
            fail(f"Missing Codex collection '{name}': {path.relative_to(ROOT)}")

    for name, relative in data.get("shared", {}).items():
        path = (CODEX / relative).resolve()
        if not path.exists():
            fail(f"Missing shared Codex source '{name}': {path}")

    sync = subprocess.run(
        [sys.executable, "scripts/sync_codex_adapter.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if sync.returncode:
        details = sync.stdout.strip() or sync.stderr.strip()
        fail(f"Codex generated artifacts are stale:\n{details}")

    native_skills = subprocess.run(
        [sys.executable, "scripts/sync_native_skills.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if native_skills.returncode:
        details = native_skills.stdout.strip() or native_skills.stderr.strip()
        fail(f"Native runtime skills are stale:\n{details}")

    manifest = json.loads(
        (CODEX / "generated" / "catalog-manifest.json").read_text(encoding="utf-8")
    )
    if manifest.get("version") != version:
        fail("Codex catalog manifest version does not match VERSION")

    required_entry_fields = {
        "canonical_name",
        "canonical_path",
        "adapter_path",
        "parity_type",
        "status",
        "notes",
        "version",
    }
    for collection, map_name in MAP_NAMES.items():
        entries = json.loads(
            (CODEX / "generated" / map_name).read_text(encoding="utf-8")
        ).get("entries", [])
        expected_names = set(registry.get(collection, []))
        actual_names = {entry.get("canonical_name") for entry in entries}
        if actual_names != expected_names or len(entries) != len(expected_names):
            fail(f"Codex {collection} map does not match the registry")
        if manifest.get("collections", {}).get(collection) != len(expected_names):
            fail(f"Codex {collection} manifest count does not match the registry")

        for entry in entries:
            missing = required_entry_fields - entry.keys()
            if missing:
                fail(
                    f"Codex {collection} map entry {entry.get('canonical_name')} "
                    f"is missing: {', '.join(sorted(missing))}"
                )
            if entry["version"] != version:
                fail(
                    f"Codex {collection} map entry {entry['canonical_name']} "
                    "has a stale version"
                )
            for field in ("canonical_path", "adapter_path"):
                if not (ROOT / entry[field]).is_file():
                    fail(
                        f"Codex {collection} map entry {entry['canonical_name']} "
                        f"has an invalid {field}: {entry[field]}"
                    )

    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for canonical_reference in [
        ".claude/registry.json",
        ".claude/contracts/",
        ".claude/memory/",
        "adapters/codex/",
    ]:
        if canonical_reference not in agents_text:
            fail(f"AGENTS.md does not reference {canonical_reference}")

    orchestrator_adapter = (
        CODEX / "agents" / "orchestrator.md"
    ).read_text(encoding="utf-8")
    if ".claude/agents/orchestrator.md" not in orchestrator_adapter:
        fail("Codex orchestrator does not reference the canonical agent")
    for stale_reference in [
        ".claude/orchestrator.md",
        "../../.claude/",
        "../../framework/",
    ]:
        if stale_reference in orchestrator_adapter:
            fail(f"Codex orchestrator contains stale path: {stale_reference}")

    print("Codex adapter validation passed.")


if __name__ == "__main__":
    main()
