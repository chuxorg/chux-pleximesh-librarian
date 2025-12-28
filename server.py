#!/usr/bin/env python3
"""Minimal REST server for PlexiMesh Librarian artifact intake."""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_ROOT = Path(os.environ.get("LIBRARIAN_ARTIFACT_ROOT", BASE_DIR))
ARTIFACT_TYPES = {"prompt", "result", "governance", "decision", "reference"}
ROLE_DIRECTORIES = ["guardian", "pm", "engineer", "qa", "documentation", "codex"]
CONTENT_FORMATS = {"markdown", "text", "json"}
TYPE_DIRECTORIES = {
    "prompt": ARTIFACT_ROOT / "prompts",
    "result": ARTIFACT_ROOT / "results",
    "governance": ARTIFACT_ROOT / "governance",
    "decision": ARTIFACT_ROOT / "decisions",
    "reference": ARTIFACT_ROOT / "references",
}

# TODO: replace HTTP transport with AWACS/event ingestion in a future phase.
# TODO: add stronger payload validation once upstream schemas are finalized.
# TODO: emit structured events rather than relying solely on stdout logging.


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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

    def storage_directory(self) -> Path:
        base = TYPE_DIRECTORIES[self.artifact_type]
        if self.artifact_type in {"prompt", "result"}:
            return base / self.agent_role
        return base

    def filename(self) -> str:
        sanitized_timestamp = self.timestamp.replace(":", "-")
        components = [
            sanitized_timestamp,
            self.artifact_type,
            self.execution_id,
        ]
        prompt_fragment = self.prompt_id or self.correlation_prompt_id
        if prompt_fragment:
            components.append(prompt_fragment)
        return "_".join(components) + ".md"

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
        }
        return header

    def canonical_relative_path(self) -> Path:
        target = self.storage_directory() / self.filename()
        try:
            return target.relative_to(ARTIFACT_ROOT)
        except ValueError:
            return target


class PersistenceError(RuntimeError):
    """Raised when artifact storage or retrieval fails."""


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

    def put(self, artifact: NormalizedArtifact) -> Dict[str, Any]:
        relative_path = artifact.canonical_relative_path()
        uri = f"central-librarian://{relative_path.as_posix()}"
        document = {
            "uri": uri,
            "path": list(relative_path.parent.parts),
            "filename": relative_path.name,
            "artifact_type": artifact.artifact_type,
            "owner_agent": artifact.agent_role,
            "created_by": artifact.agent_id or artifact.agent_role,
            "created_at": artifact.timestamp,
            "updated_at": artifact.timestamp,
            "status": artifact.status,
            "references": artifact.references,
            "metadata": artifact.metadata,
            "content": artifact.content_body,
            "content_format": artifact.content_format,
            "header": artifact.header(),
        }
        try:
            self._collection.replace_one({"uri": uri}, document, upsert=True)
        except PyMongoError as exc:  # pragma: no cover - network failure
            raise PersistenceError(f"Mongo persistence failure: {exc}") from exc

        return {
            "uri": uri,
            "path": relative_path.as_posix(),
            "artifact_type": artifact.artifact_type,
            "agent_role": artifact.agent_role,
            "execution_id": artifact.execution_id,
            "prompt_id": artifact.prompt_id or artifact.correlation_prompt_id,
            "root_execution_id": artifact.root_execution_id,
            "timestamp": artifact.timestamp,
            "status": artifact.status,
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
            "filename": 1,
            "path": 1,
            "artifact_type": 1,
            "owner_agent": 1,
            "status": 1,
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

    correlation = payload.get("correlation") or {}
    root_execution_id = correlation.get("root_execution_id")
    if not root_execution_id:
        raise ValueError("correlation.root_execution_id is required")

    correlation_prompt_id = correlation.get("prompt_id")

    prompt_id: Optional[str] = None
    if artifact_type == "prompt":
        prompt_id = str(uuid.uuid4())
    elif artifact_type == "result":
        if not correlation_prompt_id:
            raise ValueError("Result artifacts require correlation.prompt_id")
    else:
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
    tags = metadata.get("tags")
    if tags is not None and not isinstance(tags, list):
        raise ValueError("metadata.tags must be a list of strings")
    if isinstance(tags, list):
        tags = [str(tag) for tag in tags]
    status = payload.get("status") or metadata.get("status") or "canonical"
    allowed_status = {"draft", "canonical", "superseded", "blocked"}
    if status not in allowed_status:
        raise ValueError("status must be one of draft | canonical | superseded | blocked")
    references = payload.get("references") or []
    if references and not isinstance(references, list):
        raise ValueError("references must be a list of strings")
    references_list = [str(ref) for ref in references]
    metadata_normalized = {
        "client_timestamp": metadata.get("timestamp"),
        "tags": tags,
        "notes": metadata.get("notes"),
        "agent_id": agent_id,
        "status": status,
    }

    timestamp = now_timestamp()
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
    )


class ArtifactRequestHandler(BaseHTTPRequestHandler):
    server_version = "LibrarianArtifactAPI/0.0"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/artifacts":
            self.respond_json(HTTPStatus.NOT_FOUND, {"error": "Unknown path"})
            return

        length_header = self.headers.get("Content-Length")
        if length_header is None:
            self.respond_json(HTTPStatus.LENGTH_REQUIRED, {"error": "Missing Content-Length"})
            return

        try:
            length = int(length_header)
        except ValueError:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid Content-Length"})
            return

        raw_body = self.rfile.read(length)
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": "Body must be valid JSON"})
            return

        try:
            artifact = normalize_payload(payload)
        except ValueError as exc:
            self.respond_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        try:
            record = ARTIFACT_STORE.put(artifact)
        except PersistenceError as exc:
            self.log_error("Failed to store artifact: %s", exc)
            self.respond_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Failed to store artifact"},
            )
            return

        body = {
            "status": "stored",
            "uri": record["uri"],
            "path": record["path"],
            "artifact_type": artifact.artifact_type,
            "agent_role": artifact.agent_role,
            "execution_id": artifact.execution_id,
            "prompt_id": artifact.prompt_id or artifact.correlation_prompt_id,
            "root_execution_id": artifact.root_execution_id,
            "timestamp": artifact.timestamp,
        }
        self.respond_json(HTTPStatus.CREATED, body)

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
        self.respond_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Updates are not supported"})

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
