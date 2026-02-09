#!/usr/bin/env python3
"""TEMPORARY_PRE_MVP: Internal write plane for UI artifact ingestion.

This module provides a single, controlled path for writing UI artifacts
and updating Mongo catalogs. The runtime read plane remains GET-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

POLICY_DEFAULT_PATH = "library/policies/UI_ARTIFACT_STORAGE_AND_EXECUTION_POLICY.v1.yaml"
TEMPORARY_TAG = "TEMPORARY_PRE_MVP"

VERSION_RE = re.compile(r"\.v(\d+)$")


class WritePlaneError(RuntimeError):
    """Raised when write plane validation fails."""


@dataclass(frozen=True)
class StorageRule:
    base_path: str
    artifact_types: List[str]


@dataclass(frozen=True)
class PolicyRules:
    ui_phase: StorageRule
    ui_design: StorageRule


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _parse_top_level_fields(lines: Iterable[str]) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        values[key] = value
    return values


def _parse_policy(path: Path) -> PolicyRules:
    if not path.exists():
        raise WritePlaneError(f"Policy not found: {path}")
    fields = []
    with path.open("r", encoding="utf-8") as handle:
        fields = list(handle)

    ui_phase_base = None
    ui_design_base = None
    ui_phase_types: List[str] = []
    ui_design_types: List[str] = []

    current_section: Optional[str] = None
    in_types = False

    for raw in fields:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("ui_phase_artifacts:"):
            current_section = "ui_phase_artifacts"
            in_types = False
            continue
        if stripped.startswith("ui_design_policies:"):
            current_section = "ui_design_policies"
            in_types = False
            continue
        if stripped.startswith("artifact_types:"):
            in_types = True
            continue

        if current_section and "base_path:" in stripped:
            _, value = stripped.split(":", 1)
            base_path = value.strip()
            if current_section == "ui_phase_artifacts":
                ui_phase_base = base_path
            else:
                ui_design_base = base_path
            continue

        if in_types and stripped.startswith("-"):
            _, value = stripped.split("-", 1)
            artifact_type = value.strip()
            if current_section == "ui_phase_artifacts":
                ui_phase_types.append(artifact_type)
            elif current_section == "ui_design_policies":
                ui_design_types.append(artifact_type)

    if not ui_phase_base or not ui_design_base:
        raise WritePlaneError("Policy is missing required base_path entries")
    if not ui_phase_types or not ui_design_types:
        raise WritePlaneError("Policy is missing required artifact_types entries")

    return PolicyRules(
        ui_phase=StorageRule(base_path=ui_phase_base, artifact_types=ui_phase_types),
        ui_design=StorageRule(base_path=ui_design_base, artifact_types=ui_design_types),
    )


def _split_version(value: str) -> Tuple[str, Optional[str]]:
    match = VERSION_RE.search(value)
    if not match:
        return value, None
    version = f"v{match.group(1)}"
    stem = value[: match.start()]
    return stem, version


def _derive_artifact_id(headers: Dict[str, str]) -> Tuple[str, str]:
    if "artifact_id" in headers:
        artifact_id = headers["artifact_id"]
        version = headers.get("version")
        if not version:
            _, version = _split_version(artifact_id)
        if not version:
            raise WritePlaneError("version is required when artifact_id is provided")
        return artifact_id, version

    if "policy_id" in headers:
        policy_id = headers["policy_id"]
        artifact_id, version = _split_version(policy_id)
        if not version:
            raise WritePlaneError("policy_id must include version suffix (.vN)")
        return artifact_id, version

    if "declaration_id" in headers:
        declaration_id = headers["declaration_id"]
        artifact_id, version = _split_version(declaration_id)
        if not version:
            raise WritePlaneError("declaration_id must include version suffix (.vN)")
        return artifact_id, version

    if "adr_id" in headers:
        adr_id = headers["adr_id"]
        artifact_id, version = _split_version(adr_id)
        if not version:
            raise WritePlaneError("adr_id must include version suffix (.vN)")
        return artifact_id, version

    if "artifact_type" in headers:
        artifact_type = headers["artifact_type"]
        version = headers.get("version")
        if not version:
            raise WritePlaneError("version is required when artifact_type is provided")
        return artifact_type, version

    raise WritePlaneError("Unable to derive artifact_id; missing identifier fields")


def _resolve_destination(
    rules: PolicyRules,
    headers: Dict[str, str],
    artifact_id: str,
    version: str,
) -> Path:
    if "artifact_type" in headers:
        artifact_type = headers["artifact_type"]
        if artifact_type not in rules.ui_phase.artifact_types:
            raise WritePlaneError(f"Unsupported artifact_type: {artifact_type}")
        phase = headers.get("phase")
        if not phase:
            raise WritePlaneError("phase is required for ui_phase artifacts")
        base = rules.ui_phase.base_path.replace("{phase}", str(phase))
        filename = f"{artifact_type}.{version}.yaml"
        return Path(base) / filename

    kind = headers.get("kind")
    if kind != "design-interaction-policy":
        raise WritePlaneError("Unsupported artifact kind; policy cannot resolve canonical path")
    if kind not in rules.ui_design.artifact_types:
        raise WritePlaneError(f"Unsupported design policy kind: {kind}")

    base = rules.ui_design.base_path
    filename = f"{artifact_id.lower()}.{version}.yaml"
    return Path(base) / filename


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


def _get_catalog_collections(client: MongoClient) -> Tuple[Collection, Collection]:
    db_name = os.environ.get("LIBRARIAN_MONGO_DB", "librarian")
    db = client[db_name]
    return db["ui_artifact_catalog"], db["ui_artifact_events"]


def _update_catalog(
    *,
    mongo_uri: str,
    artifact_id: str,
    artifact_type: Optional[str],
    kind: Optional[str],
    version: str,
    phase: Optional[str],
    path: str,
    checksum: str,
) -> None:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    catalog, events = _get_catalog_collections(client)
    try:
        catalog.create_index([("artifact_id", ASCENDING), ("version", ASCENDING)], unique=True)
    except PyMongoError as exc:
        raise WritePlaneError(f"Failed to ensure catalog indexes: {exc}") from exc

    document = {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "kind": kind,
        "version": version,
        "phase": phase,
        "path": path,
        "checksum": checksum,
        "tags": [TEMPORARY_TAG],
        "updated_at": _now(),
    }

    try:
        catalog.replace_one({"artifact_id": artifact_id, "version": version}, document, upsert=True)
        events.insert_one(
            {
                "event": "artifact.ingested",
                "timestamp": _now(),
                "artifact_id": artifact_id,
                "version": version,
                "path": path,
                "tags": [TEMPORARY_TAG],
            }
        )
    except PyMongoError as exc:
        raise WritePlaneError(f"Mongo catalog update failed: {exc}") from exc


def ingest(payload_path: Path, policy_path: Path, repo_root: Path, mongo_uri: str) -> Dict[str, str]:
    raw = payload_path.read_text(encoding="utf-8")
    headers = _parse_top_level_fields(raw.splitlines())

    rules = _parse_policy(policy_path)
    artifact_id, version = _derive_artifact_id(headers)
    destination = _resolve_destination(rules, headers, artifact_id, version)

    repo_relative = destination
    if destination.is_absolute():
        repo_relative = destination
    else:
        repo_relative = repo_root / destination

    if repo_relative.exists():
        existing = repo_relative.read_text(encoding="utf-8")
        if existing != raw:
            raise WritePlaneError(f"Refusing to overwrite existing artifact at {repo_relative}")
        checksum = _sha256(existing)
    else:
        _atomic_write(repo_relative, raw)
        checksum = _sha256(raw)

    _update_catalog(
        mongo_uri=mongo_uri,
        artifact_id=artifact_id,
        artifact_type=headers.get("artifact_type"),
        kind=headers.get("kind"),
        version=version,
        phase=headers.get("phase"),
        path=str(destination),
        checksum=checksum,
    )

    return {"artifact_id": artifact_id, "path": str(destination)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TEMPORARY_PRE_MVP UI artifact write plane")
    parser.add_argument("payload", help="Path to YAML payload to ingest")
    parser.add_argument(
        "--policy",
        default=POLICY_DEFAULT_PATH,
        help="Path to storage policy (default: %(default)s)",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root (default: %(default)s)",
    )
    parser.add_argument(
        "--mongo-uri",
        default=os.environ.get("LIBRARIAN_MONGO_URI", "mongodb://mongo:27017"),
        help="Mongo connection string (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload_path = Path(args.payload).resolve()
    policy_path = Path(args.policy).resolve()
    repo_root = Path(args.repo_root).resolve()

    if not payload_path.exists():
        raise SystemExit(f"Payload not found: {payload_path}")

    result = ingest(payload_path, policy_path, repo_root, args.mongo_uri)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except WritePlaneError as exc:
        raise SystemExit(f"[write-plane-error] {exc}")
