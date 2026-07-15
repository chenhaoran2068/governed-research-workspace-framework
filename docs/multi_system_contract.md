# Multi-System Contract

## System Registration

An installed system is described by a system manifest. At minimum, it declares:

```text
system_id
system_version
system_role
entry_point
supported_profiles
required_dependencies
optional_shared_services
project_ownership_behavior
data_access_boundary
```

The workspace manifest lists installed systems and their workspace-relative
locations. It is a registry, not a capability grant.

## Project Ownership

Each real project declares exactly one `primary_system`. The primary system owns
the lifecycle state and governance route for that project.

The project may name `contributing_systems`. A contributing system may provide
a method, tool, skill, conversion, or review capability. It may not silently
advance project state, change a release decision, or claim project authority.

## Shared Services

A system may use a shared service only when its manifest declares that service
and the host workspace makes it available. Examples include a skill registry,
source-backed knowledge service, or shared-reference library.

Systems must use explicit paths, records, or pointers. They must not scan an
entire workspace to infer configuration or read another system's private area.

## Isolation Rule

Sharing is selective. Share only a capability whose owner, version, access
restriction, provenance, and failure behavior are known. Project data,
unpublished work, credentials, and project-local audit records are private by
default.
