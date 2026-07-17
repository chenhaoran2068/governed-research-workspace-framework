# v0.1.1 Release-Governance Gate

Status: historical pre-release gate for the backward-compatible v0.1.1 patch.
The published v0.1.1 tag and GitHub Release target
`b0e32d7710b70299e633df1316b6924cd87b647b` and were published on
`2026-07-15`. This retained gate describes the evidence required before that
Release; it is not an instruction or authorization for a later version.

## Purpose

Retrospectively evaluate the released v0.1.0 framework and define the evidence
required for v0.1.1 to correct public bootstrap tool metadata and add release
governance records without changing the framework workspace contract.

## Bounded Release Claim

If accepted, v0.1.1 may claim only that it:

- corrects bootstrap preview and receipt tool_version metadata to 0.1.1;
- preserves framework_version 0.1.0, existing schemas, root layout, and both
  public profiles;
- documents manual framework-source installation, update, rollback, and
  failure behavior;
- records public-material/rights review, release-integrity policy, candidate
  evidence, and draft release notes; and
- retains an explicit preview-and-confirm empty-workspace bootstrap helper.

It must not claim a system installer, runtime skill installer, project
creation, data access, agent runtime, automatic migration, clinical handling,
or research-execution authority.

## Required Gates

### R11-G1: Patch Scope And Contract Freeze

Confirm that README.md, ROADMAP.md, the release notes, script metadata, and
framework contracts agree that this is a documentation and metadata patch.
Framework version, schema versions, profile names, directory ownership, and
bootstrap permission boundary must remain unchanged.

### R11-G2: Public Material And Rights Boundary

Review every tracked candidate file for real project content, private paths,
credentials, copyrighted source payloads, restricted material, provenance, and
redistribution authority. An unresolved rights, privacy, DUA, confidentiality,
or credential concern stops release.

### R11-G3: Manual Lifecycle Contract

Document and test manual framework-source installation, validation, update,
rollback, and refusal behavior. Clearly separate a framework source checkout
from a workspace produced by bootstrap. State that v0.1.1 includes no automatic
installer, upgrader, migration, or overwrite behavior.

### R11-G4: Behavioral And Compatibility Evidence

Run local regression tests and the Windows, Ubuntu, and macOS CI matrix with
Python 3.11 and 3.14. Retain v0.1.0 tag-to-commit evidence and verify that
v0.1.1 changes neither the framework contract version nor supported profile
behavior.

### R11-G5: Release Integrity And Security Review

Record pinned Actions, dependency scope, secret-review results and limits,
clean candidate state, release notes, and an explicit GitHub immutable-release
decision. Do not present a policy-only no-rewrite rule as GitHub technical
immutability.

### R11-G6: Human Release Decision

A named accountable maintainer must authorize the exact main commit, annotated
v0.1.1 tag, and GitHub Release after R11-G1 through R11-G5 are refreshed. AI
output and passing tests cannot make this decision.

### R11-G7: Post-Release Verification

Verify that the public tag resolves to the intended tested main commit, the
GitHub Release source archive and notes match that tag, and the candidate
branch is retained or retired only by maintainer decision.

## Historical Candidate Records

- INSTALL_UPDATE_ROLLBACK.md
- PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.1.1.md
- RELEASE_INTEGRITY_POLICY_v1.md
- RELEASE_NOTES_v0.1.1.md
- V0_1_1_RELEASE_EVIDENCE.md

## External Basis

This gate uses the declared-public-interface discipline of
[Semantic Versioning](https://semver.org/), GitHub's
[tag-based release model](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
and GitHub's distinction between ordinary releases and
[technical immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).
