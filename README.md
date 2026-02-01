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

## Artifact Read API (Canonical)

A read-only REST service (`server.py`) serves canonical artifacts from MongoDB using the LIB-002 schema. Write operations are not supported in this phase.

### Running the server directly

```bash
pip install --no-cache-dir -r requirements.txt

LIBRARIAN_PORT=8000 \
LIBRARIAN_MONGO_URI="mongodb://localhost:27017" \
LIBRARIAN_MONGO_DB=librarian \
LIBRARIAN_MONGO_ARTIFACTS_COLLECTION=artifacts \
LIBRARIAN_MONGO_EVENTS_COLLECTION=artifact_events \
python server.py
```

`LIBRARIAN_MONGO_COLLECTION` is accepted as a legacy alias for the artifacts collection name.

### Running the server with Docker

The repository ships with a `Dockerfile` and `docker-compose.yml` so the Librarian can be run with MongoDB as an isolated dependency.

1. Start Mongo + Librarian:

   ```bash
   docker compose up --build
   ```

   This launches two services:

   - `mongo`: MongoDB 7 with its data stored in the `mongo-data` volume
   - `librarian`: read API connected to Mongo via the internal Docker network

   The Librarian API is exposed on `http://localhost:8000`. Override the port with `LIBRARIAN_PORT` to avoid collisions.

2. (Optional) Build and run only the Librarian container (requires an external Mongo instance reachable via `LIBRARIAN_MONGO_URI`):

   ```bash
   docker build -t librarian-read .
   docker run --rm \
     -p 8000:8000 \
     -e LIBRARIAN_PORT=8000 \
     -e LIBRARIAN_MONGO_URI=mongodb://host.docker.internal:27017 \
     -e LIBRARIAN_MONGO_DB=librarian \
     -e LIBRARIAN_MONGO_ARTIFACTS_COLLECTION=artifacts \
     -e LIBRARIAN_MONGO_EVENTS_COLLECTION=artifact_events \
     librarian-read
   ```

### Endpoints

- `GET /artifacts/{artifact_id}` — returns the latest active version.
- `GET /artifacts/{artifact_id}?version=vX` — returns an exact version (no fallback).
- `GET /tasks/{task_id}` — latest active version for a task.
- `GET /policies/{policy_id}` — latest active version for a policy.
- `GET /phases/{phase_id}` — latest active version for a phase.
- `GET /artifacts?kind=&domain=&status=&tag=` — lists matching artifacts.

Version parameters must match `vN`.

Example read:

```bash
curl http://localhost:8000/artifacts/ENG-UI-001
```

### Canonical artifact schema (collection: `artifacts`)

Required fields:

- `artifact_id` (string)
- `kind` (task | policy | phase | law | report | schema)
- `domain` (engineering | governance | librarian | ui | runtime)
- `version` (vN, immutable)
- `status` (planned | active | deprecated | archived)
- `content_type` (text/markdown | application/yaml | application/json)
- `content` (string)
- `checksum` (sha256)
- `source` (seed-import | api-write | migration)
- `created_at` (string)
- `effective_at` (string)

Optional fields:

- `metadata` (object)
- `links` (object)

### Read guarantees

- Checksum verified on every read.
- Latest active version resolves deterministically.
- JSON serialization is deterministic (sorted keys, stable list ordering).

### Audit events (collection: `artifact_events`)

Append-only audit events are stored in `artifact_events` with at least:

- `timestamp`
- `actor`
- `artifact_id`
- `version`
- `reason`
