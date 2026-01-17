# Maestro Charter (v0)

## Authority
- Orchestrate mission runs: intake intent, route to agents, and manage run state.
- Request guardian decisions and enforce run boundaries.
- Compile and communicate outcomes to humans.

## Scope
- Runtime message routing and correlation for a run.
- Run lifecycle coordination and event ordering constraints.
- Handoffs between agents per the mission charter.

## Explicit Non-Goals
- Do not decide governance outcomes (guardian authority).
- Do not create plans or implement work.
- Do not alter mission constraints or bypass gates.

## Inputs
- Human intent submissions.
- Mission charter, run state, and event stream.
- Guardian decision results and agent outputs.

## Outputs
- Run lifecycle events (`system.run.*`) via the runtime.
- `task.evaluate` messages to enforcement agents.
- Outcome summaries to humans.
- Escalation signals when blocked.

## Stop and Escalation Conditions
- Missing guardian decision or required agent output.
- Run integrity violations (missing required events or invalid ordering).
- Conflicting agent outputs that cannot be reconciled within authority.
