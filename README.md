# PlexiMesh Librarian

The Librarian is the canonical store for PlexiMesh governance, operational prompts, design decisions, and shared reference models. It exists to keep every agent and human aligned on the rules of engagement, expected behaviors, and institutional memory that guide delivery.

## What belongs here
- Governance artifacts: laws, mandates, SDLC guardrails, escalation and pause criteria.
- Operational prompts for every PlexiMesh agent role (PM, Engineering, QA, Documentation, Codex, etc.).
- Canonical decisions: trade studies, rationale for directional choices, and signed-off implementations.
- Reference schemas: taxonomies, role definitions, naming conventions, and directory standards used across projects.

## What does **not** belong here
- Runtime source code, configs, or infrastructure manifests (they remain with their respective services).
- Ephemeral meeting notes, raw brainstorms, or artifacts lacking final approval.
- Generated build artifacts or binaries.
- Non-PlexiMesh governance materials unless they directly affect PlexiMesh delivery.

## Repository structure
```
/README.md            ← Purpose, inclusion rules, and API basics
/CONTRIBUTING.md      ← Intake, versioning, and referencing protocol
/governance/          ← Laws, mandates, SDLC philosophy, escalation criteria
  laws/
  mandates/
  sdlc/
  escalations/
/prompts/             ← Operational prompts grouped by agent role
  pm/
  engineering/
  qa/
  documentation/
  codex/
/results/             ← Stored execution outputs grouped by agent role
  guardian/
  pm/
  engineering/
  qa/
  documentation/
  codex/
/decisions/           ← Canonical tradeoffs and architecture/process decisions
  architecture/
  process/
/references/          ← Schemas, taxonomies, role definitions, naming guidance
  taxonomies/
  roles/
  naming/
  directory-standards/
```

## How to consume this repo
- Humans can browse the directories directly or read aggregated context via curated prompts.
- Agents reference files by absolute path (e.g., `prompts/pm/backlog-curation.md`) and record the commit SHA in their responses.
- AWACS or other supervisory systems can treat directory boundaries as capability namespaces when composing briefings.

## Next steps
1. Populate each directory with the authoritative artifacts pulled from prior phases (no net-new content yet).
2. Attach version notes (see `CONTRIBUTING.md`) so consumers can reason about lineage.
3. Wire Librarian paths into PM/Engineer/Guardian prompt templates so they always cite their sources.

## Artifact Intake API

A minimal REST service (`server.py`) accepts artifacts and writes them into Mongo-backed storage while preserving the canonical Librarian URI scheme. It is intentionally boring, append-only, and transport-agnostic so we can swap HTTP for events later without changing the storage schema.

### Running the server directly

```bash
pip install --no-cache-dir -r requirements.txt

LIBRARIAN_PORT=8000 \
LIBRARIAN_ARTIFACT_ROOT=$(pwd) \
LIBRARIAN_MONGO_URI="mongodb://localhost:27017" \
LIBRARIAN_MONGO_DB=librarian \
LIBRARIAN_MONGO_COLLECTION=artifacts \
python server.py
```

Set `LIBRARIAN_ARTIFACT_ROOT` to the virtual root used when constructing canonical URIs (defaults to the repo root). All artifact content is persisted to MongoDB using the `LIBRARIAN_MONGO_*` environment variables; the filesystem is no longer used as the primary backing store.

### Running the server with Docker

The repository ships with a `Dockerfile` and `docker-compose.yml` so the Librarian can be run with MongoDB as an isolated dependency.

1. Start Mongo + Librarian:

   ```bash
   docker compose up --build
   ```

   This launches two services:

   - `mongo`: MongoDB 7 with its data stored in the `mongo-data` volume
   - `librarian`: artifact API connected to Mongo via the internal Docker network

   The Librarian API is exposed on `http://localhost:8000`. Override the port with `LIBRARIAN_PORT` to avoid collisions.

2. (Optional) Build and run only the Librarian container (requires an external Mongo instance reachable via `LIBRARIAN_MONGO_URI`):

   ```bash
   docker build -t librarian-intake .
   docker run --rm \
     -p 8000:8000 \
     -e LIBRARIAN_PORT=8000 \
     -e LIBRARIAN_ARTIFACT_ROOT=/data/librarian \
     -e LIBRARIAN_MONGO_URI=mongodb://host.docker.internal:27017 \
     -e LIBRARIAN_MONGO_DB=librarian \
     -e LIBRARIAN_MONGO_COLLECTION=artifacts \
     librarian-intake
   ```

Once the API is running you can submit and retrieve artifacts from the host.

```bash
curl -X POST http://localhost:8000/artifacts \
  -H 'Content-Type: application/json' \
  -d '{
    "artifact_type": "prompt",
    "agent": { "role": "pm", "id": "pm-42" },
    "execution": { "execution_id": "exec-123" },
    "correlation": { "root_execution_id": "root-789" },
    "content": { "format": "markdown", "body": "# Prompt body" }
  }'
```

### Endpoints

- `POST /artifacts` — idempotent create: normalizes payloads, derives the canonical URI, and persists the artifact. Duplicate payloads return `200` with `status=unchanged`.
- `PUT /artifacts` — same contract as `POST`. Provided for agents that prefer PUT semantics for idempotent writes.
- `GET /artifacts?uri=central-librarian://...` — returns the stored document (header, metadata, and raw content).
- `GET /artifacts/exists?uri=central-librarian://...` — returns `{ "exists": true|false }`.
- `GET /artifacts/list?prefix=central-librarian://project13` — enumerates artifacts whose URIs share the supplied prefix.

`DELETE` remains `405 Method Not Allowed`. Conflicting writes return `409 Conflict` with the stored and incoming digests so callers understand which URI already owns the logical artifact.

### Request contract (v0)

```json
{
  "artifact_type": "prompt | result | governance | decision | reference",
  "agent": { "role": "guardian | pm | engineer | qa | documentation | codex", "id": "optional" },
  "execution": { "execution_id": "required", "parent_execution_id": "optional", "phase": "optional" },
  "correlation": { "root_execution_id": "required", "prompt_id": "required for result" },
  "source": { "repo": "optional", "branch": "optional", "commit": "optional" },
  "content": { "format": "markdown | text | json", "body": "raw artifact text" },
  "logical_path": ["optional", "namespace"],   // OR provide canonical_prefix below
  "canonical_prefix": "central-librarian://system/librarian-integrity/",  // optional override for the namespace
  "status": "draft | canonical | superseded | blocked (optional)",
  "references": ["optional URIs"],
  "metadata": {
    "timestamp": "optional",
    "tags": ["optional"],
    "notes": "optional",
    "supersedes": ["optional URIs"],
    "deprecated_by": ["optional URIs"],
    "canonical": true
  }
}
```

### Correlation guarantees

- Every artifact must specify a `root_execution_id` so multi-hop reasoning is reproducible.
- Prompt artifacts ignore client-provided prompt IDs; the server deterministically derives a UUID from the `execution_id` so retries reuse the same prompt identifier.
- Result artifacts must cite the prompt they respond to via `correlation.prompt_id` and the same `root_execution_id`.
- Governance artifacts are only accepted from guardian agents; other types must still provide a valid role.

Each stored artifact receives a canonical URI following `central-librarian://<logical-path>/<execution_id>.<ext>`. The logical path comes from the supplied `logical_path` (or `canonical_prefix`) or falls back to the artifact-type defaults (e.g., `prompts/<role>`). The filename is the sanitized `execution_id`, so retries with the same logical artifact always target the same URI. When callers provide an explicit `canonical_prefix` such as `central-librarian://system/librarian-integrity/`, the server validates it but never rewrites it.

Replay safety: re-submitting the exact same payload returns `200 OK` with `status: "unchanged"`. Attempts to store different content at an existing URI fail with `409 Conflict` and include both the stored and incoming digests so agents can reconcile divergent data.

MongoDB documents (collection: `artifacts`) include:

- `uri` (unique, indexed)
- `path` (array of directory segments) + `relative_path` (joined string)
- `canonical_prefix`
- `filename`
- `artifact_type`
- `owner_agent`
- `execution_id`, `root_execution_id`, `prompt_id`/`correlation_prompt_id`
- `created_by`
- `created_at` / `updated_at`
- `status` (draft | canonical | superseded | blocked)
- `is_canonical`
- `supersedes` / `deprecated_by`
- `references` (array of URIs)
- `metadata` (freeform object, including client timestamps/tags)
- `content_format`
- `content_sha256`
- `content`
- `digest` (sha256 of the normalized payload)
- `header` (JSON structure mirrored from the legacy file header)

### Example requests

Submit a prompt artifact:

```bash
curl -X POST http://localhost:8000/artifacts \\
  -H 'Content-Type: application/json' \\
  -d '{
    "artifact_type": "prompt",
    "agent": { "role": "pm", "id": "pm-42" },
    "execution": { "execution_id": "exec-123", "phase": "phase-3" },
    "correlation": { "root_execution_id": "root-789" },
    "logical_path": ["prompts", "pm"],
    "content": { "format": "markdown", "body": "## Sprint Planning Prompt\\n..." },
    "metadata": { "tags": ["planning"] }
  }'
```

Submit a result artifact that references the prompt above:

```bash
curl -X POST http://localhost:8000/artifacts \\
  -H 'Content-Type: application/json' \\
  -d '{
    "artifact_type": "result",
    "agent": { "role": "engineer", "id": "eng-17" },
    "execution": { "execution_id": "exec-124" },
    "logical_path": ["results", "engineer", "mission-rail"],
    "correlation": {
      "root_execution_id": "root-789",
      "prompt_id": "PROMPT-ID-RETURNED-FROM-PREVIOUS-CALL"
    },
    "content": { "format": "markdown", "body": "Execution output body..." }
  }'
```

Each `POST /artifacts` response includes the canonical URI, canonical prefix, and deterministic digest so downstream agents can cite `uri@commit`. To write into privileged namespaces such as the Librarian integrity area, provide a fully qualified prefix:

```json
{
  "canonical_prefix": "central-librarian://system/librarian-integrity/",
  "execution": { "execution_id": "guardian-audit-20251228" },
  "...": "..."
}
```

The server validates the prefix but never rewrites it, so callers retain full control over directory-level namespaces.

### Canonical ingestion utility

Use `tools/ingest_canonical_repo.py` to load existing repository artifacts into the Mongo-backed Librarian. The script walks the specified directories, derives deterministic URIs (using `logical_path` + `execution_id`), and calls the API so stored digests match the live contract.

```bash
python tools/ingest_canonical_repo.py --api-base http://localhost:8000
```

To ingest Project 13 artifacts that live under `data/project13/` but should be stored at `central-librarian://project13/...`, supply a prefix override:

```bash
python tools/ingest_canonical_repo.py \
  --api-base http://localhost:8000 \
  --roots "data/project13=project13"
```

Add additional `dir=canonical/prefix` mappings as needed. Pass `--dry-run` to audit the files that would be ingested without performing writes.
