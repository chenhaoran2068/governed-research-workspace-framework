#!/usr/bin/env python3

"""Read-only placement-integrity audit for one caller-named workspace.

The auditor only inspects directory metadata from a scope file beneath the
workspace being audited. It never opens source material, follows a symbolic
link or Windows reparse point, changes workspace material, moves paths, or
deletes paths. Writing a JSON report is an optional, separately confirmed
operational action restricted to the scope's declared report root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path, PurePath
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


TOOL_VERSION = "0.6.0"
SCOPE_SCHEMA_VERSION = "1.0.0"
REPORT_SCHEMA_VERSION = "1.0.0"
SCRIPT_PATH = Path(__file__).resolve()
PACKAGE_ROOT = SCRIPT_PATH.parent.parent
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
SCOPE_SCHEMA_PATH = SCHEMA_ROOT / "workspace_placement_audit_scope.schema.json"
REPORT_SCHEMA_PATH = SCHEMA_ROOT / "workspace_placement_audit_report.schema.json"
KNOWN_ROOT_FILES = {"WORKSPACE_MANIFEST.yaml", "README.md", "bootstrap_receipt.json"}


class AuditRefusal(ValueError):
    """Raised when an audit would exceed its read-only placement boundary."""


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_link_or_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    if os.name != "nt":
        return False
    try:
        attributes = os.lstat(path).st_file_attributes
    except FileNotFoundError:
        return False
    reparse_attribute = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(attributes & reparse_attribute)


def is_within(candidate: Path, ancestor: Path) -> bool:
    try:
        candidate.relative_to(ancestor)
    except ValueError:
        return False
    return True


def normalize_relative(raw_path: str, label: str) -> Path:
    if not raw_path or "\x00" in raw_path:
        raise AuditRefusal("%s must be a nonempty ordinary relative path." % label)
    candidate = Path(raw_path)
    if candidate.is_absolute() or candidate.drive or any(part == ".." for part in PurePath(raw_path).parts):
        raise AuditRefusal("%s must stay relative to the named workspace." % label)
    if str(candidate) in {".", ""}:
        raise AuditRefusal("%s must name a path below the workspace root." % label)
    return candidate


def assert_no_reparse_ancestor(candidate: Path, workspace_root: Path) -> None:
    current = workspace_root
    for part in candidate.relative_to(workspace_root).parts:
        current = current / part
        if current.exists() and is_link_or_reparse_point(current):
            raise AuditRefusal("Refusing a path containing a symbolic link or reparse point: %s" % current)


def workspace_relative_path(workspace_root: Path, relative_path: str, label: str) -> Path:
    relative = normalize_relative(relative_path, label)
    candidate = workspace_root / relative
    if not is_within(candidate, workspace_root):
        raise AuditRefusal("%s escapes the named workspace." % label)
    assert_no_reparse_ancestor(candidate, workspace_root)
    return candidate


def relative_display(path: Path, workspace_root: Path) -> str:
    return path.relative_to(workspace_root).as_posix()


def load_json_schema(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AuditRefusal("Required schema is missing: %s" % path)
    return json.loads(path.read_text(encoding="utf-8"))


def load_scope(scope_path: Path) -> dict[str, Any]:
    if not scope_path.is_file() or is_link_or_reparse_point(scope_path):
        raise AuditRefusal("Scope must be one ordinary JSON file: %s" % scope_path)
    try:
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise AuditRefusal("Scope is not valid JSON: %s" % error) from error
    errors = sorted(Draft202012Validator(load_json_schema(SCOPE_SCHEMA_PATH)).iter_errors(scope), key=str)
    if errors:
        raise AuditRefusal("Scope does not satisfy its schema: %s" % errors[0].message)
    return scope


def load_workspace_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.is_file() or is_link_or_reparse_point(manifest_path):
        raise AuditRefusal("Workspace manifest must be one ordinary YAML file: %s" % manifest_path)
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise AuditRefusal("Workspace manifest is not valid YAML: %s" % error) from error
    if not isinstance(manifest, dict) or not isinstance(manifest.get("roots"), dict):
        raise AuditRefusal("Workspace manifest must contain a roots mapping.")
    if not isinstance(manifest.get("registered_systems"), list):
        raise AuditRefusal("Workspace manifest must contain a registered_systems list.")
    return manifest


def record(
    status: str,
    relative_path: str,
    evidence: str,
    recommended_action: str,
    root_key: str | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "relative_path": relative_path,
        "root_key": root_key,
        "evidence": evidence,
        "recommended_action": recommended_action,
    }


def is_excluded(relative_path: str, excluded: set[str]) -> bool:
    return any(relative_path == item or relative_path.startswith(item + "/") for item in excluded)


def is_declared_ephemeral(relative_path: str, ephemeral: set[str]) -> bool:
    return any(relative_path == item or relative_path.startswith(item + "/") for item in ephemeral)


def inspection_depth(scope: dict[str, Any], root_key: str) -> str:
    for override in scope.get("root_review_overrides", []):
        if override["root_key"] == root_key:
            return override["inspection_depth"]
    return "root_only"


def ordinary_children(path: Path) -> list[Path]:
    try:
        return sorted(path.iterdir(), key=lambda item: item.name.lower())
    except OSError as error:
        raise AuditRefusal("Unable to inspect directory metadata: %s" % error) from error


def has_no_entries(path: Path) -> bool:
    try:
        next(path.iterdir())
    except StopIteration:
        return True
    return False


def is_nested_git_worktree(path: Path) -> bool:
    """Treat a directory with a Git administrative entry as an opaque boundary."""
    return path.is_dir() and (path / ".git").exists()


def inspect_directory(
    directory: Path,
    workspace_root: Path,
    root_key: str,
    recursive: bool,
    excluded: set[str],
    ephemeral: set[str],
    generated_names: set[str],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    stack = [directory]
    while stack:
        current = stack.pop()
        for child in ordinary_children(current):
            relative_path = relative_display(child, workspace_root)
            if is_excluded(relative_path, excluded):
                records.append(record(
                    "not_assessed", relative_path, "Path is explicitly excluded by the caller-named scope.",
                    "retain", root_key,
                ))
                continue
            if is_link_or_reparse_point(child):
                records.append(record(
                    "refused_reparse_point", relative_path,
                    "Audit does not traverse symbolic links or Windows reparse points.",
                    "do_not_traverse", root_key,
                ))
                continue
            if child.is_dir():
                if is_nested_git_worktree(child):
                    records.append(record(
                        "not_assessed", relative_path,
                        "Directory is a nested Git worktree and remains an opaque ownership boundary.",
                        "retain", root_key,
                    ))
                    continue
                if child.name in generated_names and not is_declared_ephemeral(relative_path, ephemeral):
                    records.append(record(
                        "known_generated_outside_declared_zone", relative_path,
                        "Directory name matches a caller-declared generated-artifact marker outside a declared ephemeral path.",
                        "review_for_cleanup", root_key,
                    ))
                elif has_no_entries(child) and not is_declared_ephemeral(relative_path, ephemeral):
                    records.append(record(
                        "candidate_empty_directory", relative_path,
                        "Directory has no child entries; emptiness alone does not authorize deletion.",
                        "review_for_cleanup", root_key,
                    ))
                elif is_declared_ephemeral(relative_path, ephemeral):
                    records.append(record(
                        "conforms", relative_path,
                        "Path is explicitly declared as a regenerable operational location.",
                        "retain", root_key,
                    ))
                elif not recursive:
                    records.append(record(
                        "not_assessed", relative_path,
                        "The selected root uses root-only metadata inspection; deeper content remains owned by its declared System, Method, service, or Study.",
                        "retain", root_key,
                    ))
                if recursive and not is_declared_ephemeral(relative_path, ephemeral):
                    stack.append(child)
    return records


def validate_scope_paths(scope: dict[str, Any], workspace_root: Path, manifest: dict[str, Any]) -> tuple[dict[str, Path], set[str], set[str], set[str]]:
    roots: dict[str, Path] = {}
    for root_key, raw_path in manifest["roots"].items():
        if not isinstance(root_key, str) or not isinstance(raw_path, str):
            raise AuditRefusal("Workspace manifest roots must map strings to strings.")
        roots[root_key] = workspace_relative_path(workspace_root, raw_path, "manifest roots.%s" % root_key)

    missing_root_keys = sorted(set(scope["included_root_keys"]) - set(roots))
    if missing_root_keys:
        raise AuditRefusal("Scope names root keys not declared by the workspace manifest: %s" % ", ".join(missing_root_keys))

    override_keys = [item["root_key"] for item in scope.get("root_review_overrides", [])]
    if len(override_keys) != len(set(override_keys)):
        raise AuditRefusal("Scope must not define more than one inspection-depth override for the same root key.")

    excluded = {
        relative_display(workspace_relative_path(workspace_root, item, "excluded_relative_paths"), workspace_root)
        for item in scope.get("excluded_relative_paths", [])
    }
    ephemeral = {
        relative_display(workspace_relative_path(workspace_root, item["path"], "known_ephemeral_paths.path"), workspace_root)
        for item in scope.get("known_ephemeral_paths", [])
    }
    generated_names = set(scope.get("generated_directory_names", []))
    return roots, excluded, ephemeral, generated_names


def load_placement_receipts(scope: dict[str, Any], workspace_root: Path, roots: dict[str, Path]) -> list[tuple[str, dict[str, Any]]]:
    raw_receipt_paths = scope.get("placement_receipt_paths", [])
    if not raw_receipt_paths:
        return []
    ops_root = roots.get("ops")
    if ops_root is None:
        raise AuditRefusal("Caller-named placement receipts require a declared ops root.")
    receipt_schema = load_json_schema(SCHEMA_ROOT / "workspace_placement_receipt.schema.json")
    receipts: list[tuple[str, dict[str, Any]]] = []
    for raw_path in raw_receipt_paths:
        receipt_path = workspace_relative_path(workspace_root, raw_path, "placement_receipt_paths")
        if not is_within(receipt_path, ops_root):
            raise AuditRefusal("Placement receipt must be stored below the declared ops root.")
        if not receipt_path.is_file() or is_link_or_reparse_point(receipt_path):
            raise AuditRefusal("Caller-named placement receipt is not one ordinary file: %s" % receipt_path)
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise AuditRefusal("Placement receipt is not valid JSON: %s" % error) from error
        errors = sorted(Draft202012Validator(receipt_schema).iter_errors(receipt), key=str)
        if errors:
            raise AuditRefusal("Placement receipt does not satisfy its schema: %s" % errors[0].message)
        receipts.append((relative_display(receipt_path, workspace_root), receipt))
    return receipts


def build_report(scope_path: Path) -> dict[str, Any]:
    scope = load_scope(scope_path)
    workspace_root = Path(scope["workspace_root"]).expanduser()
    if not workspace_root.is_absolute() or not workspace_root.is_dir() or is_link_or_reparse_point(workspace_root):
        raise AuditRefusal("workspace_root must be one existing ordinary absolute directory.")
    workspace_root = workspace_root.resolve(strict=True)

    if not is_within(scope_path.resolve(strict=True), workspace_root):
        raise AuditRefusal("Scope must be stored below the named workspace root.")
    if Path(scope["workspace_root"]).resolve(strict=True) != workspace_root:
        raise AuditRefusal("workspace_root no longer resolves to the reviewed location.")

    manifest_path = workspace_relative_path(workspace_root, scope["workspace_manifest_path"], "workspace_manifest_path")
    manifest = load_workspace_manifest(manifest_path)
    roots, excluded, ephemeral, generated_names = validate_scope_paths(scope, workspace_root, manifest)
    placement_receipts = load_placement_receipts(scope, workspace_root, roots)
    records: list[dict[str, Any]] = []

    declared_root_paths = {relative_display(path, workspace_root) for path in roots.values()}
    root_files = KNOWN_ROOT_FILES | {relative_display(manifest_path, workspace_root)}
    for child in ordinary_children(workspace_root):
        child_relative = relative_display(child, workspace_root)
        if child_relative in declared_root_paths or child_relative in root_files:
            continue
        if is_link_or_reparse_point(child):
            records.append(record("refused_reparse_point", child_relative, "Unexpected root-level link or reparse point is not traversed.", "do_not_traverse"))
        else:
            records.append(record("unattributed_path", child_relative, "Root-level path is not a declared Framework root or known workspace record.", "register_or_explain"))

    for root_key in scope["included_root_keys"]:
        root = roots[root_key]
        root_relative = relative_display(root, workspace_root)
        if not root.exists():
            records.append(record("declared_absent", root_relative, "Manifest declares this root but it is not present on disk.", "retain", root_key))
            continue
        if is_link_or_reparse_point(root):
            records.append(record("refused_reparse_point", root_relative, "Declared root is a link or reparse point and is not traversed.", "do_not_traverse", root_key))
            continue
        records.append(record("conforms", root_relative, "Manifest declares this Framework root.", "retain", root_key))
        records.extend(inspect_directory(
            root, workspace_root, root_key,
            inspection_depth(scope, root_key) == "recursive_metadata",
            excluded, ephemeral, generated_names,
        ))

    systems_root = roots.get("systems")
    if systems_root is not None:
        for system in manifest["registered_systems"]:
            if not isinstance(system, dict) or not isinstance(system.get("path"), str):
                records.append(record("unattributed_path", "registered_systems", "Manifest contains a malformed registered-system record.", "human_decision_required", "systems"))
                continue
            registered_path = workspace_relative_path(workspace_root, system["path"], "registered_systems.path")
            registered_relative = relative_display(registered_path, workspace_root)
            if not is_within(registered_path, systems_root):
                records.append(record("unattributed_path", registered_relative, "Registered system path is not below the declared systems root.", "human_decision_required", "systems"))
            elif not registered_path.exists():
                records.append(record("registered_path_missing", registered_relative, "Workspace manifest registers this System path, but the path is absent.", "register_or_explain", "systems"))
            elif is_link_or_reparse_point(registered_path):
                records.append(record("refused_reparse_point", registered_relative, "Registered System path is a link or reparse point and is not traversed.", "do_not_traverse", "systems"))
            else:
                records.append(record("conforms", registered_relative, "Workspace manifest explicitly registers this System path.", "retain", "systems"))

    for receipt_relative, receipt in placement_receipts:
        for relation in receipt["repair_relations"]:
            mistaken_path = workspace_relative_path(
                workspace_root, relation["mistaken_relative_path"], "repair_relations.mistaken_relative_path"
            )
            corrected_path = workspace_relative_path(
                workspace_root, relation["corrected_relative_path"], "repair_relations.corrected_relative_path"
            )
            mistaken_relative = relative_display(mistaken_path, workspace_root)
            corrected_relative = relative_display(corrected_path, workspace_root)
            mistaken_exists = mistaken_path.exists()
            corrected_exists = corrected_path.exists()
            evidence_prefix = "Caller-named receipt %s declares a repair from %s to %s. " % (
                receipt_relative, mistaken_relative, corrected_relative
            )
            if mistaken_exists and corrected_exists:
                records.append(record(
                    "possible_repair_residue", mistaken_relative,
                    evidence_prefix + "Both paths remain; this may be repair residue and requires human review.",
                    "human_decision_required",
                ))
            elif mistaken_exists:
                records.append(record(
                    "not_assessed", mistaken_relative,
                    evidence_prefix + "The original path remains but the corrected path is absent; do not infer a cleanup action.",
                    "human_decision_required",
                ))
            elif corrected_exists:
                records.append(record(
                    "conforms", corrected_relative,
                    evidence_prefix + "The original path is absent and the declared corrected path is present.",
                    "retain",
                ))
            else:
                records.append(record(
                    "not_assessed", corrected_relative,
                    evidence_prefix + "Neither path is present; retain the receipt and request owner review.",
                    "human_decision_required",
                ))

    status_counts = Counter(item["status"] for item in records)
    seed = "|".join((sha256_file(scope_path), sha256_file(manifest_path), now_utc()))
    report = {
        "record_type": "workspace_placement_audit_report",
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "audit_id": "workspace-placement-audit-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24],
        "created_at": now_utc(),
        "audit_mode": "read_only",
        "workspace_root": workspace_root.as_posix(),
        "scope_path": scope_path.resolve(strict=True).as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "summary": {"record_count": len(records), "status_counts": dict(sorted(status_counts.items()))},
        "records": records,
        "execution_boundary": {
            "modified_audited_material": False,
            "report_written": False,
            "automatic_cleanup": False,
            "automatic_move": False,
            "automatic_delete": False,
        },
    }
    errors = sorted(Draft202012Validator(load_json_schema(REPORT_SCHEMA_PATH)).iter_errors(report), key=str)
    if errors:
        raise RuntimeError("Generated report violates its schema: %s" % errors[0].message)
    return report


def write_report(report: dict[str, Any], scope_path: Path, approval_reference: str, raw_report_path: str) -> Path:
    scope = load_scope(scope_path)
    workspace_root = Path(scope["workspace_root"]).resolve(strict=True)
    report_root = workspace_relative_path(workspace_root, scope["report_root"], "report_root")
    report_path = workspace_relative_path(workspace_root, raw_report_path, "report_path")
    if not is_within(report_path, report_root) or report_path.suffix.lower() != ".json":
        raise AuditRefusal("Report path must be a new .json file below the declared report_root.")
    if report_path.exists() or is_link_or_reparse_point(report_path):
        raise AuditRefusal("Refusing to overwrite or follow a report path: %s" % report_path)
    if not approval_reference.strip():
        raise AuditRefusal("Writing a local report requires a nonempty approval reference.")
    report_root.mkdir(parents=True, exist_ok=True)
    if is_link_or_reparse_point(report_root):
        raise AuditRefusal("Report root became a link or reparse point.")
    report["execution_boundary"]["report_written"] = True
    report["report_write_approval_reference"] = approval_reference.strip()
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only workspace placement-integrity audit.", allow_abbrev=False)
    parser.add_argument("--scope", required=True, help="Caller-named scope JSON stored below the workspace root.")
    parser.add_argument("--write-report", action="store_true", help="Write the reviewed report only with an explicit report path and approval reference.")
    parser.add_argument("--report-path", help="New workspace-relative JSON path below the scope's report_root.")
    parser.add_argument("--approval-reference", help="Accountable-human reference required only when writing a report.")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.write_report and (not args.report_path or not args.approval_reference):
        raise AuditRefusal("--write-report requires both --report-path and --approval-reference.")
    if not args.write_report and (args.report_path or args.approval_reference):
        raise AuditRefusal("--report-path and --approval-reference are valid only with --write-report.")
    scope_path = Path(args.scope).expanduser().resolve(strict=True)
    report = build_report(scope_path)
    if args.write_report:
        report_path = write_report(report, scope_path, args.approval_reference, args.report_path)
        return {"status": "report_written", "report_path": report_path.as_posix(), "report": report}
    return {"status": "read_only_report", "report": report}


def main(argv: list[str] | None = None) -> int:
    try:
        payload = run(parse_args(argv))
    except (AuditRefusal, OSError, ValueError) as error:
        print(json.dumps({"status": "refused", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
