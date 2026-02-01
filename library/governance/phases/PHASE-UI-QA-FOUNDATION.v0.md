# PHASE-UI-QA-FOUNDATION (v0)

## Purpose

Establish a **UI Quality Assurance foundation** whose primary function is to **detect and prevent unintended UI drift** after the UI shell geometry has been locked.

This phase introduces an automated **UI Test Agent** that enforces *structural intent*, not feature correctness.

---

## Core Principle

**The UI Test Agent is a drift sentinel, not a feature tester.**

Its role is to continuously answer:

> “Did the UI change in a way that was not explicitly intended?”

---

## Scope

This phase covers:

* Selection and setup of a UI testing framework suitable for Electron-based UIs
* Establishment of a deterministic test harness
* Encoding **structural UI invariants** as automated tests
* Capturing and managing **visual and geometric baselines**
* Defining a workflow for distinguishing:

  * Intentional UI change
  * Accidental UI drift

---

## Explicit Focus Areas

### 1. Structural Zone Integrity

The UI Test Agent must validate the continued existence and geometry of:

* Zone 1 — Application Menubar (Top Shell)
* Zone 2 — Left Control Plane (Navigation + Context)
* Zone 3 — Main Content Plane
* Zone 4 — Status Bar

Tests must assert:

* Zone presence
* Edge-to-edge alignment
* Correct boundary relationships
* Resize behavior where applicable

---

### 2. Tab Plane Structure

The UI Test Agent must verify that:

* The tab strip defines the top boundary of Zone 3
* Tabs resize with the main content plane
* No competing headers intrude into the tab plane

---

### 3. Visual Baseline Management

The phase must establish:

* A baseline set of UI screenshots or snapshots
* A mechanism for detecting visual diffs
* A documented process for updating baselines **only when change is intentional**

---

## Out of Scope

This phase explicitly does **not** include:

* Feature-level UI testing
* Business logic validation
* Data correctness assertions
* Backend or API testing
* Performance or load testing
* Styling, branding, or polish decisions

---

## Drift Governance Model

* If UI structure or visuals change **without explicit intent being declared**, the UI Test Agent must fail.
* If intent is declared (e.g., “visual change expected”), the agent may:

  * Accept the change
  * Update the baseline
  * Continue monitoring from the new reference point

This preserves **intent alignment** over time.

---

## Phase Outcome

Upon completion of PHASE-UI-QA-FOUNDATION:

* The UI has an automated sentinel guarding its structure
* UI regressions are detected early
* Visual and geometric drift becomes observable and auditable
* Future UI phases proceed with confidence

This phase is a **permanent guardrail**, not a one-time effort.
