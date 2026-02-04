# AWACS_UI_CONTEXT_SEED.v2

## Purpose

Provide authoritative, up-to-date UI context for AWACS to eliminate repeated clarification during recovery, new conversations, or agent handoff.

This seed MUST be injected at the start of any UI-related conversation involving AWACS.

This version reflects the **post-foundation-freeze** state of the UI.

---

## Project Scope

* Product: PlexiMesh
* UI Codename: AWACS
* Current Phase: **Post-shell freeze / First feature development**
* Priority:

  * Visual stability
  * Audit clarity
  * Deterministic implementation
* Explicitly NOT focusing on:

  * Foundation layout changes
  * Styling churn
  * Experimental UI behavior
  * Agent-driven UI mutation

The AWACS shell is now considered **frozen**.

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
* TS scaffolding (non-renderer models only):

  * `index.ts`
  * `src/ui/*`

Renderer architecture is **stable**. Refactors require explicit justification.

---

## Layout Architecture (Zones — Frozen)

AWACS UI is divided into explicit spatial Zones.
These define **real estate only**, not behavior.

1. **Zone 1** — Top App Menubar (frozen)
2. **Zone 2** — Left Control Plane (frozen)

   * Navigation
   * Contextual trees
3. **Zone 3** — Main Content Plane (frozen)

   * Read-only viewers
4. **Zone 4** — Bottom Status Bar (frozen)
5. **Zone 5** — Right Integration Rail (frozen)

   * Visual placeholders only
   * Disabled in read-only phases

**Zone geometry, spacing, typography, and surfaces are frozen.**

---

## Visual Foundation Status

The following passes are **complete and merged to `dev`**:

* Pass 1 — Layout & zone alignment
* Pass 2 — Typography & base elements
* Pass 3 — Surface cleanup & flat Yanzi tone
* Pass 4 — Spacing & rhythm

No further shell changes are allowed without explicit approval.

---

## Design Source of Truth

* **Figma Make is used for visual iteration only**
* Design artifacts are:

  * Disposable
  * Regenerated from prompts
* The **prompt**, not the HTML mock, is the source of truth

A **canonical Figma Make prompt** for the Library UI has been frozen and registered.

No live Figma document integration is used at this stage.

---

## Current Feature Focus

### Library UI — Phase LIB-UI-1 (Read-only)

This is the **first non-foundation feature** built on the frozen shell.

Scope:

* Tree-based Library navigation in Zone 2
* Read-only artifact viewer in Zone 3
* No editing, mutation, or workflow actions
* Visual-only placeholders in Zone 5

The Library UI is:

* Read-only
* Canonical
* Audit-oriented
* Designed to feel like **records under inspection**, not documents

---

## Canonical Implementation Flow

1. UX contract defined first
2. Minimal interactions enumerated
3. Figma Make prompt frozen
4. **Single PR implementation by Engineer Agent (CodeX)**
5. No partial or incremental PRs

All UI feature implementations must land as **one coherent PR** unless explicitly authorized otherwise.

---

## Governance & Process Notes

* PR_EXECUTION_LAW.v2 governs all PR creation and merges
* Repo-verifiable evidence is authoritative
* PR descriptions are helpful but non-authoritative
* Verification artifacts must exist in-repo

MCP / Library access may be unavailable in some agent environments.
In those cases, **bootstrap instructions** may be used, but must be explicitly declared.

---

## Communication Contract

* Responses should be concise and intent-focused
* Interrupt only for:

  * Ambiguity
  * Drift
  * Governance violations
  * Scope violations
  * ID10T circuit-breaker events
* Avoid speculative or exploratory work unless requested

---

## Guardian Posture (Current Phase)

* Canon-first by default
* Enforcement is **strict for foundation stability**
* Human override allowed but must be explicit
* Guardian must block:

  * Shell changes
  * Unauthorized refactors
  * Multi-PR feature fragmentation

---

## Recovery Rule (Updated)

Any future UI-related conversation MUST begin by injecting:

* `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`
* `LLM_MEMORY_CONTRACT.v1`
* **This seed:** `AWACS_UI_CONTEXT_SEED.v2`

v1 is now deprecated.

---

Status: **Authoritative**
