from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"


def capability_path(collection: str, name: str) -> str:
    if collection == "skills":
        path = ROOT / ".claude" / "skills" / name / "SKILL.md"
    else:
        path = ROOT / ".claude" / collection / f"{name}.md"
    if not path.is_file():
        raise ValueError(f"Missing registered {collection} capability: {name}")
    return path.relative_to(ROOT).as_posix()

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a runtime-specific ATLAS execution plan. The plan is an "
            "artifact for an AI agent or human to execute; it does not run "
            "implementation steps by itself."
        )
    )
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument(
        "--runtime",
        choices=["claude", "claude-code", "codex"],
        required=True,
    )
    parser.add_argument("--output")
    parser.add_argument(
        "--allow-missing-context",
        action="store_true",
        help="Build a draft plan even when the context pack is unavailable.",
    )
    args = parser.parse_args()

    envelope_path = Path(args.task_envelope).resolve()
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    runtime_key = "claude" if args.runtime in {"claude", "claude-code"} else "codex"
    declaration = json.loads(
        (ROOT / "adapters" / runtime_key / "runtime-declaration.json")
        .read_text(encoding="utf-8")
    )

    context_reference = str(envelope.get("context_pack", ""))
    context_path = Path(context_reference)
    if context_reference and not context_path.is_absolute():
        context_path = ROOT / context_path
    context_available = bool(context_reference and context_path.is_file())
    if not context_available and not args.allow_missing_context:
        raise SystemExit(
            "Task envelope has no available context pack. Run "
            "build_context_pack.py first or pass --allow-missing-context."
        )

    roles = [
        envelope["primary_role"],
        *envelope.get("supporting_roles", []),
    ]
    try:
        capability_sources = {
            "agents": [
                capability_path("agents", str(name))
                for name in dict.fromkeys(roles)
            ],
            "workflow": capability_path("workflows", envelope["workflow"]),
            "skills": [
                capability_path("skills", name)
                for name in envelope.get("skills", [])
            ],
            "reviews": [
                capability_path("reviews", name)
                for name in envelope["reviews"]
            ],
        }
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    registered_roles = set(registry["agents"]) | {registry["orchestrator"]}
    if envelope["primary_role"] not in registered_roles:
        raise SystemExit("Task envelope primary_role is not registered")
    if envelope["workflow"] not in registry["workflows"]:
        raise SystemExit("Task envelope workflow is not registered")

    plan = {
        "task_id": envelope["id"],
        "runtime": declaration["runtime"],
        "execution_mode": "ai-or-human-interpreted",
        "requires_external_execution": True,
        "risk": envelope.get("risk", "unspecified"),
        "primary_role": envelope["primary_role"],
        "supporting_roles": envelope.get("supporting_roles", []),
        "workflow": envelope["workflow"],
        "skills": envelope.get("skills", []),
        "reviews": envelope["reviews"],
        "validation": envelope["validation"],
        "acceptance_criteria": envelope.get("acceptance_criteria", []),
        "constraints": envelope.get("constraints", []),
        "affected_paths": envelope.get("affected_paths", []),
        "context_pack": context_reference,
        "context_available": context_available,
        "capability_sources": capability_sources,
        "steps": [
            "validate-task-envelope",
            "load-context-pack",
            "load-runtime-declaration",
            "execute-workflow",
            "run-validation",
            "run-reviews",
            "produce-execution-result",
        ],
    }
    rendered = json.dumps(plan, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
