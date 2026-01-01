# PlexiRT Testing Agent Specification (v0)

## Role and Responsibilities
- Continuously runs end-to-end mission scenarios against the live PlexiRT runtime without mocking or modifying agents under test.
- Confirms that runtime behavior, contracts, and observability remain intact (events, gating, tool usage, artifacts).
- Does **not** perform unit/component tests, does **not** stub or patch agents, and does **not** enforce business outcomes—it only detects deviations.

## Test Input Generation
- Builds AI-assisted, bounded prompts from existing artifacts (mission definitions, execution plans, prior outcomes) so scenarios mirror realistic human intents.
- Prompts must be concise, tied to known missions/tools, and issued through the normal Maestro channel (producing `intent.submission` messages).

## Observation Model
- Subscribes to runtime events: `system.run.*`, `execution.gate.*`, tool invocation request/result, Maestro guidance, Guardian decisions, outcome summaries.
- Watches state transitions purely via the event bus; correlates using `run_id`, `step_id`, correlation IDs.
- Reads canonical artifacts (`guardian-decision`, `run-outcome`, `run_state.v0`, testing reports) via read-only access to persistence (e.g., Mongo, log stores).

## Invariants and Checks
- Required per run: `system.run.started`, gate events, Maestro guidance (if requested), tool request/result pairs, terminal event, run outcome artifact.
- Ordering: events must follow legal sequences (start → gate → execute → complete) with matched correlation IDs.
- Gating: every gated plan step must emit `execution.gate.evaluated`; decisions/authorities/rationales must align with plan metadata and risk signals.
- Tool usage: tools referenced in execution plans must either emit invocation events or be marked skipped; no orphaned request/result.
- AWACS consistency: observed events/artifacts must allow AWACS to render the run with no silent gaps.

## Reporting Model
- Produces human-readable test reports stored as Library artifacts. Each report includes scenario intent, observed events, invariants checked, and findings.
- Severity levels: `info` (expected), `warning` (non-blocking drift), `error` (invariant violation/missing artifact).
- Reports describe missing/unexpected behavior with explicit references (event IDs, artifact URIs). Emission includes a telemetry event plus the stored artifact.

## Handoff and Remediation
- Reports are surfaced through Maestro/AWACS to humans or designated support agents.
- Support/Engineering use reports for remediation (bug triage, policy or mission adjustments).
- Operation is non-blocking by default: failures raise warnings/errors but do not halt production runs. Focus is continuous monitoring and explainability.
