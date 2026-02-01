# UI QA ASSIGNMENT MESSAGE (v0)

## Purpose

Provide a **standard, unambiguous assignment message** used by the PM to hand work off to the UI QA Agent after a UI pull request has been approved and merged.

This message ensures the QA Agent:

* Knows exactly what to test
* Knows which branch to test
* Knows which tasks are in scope
* Does not guess intent or scope

---

## QA ASSIGNMENT MESSAGE TEMPLATE

**Assignment:** UI QA Execution

**Branch to Test:**
`dev` (or explicitly specified `qa/*` branch)

**Authorized Phase:**
`PHASE-UI-QA-FOUNDATION v0`

**Tasks in Scope:**

* UI-QA-001 — Playwright Harness Setup (if not already completed)
* UI-QA-002 — Zone Integrity Tests

**Preconditions:**

* PR(s) for the listed task(s) have been approved by PM
* PR(s) have been merged into the specified branch
* No additional feature work is included

---

### Instructions to UI QA Agent

You are authorized to:

1. Clone the repository fresh
2. Check out the specified branch
3. Install dependencies
4. Execute QA tasks strictly as defined
5. Produce QA result artifacts (PASS / FAIL with evidence)

You are **not authorized** to:

* Modify application source code
* Commit or push changes
* Open or update pull requests
* Expand scope beyond listed tasks

---

### Reporting Requirements

Upon completion, report:

* Task status (PASS / FAIL)
* Evidence for any failures (logs, screenshots, diffs)
* Any blocking issues that prevent execution

Stop after reporting results and await PM disposition.

---

## Usage Notes

* This message is issued **only after PM approval**
* This message represents **execution authorization**, not intent discussion
* Any deviation from scope must be escalated, not assumed
