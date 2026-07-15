"""End-to-end and failure-path tests for the framework workspace bootstrap."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml
from jsonschema import Draft202012Validator, RefResolver


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "bootstrap_workspace.py"


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location("framework_bootstrap", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load framework bootstrap helper.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BootstrapWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.parent = Path(self.temporary_directory.name) / "workspaces"
        self.parent.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def command(
        self,
        *extra: str,
        workspace_id: str = "example-workspace",
        profile: str = "framework_integrated",
        parent: Path | None = None,
    ) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT_PATH),
            "--parent",
            str(parent or self.parent),
            "--workspace-id",
            workspace_id,
            "--profile",
            profile,
            *extra,
        ]

    def run_command(self, *extra: str, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(self.command(*extra, **kwargs), text=True, capture_output=True, check=False)

    def preview(self, **kwargs: object) -> dict[str, object]:
        result = self.run_command(**kwargs)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "preview")
        return payload

    @staticmethod
    def workspace_validator() -> Draft202012Validator:
        schema = json.loads(
            (REPOSITORY_ROOT / "schemas" / "workspace_manifest.schema.json").read_text(encoding="utf-8")
        )
        system_schema = json.loads(
            (REPOSITORY_ROOT / "schemas" / "system_manifest.schema.json").read_text(encoding="utf-8")
        )
        resolver = RefResolver(schema["$id"], schema, store={system_schema["$id"]: system_schema})
        return Draft202012Validator(schema, resolver=resolver)

    def test_preview_makes_no_write_and_has_exact_plan(self) -> None:
        payload = self.preview()
        self.assertEqual(list(self.parent.iterdir()), [])
        plan = payload["plan"]
        self.assertEqual(plan["tool_version"], "0.1.1")
        self.assertEqual(plan["framework_version"], "0.1.0")
        self.assertEqual(plan["workspace_id"], "example-workspace")
        self.assertEqual(plan["profile"], "framework_integrated")
        self.assertIn("parent_identity", plan)
        self.assertEqual(plan["planned_directories"], [
            "Systems", "Skills", "Shared", "Knowledge", "Methods", "Instances",
            "Papers", "Data_Raw", "Github", "Ops", "Archive",
        ])
        self.assertTrue(plan["scope"]["creates_empty_workspace_only"])
        self.assertFalse(plan["scope"]["installs_system"])

    def test_confirmed_profiles_create_only_allowlisted_scaffolds_and_valid_manifests(self) -> None:
        module = load_bootstrap_module()
        validator = self.workspace_validator()
        expected_roots = {
            "standalone": {"Systems", "Instances"},
            "framework_integrated": set(module.PROFILE_ROOTS["framework_integrated"]),
        }
        for profile, expected_directories in expected_roots.items():
            with self.subTest(profile=profile):
                workspace_id = "workspace-" + profile.replace("_", "-")
                plan = self.preview(workspace_id=workspace_id, profile=profile)["plan"]
                result = self.run_command(
                    "--confirm-create",
                    "--plan-id",
                    plan["plan_id"],
                    "--approval-reference",
                    "approval-001",
                    workspace_id=workspace_id,
                    profile=profile,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                workspace = self.parent / workspace_id
                actual_directories = {
                    path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_dir()
                }
                actual_files = {
                    path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file()
                }
                self.assertEqual(actual_directories, expected_directories)
                self.assertEqual(actual_files, set(module.PLANNED_FILES))

                manifest = yaml.safe_load((workspace / "WORKSPACE_MANIFEST.yaml").read_text(encoding="utf-8"))
                validator.validate(manifest)
                self.assertEqual(manifest["workspace_profile"], profile)
                self.assertEqual(manifest["registered_systems"], [])
                self.assertEqual(manifest["shared_services"], [])

                receipt = json.loads((workspace / "bootstrap_receipt.json").read_text(encoding="utf-8"))
                self.assertEqual(receipt["approval_reference"], "approval-001")
                self.assertTrue(receipt["receipt_file_not_self_hashed"])
                for record in receipt["created_file_hashes"]:
                    self.assertEqual(module.sha256_file(workspace / record["relative_path"]), record["sha256"])

    def test_confirmation_requires_matching_plan_and_approval_reference(self) -> None:
        self.preview()
        missing_plan = self.run_command("--confirm-create", "--approval-reference", "approval-001")
        self.assertEqual(missing_plan.returncode, 2)
        wrong_plan = self.run_command(
            "--confirm-create", "--plan-id", "grwf-plan-wrong", "--approval-reference", "approval-001"
        )
        self.assertEqual(wrong_plan.returncode, 2)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_private_profile_unknown_and_abbreviated_arguments_are_refused(self) -> None:
        private_profile = subprocess.run(
            [
                sys.executable, str(SCRIPT_PATH), "--parent", str(self.parent),
                "--workspace-id", "example-workspace", "--profile", "private_lab_extended",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(private_profile.returncode, 2)
        abbreviated = subprocess.run(
            [
                sys.executable, str(SCRIPT_PATH), "--parent", str(self.parent),
                "--workspace-id", "example-workspace", "--prof", "standalone",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(abbreviated.returncode, 2)
        unknown = self.run_command("--data-source", "not-allowed")
        self.assertEqual(unknown.returncode, 2)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_existing_or_escaped_workspace_is_not_overwritten(self) -> None:
        existing = self.parent / "example-workspace"
        existing.mkdir()
        marker = existing / "marker.txt"
        marker.write_text("do not overwrite\n", encoding="utf-8")
        result = self.run_command()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_text(encoding="utf-8"), "do not overwrite\n")

        escaped = self.run_command(workspace_id="../outside")
        self.assertEqual(escaped.returncode, 2)
        self.assertFalse((self.parent.parent / "outside").exists())

    def test_replaced_parent_invalidates_reviewed_plan(self) -> None:
        plan = self.preview()["plan"]
        parked_parent = self.parent.parent / "original-workspaces"
        self.parent.rename(parked_parent)
        self.parent.mkdir()
        result = self.run_command(
            "--confirm-create", "--plan-id", plan["plan_id"], "--approval-reference", "approval-001"
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(self.parent.iterdir()), [])
        self.assertEqual(list(parked_parent.iterdir()), [])

    def test_linked_parent_and_target_are_refused_when_supported(self) -> None:
        actual_parent = self.parent.parent / "actual-parent"
        actual_parent.mkdir()
        linked_parent = self.parent.parent / "linked-parent"
        try:
            linked_parent.symlink_to(actual_parent, target_is_directory=True)
        except OSError as error:
            self.skipTest("Symbolic links are unavailable in this test environment: %s" % error)
        parent_result = self.run_command(parent=linked_parent)
        self.assertEqual(parent_result.returncode, 2)
        self.assertEqual(list(actual_parent.iterdir()), [])

        linked_target = self.parent / "example-workspace"
        linked_target.symlink_to(self.parent / "uncreated-target", target_is_directory=True)
        target_result = self.run_command()
        self.assertEqual(target_result.returncode, 2)
        self.assertTrue(linked_target.is_symlink())

    @unittest.skipUnless(sys.platform == "win32", "Windows junction test")
    def test_windows_junction_parent_is_refused(self) -> None:
        actual_parent = self.parent.parent / "junction-target"
        actual_parent.mkdir()
        junction_parent = self.parent.parent / "junction-parent"

        def literal(path: Path) -> str:
            return "'{}'".format(str(path).replace("'", "''"))

        create = subprocess.run(
            [
                "powershell", "-NoProfile", "-NonInteractive", "-Command",
                "New-Item -ItemType Junction -Path {} -Target {} -ErrorAction Stop | Out-Null".format(
                    literal(junction_parent), literal(actual_parent)
                ),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(create.returncode, 0, create.stdout + create.stderr)
        try:
            result = self.run_command(parent=junction_parent)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(list(actual_parent.iterdir()), [])
        finally:
            subprocess.run(
                [
                    "powershell", "-NoProfile", "-NonInteractive", "-Command",
                    "Remove-Item -LiteralPath {} -Force -ErrorAction Stop".format(literal(junction_parent)),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_injected_write_failure_cleans_only_owned_staging_directory(self) -> None:
        module = load_bootstrap_module()
        args = module.parse_args([
            "--parent", str(self.parent), "--workspace-id", "example-workspace",
            "--profile", "framework_integrated",
        ])
        plan = module.build_plan(args)
        original_write_text = module.write_text
        write_count = 0

        def failing_write_text(path: Path, content: str) -> None:
            nonlocal write_count
            write_count += 1
            if write_count == 2:
                raise OSError("injected write failure")
            original_write_text(path, content)

        module.write_text = failing_write_text
        try:
            with self.assertRaises(OSError):
                module.create_workspace(plan, "approval-001")
        finally:
            module.write_text = original_write_text
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_changed_assets_and_package_internal_parent_are_refused(self) -> None:
        module = load_bootstrap_module()
        args = module.parse_args([
            "--parent", str(self.parent), "--workspace-id", "example-workspace",
            "--profile", "framework_integrated",
        ])
        plan = module.build_plan(args)
        with mock.patch.object(module, "asset_inventory", return_value=[]):
            with self.assertRaises(module.BootstrapRefusal) as raised:
                module.create_workspace(plan, "approval-001")
        self.assertIn("assets changed", str(raised.exception))
        self.assertEqual(list(self.parent.iterdir()), [])

        result = self.run_command(parent=REPOSITORY_ROOT)
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the framework package", result.stderr)

    def test_script_has_no_source_data_or_network_input_and_refuses_old_python(self) -> None:
        module = load_bootstrap_module()
        parser = module.parse_args
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser(["--parent", str(self.parent), "--workspace-id", "example", "--profile", "standalone", "--data", "x"])
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        for forbidden_import in ("import urllib", "import socket", "import requests"):
            self.assertNotIn(forbidden_import, source)
        with mock.patch.object(module.sys, "version_info", (3, 10, 99)):
            with self.assertRaises(module.BootstrapRefusal) as raised:
                module.require_supported_python()
        self.assertIn("Python 3.11 or later", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
