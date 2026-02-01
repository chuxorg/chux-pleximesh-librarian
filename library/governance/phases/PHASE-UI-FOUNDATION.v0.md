# PHASE-UI-FOUNDATION (v0)

## Purpose

Establish the **structural, navigational, and service foundation** of the PlexiMesh UI by implementing the sockets defined in `UI-SOCKET-MODEL v0`, without binding real data, backend APIs, or feature logic.

This phase creates a **complete but data-agnostic application shell**.

---

## Core Principle

**This phase builds sockets, not features.**

All functionality implemented in this phase must:

* Be backend-independent
* Be safe to stub or leave empty
* Serve as a stable attachment point for future phases

---

## In Scope

### 1. Application Frame Implementation

* Window menu (File | Edit | View | Navigate | Window | Help)
* Global toolbar socket:

  * Search bar (non-functional)
  * Profile surface (stub)
  * Workspace selector (stub)
  * Theme selector (functional)
* Layout persistence (local only)

---

### 2. Primary Navigation System

* Far-left navigation rail
* Dynamic, declarative nav entries
* Activation of Workspace Sockets
* Support for empty / placeholder workspaces

---

### 3. Workspace + Context + Main Content Sockets

* Workspace routing
* Context Panel socket (collapsible)
* Main Content socket
* Tab Manager socket with:

  * Open / close tabs
  * Empty-state tabs
  * Placeholder views

---

### 4. Cross-Cutting UI Services

* Theme system (light/dark at minimum)
* Notification surface
* Error boundary surface
* Loading / empty-state renderer
* Keyboard shortcut routing
* Command palette (shell only)

---

### 5. Visual & Interaction Polish

* Consistent spacing, typography, and affordances
* Clear empty states (“This socket is empty by design”)
* Explicit non-functional indicators where applicable

---

## Explicitly Out of Scope

This phase MUST NOT:

* Call Librarian APIs
* Call Runtime APIs
* Bind WebSocket streams
* Implement permissions or roles
* Implement mutation or write paths
* Implement business logic
* Assume data shape beyond placeholders

---

## Phase Completion Criteria

This phase is complete when:

* The UI feels structurally complete
* All sockets defined in `UI-SOCKET-MODEL v0` exist in code
* Navigation works end-to-end with placeholders
* Tabs, menus, and toolbar operate consistently
* The only remaining work is **wiring real data**

---

## Outcome

Upon completion, future UI phases (Library Viewer, Workflows, Runtime, etc.) will be able to bind functionality **without restructuring the UI**.

This phase is a one-time investment.
