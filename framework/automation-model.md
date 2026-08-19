# Automation Model

ATLAS automates repeatable governance and validation while preserving human judgment for ambiguous or high-impact decisions.

## Automation categories

### Structural automation

Validates required files, metadata, paths, schemas, and naming conventions.

### Policy automation

Evaluates explicit rules that can be represented deterministically.

### Quality automation

Runs tests, linting, type checks, security checks, package validation, and other required quality gates selected through `framework/quality-gates-model.md`.

### Release automation

Builds versioned artifacts, generates manifests, verifies integrity, and publishes evidence.

### Runtime automation

Transforms canonical ATLAS definitions into environment-specific adapters.

### AI automation

Uses models inside repeatable workflows such as classification, extraction, summarization, routing, drafting, retrieval, or tool-driven operations.

AI automation must be designed as a production workflow rather than a one-shot prompt.

## Automation principles

- Automate stable rules, not unresolved judgment.
- Make failures actionable.
- Preserve evidence.
- Avoid silent mutation.
- Keep automation reproducible.
- Allow explicit, documented exceptions.
- Treat automation code as production code.
- Separate model suggestion from authoritative system permission.
- Bound retries, timeouts, concurrency, and spend/compute.

## AI automation reliability contract

When a model call participates in an automated workflow, define where applicable:

- trigger and input source
- schema/validation for model output
- idempotency or deduplication key
- queue/background-job ownership
- concurrency limit
- model/provider capability profile
- timeout budget
- retry policy with backoff/jitter for retry-safe failures
- maximum attempts and total execution budget
- dead-letter/quarantine path for exhausted or invalid work
- fallback model/provider policy
- partial-failure behavior
- audit/correlation identifier
- human approval boundary for consequential actions
- privacy/data handling policy
- observability and cost/compute evidence

Do not place an LLM between a user request and a consequential side effect without authoritative server-side validation and permission checks.

## Retry and side-effect policy

A retry is safe only if repeating the operation cannot create duplicate or conflicting effects, or if the workflow provides idempotency/deduplication.

For model-only transformations, bounded retries may be appropriate for transport failures, capacity errors, or invalid structured output.

For tool actions, emails, payments, writes, tickets, deployments, or external mutations, retries must respect the downstream idempotency contract. If execution status is unknown, prefer reconciliation over blind replay.

## Structured output policy

Machine-consumed model output must be validated before it reaches authoritative business logic.

At minimum:

- define the schema or accepted shape;
- reject malformed/unknown fields according to the consumer contract;
- validate identifiers and permissions against authoritative data;
- separate recoverable format errors from semantic failures;
- record invalid-output rates when they matter operationally.

## Human approval

Human approval is appropriate when model-driven automation can cause material financial, security, legal, privacy, destructive, customer-facing, or irreversible impact.

Approval should show the proposed action, relevant evidence, and consequences rather than asking a reviewer to approve an opaque model conclusion.

## Model/provider portability

Use `framework/llm-provider-routing-model.md` when an automation can use hosted, self-hosted, local/Ollama, or fallback model providers.

The workflow should request a logical capability profile. Provider-specific model names and endpoints belong at the adapter/configuration boundary when practical.

## Operational evidence

A production automation should make it possible to determine:

- what triggered the run;
- which work item/input was processed;
- current status and attempt count;
- model/provider used when applicable;
- why it failed;
- whether a side effect occurred;
- whether it is safe to retry;
- whether fallback or human review was invoked;
- what final result was committed.

## Failure policy

Automation must fail explicitly rather than silently dropping work.

Use the project's appropriate combination of:

- retry/backoff
- dead-letter or quarantine state
- operator-visible failed status
- alerting
- compensating action
- reconciliation job
- manual replay after verification

The selected mechanism must fit the workflow's consequence and traffic profile.
