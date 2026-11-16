"""Synthetic tests for the v0.6.0 read-only placement-integrity auditor."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_workspace_placement.py"
SCOPE_SCHEMA = ROOT / "schemas" / "workspace_placement_audit_scope.schema.json"
REPORT_SCHEMA = ROOT / "schemas" / "workspace_placement_audit_report.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas" / "workspace_placement_receipt.schema.json"
QUEUE_SCHEMA = ROOT / "schemas" / "workspace_placement_remediation_queue.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("workspace_placement_audit", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load workspace placement auditor.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def inventory(root: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            records[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            records[path.relative_to(root).as_posix() + "/"] = "directory"
    return records


class WorkspacePlacementAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name) / "synthetic-workspace"
        self.workspace.mkdir()
        for name in ("Systems", "Methods", "Data_Raw", "Github", "Ops", "Archive"):
            (self.workspace / name).mkdir()
        (self.workspace / "Systems" / "example-system").mkdir()
        (self.workspace / "Methods" / "workbench" / "__pycache__").mkdir(parents=True)
        (self.workspace / "Methods" / "workbench" / "__pycache__" / "generated.pyc").write_bytes(b"synthetic")
        (self.workspace / "Ops" / "legacy-empty").mkdir()
        (self.workspace / "Ops" / "workspace_hygiene").mkdir()
        (self.workspace / "Ops" / "workspace_hygiene" / "placement_receipts").mkdir()
        (self.workspace / "Data_Raw" / "restricted-source" / "nested").mkdir(parents=True)
        (self.workspace / "Data_Raw" / "restricted-source" / "nested" / "do-not-read.txt").write_text("synthetic-only", encoding="utf-8")
        (self.workspace / "unattributed-root-note.txt").write_text("synthetic-only", encoding="utf-8")
        (self.workspace / "Methods" / "workbench" / "wrong-location.txt").write_text("synthetic-only", encoding="utf-8")
        (self.workspace / "Methods" / "workbench" / "correct-location.txt").write_text("synthetic-only", encoding="utf-8")

        manifest = {
            "manifest_schema_version": 1,
            "framework_version": "0.5.0",
            "workspace_id": "synthetic-workspace",
            "workspace_profile": "framework_integrated",
            "roots": {
                "systems": "Systems",
                "methods": "Methods",
                "data_raw": "Data_Raw",
                "github": "Github",
                "ops": "Ops",
                "archive": "Archive",
            },
            "registered_systems": [
                {"system_id": "example-system", "path": "Systems/example-system", "system_version": "0.1.0"},
                {"system_id": "missing-system", "path": "Systems/missing-system", "system_version": "0.1.0"},
            ],
        }
        (self.workspace / "WORKSPACE_MANIFEST.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        receipt_path = self.workspace / "Ops" / "workspace_hygiene" / "placement_receipts" / "synthetic-fix.json"
        receipt_path.write_text(json.dumps({
            "record_type": "workspace_placement_receipt",
            "receipt_schema_version": "1.0.0",
            "operation_id": "synthetic-fix",
            "declared_owner_root_key": "methods",
            "target_root": "Methods",
            "written_relative_paths": ["Methods/workbench/correct-location.txt"],
            "ephemeral_outputs": [],
            "repair_relations": [{
                "mistaken_relative_path": "Methods/workbench/wrong-location.txt",
                "corrected_relative_path": "Methods/workbench/correct-location.txt",
                "source_disposition": "retained_pending_human_review",
            }],
            "human_reference": "synthetic-test",
        }, indent=2) + "\n", encoding="utf-8")
        self.scope_path = self.workspace / "Ops" / "workspace_hygiene" / "placement_audit_scope.json"
        scope = {
            "record_type": "workspace_placement_audit_scope",
            "scope_schema_version": "1.0.0",
            "workspace_root": str(self.workspace),
            "workspace_manifest_path": "WORKSPACE_MANIFEST.yaml",
            "audit_mode": "read_only",
            "included_root_keys": ["systems", "methods", "data_raw", "github", "ops", "archive"],
            "root_review_overrides": [
                {"root_key": "methods", "inspection_depth": "recursive_metadata"},
                {"root_key": "ops", "inspection_depth": "recursive_metadata"},
                {"root_key": "data_raw", "inspection_depth": "root_only"},
            ],
            "known_ephemeral_paths": [
                {"path": "Ops/workspace_hygiene", "owner": "Synthetic audit", "regeneration_basis": "Synthetic tests."}
            ],
            "placement_receipt_paths": ["Ops/workspace_hygiene/placement_receipts/synthetic-fix.json"],
            "excluded_relative_paths": [],
            "generated_directory_names": ["__pycache__"],
            "report_root": "Ops/workspace_hygiene/reports",
        }
        self.scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def command(self, *extra: str) -> list[str]:
        return [sys.executable, str(SCRIPT), "--scope", str(self.scope_path), *extra]

    def run_command(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(self.command(*extra), text=True, capture_output=True, check=False)

    def test_scope_templates_and_schemas_are_valid(self) -> None:
        scope = json.loads((ROOT / "templates" / "workspace_placement_audit_scope.template.json").read_text(encoding="utf-8"))
        scope["workspace_root"] = str(self.workspace)
        Draft202012Validator(json.loads(SCOPE_SCHEMA.read_text(encoding="utf-8"))).validate(scope)

        receipt = json.loads((ROOT / "templates" / "workspace_placement_receipt.template.json").read_text(encoding="utf-8"))
        receipt.update({
            "operation_id": "synthetic-operation",
            "declared_owner_root_key": "ops",
            "target_root": "Ops",
            "written_relative_paths": ["Ops/example.txt"],
            "human_reference": "synthetic-test",
        })
        Draft202012Validator(json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))).validate(receipt)

        queue = json.loads((ROOT / "templates" / "workspace_placement_remediation_queue.template.json").read_text(encoding="utf-8"))
        queue["audit_id"] = "workspace-placement-audit-" + "0" * 24
        Draft202012Validator(json.loads(QUEUE_SCHEMA.read_text(encoding="utf-8"))).validate(queue)

    def test_default_run_is_read_only_and_reports_boundaries(self) -> None:
        module = load_module()
        before = inventory(self.workspace)
        payload = module.run(module.parse_args(["--scope", str(self.scope_path)]))
        after = inventory(self.workspace)
        self.assertEqual(before, after)
        self.assertEqual(payload["status"], "read_only_report")
        report = payload["report"]
        self.assertFalse(report["execution_boundary"]["modified_audited_material"])
        self.assertFalse(report["execution_boundary"]["report_written"])
        self.assertFalse(report["execution_boundary"]["automatic_cleanup"])
        self.assertFalse(report["execution_boundary"]["automatic_move"])
        self.assertFalse(report["execution_boundary"]["automatic_delete"])
        statuses = {item["status"] for item in report["records"]}
        self.assertIn("known_generated_outside_declared_zone", statuses)
        self.assertIn("candidate_empty_directory", statuses)
        self.assertIn("registered_path_missing", statuses)
        self.assertIn("unattributed_path", statuses)
        self.assertIn("possible_repair_residue", statuses)
        self.assertFalse(any(item["relative_path"].endswith("do-not-read.txt") for item in report["records"]))
        Draft202012Validator(json.loads(REPORT_SCHEMA.read_text(encoding="utf-8"))).validate(report)

    def test_report_write_requires_explicit_path_and_approval(self) -> None:
        missing = self.run_command("--write-report")
        self.assertEqual(missing.returncode, 2)
        self.assertFalse((self.workspace / "Ops" / "workspace_hygiene" / "reports").exists())

        report_path = "Ops/workspace_hygiene/reports/synthetic-audit.json"
        result = self.run_command(
            "--write-report", "--report-path", report_path, "--approval-reference", "synthetic-approval"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "report_written")
        written = self.workspace / Path(report_path)
        self.assertTrue(written.is_file())
        report = json.loads(written.read_text(encoding="utf-8"))
        self.assertTrue(report["execution_boundary"]["report_written"])
        self.assertEqual(report["report_write_approval_reference"], "synthetic-approval")
        Draft202012Validator(json.loads(REPORT_SCHEMA.read_text(encoding="utf-8"))).validate(report)

    def test_scope_cannot_escape_workspace_or_name_unknown_root(self) -> None:
        scope = json.loads(self.scope_path.read_text(encoding="utf-8"))
        scope["workspace_manifest_path"] = "../outside.yaml"
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not match", result.stderr)

        scope["workspace_manifest_path"] = "WORKSPACE_MANIFEST.yaml"
        scope["included_root_keys"].append("unknown_root")
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertIn("not declared", result.stderr)

    def test_scope_refuses_duplicate_depth_overrides(self) -> None:
        scope = json.loads(self.scope_path.read_text(encoding="utf-8"))
        scope["root_review_overrides"].append({"root_key": "ops", "inspection_depth": "root_only"})
        self.scope_path.write_text(json.dumps(scope), encoding="utf-8")
        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertIn("more than one", result.stderr)

    def test_symlink_below_selected_root_is_not_traversed_when_supported(self) -> None:
        linked = self.workspace / "Methods" / "linked-outside"
        outside = Path(self.temporary_directory.name) / "outside"
        outside.mkdir()
        (outside / "outside-only.txt").write_text("synthetic-only", encoding="utf-8")
        try:
            linked.symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest("Symbolic links are unavailable in this test environment: %s" % error)
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)["report"]
        refused = [item for item in report["records"] if item["status"] == "refused_reparse_point"]
        self.assertTrue(any(item["relative_path"] == "Methods/linked-outside" for item in refused))
        self.assertFalse(any("outside-only.txt" in item["relative_path"] for item in report["records"]))

    def test_nested_git_worktree_is_an_opaque_boundary(self) -> None:
        nested = self.workspace / "Ops" / "nested-worktree"
        nested.mkdir()
        (nested / ".git").write_text("gitdir: synthetic\n", encoding="utf-8")
        (nested / "nested-only.txt").write_text("synthetic-only", encoding="utf-8")
        result = self.run_command()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)["report"]
        self.assertTrue(any(
            item["status"] == "not_assessed" and item["relative_path"] == "Ops/nested-worktree"
            for item in report["records"]
        ))
        self.assertFalse(any("nested-only.txt" in item["relative_path"] for item in report["records"]))


if __name__ == "__main__":
    unittest.main()
