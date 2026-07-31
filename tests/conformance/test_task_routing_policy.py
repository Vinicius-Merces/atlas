from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_task_routing_policy_resolves_registered_capabilities() -> None:
    registry = load(".claude/registry.json")
    policy = load("adapters/shared/task-routing-policy.json")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert policy["version"] == version

    routes = [*policy["routes"], policy["fallback"]]
    assert len({route["task_type"] for route in policy["routes"]}) == len(
        policy["routes"]
    )
    valid_roles = set(registry["agents"]) | {registry["orchestrator"]}
    for route in routes:
        assert route["primary_role"] in valid_roles
        assert set(route.get("supporting_roles", [])) <= valid_roles
        assert route["workflow"] in registry["workflows"]
        assert set(route.get("skills", [])) <= set(registry["skills"])
        assert set(route.get("reviews", [])) <= set(registry["reviews"])
        assert route.get("risk") in {"low", "medium", "high"}
