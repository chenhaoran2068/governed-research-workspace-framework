# Framework v0.2.0 Release Evidence

Status: historical pre-release candidate evidence. It is not a C4 approval,
tag, GitHub Release, installed-source receipt, or local workspace-retirement
receipt.

## Candidate Evidence Required

The reviewed candidate must retain evidence that:

- it starts from the exact approved v0.1.2 baseline;
- its diff is limited to the approved v0.2.0 allowlist;
- future framework-integrated bootstrap output omits `Papers/` and
  `roots.papers`;
- standalone output is unchanged;
- a synthetic legacy manifest retaining `roots.papers: Papers` remains schema
  valid without schema change or migration;
- the synthetic workspace Framework version and synthetic System compatibility
  declarations are internally consistent;
- local tests and three-platform Python 3.11/3.14 CI pass; and
- material, rights, dependency, privacy, secret, and release-boundary review
  has passed.

## Release And Adoption Separation

After an approved exact main commit receives a v0.2.0 annotated tag and
matching GitHub Release, retain the separate C4 receipt. That public release
does not prove Research System compatibility, local Framework source adoption,
Codex runtime adoption, or permission to retire a physical `Papers/` root.
