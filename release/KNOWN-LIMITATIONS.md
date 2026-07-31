# Known Limitations

## Runtime adapters

Claude Code is the canonical supported runtime and Codex is supported through
validated semantic parity. Gemini and Cursor remain experimental.

## Contract automation

All registered capability assets are structurally conformant with their
canonical contracts. Validators prove declared fields and controlled values;
they cannot prove the truth or quality of domain-specific reasoning. Semantic
review still requires a capable runtime or human reviewer.

## Reference implementations

Blueprints are architecture starters, not production-complete applications.

## Link validation

Repository-relative Markdown and Obsidian links are validated. External URL
availability and semantic accuracy still require review.

## Runtime-specific tool mapping

Target runtimes may expose different tools, permissions, or invocation models.
Repository tests validate structure and semantic mappings, but do not launch a
live Claude Code or Codex process.

## Evidence trust

Audit bundles validate schemas, canonical SHA-256 hashes, source commit
metadata, and record-index integrity. They are not cryptographically signed;
publish their external hashes with a trusted Git commit or release when
independent non-repudiation is required.

## Stable scope

The `0.1.x` line protects core contracts and canonical paths. Experimental
adapters and non-core integrations may still evolve without stable guarantees.
