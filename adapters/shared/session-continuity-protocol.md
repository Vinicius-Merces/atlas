# Shared Session Continuity Protocol

## Start

1. Read `AGENTS.md`.
2. Read `VERSION`.
3. Read the project brief.
4. Read the latest session brief and resume packet.
5. Validate memory freshness.
6. Inspect current repository and task state.

## Close

1. Record completed work and changed files.
2. Record validation and reviews.
3. Record decisions, risks, and pending work.
4. Update durable memory when appropriate.
5. Create a new session brief.
6. Rebuild the resume packet.
7. Validate active continuity with `python scripts/validate_continuity_state.py`.
   Preserve session risks, next action and pending work; do not rewrite historical
   evidence to conceal drift. Follow `docs/project-delivery-feedback.md` for
   checkpoints after validated batches and product-specific acceptance evidence.

## Product repositories

Use `scripts/project_memory.py start --project-root <product-root>` before
resuming product work, and its `close` action with a staged identity-bound session
after a checkpoint. Initialize once with `init`. Product knowledge stays in that
product; upstream ATLAS receives framework changes only. See
`docs/project-local-memory-guide.md`.
