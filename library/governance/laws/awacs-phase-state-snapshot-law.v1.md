# AWACS Phase State Snapshot Law (v1)

## Purpose

Formalize a required, authoritative snapshot artifact to be created at the conclusion of each major phase or coherent functionality set, to support recovery, Guardian rehydration, and agent handoff.

---

## 1. Snapshot Requirement

* At the conclusion of each phase (or explicitly authorized functional milestone), a Phase State Snapshot MUST be created and registered.
* Execution of subsequent phases may proceed, but the snapshot must exist before recovery or Guardian rehydration is considered valid.

---

## 2. Snapshot Scope

Each snapshot MUST explicitly declare:

* Phase name and scope
* Completion status
* Frozen elements (what must not change)
* Active scope moving forward
* Explicitly out-of-scope items
* Authoritative seeds, contracts, and laws in effect
* Guardian enforcement posture

---

## 3. Authority and Mutability

* Phase State Snapshots are authoritative and immutable once registered.
* They do not replace seeds or contracts; they reference them.
* Later snapshots supersede earlier snapshots but do not invalidate them.

---

## 4. Storage Location

Snapshots must be stored under:

* /library/recovery/phase-snapshots/

---

## 5. Intended Consumers

* Guardian agents
* Human operators
* Recovery workflows
* Agent bootstrap sequences

---

## 6. Non-Goals

* Snapshots are not design docs, PR descriptions, or execution logs.
* They must not contain speculative future plans unless explicitly authorized.
