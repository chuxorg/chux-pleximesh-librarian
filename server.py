#!/usr/bin/env python3
"""Read-only REST server for canonical Librarian artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, unquote, urlparse

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

KIND_VALUES = {"task", "policy", "phase", "law", "report", "schema"}
DOMAIN_VALUES = {"engineering", "governance", "librarian", "ui", "runtime"}
STATUS_VALUES = {"planned", "active", "deprecated", "archived"}
CONTENT_TYPES = {"text/markdown", "application/yaml", "application/json"}
SOURCE_VALUES = {"seed-import", "api-write", "migration"}
VERSION_PATTERN = re.compile(r"^v\d+$")

REQUIRED_FIELDS = {
    "artifact_id",
    "kind",
    "domain",
    "version",
    "status",
    "content_type",
    "content",
    "checksum",
    "source",
    "created_at",
    "effective_at",
}


class PersistenceError(RuntimeError):
    """Raised when Mongo operations fail."""


class DataIntegrityError(RuntimeError):
    """Raised when stored artifacts violate the canonical schema."""


def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def parse_version(value: str) -> int:
    match = VERSION_PATTERN.match(value)
    if not match:
        raise DataIntegrityError(f"Invalid version format: {value}")
    return int(value[1:])


def _require_string(document: Dict[str, Any], field: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DataIntegrityError(f"Field '{field}' must be a non-empty string")
    return value


def _optional_mapping(document: Dict[str, Any], field: str) -> Optional[Dict[str, Any]]:
    if field not in document or document[field] is None:
        return None
    value = document[field]
    if not isinstance(value, dict):
        raise DataIntegrityError(f"Field '{field}' must be an object if provided")
    return value


def validate_document(document: Dict[str, Any]) -> Dict[str, Any]:
    missing = sorted(field for field in REQUIRED_FIELDS if field not in document)
    if missing:
        raise DataIntegrityError(f"Missing required fields: {', '.join(missing)}")

    artifact_id = _require_string(document, "artifact_id")
    kind = _require_string(document, "kind")
    domain = _require_string(document, "domain")
    version = _require_string(document, "version")
    status = _require_string(document, "status")
    content_type = _require_string(document, "content_type")
    content_value = document.get("content")
    if not isinstance(content_value, str):
        raise DataIntegrityError("Field 'content' must be a string")
    content = content_value
    checksum = _require_string(document, "checksum")
    source = _require_string(document, "source")
    _require_string(document, "created_at")
    _require_string(document, "effective_at")

    if kind not in KIND_VALUES:
        raise DataIntegrityError(f"Unsupported kind: {kind}")
    if domain not in DOMAIN_VALUES:
        raise DataIntegrityError(f"Unsupported domain: {domain}")
    if status not in STATUS_VALUES:
        raise DataIntegrityError(f"Unsupported status: {status}")
    if content_type not in CONTENT_TYPES:
        raise DataIntegrityError(f"Unsupported content_type: {content_type}")
    if source not in SOURCE_VALUES:
        raise DataIntegrityError(f"Unsupported source: {source}")

    parse_version(version)

    expected_checksum = compute_checksum(content)
    if checksum != expected_checksum:
        raise DataIntegrityError(
            f"Checksum mismatch for artifact '{artifact_id}' (expected {expected_checksum})"
        )

    _optional_mapping(document, "metadata")
    _optional_mapping(document, "links")

    return document


class CanonicalArtifactStore:
    """Mongo-backed read-only store for canonical artifacts."""

    def __init__(self) -> None:
        uri = os.environ.get("LIBRARIAN_MONGO_URI", "mongodb://mongo:27017")
        db_name = os.environ.get("LIBRARIAN_MONGO_DB", "librarian")
        artifacts_collection = os.environ.get(
            "LIBRARIAN_MONGO_ARTIFACTS_COLLECTION",
            os.environ.get("LIBRARIAN_MONGO_COLLECTION", "artifacts"),
        )
        events_collection = os.environ.get("LIBRARIAN_MONGO_EVENTS_COLLECTION", "artifact_events")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        database = client[db_name]
        self._artifacts: Collection = database[artifacts_collection]
        self._events: Collection = database[events_collection]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        try:
            self._artifacts.create_index(
                [("artifact_id", ASCENDING), ("version", ASCENDING)],
                unique=True,
                partialFilterExpression={
                    "artifact_id": {"$type": "string"},
                    "version": {"$type": "string"},
                },
            )
            self._artifacts.create_index("artifact_id")
            self._artifacts.create_index("kind")
            self._artifacts.create_index("domain")
            self._artifacts.create_index("status")
            self._artifacts.create_index("metadata.tags")
            self._artifacts.create_index([("kind", ASCENDING), ("domain", ASCENDING), ("status", ASCENDING)])
            self._events.create_index([("artifact_id", ASCENDING), ("version", ASCENDING)])
            self._events.create_index("timestamp")
            self._events.create_index("event")
        except PyMongoError as exc:
            raise PersistenceError(f"Failed to create indexes: {exc}") from exc

    def get_by_id_version(self, artifact_id: str, version: str, kind: Optional[str]) -> Optional[Dict[str, Any]]:
        query: Dict[str, Any] = {"artifact_id": artifact_id, "version": version}
        if kind:
            query["kind"] = kind
        try:
            document = self._artifacts.find_one(query, {"_id": 0})
        except PyMongoError as exc:
            raise PersistenceError(f"Mongo read failure: {exc}") from exc
        if document is None:
            return None
        return validate_document(document)

    def get_latest_active(self, artifact_id: str, kind: Optional[str]) -> Optional[Dict[str, Any]]:
        query: Dict[str, Any] = {"artifact_id": artifact_id, "status": "active"}
        if kind:
            query["kind"] = kind
        try:
            documents = list(self._artifacts.find(query, {"_id": 0}))
        except PyMongoError as exc:
            raise PersistenceError(f"Mongo read failure: {exc}") from exc
        if not documents:
            return None
        validated = [validate_document(document) for document in documents]
        return max(validated, key=lambda doc: parse_version(doc["version"]))

    def list(
        self,
        *,
        kind: Optional[str],
        domain: Optional[str],
        status: Optional[str],
        tag: Optional[str],
    ) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if kind:
            query["kind"] = kind
        if domain:
            query["domain"] = domain
        if status:
            query["status"] = status
        if tag:
            query["metadata.tags"] = tag
        try:
            documents = list(self._artifacts.find(query, {"_id": 0}))
        except PyMongoError as exc:
            raise PersistenceError(f"Mongo list failure: {exc}") from exc

        validated = [validate_document(document) for document in documents]
        validated.sort(key=lambda doc: (doc["artifact_id"], parse_version(doc["version"])))
        return validated


ARTIFACT_STORE = CanonicalArtifactStore()


class ArtifactRequestHandler(BaseHTTPRequestHandler):
    server_version = "LibrarianReadAPI/0.1"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        segments = [segment for segment in parsed.path.split("/") if segment]

        if segments == ["artifacts"]:
            self._handle_artifact_list(params)
            return

        if len(segments) == 2 and segments[0] == "artifacts":
            artifact_id = unquote(segments[1])
            self._handle_artifact_get(artifact_id, params, kind=None)
            return

        kind_by_path = {"tasks": "task", "policies": "policy", "phases": "phase"}
        if len(segments) == 2 and segments[0] in kind_by_path:
            artifact_id = unquote(segments[1])
            self._handle_artifact_get(artifact_id, params, kind=kind_by_path[segments[0]])
            return

        self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Unknown path"})

    def do_POST(self) -> None:  # noqa: N802
        self.respond_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Write operations are not supported"})

    def do_PUT(self) -> None:  # noqa: N802
        self.respond_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Write operations are not supported"})

    def do_DELETE(self) -> None:  # noqa: N802
        self.respond_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Write operations are not supported"})

    def respond_json(self, status: HTTPStatus, body: Dict[str, Any]) -> None:
        encoded = json.dumps(
            body,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        message = "%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args,
        )
        print(message)

    @staticmethod
    def _single_param(params: Dict[str, List[str]], key: str) -> Optional[str]:
        values = params.get(key)
        if not values:
            return None
        return values[0]

    def _handle_artifact_get(self, artifact_id: str, params: Dict[str, List[str]], kind: Optional[str]) -> None:
        if not artifact_id:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "artifact_id is required"})
            return
        version = self._single_param(params, "version")
        if version is not None:
            if not VERSION_PATTERN.match(version):
                self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "version must match vN"})
                return
            try:
                document = ARTIFACT_STORE.get_by_id_version(artifact_id, version, kind)
            except (PersistenceError, DataIntegrityError) as exc:
                self.log_error("Failed to fetch artifact: %s", exc)
                self.respond_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
                return
            if document is None:
                self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Artifact not found"})
                return
            self.respond_json(HTTPStatus.OK, document)
            return

        try:
            document = ARTIFACT_STORE.get_latest_active(artifact_id, kind)
        except (PersistenceError, DataIntegrityError) as exc:
            self.log_error("Failed to fetch artifact: %s", exc)
            self.respond_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return
        if document is None:
            self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Artifact not found"})
            return
        self.respond_json(HTTPStatus.OK, document)

    def _handle_artifact_list(self, params: Dict[str, List[str]]) -> None:
        kind = self._single_param(params, "kind")
        domain = self._single_param(params, "domain")
        status = self._single_param(params, "status")
        tag = self._single_param(params, "tag")

        if kind and kind not in KIND_VALUES:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid kind filter"})
            return
        if domain and domain not in DOMAIN_VALUES:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid domain filter"})
            return
        if status and status not in STATUS_VALUES:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid status filter"})
            return

        try:
            artifacts = ARTIFACT_STORE.list(kind=kind, domain=domain, status=status, tag=tag)
        except (PersistenceError, DataIntegrityError) as exc:
            self.log_error("Failed to list artifacts: %s", exc)
            self.respond_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        response_body = {
            "filters": {
                "kind": kind,
                "domain": domain,
                "status": status,
                "tag": tag,
            },
            "artifacts": artifacts,
        }
        self.respond_json(HTTPStatus.OK, response_body)


def run_server() -> None:
    port = int(os.environ.get("LIBRARIAN_PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), ArtifactRequestHandler)
    print(f"Librarian read API listening on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down read API")
    finally:
        server.server_close()


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
