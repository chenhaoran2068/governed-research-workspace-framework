# Release Notes: v0.1.1

Status: release-note source. The GitHub Release records the exact final main
commit, validation links, human authorization, and post-release verification.

## Patch Scope

v0.1.1 is a backward-compatible release-governance patch for the public
Workspace Framework.

## Changed

- Correct bootstrap preview and receipt tool_version from the stale
  0.1.0-framework-candidate label to 0.1.1.
- Add manual source-package installation, update, rollback, and failure
  documentation.
- Add public-material/rights review, release-integrity policy, release gate,
  candidate evidence, and release-notes records.
- Correct the versioning documentation to distinguish an immutable public
  contract by policy from GitHub technical immutable releases.

## Unchanged

- Framework contract version remains 0.1.0.
- Workspace, system, and project-binding schemas remain unchanged.
- Profile names and their output roots remain unchanged.
- Bootstrap remains explicit, preview-first, human-confirmed, no-overwrite,
  no-data, no-project, and no-system-installation.
- No runtime dependency, data-access, system-installation, agent-runtime, or
  research-execution capability is added.

## Compatibility And Rollback

Users may retain existing v0.1.0-created workspaces. Updating the framework
source package does not migrate or modify them. Use the exact-tag procedures
in INSTALL_UPDATE_ROLLBACK.md for a clean update or source-only rollback.

## Validation

Before publication, replace this section with the exact final main commit and
links to the final local test run, Windows/Ubuntu/macOS Python 3.11/3.14 CI
matrix, material/rights review, and completed R11 evidence record.

## Integrity Limit

GitHub technical immutable releases are deferred for v0.1.1. The release uses
the compensating controls recorded in RELEASE_INTEGRITY_POLICY_v1.md and must
not be described as technically immutable.
