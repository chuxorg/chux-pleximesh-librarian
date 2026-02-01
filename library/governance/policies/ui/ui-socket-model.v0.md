# UI SOCKET MODEL — CANONICAL FOUNDATION (v0)

## Purpose

Define the authoritative, feature-agnostic structural model for the PlexiMesh user interface.

The UI is governed as a system of **stable sockets** into which future functionality may be bound without restructuring the application.

---

## Core Law

**The PlexiMesh UI does not implement features.
It exposes sockets.
Features bind to sockets in later phases.**

This law is binding across all UI work.

---

## Definition: UI Socket

A **UI Socket** is a named, addressable region of the UI that:

* Emits user intent
* Accepts feature bindings
* Does not encode business logic
* Does not imply data authority
* May be empty by design

Empty sockets are **intentional and first-class**.

---

## Socket Taxonomy (Authoritative)

### 1. Application Frame Sockets (Always Present)

#### 1.1 Window Menu Socket

* OS-level menu surface (File | Edit | View | Navigate | Window | Help)
* Emits application-level intent only
* Never owned by a feature

#### 1.2 Global Toolbar Socket

* Global search
* Profile / identity surface
* Workspace selector
* Theme selector
* Global status indicators

This socket is context-agnostic.

---

### 2. Primary Navigation Socket (Far-Left Rail)

* Declarative, dynamic list
* Maps entries to Workspace Sockets
* Does not encode feature semantics

Primary Navigation is structural, not functional.

---

### 3. Workspace Socket (One Active at a Time)

Each Workspace Socket owns:

#### 3.1 Context Panel Socket

* Trees
* Filters
* Secondary navigation
* Scoping controls

Optional but reserved.

#### 3.2 Main Content Socket

* Hosts the Tab Manager Socket
* Never renders feature content directly

---

### 4. Tab Manager Socket

* Manages addressable, restorable tabs
* Tabs host View Sockets
* Feature-agnostic

---

### 5. View Socket (Leaf-Level)

The only socket where feature UI appears.

Examples:

* Artifact viewer
* Workflow editor
* Agent interaction surface
* Dashboard
* Visualization

View Sockets:

* Receive context
* Emit intent
* Own no authority

---

## Cross-Cutting Service Sockets

Always present, non-visual infrastructure:

* Theme system
* Layout persistence
* Command palette
* Notification surface
* Error boundaries
* Loading / empty state renderer
* Keyboard routing

---

## Phase Binding Rules

Each future phase must declare:

* Which Primary Navigation entry it occupies
* Which Workspace Socket it binds
* Which View Sockets it provides

No phase may:

* Restructure the Application Frame
* Remove or repurpose sockets
* Introduce hidden coupling between sockets

---

## Explicit Non-Goals

This canon does not define:

* Backend APIs
* Permissions models
* Business logic
* Feature prioritization
* Data ownership

---

## Canonical Outcome

This model guarantees:

* Zero ambiguity in UI structure
* Infinite extensibility without refactor
* Clear separation between structure and capability
* Protection against stakeholder-driven architectural erosion

**This artifact is binding.
All PlexiMesh UI work must conform to it.**
