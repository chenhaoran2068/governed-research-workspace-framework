#!/usr/bin/env python3

"""Validate a knowledge-service manifest without reading source artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PACKAGE_ROOT / "schemas" / "knowledge_service_manifest.schema.json"


def validate_manifest_document(document: Any, schema: dict[str, Any]) -> list[str]:
    """Return structural and v2 path-boundary errors for one manifest."""

    errors = [error.message for error in Draft202012Validator(schema).iter_errors(document)]
    if errors or not isinstance(document, dict) or document.get("manifest_schema_version") != 2:
        return errors

    service_root = PurePosixPath(document["service_root"])
    boundary = document["source_artifact_boundary"]
    artifact_root = PurePosixPath(boundary["artifact_store_root"])
    try:
        relative_store = artifact_root.relative_to(service_root)
    except ValueError:
        errors.append("artifact_store_root must be below the declared service_root")
        return errors

    if len(relative_store.parts) < 2 or relative_store.parts[0] != "reference_manager":
        errors.append("artifact_store_root must be inside service_root/reference_manager/")
    forbidden_segments = {"archive", "github", "public", "release"}
    if forbidden_segments.intersection(relative_store.parts):
        errors.append("artifact_store_root must not use a public or release path")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    document = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    errors = validate_manifest_document(document, schema)
    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps({"status": "valid", "manifest_schema_version": document["manifest_schema_version"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
