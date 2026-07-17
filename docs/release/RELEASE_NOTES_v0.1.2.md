# Release Notes: v0.1.2

Status: release-note source for an exact approved v0.1.2 commit. This file
does not itself state whether v0.1.2 is published; resolve that current
identity only from the exact tag and GitHub Release.

## Scope

v0.1.2 is a documentation-only correction. It separates the published v0.1.1
Release from retained candidate-era gates, scans, and evidence.

## Changed

- Correct current README wording that still described v0.1.1 material as an
  unreleased candidate.
- Mark retained v0.1.1 candidate gates, rights review, and evidence as
  historical pre-release records.
- Add a regression test that prevents current-facing material from presenting
  v0.1.1 as an active candidate.

## Compatibility

The framework contract remains `0.1.0`. No schema, profile, bootstrap behavior,
tool version, workspace layout, or installation behavior changes.

## Validation

The final Release must link the exact candidate commit and local plus
cross-platform CI evidence.
