# Agent & Skill Landscape 2026

**Research date:** 2026-08-12  
**Purpose:** guide ATLAS capability evolution for websites, SaaS products, internal systems, AI features, and production engineering without turning the framework into an uncurated prompt pack.

## Executive conclusion

ATLAS already has enough roles to behave like an engineering organization. The highest-value next step is not maximizing agent count. It is making the existing roles easier to discover, giving them a stable capability taxonomy, improving skill triggering, and exposing native/runtime-compatible packaging with measurable quality gates.

The strongest current ecosystems converge on a few ideas:

1. Keep a canonical source and generate runtime-native representations instead of maintaining divergent prompt copies.
2. Treat agent descriptions as routing metadata and human-facing purpose labels.
3. Treat skills as small, composable, progressively disclosed capability packages.
4. Separate specialist roles from reusable procedures.
5. Prefer real validation, scripts, browser checks, static analysis, and evidence over prose-only instructions.
6. Evaluate capability quality and triggering, not only file shape.
7. Package capabilities in installable domains so large libraries do not flood context or navigation.
8. Publish machine-readable catalogs and generated marketplace/runtime views when the library becomes large.

## Sources reviewed

### OpenAI Plugins

Repository: `openai/plugins`

Why it matters:

- Current Codex plugin examples package skills, agents, MCP/app integrations, hooks, and supporting assets.
- The official `build-web-apps` and Vercel-oriented material shows that production web work benefits from dedicated guidance for UI, deployment, databases, payments, and AI integration rather than one oversized full-stack prompt.
- Plugin agents use short frontmatter discovery metadata and focused bodies.

ATLAS adoption:

- Preserve canonical `name` + `description` semantics.
- Keep runtime packaging separate from role semantics.
- Add web/SaaS capabilities as composable skills before creating more agents.

### Anthropic Skills

Repository: `anthropics/skills`

Why it matters:

- Skills are self-contained folders with `SKILL.md` plus optional scripts, references, and assets.
- Discovery depends on a clear description that explains what the skill does and when it should be used.
- Complex production skills keep supporting material outside the main instruction file.

ATLAS adoption:

- Strengthen skill descriptions as trigger contracts.
- Move large reference material and deterministic helpers into bounded companion resources.
- Keep the main skill procedure concise.

### Agent Skills open standard

Reference: `agentskills.io`

Why it matters:

- Provides a portable skill model across multiple agent runtimes.
- Encourages progressive disclosure instead of loading every capability into the initial context.

ATLAS adoption:

- Keep `.claude/skills` canonical and `.agents/skills` synchronized for runtime discovery.
- Add validation for discovery metadata, references, and context size.

### GitHub Awesome Copilot

Repository: `github/awesome-copilot`

Why it matters:

- Provides a broad, actively maintained collection of custom agents, instructions, skills, hooks, workflows, and plugins rather than treating prompts as the only extension primitive.
- Its skill model follows self-contained skill folders and progressive disclosure.
- The catalog exposes search/filtering and machine-readable discovery, useful patterns once a capability library becomes large.
- Plugins group related capabilities into installable workflow-oriented bundles.

ATLAS adoption:

- Preserve distinct primitives for agents, skills, workflows, rules, hooks, and adapters instead of collapsing everything into agents.
- Add machine-readable capability discovery derived from canonical metadata.
- Evolve toward bounded installable domain bundles while retaining a global canonical taxonomy.
- Keep generated marketplace/runtime artifacts reproducible and validation-backed.

### VoltAgent Awesome Agent Skills

Repository: `VoltAgent/awesome-agent-skills`

Why it matters:

- Serves as a wide discovery radar across official and community skills from engineering teams spanning cloud, authentication, databases, testing, security, payments, observability, frontend, AI, and product work.
- Its scale shows that skill discovery quality becomes more important than raw skill count.
- The collection emphasizes curated real-world skills and explicit skill-quality standards rather than bulk-generated prompt inventory.

ATLAS adoption:

- Use large catalogs to identify capability gaps, not as direct copy sources.
- Prefer skills backed by upstream domain expertise when learning patterns for auth, databases, payments, deployment, and testing.
- Require trigger quality, bounded scope, references, validation evidence, and context discipline before admitting new ATLAS skills.

### Trail of Bits Skills

Repository: `trailofbits/skills`

Why it matters:

- Demonstrates narrow security capabilities backed by concrete tools and verification.
- Strong examples include differential review, static analysis, supply-chain risk analysis, false-positive verification, property-based testing, and mutation testing.

ATLAS adoption:

- Prefer evidence-producing security/reliability skills instead of a single generic security checklist.
- Add dependency/supply-chain and change-focused security review capabilities.

### Superpowers

Repository: `obra/superpowers`

Why it matters:

- Treats skills as a software-development methodology, not a bag of prompts.
- Emphasizes specification, implementation planning, test discipline, subagent execution, and independent review.

ATLAS adoption:

- Keep workflows explicit and composable.
- Preserve independent review after implementation.
- Add stronger skill-trigger and workflow-evaluation tests rather than copying methodology text.

### wshobson/agents

Repository: `wshobson/agents`

Why it matters:

- Demonstrates a very large multi-runtime marketplace with a single source of truth, generated runtime artifacts, capability grouping, and explicit evaluation.
- Its scale is useful as architecture evidence, but also shows why discovery and context budgeting matter more as catalogs grow.

ATLAS adoption:

- Use domain taxonomy and generated runtime views.
- Add capability evaluation and drift checks.
- Do not copy the strategy of adding roles merely to increase catalog size.

## ATLAS strengths confirmed by the research

ATLAS already contains several patterns that current ecosystems are converging toward:

- canonical agent and skill registries;
- dedicated runtime adapters;
- synchronized Codex-native skill copies;
- contracts, workflows, review gates, and evidence concepts;
- project memory and continuity artifacts;
- adapter-drift and runtime-parity concepts;
- generated human-readable catalogs.

This means the framework should evolve by tightening these primitives rather than replacing them.

## Priority capability gaps for website and SaaS work

The following capabilities should be implemented primarily as skills and attached to existing specialist agents before new agents are considered.

Status markers in this research note describe repository state as of the current capability-pack work:

- **Implemented**: canonical skill exists, is registered, has runtime discovery metadata, and is covered by ATLAS validation.
- **Pending**: remains a capability gap or has not yet been promoted into the validated skill layer.

### P0: production web quality

- **Pending** `browser-flow-validation`: exercise critical user journeys in a real browser and capture failures/evidence.
- **Implemented** `responsive-layout-audit`: validate breakpoints, overflow, stacking, typography, touch targets, and media behavior across viewport classes.
- **Implemented** `visual-regression-review`: compare intended and observed UI and classify meaningful visual regressions.
- **Pending** `seo-technical-audit`: validate crawlability, canonical URLs, redirects, sitemap/robots behavior, metadata, indexing blockers, and internal discovery.
- **Pending** `structured-data-validation`: review JSON-LD/schema markup against page meaning and supported search features.
- **Implemented** `web-performance-field-readiness`: connect performance budgets to Core Web Vitals, asset strategy, hydration, caching, and runtime behavior.

The implemented web-quality capabilities are governed by the Frontend Craft Pack. Browser-flow and search/discoverability capabilities remain separate P0 work rather than being hidden inside frontend craft.

### P0: SaaS trust boundaries

- **Implemented** `authentication-flow-review`: validate sign-in, sign-out, recovery, session lifecycle, MFA/passkey boundaries where applicable, and failure states.
- **Implemented** `authorization-boundary-review`: verify server-side authorization, object-level access, role boundaries, and privilege escalation risks.
- **Implemented** `row-level-security-review`: validate database tenant/user isolation policies and dangerous bypass paths.
- **Implemented** `secret-environment-audit`: detect accidental secret exposure, unsafe defaults, environment drift, and client/server variable boundary mistakes.
- **Pending** `supply-chain-risk-audit`: inspect dependency advisories, install scripts, maintainer/upstream risk, and suspicious package changes.

The first four capabilities are now governed by the SaaS Production Trust Model, readiness workflow, independent trust review, Claude/Codex discovery parity, and pack-specific contract validation. `supply-chain-risk-audit` remains the only unresolved P0 item in this trust-boundary group.

### P0: integrations and money paths

- **Implemented** `webhook-reliability-review`: validate signatures, idempotency, retries, ordering, replay handling, dead-letter behavior, and observability.
- **Implemented** `payment-integration-review`: validate checkout/subscription state transitions, webhook truth, duplicate processing, cancellation, entitlement, and failure recovery.
- **Implemented** `external-api-resilience-review`: validate timeout, retry, circuit-breaking, quota, pagination, schema drift, and graceful degradation behavior.

These capabilities are part of the SaaS Production Trust Pack and are routed through existing security, backend, integration, platform, reliability, and QA responsibilities rather than new provider-specific agents.

### P1: data and multi-tenant systems

- **Pending** `database-schema-review`: assess constraints, indexes, ownership, lifecycle, query patterns, and migration impact.
- **Pending** `saas-multitenancy-review`: assess tenant isolation, tenancy model, noisy-neighbor risk, quotas, background work, and operational boundaries.
- **Pending** `background-job-reliability`: assess queues, retry policy, idempotency, poison jobs, scheduling, cancellation, and observability.
- **Pending** `cache-strategy-assessment`: decide what may be cached, where, for how long, and how invalidation/consistency is proven.

### P1: growth and product quality

- **Pending** `conversion-funnel-review`: connect UX friction, instrumentation, forms, handoff states, and conversion measurement without dark patterns.
- **Pending** `analytics-implementation-audit`: compare implemented events against the canonical taxonomy, privacy rules, and decision metrics.
- **Pending** `content-discoverability-review`: align information architecture, internal links, semantic HTML, structured content, and AI/search discoverability.

### P1: capability quality itself

- **Pending** `skill-trigger-evaluation`: test whether a skill activates on positive cases and stays quiet on negative/adjacent cases.
- **Pending** `skill-quality-evaluation`: score scope clarity, evidence, repeatability, context cost, references, failure handling, and validation quality.
- **Pending** `agent-overlap-analysis`: detect redundant role scopes and ambiguous routing before adding a new agent.

## Agent creation policy

A new agent should only be introduced when all of the following are true:

- the responsibility owns a durable engineering outcome, not a single procedure;
- it has a boundary that cannot be expressed cleanly as an existing agent plus a new skill;
- it requires independent judgment or collaboration patterns distinct from adjacent agents;
- routing can distinguish it reliably from current roles;
- its addition does not make an existing agent redundant.

This policy intentionally biases ATLAS toward richer skills and fewer overlapping personas.

## Runtime label policy

ATLAS uses the canonical agent frontmatter `description` as the purpose label. Runtime adapters may surface that value in a picker, tooltip-like description, delegation UI, generated catalog, or runtime-native metadata, but must not invent a second semantic label.

A good label answers, in one scan: **what does this agent own, and why would I choose it instead of the neighboring agent?**

## Capability packaging direction

The recommended long-term packaging model is:

- **Core:** orchestration, repository mapping, implementation, QA, security, memory, release.
- **Web/SaaS:** frontend, backend, browser QA, SEO, auth, database, payments, integrations, observability.
- **AI/Data:** AI systems, RAG, evals, analytics, data engineering.
- **Platform:** cloud, DevOps, reliability, performance, FinOps.
- **Governance/Enterprise:** policy, privacy, compliance, architecture, program management.
- **Runtime Engineering:** adapters, parity, conformance, synchronization.

The taxonomy can remain global while install/discovery surfaces expose smaller domain bundles as the ecosystem grows.

## Next implementation sequence

1. **Completed:** formalize canonical runtime labels and capability taxonomy.
2. **Completed:** expose agents and domain-to-skill relationships through Obsidian capability views.
3. **Completed:** validate that every registered agent belongs to exactly one domain and every principal skill is registered.
4. **Completed:** enforce canonical agent/skill discovery descriptions and Codex skill metadata parity.
5. **In progress:** implement the P0 web/SaaS skills with deterministic evidence where possible. Frontend Craft and SaaS Production Trust packs cover the implemented items above; browser flow, SEO/structured data, and supply-chain risk remain P0.
6. **Pending:** add skill-trigger and skill-quality evaluation fixtures.
7. **Pending:** reassess the agent catalog only after the remaining P0/P1 skill layer exists.
8. **In progress:** publish runtime-native/plugin packaging from canonical sources and continuously test drift; Claude Code and Codex are first-class supported runtimes while other adapters remain experimental.

## Research guardrails

External repositories are architecture and capability references, not copy sources. New ATLAS content should remain original, respect upstream licenses, and be validated against official runtime behavior before being promoted to stable support.
