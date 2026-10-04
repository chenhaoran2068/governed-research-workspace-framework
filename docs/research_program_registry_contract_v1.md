# Research Program Registry Contract

## Purpose

A Research Program is an optional, human-reviewed grouping of independent
Studies with a stated upper-level purpose, bounded question family, and a
meaningful shared backbone or documented lineage. It is not another Study and
does not replace any member Study's lifecycle, primary System, data boundary,
result authority, governance record, manuscript, or release decision.

The term **Study Instance** is used in this Framework for one real Study. Some
older compatible Systems and local records use `project` or `project_id` for
that same Study-level object. This contract does not rename or migrate those
records. **Research Program** is the distinct upper-level grouping term.

## Optional Instance-Level Placement

An instance that already declares an internal registry may keep a Program
index at:

```text
<instance-root>/Registry/Research_Programs/<research-program-id>/
  research_program_index.json
```

This is an optional second-level placement point, not a required Framework
root, bootstrap output, or migration instruction. Existing Study roots may be
directly below an instance or within a System-owned container such as
`Programs/`; they are not moved or renamed to join a Research Program.

The index uses instance-relative references to existing Study roots. It must
not contain an absolute local path, copied Study tree, data, credential, or
claim that membership grants access.

## Required Boundaries

The index must declare that Program membership does not merge independent
Studies, transfer ethics, governance, data, result, manuscript, release, or
other authority, or grant material access.

Shared material stays local by default. A Program may name a narrow explicit
reference only when it identifies the exact source artifact, owner, reference
mode, receiving scope, source version or date, sharing status, and human-review
reference. A pointer, adopted copy, or scoped derivative is not permission to
read a full Study workspace or inherit a decision.

## Human Review And Compatibility

Before a Program is marked `confirmed`, an accountable human reviews its
purpose, membership basis, members, and any declared shared reference. The
record stores the review date and a review reference. Common
topic, contributor group, schedule, target venue, dataset, or tool alone is
insufficient evidence for grouping.

This is additive. A workspace without a Research Program index remains valid.
Existing Study locations and `PROJECT_SYSTEM_BINDING.yaml` records stay
unchanged. The schema and template are structural aids only: they do not
discover Studies, resolve a path, read material, decide membership, or create
a Program.
