#!/usr/bin/env python3
"""PreToolUse hook. Blocking.

Denies creating a new .md/.txt file directly at the project root unless its
name is on the root allowlist. Files written anywhere inside a subdirectory
(docs/, .claude/, or any other) are never affected — only new stray files
created at the top level of the working directory, which is the pattern this
hook exists to prevent (see .claude/contracts/hook-contract.md).

Fails open: any unexpected error allows the write rather than blocking it.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT_ALLOWLIST = {
    "readme.md",
    "claude.md",
    "agents.md",
    "contributing.md",
    "changelog.md",
}

DOC_PATTERN = re.compile(r"\.(md|txt)$", re.IGNORECASE)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") != "Write":
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    if not file_path or not DOC_PATTERN.search(file_path):
        return 0

    cwd = payload.get("cwd") or ""
    if not cwd:
        return 0

    directory = os.path.dirname(file_path)
    basename = os.path.basename(file_path).lower()
    # os.path.join(cwd, directory) resolves a relative (including empty)
    # directory against cwd, while leaving an already-absolute directory
    # untouched — so both absolute and relative tool_input.file_path values
    # compare correctly against cwd.
    resolved_directory = os.path.normpath(os.path.join(cwd, directory))
    is_at_root = resolved_directory == os.path.normpath(cwd)

    if is_at_root and basename not in ROOT_ALLOWLIST:
        reason = (
            f"Blocked: creating a new top-level '{os.path.basename(file_path)}' "
            "was not explicitly requested. Put documentation inside an existing "
            "directory (docs/, .claude/, etc.) or ask the user before adding a "
            "new root-level doc file."
        )
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                }
            )
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
