#!/usr/bin/env python3
"""Generate human-readable agent and skill catalogs from canonical frontmatter."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".claude" / "agents"
SKILLS_DIR = ROOT / ".claude" / "skills"
AGENT_CATALOG = ROOT / "docs" / "agent-catalog.md"
SKILL_CATALOG = ROOT / "docs" / "skill-catalog.md"


def read_frontmatter(path: Path) -> dict[str, object]:
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


def title(name: str) -> str:
    acronyms = {
        "adr": "ADR",
        "ai": "AI",
        "api": "API",
        "ci": "CI",
        "codex": "Codex",
        "devops": "DevOps",
        "finops": "FinOps",
        "qa": "QA",
        "rag": "RAG",
        "runtime": "Runtime",
        "ux": "UX",
    }
    return " ".join(acronyms.get(word, word.title()) for word in name.split("-"))


def entry(path: Path, expected_name: str) -> tuple[str, str]:
    data = read_frontmatter(path)
    name = data.get("name")
    description = data.get("description")
    if name != expected_name:
        raise ValueError(
            f"Frontmatter name mismatch in {path.relative_to(ROOT)}: "
            f"expected {expected_name!r}, got {name!r}"
        )
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"Missing description: {path.relative_to(ROOT)}")
    return name, " ".join(description.split())


def agent_entries() -> list[tuple[str, str]]:
    entries = [
        entry(path, path.stem)
        for path in AGENTS_DIR.glob("*.md")
        if path.name.lower() != "readme.md"
    ]
    return sorted(entries)


def skill_entries() -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        entries.append(entry(path, path.parent.name))
    return sorted(entries)


def render_catalog(kind: str, source: str, entries: list[tuple[str, str]]) -> str:
    plural = f"{kind}s"
    lines = [
        f"# {kind} Catalog",
        "",
        (
            f"Canonical, generated inventory of every {kind.lower()} under "
            f"`{source}`. Each entry mirrors its frontmatter `description`, "
            "which is the routing and discovery summary used by AI runtimes."
        ),
        "",
        (
            "Regenerate both capability catalogs with "
            "`python scripts/generate_capability_catalogs.py`. "
            "Use `--check` in validation and CI."
        ),
        "",
        f"Total: {len(entries)} {plural.lower()}.",
        "",
    ]
    for name, description in entries:
        lines.extend(
            [
                f"## {title(name)}",
                "",
                f"`{name}`. {description}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    return {
        AGENT_CATALOG: render_catalog(
            "Agent", ".claude/agents/", agent_entries()
        ),
        SKILL_CATALOG: render_catalog(
            "Skill", ".claude/skills/<skill-name>/SKILL.md", skill_entries()
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated catalogs differ from canonical frontmatter.",
    )
    args = parser.parse_args()

    stale: list[str] = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
            print(f"Generated {path.relative_to(ROOT)}")

    if stale:
        print("Stale capability catalogs:")
        for path in stale:
            print(f"- {path}")
        return 1
    if args.check:
        print("Capability catalogs are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
