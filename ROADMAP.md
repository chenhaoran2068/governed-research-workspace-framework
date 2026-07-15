# Roadmap

This roadmap records review sequence, not delivery dates or promises.

## v0.1.0 (released 2026-07-15)

This release:

- define generic root ownership and multi-system contracts;
- provide JSON Schema definitions for workspace, system, and project-binding
  manifests;
- provide standalone and framework-integrated synthetic profiles;
- provide blank templates and a synthetic multi-system example; and
- validates that the package remains path-independent and public-safe.

It does not provide a system installer, live registry, runtime adapter, agent
implementation, or universal production compatibility claim.

## Workspace Bootstrap

This release includes an explicitly invoked `bootstrap_workspace` helper. Its
accepted contract is recorded in
`docs/controlled_workspace_bootstrap_design_v1.md`. It creates an empty
profile-appropriate workspace skeleton, a blank workspace manifest, and
orientation material. It:

- show a no-write plan and require matching human confirmation before writing;
- refuse an unsafe or nonempty target rather than merge with existing content;
- create no system registration, project, data, credential, account setting,
  access right, research claim, or compliance fact;
- record a receipt of the created skeleton and declared framework version; and
- passed testing on Windows, Ubuntu, and macOS with Python 3.11 and 3.14; and
- use Python 3.11+ standard library only, accept `standalone` and
  `framework_integrated`, and refuse `private_lab_extended`.

Its Windows, Ubuntu, and macOS GitHub Actions matrix passed with Python 3.11
and 3.14.

## Future Review Gates

1. Maintain the ownership, public/private, schema, template, and boundary
   contracts through reviewed releases.
2. Keep supported operating-system validation current as runtime baselines
   change.
3. Require every concrete system to validate its own declared profiles and
   exact compatible framework version before it claims stable compatibility.
4. Add an explicit, independently reviewed system-installation method only if
   real user need and safety evidence justify it.

## Not Automatic Future Scope

- automatic installation into a host workspace;
- access to external tools, repositories, data, or credentials;
- clinical, ethical, legal, or publication authority;
- publication of any private workspace material; and
- a requirement that all research systems use this framework.
