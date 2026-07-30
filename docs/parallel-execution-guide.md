# Parallel Execution Guide

Parallelize only independent work. Shared schemas, migrations, API contracts,
canonical memory, and architecture decisions require coordinated ownership.

Use exclusive claims for resources that cannot be safely edited concurrently.
Use shared claims for read-only or intentionally coordinated access.
