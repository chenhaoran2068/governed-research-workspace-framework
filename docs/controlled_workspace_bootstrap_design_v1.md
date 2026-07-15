# Controlled Workspace Bootstrap Design v1

Status: accepted design; implementation candidate is present, cross-platform
CI has passed, and release review remains pending.

## Purpose

`bootstrap_workspace` will create one empty generic workspace framework after
an exact human-reviewed preview. It creates a framework root, not a research
project and not a concrete system installation.

It must be an explicit command. Loading a skill, opening the repository, or
mentioning a research task must never invoke it automatically.

## Runtime And Implementation Boundary

- minimum runtime: Python 3.11;
- implementation: Python standard library only;
- planned path: `scripts/bootstrap_workspace.py`;
- supported release platforms: Windows, Ubuntu, and macOS, but only after the
  corresponding CI matrix has passed; and
- no network, credentials, account access, dependency installation, system
  registration, or project creation.

Python 3.11 aligns the helper with the existing controlled bootstrap safety
baseline in the governed-research-workflow package.

## Design Evidence

- Python `argparse` is the standard-library CLI parser used for explicit
  arguments, choices, help text, and invalid-input refusal. The helper will
  additionally disable abbreviated long options to avoid ambiguous command
  interpretation. Source: https://docs.python.org/3/library/argparse.html
- Python `pathlib` and `os` documentation describe canonical path resolution,
  symbolic-link behavior, and Windows reparse-point behavior. The design uses
  those facts to refuse linked parents and avoid following links during
  cleanup. Sources: https://docs.python.org/3/library/pathlib.html and
  https://docs.python.org/3/library/os.html
- OWASP recommends allowlisted input and normalized paths for file-system
  operations instead of trusting arbitrary user-provided path fragments. The
  direct-child parent-plus-ID contract implements that boundary. Source:
  https://owasp.org/www-community/attacks/Path_Traversal

## Command Contract

The helper accepts only a direct-child creation model:

```text
--parent <existing-normal-directory>
--workspace-id <lowercase-ascii-id>
--profile <standalone|framework_integrated>
```

`--workspace-id` must match `^[a-z0-9][a-z0-9-]{0,63}$`. The final target is
always `<parent>/<workspace-id>`; no arbitrary target path is accepted.

The default invocation is a no-write preview. Confirmation additionally
requires:

```text
--confirm-create
--plan-id <exact-preview-plan-id>
--approval-reference <nonempty-accountable-reference>
```

The parser must disable abbreviated long options. It must reject unknown
arguments, a simultaneous preview/confirmation request, and
`private_lab_extended`. The public helper cannot infer an organization's
private controls or services.

Candidate preview:

```text
python scripts/bootstrap_workspace.py \
  --parent <existing-parent-directory> \
  --workspace-id <lowercase-ascii-id> \
  --profile framework_integrated
```

After reviewing the emitted plan, confirmation repeats those inputs with
`--confirm-create`, the exact `--plan-id`, and a nonempty
`--approval-reference`.

## Profile Output

### `framework_integrated`

Create the complete empty reference root set:

```text
Systems/  Skills/  Shared/  Knowledge/  Methods/  Instances/
Papers/   Data_Raw/  Github/  Ops/  Archive/
```

Also create the root `WORKSPACE_MANIFEST.yaml`, orientation `README.md`, and
`bootstrap_receipt.json`. The manifest has no registered systems and no shared
services. Empty roots do not create access rights or active capabilities.

### `standalone`

Create only:

```text
Systems/  Instances/
```

Also create the same root manifest, orientation README, and receipt. This is
the minimum framework-compatible scaffold.

## Preview, Confirmation, And Receipt

The preview must show and bind:

- tool and framework versions;
- selected profile;
- normalized parent path and filesystem identity;
- final target path;
- exact directory and file allowlists;
- source-template hashes;
- scope flags proving the operation is empty-scaffold-only; and
- a deterministic `plan_id` derived from the reviewed plan.

On confirmation, the helper must re-check the parent path, identity, target,
profile, plan ID, template hashes, and approval reference. It must write a
receipt containing the reviewed plan, approval reference, creation time, and
hashes of created files other than the receipt itself.

## Safety Controls

The helper must refuse:

- a missing, non-directory, symbolic-link, or Windows reparse-point parent;
- a target inside the package itself;
- a target that already exists, even when empty;
- path escape, non-allowlisted ID, or a target that is not the selected
  parent's direct child;
- a parent identity change after preview;
- any confirmation that does not exactly match its preview; and
- any attempt to use a private-lab-extended profile.

It must stage files in a same-parent, helper-owned directory, verify the
staged tree against the allowlist, and rename it into place only after the
final re-check. On failure, it may remove only its own verified staging path.
It must not follow a symbolic link or reparse point during cleanup.

## Required Tests Before Implementation Is Accepted

1. Preview makes no filesystem change.
2. Each supported profile creates exactly its allowlisted tree and valid
   manifest.
3. Unknown, abbreviated, conflicting, or missing arguments are refused.
4. Existing, escaped, linked, junction, package-internal, and changed-identity
   targets are refused without modification.
5. A mismatched plan or missing approval reference is refused.
6. Injected write failure cleans only an owned staging directory.
7. Receipt hashes and manifest values match the generated files.
8. No source data, network, credential, project, system registration, or
   account input is accepted.
9. Windows, Ubuntu, and macOS CI pass with Python 3.11 and the maintained
   current Python version.

## Non-Goals

The helper does not install a system, install a runtime skill, populate
Knowledge, create a project, copy data, create credentials, claim compliance,
or authorize research work. Those actions remain separately governed.
