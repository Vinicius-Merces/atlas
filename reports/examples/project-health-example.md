# Project Health Example

- **Project:** Example SaaS
- **Scope:** Web application, API, deployment, and project knowledge
- **Date:** 2026-07-30

| Dimension | Rating | Evidence |
|---|---|---|
| Product clarity | Healthy | Product requirements and metrics exist |
| Architecture | Watch | Service boundaries exist but one integration lacks ownership |
| Maintainability | Watch | Tests exist, but shared frontend components are duplicated |
| Delivery | Healthy | CI and release workflow are documented |
| Security and privacy | Watch | Privacy review exists; threat model is incomplete |
| Reliability and operations | At risk | Alerts exist, but rollback runbook is missing |
| Knowledge quality | Healthy | Memory and ADRs are current |
| Economics | Unknown | Cloud cost ownership is incomplete |

## Priority actions

1. Create rollback runbook.
2. Complete threat model.
3. Assign integration owner.
4. Establish cost allocation.
