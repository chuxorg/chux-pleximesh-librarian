#!/usr/bin/env python3
"""Minimal REST server for PlexiMesh Librarian artifact intake."""

from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, NamedTuple, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

ARTIFACT_TYPES = {"prompt", "result", "governance", "decision", "reference"}
ROLE_DIRECTORIES = ["guardian", "pm", "engineer", "qa", "documentation", "codex"]
CONTENT_FORMATS = {"markdown", "text", "json"}
FORMAT_EXTENSIONS = {"markdown": ".md", "text": ".txt", "json": ".json"}
URI_SCHEME = "central-librarian://"
SAFE_SEGMENT_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")
PROMPT_ID_NAMESPACE = uuid.UUID("4b2144e3-7b01-4b2f-92ad-7d949015135a")

# TODO: replace HTTP transport with AWACS/event ingestion in a future phase.
# TODO: add stronger payload validation once upstream schemas are finalized.
# TODO: emit structured events rather than relying solely on stdout logging.


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_safe_segment(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    trimmed = value.strip()
    if not trimmed:
        raise ValueError(f"{field_name} must not be empty")
    if SAFE_SEGMENT_PATTERN.search(trimmed):
        raise ValueError(f"{field_name} contains invalid characters; only letters, numbers, ., _, - are allowed")
    if trimmed in {".", ".."}:
        raise ValueError(f"{field_name} cannot be '.' or '..'")
    return trimmed


def canonical_prefix_from_segments(segments: List[str]) -> str:
    if not segments:
        return URI_SCHEME
    return f"{URI_SCHEME}{'/'.join(segments)}/"


def default_logical_path(artifact_type: str, agent_role: str) -> List[str]:
    if artifact_type == "prompt":
        return ["prompts", agent_role]
    if artifact_type == "result":
        return ["results", agent_role]
    if artifact_type == "governance":
        return ["governance"]
    if artifact_type == "decision":
        return ["decisions"]
    if artifact_type == "reference":
        return ["references"]
    raise ValueError(f"Unsupported artifact_type: {artifact_type}")


def _logical_segments_from_value(value: Any, field_name: str) -> List[str]:
    if isinstance(value, str):
        stripped = value.strip().strip("/")
        if not stripped:
            raise ValueError(f"{field_name} must include at least one segment when provided")
        raw_segments = [segment for segment in stripped.split("/") if segment]
    elif isinstance(value, list):
        raw_segments = value
    else:
        raise ValueError(f"{field_name} must be a string or list of strings")
    return [ensure_safe_segment(segment, f"{field_name} segment") for segment in raw_segments]


def _segments_from_prefix(prefix: str) -> List[str]:
    if not prefix.startswith(URI_SCHEME):
        raise ValueError("canonical_prefix must start with 'central-librarian://'")
    if not prefix.endswith("/"):
        raise ValueError("canonical_prefix must end with '/'")
    body = prefix[len(URI_SCHEME) : -1]
    if not body:
        return []
    raw_segments = [segment for segment in body.split("/") if segment]
    return [ensure_safe_segment(segment, "canonical_prefix segment") for segment in raw_segments]


def derive_logical_path(payload: Dict[str, Any], artifact_type: str, agent_role: str) -> Tuple[List[str], str]:
    prefix_value = payload.get("canonical_prefix")
    logical_value = payload.get("logical_path")
    if prefix_value:
        segments = _segments_from_prefix(prefix_value)
        return segments, prefix_value
    if logical_value:
        segments = _logical_segments_from_value(logical_value, "logical_path")
    else:
        segments = default_logical_path(artifact_type, agent_role)
    prefix = canonical_prefix_from_segments(segments)
    return segments, prefix


def enforce_execution_id(value: Any) -> str:
    execution_id = ensure_safe_segment(value, "execution.execution_id")
    return execution_id


def build_filename(artifact_type: str, execution_id: str, content_format: str) -> str:
    extension = FORMAT_EXTENSIONS[content_format]
    return f"{execution_id}{extension}"


def deterministic_prompt_id(execution_id: str) -> str:
    return str(uuid.uuid5(PROMPT_ID_NAMESPACE, execution_id))


def normalize_string_list(value: Any, field_name: str) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        cleaned: List[str] = []
        for item in value:
            if item is None:
                continue
            stringified = str(item).strip()
            if stringified:
                cleaned.append(stringified)
        return cleaned
    if isinstance(value, str):
        trimmed = value.strip()
        return [trimmed] if trimmed else []
    raise ValueError(f"{field_name} must be a string or list of strings")


@dataclass
class NormalizedArtifact:
    artifact_type: str
    agent_role: str
    agent_id: Optional[str]
    execution_id: str
    parent_execution_id: Optional[str]
    root_execution_id: str
    prompt_id: Optional[str]
    correlation_prompt_id: Optional[str]
    source: Dict[str, Optional[str]]
    content_format: str
    content_body: str
    metadata: Dict[str, Any]
    timestamp: str
    execution_phase: Optional[str]
    references: List[str]
    status: str
    logical_path: List[str]
    canonical_prefix: str
    canonical_path: str
    filename: str
    canonical_uri: str
    content_sha256: str
    payload_digest: str

    def header(self) -> Dict[str, Any]:
        header = {
            "artifact_type": self.artifact_type,
            "timestamp": self.timestamp,
            "agent": {"role": self.agent_role, "id": self.agent_id},
            "execution": {
                "execution_id": self.execution_id,
                "parent_execution_id": self.parent_execution_id,
                "phase": self.execution_phase,
            },
            "correlation": {
                "root_execution_id": self.root_execution_id,
                "prompt_id": self.prompt_id or self.correlation_prompt_id,
            },
            "source": self.source,
            "content": {"format": self.content_format},
            "metadata": self.metadata,
            "canonical": {
                "uri": self.canonical_uri,
                "path": self.canonical_path,
                "prefix": self.canonical_prefix,
            },
        }
        return header


class PersistenceError(RuntimeError):
    """Raised when artifact storage or retrieval fails."""


class ArtifactConflictError(PersistenceError):
    """Raised when attempting to overwrite an existing artifact with different content."""

    def __init__(self, uri: str, message: str, existing_digest: Optional[str], incoming_digest: Optional[str]) -> None:
        super().__init__(message)
        self.uri = uri
        self.existing_digest = existing_digest
        self.incoming_digest = incoming_digest


class StoreResult(NamedTuple):
    document: Dict[str, Any]
    created: bool
    unchanged: bool


class MongoArtifactStore:
    """Mongo-backed persistence adapter for Librarian artifacts."""

    def __init__(self) -> None:
        uri = os.environ.get("LIBRARIAN_MONGO_URI", "mongodb://mongo:27017")
        db_name = os.environ.get("LIBRARIAN_MONGO_DB", "librarian")
        collection_name = os.environ.get("LIBRARIAN_MONGO_COLLECTION", "artifacts")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        collection = client[db_name][collection_name]
        collection.create_index("uri", unique=True)
        collection.create_index([("path", ASCENDING)])
        self._collection: Collection = collection

    def put(self, artifact: NormalizedArtifact) -> StoreResult:
        document = self._document_from_artifact(artifact)
        try:
            existing = self._collection.find_one({"uri": artifact.canonical_uri})
        except PyMongoError as exc:  # pragma: no cover - network failure
            raise PersistenceError(f"Mongo read failure before write: {exc}") from exc

        if existing:
            existing = {key: value for key, value in existing.items() if key != "_id"}
            if existing.get("digest") == document["digest"]:
                return StoreResult(document=existing, created=False, unchanged=True)
            raise ArtifactConflictError(
                artifact.canonical_uri,
                f"Artifact already exists at {artifact.canonical_uri} with different content",
                existing_digest=existing.get("digest"),
                incoming_digest=document["digest"],
            )

        try:
            self._collection.insert_one(document)
        except PyMongoError as exc:  # pragma: no cover
            raise PersistenceError(f"Mongo persistence failure: {exc}") from exc

        return StoreResult(document=document, created=True, unchanged=False)

    def _document_from_artifact(self, artifact: NormalizedArtifact) -> Dict[str, Any]:
        supersedes = artifact.metadata.get("supersedes") or []
        deprecated_by = artifact.metadata.get("deprecated_by") or []
        canonical_flag = bool(artifact.metadata.get("canonical", True))
        return {
            "uri": artifact.canonical_uri,
            "path": list(artifact.logical_path),
            "relative_path": artifact.canonical_path,
            "canonical_prefix": artifact.canonical_prefix,
            "filename": artifact.filename,
            "artifact_type": artifact.artifact_type,
            "owner_agent": artifact.agent_role,
            "execution_id": artifact.execution_id,
            "parent_execution_id": artifact.parent_execution_id,
            "root_execution_id": artifact.root_execution_id,
            "prompt_id": artifact.prompt_id,
            "correlation_prompt_id": artifact.correlation_prompt_id,
            "created_by": artifact.agent_id or artifact.agent_role,
            "created_at": artifact.timestamp,
            "updated_at": artifact.timestamp,
            "status": artifact.status,
            "is_canonical": canonical_flag,
            "supersedes": supersedes,
            "deprecated_by": deprecated_by,
            "references": artifact.references,
            "metadata": artifact.metadata,
            "content": artifact.content_body,
            "content_format": artifact.content_format,
            "content_sha256": artifact.content_sha256,
            "header": artifact.header(),
            "digest": artifact.payload_digest,
        }

    def get(self, uri: str) -> Optional[Dict[str, Any]]:
        try:
            document = self._collection.find_one({"uri": uri}, {"_id": 0})
        except PyMongoError as exc:  # pragma: no cover
            raise PersistenceError(f"Mongo read failure: {exc}") from exc
        return document

    def exists(self, uri: str) -> bool:
        try:
            return self._collection.count_documents({"uri": uri}, limit=1) > 0
        except PyMongoError as exc:  # pragma: no cover
            raise PersistenceError(f"Mongo read failure: {exc}") from exc

    def list(self, prefix: Optional[str]) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if prefix:
            query["uri"] = {"$regex": f"^{re.escape(prefix)}"}

        projection = {
            "_id": 0,
            "uri": 1,
            "relative_path": 1,
            "canonical_prefix": 1,
            "filename": 1,
            "path": 1,
            "artifact_type": 1,
            "owner_agent": 1,
            "status": 1,
            "is_canonical": 1,
            "created_at": 1,
            "updated_at": 1,
        }
        try:
            cursor = self._collection.find(query, projection).sort("created_at", ASCENDING)
            return list(cursor)
        except PyMongoError as exc:  # pragma: no cover
            raise PersistenceError(f"Mongo list failure: {exc}") from exc


ARTIFACT_STORE = MongoArtifactStore()


def normalize_payload(payload: Dict[str, Any]) -> NormalizedArtifact:
    if not isinstance(payload, dict):  # pragma: no cover
        raise ValueError("Payload must be an object")

    artifact_type = payload.get("artifact_type")
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError("Unsupported artifact_type")

    agent = payload.get("agent") or {}
    agent_role = agent.get("role")
    agent_id = agent.get("id")
    if agent_role not in ROLE_DIRECTORIES:
        raise ValueError("Unsupported or missing agent role")
    if artifact_type == "governance" and agent_role != "guardian":
        raise ValueError("Governance artifacts must come from guardian agents")

    execution = payload.get("execution") or {}
    execution_id = execution.get("execution_id")
    parent_execution_id = execution.get("parent_execution_id")
    execution_phase = execution.get("phase")
    if not execution_id:
        raise ValueError("execution.execution_id is required")
    execution_id = enforce_execution_id(execution_id)
    if parent_execution_id is not None:
        parent_execution_id = ensure_safe_segment(parent_execution_id, "execution.parent_execution_id")

    correlation = payload.get("correlation") or {}
    root_execution_id = correlation.get("root_execution_id")
    if not root_execution_id:
        raise ValueError("correlation.root_execution_id is required")
    root_execution_id = ensure_safe_segment(root_execution_id, "correlation.root_execution_id")

    correlation_prompt_id = correlation.get("prompt_id")

    prompt_id: Optional[str] = None
    if artifact_type == "prompt":
        prompt_id = deterministic_prompt_id(execution_id)
    elif artifact_type == "result":
        if not correlation_prompt_id:
            raise ValueError("Result artifacts require correlation.prompt_id")
        correlation_prompt_id = ensure_safe_segment(correlation_prompt_id, "correlation.prompt_id")
    else:
        if correlation_prompt_id is not None:
            correlation_prompt_id = ensure_safe_segment(correlation_prompt_id, "correlation.prompt_id")
        prompt_id = correlation_prompt_id

    if artifact_type == "prompt" and correlation_prompt_id:
        raise ValueError("Prompt artifacts must not provide a prompt_id; it is auto-generated")

    content = payload.get("content") or {}
    content_format = content.get("format")
    content_body = content.get("body")
    if content_format not in CONTENT_FORMATS:
        raise ValueError("Unsupported content.format")
    if not isinstance(content_body, str):
        raise ValueError("content.body must be a string")

    source = payload.get("source") or {}
    cleaned_source = {
        "repo": source.get("repo"),
        "branch": source.get("branch"),
        "commit": source.get("commit"),
    }

    metadata = payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be an object if provided")
    tags = metadata.get("tags")
    if tags is not None and not isinstance(tags, list):
        raise ValueError("metadata.tags must be a list of strings")
    if isinstance(tags, list):
        tags = [str(tag) for tag in tags]
    status = payload.get("status") or metadata.get("status") or "canonical"
    allowed_status = {"draft", "canonical", "superseded", "blocked"}
    if status not in allowed_status:
        raise ValueError("status must be one of draft | canonical | superseded | blocked")
    references_list = normalize_string_list(payload.get("references"), "references")
    supersedes = normalize_string_list(metadata.get("supersedes"), "metadata.supersedes")
    deprecated_by = normalize_string_list(metadata.get("deprecated_by"), "metadata.deprecated_by")
    canonical_flag_raw = metadata.get("canonical")
    if canonical_flag_raw is None:
        canonical_flag = status == "canonical"
    elif isinstance(canonical_flag_raw, bool):
        canonical_flag = canonical_flag_raw
    elif isinstance(canonical_flag_raw, str):
        canonical_flag = canonical_flag_raw.strip().lower() in {"1", "true", "yes"}
    else:
        raise ValueError("metadata.canonical must be a boolean or string value")
    metadata_normalized = {
        "client_timestamp": metadata.get("timestamp"),
        "tags": tags,
        "notes": metadata.get("notes"),
        "agent_id": agent_id,
        "status": status,
        "supersedes": supersedes,
        "deprecated_by": deprecated_by,
        "canonical": canonical_flag,
    }

    logical_path, canonical_prefix = derive_logical_path(payload, artifact_type, agent_role)
    filename = build_filename(artifact_type, execution_id, content_format)
    canonical_path = "/".join([*logical_path, filename]) if logical_path else filename
    canonical_uri = f"{URI_SCHEME}{canonical_path}"

    timestamp = now_timestamp()
    content_sha256 = hashlib.sha256(content_body.encode("utf-8")).hexdigest()
    digest_source = {
        "artifact_type": artifact_type,
        "agent_role": agent_role,
        "agent_id": agent_id,
        "execution_id": execution_id,
        "parent_execution_id": parent_execution_id,
        "root_execution_id": root_execution_id,
        "prompt_id": prompt_id,
        "correlation_prompt_id": correlation_prompt_id,
        "source": cleaned_source,
        "content_format": content_format,
        "content_body": content_body,
        "metadata": metadata_normalized,
        "references": references_list,
        "status": status,
        "logical_path": logical_path,
        "canonical_path": canonical_path,
    }
    payload_digest = hashlib.sha256(json.dumps(digest_source, sort_keys=True).encode("utf-8")).hexdigest()
    return NormalizedArtifact(
        artifact_type=artifact_type,
        agent_role=agent_role,
        agent_id=agent_id,
        execution_id=execution_id,
        parent_execution_id=parent_execution_id,
        root_execution_id=root_execution_id,
        prompt_id=prompt_id,
        correlation_prompt_id=correlation_prompt_id,
        source=cleaned_source,
        content_format=content_format,
        content_body=content_body,
        metadata=metadata_normalized,
        timestamp=timestamp,
        execution_phase=execution_phase,
        references=references_list,
        status=status,
        logical_path=logical_path,
        canonical_prefix=canonical_prefix,
        canonical_path=canonical_path,
        filename=filename,
        canonical_uri=canonical_uri,
        content_sha256=content_sha256,
        payload_digest=payload_digest,
    )


class ArtifactRequestHandler(BaseHTTPRequestHandler):
    server_version = "LibrarianArtifactAPI/0.0"

    def do_POST(self) -> None:  # noqa: N802
        self._handle_artifact_write()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if parsed.path == "/artifacts":
            uri = self._single_param(params, "uri")
            if not uri:
                self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "uri query parameter is required"})
                return
            try:
                document = ARTIFACT_STORE.get(uri)
            except PersistenceError as exc:
                self.log_error("Failed to fetch artifact: %s", exc)
                self.respond_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": "Failed to fetch artifact"},
                )
                return
            if document is None:
                self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Artifact not found"})
                return
            self.respond_json(HTTPStatus.OK, document)
            return

        if parsed.path == "/artifacts/exists":
            uri = self._single_param(params, "uri")
            if not uri:
                self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "uri query parameter is required"})
                return
            try:
                exists = ARTIFACT_STORE.exists(uri)
            except PersistenceError as exc:
                self.log_error("Failed to check existence: %s", exc)
                self.respond_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": "Failed to check existence"},
                )
                return
            self.respond_json(HTTPStatus.OK, {"uri": uri, "exists": exists})
            return

        if parsed.path == "/artifacts/list":
            prefix = self._single_param(params, "prefix") or ""
            try:
                artifacts = ARTIFACT_STORE.list(prefix)
            except PersistenceError as exc:
                self.log_error("Failed to list artifacts: %s", exc)
                self.respond_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": "Failed to list artifacts"},
                )
                return
            self.respond_json(
                HTTPStatus.OK,
                {"prefix": prefix, "artifacts": artifacts},
            )
            return

        self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Unknown path"})

    def do_PUT(self) -> None:  # noqa: N802
        self._handle_artifact_write()

    def do_DELETE(self) -> None:  # noqa: N802
        self.respond_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Deletes are not supported"})

    def respond_json(self, status: HTTPStatus, body: Dict[str, Any]) -> None:
        encoded = json.dumps(body).encode("utf-8")
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

    def _handle_artifact_write(self) -> None:
        if self.path != "/artifacts":
            self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Unknown path"})
            return

        payload = self._parse_json_body()
        if payload is None:
            return

        try:
            artifact = normalize_payload(payload)
        except ValueError as exc:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        try:
            result = ARTIFACT_STORE.put(artifact)
        except ArtifactConflictError as exc:
            self.respond_json(
                HTTPStatus.CONFLICT,
                {
                    "error": "Artifact already exists with different content",
                    "uri": exc.uri,
                    "existing_digest": exc.existing_digest,
                    "incoming_digest": exc.incoming_digest,
                },
            )
            return
        except PersistenceError as exc:
            self.log_error("Failed to store artifact: %s", exc)
            self.respond_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Failed to store artifact"},
            )
            return

        status = HTTPStatus.CREATED if result.created else HTTPStatus.OK
        body = self._format_store_response(result)
        self.respond_json(status, body)

    def _parse_json_body(self) -> Optional[Dict[str, Any]]:
        length_header = self.headers.get("Content-Length")
        if length_header is None:
            self.respond_json(HTTPStatus.LENGTH_REQUIRED, {"error": "Missing Content-Length"})
            return None
        try:
            length = int(length_header)
        except ValueError:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid Content-Length"})
            return None
        raw_body = self.rfile.read(length)
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Body must be valid JSON"})
            return None
        return payload

    def _format_store_response(self, result: StoreResult) -> Dict[str, Any]:
        document = result.document
        if result.unchanged:
            response_status = "unchanged"
        else:
            response_status = "stored"
        return {
            "status": response_status,
            "uri": document.get("uri"),
            "path": document.get("relative_path"),
            "canonical_prefix": document.get("canonical_prefix"),
            "artifact_type": document.get("artifact_type"),
            "agent_role": document.get("owner_agent"),
            "execution_id": document.get("execution_id"),
            "prompt_id": document.get("prompt_id") or document.get("correlation_prompt_id"),
            "root_execution_id": document.get("root_execution_id"),
            "timestamp": document.get("created_at"),
            "content_sha256": document.get("content_sha256"),
            "is_canonical": document.get("is_canonical"),
        }


def run_server() -> None:
    port = int(os.environ.get("LIBRARIAN_PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), ArtifactRequestHandler)
    print(f"Artifact intake server listening on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down intake server")
    finally:
        server.server_close()


def main() -> None:
    run_server()


if __name__ == "__main__":
    main()
