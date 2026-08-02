# Public Material And Rights Review: Framework v0.2.0

Status: pre-release material review for the v0.2.0 candidate. It does not
declare publication, authorization, or local installation.

## Reviewed Public Material

The candidate contains only generic Framework contracts, blank templates,
synthetic manifests, Python bootstrap code, tests, and release records. The
v0.2.0 change removes a generic root name from future synthetic full-profile
output and clarifies System ownership of manuscript/submission structure.

## Excluded Material

The candidate must not contain private workspace paths, real `Papers/`
content, Study material, manuscripts, data, credentials, user identifiers,
external full text, private memories, or unpublished source material.

## Rights And Dependency Boundary

The repository remains Apache-2.0. The bootstrap helper has no runtime Python
dependency. Test-only dependencies remain declared in
`requirements-dev.txt`; no dependency is added by v0.2.0. Public release does
not transfer rights to private material or create data, authorship,
publication, or compliance authority.

## Required Recheck

Before C4, recheck the exact candidate diff, public-boundary tests, release
notes, licenses, dependency declaration, secrets/credential absence, and
release identity. Stop on any uncertain ownership, privacy, or rights issue.
