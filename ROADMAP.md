# Roadmap

This roadmap records review sequence, not delivery dates or promises.

## Local-Only v0.1.0 Framework Candidate

Current candidate goals:

- define generic root ownership and multi-system contracts;
- provide JSON Schema definitions for workspace, system, and project-binding
  manifests;
- provide standalone and framework-integrated synthetic profiles;
- provide blank templates and a synthetic multi-system example; and
- validate that the candidate remains path-independent and public-safe.

The candidate does not yet provide a released installer, live registry,
runtime adapter, agent implementation, or production compatibility claim.

## Planned Workspace Bootstrap Candidate

A future candidate may add an explicitly invoked `bootstrap_workspace` helper
only after the reference workspace tree and manifest semantics are accepted.
It would create an empty full-profile workspace skeleton, a blank workspace
manifest, and orientation material. It must:

- show a no-write plan and require matching human confirmation before writing;
- refuse an unsafe or nonempty target rather than merge with existing content;
- create no system registration, project, data, credential, account setting,
  access right, research claim, or compliance fact;
- record a receipt of the created skeleton and declared framework version; and
- be tested on Windows, Ubuntu, and macOS before any release claim.

This is a planned controlled capability, not current package behavior.

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
