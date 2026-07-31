from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "adapters" / "shared" / "task-routing-policy.json"
REGISTRY = ROOT / ".claude" / "registry.json"


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def validate_route(route: dict[str, object], registry: dict[str, object]) -> None:
    roles = set(registry["agents"]) | {str(registry["orchestrator"])}
    collections = {
        "primary_role": roles,
        "supporting_roles": roles,
        "workflow": set(registry["workflows"]),
        "skills": set(registry["skills"]),
        "reviews": set(registry["reviews"]),
    }
    for field, valid in collections.items():
        values = route.get(field, [])
        if isinstance(values, str):
            values = [values]
        unknown = sorted(set(values) - valid)
        if unknown:
            raise ValueError(
                f"Routing policy {field} contains unknown values: "
                f"{', '.join(unknown)}"
            )

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Route a task through registered ATLAS roles, skills, workflows, "
            "reviews, and validation."
        )
    )
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument(
        "--risk",
        choices=["auto", "low", "medium", "high"],
        default="auto",
    )
    parser.add_argument(
        "--runtime",
        choices=["claude-code", "codex"],
        help="Optional intended execution runtime.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Affected repository path. Repeat for multiple paths.",
    )
    parser.add_argument(
        "--acceptance",
        action="append",
        default=[],
        help="Acceptance criterion. Repeat for multiple criteria.",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Task constraint. Repeat for multiple constraints.",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matched = next(
        (
            item
            for item in policy["routes"]
            if item["task_type"] == args.task_type
        ),
        None,
    )
    route = matched or policy["fallback"]
    try:
        validate_route(route, registry)
    except ValueError as exc:
        raise SystemExit(str(exc)) from None

    risk = route.get("risk", "medium") if args.risk == "auto" else args.risk
    reviews = list(route.get("reviews", []))
    if risk == "high":
        reviews.append("governance-review")
    reviews = unique(reviews)

    envelope = {
        "id": f"task-{uuid.uuid4().hex[:12]}",
        "task_type": args.task_type,
        "summary": args.summary,
        "risk": risk,
        "runtime": args.runtime or "",
        "route_source": "matched" if matched else "fallback",
        "primary_role": route["primary_role"],
        "supporting_roles": route.get("supporting_roles", []),
        "workflow": route["workflow"],
        "skills": route.get("skills", []),
        "reviews": reviews,
        "validation": route.get("validation", ["project-appropriate-validation"]),
        "affected_paths": unique(args.path),
        "acceptance_criteria": unique(args.acceptance),
        "constraints": unique(args.constraint),
        "context_pack": "",
        "state": "routed",
    }

    rendered = json.dumps(envelope, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
