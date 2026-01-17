# MVP Required Event Types (v0)

This document defines the minimal event taxonomy subset required for MVP execution, audit, and replay.

## Required (MVP MUST emit)

Lifecycle:

- system.run.started
- system.run.completed OR system.run.aborted (exactly one terminal)

Gateway:

- guardian.decision.recorded

Execution:

- engineer.started
- engineer.completed

Verification:

- qa.verification.passed OR qa.verification.failed (at least one MUST occur before completion; failed MAY lead to abort depending on mission rules)

## Optional (allowed in MVP but not required)

Lifecycle control:

- system.run.paused
- system.run.resumed

Progress:

- engineer.progress

System coordination:

- system.blocked
- system.escalation.required

Planning (if enabled by mission):

- pm.plan.created
- pm.plan.approved

## Out of scope (MVP MUST NOT require)

- Dynamic replanning / multi-plan negotiation events
- Concurrent multi-agent orchestration events
- Nested run / child-run lifecycle events
- Voting / multi-guardian consensus events
