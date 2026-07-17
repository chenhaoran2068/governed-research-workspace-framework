# Release Integrity Policy

Status: active policy introduced with v0.1.1. It defines a
maintainer-controlled procedure and does not authorize AI publication. Its
v0.1.1-specific candidate records and decisions are historical; each later
version requires its own current gate, evidence, and human release decision.

## Release Identity

Every public framework release must be an annotated tag resolving to one exact
tested main commit. Its GitHub Release must use the same tag and identify scope,
framework-contract compatibility, validation, limits, installation, and
rollback. Do not publish from a branch tip and do not silently alter a
published version. Corrections use a new release version.

## Candidate-To-Release Controls

1. Keep a candidate branch separate from main until R11-G1 through R11-G5 are
   evidenced.
2. Review the final diff, clean working tree, whitespace, reachable history,
   staged content, dependencies, and release notes.
3. Run local tests and the full CI matrix. The exact intended main commit must
   receive its own successful matrix run before tag creation.
4. Require named human approval before merge, annotated tag creation, and
   GitHub Release publication.
5. Verify tag, Release, and source archive after publication. Record defects
   as new issues or releases, not silent rewrites.

## Workflow, Dependencies, And Hosted Scanning

The workflow has read-only contents permission and pins actions/checkout and
actions/setup-python to reviewed full commit SHAs. Changes to Action references
require upstream-release identification, immutable-SHA review, and a full
matrix rerun.

The framework has no runtime Python dependency. PyYAML and jsonschema are
test-only ranges rather than hash-locked artifacts, so test reproducibility is
bounded and must not be described as a fully locked software supply chain.

At retrospective review, the public GitHub API did not expose a
security_and_analysis status. Maintainer-authenticated checks may also be
unavailable because hosted scanning features or scopes differ by account and
plan. This policy therefore does not claim that GitHub secret scanning,
Dependabot, or code scanning is enabled or clear. Manual tree and reachable
history scans remain release evidence, not a replacement for hosted security
controls.

## Immutable Release Decision For v0.1.1

Decision: defer GitHub technical immutable releases for v0.1.1 and retain an
immutable-by-policy process with compensating controls.

The existing v0.1.0 GitHub Release reports immutable false. Enabling a
repository-level immutable-release setting requires a deliberate maintainer
incident and withdrawal process, so it will not be switched on implicitly
during this documentation patch.

Compensating controls are: exact annotated tag, source identity recorded in
release notes, SHA-pinned Actions, final main CI, human authorization,
post-release verification, and no retag/no-silent-rewrite policy. This is not
equivalent to GitHub technical immutability. Reconsider enablement before every
future minor release and record the decision.
