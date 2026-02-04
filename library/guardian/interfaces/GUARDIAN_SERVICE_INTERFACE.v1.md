# GUARDIAN_SERVICE_INTERFACE.v1

## Purpose

Define the interface and invariants for the **Guardian Service**, a backend component that uses Codex app-server to assist with Guardian operations while preserving auditability and human control.

---

## Role Definition

The Guardian Service:

* Assists with **analysis and proposal**
* Never mutates state silently
* Never replaces human authority
* Emits artifacts and diffs, not actions

---

## Execution Model

* Backend service
* Integrates with **Codex app-server**
* Stateless between requests except for request-scoped context
* All state is sourced from the Librarian

---

## Inputs

### Required Inputs

* Active Project State Snapshot
* Active Phase Artifact
* Applicable Guardian Laws
* Requested operation (e.g., “Propose Phase Close”)

### Optional Inputs

* Diff target (snapshot vN → vN+1)
* Constraints (e.g., “UI-only”)

---

## Outputs (Strict)

The Guardian Service may return **only**:

* Proposed artifacts (markdown / yaml / json)
* Diff patches against existing artifacts
* Structured plans (step lists)

It must **never**:

* Write to the Librarian
* Modify repositories
* Execute system commands
* Assume approval

---

## Core Operations (v1)

### 1. Generate Context Bundle

* Returns a deterministic concatenation of authoritative artifacts
* Used for:

  * Chat rehydration
  * External agent invocation

### 2. Propose Phase Close

* Produces:

  * Candidate `PROJECT_STATE_SNAPSHOT.v(N+1)`
  * Archive list
  * Seed update deltas
* Must cite the Phase Close Law explicitly

### 3. Diff Snapshots

* Structural and semantic diff between snapshots
* Read-only, explanatory

---

## Security & Audit Invariants

* Every response must reference input artifact checksums
* Outputs must be content-addressable
* No hidden state
* No side effects

---

## Failure Behavior

* Missing inputs → explicit error
* Conflicting laws → explicit refusal
* Ambiguous authority → request clarification

---

## Relationship to AWACS

* AWACS is the **control plane**
* Guardian Service is the **proposal engine**
* Codex app-server is the **reasoning substrate**

ChatGPT / Atlas is **advisory only**.

---

## Future Extensions (Non-binding)

* Event streaming of Guardian proposals
* Approval workflows
* Automated Phase Close execution (explicitly gated)

---

## Canonical Rule

Guardian authority lives in **artifacts**, not conversations.
