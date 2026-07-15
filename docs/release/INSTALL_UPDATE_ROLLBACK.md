# Manual Framework Installation, Update, And Rollback

Status: candidate operating contract for the future public v0.1.1 release.
The framework is a source package and controlled workspace-bootstrap tool; it
is not a Codex skill installer, a concrete research system, or a project
migration utility.

## Preconditions

- Use an existing public release tag, not a candidate branch, for normal use.
- Use Git and Python 3.11 or later for validation and bootstrap.
- Keep the framework source checkout outside any workspace the helper creates.
  Do not place research data, projects, credentials, or private material in
  the framework checkout.
- Preserve a clean checkout. Local edits are not a supported update target;
  use a documented fork or separate private overlay.

## Obtain And Verify A Release

Clone an exact future public tag into a source directory chosen by the user:

~~~text
git clone --branch v0.1.1 --depth 1 https://github.com/chenhaoran2068/governed-research-workspace-framework.git <framework-source-root>
cd <framework-source-root>
git describe --exact-match --tags HEAD
git rev-parse HEAD
git status --porcelain
python --version
python -m unittest discover -s tests -v
~~~

Replace v0.1.1 only with an existing reviewed release tag. The tag command must
print the selected tag, the status command must be empty, and tests must pass.
Do not use main or another mutable branch name as a release identity.

## Create A New Empty Workspace

The framework source checkout and a workspace are distinct. After the user
selects an existing ordinary parent directory, run the helper without
confirmation to obtain a no-write plan:

~~~text
python scripts/bootstrap_workspace.py --parent <existing-parent> --workspace-id <lowercase-ascii-id> --profile framework_integrated
~~~

Explain the emitted plan, then wait for accountable human approval. Rerun only
with the exact plan ID and an approval reference:

~~~text
python scripts/bootstrap_workspace.py --parent <existing-parent> --workspace-id <lowercase-ascii-id> --profile framework_integrated --confirm-create --plan-id <previewed-plan-id> --approval-reference <approval-reference>
~~~

Use profile standalone only when its smaller root set is appropriate. The
public helper rejects private_lab_extended and does not install a concrete
system, register a system, create a project, copy data, or grant access.

## Update

Update only the clean framework source checkout. Record its current tag and
commit, inspect the next release notes and compatibility statement, then:

~~~text
git status --porcelain
git describe --exact-match --tags HEAD
git rev-parse HEAD
git fetch --tags --prune
git checkout --detach v0.1.2
git describe --exact-match --tags HEAD
python -m unittest discover -s tests -v
~~~

v0.1.2 is illustrative. Use only a tag that exists and whose release notes
support the intended update. Updating the framework source does not alter any
existing workspace, workspace manifest, registered system, project binding,
data, or project state.

## Rollback

Rollback returns only the framework source checkout to a previously recorded
clean release. It does not delete or modify an already created workspace.

~~~text
git checkout --detach <previous-reviewed-tag-or-commit>
git status --porcelain
git describe --exact-match --tags HEAD
python -m unittest discover -s tests -v
~~~

If the source version and an existing workspace manifest need compatibility
review, stop and assess that explicitly. Do not rerun bootstrap into an
existing workspace, force overwrite, or attempt an automatic manifest
migration.

## Failure Boundary

Stop when the tag is not exact, the checkout is dirty, Python is unsupported,
tests fail, the bootstrap parent is unsafe or linked, the target exists, the
approval reference is absent, or a plan no longer matches its preview. This
public package contains no automatic installer, updater, rollback helper,
migration tool, system installer, or destructive repair path.
