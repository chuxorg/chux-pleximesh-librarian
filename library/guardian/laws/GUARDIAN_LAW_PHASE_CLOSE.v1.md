# Guardian Law — Phase Close (v1)

## Status

Constitutional Law
Enforced by Guardian
Effective Immediately

---

## Title

Phase Close Law

## Summary

At the end of every phase, publish a new authoritative snapshot, archive prior snapshots, and update recovery seeds; agents must not auto-load archived snapshots.

---

## Law

1. At phase close, the system MUST create a new `PLEXIMESH_PROJECT_STATE_SNAPSHOT.v(N+1)` that is declarative and canonical.
2. The new snapshot MUST explicitly override prior UI context and become the sole authoritative snapshot for its scope.
3. All prior snapshots MUST be marked **Archived** and **Non-authoritative** (retained for audit only).
4. All recovery seeds MUST be updated to reference the newest snapshot:

   * `MASTER_SEED_PROMPT.*`
   * `PANIC_PROMPT.*`
   * `AWACS_UI_CONTEXT_SEED.*`
5. Agents MUST NOT reason across archived snapshots unless explicitly instructed to load a specific archived version.
6. The Librarian MUST record checksum + canonical path + active pointer for every snapshot and phase-close action.

---

## Applicability

This law is required at the end of every phase and applies to all agents.
