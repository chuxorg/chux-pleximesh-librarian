# ENG-UI-001 — AWACS Application Shell (Postman-Style)

## Status
Planned

## Objective
Establish a visible, navigable AWACS UI shell modeled after the Postman application (not VS Code), providing immediate psychological presence and spatial structure without implementing real behavior or workflows.

This task focuses on form, layout, and affordances — not function.

---

## Design Reference (Authoritative)

The UI layout and interaction model should take inspiration from the Postman desktop application:

- Left icon rail for primary domains
- Secondary tree view navigator
- Central main content canvas with tabs
- Clean, operational, non-IDE feel

VS Code primitives may be reused only as implementation details, not as UX inspiration.

---

## In-Scope Deliverables

### 1. Application Frame (Shell)

The application MUST render with the following regions:

#### A. Left Icon Rail
- Vertical, icon-only
- Fixed width
- Visual selection state only
- No routing logic

Domains (icons only):
- Missions
- Event Streams
- Agents
- Policies
- Reports

---

#### B. Secondary Sidebar (Tree View)
- Positioned right of icon rail
- Contextual to selected domain
- Expandable tree structure
- Mocked / hardcoded data only

Example:


Missions
└─ UI Bootstrap
├─ Event Stream
├─ Agents
└─ Policies


---

#### C. Main Content Area
- Central, dominant canvas
- Static tabbed surfaces

Initial tabs:
- Overview
- Event Stream
- Agents
- Policies

Each tab contains placeholder panels with titles, badges, and mock metadata.

---

### 2. Tabs (Phase-0)

- Visual only
- Switching tabs swaps placeholder content
- No routing, no persistence, no deep state

Architectural note (not implemented):
The tab system should not preclude a future grid mode where tabs collapse into resizable tiles arranged in columns.

---

### 3. Visual Cues
- Section titles
- Status badges (ACTIVE, IDLE, MOCK)
- Clear spacing and hierarchy

All values may be mocked.

---

### 4. Theme
- Light theme only
- Neutral, clean palette
- No theming system required

---

## Explicit Non-Goals

The following are out of scope and MUST NOT be implemented:

- Backend or API calls
- Renderer changes
- State management
- Workflow execution
- Persistence
- Authentication
- Performance optimization

This task is shape-only.

---

## Allowed Scope (Paths)


src/ui/**
src/ui-shell/**
src/components/**
assets/**
styles/**
tests/ui/**


---

## Forbidden Scope


src/renderer/**
src/state/**
runtime/**
dev/**


Scope violations require declared exceptions per Engineer PR Policy.

---

## Acceptance Criteria

1. App loads and renders without errors
2. Postman-style layout is clearly recognizable
3. At least one mock Mission is visible
4. Tabs switch visible placeholder content
5. No backend/runtime dependencies exist
6. All changes remain within allowed paths

---

## PR Requirements
- Single atomic PR
- No scope exceptions expected
- Screenshots encouraged
- No opportunistic refactors

---

## Success Definition (Psychological)

A human opens the app and immediately thinks:

“Okay — this is a mission-control UI.”

 --- END ARTIFACT --- 
