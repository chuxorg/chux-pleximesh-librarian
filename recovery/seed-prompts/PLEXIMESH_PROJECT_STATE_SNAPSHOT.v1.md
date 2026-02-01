# PLEXIMESH_PROJECT_STATE_SNAPSHOT.v1

## Status

Active, mid-development. Context intentionally externalized to prevent drift and context overload.

---

## Mission

PlexiMesh is an agent-oriented orchestration platform designed to make complex, cross-disciplinary work reliable, auditable, deterministic, and resilient to failure.

It treats **process as a first-class artifact**, with the same rigor applied to code.

---

## Core Principles (Frozen)

* Determinism over convenience
* Explicit intent beats emergent behavior
* Artifacts > chat memory
* Auditability is non-negotiable
* No silent state, no hidden decisions
* Agents must fail loudly and early

These principles MUST NOT be re-debated unless explicitly versioned.

---

## Architecture (High-Level)

* Multi-agent system (PM, Engineer, QA, Guardian, Librarian, etc.)
* AWACS runtime orchestrates agents and message flow
* Librarian is the canonical artifact store (append-only, versioned)
* Guardian enforces laws, invariants, and execution preconditions
* UI is Postman-like: inspectable, deterministic, audit-safe

---

## Current Focus

* Bringing minimal agents online
* Establishing reliable agent communication via AWACS
* Styling AWACS UI to a usable baseline
* Hardening process while development continues

---

## Locked Decisions

* No direct pushes to `master`
* Agents work from task-specific branches
* PM approves or rejects PRs
* Librarian artifacts are canonical and immutable once registered
* Documentation is isolated and low-risk (for now)
* Mermaid is an approved documentation tool (PlexiMesh-specific)

---

## Known Risks (Acknowledged)

* Context bloat → mitigated via snapshots + seeds
* Agent drift → mitigated via Guardian laws
* Over-documentation → intentionally avoided at this stage

---

## Recovery Assumption

Any future conversation MUST begin by loading:

* This snapshot
* Relevant role seed prompts
* Current task directive

No other prior chat context is assumed.
