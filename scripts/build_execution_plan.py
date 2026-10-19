from __future__ import annotations

import argparse
import json
from pathlib import Path

if __package__:
    from .validate_context_pack import verify
    from .build_context_pack import canonical_sources
else:
    from validate_context_pack import verify
    from build_context_pack import canonical_sources

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"


def capability_path(collection: str, name: str, root: Path = ROOT) -> str:
    if collection == "skills":
        path = root / ".claude" / "skills" / name / "SKILL.md"
    else:
        path = root / ".claude" / collection / f"{name}.md"
    if not path.is_file():
        raise ValueError(f"Missing registered {collection} capability: {name}")
    return path.relative_to(root).as_posix()

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
    parser.add_argument("--project-root", type=Path)
    parser.add_argument(
        "--allow-missing-context",
        action="store_true",
        help="Build a draft plan even when the context pack is unavailable.",
    )
    parser.add_argument(
        "--allow-unverified-context",
        action="store_true",
        help="Explicit legacy draft without a manifest; never bypasses failed verification",
    )
    args = parser.parse_args()

    envelope_path = Path(args.task_envelope).resolve()
    root = args.project_root.resolve(strict=True) if args.project_root else ROOT
    if args.project_root and (not envelope_path.is_relative_to(root) or (args.output and not Path(args.output).resolve().is_relative_to(root))):
        raise SystemExit('Task and plan output must remain in the explicit project root')
    if args.output and Path(args.output).resolve() == envelope_path:
        raise SystemExit('Plan output cannot overwrite its task envelope')
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    registry = json.loads((root / '.claude/registry.json').read_text(encoding="utf-8"))
    runtime_key = "claude" if args.runtime in {"claude", "claude-code"} else "codex"
    declaration = json.loads(
        (root / "adapters" / runtime_key / "runtime-declaration.json")
        .read_text(encoding="utf-8")
    )

    context_reference = str(envelope.get("context_pack", ""))
    context_path = Path(context_reference)
    if context_reference and not context_path.is_absolute():
        context_path = root / context_path
    context_available = bool(context_reference and context_path.is_file())
    if not context_available and not args.allow_missing_context:
        raise SystemExit(
            "Task envelope has no available context pack. Run "
            "build_context_pack.py first or pass --allow-missing-context."
        )

    context_verified = False
    context_limitations = []
    manifest_path = None
    if context_available:
        manifest_reference = envelope.get("context_manifest")
        manifest_path = Path(manifest_reference) if manifest_reference else context_path.with_suffix(".manifest.json")
        if not manifest_path.is_absolute():
            manifest_path = root / manifest_path
        if manifest_path.is_file():
            try:
                manifest = verify(manifest_path, context_path, task_id=envelope["id"], root=root, envelope=envelope)
            except Exception as exc:
                raise SystemExit(f"Context verification failed: {exc}") from None
            context_verified = True
            for key in ("missing_sources", "deferred_sources", "truncated_sources"):
                context_limitations.extend(f"{key}: {name}" for name in manifest.get(key, []))
        elif args.allow_unverified_context:
            context_limitations.append("Legacy context has no verified manifest; draft only")
        else:
            raise SystemExit("Context manifest is required; rebuild with build_context_pack.py or use --allow-unverified-context for a legacy draft")
    else:
        context_limitations.append("Context is unavailable; draft only")

    roles = [
        envelope["primary_role"],
        *envelope.get("supporting_roles", []),
    ]
    try:
        capability_sources = {
            "agents": [
                capability_path("agents", str(name), root)
                for name in dict.fromkeys(roles)
            ],
            "workflow": capability_path("workflows", envelope["workflow"], root),
            "skills": [
                capability_path("skills", name, root)
                for name in envelope.get("skills", [])
            ],
            "reviews": [
                capability_path("reviews", name, root)
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
        "context_verified": context_verified,
        "context_limitations": context_limitations,
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
        protected = {(root / name).resolve() for name in canonical_sources(envelope)}
        protected.update({envelope_path, (root / '.claude/registry.json').resolve(),
                          (root / 'adapters' / runtime_key / 'runtime-declaration.json').resolve()})
        if context_reference:
            protected.add(context_path.resolve())
        if manifest_path is not None:
            protected.add(manifest_path.resolve())
        if context_verified:
            protected.update((root / name).resolve() for name in manifest['sources'])
        if output in protected:
            raise SystemExit('Plan output cannot overwrite its context or source inputs')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
