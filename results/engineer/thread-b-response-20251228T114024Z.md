## Thread B Kickoff — Librarian API Hardening

1. **Working branch**: `eng/thread-b-librarian-api`
2. **Endpoints to document**: `POST /artifacts`, `GET /artifacts`, `GET /artifacts/exists`, `GET /artifacts/list` (matching existing Mongo-backed REST surface).
3. **Postman files to create**:
   - `postman/librarian-api.postman_collection.json`
   - `postman/librarian-api.postman_environment.json`
   - `postman/README.md` (usage + API guarantees per instructions)
4. **Initial API clarification scope**:
   - Formalize request/response schemas for all four endpoints, including canonical URI expectations, error semantics (400 vs 404 vs 500), and metadata fields (`status`, `references`).
   - Document how prefix matching works for `GET /artifacts/list` and how URIs map to Mongo’s `artifacts` collection.
   - Capture persistence guarantees (append-only, no PUT/DELETE) and note that filesystem writes are deprecated.
5. **Persistence paths**:
   - Prompt stored at `results/engineer/thread-b-prompt-20251228T114024Z.md`
   - Response stored at `results/engineer/thread-b-response-20251228T114024Z.md`

Next execution step: branch from `dev` using the name above, implement the documented Postman + README artifacts, then commit/push per contract.
