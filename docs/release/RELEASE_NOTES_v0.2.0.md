# Framework v0.2.0 Release Notes

Release identity must be verified from the exact `v0.2.0` annotated tag and
matching GitHub Release. This file describes the v0.2.0 contract; it does not
independently declare a release published.

## Changed

- New confirmed `framework_integrated` bootstraps no longer create `Papers/`
  or a `roots.papers` manifest entry.
- Project manuscript and submission structures are explicitly owned by the
  concrete installed System rather than a universal Framework root.
- Framework bootstrap output and tool identities are both `0.2.0`.
- The public synthetic multi-system example declares Framework `0.2.0`; its
  two synthetic System manifests declare the fixed compatible range
  `>=0.1.0 <0.3.0`.

## Compatibility

- `standalone` remains unchanged.
- Workspace-manifest schema remains version `1`.
- Existing manifests with `roots.papers: Papers` remain valid and are not
  automatically changed.
- Updating Framework source does not inspect, move, delete, or archive a
  physical `Papers/` directory.
- Real Systems must separately declare and validate v0.2 compatibility.

## Not Added

v0.2.0 adds no system installer, runtime adapter, project migration, data
operation, manuscript/submission executor, agent, access authority, or local
cleanup command.
