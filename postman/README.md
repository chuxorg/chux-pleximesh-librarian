# PlexiMesh Librarian Read API — Postman Guide

This directory packages a ready-to-run Postman environment and collection for the
Mongo-backed Librarian read API. Import the files into Postman (v10+) to exercise
canonical read endpoints described in `librarian/openapi/librarian.v0.yaml`.

## Contents
- `librarian-api.postman_collection.json` — read-only requests for `GET /artifacts`,
  `GET /artifacts/{artifact_id}`, typed aliases (`/tasks`, `/policies`, `/phases`),
  and the documented health probe (expected 404).
- `librarian-api.postman_environment.json` — default variables for `protocol`, `host`,
  `port`, `baseUrl`, and sample identifiers used in the requests.

## Prerequisites
1. Start the Librarian API locally (choose one):
   - `docker compose up -d` (launches Mongo + API on port `8000`).
   - `pip install -r requirements.txt && LIBRARIAN_MONGO_URI=... python server.py`.
2. Ensure MongoDB is reachable and the server logs `Librarian read API listening on port <PORT>`.
3. Install the latest Postman desktop app.

## Import & Setup
1. Open Postman → **Import** → select both JSON files in `postman/`.
2. Choose the `PlexiMesh Librarian (Local)` environment from the environment picker.
3. Adjust variables as needed:
   - `protocol` (default `http`).
   - `host` (default `localhost`).
   - `port` (default `8000`).
   - `artifactId`, `taskId`, `policyId`, `phaseId` for sample reads.
   - `versionParam`, `kindFilter`, `domainFilter`, `statusFilter`, `tagFilter`.

## Running Requests
1. Select the desired request inside the **PlexiMesh Librarian Read API** collection.
2. Review the request description for parameter behavior and known limitations.
3. Hit **Send**.

| Method | Path | Required Parameters | Example Usage |
| --- | --- | --- | --- |
| `GET` | `/artifacts/{artifact_id}` | `artifact_id` | Retrieve the latest active artifact. |
| `GET` | `/artifacts/{artifact_id}?version=vX` | `artifact_id`, `version` | Exact version lookup (see limitation below). |
| `GET` | `/tasks/{task_id}` | `task_id` | Typed alias for task artifacts. |
| `GET` | `/policies/{policy_id}` | `policy_id` | Typed alias for policy artifacts. |
| `GET` | `/phases/{phase_id}` | `phase_id` | Typed alias for phase artifacts. |
| `GET` | `/artifacts` | optional `kind`, `domain`, `status`, `tag` | Filtered listing of artifacts. |
| `GET` | `/health` | none | Expected 404 (no health endpoint implemented). |

## Known Limitations
- No explicit health endpoint is implemented; `/health` returns 404.
- Write operations are disabled in the read-only API.

## OpenAPI Source of Truth
The OpenAPI spec is the canonical contract:
- `librarian/openapi/librarian.v0.yaml`

Postman assets are derived artifacts and must remain aligned with the spec.
