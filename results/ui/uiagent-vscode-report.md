Conceptual Mapping Table

Original VS Code concept AWACS-native name AWACS description Why it reinforces cockpit mentality
Command Palette Action Compass A global, zero-latency overlay that exposes every certified procedure as a searchable card, independent of layout state. Keeps the operator in the “hot seat” by letting them call any maneuver without hunting for screens, mirroring how pilots access critical controls via a single locus.
Quick Pick multi-step prompts Procedure Ladder Guided stepper that asks for successive parameters, pruning choices as context narrows. Matches cockpit checklists—each rung confirms intent before the next, reducing accidental command launches and surfacing uncertainty mid-flow.
Activity Bar with docked view containers Mission Rail Vertical mission selectors that swap whole instrument stacks while preserving global awareness cues. Lets the pilot slide between mission profiles (surveillance, triage, analytics) without leaving the cockpit frame, so UI stays the product.
Split panel docking & drag-resize grid Instrumentation Grid Snap-to-grid canvas where gauges, maps, and logs can be arranged, tethered, or collapsed according to mission priorities. Mirrors reconfigurable cockpit panels: operators can foreground urgent telemetry and sideline the rest without abandoning the shared spatial model.
Status Bar segments & item badges Vitals Band Always-on horizon strip showing system vitals, comms locks, and pending actions as colored capsules with numeric fidelity scores. Establishes a single glanceable ribbon for trust signals; deviations immediately pop, matching the “scan the gauges” discipline.
Toast & progress notifications Alert Flow Time-ordered alert stack that animates from the Vitals Band, showing severity, elapsed time, and acknowledgement state. Alerts never hide ambiguity; they pulse until owned, ensuring nothing falls behind the pilot’s peripheral awareness.
Extension contribution points & when contexts Authority Matrix Declarative contract where each module announces the surfaces, triggers, and state predicates it needs before the cockpit allows it onto the grid. Maintains command discipline: only mission-relevant controls appear when the Authority Matrix affirms context, limiting clutter without concealment.
Rejected Concepts

File Explorer tree: Explicit file-system metaphor; violates the directive to ignore filesystem-centric views and would drag the operator back into clerical workflows.
Editor tab strip: Embeds an editor-first assumption, conflicting with the “UI is the product” charter because it frames AWACS as a document editor instead of an operations cockpit.
Source Control view: Pure Git workflow; breaches cockpit mentality by shifting focus to repository hygiene rather than live operations.
Run/Debug view: Debugger metaphor and breakpoints are developer-centric, adding latency-focused tooling the charter explicitly deprioritizes.
Extension Marketplace: Marketplace mechanics reposition the cockpit as an app store; that dilutes authority boundaries and undermines curated mission readiness.
Observability & Trust Notes

Action Compass + Procedure Ladder keep every operation inspectable: even when invoked via keyboard, each card shows provenance and required states before engaging.
Mission Rail and Instrumentation Grid promote situational awareness by keeping layout changes declarative; the pilot always sees which mission deck is active and how instruments are spatially prioritized.
Vitals Band centralizes telemetry so drift, backlog, and degraded comms are highlighted in one strip rather than scattered, helping the operator maintain continuous scans.
Alert Flow surfaces ambiguity by showing pending acknowledgements with time stamps; nothing silently disappears until explicitly dismissed under Authority Matrix rules.
Authority Matrix logs why a surface admitted or rejected a control, so gaps in instrumentation are traceable rather than mysterious.
Risks & Ambiguities (flagged for Guardian review)

The actual text of nfr-charter.md was absent in this workspace; alignment relies on the summarized principles (“UI is the product”, “cockpit mentality”). Need confirmation that no additional NFRs were missed.
Procedure Ladder assumes operators accept sequential prompts; if AWACS scenarios demand simultaneous multi-parameter actioning, this pattern may introduce friction.
Mission Rail/Multi-deck layout presumes a manageable number of mission modes; if AWACS needs dozens, we risk reintroducing clutter unless a higher-order grouping is defined.
Authority Matrix adaptation of VS Code contribution gating assumes modules can declare contexts safely; governance must define who certifies those declarations to prevent rogue surfaces.
Submission ready for Guardian evaluation.
