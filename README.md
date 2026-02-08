# PlexiMesh Librarian

The Librarian is the canonical store for PlexiMesh governance, operational prompts, design decisions, and shared reference models. It exists to keep every agent and human aligned on the rules of engagement, expected behaviors, and institutional memory that guide delivery.

# The PlexiMesh Library

### Why it exists, what problem it solves, and how it’s different

## The problem PlexiMesh is solving

Modern software development — especially with AI — has a **memory problem**.

Not human memory.
**System memory.**

Teams struggle with questions like:

* *What is actually true right now?*
* *Which decisions are final, and which were just ideas?*
* *Why does this rule exist?*
* *Can we safely continue work without re-explaining everything?*
* *How do we avoid drifting when tools, agents, or people change?*

AI makes this worse, not better.

AI systems are:

* Helpful
* Fast
* But **stateless by default**

They don’t know:

* What was already decided
* What is off-limits
* What must never change
* What phase you’re in

Without a durable memory, AI *guesses*.
And guessing is how projects drift, regress, or collapse.

PlexiMesh exists to fix that.

---

## What the Library is (in plain terms)

The **PlexiMesh Library** is the **system of record for intent**.

It is not:

* A document repository
* A wiki
* A log archive
* A place where “everything ever written” lives

Instead, the Library answers one question reliably:

> **“What is authoritative right now, and what rules govern change?”**

If something matters for:

* Recovery
* Execution
* Governance
* Drift prevention

…it belongs in the Library.

If it doesn’t, it doesn’t.

---

## Why this matters with AI

Most AI workflows fail in one of two ways:

### 1. Everything is remembered

* Long chat histories
* Endless context
* Old decisions bleeding into new work
  → **Drift, confusion, hallucination**

### 2. Nothing is remembered

* Every session starts fresh
* Re-explaining constantly
  → **Fatigue, inconsistency, repeated mistakes**

PlexiMesh takes a third approach:

> **Remember only what must be remembered — explicitly, structurally, and verifiably.**

That’s what the Library does.

---

## The core idea: Canonical truth vs. everything else

The Library only stores **canonical artifacts** — things that are:

* Explicitly approved
* Versioned
* Checksummed
* Recoverable
* Enforceable

Everything else is:

* Temporary
* Exploratory
* Disposable

This separation is intentional.

It allows:

* Fast iteration
* Strong guarantees
* Safe use of AI

---

## What lives in the Library (at a high level)

You don’t need to know internal formats to understand the categories.

### 1. Rules

**What may never change**

Examples:

* How execution works
* What “EXECUTE” means
* What an agent is allowed to do

Rules are rare, stable, and global.

---

### 2. Charters

**Who can do what**

Each role (UI agent, runtime agent, PM, Guardian) has a Charter that defines:

* Responsibilities
* Boundaries
* Prohibitions

This prevents “helpful” AI from overstepping.

---

### 3. Seeds

**The minimum state needed to continue work**

Seeds are compact state vectors that say:

* What project this is
* What phase you’re in
* What’s frozen
* What’s active

Seeds are what let you start a new AI session **without re-explaining everything**.

---

### 4. Snapshots

**Where you are in time**

At the end of every phase, PlexiMesh records:

* What was completed
* What is now frozen
* What comes next

Snapshots prevent “where were we again?” moments.

Only the **latest snapshot** matters for execution.

---

### 5. Packs

**How a new AI session is born correctly**

A Pack is a curated bundle of references that tells PlexiMesh:

> “To start a new session for this role, inject *these* rules, *these* seeds, and *this* snapshot.”

This turns AI rehydration into a mechanical step, not a ritual.

---

## What the Library deliberately does NOT do

This is just as important.

The Library does **not**:

* Store brainstorming
* Store chat transcripts
* Store half-finished ideas
* Store history by default
* Require humans to read everything

History may exist elsewhere, but **execution never depends on it**.

This keeps the system:

* Calm
* Predictable
* Recoverable

---

## Why this prevents drift

Drift happens when:

* Past ideas masquerade as current truth
* AI fills in gaps
* Humans assume things are “still understood”

The Library prevents this by enforcing a simple rule:

> **If it’s not in the Library, it is not authoritative.**

No guessing.
No vibes.
No accidental regressions.

---

## What this means for you as a user

Practically, the Library gives you:

* Confidence that AI is operating within agreed boundaries
* The ability to stop and resume work without loss
* Protection against silent scope creep
* A clean separation between *thinking* and *doing*
* A way to scale AI without scaling chaos

You don’t have to micromanage the AI.
You just define intent once — and the Library makes it stick.

---

## The bigger picture

PlexiMesh is not trying to make AI smarter.

It’s trying to make **systems resilient** in the presence of AI.

The Library is the memory that makes that possible.

When AI forgets, the Library remembers.
When humans are tired, the Library protects decisions.
When teams change, the Library preserves intent.

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
