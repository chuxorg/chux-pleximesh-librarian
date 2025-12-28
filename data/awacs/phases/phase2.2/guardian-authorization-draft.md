# Phase 2.2 — Interaction Semantics & Input Handling

## Phase
2.2

## System
AWACS (chux-pleximesh-awacs)

---

## Phase Intent
Phase 2.2 introduces interaction semantics to the Mission Rail without altering system doctrine, authority, telemetry meaning, or backend behavior.

This phase defines how humans interact with existing structure, not what actions the system performs.

The goal is to establish a deterministic, observable interaction grammar that future phases may safely extend.

---

## Authorized Scope

### 1. Selection Model
- Introduce a single authoritative selection state:
  - Selected group
  - Selected mission
- Selection must be:
  - Explicit
  - Observable
  - Represented as plain data
- Selection must not trigger execution or side effects.

### 2. Focus Model
- Define keyboard focus traversal: Mission Rail → Group → Mission.
- Focus must:
  - Be distinct from selection
  - Be visually observable
- Mouse and keyboard interactions must converge on the same focus model.

### 3. Keyboard Navigation
- Implement non-destructive keyboard navigation (arrow keys, Tab/Shift+Tab).
- Navigation may move focus or expand/collapse groups.
- Navigation must not execute commands, mutate Mission Rail doctrine, or change telemetry semantics.

### 4. Action Compass Hook (Non-Executing)
- Wire a placeholder Action Compass invocation.
- Allowed behaviors: open/close, populate contextual read-only cards.
- Forbidden behaviors: command execution, backend/IPC calls, policy enforcement, authority checks.

---

## Explicitly Forbidden (Hard Constraints)
- No Mission Rail doctrine changes
- No grouping or registry changes
- No telemetry semantic changes
- No backend or IPC command execution
- No UX polish (styling, theming, animation)
- No new policy, authority, or permission logic

Any need to violate these constraints requires a new Guardian gate.

---

## Execution Contract
- Branch from `dev`
- One task branch per slice
- Commit and push after every prompt
- Pull request targeting `dev`
- No self-merges
- dev → qa → master flow unchanged
- All prompts, responses, and artifacts must be persisted
- Every PR must cite the Phase 2.2 Guardian authorization

---

## Acceptance Criteria
Phase 2.2 is complete when:
- A user can navigate the Mission Rail entirely via keyboard
- Focus and selection states are separate, deterministic, and observable
- The Action Compass opens contextually without executing actions
- No Mission Rail logic, grouping, or telemetry behavior is modified

---

## Guardian Review Checklist
- Interaction must not alter system meaning
- Focus must not imply authority or execution
- Selection must not trigger behavior
- All interactions must be reversible and non-destructive

---

## Governing Canon
- AWACS NFR Charter
- Persistence Law
- Phase 1 Mission Rail Canon
- Phase 2.0 and Phase 2.1 Guardian Decisions

---

## Next Step
This document must be reviewed by the Guardian. The Guardian shall issue a PASS, BLOCK, or ESCALATE decision and persist it under `central-librarian://awacs/phases/phase2.2/review/guardian-decision.md`.
