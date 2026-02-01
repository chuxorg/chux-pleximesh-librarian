# +LLM Memory Contract v1

## Purpose

Define explicit, non-ambiguous rules governing how Large Language Models (LLMs) are treated with respect to memory, context, persistence, and authority within PlexiMesh.

This contract exists to eliminate false assumptions about LLM memory and to ensure system survivability under failure.

---

## Fundamental Assertion

LLMs are treated as **stateless compute units**.

Any appearance of memory is:

* Ephemeral
* Non-authoritative
* Non-deterministic
* Not relied upon for correctness

---

## Memory Sources (Ordered by Authority)

### 1. Explicitly Injected Context (Authoritative)

Includes:

* Current conversation messages
* Pasted artifacts
* Seed prompts
* Project State Snapshots
* Role definitions

This is the ONLY trusted memory source.

---

### 2. External Canonical Storage (Authoritative)

Includes:

* Librarian-managed artifacts
* Versioned files
* Checksummed records

LLMs do NOT retain this memory.
It must be explicitly re-injected.

---

### 3. System/User Memory (Non-Authoritative)

May include:

* High-level summaries
* Behavioral preferences
* Past interaction hints

This memory:

* Is incomplete
* Is lossy
* May be absent
* MUST NOT be relied upon for system behavior

---

## Prohibited Assumptions

LLMs MUST NOT be assumed to:

* Remember prior conversations
* Recall decisions unless restated
* Maintain project state across chats
* Coordinate state implicitly
* Act consistently without explicit constraints

---

## Required Design Rules

1. All critical state MUST live outside the LLM.
2. Every conversation MUST be disposable.
3. Recovery MUST be possible using stored artifacts alone.
4. No task may depend on implicit recall.
5. Ambiguity MUST halt execution.

---

## Drift Prevention

To prevent semantic or procedural drift:

* Conversations are phase-bounded
* Future speculation is isolated into separate conversations
* Guardian may enforce rollovers
* Snapshots are regenerated as needed

---

## Failure Model

The system MUST assume:

* Chats will terminate unexpectedly
* Context will be lost
* Agents will forget
* Models will change
* Outputs may vary

Survivability is defined as the ability to resume deterministically after any such failure.

---

## Compliance

Any workflow, agent, or process that violates this contract is considered UNSAFE and MUST be halted by the Guardian.
