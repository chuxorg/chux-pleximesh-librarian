# PlexiMesh Librarian API — Postman Guide

This directory packages a ready-to-run Postman environment and collection for the Mongo-backed Librarian REST API. Import the files into Postman (v10+) to exercise the canonical persistence endpoints that every PlexiMesh agent depends on.

## Contents
- `librarian-api.postman_collection.json` — fully documented requests for `POST /artifacts`, `GET /artifacts`, `GET /artifacts/exists`, and `GET /artifacts/list`, including sample bodies/responses and parameter explanations.
- `librarian-api.postman_environment.json` — default variables for `protocol`, `host`, `port`, `baseUrl`, and representative IDs/URIs used in request examples.

## Prerequisites
1. Start the Librarian API locally (choose one):
   - `docker compose up -d` (launches Mongo + API on port `8000`).
   - `pip install -r requirements.txt && LIBRARIAN_MONGO_URI=... python server.py`.
2. Ensure MongoDB is reachable and the server logs `Artifact intake server listening on port <PORT>`.
3. Install the latest Postman desktop app.

## Import & Setup
1. Open Postman → **Import** → select both JSON files in `postman/`.
2. Choose the `PlexiMesh Librarian (Local)` environment from the environment picker.
3. Adjust variables as needed:
   - `protocol` (default `http`).
   - `host` (default `localhost`).
   - `port` (default `8000`).
   - `sampleExecutionId`, `sampleRootExecutionId`, `samplePromptId`, `sampleArtifactUri`, `samplePrefix` for convenience when crafting demo payloads.

## Running Requests
1. Select the desired request inside the **PlexiMesh Librarian API** collection.
2. Review the markdown description for parameters, required fields, and error semantics.
3. Hit **Send**. The included example bodies/responses illustrate the canonical schema:

| Method | Path | Required Parameters | Example Usage |
| --- | --- | --- | --- |
| `POST` | `/artifacts` | JSON body with `artifact_type`, `agent.role`, `execution.execution_id`, `correlation.root_execution_id`, `content.format`, `content.body` | Persist a new artifact. Responses echo the canonical URI, prefix, and deterministic digest. |
| `PUT` | `/artifacts` | Same as `POST` | Idempotent writes; retries return `status: \"unchanged\"` instead of creating duplicates. |
| `GET` | `/artifacts` | Query `uri` | Retrieve the stored document (headers + raw content) for the supplied canonical URI. |
| `GET` | `/artifacts/exists` | Query `uri` | Lightweight existence check that returns `{ "exists": true|false }`. |
| `GET` | `/artifacts/list` | Optional query `prefix` | Enumerate artifacts whose URIs start with the prefix (e.g., `central-librarian://project13/`). |

Every request is ready to run as-is against a clean database; swap in real execution IDs, URIs, and content to capture production artifacts.

## API Guarantees (per `README.md`)
- **Idempotent persistence**: `POST` and `PUT` share the same contract. Duplicate payloads return `200 OK` with `status: "unchanged"`. `DELETE` remains disabled.
- **Canonical URIs**: responses always map files to `central-librarian://<logical-path>/<execution_id>.<ext>` and store metadata + content in Mongo. Supply `logical_path` or a `canonical_prefix` (e.g., `central-librarian://system/librarian-integrity/`) to control namespaces explicitly.
- **Conflict signaling**: different content at an existing URI triggers `409 Conflict` with both digests so agents can reconcile divergent artifacts.
- **Role-aware validation**: `agent.role` must be one of `guardian`, `pm`, `engineer`, `qa`, `documentation`, `codex`; governance artifacts must come from `guardian`.
- **Schema enforcement**: `execution.execution_id`, `correlation.root_execution_id`, and `content.body` are mandatory. Result artifacts must reference `correlation.prompt_id`. Optional metadata fields capture `supersedes`, `deprecated_by`, and `canonical` flags for consolidation.
- **Consistency helpers**: use `/exists` before `/get` when only presence matters, and `/list` to audit namespaces or build inventories.

## Extending the Collection
- Add new folders/items as endpoints evolve (e.g., future AWACS event bus integrations).
- Populate the pre-request or test scripts for auth tokens, schema assertions, or automated regression checks.
- When new endpoints land, update both the collection and `README.md` to keep Postman as the source of truth for REST interactions.
