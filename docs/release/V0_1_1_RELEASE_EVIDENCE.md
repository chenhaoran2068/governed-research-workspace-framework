# v0.1.1 Release Evidence Record

Status: historical pre-release candidate evidence for the published v0.1.1
Release. The final published tag and GitHub Release target
`b0e32d7710b70299e633df1316b6924cd87b647b` and were published on
`2026-07-15`. Candidate statuses, pending actions, and next-action wording
below are preserved as the historical record captured before that Release;
they must not be read as current instructions or authorization for a later
version.

## Release Identity Under Review

| Field | Candidate value |
| --- | --- |
| Package | governed-research-workspace-framework |
| Intended version | v0.1.1 |
| Candidate branch | v0.1.1-release-governance |
| Release type | backward-compatible metadata and governance patch |
| Framework contract version | 0.1.0, unchanged |
| Release assets | GitHub-generated source archives only |

## Retrospective v0.1.0 Findings

- The public v0.1.0 annotated tag resolves to
  cf90e3003d0117e7d99aaeed364401767db38692, the released main commit.
- GitHub Release v0.1.0 exists, has no uploaded assets, and reports immutable
  false.
- Its Windows, Ubuntu, and macOS Python 3.11/3.14 CI matrix completed
  successfully.
- The package had public boundary documentation and pinned Actions, but lacked
  a manual package lifecycle contract, comprehensive material/rights record,
  explicit immutable-release decision, and gate evidence record.
- The bootstrap helper emitted stale tool_version 0.1.0-framework-candidate.
  v0.1.1 corrects that metadata without changing framework_version 0.1.0.

## Candidate Gate Status

### R11-G1: Patch Scope And Contract Freeze

Historical candidate-time status: candidate documentation prepared.

Evidence: ROADMAP.md, README.md, release notes, versioning guidance, and
bootstrap metadata state that v0.1.1 changes release governance and tool
metadata only.

Candidate documentation audit completed at
10c979e15ee1abddeba4286954b2823e2bb23716.

Next action: review the final candidate diff before R11-G6.

### R11-G2: Public Material And Rights Boundary

Historical candidate-time status: candidate technical review prepared; human rights confirmation remained
required in R11-G6.

Evidence: PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.1.1.md records classes, scan result,
exceptions, and limits.

The current-tree and seven-commit reachable-history pattern scans reported zero
credential and known-private-path matches at
10c979e15ee1abddeba4286954b2823e2bb23716.

### R11-G3: Manual Lifecycle Contract

Historical candidate-time status: candidate documentation prepared; final clean-install and rollback
test were required before R11-G6.

Evidence: INSTALL_UPDATE_ROLLBACK.md separates source checkout from a created
workspace and prohibits automatic installation, migration, or overwrite.

An isolated lifecycle test cloned candidate
10c979e15ee1abddeba4286954b2823e2bb23716, ran 19 tests successfully, created
an empty workspace only after preview and confirmation, verified receipt
tool_version 0.1.1 and framework_version 0.1.0, rolled back to released
v0.1.0 and ran 18 tests successfully, then restored the candidate and reran
all 19 tests successfully.

### R11-G4: Behavioral And Compatibility Evidence

Historical candidate-time status: candidate baseline available; final candidate CI required.

Evidence: the v0.1.0 release matrix passed across Windows, Ubuntu, and macOS
with Python 3.11 and 3.14. Existing local regression tests pass. Candidate
tests additionally assert tool_version 0.1.1 while framework_version remains
0.1.0.

Candidate GitHub Actions run 29397040167 completed successfully on commit
10c979e15ee1abddeba4286954b2823e2bb23716 for Windows, Ubuntu, and macOS with
Python 3.11 and 3.14.

### R11-G5: Release Integrity And Security Review

Historical candidate-time status: candidate policy prepared; final clean-tree, history, and accessible
hosted-alert check required.

Evidence: RELEASE_INTEGRITY_POLICY_v1.md records pinned Actions, test-only
dependency ranges, scanning limits, exact tag policy, and immutable-release
deferral.

GitHub alert APIs were checked with maintainer credentials during candidate
review. Dependabot returned 403, code scanning returned 404, and secret
scanning was unavailable to the current credential; therefore no claim is made
that hosted scanning is enabled or clear.

### R11-G6: Human Release Decision

Historical candidate-time status: pending. A named accountable maintainer had to authorize
the exact main commit, v0.1.1 annotated tag, and GitHub Release after R11-G1
through R11-G5 were refreshed.

### R11-G7: Post-Release Verification

Historical candidate-time status: not applicable until v0.1.1 existed. Verify exact
tag-to-main commit resolution, Release/source-archive correspondence, and
candidate-branch retention or retirement.
