# Controlled Reference-Manager Library Contract V1

## Purpose

This contract permits one opt-in knowledge service to declare a private,
manager-owned local source-artifact library. It exists for portable reference
management where the user intentionally keeps a reference-manager data
directory inside the workspace. It is not a general PDF repository, source
discovery mechanism, or public distribution channel.

## Required Registration

The established registration chain remains mandatory:

1. the workspace lists the service in `shared_services`;
2. the service manifest exists at its declared `Knowledge/<service-id>/` root;
3. the owner and each consumer declare the same service identifier; and
4. the version-2 manifest validates its private artifact boundary.

A missing or mismatched record is a refusal state. It must not trigger repair,
filesystem scanning, migration, manager installation, or source reading.

## Version-2 Artifact Boundary

`source_artifact_boundary` has `mode:
managed_local_reference_library` and must declare a workspace-relative store
below the service root. It also requires:

- a non-secret `manager_kind` identifier;
- `public_derivation: excluded`;
- `workspace_scanning: false` and `automatic_content_import: false`;
- `migration_rule:
  closed_manager_user_directed_copy_or_native_manager_sync`.

The Framework rejects absolute paths, parent traversal, sibling-service paths,
external-drive paths, public-release paths, credentials, and cloud locations.
The declared root identifies a boundary; it does not grant permission to read
or modify any source artifact.

## Migration And Public Boundary

Close the reference manager before copying a workspace backup. On a new
computer, install the manager, point it to the copied workspace-relative data
directory, and validate the configured service before use. Do not live-sync a
manager database through an arbitrary filesystem synchronizer.

Raw library contents, attachments, manager configuration, account identifiers,
and credentials are private. They are never committed or included in a public
Framework package, and they are not copied into a Study by this contract.

## What Remains Elsewhere

A concrete Skill may, under its own approved contract, support an explicitly
requested import after this Framework boundary is active. A consumer System
may exchange only approved metadata and must not claim project authority from
the service. This Framework does not create knowledge cards, infer rights,
promote experience, or decide scientific, ethical, or publication matters.
