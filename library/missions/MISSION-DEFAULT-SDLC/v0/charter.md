# Mission Charter: MISSION-DEFAULT-SDLC (v0)

## Authority
- Define the allowed SDLC flow for this mission.
- Establish required agents and handoffs.
- Set constraints for run execution and escalation.

## Scope
- Requirements to planning to implementation to verification to outcome reporting.
- Single mission run with MVP event taxonomy requirements.
- Governance laws and guardian decisions applied to all stages.

## Explicit Non-Goals
- Not a multi-mission orchestration or dynamic replanning model.
- Not a governance override or runtime behavior change.
- Not a substitute for project-specific charters or prompts.

## Inputs
- Human intent submissions and requirements artifacts.
- Governance laws and guardian decisions.
- Agent charters, plans, and work orders.
- Runtime event stream.

## Outputs
- Mission outcomes and run reports.
- Required MVP events: `system.run.*`, `guardian.decision.recorded`, `engineer.*`, `qa.verification.*`.
- Escalation signals when blocked or non-compliant.

## Stop and Escalation Conditions
- Guardian decision is REJECT or REVISE.
- Required events missing or run state invalid.
- Human intervention required per mission constraints.
