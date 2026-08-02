# Papers-Root Retirement Compatibility

Status: v0.2.0 compatibility contract. Determine the published state of v0.2.0
from its exact tag and matching GitHub Release; this document does not itself
declare a Release published.

## Future Full Profile

Framework v0.2.0 changes only a newly confirmed `framework_integrated`
bootstrap. The new empty scaffold omits the top-level `Papers/` directory and
does not generate `roots.papers` in `WORKSPACE_MANIFEST.yaml`. All other
declared future full-profile roots remain unchanged. `standalone` remains only
`Systems/` and `Instances/`.

The Framework does not define a replacement universal manuscript or submission
tree. A concrete installed System owns those project-level structures and its
own cross-project guidance.

## Retained Workspaces

The workspace-manifest schema remains version `1` and still accepts an
existing `roots.papers: Papers` entry. Framework v0.2.0 does not automatically
migrate, remove, rename, inspect, copy, archive, or otherwise process that
manifest entry or its physical directory.

Review an existing workspace, its installed Systems, and any intended local
retirement separately. Do not rerun bootstrap into an existing workspace or
treat a Framework source update as authority to delete a directory.

## System Compatibility

A concrete System may claim support for the v0.2.0 framework-integrated
profile only after it declares a compatible Framework version range and
validates that profile. Framework v0.2.0 neither updates a System manifest nor
proves that a separately released System is compatible.

The two System manifests in this repository's synthetic example are not real
System packages. Their declared range only keeps that fixed public example
internally consistent; it is not a general compatibility assurance.
