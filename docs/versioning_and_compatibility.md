# Versioning And Compatibility

## Versioned Contracts

The framework, every system manifest, and every schema expose explicit version
fields. A system may claim framework integration only when it declares a
supported framework-version range and has validated that profile.

## Compatibility Expectations

- Additive optional fields are normally backward compatible.
- Required-field changes, semantic changes, and path-contract changes require
  a deliberate compatibility decision.
- A workspace must not infer compatibility solely from folder names.
- A system must stop and report an unsupported manifest or profile rather than
  attempting a blind migration.

## Release Discipline

Candidate branches, released tags, and local private variants are distinct.
A published version is an immutable public contract by policy. A correction is
released as a new version rather than silently changing the published contract.
Do not claim GitHub technical immutable-release protection unless that
repository setting is actually enabled and recorded for the release.
