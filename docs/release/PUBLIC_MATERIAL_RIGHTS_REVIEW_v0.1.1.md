# Public Material And Rights Review: v0.1.1 Candidate

Status: candidate technical review. Final release authorization and contribution
authority confirmation remain human maintainer responsibilities.

## Scope And Method

The retrospective review covers the released v0.1.0 tag and the v0.1.1
candidate changes. It uses tracked-tree, diff, whitespace, history, and object
checks, plus scans for common credentials and known private local paths.

The v0.1.0 release tag is an annotated tag that resolves to the same commit as
the published main release commit. The release has no uploaded assets beyond
the GitHub-generated source archives.

## Reviewed Material Classes

| Material class | Included paths | Provenance and rights finding | Candidate decision |
| --- | --- | --- | --- |
| Framework contracts | docs/, README.md, ROADMAP.md | Generic workspace ownership, profile, and compatibility material written for this repository. | Admit. |
| Schemas and templates | schemas/, templates/, profiles/ | Generic public contracts and blank data structures only. | Admit. |
| Synthetic example | examples/ | Synthetic identifiers and manifests only; no real project data, manuscript, audit, or source extract. | Admit. |
| Controlled helper and tests | scripts/, tests/, .github/workflows/ | Repository-authored Python helper and synthetic regression tests. Actions are pinned to full commit SHAs. | Admit subject to integrity policy. |
| Governance files | LICENSE, SECURITY.md, CONTRIBUTING.md, PUBLIC_BOUNDARY.md, .gitignore | Generic repository governance. LICENSE is the Apache-2.0 license text. | Admit. |
| v0.1.1 release records | docs/release/ | Original release-control documentation with no source payload, private record, or project-specific content. | Admit. |

## Explicit Exceptions And Limits

- LICENSE intentionally redistributes Apache License 2.0 text.
- Bootstrap design documentation links to Python, OWASP, GitHub, and Semantic
  Versioning sources. It does not bundle their documentation or source code.
- The test-only dependency ranges are PyYAML>=6.0.2,<7 and jsonschema>=4.23,<5.
  The framework has no runtime Python dependency and no vendored third-party
  packages.
- The public release uses GitHub-generated source archives only; it has no
  binary, research, data, or manuscript asset.
- Pattern scans cannot prove legal ownership, absence of every possible secret,
  or compliance with an external institution or agreement.

## Retrospective Scan Result

For the seven commits reachable from the v0.1.1 candidate at review time, the
selected GitHub-token, cloud-key, private-key, assignment-style secret, and
known private-path patterns returned zero matches. The released tracked tree
has no Git LFS objects or Git submodules. Local dangling Git objects were
older generic candidate commits and are not reachable from the published tag;
they are not part of the public release tree.

Before R11-G6, the accountable maintainer must confirm that every contribution
is original, properly authorized, or used under a compatible license, and that
no privacy, employment, institutional, DUA, confidentiality, or copyright
restriction blocks publication. Any uncertainty is a release stop.
