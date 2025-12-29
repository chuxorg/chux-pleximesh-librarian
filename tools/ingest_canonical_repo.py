#!/usr/bin/env python3
"""Bootstrap ingestion utility for loading canonical repo artifacts into the Librarian API."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence
from urllib import error, request

ROLE_DIRECTORIES = ["guardian", "pm", "engineer", "qa", "documentation", "codex"]
TYPE_BY_SEGMENT = {
    "prompts": "prompt",
    "results": "result",
    "governance": "governance",
    "decisions": "decision",
    "references": "reference",
}
DEFAULT_ROLE_BY_TYPE = {
    "prompt": "documentation",
    "result": "engineer",
    "governance": "guardian",
    "decision": "guardian",
    "reference": "documentation",
}
FORMAT_BY_SUFFIX = {
    ".md": "markdown",
    ".markdown": "markdown",
    ".txt": "text",
    ".json": "json",
}


@dataclass
class RootMapping:
    local: Path
    canonical_prefix: List[str]


class LibrarianIngestor:
    def __init__(self, api_base: str, repo_root: Path, agent_id: str, dry_run: bool = False) -> None:
        self.api_base = api_base.rstrip("/")
        self.repo_root = repo_root
        self.agent_id = agent_id
        self.dry_run = dry_run
        self.processed = 0
        self.stored = 0
        self.skipped = 0
        self.failed = 0

    def ingest_roots(self, roots: Sequence[RootMapping]) -> None:
        for mapping in roots:
            if not mapping.local.exists():
                print(f"[skip] {mapping.local} does not exist")
                self.skipped += 1
                continue
            for file_path in mapping.local.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.name.startswith("."):
                    continue
                self.process_file(mapping, file_path)

    def process_file(self, mapping: RootMapping, file_path: Path) -> None:
        relative_under_root = file_path.relative_to(mapping.local)
        canonical_segments = mapping.canonical_prefix + list(relative_under_root.parts)
        if not canonical_segments:
            self.skipped += 1
            return
        filename = canonical_segments[-1]
        logical_path = canonical_segments[:-1]
        suffix = file_path.suffix.lower()
        content_format = FORMAT_BY_SUFFIX.get(suffix)
        if not content_format:
            print(f"[skip] Unsupported format for {file_path}")
            self.skipped += 1
            return
        artifact_type = infer_artifact_type(canonical_segments)
        agent_role = infer_agent_role(artifact_type, canonical_segments)
        execution_id = Path(filename).stem
        if not execution_id:
            print(f"[skip] Cannot derive execution_id for {file_path}")
            self.skipped += 1
            return
        logical_segments = [segment for segment in logical_path if segment]
        content_body = file_path.read_text(encoding="utf-8")
        correlation = {
            "root_execution_id": f"import-{execution_id}",
        }
        if artifact_type == "result":
            correlation["prompt_id"] = f"import-prompt-{execution_id}"
        payload = {
            "artifact_type": artifact_type,
            "agent": {"role": agent_role, "id": self.agent_id},
            "execution": {"execution_id": execution_id},
            "correlation": correlation,
            "logical_path": logical_segments,
            "content": {"format": content_format, "body": content_body},
            "metadata": {
                "tags": ["ingested", f"source:{file_path.relative_to(self.repo_root).as_posix()}"],
                "notes": "Imported from canonical repository snapshot",
                "canonical": True,
            },
            "status": "canonical",
        }
        self._send_payload(file_path, payload)

    def _send_payload(self, file_path: Path, payload: Dict[str, object]) -> None:
        self.processed += 1
        if self.dry_run:
            print(f"[dry-run] Would ingest {file_path}")
            return
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url=f"{self.api_base}/artifacts",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req) as response:
                body = json.loads(response.read().decode("utf-8"))
                status = body.get("status")
                uri = body.get("uri")
                print(f"[{status}] {file_path} -> {uri}")
                self.stored += 1
        except error.HTTPError as exc:  # pragma: no cover - CLI script
            details = exc.read().decode("utf-8") if exc.fp else exc.reason
            print(f"[error] {file_path} — HTTP {exc.code}: {details}")
            self.failed += 1
        except error.URLError as exc:  # pragma: no cover - CLI script
            print(f"[error] {file_path} — {exc.reason}")
            self.failed += 1


def infer_artifact_type(segments: Sequence[str]) -> str:
    if not segments:
        return "reference"
    return TYPE_BY_SEGMENT.get(segments[0], "reference")


def infer_agent_role(artifact_type: str, segments: Sequence[str]) -> str:
    if artifact_type in {"prompt", "result"} and len(segments) > 1:
        candidate = segments[1]
        if candidate in ROLE_DIRECTORIES:
            return candidate
    return DEFAULT_ROLE_BY_TYPE.get(artifact_type, "documentation")


def parse_root_arg(arg: str, repo_root: Path) -> RootMapping:
    if "=" in arg:
        local_part, canonical_part = arg.split("=", 1)
        canonical_segments = [segment for segment in canonical_part.strip("/").split("/") if segment]
    else:
        local_part = arg
        canonical_segments = [segment for segment in Path(arg).parts if segment]
    local_path = (repo_root / local_part).resolve()
    return RootMapping(local=local_path, canonical_prefix=canonical_segments)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest canonical repository artifacts into the Librarian API")
    parser.add_argument(
        "--api-base",
        default=os.environ.get("LIBRARIAN_API_BASE", "http://localhost:8000"),
        help="Librarian API base URL (default: %(default)s)",
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root containing canonical artifacts",
    )
    parser.add_argument(
        "--roots",
        nargs="+",
        default=["prompts", "results", "governance", "decisions", "references"],
        help="Root directories to ingest. Use src=namespace to override canonical prefix (e.g., data/project13=project13)",
    )
    parser.add_argument(
        "--agent-id",
        default="librarian-ingest",
        help="Agent identifier recorded in ingested artifacts",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print payloads without calling the API")
    return parser.parse_args()


def main() -> None:  # pragma: no cover - CLI script
    args = parse_args()
    repo_root = args.repo_root.resolve()
    roots = [parse_root_arg(root_arg, repo_root) for root_arg in args.roots]
    ingestor = LibrarianIngestor(api_base=args.api_base, repo_root=repo_root, agent_id=args.agent_id, dry_run=args.dry_run)
    ingestor.ingest_roots(roots)
    print(
        f"Processed={ingestor.processed} stored={ingestor.stored} skipped={ingestor.skipped} failed={ingestor.failed}",
    )


if __name__ == "__main__":  # pragma: no cover - CLI script
    main()
