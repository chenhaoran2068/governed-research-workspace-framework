# Knowledge Service Contract V1

## Purpose

This contract defines the generic Framework boundary for an opt-in,
source-backed knowledge service. It identifies a service and its consumers; it
does not define a universal taxonomy, reading workflow, reference manager, or
knowledge-record layout.

## Registration

A registered knowledge service requires all of the following:

1. `WORKSPACE_MANIFEST.yaml` lists its `service_id` in `shared_services`.
2. Its manifest exists at
   `Knowledge/<knowledge-service-id>/KNOWLEDGE_SERVICE_MANIFEST.yaml`.
3. The manifest validates against
   `schemas/knowledge_service_manifest.schema.json`.
4. A consumer System lists the same identifier in `optional_shared_services`.
5. The service manifest lists that System in `allowed_consumer_system_ids`.

The service root and service identifier must agree. A mismatch, missing
manifest, undeclared consumer, or unavailable service is a refusal boundary;
it must not trigger workspace scanning, repair, creation, or migration.

## Ownership And Boundaries

The manifest names one owning contract and one service root. The owner may be a
skill, a System, or another explicitly governed service. The owner must define
the deeper layout and retention policy.

The generic Framework contract does not grant:

- source discovery, source reading, or source-artifact retention;
- access to project files, credentials, accounts, data, or private memory;
- knowledge-card creation, experience promotion, rule integration, or a
  project lifecycle transition; or
- automatic installation, synchronization, workspace repair, or migration.

Source identities and pointers may be retained only within a concrete service's
approved contract. A knowledge service is not a second ungoverned PDF or
reference-manager library.

## Bootstrap And Compatibility

The controlled bootstrap creates an empty `Knowledge/` root only. It never
registers a service, creates a service manifest, or populates service content.

The v0.3.0 contract retains workspace-manifest schema version `1` and its
existing optional `shared_services` field. Existing workspaces without a
knowledge service remain valid and are not inspected or migrated.
