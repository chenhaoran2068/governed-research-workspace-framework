# Workspace Placement Integrity Audit Contract v1

## Purpose

This optional Framework control makes path-placement residue visible after a
caller-named workspace operation. It reviews only Framework-declared roots and
returns a structured report; it is not a cleanup, migration, discovery, or
content-classification service.

The audit answers limited filesystem questions: whether a declared root is
present, whether a registered System path is present, whether a selected
metadata-only area contains an empty directory, and whether an explicitly named
generated-directory marker appears outside a declared regenerable location.

## Scope And Ownership

The caller supplies one `workspace_placement_audit_scope` JSON record below
the workspace root. The scope names its workspace root, the existing
`WORKSPACE_MANIFEST.yaml`, a subset of manifest root keys, optional metadata
inspection depth, exclusions, known regenerable operational locations, and a
report root below `Ops/`.

The auditor derives reviewed root paths from `WORKSPACE_MANIFEST.yaml` rather
than guessing them from directory names. A path outside the caller-named
workspace, a root key absent from the manifest, an absolute/escaping relative
path, a symbolic link, a Windows reparse point, or a nested Git worktree is a
stop or `not_assessed` boundary.

The Framework owns only root placement. Concrete Systems, Methods, Knowledge
Services, and Studies own deeper domain layouts. The Framework must not infer
that an ordinary file inside such a subtree is misplaced merely because it
cannot determine its scientific or operational role.

## Privacy And Data Boundary

The audit reads directory metadata only. It does not open source files,
databases, PDFs, data tables, manuscript text, credentials, Git history, or
network resources. `Data_Raw/` defaults to root-only review. A report can
contain local relative paths, so it remains an operational record in the
private workspace and is never a public-package artifact by default.

## Records

The Framework provides four generic schemas:

- `workspace_placement_audit_scope`: caller-approved read-only boundary;
- `workspace_placement_audit_report`: findings from one audit run;
- `workspace_placement_receipt`: an optional declaration for a bounded
  material-writing, migration, or repair operation; and
- `workspace_placement_remediation_queue`: human-reviewed proposed actions.

Suggested local location:

```text
Ops/workspace_hygiene/
  placement_audit_scope.json
  placement_receipts/<operation-id>.json
  reports/<audit-id>.json
  remediation_queues/<audit-id>.json
```

This is a suggested private operational location, not a new required root and
not a Framework instruction to create any of these directories.

## Findings And Meaning

`conforms` means a limited structural condition is known, not that material is
scientifically correct. `declared_absent` and `registered_path_missing` require
the owner to explain a manifest/disk mismatch. `candidate_empty_directory` and
`known_generated_outside_declared_zone` are review candidates only.
`unattributed_path` means the Framework cannot associate a root-level path with
a declared root or known workspace record. `not_assessed` preserves an explicit
boundary. `refused_reparse_point` prevents traversal outside the reviewed tree.

When a caller-named placement receipt supplies a `repair_relations` entry, the
auditor checks only whether its mistaken and corrected paths still exist. If
both remain, it reports `possible_repair_residue`; this is a human-review
candidate, not proof that the files are duplicates or that either can be
deleted. A receipt is optional and must be explicitly listed in the scope.

None of these statuses proves that a path may be removed.

## Execution Boundary

`scripts/audit_workspace_placement.py` emits a report to standard output by
default and makes no write. Writing a report below the scope's declared report
root requires an explicit `--write-report`, a new `.json` destination, and a
nonempty accountable-human approval reference. Writing the report does not
permit changing audited material.

```text
# Read-only: JSON report goes only to standard output.
python scripts/audit_workspace_placement.py --scope <workspace>/Ops/workspace_hygiene/placement_audit_scope.json

# Operational-record write only after an accountable-human approval.
python scripts/audit_workspace_placement.py \
  --scope <workspace>/Ops/workspace_hygiene/placement_audit_scope.json \
  --write-report \
  --report-path Ops/workspace_hygiene/reports/<audit-id>.json \
  --approval-reference <human-reference>
```

No Framework helper in this contract moves, archives, deletes, renames,
registers, repairs, cleans, or creates a real Study or System. A future repair
helper, if separately proposed, must consume one caller-named queue item and
require a fresh human approval for that exact action.

## Monthly Review

A monthly reminder may request this read-only audit, but a reminder does not
run it, authorize a report write, or approve a remediation action. The host
automation is separate from this Framework package and must name the workspace
and scope at run time.
