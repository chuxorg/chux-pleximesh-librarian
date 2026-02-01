# UI LIBRARY VIEWER — TASK INVENTORY (v0)

## Execution Rules

* Tasks execute **sequentially**
* Authorization ≠ execution
* Each task produces a completion report
* UI QA is rerun at phase completion

---

## UI-LIB-001 — Librarian API Wiring (Read-Only)

**Purpose:**
Connect the UI to the Librarian Read API.

**Scope:**

* Configure API client
* Fetch artifact lists
* Fetch artifact details by ID/version
* Handle errors and loading states

**Out of Scope:**

* Writes
* Mutations
* Caching as authority

---

## UI-LIB-002 — Library Context Panel (Zone 2)

**Purpose:**
Render a navigable Library tree in the context panel.

**Scope:**

* Artifact grouping
* Expand/collapse tree
* Selection handling

**Out of Scope:**

* Editing
* Drag/drop
* Reordering

---

## UI-LIB-003 — Artifact Viewer Tabs (Zone 3)

**Purpose:**
Display Library artifacts in read-only tabs.

**Scope:**

* Open artifact in tab
* Render structured content (JSON / Markdown)
* Handle multiple open artifacts

**Out of Scope:**

* Editing
* Saving
* Version creation

---

## UI-LIB-004 — Navigation & State Sync

**Purpose:**
Synchronize context panel selection with tab state.

**Scope:**

* Click in tree opens tab
* Tab focus highlights tree selection

**Out of Scope:**

* Deep linking
* URL routing

---

## UI-LIB-005 — Read-Only Safeguards

**Purpose:**
Ensure the UI cannot accidentally mutate canonical state.

**Scope:**

* Remove / disable any write affordances
* Explicit read-only indicators
* Guardrails in UI logic

---

## Completion Condition

PHASE-UI-LIBRARY-VIEWER is complete when:

* The Library can be browsed end-to-end
* Artifacts render accurately
* UI remains read-only
* No structural zones are violated
* UI QA passes against the new bindings
