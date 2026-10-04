# Reference Workspace Tree

Status: `v0.5.0` candidate reference layout. This document describes stable locations
and ownership boundaries; it is not an installer and does not make any
directory mandatory merely by naming it.

## Scope

The framework defines four levels:

1. **Workspace level**: root ownership and registration records.
2. **System level**: a concrete system's manifest and self-owned package
   layout.
3. **Study level**: one real Study's binding to its primary system and the
   primary system's Study-specific structure.
4. **Research Program level (optional)**: an instance-local metadata index
   that relates independently governed Studies without moving or merging them.

It deliberately does not define universal data, manuscript, method, or
knowledge taxonomies. A registered knowledge service has one generic manifest
location, but its internal records remain owned by that service and may differ
safely between services.

## Reference Tree

```text
<workspace>/
  WORKSPACE_MANIFEST.yaml                         [workspace record]
  Systems/                                        [bootstrap default]
    <system-id>/                                  [on system installation]
      SYSTEM_MANIFEST.yaml                        [required for a registered system]
      ...system-owned package content...
  Skills/                                         [bootstrap default]
    <skill-id>/                                   [optional reusable skill source]
      ...skill-owned content...
  Shared/                                         [bootstrap default]
    <shared-service-id>/                          [only when an approved service exists]
      ...service-owned content...
  Knowledge/                                      [bootstrap default]
    <knowledge-service-id>/                       [only when explicitly registered]
      KNOWLEDGE_SERVICE_MANIFEST.yaml             [required for a registered service]
      reference_manager/                          [only for an explicitly declared private manager library]
        <manager-owned-library>/                  [private source artifacts; never public by default]
      ...service-owned curated knowledge records...
  Methods/                                        [bootstrap default]
    ...method workbenches as configured...
  Instances/                                      [bootstrap default]
    <study-id>/                                   [on real Study creation]
      00_state/
        PROJECT_SYSTEM_BINDING.yaml               [required once the project is bound]
      ...primary-system-owned project content...
    <instance-id>/                                [only when a concrete System declares an instance root]
      Registry/
        Research_Programs/
          <research-program-id>/                  [only after human-reviewed grouping]
            research_program_index.json
      ...System-owned Study containers or existing Study roots...
  Data_Raw/                                       [bootstrap default]
    ...retained source holdings only when permitted...
  Github/                                         [bootstrap default]
    <repository-worktree>/                        [only for a reviewed public worktree]
  Ops/                                            [bootstrap default]
    ...machine-local operational material as configured...
  Archive/                                        [bootstrap default]
    ...retained historical material as configured...
```

`<workspace>`, `<system-id>`, `<skill-id>`, `<shared-service-id>`,
`<study-id>`, and `<research-program-id>` are placeholders. They are never
literal required names.

## Lifecycle Rules

### Workspace Bootstrap

A future full-profile bootstrap may create the empty named root directories,
an empty `WORKSPACE_MANIFEST.yaml` based on the supplied template, and an
orientation document. At this point it must not register a system, create a
real project, copy data, discover user files, or infer access rights.

For compatibility, only the manifest and the paths explicitly declared in it
matter. Empty recommended roots may be omitted from a minimal workspace until
they are needed.

### System Installation

A system becomes registered only when:

1. its package is placed at the workspace-relative path recorded in
   `WORKSPACE_MANIFEST.yaml`;
2. it provides `SYSTEM_MANIFEST.yaml` at its own declared location; and
3. its profile and version are independently validated.

The system owns all deeper package layout. The framework does not decide
whether a system has agents, scripts, templates, knowledge, or project tools.

### Study Creation

A real Study is placed under `Instances/<study-id>/`. Once it has a primary
system, `00_state/PROJECT_SYSTEM_BINDING.yaml` records that system and any
explicitly contributing systems. `project` remains the legacy field vocabulary
inside that binding; it denotes the Study-level workspace. The primary system
owns the remaining Study lifecycle and Study-specific subdirectories.

The primary System, not this Framework, defines any project manuscript or
submission area. The Framework does not create a top-level paper workspace.

The framework does not authorize project execution, data access, analysis,
compliance, release, or submission through this binding.

### Research Program Registry

An optional instance-local Research Program index may relate named existing
Study roots. It is not a parent directory for those Studies and does not
change their physical paths. The index records membership and narrowly scoped
shared references only; it cannot merge Study facts, transfer authority, or
grant access. See [the Research Program registry contract](research_program_registry_contract_v1.md).

### Shared and Public Material

`Shared/`, `Knowledge/`, and `Methods/` hold only material that has an
identified owner and an appropriate sharing boundary. A system may use a
shared service only when its own manifest declares it and the workspace makes
it available.

A knowledge service is registered only when its identifier appears in the
workspace manifest's `shared_services`, its service manifest exists at
`Knowledge/<knowledge-service-id>/KNOWLEDGE_SERVICE_MANIFEST.yaml`, and its
declared consumer System also names that identifier as an optional shared
service. Bootstrap creates neither this service directory nor its manifest.

`Github/` holds local worktrees for reviewed public derivatives. It cannot
replace private authority or be used to copy private projects into a public
repository.

An opted-in `managed_local_reference_library` remains below the owning
knowledge-service root. Its manifest must name a workspace-relative artifact
store, prohibit scanning, exclude raw artifacts from public derivation, and
use only a closed-manager copy or native-manager sync for migration. The
Framework does not create that directory during bootstrap.

## What This Tree Does Not Standardize

The following remain system- or project-specific:

- data lifecycle layers and access restrictions;
- protocol, ethics, analysis, manuscript, and submission directories;
- knowledge taxonomy, external-source records, and a service's internal
  knowledge layout;
- detailed skill runtime installation paths; and
- cache, archive, and operational retention policy.

Those details must be declared by the relevant owner rather than assumed from
the presence of a root directory.
