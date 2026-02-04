# PHASE_OPEN_SEED_DELTA.v1 — Guardian Workbench

## Purpose

Ensure that all future recoveries, rehydrations, and new conversations **open directly into the Guardian Workbench context** when the active phase is **PHASE-GUARDIAN-WORKBENCH**.

This delta modifies *startup orientation*, not system behavior.

---

## Applicability

This seed delta applies when:

* Active Phase = `PHASE-GUARDIAN-WORKBENCH.v1`
* Active Snapshot = `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`

---

## Injection Order (Mandatory)

When starting a new conversation or recovery flow, inject **in this order**:

1. `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v2`
2. `LLM_MEMORY_CONTRACT.v1`
3. `AWACS_UI_CONTEXT_SEED.v1`
4. `PHASE-GUARDIAN-WORKBENCH.v1`
5. `GUARDIAN_LAW_PHASE_CLOSE.v1`
6. **This seed delta**

---

## Behavioral Directive

From conversation start:

* Assume **Guardian Workbench** is the primary operating context.
* Treat ChatGPT / Atlas as:

  * advisory
  * non-authoritative
  * stateless beyond injected artifacts
* All Guardian authority must be derived from:

  * active snapshot
  * phase artifact
  * guardian laws
* Do not infer Guardian state from prior conversations.
* Do not reason across archived snapshots unless explicitly instructed.

---

## UI Orientation Hint (Non-binding)

If a UI is present:

* Default view should surface **Guardian Workbench**
* Show:

  * Active Snapshot
  * Active Phase
  * Guardian Laws
* Hide or de-emphasize execution or runtime surfaces unless explicitly requested.

---

## Non-Goals (Explicit)

* This delta does not add execution semantics.
* This delta does not authorize state mutation.
* This delta does not change Librarian rules.
* This delta does not replace Phase Close Law.

---

## Canonical Rule

Guardian continuity is achieved through **artifact selection**, not conversational memory.
