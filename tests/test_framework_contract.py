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
            "docs/multi_system_contract.md",
            "docs/installation_profiles.md",
            "schemas/workspace_manifest.schema.json",
            "schemas/system_manifest.schema.json",
            "schemas/project_system_binding.schema.json",
            "templates/workspace_manifest.template.yaml",
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
        checked_roots = [ROOT / "profiles", ROOT / "templates", ROOT / "examples"]
        for checked_root in checked_roots:
            for path in checked_root.rglob("*"):
                if not path.is_file():
                    continue
                content = path.read_text(encoding="utf-8")
                for marker in PRIVATE_MARKERS:
                    self.assertNotIn(marker, content, f"{marker!r} found in {path}")

    def test_synthetic_project_has_one_primary_system(self):
        path = ROOT / "examples/synthetic_multi_system_workspace/Instances/Research0001_synthetic/00_state/PROJECT_SYSTEM_BINDING.yaml"
        binding = path.read_text(encoding="utf-8")
        self.assertEqual(sum(line.startswith("primary_system:") for line in binding.splitlines()), 1)
        self.assertIn("contributing_systems:", binding)


if __name__ == "__main__":
    unittest.main()
