# v0.1.2 Current-State Correction Gate

Status: release-candidate gate. It authorizes neither merge, tag, nor
publication, and it does not itself state whether v0.1.2 is published. Resolve
that current identity only from the exact tag and GitHub Release.

## Purpose

Define the evidence required to publish a documentation-only patch that
distinguishes the published v0.1.1 Release from its retained historical
candidate records.

## Bounded Release Claim

If accepted, v0.1.2 may claim only that it corrects current-facing release
status wording and labels v0.1.1 candidate material as historical evidence.

It must not claim any change to:

- framework contract version `0.1.0`;
- manifest or system schemas;
- workspace profiles or reference tree;
- bootstrap behavior, tool version, permissions, or network boundary;
- system installation, project creation, data access, or research execution.

## Required Gates

### R12-G1: Exact Scope

Confirm the candidate changes only release-status documentation, release
evidence labels, release notes, roadmap wording, and the regression test that
protects that boundary.

### R12-G2: Current And Historical Identity

Confirm that current-facing documents identify v0.1.1 as released, while
retained v0.1.1 candidate gates, scans, and evidence explicitly identify their
historical pre-release role. Historical content may not be rewritten to invent
evidence that did not exist at the time.

### R12-G3: Public Material And Rights

Review the exact candidate for private paths, real projects, credentials,
restricted material, third-party payloads, and unsupported public claims. A
documentation-only patch does not bypass the public-material review.

### R12-G4: Validation And Compatibility

Run the complete local test suite. Confirm that all schemas, profile names,
bootstrap output, and framework behavior remain unchanged except for the
documentation and test additions recorded in the candidate diff.

### R12-G5: Integrity And Release Material

Review the exact candidate commit, clean worktree, release notes, version
references, dependency scope, and current repository protection decisions.
Record the exact commit and CI outcome before release review.

### R12-G6: Human Release Decision

A named accountable maintainer must approve the exact main commit, annotated
`v0.1.2` tag, GitHub Release title, and Release notes after R12-G1 through
R12-G5 are complete. Passing tests and AI preparation are insufficient.

### R12-G7: Post-Release Verification

Verify that the published tag and GitHub Release resolve to the approved
commit, Release notes match the released content, and the public README no
longer presents v0.1.1 as an active candidate.
