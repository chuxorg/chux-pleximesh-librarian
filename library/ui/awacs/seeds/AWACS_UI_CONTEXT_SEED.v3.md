# AWACS_UI_CONTEXT_SEED.v3

Status: **Active (Canonical)**
Supersedes: AWACS_UI_CONTEXT_SEED.v1
Authority: Human Architect

---

## Purpose

Provide authoritative, up-to-date UI context for AWACS to eliminate repeated clarification during recovery, new conversations, or agent handoff.

This seed MUST be injected at the start of any UI-related conversation involving AWACS.

This version reflects the **post–shell freeze** state and the transition into **first feature implementation**.

---

## Project Scope

* Product: PlexiMesh
* UI Codename: AWACS
* Current Phase: **Post-foundation freeze / Feature execution**
* Priority:

  * Visual stability
  * Audit clarity
  * Deterministic execution
* Explicitly NOT focusing on:

  * Shell/layout redesign
  * Styling churn
  * Experimental UI behavior
  * Agent-driven UI mutation

The AWACS UI shell is now considered **frozen**.

---

## UI Stack (Frozen)

* Platform: Electron
* Renderer: Vanilla HTML / CSS / JavaScript
* Frameworks: **NONE** (no React, no Vue)
* Entry points:

  * `main.js` → loads `index.html`
  * `renderer.js` → workspace + tab switching
* Supporting UI logic:

  * `runtime-context.js`
  * `runtime-tabs.js`
* TypeScript scaffolding (non-renderer models only):

  * `index.ts`
  * `src/ui/*`

Renderer architecture is stable. Refactors require explicit approval.

---

## Layout Architecture (Zones — Frozen)

AWACS UI is divided into explicit spatial zones.
Zones define **real estate only**, not behavior.

1. **Zone 1** — Top App Menubar (frozen)
2. **Zone 2** — Left Control Plane (frozen)

   * Navigation
   * Contextual trees
3. **Zone 3** — Main Content Plane (frozen)

   * Read-only viewers
4. **Zone 4** — Bottom Status Bar (frozen)
5. **Zone 5** — Right Integration Rail (frozen)

   * Visual placeholders only
   * Disabled during read-only phases

**Zone geometry, spacing, typography, and surfaces are frozen.**

---

## Visual Foundation Status

The following UI foundation passes are complete and merged:

* Pass 1 — Layout & zone alignment
* Pass 2 — Typography & base elements
* Pass 3 — Surface cleanup & flat tone
* Pass 4 — Spacing & rhythm

No further shell or foundation changes are permitted without explicit authorization.

---

## Current Feature Focus

### Library UI — Phase LIB-UI-1 (Read-only)

The Library UI is the **first non-foundation feature** built on the frozen shell.

Scope:

* Tree-based Library navigation in Zone 2
* Read-only artifact viewer in Zone 3
* Visual-only placeholders in Zone 5
* No editing, mutation, approvals, or workflow actions

Design intent:

* Canonical artifacts
* Read-only
* Audit-oriented
* “Records under glass” (not documents, not editors)

---

## Canonical Implementation Model

* UX intent is defined first (contract + minimal interactions)
* Implementation is performed by the **UI Agent**
* Execution engine may be CodeX, but **Codex is not the agent**
* Each feature phase must land as **one coherent PR**
* No partial or incremental feature PRs unless explicitly authorized

---

## Governance & Process Notes

* PR creation and merging governed by `PR_EXECUTION_LAW.v2`
* Repo-verifiable evidence is authoritative
* Verification artifacts must exist in-repo
* PR descriptions are informative but non-authoritative
* Test contracts must assert **semantic behavior**, not implementation detail

MCP / Librarian API access may be unavailable in some agent environments.
In those cases, explicit bootstrap instructions may be used and must be declared.

---

## Communication Contract

* EXECUTION MODE is default
* Deliverables should be prompts or concrete actions
* No explanations unless:

  * Intent is unclear
  * A blocking ambiguity exists
  * A governance or scope violation is detected

---

## Guardian Posture (Current Phase)

* Canon-first and **strict** for foundation stability
* Guardian must block:

  * Shell/layout changes
  * Unauthorized refactors
  * Multi-PR feature fragmentation
* Human override is allowed but must be explicit

---

## Recovery Rule (Updated)

Any future UI-related conversation MUST begin by injecting:

* `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`
* `LLM_MEMORY_CONTRACT.v1`
* **This seed:** `AWACS_UI_CONTEXT_SEED.v3`

v1 is deprecated and must not be used.

---

Status: **Authoritative**
