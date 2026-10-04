# Release Notes V0.5.0

## Added

- An optional Research Program index schema and blank template.
- Instance-local placement guidance and a synthetic validation fixture.
- Explicit distinction between a Study Instance and an upper-level Research
  Program.

## Preserved

- Existing Study roots, workspace-manifest schema version `1`, and
  Study-level `project_id` records remain unchanged.
- A Research Program is metadata only; it cannot merge Studies, transfer
  authority, or grant access.

## Excluded

- Real Program or Study content, data, credentials, local paths, migration
  helpers, workspace scanners, and automatic grouping remain outside this
  release.
