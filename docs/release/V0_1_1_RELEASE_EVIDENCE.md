# v0.1.1 Release Evidence Record

Status: pre-release candidate evidence. This record cannot authorize merge,
tagging, or publication and must be refreshed for the final intended main
commit.

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

Status: candidate documentation prepared.

Evidence: ROADMAP.md, README.md, release notes, versioning guidance, and
bootstrap metadata state that v0.1.1 changes release governance and tool
metadata only.

Next action: review the final candidate diff before R11-G6.

### R11-G2: Public Material And Rights Boundary

Status: candidate technical review prepared; human rights confirmation remains
required in R11-G6.

Evidence: PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.1.1.md records classes, scan result,
exceptions, and limits.

### R11-G3: Manual Lifecycle Contract

Status: candidate documentation prepared; final clean-install and rollback
test required before R11-G6.

Evidence: INSTALL_UPDATE_ROLLBACK.md separates source checkout from a created
workspace and prohibits automatic installation, migration, or overwrite.

### R11-G4: Behavioral And Compatibility Evidence

Status: candidate baseline available; final candidate CI required.

Evidence: the v0.1.0 release matrix passed across Windows, Ubuntu, and macOS
with Python 3.11 and 3.14. Existing local regression tests pass. Candidate
tests additionally assert tool_version 0.1.1 while framework_version remains
0.1.0.

### R11-G5: Release Integrity And Security Review

Status: candidate policy prepared; final clean-tree, history, and accessible
hosted-alert check required.

Evidence: RELEASE_INTEGRITY_POLICY_v1.md records pinned Actions, test-only
dependency ranges, scanning limits, exact tag policy, and immutable-release
deferral.

### R11-G6: Human Release Decision

Status: pending. A named accountable maintainer must authorize the exact main
commit, v0.1.1 annotated tag, and GitHub Release after R11-G1 through R11-G5
are refreshed.

### R11-G7: Post-Release Verification

Status: not applicable until v0.1.1 exists. Verify exact tag-to-main commit
resolution, Release/source-archive correspondence, and candidate-branch
retention or retirement.
