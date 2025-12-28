## Engineer — Implement Mongo-Backed Librarian Persistence (Step 2)

### Context

We are upgrading the Librarian persistence layer from filesystem-based storage to **MongoDB**, while preserving the **existing mental model and canonical URI structure**.

Mongo will run **containerized**, alongside the current Librarian API, within the **same `docker-compose.yml`**.

The Librarian remains the **single source of truth**.
Mongo replaces the filesystem — **not** the domain model.

---

### Objectives

1. Add a MongoDB container to the existing `docker-compose.yml`
2. Extend the Librarian API to use Mongo as its primary persistence backend
3. Preserve canonical artifact addressing using:

   ```
   central-librarian://<namespace>/<path>/<filename>
   ```
4. Implement a minimal, explicit Librarian–Mongo adapter

No agent behavior, governance logic, or workflow semantics should change.

---

### Mongo Data Model (Required)

Create a primary Mongo collection called **`artifacts`** with documents that map 1:1 to canonical Librarian artifacts.

Each artifact must include at least:

* `uri` (string, unique, indexed)
* `path` (array of strings)
* `filename`
* `content` (raw text / markdown)
* `owner_agent`
* `created_by`
* `created_at`
* `updated_at`
* `status` (draft | canonical | superseded | blocked)
* `references` (array of URIs)
* `metadata` (freeform object)

Do **not** split into multiple collections yet unless required for correctness.

---

### Librarian API Contract (Must Exist)

Implement or adapt these methods in the Librarian service:

```
put(uri, content, metadata)
get(uri)
exists(uri)
list(prefix)
```

These methods must:

* Use Mongo as the backing store
* Treat `uri` as the authoritative identifier
* Be deterministic and side-effect free

Filesystem writes should be **disabled or deprecated**, not mixed.

---

### Docker / Compose Requirements

* Add a `mongo` service to `docker-compose.yml`
* Use an official Mongo image
* Expose Mongo only to the Librarian container (no public port)
* Librarian should connect via internal Docker network
* Connection string should be configurable via env vars

No authentication or replication required at this stage.

---

### Explicit Non-Goals (Do NOT do these)

* ❌ Do not redesign Librarian semantics
* ❌ Do not add agent permissions or auth
* ❌ Do not migrate old data yet
* ❌ Do not change canonical URIs
* ❌ Do not add business logic to the Librarian

This is a **persistence swap**, not a feature.

---

### Execution Rules

* Branch from `dev`
* One task branch
* Commit and push after each meaningful step
* Open PR → `dev`
* Reference this effort as:

  ```
  Librarian Mongo Persistence — Step 2
  ```
* Persist:

  * This prompt
  * Your responses
  * Any schema or API docs you create

---

### Acceptance Criteria

This task is complete when:

1. `docker-compose up` starts Mongo + Librarian successfully
2. Librarian can:

   * `put` an artifact into Mongo
   * `get` it back by URI
   * `exists` returns correct results
   * `list` returns artifacts by prefix
3. No filesystem writes are required for normal operation
4. Guardian can reliably retrieve authorization drafts without “missing file” errors

---

### Final Note

This change unblocks Guardian, PM, and all Agents.
Correctness and clarity matter more than speed — but keep it minimal.

Proceed.
