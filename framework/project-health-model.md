# Project Health Model

Project health describes how safely and effectively a software system can be
understood, changed, operated, and evolved.

## Health dimensions

### Product clarity

The project has clear users, outcomes, scope, ownership, and success measures.

### Architecture

Boundaries, data ownership, integrations, and decisions are understandable.

### Codebase maintainability

The repository is navigable, tested, consistent, and free from uncontrolled
duplication or coupling.

### Delivery system

Build, test, review, release, and rollback paths are reliable.

### Security and privacy

Trust boundaries, permissions, secrets, and sensitive data are governed.

### Reliability and operations

Critical journeys are observable, recoverable, and supported by runbooks.

### Knowledge quality

Documentation, memory, ADRs, ownership, and operational guidance are current.

### Economics

Cost, effort, maintenance burden, and strategic flexibility are understood.

## Scoring

Each dimension may be rated:

- **Healthy**
- **Watch**
- **At risk**
- **Critical**
- **Unknown**

Unknown is not healthy. Missing evidence should remain visible.
