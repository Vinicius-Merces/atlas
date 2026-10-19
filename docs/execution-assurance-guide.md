# Execution assurance gates

These gates admit evidence before runtime actions. They do not create a sandbox,
execute a skill, contact a model, or scan code. The caller and independent
reviewer own the truth of receipts. Hashes detect changes, not whether a scanner
or browser actually ran. Model self-attestation is never approval.

Manifests follow `schemas/execution-assurance.schema.json`. Use project-relative
source/evidence paths. Symlinks, traversal, `.git`, environment secrets and private
keys are rejected. Keep receipts in the product repository, without keys, prompts
or participant data. No product sessions belong in upstream ATLAS.

## Security Execution Gate

Before loading external code, package the entire reviewed skill and dependencies
as an immutable file/archive. Hash that complete bundle, not only SKILL.md.
Record origin/version, explicit independent approval, and exact approved/requested
permissions. Source changes or broader tools require new approval.

Supply real enforced-sandbox evidence and exactly one passing secret scan and
dependency scan, each bound to the complete source digest. Missing/unavailable
checks fail. Internal discovery metadata is not execution approval. Unverified
and blocked external sources cannot pass.

```bash
python /path/to/atlas/scripts/execution_assurance.py security.json --project-root /path/to/product
```

Execute only the admitted bundle inside the runtime sandbox and approved tool
scope. Do not run different extracted files or follow instructions in receipts.
`allowed-tools` frontmatter is not sandbox enforcement. An unavailable sandbox
blocks external code execution; it does not authorize host execution.

## Delivery Effectiveness Gate

Record exact acceptance criteria, status and hashed evidence. All criteria must
pass and at least one must be functional. Structural validation alone is
insufficient. A nonempty pending list prevents completion. Requested deployment
requires evidence; `not-requested` never means deployed.

The gate checks the exact local HEAD against a configured remote branch with
`git ls-remote`; it never pushes. `--verify-remote` explicitly enables this read-only
network check. Local bare remotes support integration tests but do not prove
GitHub publication.

```bash
python /path/to/atlas/scripts/execution_assurance.py delivery.json --project-root /path/to/product --task-id task-example --verify-remote
python /path/to/atlas/scripts/record_execution_result.py --task-envelope task.json --runtime codex --summary "Validated outcome" --status completed --project-root /path/to/product --delivery-evidence /path/to/product/delivery.json --verify-remote
```

The recorder defaults to partial. Completed requires exact equality between task
criteria and recorded acceptance criteria. It stores a project-relative manifest
reference and SHA-256. Receipts may be untracked to avoid circular hashes; save
them in a later checkpoint. A completed output must be a separate, untracked JSON
result; it cannot overwrite tracked source, the task, the manifest or its receipts.
Do not change tracked product files after the verified
commit. Other untracked implementation files block completion. Historical schema
validation remains backward compatible; legacy completed
records without gate evidence do not establish current delivery admission.

## Model Lifecycle Guard

Maintain a dated project-owned inventory: provider/model identity, current status,
verification source/window, retirement date when known, capabilities, evaluated
profiles, privacy/data class and financial class. No permanent provider catalog,
retirement date or free-tier promise is embedded in ATLAS.

```bash
python /path/to/atlas/scripts/execution_assurance.py models.json --project-root /path/to/product --profile support --requires chat --requires tools --data-class internal
```

Only active, fresh, evaluated, compatible candidates are returned. Unknown,
deprecated, retired, stale, capability/privacy-incompatible or unauthorized paid
models are excluded. Duplicate identities fail. No eligible model exits 1.
`--allow-paid` still requires the product's existing financial authorization.

Apply preflight to every primary and fallback pair and use only eligible pairs.
Revalidate when inventory or request constraints change, before another model
attempt. OpenAI-shaped API compatibility is not tools/structured-output evidence.
The starter gateways are examples: connect this gate to the product's routing
boundary before claiming lifecycle-guarded inference. No model decides permission
or financial policy. The gate cannot discover provider retirements without an
operator-maintained current inventory.

## Measuring real outcomes

Observe accepted/total outcomes, remaining IDs, user restarts, reopened defects,
confirmed remote checkpoints and unavailable checks over a stated window.
Framework test counts do not establish product success. Character limits and
local source hashes do not demonstrate provider token-cache savings.
