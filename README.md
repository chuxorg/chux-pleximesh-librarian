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

- `POST /artifacts` — `put`: normalizes and persists artifacts into MongoDB. Responds with the canonical URI plus metadata.
- `GET /artifacts?uri=central-librarian://...` — `get`: returns the stored document (header, metadata, and raw content).
- `GET /artifacts/exists?uri=central-librarian://...` — `exists`: returns `{ "exists": true|false }`.
- `GET /artifacts/list?prefix=central-librarian://project13` — `list`: enumerates artifacts whose URIs share the supplied prefix.

All endpoints are append-only; `PUT` and `DELETE` return `405 Method Not Allowed` to protect immutability.

### Request contract (v0)

```json
{
  "artifact_type": "prompt | result | governance | decision | reference",
  "agent": { "role": "guardian | pm | engineer | qa | documentation | codex", "id": "optional" },
  "execution": { "execution_id": "required", "parent_execution_id": "optional", "phase": "optional" },
  "correlation": { "root_execution_id": "required", "prompt_id": "required for result" },
  "source": { "repo": "optional", "branch": "optional", "commit": "optional" },
  "content": { "format": "markdown | text | json", "body": "raw artifact text" },
  "metadata": { "timestamp": "optional", "tags": ["optional"], "notes": "optional" }
}
```

### Correlation guarantees

- Every artifact must specify a `root_execution_id` so multi-hop reasoning is reproducible.
- Prompt artifacts ignore client-provided prompt IDs; the server issues a new UUID and embeds it in the stored file header.
- Result artifacts must cite the prompt they respond to via `correlation.prompt_id` and the same `root_execution_id`.
- Governance artifacts are only accepted from guardian agents; other types must still provide a valid role.

Each stored artifact receives a canonical URI following `central-librarian://<relative-path>/<filename>`. URIs map to the logical Librarian directory structure (prompts/, results/, governance/, etc.) even though the backing store is Mongo.

MongoDB documents (collection: `artifacts`) include:

- `uri` (unique, indexed)
- `path` (array of directory segments)
- `filename`
- `artifact_type`
- `owner_agent`
- `created_by`
- `created_at` / `updated_at`
- `status` (draft | canonical | superseded | blocked)
- `references` (array of URIs)
- `metadata` (freeform object, including client timestamps/tags)
- `content_format`
- `content`
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
    "correlation": {
      "root_execution_id": "root-789",
      "prompt_id": "PROMPT-ID-RETURNED-FROM-PREVIOUS-CALL"
    },
    "content": { "format": "markdown", "body": "Execution output body..." }
  }'
```

Each `POST /artifacts` response includes the canonical URI and logical path (relative to `LIBRARIAN_ARTIFACT_ROOT`) plus correlation identifiers so downstream agents can cite `uri@commit` in tasks and prompts.
