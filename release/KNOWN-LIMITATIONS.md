# Known Limitations

## Runtime adapters

Claude Code is the canonical supported runtime and Codex is supported through
validated semantic parity. Gemini and Cursor remain experimental.

## Contract automation

Core contracts are validated structurally, but semantic review still requires
human or agent judgment.

## Reference implementations

Blueprints are architecture starters, not production-complete applications.

## Link validation

Repository-relative Markdown and Obsidian links are validated. External URL
availability and semantic accuracy still require review.

## Runtime-specific tool mapping

Target runtimes may expose different tools, permissions, or invocation models.

## Stable scope

The `0.1.x` line protects core contracts and canonical paths. Experimental
adapters and non-core integrations may still evolve without stable guarantees.
