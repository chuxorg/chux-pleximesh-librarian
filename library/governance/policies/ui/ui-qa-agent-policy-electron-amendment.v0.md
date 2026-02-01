# GOVERNANCE AMENDMENT — UI QA ELECTRON DEPENDENCY (v0)

## Purpose

Authorize the UI QA Agent to install the Electron runtime **solely** to enable execution of UI-QA smoke and structure tests.

This amendment is narrow, explicit, and non-expansive.

---

## Authorization

The UI QA Agent is authorized to:

* Install Electron as a **dev dependency** using:

  ```
  npm install -D electron
  ```
* Install related Electron runtime dependencies as required by Playwright
* Use the locally installed Electron executable for test execution

---

## Constraints (Reasserted)

The UI QA Agent is **not authorized** to:

* Modify application source code
* Commit or push changes
* Open or modify pull requests
* Change application behavior
* Introduce new dependencies beyond Electron required for testing

All changes remain local to the QA working copy.

---

## Scope Limitation

This authorization applies **only** to:

* UI-QA-001 smoke test execution
* UI-QA-002 zone integrity tests
* Future UI QA tasks that require an Electron runtime

No other agents or phases are affected.

---

## Intent

This amendment resolves a missing environmental precondition and does **not** alter governance boundaries, authority, or release rules.
