# UI FOUNDATION — TASK INVENTORY (v0)

## Purpose

Define the **minimal, ordered execution tasks** required to implement the UI socket foundation defined in `UI-SOCKET-MODEL v0` and governed by `PHASE-UI-FOUNDATION v0`.

These tasks establish **structure only**.
They explicitly exclude feature logic and backend integration.

---

## Task Ordering Rule

Tasks are executed **sequentially** unless explicitly authorized otherwise.

Authorization ≠ execution.

---

## UI-001 — Application Frame & Window Menu

**Purpose:**
Establish the immutable application frame.

**Scope:**

* Electron window shell
* OS-level menu:

  * File | Edit | View | Navigate | Window | Help
* Menu actions may emit intents but perform no feature logic

**Out of Scope:**

* Feature routing
* API calls
* Permissions

---

## UI-002 — Global Toolbar Socket

**Purpose:**
Create the always-visible global toolbar socket.

**Scope:**

* Global search bar (non-functional stub)
* Profile surface (placeholder)
* Workspace selector (placeholder)
* Theme selector (functional)
* Global status indicators (stub)

**Out of Scope:**

* Search indexing
* Identity management
* Backend wiring

---

## UI-003 — Primary Navigation Rail & Workspace Routing

**Purpose:**
Implement the far-left navigation and workspace activation model.

**Scope:**

* Declarative nav list
* Dynamic nav entries
* Workspace activation
* Empty workspace support

**Out of Scope:**

* Feature ownership
* Data loading
* Permissions

---

## UI-004 — Workspace Layout Sockets

**Purpose:**
Implement structural sockets inside each workspace.

**Scope:**

* Context Panel socket
* Main Content socket
* Collapsing / resizing behavior
* Placeholder rendering

**Out of Scope:**

* Trees with real data
* Domain-specific controls

---

## UI-005 — Tab Manager Socket

**Purpose:**
Provide tabbed interaction inside the Main Content socket.

**Scope:**

* Open / close tabs
* Empty tab states
* Placeholder tab content
* Addressable tab identifiers

**Out of Scope:**

* Editors
* Persistence beyond local state

---

## UI-006 — Cross-Cutting UI Services

**Purpose:**
Install foundational services used by all future UI phases.

**Scope:**

* Theme system
* Layout persistence (local)
* Notification surface
* Error boundary
* Loading / empty-state renderer
* Keyboard shortcut routing
* Command palette shell (no commands bound)

**Out of Scope:**

* Domain logic
* Runtime events
* WebSocket streams

---

## Explicit Non-Goals (Global)

No task in this inventory may:

* Call Librarian APIs
* Call Runtime APIs
* Bind WebSockets
* Implement mutation or write paths
* Implement permissions or roles
* Assume real data shape

---

## Completion Condition

PHASE-UI-FOUNDATION is complete when:

* All tasks UI-001 through UI-006 are completed and reviewed
* The UI feels structurally complete but functionally empty
* The only remaining work is **binding APIs and data**
