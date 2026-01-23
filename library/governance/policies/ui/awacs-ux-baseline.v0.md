# AWACS UX Baseline Policy v0

**Status:** Canonical
**Applies to:** All AWACS UI work
**Enforced by:** PM, Guardian, UI Test Agent

---

## 1. Purpose

This policy defines the **non-negotiable UX and interaction baseline** for AWACS.

AWACS is **not an IDE**, but it must feel like a **professional workstation** on par with VS Code in:

- stability
- predictability
- comfort
- performance
- trustworthiness

This policy exists to prevent UI drift, accidental “web-app jank,” and irreversible UX regressions.

---

## 2. Core UX Principles (Must Always Hold)

### 2.1 No Invented State

- AWACS **must never fabricate or infer system state**.
- Every fact shown in the UI must trace directly to:

  - a persisted artifact
  - an event
  - an explicit absence (“missing”, “unknown”, “not recorded”)

If something is not known, it must be **shown as unknown**, not guessed.

---

### 2.2 Deterministic Rendering

- Given the same artifacts and events, AWACS must render **the same UI**.
- Ordering must be explicit:

  - Prefer explicit sequence numbers when available
  - Otherwise use timestamp + stable tiebreaker

- UI must not rely on incidental DOM order.

---

### 2.3 Read-Only Authority (This Phase)

- AWACS is **observational** in this phase.
- No mutation of runtime, Librarian, or external systems.
- Any future control actions must be introduced by a **separate, explicit phase**.

---

## 3. Workbench Layout (Non-Negotiable)

AWACS must present a **fixed workbench layout**, inspired by VS Code:

### Required Regions

1. **Activity Bar** (left, icons)
2. **Side Bar** (trees/lists)
3. **Main Surface Area** (primary content)
4. **Bottom Panel** (logs, telemetry, diagnostics)
5. **Status Bar** (connection state, run id, mode)

### Layout Rules

- Panes are:

  - resizable
  - dockable
  - collapsible

- Layout state must persist across restarts.
- No full-screen modal workflows for primary navigation.

---

## 4. Interaction Rules

### 4.1 Keyboard-First Friendly

- All primary navigation must be accessible without a mouse.
- A **Command Palette** must exist (even if minimal initially).
- Keyboard shortcuts must be discoverable.

---

### 4.2 Navigation Discipline

- No blocking spinners for read-only data.
- Progressive disclosure is preferred:

  - list → select → detail

- Back/forward navigation should feel natural and reversible.

---

### 4.3 Surface Discipline

- AWACS is composed of **Surfaces**:

  - Run Explorer
  - Timeline Stepper
  - Artifact Viewer
  - Mission Rail
  - Governance Views (later)

- Surfaces must be:

  - independently testable
  - independently renderable
  - free of hidden cross-dependencies

---

## 5. Visual & Interaction Quality Bar

### 5.1 Visual Rules

- Dark theme is first-class; light theme supported.
- Typography and spacing must be consistent.
- Avoid:

  - layout jumps
  - scroll snapping surprises
  - flicker during data updates

This must not “feel like a web demo.”

---

### 5.2 Performance Rules

- Large lists (runs, events, artifacts) must be virtualized.
- Rendering must be incremental.
- Selection changes must not cause full re-renders.

Performance regressions are **UX regressions**.

---

## 6. Testability Requirements (Hard Requirement)

To support the UI Test Agent:

- Every surface must expose stable `data-testid` attributes.
- UI state transitions must be observable without timing hacks.
- Missing data must produce **explicit UI markers** that can be asserted.

If a UI cannot be tested deterministically, it is considered **out of compliance**.

---

## 7. Enforcement

### PM Responsibilities

- Reject PRs that violate this policy.
- Require waivers for any deviation (with expiration).

### Guardian Responsibilities

- Block PRs that:

  - invent state
  - weaken determinism
  - introduce modal or blocking flows
  - degrade workstation layout guarantees

### UI Test Agent Responsibilities

- Fail tests if:

  - layout contracts break
  - deterministic rendering is violated
  - missing data is hidden or fabricated

---

## 8. Waivers

Any violation of this policy requires a **formal waiver artifact**:

```
library/governance/decisions/waivers/<date>-awacs-ux-<slug>.v0.md
```

Waivers must include:

- rationale
- scope
- rollback plan
- explicit expiration condition

“No time” is not a valid justification.

---

## 9. Success Criteria

AWACS is considered compliant when:

- Users trust what they see.
- The UI feels stable and predictable.
- Engineers can iterate rapidly without UX debt.
- Tests can assert correctness without flakiness.

This policy is intentionally strict.
Comfort and trust are features.
