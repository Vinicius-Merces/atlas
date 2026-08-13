---
name: file-upload-storage-design
description: "Design file upload and object-storage flows with ownership, authorization, signed access, type/size validation, safe object keys, integrity, processing, retention, deletion, and tenant isolation."
---

# File Upload & Storage Design

## Purpose

Design uploads as controlled object lifecycles with explicit ownership, authorization, integrity, processing, access, retention, and deletion behavior.

## Trigger conditions

Use for images, avatars, documents, attachments, imports, audio/video, generated files, object storage, signed URLs, or direct-to-storage browser uploads.

## Inputs

- File purpose, allowed types, maximum sizes, and expected volume
- User/tenant ownership model
- Storage provider/runtime constraints
- Access pattern: public, private, expiring, or service-only
- Processing pipeline and lifecycle/retention requirements

## Procedure

1. Define object owner, tenant scope, authoritative metadata, lifecycle states, and deletion semantics.
2. Enforce allowed size, media type, extension/content agreement, and filename normalization server-side or at the trusted storage boundary.
3. Generate unpredictable, namespace-safe object keys; do not trust user filenames as authorization boundaries.
4. Prefer scoped time-limited upload/download authorization when direct storage access is appropriate; ensure the signer cannot grant broader privileges than intended.
5. Treat upload completion and application attachment as separate states when storage and database writes can diverge.
6. Validate checksum/integrity when consequences or file size justify it.
7. Define malware/content scanning, image transformation, transcoding, metadata extraction, or quarantine when required by risk.
8. Prevent cross-tenant object access through path policy, metadata authorization, signed access, and negative tests.
9. Define orphan cleanup, replacement/version behavior, retention, archival, and hard deletion.
10. Test interrupted upload, duplicate object key, expired authorization, oversized/invalid content, processing failure, and cleanup/reconciliation.

## Outputs

- Upload/storage authority model
- Object key and metadata strategy
- Authorization and signed-access design
- Validation/processing/lifecycle controls
- Failure and reconciliation evidence

## Dependencies

- `authorization-boundary-review` and `saas-multitenancy-review` for protected tenant files
- `rate-limit-abuse-control` for expensive or public upload surfaces
- `background-job-reliability` for asynchronous processing
- `secret-environment-audit` for storage credentials and signing keys

## Limitations

Provider-specific signed URL semantics, multipart upload behavior, and malware services must be verified against the selected provider. Signed access is delegated authority, not public access by default.

## Validation

- Attempt cross-user/cross-tenant read and write access.
- Test invalid type, oversized payload, expired authorization, interrupted transfer, duplicate key, and processing failure.
- Verify orphan cleanup/deletion behavior and authoritative metadata after success.
- Confirm no privileged storage credential reaches the client.
