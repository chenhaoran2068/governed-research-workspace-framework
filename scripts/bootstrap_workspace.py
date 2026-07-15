#!/usr/bin/env python3

"""Create one empty framework workspace after exact human confirmation.

The helper creates a generic workspace root only. It never creates a project,
installs a system, reads or copies source material, calls a network service, or
asserts research, compliance, or access status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TOOL_VERSION = "0.1.0-framework-candidate"
FRAMEWORK_VERSION = "0.1.0"
PLAN_SCHEMA_VERSION = "1.0.0"
RECEIPT_SCHEMA_VERSION = "1.0.0"
MIN_PYTHON = (3, 11)
SAFE_WORKSPACE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

SCRIPT_PATH = Path(__file__).resolve()
PACKAGE_ROOT = SCRIPT_PATH.parent.parent
TEMPLATE_ROOT = PACKAGE_ROOT / "templates"
README_TEMPLATE = TEMPLATE_ROOT / "workspace_bootstrap_readme.template.md"
MANIFEST_TEMPLATES = {
    "standalone": TEMPLATE_ROOT / "workspace_manifest.standalone.template.yaml",
    "framework_integrated": TEMPLATE_ROOT / "workspace_manifest.framework_integrated.template.yaml",
}
PROFILE_ROOTS = {
    "standalone": ("Systems", "Instances"),
    "framework_integrated": (
        "Systems",
        "Skills",
        "Shared",
        "Knowledge",
        "Methods",
        "Instances",
        "Papers",
        "Data_Raw",
        "Github",
        "Ops",
        "Archive",
    ),
}
PLANNED_FILES = ("WORKSPACE_MANIFEST.yaml", "README.md", "bootstrap_receipt.json")


class BootstrapRefusal(ValueError):
    """Raised when a requested bootstrap operation violates this contract."""


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(payload: dict[str, Any], stream: Any = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def require_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        current = ".".join(str(part) for part in sys.version_info[:3])
        minimum = ".".join(str(part) for part in MIN_PYTHON)
        raise BootstrapRefusal(
            "Python %s or later is required; current interpreter is %s. "
            "Install or select a supported Python interpreter, then rerun."
            % (minimum, current)
        )


def is_link_or_reparse_point(path: Path) -> bool:
    """Identify symlinks on every platform and Windows directory junctions."""
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


def filesystem_identity(path: Path) -> dict[str, int]:
    metadata = os.stat(path, follow_symlinks=False)
    return {"device": int(metadata.st_dev), "inode": int(metadata.st_ino)}


def is_within(candidate: Path, ancestor: Path) -> bool:
    try:
        candidate.relative_to(ancestor)
    except ValueError:
        return False
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or create one empty governed research workspace framework.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--parent",
        required=True,
        help="Existing ordinary directory in which one new workspace may be created.",
    )
    parser.add_argument(
        "--workspace-id",
        required=True,
        help="Lowercase ASCII directory identifier for the new direct-child workspace.",
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=tuple(PROFILE_ROOTS),
        help="Empty scaffold profile to create after preview and confirmation.",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Emit an explicit no-write preview; preview is already the default.",
    )
    parser.add_argument(
        "--confirm-create",
        action="store_true",
        help="Create only with the exact preview plan ID and approval reference.",
    )
    parser.add_argument("--plan-id", help="Exact plan ID returned by the reviewed preview.")
    parser.add_argument(
        "--approval-reference",
        help="Nonempty accountable-human approval reference for the reviewed plan.",
    )
    return parser.parse_args(argv)


def validate_workspace_id(workspace_id: str) -> str:
    if not SAFE_WORKSPACE_ID.fullmatch(workspace_id):
        raise BootstrapRefusal(
            "Workspace ID must use lowercase ASCII letters, digits, and hyphens, "
            "start with an alphanumeric character, and be at most 64 characters."
        )
    return workspace_id


def validate_parent(raw_parent: str) -> Path:
    candidate = Path(raw_parent).expanduser()
    if not candidate.exists() or not candidate.is_dir():
        raise BootstrapRefusal("Parent must already exist as a directory: %s" % candidate)
    if is_link_or_reparse_point(candidate):
        raise BootstrapRefusal("Parent must not be a symbolic link or reparse point: %s" % candidate)
    resolved = candidate.resolve(strict=True)
    if is_within(resolved, PACKAGE_ROOT):
        raise BootstrapRefusal(
            "Parent must be outside the framework package so generated workspaces "
            "cannot enter the public repository."
        )
    return resolved


def validate_plan_parent(plan: dict[str, Any]) -> Path:
    parent = validate_parent(str(plan["parent"]))
    if parent.as_posix() != plan["parent"]:
        raise BootstrapRefusal("Parent no longer resolves to the reviewed location.")
    if filesystem_identity(parent) != plan["parent_identity"]:
        raise BootstrapRefusal("Parent identity changed after the reviewed preview.")
    return parent


def build_target(parent: Path, workspace_id: str) -> Path:
    requested = parent / validate_workspace_id(workspace_id)
    if requested.exists() or is_link_or_reparse_point(requested):
        raise BootstrapRefusal("Refusing to create or overwrite existing workspace: %s" % requested)
    target = requested.resolve(strict=False)
    if target.parent != parent:
        raise BootstrapRefusal("Final workspace must be a direct child of the selected parent.")
    if is_within(target, PACKAGE_ROOT):
        raise BootstrapRefusal("Final workspace must be outside the framework package.")
    return target


def asset_inventory(profile: str) -> list[dict[str, str]]:
    assets = (SCRIPT_PATH, README_TEMPLATE, MANIFEST_TEMPLATES[profile])
    for asset in assets:
        if not asset.is_file():
            raise BootstrapRefusal("Required bootstrap asset is missing: %s" % asset)
    return [
        {
            "relative_path": asset.relative_to(PACKAGE_ROOT).as_posix(),
            "sha256": sha256_file(asset),
        }
        for asset in assets
    ]


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    parent = validate_parent(args.parent)
    workspace_id = validate_workspace_id(args.workspace_id)
    target = build_target(parent, workspace_id)
    scope = {
        "creates_empty_workspace_only": True,
        "installs_system": False,
        "creates_project": False,
        "copies_or_reads_source_data": False,
        "uses_network_or_accounts": False,
        "asserts_research_or_compliance_status": False,
    }
    payload = {
        "plan_schema_version": PLAN_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "minimum_python": ".".join(str(part) for part in MIN_PYTHON),
        "parent": parent.as_posix(),
        "parent_identity": filesystem_identity(parent),
        "workspace_id": workspace_id,
        "profile": args.profile,
        "final_workspace": target.as_posix(),
        "planned_directories": list(PROFILE_ROOTS[args.profile]),
        "planned_files": list(PLANNED_FILES),
        "asset_inventory": asset_inventory(args.profile),
        "scope": scope,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["plan_id"] = "grwf-plan-" + sha256_bytes(encoded)[:24]
    return payload


def render_template(path: Path, replacements: dict[str, str]) -> str:
    rendered = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        rendered = rendered.replace("{{%s}}" % key, value)
    if "{{" in rendered or "}}" in rendered:
        raise BootstrapRefusal("Unresolved placeholder in template: %s" % path)
    return rendered


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def collect_hashed_files(root: Path, excluded: set[str] | None = None) -> list[dict[str, str]]:
    excluded = excluded or set()
    records = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative_path = path.relative_to(root).as_posix()
        if relative_path not in excluded:
            records.append({"relative_path": relative_path, "sha256": sha256_file(path)})
    return records


def validate_staged_tree(staging_root: Path, plan: dict[str, Any]) -> None:
    actual_directories = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_dir()
    }
    actual_files = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_file()
    }
    if actual_directories != set(plan["planned_directories"]):
        raise RuntimeError("Staging directory set differs from the allowlisted scaffold.")
    if actual_files != set(plan["planned_files"]):
        raise RuntimeError("Staging file set differs from the allowlisted scaffold.")


def remove_staging_tree(staging_root: Path, plan: dict[str, Any]) -> None:
    if not staging_root.exists():
        return
    parent = validate_plan_parent(plan)
    if is_link_or_reparse_point(staging_root) or is_link_or_reparse_point(parent):
        raise RuntimeError("Refusing to clean a linked or reparse-point staging path.")
    if staging_root.parent != parent or not staging_root.name.startswith(".grwf-bootstrap-"):
        raise RuntimeError("Refusing to clean an unexpected staging path.")
    shutil.rmtree(staging_root)


def create_workspace(plan: dict[str, Any], approval_reference: str) -> dict[str, Any]:
    parent = validate_plan_parent(plan)
    target = build_target(parent, str(plan["workspace_id"]))
    if target.as_posix() != plan["final_workspace"]:
        raise BootstrapRefusal("Final workspace location no longer matches the reviewed preview.")
    if asset_inventory(str(plan["profile"])) != plan["asset_inventory"]:
        raise BootstrapRefusal("Bootstrap assets changed after the reviewed preview.")

    staging_root = parent / (".grwf-bootstrap-" + str(plan["workspace_id"]) + "-" + uuid.uuid4().hex)
    created_at = now_utc()
    try:
        staging_root.mkdir()
        for directory in plan["planned_directories"]:
            (staging_root / directory).mkdir(parents=True, exist_ok=False)

        replacements = {
            "FRAMEWORK_VERSION": str(plan["framework_version"]),
            "WORKSPACE_ID": str(plan["workspace_id"]),
        }
        write_text(
            staging_root / "WORKSPACE_MANIFEST.yaml",
            render_template(MANIFEST_TEMPLATES[str(plan["profile"])], replacements),
        )
        write_text(staging_root / "README.md", render_template(README_TEMPLATE, replacements))

        receipt = {
            "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
            "created_at": created_at,
            "tool_version": TOOL_VERSION,
            "plan": plan,
            "approval_reference": approval_reference,
            "created_file_hashes": collect_hashed_files(staging_root, excluded={"bootstrap_receipt.json"}),
            "receipt_file_not_self_hashed": True,
            "scope": plan["scope"],
        }
        write_text(
            staging_root / "bootstrap_receipt.json",
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        validate_staged_tree(staging_root, plan)
        parent = validate_plan_parent(plan)
        target = build_target(parent, str(plan["workspace_id"]))
        if target.as_posix() != plan["final_workspace"]:
            raise BootstrapRefusal("Final workspace location no longer matches the reviewed preview.")
        staging_root.rename(target)
    except Exception:
        remove_staging_tree(staging_root, plan)
        raise

    return {
        "status": "created",
        "workspace_root": target.as_posix(),
        "plan_id": plan["plan_id"],
        "approval_reference": approval_reference,
        "receipt_path": (target / "bootstrap_receipt.json").as_posix(),
        "next_required_action": "Install or register a reviewed system before creating a project.",
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.plan and args.confirm_create:
        raise BootstrapRefusal("Use either preview or confirmation, not both in one invocation.")
    plan = build_plan(args)
    if not args.confirm_create:
        return {
            "status": "preview",
            "plan": plan,
            "next_required_action": (
                "Review the no-write plan. A human must explicitly approve it before rerunning "
                "with --confirm-create, a matching --plan-id, and a nonempty --approval-reference."
            ),
        }
    if args.plan_id != plan["plan_id"]:
        raise BootstrapRefusal("Provided plan ID does not match the current no-write preview.")
    approval_reference = (args.approval_reference or "").strip()
    if not approval_reference:
        raise BootstrapRefusal("Confirmation requires a nonempty --approval-reference.")
    return create_workspace(plan, approval_reference)


def main(argv: list[str] | None = None) -> int:
    try:
        require_supported_python()
        result = run(parse_args(argv))
        emit(result)
        return 0
    except BootstrapRefusal as error:
        emit({"status": "refused", "reason": str(error)}, stream=sys.stderr)
        return 2
    except Exception as error:
        emit({"status": "error", "reason": str(error)}, stream=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
