# CODEX PROMPT — IMPLEMENT AWACS LIBRARY UI (LIB-UI-1)

Role: Engineer Agent (CodeX)
Authority: Canonical (Human Architect)
Governing Law: PR_EXECUTION_LAW.v2
Scope: UI only
PR Policy: SINGLE PR for entire task

---

OBJECTIVE

Implement the AWACS Library UI (Phase LIB-UI-1) exactly as defined by the
CANONICAL FIGMA MAKE PROMPT — AWACS LIBRARY VIEW (FINAL).

This is a **read-only feature**.
No foundation changes are allowed.

---

INPUTS (AUTHORITATIVE)

1. Frozen AWACS shell (Zones 1–5)
2. Existing Yanzi theme, spacing, typography
3. Canonical Figma Make Prompt (FINAL)
4. Library UX Contract (LIB-UI-1)

If any ambiguity exists:

* STOP
* Ask for clarification
* Do NOT invent behavior

---

IMPLEMENTATION REQUIREMENTS

### Zone 2 — Library Tree

* Render tree structure visually
* Single-select state only
* No drag/drop
* No inline edits
* Wiring may be stubbed if backend unavailable

### Zone 3 — Artifact Viewer

* Implement framed viewport (not page)
* Render:

  * Header
  * Metadata strip
  * Content body
  * View toggle (Markdown / JSON)
  * Provenance indicator
* Everything must be read-only
* Viewer scrolls internally

### Zone 5 — Integration Rail

* Render disabled placeholders only
* No active behavior

---

EXPLICITLY OUT OF SCOPE

* Editing
* Mutations
* Diffing
* Agent actions
* Runtime integration
* Search beyond simple stubs
* Dark mode (handled later)

---

PR REQUIREMENTS

* Create ONE PR only
* Branch from dev
* UI-only changes
* No foundation refactors
* No renderer architectural changes unless unavoidable
  (If unavoidable, STOP and explain)

PR description must include:

* Summary of implementation
* Explicit statement: “Read-only Library UI (LIB-UI-1)”
* Confirmation of single-PR policy

---

VERIFICATION

* App builds
* App launches
* No regressions in existing UI
* Library view renders correctly with stub data

---

FAILURE CONDITIONS

If you cannot comply exactly:

* STOP
* Report the blocker
* Do not proceed
