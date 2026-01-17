# Run Abort Semantics (v0) — MVP Locked Contract

## Definition

A run is ABORTED when the system terminates execution before reaching a normal completion boundary, due to a hard stop condition (safety, policy, invariant violation, or explicit termination).

ABORTED is a terminal lifecycle state and MUST be represented only by the system lifecycle event:

- system.run.aborted

The event:

- system.run.completed MUST NOT represent ABORTED via any outcome value.

## Required triggers (MVP)

The system MUST emit system.run.aborted when any of the following occurs:

1. Guardian decision result == REJECT (hard gate failure)
2. A runtime invariant is violated (e.g., events after terminal, missing required gate, illegal transition)
3. A non-recoverable system failure occurs
4. A human explicitly terminates the run

Guardian decision result == REVISE MUST block forward progress, but MUST NOT abort the run.

## Required abort payload fields (MVP minimum)

system.run.aborted payload MUST include:

- reason_code: one of {GUARDIAN_REJECT, INVARIANT_VIOLATION, SYSTEM_FAILURE, HUMAN_TERMINATION, TIMEOUT}
- reason: human-readable description
- initiator: {guardian, system, human, agent, tool}
- at_state: {CREATED, STARTED, PAUSED}
- at_sequence: integer (the last known emitted sequence OR the sequence of the abort event)
- last_event_id: the last causal/preceding event id if available
- recoverable: boolean
- evidence_refs: optional references to related artifacts/events (e.g., guardian decision event)

## Guardian coupling (MVP)

If guardian.decision.recorded has decision.result == REJECT:

- The system MUST emit system.run.aborted
- reason_code MUST be GUARDIAN_REJECT
- evidence_refs MUST include the guardian decision event_id

## Post-conditions

After system.run.aborted is emitted:

- No further events may be emitted for the run_id.
