artifact_id: AWACS_UI_CHANGE_REVIEW_CHECKLIST
version: v1
kind: ui-process
domain: ui
scope: awacs
status: canonical
authority: product-architecture
mutability: read-only

# AWACS_UI_CHANGE_REVIEW_CHECKLIST

**Artifact ID:** AWACS_UI_CHANGE_REVIEW_CHECKLIST
**Version:** v1
**Kind:** UI Change Review Checklist
**Status:** Canonical
**Authority:** Product / Architecture

---

## 1. Purpose

This checklist defines the **mandatory review criteria** for any proposed change to the AWACS user interface.

Its purpose is to:

* Prevent unintended UI drift
* Enforce canonical intent
* Ensure consistency across human and AI contributions
* Catch violations *before* they enter the system

No UI change may be accepted unless all applicable checklist items pass.

---

## 2. Scope of Application

This checklist MUST be applied to:

* HTML structure changes
* CSS changes
* Figma-driven UI updates
* AI-generated UI proposals
* UI refactors and cleanups

---

## 3. Pre-Review Declaration

Before review begins, the proposer MUST declare:

* What artifact(s) the change affects
* Whether the change is:

  * Structural
  * Visual
  * Semantic
  * Corrective (bug fix)
* Whether the change introduces:

  * New affordances
  * New semantics
  * New decisions

If the change introduces a **new decision**, review MUST stop and a decision artifact must be created instead.

---

## 4. Canonical Alignment Checks

### CR-001 — State Alignment

* Does the change remain consistent with `AWACS_UI_STATE_REPORT.v1`?
* If reality changes, is a new state report required?

---

### CR-002 — Information Architecture Alignment

* Does the change preserve all semantic roles defined in `AWACS_UI_INFORMATION_ARCHITECTURE.v1`?
* Does it avoid redefining navigation, task context, detail panel, inspector, or status scopes?

---

### CR-003 — Operational Mode Compliance

* Does the change comply with `AWACS_UI_OPERATIONAL_MODE.v1`?
* Does it avoid introducing interaction, execution, or mutation?

---

### CR-004 — MVP Requirements Compliance

* Does the change satisfy `AWACS_UI_REQUIREMENTS_MVP.v1`?
* Does it avoid introducing MVP non-goals?

---

## 5. Interaction & Affordance Checks

### CR-005 — Affordance Discipline

* Does the change avoid implying capabilities that do not exist?
* Are visual cues consistent with declared non-interactive operation?

---

### CR-006 — Interaction Introduction Gate

* Does the change introduce any element that *could be perceived* as interactive?
* If yes:

  * Is this explicitly authorized by a decision artifact?
  * If not, the change MUST be rejected.

---

## 6. Semantic Integrity Checks

### CR-007 — No Implicit Semantics

* Does the change avoid introducing new meanings via styling, labels, or layout?
* Are all meanings traceable to existing artifacts?

---

### CR-008 — No Taxonomy Injection

* Does the change avoid introducing task states, workflows, progress models, or classifications not defined by a canonical artifact?

---

## 7. Figma & AI-Specific Checks

### CR-009 — Figma Constraint Compliance

* Was Figma used as an execution surface rather than an author of intent?
* Were changes constrained by existing canonical artifacts?

---

### CR-010 — AI Output Validation

* Was AI output reviewed against this checklist?
* Were hallucinated semantics or UI behaviors explicitly rejected?

---

## 8. Decision Boundary Enforcement

### CR-011 — Decision Detection

* Does the change *implicitly* answer a question that has not been formally decided?
* If yes, the change MUST be blocked and escalated to a decision artifact.

---

## 9. Approval Conditions

A UI change may be approved only if:

* All applicable checklist items pass
* No new decisions are introduced implicitly
* No canonical artifact is contradicted

Approval does **not** imply permanence; it implies compliance at the time of review.

---

## 10. Failure Handling

If a change fails review:

* The reason for failure MUST be documented
* The violated checklist item(s) MUST be cited
* The change MUST NOT be merged, applied, or released

---

## 11. Evolution

This checklist remains authoritative until superseded by a new version.

Changes to this checklist require a **decision artifact**, not an amendment.

---

**End of Canonical UI Change Review Checklist**
