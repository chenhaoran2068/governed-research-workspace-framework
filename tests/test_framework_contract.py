import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, RefResolver, ValidationError

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = ("E:\\\\", "C:\\\\Users", "Chenhaoran", "patient-derived")
MANIFEST_VALIDATOR_PATH = ROOT / "scripts" / "validate_knowledge_service_manifest.py"


def load_manifest_validator_module():
    spec = importlib.util.spec_from_file_location("knowledge_service_validator", MANIFEST_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load knowledge-service validator.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FrameworkContractTests(unittest.TestCase):
    @staticmethod
    def _load_yaml(relative_path):
        return yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))

    @staticmethod
    def _load_schema(name):
        return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

    def test_required_public_files_exist(self):
        required = [
            "README.md",
            "PUBLIC_BOUNDARY.md",
            "docs/root_ownership_contract.md",
            "docs/reference_workspace_tree.md",
            "docs/controlled_workspace_bootstrap_design_v1.md",
            "docs/multi_system_contract.md",
            "docs/knowledge_service_contract_v1.md",
            "docs/controlled_reference_manager_library_contract_v1.md",
            "docs/installation_profiles.md",
            "docs/papers_root_retirement_compatibility_v1.md",
            "docs/release/V0_1_1_RELEASE_GATE.md",
            "docs/release/INSTALL_UPDATE_ROLLBACK.md",
            "docs/release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.1.1.md",
            "docs/release/RELEASE_INTEGRITY_POLICY_v1.md",
            "docs/release/RELEASE_NOTES_v0.1.1.md",
            "docs/release/V0_1_1_RELEASE_EVIDENCE.md",
            "docs/release/V0_1_2_RELEASE_GATE.md",
            "docs/release/V0_1_2_RELEASE_EVIDENCE.md",
            "docs/release/RELEASE_NOTES_v0.1.2.md",
            "docs/release/V0_2_0_RELEASE_GATE.md",
            "docs/release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.2.0.md",
            "docs/release/RELEASE_NOTES_v0.2.0.md",
            "docs/release/V0_2_0_RELEASE_EVIDENCE.md",
            "schemas/workspace_manifest.schema.json",
            "schemas/system_manifest.schema.json",
            "schemas/project_system_binding.schema.json",
            "schemas/knowledge_service_manifest.schema.json",
            "templates/workspace_manifest.template.yaml",
            "templates/workspace_manifest.standalone.template.yaml",
            "templates/workspace_manifest.framework_integrated.template.yaml",
            "templates/workspace_bootstrap_readme.template.md",
            "scripts/bootstrap_workspace.py",
            "scripts/validate_knowledge_service_manifest.py",
            "templates/system_manifest.template.yaml",
            "templates/project_system_binding.template.yaml",
            "templates/knowledge_service_manifest.template.yaml",
            "examples/synthetic_multi_system_workspace/WORKSPACE_MANIFEST.yaml",
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-reading-knowledge/KNOWLEDGE_SERVICE_MANIFEST.yaml",
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-managed-reference-library/KNOWLEDGE_SERVICE_MANIFEST.yaml",
            "docs/release/V0_3_0_RELEASE_GATE.md",
            "docs/release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.3.0.md",
            "docs/release/RELEASE_NOTES_v0.3.0.md",
            "docs/release/V0_3_0_RELEASE_EVIDENCE.md",
            "docs/release/V0_4_0_RELEASE_GATE.md",
            "docs/release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.4.0.md",
            "docs/release/RELEASE_NOTES_v0.4.0.md",
            "docs/release/V0_4_0_RELEASE_EVIDENCE.md",
        ]
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_schemas_are_valid_json_and_versioned(self):
        for path in (ROOT / "schemas").glob("*.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertIn("title", schema)
            self.assertIn("required", schema)

        workspace = json.loads((ROOT / "schemas/workspace_manifest.schema.json").read_text(encoding="utf-8"))
        system = json.loads((ROOT / "schemas/system_manifest.schema.json").read_text(encoding="utf-8"))
        knowledge_service = self._load_schema("knowledge_service_manifest.schema.json")
        self.assertIn("framework_version", workspace["required"])
        self.assertIn("allOf", system)
        self.assertIn("framework_compatibility", system["properties"])
        self.assertEqual(knowledge_service["properties"]["service_kind"]["const"], "source_backed_knowledge")
        for schema_path in (ROOT / "schemas").glob("*.schema.json"):
            Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))

    def test_synthetic_profiles_and_examples_validate_against_schemas(self):
        workspace_schema = self._load_schema("workspace_manifest.schema.json")
        system_schema = self._load_schema("system_manifest.schema.json")
        project_schema = self._load_schema("project_system_binding.schema.json")
        knowledge_service_schema = self._load_schema("knowledge_service_manifest.schema.json")
        resolver = RefResolver(
            workspace_schema["$id"],
            workspace_schema,
            store={system_schema["$id"]: system_schema},
        )

        workspace_validator = Draft202012Validator(workspace_schema, resolver=resolver)
        system_validator = Draft202012Validator(system_schema)
        project_validator = Draft202012Validator(project_schema)
        knowledge_service_validator = Draft202012Validator(knowledge_service_schema)

        for path in [
            "profiles/standalone_workspace.example.yaml",
            "profiles/framework_integrated.example.yaml",
            "examples/synthetic_multi_system_workspace/WORKSPACE_MANIFEST.yaml",
        ]:
            workspace_validator.validate(self._load_yaml(path))

        for path in [
            "examples/synthetic_multi_system_workspace/Systems/example-research-system/SYSTEM_MANIFEST.yaml",
            "examples/synthetic_multi_system_workspace/Systems/example-method-system/SYSTEM_MANIFEST.yaml",
        ]:
            system_validator.validate(self._load_yaml(path))

        project_validator.validate(self._load_yaml(
            "examples/synthetic_multi_system_workspace/Instances/Research0001_synthetic/00_state/PROJECT_SYSTEM_BINDING.yaml"
        ))
        knowledge_service_validator.validate(self._load_yaml(
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-reading-knowledge/KNOWLEDGE_SERVICE_MANIFEST.yaml"
        ))
        managed_service = self._load_yaml(
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-managed-reference-library/KNOWLEDGE_SERVICE_MANIFEST.yaml"
        )
        knowledge_service_validator.validate(managed_service)
        self.assertEqual(
            load_manifest_validator_module().validate_manifest_document(managed_service, knowledge_service_schema),
            [],
        )

    def test_synthetic_registered_systems_cover_the_v0_4_workspace_example(self):
        workspace = self._load_yaml("examples/synthetic_multi_system_workspace/WORKSPACE_MANIFEST.yaml")
        self.assertEqual(workspace["framework_version"], "0.4.0")
        for path in [
            "examples/synthetic_multi_system_workspace/Systems/example-research-system/SYSTEM_MANIFEST.yaml",
            "examples/synthetic_multi_system_workspace/Systems/example-method-system/SYSTEM_MANIFEST.yaml",
        ]:
            system = self._load_yaml(path)
            self.assertEqual(
                system["framework_compatibility"]["supported_framework_versions"],
                ">=0.1.0 <0.5.0",
            )

    def test_synthetic_knowledge_service_requires_explicit_consumer_matching(self):
        workspace = self._load_yaml("examples/synthetic_multi_system_workspace/WORKSPACE_MANIFEST.yaml")
        service = self._load_yaml(
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-reading-knowledge/KNOWLEDGE_SERVICE_MANIFEST.yaml"
        )
        systems = {
            system["system_id"]: system
            for system in (
                self._load_yaml("examples/synthetic_multi_system_workspace/Systems/example-research-system/SYSTEM_MANIFEST.yaml"),
                self._load_yaml("examples/synthetic_multi_system_workspace/Systems/example-method-system/SYSTEM_MANIFEST.yaml"),
            )
        }

        self.assertIn(service["service_id"], workspace["shared_services"])
        self.assertEqual(service["service_root"], "Knowledge/" + service["service_id"])
        self.assertEqual(service["allowed_consumer_system_ids"], ["example-research-system"])
        self.assertIn(service["service_id"], systems["example-research-system"]["optional_shared_services"])
        self.assertNotIn(service["service_id"], systems["example-method-system"]["optional_shared_services"])

    def test_managed_library_requires_a_private_store_below_its_service_root(self):
        schema = self._load_schema("knowledge_service_manifest.schema.json")
        validator_module = load_manifest_validator_module()
        service = self._load_yaml(
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-managed-reference-library/KNOWLEDGE_SERVICE_MANIFEST.yaml"
        )

        self.assertEqual(validator_module.validate_manifest_document(service, schema), [])

        service["source_artifact_boundary"]["artifact_store_root"] = "C:/outside/zotero-data"
        self.assertTrue(validator_module.validate_manifest_document(service, schema))

        service["source_artifact_boundary"]["artifact_store_root"] = (
            "Knowledge/another-service/reference_manager/synthetic-zotero-data"
        )
        self.assertIn(
            "artifact_store_root must be below the declared service_root",
            validator_module.validate_manifest_document(service, schema),
        )

        service["source_artifact_boundary"]["artifact_store_root"] = (
            "Knowledge/synthetic-managed-reference-library/release/synthetic-zotero-data"
        )
        self.assertTrue(validator_module.validate_manifest_document(service, schema))

    def test_knowledge_service_schema_rejects_relaxed_access_boundary(self):
        schema = self._load_schema("knowledge_service_manifest.schema.json")
        validator = Draft202012Validator(schema)
        service = self._load_yaml(
            "examples/synthetic_multi_system_workspace/Knowledge/synthetic-reading-knowledge/KNOWLEDGE_SERVICE_MANIFEST.yaml"
        )
        service["access_boundary"]["workspace_scanning"] = True
        with self.assertRaises(ValidationError):
            validator.validate(service)

    def test_templates_and_examples_have_no_private_workspace_markers(self):
        checked_roots = [ROOT / "profiles", ROOT / "templates", ROOT / "examples", ROOT / "scripts"]
        for checked_root in checked_roots:
            for path in checked_root.rglob("*"):
                if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".py"}:
                    continue
                content = path.read_text(encoding="utf-8")
                for marker in PRIVATE_MARKERS:
                    self.assertNotIn(marker, content, f"{marker!r} found in {path}")

    def test_public_package_contains_no_manager_database_or_source_artifact(self):
        forbidden_suffixes = {".pdf", ".pyc", ".sqlite", ".sqlite3"}
        forbidden_names = {"zotero.sqlite", "zotero.sqlite.bak", "zotero.sqlite-journal"}
        tracked_files = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, text=True, check=True, capture_output=True
        ).stdout.splitlines()
        offenders = [
            relative_path
            for relative_path in tracked_files
            if Path(relative_path).suffix.lower() in forbidden_suffixes
            or Path(relative_path).name.lower() in forbidden_names
        ]
        self.assertEqual(offenders, [])

    def test_synthetic_project_has_one_primary_system(self):
        path = ROOT / "examples/synthetic_multi_system_workspace/Instances/Research0001_synthetic/00_state/PROJECT_SYSTEM_BINDING.yaml"
        binding = path.read_text(encoding="utf-8")
        self.assertEqual(sum(line.startswith("primary_system:") for line in binding.splitlines()), 1)
        self.assertIn("contributing_systems:", binding)

    def test_reference_tree_has_stable_cross_system_locations(self):
        tree = (ROOT / "docs/reference_workspace_tree.md").read_text(encoding="utf-8")
        for location in [
            "WORKSPACE_MANIFEST.yaml",
            "Systems/",
            "<system-id>/",
            "SYSTEM_MANIFEST.yaml",
            "Instances/",
            "00_state/",
            "PROJECT_SYSTEM_BINDING.yaml",
        ]:
            self.assertIn(location, tree)
        self.assertIn("does not define universal data, manuscript, method, or", tree)
        self.assertIn("KNOWLEDGE_SERVICE_MANIFEST.yaml", tree)
        self.assertNotIn("Papers/                                         [bootstrap default]", tree)
        roots = (ROOT / "docs" / "root_ownership_contract.md").read_text(encoding="utf-8")
        self.assertNotIn("| `Papers/` |", roots)

    def test_bootstrap_design_has_accepted_runtime_and_profile_boundaries(self):
        design = (ROOT / "docs/controlled_workspace_bootstrap_design_v1.md").read_text(encoding="utf-8")
        for requirement in [
            "minimum runtime: Python 3.11",
            "## Design Evidence",
            "--profile <standalone|framework_integrated>",
            "`private_lab_extended`",
            "--confirm-create",
            "--plan-id",
            "--approval-reference",
            "Windows, Ubuntu, and macOS",
        ]:
            self.assertIn(requirement, design)

    def test_release_governance_records_and_metadata_are_present(self):
        script = (ROOT / "scripts/bootstrap_workspace.py").read_text(encoding="utf-8")
        versioning = (ROOT / "docs/versioning_and_compatibility.md").read_text(encoding="utf-8")
        evidence = (ROOT / "docs/release/V0_1_1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn('TOOL_VERSION = "0.4.0"', script)
        self.assertIn('FRAMEWORK_VERSION = "0.4.0"', script)
        self.assertNotIn("0.1.0-framework-candidate", script)
        self.assertIn("immutable public contract by policy", versioning)
        self.assertIn("## v0.3.0 Knowledge-Service Compatibility", versioning)
        self.assertIn("## v0.4.0 Controlled Reference-Manager Compatibility", versioning)
        self.assertIn("R11-G6", evidence)
        self.assertIn("R11-G7", evidence)

    def test_current_release_identity_is_not_inferred_from_candidate_records(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        gate = (ROOT / "docs/release/V0_1_1_RELEASE_GATE.md").read_text(encoding="utf-8")
        evidence = (ROOT / "docs/release/V0_1_1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")

        self.assertIn("Determine the current published version from", readme)
        self.assertNotIn("The unreleased `v0.1.1-release-governance` candidate", readme)
        self.assertIn("## v0.2.0 Papers-Root Retirement", roadmap)
        self.assertIn("Status: historical pre-release gate", gate)
        self.assertIn("Status: historical pre-release candidate evidence", evidence)


if __name__ == "__main__":
    unittest.main()
