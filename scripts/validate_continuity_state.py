"""Check active continuity without rewriting evidence or historical artifacts."""
from __future__ import annotations

import json
from pathlib import Path

if __package__:
    from .project_memory_utils import framework_version, identity
else:
    from project_memory_utils import framework_version, identity

ROOT = Path(__file__).resolve().parents[1]
CONTINUITY = Path(".atlas/continuity")


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    version = framework_version(root)
    documents = {}
    for name in ("project-brief.json", "latest-session.json", "resume-packet.json"):
        path = root / CONTINUITY / name
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("expected an object")
        except (OSError, ValueError) as exc:
            failures.append(f"{name}: {exc}")
            continue
        documents[name] = data
        if identity(root) and data.get("project_id") != identity(root)["project_id"]:
            failures.append(f"{name}: belongs to another project")
        if data.get("framework_version") != version:
            failures.append(f"{name}: expected framework_version {version}")

    packet = documents.get("resume-packet.json", {})
    for field, name in (("project_brief", "project-brief.json"), ("latest_session", "latest-session.json")):
        expected = (CONTINUITY / name).as_posix()
        if packet.get(field) != expected:
            failures.append(f"resume-packet.json: {field} must reference {expected}")
    for field in ("memory_sources", "open_tasks", "checkpoints", "handoffs", "workstreams"):
        items = packet.get(field, [])
        if not isinstance(items, list):
            failures.append(f"resume-packet.json: {field} must be an array")
            continue
        for item in items:
            if not isinstance(item, str):
                failures.append(f"resume-packet.json: invalid {field} entry")
                continue
            path = (root / item).resolve()
            allowed = root / (".claude/memory" if field == "memory_sources" else CONTINUITY)
            if not path.is_relative_to(allowed.resolve()) or not path.is_file():
                failures.append(f"resume-packet.json: invalid {field} reference {item}")

    session = documents.get("latest-session.json", {})
    for risk in session.get("risks", []):
        if risk not in packet.get("risks", []):
            failures.append("resume-packet.json: session risk was lost")
    for action in [session.get("next_action"), *session.get("pending_work", [])]:
        if action and action not in packet.get("next_actions", []):
            failures.append("resume-packet.json: session next action or pending work was lost")
    return failures


def main() -> None:
    failures = validate(ROOT)
    if failures:
        print("Continuity state validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Continuity state validation passed")


if __name__ == "__main__":
    main()
