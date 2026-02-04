# PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2

## Purpose

Provide authoritative, current project state for PlexiMesh / AWACS to eliminate drift, ambiguity, and re-litigation of decisions during recovery, new conversations, or agent handoff.

This snapshot MUST be treated as **canonical** for all UI-related work unless explicitly superseded by a higher-version snapshot.

---

## Project Scope

* Product: PlexiMesh
* UI Codename: AWACS
* Phase: Early UI maturation (pre-runtime integration)
* Priority:

  * Structural clarity
  * Deterministic layout contracts
  * Read-only audit surface
* Explicitly NOT focusing on (yet):

  * Pixel perfection
  * Write-capable UI
  * Agent execution controls
  * Runtime event orchestration

---

## UI Stack (Frozen for This Phase)

* Platform: Electron
* Renderer: Vanilla HTML / CSS / JavaScript
* Frameworks: **NONE** (no React, no Vue)
* Entry points:

  * `main.js` → loads `index.html`
  * `renderer.js` → workspace, tabs, UI wiring
* Supporting UI logic:

  * `runtime-context.js`
  * `runtime-tabs.js`
* TypeScript usage:

  * Non-renderer models only
  * `index.ts`
  * `src/ui/*`

Renderer remains **single-file shell** (`index.html`) by design in this phase.

---

## Layout Architecture (Zones — Canonical)

AWACS UI is divided into explicit, enforced spatial Zones.
Zones define **real estate**, not functionality.

1. **Zone 1 — Top App Menubar**
2. **Zone 2 — Left Control Plane**

   * Navigation
   * Context panel
   * Library Tree (read-only)
3. **Zone 3 — Main Content Plane**

   * Artifact Viewer (read-only)
4. **Zone 4 — Bottom Status Bar**
5. **Zone 5 — Right Integration Rail**

   * Far-right vertical rail
   * Visual-only scaffolding
   * No execution semantics

### Zone Contract Enforcement

* Zones are laid out via explicit CSS grid columns
* Widths are controlled by variables:

  * `--zone2-width`
  * `--inspector-width`
  * `--zone5-width`
* All zone containers are marked with stable `data-zone` attributes
* A UI smoke test enforces:

  * Zone presence
  * Ordering
  * Grid usage

---

## Styling & Theme Model (Current Truth)

* Styling is inline within `index.html` (by intent, for now)
* Scoped theme enabled via:

  * `body[data-theme="yanzi"]`
* **Token Layer v1** is canonical:

  * Semantic CSS variables (`--awacs-*`)
  * All major surfaces consume tokens
  * Prevents palette drift
* Light mode is the active baseline
* Dark mode exists only as a stub (no wiring, no toggle)
* No parallel theme systems are permitted

---

## Figma Make Design Source

* Design provided as a **single static HTML file**
* File location:

  * `yanzi-design.html`
* Includes:

  * HTML structure
  * CSS styles
* Role:

  * Visual reference + style source
  * Not a live dependency
  * Not a runtime artifact

---

## Library UI (Current Capability)

### Library Tree (Zone 2)

* Renders automatically on Library workspace activation
* Uses existing Librarian REST API (GET-only)
* Deterministic grouping and ordering
* Expand / collapse supported
* Single-selection model
* Selected row is tokenized and visually distinct
* Session-local persistence of last selection (optional feature, enabled)

### Artifact Viewer (Zone 3)

* Read-only by design
* Displays:

  * Artifact metadata
  * Content path
  * Artifact body (pretty JSON or raw)
* Explicit read-only indicator
* Explicit error messaging (e.g., “Content unavailable”)
* Viewer failures do not affect tree rendering

---

## Librarian Connectivity (Canonical Behavior)

* Base URL resolution uses a single resolver:

  * Default: `http://localhost:8000`
  * Existing UI inputs override
* Supported endpoints:

  * `GET /artifacts`
  * `GET /artifacts/:id`
  * `GET /artifacts/:id/content`
* Payload normalization supports only:

  * `Array`
  * `{ artifacts: [] }`
  * `{ items: [] }`
* Health endpoint availability is **not** required
* Empty or invalid payloads fail visibly, not silently

---

## Runtime UI Posture (As of v2)

* Runtime daemon connectivity is **optional**
* Runtime event streams (e.g., `/events`) must:

  * Be lazy (Runtime workspace only)
  * Never block Library UI
  * Never fail the renderer on connection errors
* Runtime integration is **not yet active**
* Zone 5 exists to prepare for this future work

---

## Determinism & Hardening Guarantees

* Library Tree rendering is hardened:

  * Safe selection state (`selectedId` always defined or null)
  * Per-item render isolation (one bad artifact cannot blank the tree)
* UI contract smoke tests assert:

  * Zone presence and order
  * Read-only posture
  * No write-like controls
  * Grid-based shell layout
* Tests run via:

  * `npm run test` → `tsc` + `scripts/test-stub.js`

---

## UI Migration Rules (Still in Effect)

* Allowed:

  * Inline CSS refinements
  * Token tuning
  * Structural hardening
  * Read-only UI extensions
* Disallowed (unless blocking progress):

  * Adding write/execute semantics
  * Introducing frameworks
  * Large renderer refactors
* Any exception must be explicitly called out and justified

---

## Guardian Posture (Phase-Specific)

* Canon-first by default
* Enforcement is **advisory**, not blocking
* Human override expected
* Guardian must warn loudly if:

  * A change risks determinism
  * A change risks auditability
  * A change collapses zone or read-only contracts

---

## Recovery Rule (Updated)

Any future UI-related conversation MUST begin by injecting:

* `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`
* `LLM_MEMORY_CONTRACT.v1`
* `AWACS_UI_CONTEXT_SEED.v1`

Older snapshots (v1 and earlier) are **superseded** and must not be treated as authoritative.
