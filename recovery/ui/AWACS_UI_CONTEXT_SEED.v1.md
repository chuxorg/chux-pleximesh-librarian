# AWACS UI Context Seed v1

Status: Deprecated
Note: Superseded by AWACS_UI_CONTEXT_SEED.v3 after completion of UI foundation passes and transition to first feature implementation (LIB-UI-1).

## Purpose

Provide authoritative UI context for AWACS to eliminate repeated clarification during recovery, new conversations, or agent handoff.

This seed MUST be injected at the start of any UI-related conversation involving AWACS.

---

## Project Scope

* Product: PlexiMesh
* UI Codename: AWACS
* Phase: Early UI maturation (pre-runtime integration)
* Priority: Visual structure, clarity, and audit surface
* Explicitly NOT focusing on: pixel perfection, new functionality, agent data ingestion (yet)

---

## UI Stack (Frozen for this Phase)

* Platform: Electron
* Renderer: Vanilla HTML / CSS / JavaScript
* Frameworks: NONE (no React, no Vue)
* Entry points:

  * main.js → loads index.html
  * renderer.js → workspace + tab switching
* Supporting UI logic:

  * runtime-context.js
  * runtime-tabs.js
* TS scaffolding (non-renderer models only):

  * index.ts
  * src/ui/*

---

## Layout Architecture (Zones)

AWACS UI is divided into explicit spatial Zones:

1. **Zone 1** — Top App Menubar
2. **Zone 2** — Left Control Plane

   * Navigation
   * Context panel
3. **Zone 3** — Main Content Plane
4. **Zone 4** — Bottom Status Bar
5. **Zone 5** — Right Integration Rail (NEW)

   * Far-right vertical zone
   * Holds buttons / controls for external integrations
   * Visual-only at first; minimal behavior

Zones define **real estate**, not functionality.

---

## Figma Make Design Source

* Design provided as a **single static HTML file**
* File location (repo root):

  * `yanzi-design.html`
* Includes:

  * HTML structure
  * CSS styles
* No live Figma integration required or desired at this stage

---

## UI Migration Rules

* Goal: Apply design + structure to existing AWACS UI
* Allowed:

  * Move styles into existing CSS or inline style patterns
  * Map static HTML structure onto existing components/views
  * Add Zone 5 scaffolding
* Disallowed (unless blocking progress):

  * Removing existing functionality
  * Adding new behavioral features
  * Refactoring renderer logic unnecessarily

Exception:
If not adding/removing something blocks forward progress, it is allowed but must be called out.

---

## Near-Term UI Goals

1. Apply Figma Make styles to AWACS
2. Introduce Zone 5 scaffolding
3. Use existing wiring to:

   * Call Librarian REST API
   * Display Library contents as a tree in the Left Control Plane
   * Render selected artifacts in the Main Content Plane
4. Prepare a clean audit surface for upcoming runtime + agent integration

---

## Communication Contract

* Responses should be concise
* Only interrupt for:

  * Gaps in agent handoff
  * Ambiguity
  * Drift
  * Progress risk
  * ID10T Circuit Breaker events
* No verbose explanations unless explicitly requested

---

## Guardian Posture (Phase-Specific)

* Canon-first by default
* Enforcement is **advisory**, not blocking
* Human override expected
* Guardian must warn loudly if an action risks long-term harm to progress

---

## Recovery Rule

Any future UI-related conversation MUST begin by injecting:

* `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`
* `LLM_MEMORY_CONTRACT.v1`
* This seed: `AWACS_UI_CONTEXT_SEED.v1`
