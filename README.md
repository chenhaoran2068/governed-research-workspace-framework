# Governed Research Workspace Framework

Status: public `v0.1.0-framework-candidate`; cross-platform CI has passed.
It is not yet tagged or released.

## Purpose

This repository defines a generic, multi-system workspace framework for
governed research. It is an architecture contract, not a research-execution
system, agent, data platform, or copy of any private laboratory workspace.

The framework keeps the following distinct:

- system control planes and reusable skills;
- shared rules, source-backed knowledge, methods, and raw-source holdings;
- real project instances and their accountable state; and
- public release worktrees and private local authority.

It supports a concrete system package in either of two modes:

```text
standalone
  -> the system uses only its bundled public resources

framework-integrated
  -> the system registers in a compatible workspace and uses only declared
     shared services
```

## Non-Goals

This framework does not perform research, analysis, medical decision-making,
or submission work. It does not create a right to access data, sources,
accounts, or tools. It does not bundle real study data, manuscripts, audit
trails, credentials, or private memory.

## Core Model

```text
Workspace Framework
  -> root ownership, manifests, profiles, and shared-service contracts

System Package
  -> one bounded control plane or domain capability

Skill
  -> a focused, reusable entry or capability used by one or more systems

Project Instance
  -> one real study with one primary system and optional contributors
```

See:

- [root ownership contract](docs/root_ownership_contract.md)
- [reference workspace tree](docs/reference_workspace_tree.md)
- [controlled workspace bootstrap design](docs/controlled_workspace_bootstrap_design_v1.md)
- [multi-system contract](docs/multi_system_contract.md)
- [installation profiles](docs/installation_profiles.md)
- [public/private boundary](docs/public_private_boundary.md)
- [versioning and compatibility](docs/versioning_and_compatibility.md)

## Repository Layout

```text
docs/       Human-readable framework contracts
schemas/    Versioned JSON Schema contracts
profiles/   Complete synthetic profile examples
templates/  Blank manifest templates
scripts/    Explicitly invoked controlled helpers
examples/   Synthetic multi-system workspace example
tests/      Contract and public-boundary checks
```

## Current Candidate Scope

This candidate provides framework contracts, examples, and one explicitly
invoked controlled empty-workspace bootstrap helper. It does not claim an
agent-runtime integration, system registry service, or full interoperability
with any concrete research system.

The bootstrap helper is no-write by default. It creates a framework root only
after a reviewed preview, an exact plan ID, and an accountable approval
reference. It cannot install a system, create a project, import data, or grant
access. See the [controlled workspace bootstrap design](docs/controlled_workspace_bootstrap_design_v1.md).

Candidate preview:

```text
python scripts/bootstrap_workspace.py \
  --parent <existing-parent-directory> \
  --workspace-id <lowercase-ascii-id> \
  --profile framework_integrated
```

After reviewing the emitted plan, confirmation requires the exact returned
`plan_id` and a nonempty `approval_reference`. The candidate requires Python
3.11 or later. Its Windows, Ubuntu, and macOS CI matrix passed on Python 3.11
and 3.14; the candidate remains unreleased pending final review.

A future concrete system may state framework support only after it validates
the declared profile and compatibility version.

## License

Apache-2.0. See [LICENSE](LICENSE).
