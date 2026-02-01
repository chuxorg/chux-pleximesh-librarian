# UI RUNTIME VIEWER — TASK INVENTORY (v0)

## Execution Rules

* Tasks execute **sequentially**
* Authorization ≠ execution
* Each task requires:

  * Unit tests (where logic exists)
  * Build / lint / dependency reporting
* UI QA will run at phase completion

---

## UI-RT-001 — Runtime API Wiring (Read-Only)

**Purpose:**
Bind the UI to Runtime / AWACS **read-only APIs**.

**Scope:**

* Configure runtime API client
* Fetch agent status, execution state, runtime metadata
* Handle loading and error states

**Out of Scope:**

* Commands
* Mutations
* Polling control logic

---

## UI-RT-002 — Runtime Context Panel (Zone 2)

**Purpose:**
Render runtime entities (agents, executions, nodes) in the context panel.

**Scope:**

* Group runtime entities
* Selection and navigation
* Expand/collapse behavior

**Out of Scope:**

* Editing
* Reordering
* Control affordances

---

## UI-RT-003 — Runtime Viewer Tabs (Zone 3)

**Purpose:**
Display runtime views in read-only tabs.

**Scope:**

* Agent detail views
* Execution timelines
* Log / event stream viewers (read-only)

**Out of Scope:**

* Command execution
* Streaming control
* Write actions

---

## UI-RT-004 — Navigation & State Sync

**Purpose:**
Synchronize runtime context selection with open tabs.

**Scope:**

* Context selection opens/focuses tabs
* Tab focus updates context highlight
* Local UI state only

---

## UI-RT-005 — Safeguards, Tests, & Validation

**Purpose:**
Enforce read-only guarantees and correctness.

**Scope:**

* Remove or disable control affordances
* Unit tests for runtime views
* Build / lint / dependency checks
* Report warnings and deprecated usage

---

## Completion Condition

PHASE-UI-RUNTIME-VIEWER is complete when:

* Runtime data is visible and navigable
* All interactions are read-only
* Unit tests exist and pass
* Build/lint gates pass
* UI QA validates structure and behavior
