import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = ("E:\\\\", "C:\\\\Users", "Chenhaoran", "patient-derived")


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
            "docs/installation_profiles.md",
            "docs/release/V0_1_1_RELEASE_GATE.md",
            "docs/release/INSTALL_UPDATE_ROLLBACK.md",
            "docs/release/PUBLIC_MATERIAL_RIGHTS_REVIEW_v0.1.1.md",
            "docs/release/RELEASE_INTEGRITY_POLICY_v1.md",
            "docs/release/RELEASE_NOTES_v0.1.1.md",
            "docs/release/V0_1_1_RELEASE_EVIDENCE.md",
            "docs/release/V0_1_2_RELEASE_GATE.md",
            "docs/release/V0_1_2_RELEASE_EVIDENCE.md",
            "docs/release/RELEASE_NOTES_v0.1.2.md",
            "schemas/workspace_manifest.schema.json",
            "schemas/system_manifest.schema.json",
            "schemas/project_system_binding.schema.json",
            "templates/workspace_manifest.template.yaml",
            "templates/workspace_manifest.standalone.template.yaml",
            "templates/workspace_manifest.framework_integrated.template.yaml",
            "templates/workspace_bootstrap_readme.template.md",
            "scripts/bootstrap_workspace.py",
            "templates/system_manifest.template.yaml",
            "templates/project_system_binding.template.yaml",
            "examples/synthetic_multi_system_workspace/WORKSPACE_MANIFEST.yaml",
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
        self.assertIn("framework_version", workspace["required"])
        self.assertIn("allOf", system)
        self.assertIn("framework_compatibility", system["properties"])
        for schema_path in (ROOT / "schemas").glob("*.schema.json"):
            Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))

    def test_synthetic_profiles_and_examples_validate_against_schemas(self):
        workspace_schema = self._load_schema("workspace_manifest.schema.json")
        system_schema = self._load_schema("system_manifest.schema.json")
        project_schema = self._load_schema("project_system_binding.schema.json")
        resolver = RefResolver(
            workspace_schema["$id"],
            workspace_schema,
            store={system_schema["$id"]: system_schema},
        )

        workspace_validator = Draft202012Validator(workspace_schema, resolver=resolver)
        system_validator = Draft202012Validator(system_schema)
        project_validator = Draft202012Validator(project_schema)

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

    def test_templates_and_examples_have_no_private_workspace_markers(self):
        checked_roots = [ROOT / "profiles", ROOT / "templates", ROOT / "examples", ROOT / "scripts"]
        for checked_root in checked_roots:
            for path in checked_root.rglob("*"):
                if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".py"}:
                    continue
                content = path.read_text(encoding="utf-8")
                for marker in PRIVATE_MARKERS:
                    self.assertNotIn(marker, content, f"{marker!r} found in {path}")

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
        self.assertIn('TOOL_VERSION = "0.1.1"', script)
        self.assertNotIn("0.1.0-framework-candidate", script)
        self.assertIn("immutable public contract by policy", versioning)
        self.assertIn("R11-G6", evidence)
        self.assertIn("R11-G7", evidence)

    def test_current_release_identity_is_not_inferred_from_candidate_records(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        gate = (ROOT / "docs/release/V0_1_1_RELEASE_GATE.md").read_text(encoding="utf-8")
        evidence = (ROOT / "docs/release/V0_1_1_RELEASE_EVIDENCE.md").read_text(encoding="utf-8")

        self.assertIn("Determine the current published version from", readme)
        self.assertNotIn("The unreleased `v0.1.1-release-governance` candidate", readme)
        self.assertIn("## v0.1.2 Current-State Correction", roadmap)
        self.assertIn("Status: historical pre-release gate", gate)
        self.assertIn("Status: historical pre-release candidate evidence", evidence)


if __name__ == "__main__":
    unittest.main()
