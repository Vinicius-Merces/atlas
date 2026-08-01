---
name: rag-architecture-assessment
description: "Evaluate retrieval-augmented generation architecture for grounding, security, freshness, quality, latency, and cost."
---

# RAG Architecture Assessment Skill

## Purpose

Evaluate retrieval-augmented generation architecture for grounding, security,
freshness, quality, latency, and cost.

## Checks

- Corpus definition
- Source provenance
- Access control
- Ingestion and refresh
- Chunking strategy
- Metadata strategy
- Embedding choice
- Retrieval and reranking
- Citation behavior
- Evaluation set
- Prompt injection risk
- Cost and latency budgets
- Fallback behavior

## Output

- Architecture findings
- Retrieval risks
- Evaluation plan
- Security controls
- Improvement recommendations

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to rag architecture assessment.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
