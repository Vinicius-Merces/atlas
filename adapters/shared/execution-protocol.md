# Shared Execution Protocol

Before external code execution, completed delivery claims, or primary/fallback
model admission, follow `docs/execution-assurance-guide.md` and run
`scripts/execution_assurance.py` with the explicit project root. Source trust
never grants execution authority. Functional evidence, task identity, verified
remote checkpoint, pending work and runtime limitations remain separate facts.
The gates govern runtimes; they do not implement sandboxes, scanners or catalogs.

A runtime receives a task envelope, context pack, canonical contracts, and its runtime declaration. It executes the routed workflow, performs validation and reviews, updates stable knowledge when needed, and returns an execution result.
