"""Shared project-local identity; product VERSION is not the framework version."""
from __future__ import annotations

import json
from pathlib import Path

CONFIG = Path('.atlas/project-memory.json')


def identity(root: Path) -> dict:
    path = root / CONFIG
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


def framework_version(root: Path) -> str:
    return identity(root).get('framework_version') or (root / 'VERSION').read_text(encoding='utf-8').strip()
