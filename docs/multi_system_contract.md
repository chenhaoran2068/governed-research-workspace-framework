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

## Research Program Grouping

An optional Research Program may be recorded in an instance-local registry to
relate independent Study Instances. It is a metadata grouping, not a second
primary System or a replacement for any Study's `project_id` or binding.

Program membership needs accountable-human review of a stated upper-level
purpose, bounded question family, and meaningful shared backbone or documented
lineage. It does not merge Study content or let one Study inherit another's
data access, ethics, result authority, manuscript state, submission route, or
release decision.

The Framework schema records only caller-supplied metadata. It does not scan
for Studies, resolve references, decide membership, or create a Program.

## Shared Services

A system may use a shared service only when its manifest declares that service
and the host workspace makes it available. Examples include a skill registry,
source-backed knowledge service, or shared-reference library.

Systems must use explicit paths, records, or pointers. They must not scan an
entire workspace to infer configuration or read another system's private area.

### Registered Knowledge Services

A registered knowledge service is a shared service whose workspace-relative
root is `Knowledge/<knowledge-service-id>/` and whose
`KNOWLEDGE_SERVICE_MANIFEST.yaml` conforms to the Framework knowledge-service
schema. A skill or System may own the service contract, but a consumer System
may use it only when all of the following are true:

1. the workspace manifest lists the service identifier in `shared_services`;
2. the service manifest names the consumer System in
   `allowed_consumer_system_ids`; and
3. the consumer System lists the identifier in `optional_shared_services`.

Registration does not authorize source reading, source-artifact retention,
project access, knowledge-card creation, rule promotion, or a project-state
transition. A missing or mismatched declaration is an unavailable optional
service, not a reason to search or repair the workspace.

## Isolation Rule

Sharing is selective. Share only a capability whose owner, version, access
restriction, provenance, and failure behavior are known. Project data,
unpublished work, credentials, and project-local audit records are private by
default.
