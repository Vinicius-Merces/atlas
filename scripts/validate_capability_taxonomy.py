#!/usr/bin/env python3
"""Validate the ATLAS agent taxonomy, skill affinities, and runtime labels."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
TAXONOMY = ROOT / "framework" / "capabilities" / "agent-taxonomy.yaml"
AGENTS_DIR = ROOT / ".claude" / "agents"
DOMAINS_DIR = ROOT / ".claude" / "memory" / "capabilities" / "domains"
AGENT_BASE = ROOT / ".claude" / "memory" / "capabilities" / "agents.base"
DOMAIN_BASE = ROOT / ".claude" / "memory" / "capabilities" / "domains.base"
MAX_DESCRIPTION_LENGTH = 240


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        raw, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(
            f"Unterminated YAML frontmatter: {path.relative_to(ROOT)}"
        ) from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML frontmatter: {path.relative_to(ROOT)}")
    return data


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    taxonomy = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    if not isinstance(taxonomy, dict):
        raise SystemExit("ERROR: capability taxonomy must be a YAML mapping")

    categories = taxonomy.get("categories")
    if not isinstance(categories, dict) or not categories:
        raise SystemExit("ERROR: capability taxonomy has no categories")

    registered_agents = set(registry.get("agents", []))
    registered_skills = set(registry.get("skills", []))
    assigned_agents: list[str] = []
    failures: list[str] = []

    for category_name, raw_category in categories.items():
        if not isinstance(raw_category, dict):
            failures.append(f"category {category_name!r} must be a mapping")
            continue

        agents = raw_category.get("agents", [])
        skills = raw_category.get("principal_skills", [])
        purpose = raw_category.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            failures.append(f"category {category_name!r} has no purpose")
        if not isinstance(agents, list) or not all(isinstance(item, str) for item in agents):
            failures.append(f"category {category_name!r} has invalid agents")
            continue
        if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
            failures.append(f"category {category_name!r} has invalid principal_skills")
            continue

        assigned_agents.extend(agents)
        unknown_skills = sorted(set(skills) - registered_skills)
        if unknown_skills:
            failures.append(
                f"category {category_name!r} references unknown skills: "
                + ", ".join(unknown_skills)
            )

        domain_path = DOMAINS_DIR / f"{category_name}.md"
        if not domain_path.is_file():
            failures.append(f"missing Obsidian domain note: {domain_path.relative_to(ROOT)}")
        else:
            try:
                domain_meta = frontmatter(domain_path)
            except ValueError as exc:
                failures.append(str(exc))
            else:
                expected = {
                    "domain": category_name,
                    "purpose": purpose,
                    "agents": agents,
                    "principal_skills": skills,
                }
                for key, value in expected.items():
                    if domain_meta.get(key) != value:
                        failures.append(
                            f"{domain_path.relative_to(ROOT)} {key!r} differs from taxonomy"
                        )

    duplicates = sorted(
        {name for name in assigned_agents if assigned_agents.count(name) > 1}
    )
    if duplicates:
        failures.append("agents assigned to multiple categories: " + ", ".join(duplicates))

    assigned_set = set(assigned_agents)
    missing = sorted(registered_agents - assigned_set)
    unknown = sorted(assigned_set - registered_agents)
    if missing:
        failures.append("registered agents missing from taxonomy: " + ", ".join(missing))
    if unknown:
        failures.append("taxonomy contains unknown agents: " + ", ".join(unknown))

    descriptions: dict[str, str] = {}
    for agent in sorted(registered_agents):
        path = AGENTS_DIR / f"{agent}.md"
        if not path.is_file():
            failures.append(f"missing canonical agent file: {path.relative_to(ROOT)}")
            continue
        try:
            meta = frontmatter(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if meta.get("name") != agent:
            failures.append(f"{path.relative_to(ROOT)} name does not match registry")
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip():
            failures.append(f"{path.relative_to(ROOT)} has no runtime label description")
            continue
        normalized = " ".join(description.split())
        if len(normalized) > MAX_DESCRIPTION_LENGTH:
            failures.append(
                f"{path.relative_to(ROOT)} description exceeds "
                f"{MAX_DESCRIPTION_LENGTH} characters"
            )
        descriptions[agent] = normalized

    reverse: dict[str, list[str]] = {}
    for agent, description in descriptions.items():
        reverse.setdefault(description.casefold(), []).append(agent)
    for agents_with_same_label in reverse.values():
        if len(agents_with_same_label) > 1:
            failures.append(
                "duplicate runtime label description: "
                + ", ".join(sorted(agents_with_same_label))
            )

    for base in (AGENT_BASE, DOMAIN_BASE):
        if not base.is_file():
            failures.append(f"missing Obsidian Base: {base.relative_to(ROOT)}")

    if failures:
        print("Capability taxonomy validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Capability taxonomy valid: "
        f"{len(registered_agents)} agents, {len(categories)} domains, "
        f"{len(registered_skills)} registered skills."
    )


if __name__ == "__main__":
    main()
