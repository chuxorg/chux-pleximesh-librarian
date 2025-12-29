# Librarian Intake Agent — Canonical Contract

## Purpose

The **Librarian Intake Agent** is responsible for reconciling *all discovered artifacts* into the Librarian persistence layer (Mongo), transforming a messy, evolving filesystem and agent output into a **single, queryable source of truth**.

This agent exists to **observe, normalize, and catalog reality**, not to enforce process correctness.

---

## Core Mandate

The Librarian Intake Agent SHALL:

1. Discover artifacts produced by humans or agents
2. Submit artifacts to the Librarian API
3. Assess validity, relevance, and uniqueness
4. Persist artifacts with appropriate canonical status
5. Emit events describing what changed
6. Never block execution due to process defects

---

## Inputs

### 1. Filesystem Sources (Configurable)

The agent crawls one or more configured roots, for example:

* `data/`
* `.awacs-staging/`
* agent-specific output directories
* repo roots (read-only)

Each discovered file is treated as a **candidate artifact**, never as canon by default.

---

### 2. Contextual Metadata (Optional)

If available, the agent may attach:

* originating agent ID
* git commit hash
* branch name
* execution ID
* timestamp
* inferred artifact type

Missing metadata **must not block ingestion**.

---

## Artifact Evaluation Pipeline

For every candidate artifact, the agent executes the following steps:

### Step 1 — Validity Check

Determines whether the artifact is intelligible.

Examples:

* Is the file readable?
* Is it non-empty?
* Does it conform to a known artifact format (Markdown, JSON, YAML, etc.)?

**Failure result:**
→ Store as `artifact.status = invalid` (still persisted)

---

### Step 2 — Relevance Assessment

Determines whether the artifact is related to an active system domain.

Signals include:

* Namespace hints (`project13`, `mission-rail`, `phase2-1`)
* References to known canon
* Proximity to active directories

**Failure result:**
→ Store as `artifact.status = reference`

---

### Step 3 — Uniqueness & Lineage

Computes:

* SHA-256 digest
* Logical path
* Supersession relationships

Outcomes:

* Exact duplicate → link to existing artifact
* Modified version → mark as superseding
* Conflict at same URI → flag anomaly

**No deletions occur. Ever.**

---

## Persistence Rules

The agent submits artifacts to the **Librarian REST API** using deterministic URIs.

### Canonical Status

Each artifact is persisted with one of:

* `canonical = true`
* `canonical = false`
* `canonical = unknown`

The Librarian Intake Agent **may suggest** canonical placement, but:

> **Only Guardian decisions can elevate an artifact to authoritative canon.**

---

## Event Emission

For every processed artifact, the agent emits one or more events:

* `artifact.discovered`
* `artifact.ingested`
* `artifact.duplicated`
* `artifact.superseded`
* `artifact.flagged`

These events are consumed by:

* AWACS UI
* Guardian Agent (optional)
* Audit/logging systems

---

## Non-Responsibilities (Explicit)

The Librarian Intake Agent SHALL NOT:

* Block agent execution
* Enforce SDLC gates
* Decide final authority
* Delete artifacts
* Modify artifact content
* Interpret business logic

It is a **recorder and organizer**, not a judge.

---

## Failure Philosophy

All failures are **recorded, not fatal**.

Examples:

* Unknown artifact type → persisted + flagged
* Missing metadata → persisted + noted
* Conflicting content → persisted + anomaly event

This agent exists to **surface entropy**, not suppress it.

---

## Relationship to Other Agents

| Agent         | Relationship                               |
| ------------- | ------------------------------------------ |
| Guardian      | Evaluates artifacts after ingestion        |
| PM            | Consumes Librarian views, never filesystem |
| UI / Engineer | Produce artifacts, never store canon       |
| Documentation | Curates *human-readable* system docs       |

---

## Storage Location (Authoritative)

This contract MUST be stored in the Librarian under governance canon.

### **Canonical Path**

```
central-librarian://governance/librarian/librarian-intake-agent-contract.md
```

### **Filesystem Source (for ingestion only)**

```
governance/librarian/librarian-intake-agent-contract.md
```

> Once ingested, **Mongo is authoritative**.
> The filesystem copy is merely a seed.

---

# Librarian Intake Agent — Execution Loop (Phase A)

## Goal

Continuously reconcile **filesystem reality → Librarian (Mongo)** and emit observability events.
No blocking. No enforcement. No deletion.

---

## Loop Overview (Continuous)

```
scan → classify → ingest → emit → sleep → repeat
```

---

## 1. Scan (Discovery)

**Inputs (configurable roots):**

* `governance/`
* `data/`
* `.awacs-staging/`
* agent output dirs

**Action:**

* Walk directories
* Ignore `.git`, `node_modules`, build outputs
* For each file → emit `artifact.discovered`

---

## 2. Classify (Lightweight)

For each file:

* Compute `sha256`
* Infer:

  * artifact_type (governance | prompt | result | decision | unknown)
  * logical namespace (best-effort from path)
* Attach metadata:

  * source_path
  * discovered_at
  * hash

⚠️ Missing / weird metadata is OK.

---

## 3. Ingest (Authoritative Write)

POST to Librarian API:

```
POST /artifacts
{
  logical_path,
  content,
  content_sha256,
  metadata
}
```

**Outcomes:**

* `201 stored` → new artifact
* `200 unchanged` → already known
* `409 conflict` → same URI, different content

All outcomes are valid.

---

## 4. Emit Events (Always)

After POST result:

* `artifact.ingested`
* OR `artifact.duplicated`
* OR `artifact.flagged` (on conflict / anomaly)

Also emit `process.anomaly_detected` when:

* same logical_path, different hash
* unknown artifact_type
* missing expected namespace

Nothing blocks.

---

## 5. Sleep / Repeat

* Sleep interval: 2–5 seconds (configurable)
* Stateless between runs (Mongo is memory)

---

## Pseudocode (Minimal)

```python
while True:
  files = scan_roots()
  for f in files:
    emit("artifact.discovered")
    meta = classify(f)
    result = librarian.put(meta)
    emit(result.event_type)
  sleep(INTERVAL)
```

---

## What This Immediately Unlocks

* Mongo becomes **accurate mirror of reality**
* AWACS can show:

  * artifacts appearing
  * duplicates
  * conflicts
* Guardian can **observe without blocking**
* Process bugs surface naturally

---

## Known Limitations (Accepted in Phase A)

* No prioritization
* No cleanup
* No authority decisions
* No retries beyond idempotent PUT

All acceptable.

---

## Canonical Contract Location

Already defined, but to be explicit:

```
central-librarian://governance/librarian/librarian-intake-agent-contract.md
```

---
