---
artifact_type: governance
rule_name: qa_escalation_rule
version: v1
owner: guardian
scope: process
effective_date: 2025-12-21
---

## Rule
QA operates as a decision gate with a maximum dwell time of one sprint. Every slice entering QA exits with an explicit Guardian-owned decision.

## Decision Outcomes
- **Approve:** QA signs off, recording evidence and allowing downstream closure.
- **Reject with reason:** QA documents the blocking issue(s) and returns the slice to engineering remediation.
- **Explicitly defer:** QA records why the decision cannot be made within the sprint and escalates to the Guardian for next-step instructions.

If QA activity exceeds one sprint without a decision, the Guardian must intervene and either defer or reject; “waiting” is not an acceptable steady state.

## Rationale
Treating QA as a binary decision point prevents work from idling in a quasi-complete state, keeps accountability with the Guardian, and ensures that acceptance evidence is timely. This protects the integrity of the Librarian’s records while keeping the delivery loop tight.
