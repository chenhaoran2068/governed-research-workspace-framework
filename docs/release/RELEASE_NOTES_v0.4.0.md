# Release Notes V0.4.0

## Added

- A version-2, opt-in knowledge-service manifest mode for one private,
  manager-owned local reference library below its registered service root.
- Generic boundary, migration, template, synthetic-example, and validation
  guidance for that mode.

## Preserved

- Version-1 `pointer_only` knowledge-service manifests remain valid.
- Workspace-manifest schema version `1` and empty bootstrap behavior remain
  unchanged.
- The Framework neither creates a real service nor installs, configures, or
  accesses a reference manager or source artifact.

## Excluded

- Real reference libraries, PDFs, accounts, credentials, private paths, and
  source-derived content remain outside the public package.
