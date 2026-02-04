# PHASE-GUARDIAN-WORKBENCH.v1

## Purpose

Introduce a first-class **Guardian Workbench** inside AWACS to manage Guardian context, phase boundaries, and recovery deterministically.

This phase exists to eliminate reliance on chat memory for Guardian continuity and to reduce recovery and rehydration cost as PlexiMesh scales.

---

## Phase Scope

* Product: PlexiMesh
* UI: AWACS
* Phase: Guardian Workbench (MVP)
* Posture: Read-only + assisted actions (no silent mutation)

---

## Problem Statement

The Guardian role is critical and state-heavy. Maintaining Guardian continuity through conversational context alone does not scale as:

* The number of artifacts increases
* Phases shorten
* Context switches become frequent
* Multiple agent roles operate concurrently

This phase moves Guardian from a *role performed in chat* to a *first-class system component*.

---

## Core Objectives

1. Make **Guardian context explicit, visible, and selectable**
2. Eliminate manual cut/copy/paste recovery workflows
3. Provide deterministic context bundles for:

   * Chat rehydration
   * Agent invocation
   * Phase close operations
4. Preserve **human authority** at all times

---

## In-Scope Capabilities (MVP)

### Guardian Workbench UI (AWACS)

**Zone 2 — Guardian Tree**

* Active Snapshot
* Phase Artifacts
* Guardian Laws
* Seeds (MASTER / PANIC / UI)
* Archived Snapshots (collapsed, read-only)

**Zone 3 — Context Composer (Read-only)**

* Displays the current authoritative Guardian set:

  * Active `PLEXIMESH_PROJECT_STATE_SNAPSHOT`
  * Active Phase artifact
  * Required Guardian Laws
  * Active Seeds
* One-click **Context Bundle Export** (copy only)

**Zone 5 — Guardian Actions (Visual-first)**

* Bundle
* Diff
* Propose Phase Close
* Archive
  (No execution semantics in v1)

---

## Out of Scope (Explicit)

* No autonomous Guardian decisions
* No silent snapshot mutation
* No direct writes to Librarian
* No execution of Codex outputs without human confirmation
* No dependency on chat history for correctness

---

## Data Sources

* Librarian API (GET-only)
* Canonical artifacts:

  * Project State Snapshots
  * Guardian Laws
  * Phase Artifacts
  * Seeds

---

## Success Criteria

* A user can recover Guardian context in seconds by selecting artifacts
* Guardian state is reproducible without chat transcripts
* Phase Close Law can be executed with predictable, bounded effort
* ChatGPT is no longer a single point of failure for Guardian continuity

---

## Completion Rule

This phase is complete when:

* Guardian Workbench MVP is live in AWACS
* Context Bundle export is functional
* Guardian continuity no longer depends on conversational memory
