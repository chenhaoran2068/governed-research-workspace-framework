# Release Notes V0.6.0

## Added

- An optional read-only workspace placement-integrity audit contract.
- Separate schemas and blank templates for an audit scope, audit report,
  placement receipt, and human-reviewed remediation queue.
- A caller-named metadata-only auditor with synthetic regression tests.

## Preserved

- Workspace-manifest schema version `1`, existing root paths, existing Study
  roots, Program records, and all installed System packages remain unchanged.
- The Framework still does not infer deeper System, Method, Study, or data
  semantics from a directory name.

## Excluded

- Automatic scans, scheduled execution, source-content reading, link/reparse
  traversal, cleanup, deletion, archiving, migration, renaming, moving, or
  repair are outside this release.
