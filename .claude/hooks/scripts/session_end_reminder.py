#!/usr/bin/env python3
"""SessionEnd hook. Advisory only — never blocks, exits 0 unconditionally.

Prints a reminder to capture continuity artifacts (checkpoint / close-session)
before the session's context is lost. SessionEnd cannot block per the Claude
Code hooks contract, so this never needs a deny path.
"""
from __future__ import annotations

import json
import sys

MESSAGE = (
    "[ATLAS] Session ending. If this session produced validated work, "
    "consider running /atlas-checkpoint or /atlas-close-session to capture "
    "continuity artifacts before the context is lost."
)


def main() -> int:
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    print(MESSAGE, file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
