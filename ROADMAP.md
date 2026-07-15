# Roadmap

This roadmap records review sequence, not delivery dates or promises.

## Public v0.1.0 Framework Candidate

Current candidate goals:

- define generic root ownership and multi-system contracts;
- provide JSON Schema definitions for workspace, system, and project-binding
  manifests;
- provide standalone and framework-integrated synthetic profiles;
- provide blank templates and a synthetic multi-system example; and
- validate that the candidate remains path-independent and public-safe.

The candidate does not yet provide a released installer, live registry,
runtime adapter, agent implementation, or production compatibility claim.

## Workspace Bootstrap Implementation Candidate

The candidate now includes an explicitly invoked `bootstrap_workspace` helper.
Its accepted contract is recorded in
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

It remains unreleased until the candidate is independently reviewed. Its
Windows, Ubuntu, and macOS GitHub Actions matrix has passed.

## Future Review Gates

1. Review framework terms, ownership boundaries, and public/private rules.
2. Validate schemas, templates, examples, and boundary checks on supported
   operating systems.
3. Independently validate at least one concrete system in standalone and
   framework-integrated profiles.
4. Decide repository visibility, release version, maintainer process, and
   compatibility policy.
5. Only then create a public release.

## Not Automatic Future Scope

- automatic installation into a host workspace;
- access to external tools, repositories, data, or credentials;
- clinical, ethical, legal, or publication authority;
- publication of any private workspace material; and
- a requirement that all research systems use this framework.
