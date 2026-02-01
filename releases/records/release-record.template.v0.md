# Release Record — Template

## Purpose

This document defines the **canonical record format** for an AWACS (Yanzi) release.

A Release Record captures an **immutable snapshot** of system state at the time a release is declared and authorized.
It is descriptive, not procedural, and may include known limitations.

---

## Release Metadata

* **Release Name:**
* **Version:** (e.g. v0.1, v0.2, v1.0)
* **Release Date:** (ISO 8601)
* **Release Type:**

  * internal
  * milestone
  * experimental
  * external

---

## Code Reference

* **Repository:**
* **Branch:**
* **Commit SHA(s):**
* **Tag (if any):**

---

## Canonical Library Snapshot

* **Library Snapshot ID:**
* **Artifact Set Included:**

  * (list of artifact IDs or references)
* **Policies / Laws in Effect:**

  * (list of policy IDs)

---

## UI Foundation State

* **UI Surface Version / Commit:**
* **UI Contract Version:**
* **UI Scope Notes:**
* **Known UI Limitations:**

---

## Runtime State

* **Runtime Version / Commit:**
* **Runtime Constraints:**
* **Known Runtime Limitations:**

---

## QA Certification

* **QA Status:**

  * certified
  * certified with known issues

* **QA Scope Covered:**

  * (brief description)

* **Known Open Violations:**

  * Violation ID
  * Description
  * Scope (UI / Runtime / Policy / Other)
  * Accepted by Guardian (yes / no)

---

## Guardian Authorization

* **Authorization Status:** approved / rejected
* **Authorizing Guardian:**
* **Authorization Timestamp:** (ISO 8601)
* **Risk Acceptance Notes:**

---

## Release Notes (Optional)

* Intent of this release
* Notable changes
* Explicit non-goals

---

## Immutability & Audit Notice

Once recorded and registered, this Release Record is **read-only**.

Any modification or correction requires creation of a **new Release Record**.

This record is intended to support auditability, traceability, and future automation.
