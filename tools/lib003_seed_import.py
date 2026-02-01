#!/usr/bin/env python3
"""Reset Mongo and import canonical seed artifacts for LIB-003."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

KIND_VALUES = {"task", "policy", "phase", "law", "report", "schema"}
DOMAIN_VALUES = {"engineering", "governance", "librarian", "ui", "runtime"}
STATUS_VALUES = {"planned", "active", "deprecated", "archived"}
CONTENT_TYPES = {
    ".md": "text/markdown",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
    ".json": "application/json",
}
VERSION_PATTERN = re.compile(r"^(?P<artifact_id>.+)\.(?P<version>v\d+)\.(?P<ext>md|yaml|yml|json)$")


class ImportError(RuntimeError):
    """Raised when seed import validation fails."""


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    artifact_id: str
    kind: str
    domain: str
    status: str
    checksum: str
    created_at: str
    effective_at: str


@dataclass
class ImportResult:
    artifact_id: str
    version: str
    kind: str
    domain: str
    status: str
    source_path: str
    checksum: str


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_manifest(path: Path) -> Tuple[Dict[str, Any], List[ManifestEntry]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - invalid manifest
        raise ImportError(f"Manifest is not valid JSON/YAML: {exc}") from exc

    manifest = raw.get("manifest")
    if not isinstance(manifest, dict):
        raise ImportError("Manifest missing 'manifest' object")

    default_created_at = manifest.get("default_created_at")
    default_effective_at = manifest.get("default_effective_at")
    if not default_created_at or not default_effective_at:
        raise ImportError("Manifest requires default_created_at and default_effective_at")

    entries_raw = raw.get("artifacts")
    if not isinstance(entries_raw, list) or not entries_raw:
        raise ImportError("Manifest requires non-empty 'artifacts' list")

    entries: List[ManifestEntry] = []
    for entry in entries_raw:
        if not isinstance(entry, dict):
            raise ImportError("Manifest artifacts must be objects")
        entry_path = entry.get("path")
        artifact_id = entry.get("artifact_id")
        kind = entry.get("kind")
        domain = entry.get("domain")
        status = entry.get("status")
        checksum = entry.get("checksum")
        created_at = entry.get("created_at") or default_created_at
        effective_at = entry.get("effective_at") or default_effective_at

        missing = [
            field
            for field, value in {
                "path": entry_path,
                "artifact_id": artifact_id,
                "kind": kind,
                "domain": domain,
                "status": status,
                "checksum": checksum,
            }.items()
            if not value
        ]
        if missing:
            raise ImportError(f"Manifest entry missing fields: {', '.join(missing)}")

        if kind not in KIND_VALUES:
            raise ImportError(f"Unsupported kind '{kind}' in manifest for {entry_path}")
        if domain not in DOMAIN_VALUES:
            raise ImportError(f"Unsupported domain '{domain}' in manifest for {entry_path}")
        if status not in STATUS_VALUES:
            raise ImportError(f"Unsupported status '{status}' in manifest for {entry_path}")

        entries.append(
            ManifestEntry(
                path=str(entry_path),
                artifact_id=str(artifact_id),
                kind=str(kind),
                domain=str(domain),
                status=str(status),
                checksum=str(checksum),
                created_at=str(created_at),
                effective_at=str(effective_at),
            )
        )

    return manifest, entries


def parse_filename(path: Path) -> Tuple[str, str, str]:
    match = VERSION_PATTERN.match(path.name)
    if not match:
        raise ImportError(f"Filename must include version suffix: {path.name}")
    artifact_id = match.group("artifact_id")
    version = match.group("version")
    extension = f".{match.group('ext')}"
    return artifact_id, version, extension


def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_seed_documents(seed_root: Path, entries: Iterable[ManifestEntry]) -> Tuple[List[Dict[str, Any]], List[ImportResult]]:
    documents: List[Dict[str, Any]] = []
    results: List[ImportResult] = []
    seen_keys: set[Tuple[str, str]] = set()

    for entry in entries:
        path = (seed_root / entry.path).resolve()
        if not path.exists():
            raise ImportError(f"Seed file not found: {path}")
        artifact_id_from_name, version, extension = parse_filename(path)
        if artifact_id_from_name != entry.artifact_id:
            raise ImportError(f"Artifact ID mismatch for {path}: {artifact_id_from_name} != {entry.artifact_id}")
        content_type = CONTENT_TYPES.get(extension)
        if not content_type:
            raise ImportError(f"Unsupported content type for {path}")

        content = path.read_text(encoding="utf-8")
        checksum = compute_checksum(content)
        if checksum != entry.checksum:
            raise ImportError(f"Checksum mismatch for {path}")

        key = (entry.artifact_id, version)
        if key in seen_keys:
            raise ImportError(f"Duplicate artifact_id+version in manifest: {key[0]} {key[1]}")
        seen_keys.add(key)

        document = {
            "artifact_id": entry.artifact_id,
            "kind": entry.kind,
            "domain": entry.domain,
            "version": version,
            "status": entry.status,
            "content_type": content_type,
            "content": content,
            "checksum": checksum,
            "metadata": {
                "tags": ["seed-import"],
                "notes": "LIB-003 seed import",
            },
            "links": {
                "seed_path": entry.path,
            },
            "source": "seed-import",
            "created_at": entry.created_at,
            "effective_at": entry.effective_at,
        }
        documents.append(document)
        results.append(
            ImportResult(
                artifact_id=entry.artifact_id,
                version=version,
                kind=entry.kind,
                domain=entry.domain,
                status=entry.status,
                source_path=entry.path,
                checksum=checksum,
            )
        )

    documents.sort(key=lambda doc: (doc["artifact_id"], doc["version"]))
    results.sort(key=lambda doc: (doc.artifact_id, doc.version))
    return documents, results


def ensure_indexes(artifacts: Collection, events: Collection) -> None:
    artifacts.create_index(
        [("artifact_id", ASCENDING), ("version", ASCENDING)],
        unique=True,
        partialFilterExpression={
            "artifact_id": {"$type": "string"},
            "version": {"$type": "string"},
        },
    )
    artifacts.create_index("artifact_id")
    artifacts.create_index("kind")
    artifacts.create_index("domain")
    artifacts.create_index("status")
    artifacts.create_index("metadata.tags")
    artifacts.create_index([("kind", ASCENDING), ("domain", ASCENDING), ("status", ASCENDING)])
    events.create_index([("artifact_id", ASCENDING), ("version", ASCENDING)])
    events.create_index("timestamp")
    events.create_index("event")


def reset_database(db) -> List[str]:
    dropped: List[str] = []
    for name in db.list_collection_names():
        if name.startswith("system."):
            continue
        db.drop_collection(name)
        dropped.append(name)
    return dropped


def write_report(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset Mongo and seed Librarian artifacts for LIB-003")
    parser.add_argument(
        "--mongo-uri",
        default=os.environ.get("LIBRARIAN_MONGO_URI", "mongodb://localhost:27017"),
        help="MongoDB URI (default: %(default)s)",
    )
    parser.add_argument(
        "--db",
        default=os.environ.get("LIBRARIAN_MONGO_DB", "librarian"),
        help="Mongo database name (default: %(default)s)",
    )
    parser.add_argument(
        "--artifacts-collection",
        default=os.environ.get(
            "LIBRARIAN_MONGO_ARTIFACTS_COLLECTION",
            os.environ.get("LIBRARIAN_MONGO_COLLECTION", "artifacts"),
        ),
        help="Artifacts collection name (default: %(default)s)",
    )
    parser.add_argument(
        "--events-collection",
        default=os.environ.get("LIBRARIAN_MONGO_EVENTS_COLLECTION", "artifact_events"),
        help="Artifact events collection name (default: %(default)s)",
    )
    parser.add_argument(
        "--seed-root",
        default=".",
        help="Repository root containing the seed directory (default: %(default)s)",
    )
    parser.add_argument(
        "--manifest",
        default="library_seed/seed-manifest.v0.yaml",
        help="Seed manifest path (default: %(default)s)",
    )
    parser.add_argument(
        "--report-out",
        default="library/_reports/lib-003-migration.v0.yaml",
        help="Write migration report to this path (default: %(default)s)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not modify Mongo")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed_root = Path(args.seed_root).resolve()
    manifest_path = seed_root / args.manifest

    manifest, entries = parse_manifest(manifest_path)
    documents, results = load_seed_documents(seed_root, entries)

    if args.dry_run:
        print(f"[dry-run] {len(documents)} artifacts validated from {manifest_path}")
        return

    client = MongoClient(args.mongo_uri)
    db = client[args.db]

    print(f"[reset] Dropping collections in database '{args.db}'")
    dropped = reset_database(db)
    for name in dropped:
        print(f"[reset] Dropped collection: {name}")

    artifacts = db[args.artifacts_collection]
    events = db[args.events_collection]

    try:
        ensure_indexes(artifacts, events)
    except PyMongoError as exc:
        raise SystemExit(f"Index creation failed: {exc}") from exc

    try:
        artifacts.insert_many(documents, ordered=True)
    except PyMongoError as exc:
        raise SystemExit(f"Artifact insert failed: {exc}") from exc

    event_timestamp = manifest.get("generated_at") or now_timestamp()
    event_docs = [
        {
            "event": "artifact.imported",
            "timestamp": event_timestamp,
            "actor": "lib-003-migration",
            "artifact_id": result.artifact_id,
            "version": result.version,
            "reason": "LIB-003 seed import",
        }
        for result in results
    ]

    try:
        events.insert_many(event_docs, ordered=True)
    except PyMongoError as exc:
        raise SystemExit(f"Artifact event insert failed: {exc}") from exc

    report_payload = {
        "report": {
            "name": "lib-003-migration",
            "version": "v0",
            "generated_at": now_timestamp(),
        },
        "reset": {
            "database": args.db,
            "dropped_collections": dropped,
            "justification": "LIB-003 Mongo reset before canonical seed import",
        },
        "seed_manifest": {
            "path": args.manifest,
            "artifact_count": len(results),
        },
        "artifacts": [
            {
                "artifact_id": result.artifact_id,
                "version": result.version,
                "kind": result.kind,
                "domain": result.domain,
                "status": result.status,
                "checksum": result.checksum,
                "source_path": result.source_path,
            }
            for result in results
        ],
    }

    write_report(seed_root / args.report_out, report_payload)
    print(f"[report] Wrote migration report to {args.report_out}")


if __name__ == "__main__":
    try:
        main()
    except ImportError as exc:
        print(f"[error] {exc}")
        sys.exit(1)
