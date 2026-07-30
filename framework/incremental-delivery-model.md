# Incremental Delivery Model

An incremental ATLAS package contains only new, changed, or deleted paths
relative to an explicit base version.

Every patch includes:

- Source and target versions
- Added files
- Modified files
- Deleted files
- SHA-256 hashes
- Application instructions
- Preflight requirements

A cumulative package can always be rebuilt from the consolidated target tree.
