# Framework v0.2.0 Release Gate

Status: pre-release gate record. It is not an approval, tag, GitHub Release,
or installed-workspace receipt.

## Candidate Scope

v0.2.0 changes future confirmed `framework_integrated` bootstrap output only:
it omits the Framework-owned `Papers/` root and generated `roots.papers`
entry. It retains `standalone`, manifest schema version `1`, legacy manifest
validity, and the bootstrap's existing confirmation and path-safety controls.

It does not inspect, migrate, or delete an existing `Papers/` directory, and
does not add a universal manuscript/submission tree or change a real System.

## Required Evidence Before C4

1. Exact local candidate diff is limited to the approved allowlist.
2. Targeted and complete local tests pass with the approved interpreter.
3. Two M48 reviews cover implementation, public claims, tests, release
   materials, privacy/rights, dependencies, and prohibited scope.
4. Windows, Ubuntu, and macOS CI succeed on Python 3.11 and 3.14 with no
   unexpected skip.
5. A reviewed PR merges to protected `main`; the accountable human then
   reviews the exact resulting main commit.
6. Only after explicit C4 approval may an annotated `v0.2.0` tag and matching
   GitHub Release be created for that exact commit.

## Post-Release Boundaries

The public Release does not install or migrate Framework source, update a
concrete System, update Codex runtime, or authorize retirement of a local
`Papers/` directory. Those remain separate controlled actions.
