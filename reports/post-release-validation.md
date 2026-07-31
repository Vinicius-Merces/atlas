# Codex Execution Evidence

## Request

Complete ATLAS, create and merge the required pull requests, and publish the
finished release.

## Scope

Record the externally observable publication state after stable promotion.
This closeout does not alter the tagged release source or its artifacts.

## Context consulted

- Pull request #4
- Tag `v0.1.0`
- GitHub Release `v0.1.0`
- `reports/stable-promotion-validation.md`
- `adapters/codex/instructions/execution-evidence.md`

## Roles used

Codex primary agent following release manager and continuity responsibilities.
No subagents were used.

## Files changed

- `.atlas/continuity/`
- `reports/post-release-validation.md`

## Tests and checks

- Pull request #4 `validate` check
  `30605332766/job/91076294288`: passed
- Pull request #4 `validate` check
  `30605313439/job/91076239123`: passed
- Pull request head `9e1acfbf5981635fe220c1ca8682f5b14d98c2bd`:
  mergeable and clean before merge
- Stable merge commit:
  `ce18265b0ece839a862240bb1a170e7532c7b7bd`
- Tag `v0.1.0`: published
- GitHub Release: published, not draft, not prerelease
- Release assets: 9 uploaded; all GitHub SHA-256 digests matched local files

## Reviews completed

- Hosted CI, merge SHA, tag, release classification, asset count, upload state,
  sizes, and digests verified

## Findings

- No publication failure or checksum mismatch remains

## Assumptions

- None beyond the repository and GitHub states directly verified

## Remaining risks

- Gemini and Cursor remain experimental
- Runtime-specific tool invocation remains intentionally different

## Documentation and memory updates

- Latest session reconciled with the completed stable publication
- No release work remains pending
