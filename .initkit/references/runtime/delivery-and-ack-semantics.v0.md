---
artifact_type: reference
name: delivery-and-ack-semantics
version: v0
scope: runtime
status: observational
---

# Runtime Delivery and ACK Semantics (v0)
This document captures the observed runtime behavior for fan-out Task.Created delivery and acknowledgement semantics as of version 0.

## Definitions
- **Broadcast:** A delivery pattern where an event is emitted without expectation of acknowledgement, primarily intended for passive listening. Broadcast does not imply any ownership or competitive consumption.
- **Fan-out:** A delivery scope where the runtime sends the same event payload to multiple subscribed agents, expecting at least one acknowledgement to satisfy delivery. In PlexiMesh, fan-out includes ACK tracking and therefore differs from broadcast.

## Observed Behavior (Live-Fire)
- Fan-out delivers the same Task.Created event instance to every subscriber within scope.
- The runtime maintains a single authoritative ACK record per event.
- The first ACK received is accepted and marks the delivery as satisfied.
- Subsequent ACK attempts fail with a visible error, indicating the ACK window is already closed.
- Despite ACK failures, all subscribers may still process the event locally or continue their own workflows; only the ACK state is rejected.

## Implications
- Fan-out currently behaves as competitive consumption: only the agent that ACKs first establishes ownership in the ledger.
- Agents cannot assume ownership or downstream authority unless they are the first to ACK the event.
- An ACK failure does **not** imply the execution itself failed; it only reflects that another agent already satisfied delivery.

## Non-Goals
- This reference does not propose runtime changes or enhancements.
- It does not define future guarantees or backward compatibility promises.
- It does not prescribe how agents must behave in response to fan-out events.

## Rationale
Documenting the current semantics prevents accidental drift and ensures Guardians, agents, and AWACS share the same understanding of how fan-out behaves today. Future changes must be explicitly versioned so downstream consumers can align their prompts, escalation paths, and evidence handling with the updated guarantees.
