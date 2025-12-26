# AWACS Project 13 — Task Entries (2025-12-25)

## Task: Procedure Ladder Guardrails (Simultaneous Parameters)
- **Source references**: results/guardian/awacs-vscode-ui-mining-review.md; decisions/architecture/awacs-procedure-ladder-guardrails.md
- **Owning agent**: UI Agent (Procedure Ladder maintainer). PM tracks progress; Guardian notified on completion.
- **Scope**:
  - Define the guardrails determining when Procedure Ladder steps can run sequentially vs. simultaneous input capture, including dependency detection logic and operator confirmation rules.
  - Update the AWACS cockpit specification to show simultaneous submission surfaces every parameter with inline validation, provenance badges, and a single launch confirmation.
  - Capture acceptance criteria + QA notes covering dependent/independent parameter identification, validation error surfacing, and telemetry hooks for ambiguity reporting.
- **Execution rules**:
  - Work in repo `chux-pleximesh-awacs` on a dedicated branch off `dev` (e.g., `ui/procedure-ladder-guardrails`); promote changes strictly dev → qa → master.
  - UI Agent MUST open a PR targeting `dev`, referencing this Project 13 task and linking Librarian artifacts before merge.
  - Commit after every prompt execution that changes specs, diagrams, or code for this task and note the task ID in each commit message.
  - Persist all updated specs, validation notes, and QA evidence to the Librarian; no work is considered done until artifacts exist.

## Task: Mission Rail Scaling & Grouping Rules
- **Source references**: results/guardian/awacs-vscode-ui-mining-review.md; decisions/architecture/awacs-mission-rail-scaling.md
- **Owning agent**: UI Agent (Mission Rail owner). PM coordinates reviews; Guardian validates grouping governance when ready.
- **Scope**:
  - Document how Mission Rail evolves from a flat deck list to grouped decks as mission modes grow, including thresholds, grouping metadata, and operator cues.
  - Specify UI behaviors for selecting a group, keeping the active deck visible, and ensuring groups remain glanceable without search-only flows.
  - Provide acceptance criteria describing clutter limits, grouping transitions, and observability signals for Guardian/QA sign-off.
- **Execution rules**:
  - Use repo `chux-pleximesh-awacs` with a working branch per task (e.g., `ui/mission-rail-scaling`) branched from `dev`; integrate via dev → qa → master only.
  - UI Agent MUST raise a PR against `dev` referencing this Project 13 task and attach Librarian artifact links before review.
  - Commit after every prompt execution contributing to this scope and cite the task ID.
  - Persist the finalized Mission Rail spec updates, diagrams, and QA notes to the Librarian immediately when produced.

## Task: Authority Matrix Certification Workflow
- **Source references**: governance/awacs/authority-matrix-certification.md; results/guardian/awacs-vscode-ui-mining-review.md
- **Owning agent**: Guardian Agent (coordinates with PM; works with UI Agent only when UI changes arise).
- **Scope**:
  - Author the certification workflow describing how modules declare requested surfaces/triggers/state predicates, how PM submits the declarations, and how Guardian certifies or rejects them with rationale surfaced to operators.
  - Define enforcement + auditing expectations so rejected declarations produce cockpit-visible notices and Librarian evidence per the governance file.
  - Produce acceptance criteria covering audit log structure, notification pathways, and escalation triggers for violations.
- **Execution rules**:
  - Work in repo `chux-pleximesh-awacs` on a dedicated branch from `dev` (e.g., `guardian/authority-matrix-cert`), promoting through dev → qa → master post-approval.
  - Any UI Agent contributions spawned by this workflow must land via PRs targeting `dev` referencing this task and citing Librarian artifacts.
  - Commit after every prompt execution affecting certification specs, enforcement plans, or supporting assets.
  - Persist the certification workflow, enforcement plan, and acceptance/QA documentation to the Librarian; cite those paths back in the eventual PR and Project 13 comment.
