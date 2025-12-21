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

A minimal REST service (`server.py`) accepts artifacts and writes them into the correct Librarian lane. It is intentionally boring, append-only, and transport-agnostic so we can swap HTTP for events later without changing the storage schema.

### Running the server directly

```bash
LIBRARIAN_PORT=8000 LIBRARIAN_ARTIFACT_ROOT=$(pwd) python server.py
```

Set `LIBRARIAN_ARTIFACT_ROOT` to the path where artifacts should be written (defaults to the repo root). This makes it easy to store data on a mounted volume when running inside containers.

### Running the server with Docker

The repository ships with a `Dockerfile` and `docker-compose.yml` so the Librarian can be run as an isolated container with its artifacts persisted to the host.

1. Create a host directory for artifacts (ignored by git):

   ```bash
   mkdir -p ./data
   ```

2. Start the intake service:

   ```bash
   docker compose up --build
   ```

   This maps `./data` to `/data/librarian` inside the container and exposes the API on `http://localhost:8000`. Override the port with `LIBRARIAN_PORT` to avoid collisions.

3. (Optional) Build and run with plain Docker:

   ```bash
   docker build -t librarian-intake .
   docker run --rm \
     -p 8000:8000 \
     -e LIBRARIAN_PORT=8000 \
     -e LIBRARIAN_ARTIFACT_ROOT=/data/librarian \
     -v "$(pwd)/data":/data/librarian \
     librarian-intake
   ```

Once the container is running you can submit artifacts from the host:

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

### Endpoint

- `POST /artifacts`
- JSON body (see contract below)
- Responds with the stored path, timestamp, and prompt identifier (when applicable)
- `PUT` and `DELETE` return `405 Method Not Allowed` to protect immutability

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

The stored file name follows `timestamp_artifact-type_execution-id_prompt-id.md` (prompt ID is omitted when not applicable). Each file begins with a JSON header that includes artifact type, agent role, execution/correlation identifiers, timestamp, content format, metadata, and source control references, separated from the raw body by `---`.

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

Each response includes the stored path (relative to `LIBRARIAN_ARTIFACT_ROOT`) plus the correlation identifiers so agents can cite `path@commit` in downstream work.
