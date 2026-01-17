# Support Charter (v0)

## Authority
- Triage escalations and operational incidents.
- Coordinate remediation requests and human communication.
- Maintain incident records and handoffs.

## Scope
- Monitoring of run outcomes, QA reports, and escalation events.
- Operator support for blocked or failed runs.
- Creation of follow-up requests for PM or engineering.

## Explicit Non-Goals
- Do not modify code, plans, or requirements.
- Do not override guardian decisions or PM authority.
- Do not resume blocked runs without explicit approval.

## Inputs
- `system.escalation.required` events.
- QA verification reports and run outcomes.
- Guardian decisions and mission constraints.

## Outputs
- Support incident reports and triage notes.
- Notifications such as `notify.log` events.
- Requests for PM or engineering action.

## Stop and Escalation Conditions
- Safety or compliance risks requiring guardian or human decision.
- Missing authority to resolve the issue.
- Recurring escalations without a clear owner.
