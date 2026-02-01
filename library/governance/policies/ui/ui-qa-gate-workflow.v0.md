# UI QA & RELEASE GATE WORKFLOW (v0)

## Purpose

Define the authoritative workflow for **UI quality assurance, drift detection, and release approval**, enabling development and QA to proceed in parallel without loss of control or intent.

---

## Core Principle

**QA validates facts.
PM validates intent.
Release requires both.**

---

## Branch Model

* `feature/*` — Active engineering
* `qa/*` — QA validation snapshot
* `main` — Approved, released code

---

## Workflow

### 1. Engineering Completion

* Engineer completes a task set or phase
* Engineer opens a PR: `feature/* → qa/*`

---

### 2. PM Review (Pre-QA Gate)

* PM reviews PR for scope and intent
* PM may:

  * Approve → enter QA
  * Reject → return to Engineer

Upon approval, status becomes **QA-IN-PROGRESS**.

---

### 3. QA Execution

* UI Test Agent executes tests against `qa/*`
* Tests include:

  * Zone integrity
  * Resize behavior
  * Tab plane structure
  * Visual drift detection
* Results are recorded as QA artifacts

---

### 4. QA Failure Handling

If QA fails:

* UI Test Agent reports findings with evidence
* Task is marked **FAILED**
* PM reviews findings and decides:

  * Patch required → new task created
  * Intentional change → baseline updated
  * Defer → issue added to backlog

QA is factual, not discretionary.

---

### 5. QA Approval & Release

If QA passes:

* PM approves PR: `qa/* → main`
* Release proceeds
* QA baselines become authoritative

---

## Outcome

This workflow ensures:

* Continuous UI drift detection
* Parallel development and QA
* Clear ownership of intent vs validation
* Auditable release decisions

This gate is binding for all UI-related work.
