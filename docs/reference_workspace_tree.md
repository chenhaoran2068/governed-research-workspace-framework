# Reference Workspace Tree

Status: `v0.1.0` reference layout. This document describes stable locations
and ownership boundaries; it is not an installer and does not make any
directory mandatory merely by naming it.

## Scope

The framework defines three levels:

1. **Workspace level**: root ownership and registration records.
2. **System level**: a concrete system's manifest and self-owned package
   layout.
3. **Project level**: one real project's binding to its primary system and
   the primary system's project-specific structure.

It deliberately does not define universal data, manuscript, method, or
knowledge subdirectories. Those structures are owned by the relevant concrete
system or project and may differ safely between systems.

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
    ...curated, source-backed records as configured...
  Methods/                                        [bootstrap default]
    ...method workbenches as configured...
  Instances/                                      [bootstrap default]
    <project-id>/                                 [on real project creation]
      00_state/
        PROJECT_SYSTEM_BINDING.yaml               [required once the project is bound]
      ...primary-system-owned project content...
  Papers/                                         [bootstrap default]
    ...shared paper rules or retained special workspaces as configured...
  Data_Raw/                                       [bootstrap default]
    ...retained source holdings only when permitted...
  Github/                                         [bootstrap default]
    <repository-worktree>/                        [only for a reviewed public worktree]
  Ops/                                            [bootstrap default]
    ...machine-local operational material as configured...
  Archive/                                        [bootstrap default]
    ...retained historical material as configured...
```

`<workspace>`, `<system-id>`, `<skill-id>`, `<shared-service-id>`, and
`<project-id>` are placeholders. They are never literal required names.

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

### Project Creation

A real project is placed under `Instances/<project-id>/`. Once it has a
primary system, `00_state/PROJECT_SYSTEM_BINDING.yaml` records that system and
any explicitly contributing systems. The primary system owns the remaining
project lifecycle and project-specific subdirectories.

The framework does not authorize project execution, data access, analysis,
compliance, release, or submission through this binding.

### Shared and Public Material

`Shared/`, `Knowledge/`, and `Methods/` hold only material that has an
identified owner and an appropriate sharing boundary. A system may use a
shared service only when its own manifest declares it and the workspace makes
it available.

`Github/` holds local worktrees for reviewed public derivatives. It cannot
replace private authority or be used to copy private projects into a public
repository.

## What This Tree Does Not Standardize

The following remain system- or project-specific:

- data lifecycle layers and access restrictions;
- protocol, ethics, analysis, manuscript, and submission directories;
- knowledge taxonomy and external-source records;
- detailed skill runtime installation paths; and
- cache, archive, and operational retention policy.

Those details must be declared by the relevant owner rather than assumed from
the presence of a root directory.
