# PHASE — Library Hardening (Authoritative Intent System)

## Status

Active

## Purpose

Harden the Librarian and Library architecture so that **intent artifacts are authoritative, immutable, and unambiguous**, even for MVP demos.

This phase establishes the Librarian (API + persistence) as the **single source of truth** for all governance, task, and policy artifacts. Filesystem-based libraries are demoted to seed-only or human-reference roles.

---

## Problem Statement

The current directory-based library model introduces ambiguity and drift:

- Agents depend on filesystem layout and repo state
- Branch or checkout mismatches cause artifact discovery failures
- Multiple “copies” of intent emerge (disk vs git vs agent memory)
- Demos become non-deterministic across environments

This phase resolves these issues by formalizing **authoritative artifact storage and retrieval**.

---

## Core Invariants (Non-Negotiable)

1. **Authoritative Source**

   - The Librarian API backed by persistent storage is the sole authority for artifacts.
   - Agents MUST NOT read authoritative artifacts from disk.

2. **Immutability**

   - Artifacts are immutable once versioned.
   - Changes require new versions with explicit reasons.

3. **Addressability**

   - All artifacts are retrieved by stable identity:
     - `artifact_id`
     - `kind`
     - `version`

4. **Auditability**

   - Every artifact mutation is recorded as an append-only event.

5. **Determinism**
   - Given the same Librarian state, agent behavior is repeatable and environment-independent.

---

## Scope

### In Scope

- Canonical artifact data model
- Librarian REST API (read-first)
- Persistent storage (MongoDB or equivalent)
- Seed import/export mechanism
- Agent contract for artifact retrieval

### Out of Scope (for this phase)

- Multi-tenant permissions
- User-defined workflow views
- Advanced search or indexing
- UI integration beyond basic consumption

---

## Filesystem Role (Post-Hardening)

The repository filesystem MAY contain:

- Seed artifacts
- Migration scripts
- Schemas
- Human-readable references

The filesystem MUST NOT be treated as authoritative at runtime.

---

## Exit Criteria

This phase is complete when:

1. At least one task artifact (e.g., ENG-UI-001) is served authoritatively via the Librarian API.
2. Agents retrieve tasks and policies exclusively via API calls.
3. No agent execution depends on filesystem library traversal.
4. Artifact identity, versioning, and audit history are verifiable.

---

## Rationale

This phase is required even for MVP:

- Demo reliability depends on deterministic intent
- Agent governance cannot be probabilistic
- UI execution must consume hardened intent, not fragile files

The Library Hardening Phase enables safe continuation of product development.
