# AWACS Project 13 — Follow-Up Task Entries

## Task: Procedure Ladder Guardrails (Simultaneous Parameters)
- **Source**: decisions/architecture/awacs-procedure-ladder-guardrails.md; aligns with Guardian follow-up (results/guardian/awacs-vscode-ui-mining-review.md)
- **Owning agent**: UI Agent — Procedure Ladder owner (PM to track; Guardian to review governance impact)
- **Scope**:
  - Encode the guardrails that determine when Procedure Ladder steps can gather parameters sequentially vs. simultaneously, ensuring simultaneous mode still surfaces all parameters, inline validation, and provenance before execution.
  - Update the AWACS cockpit UI specification so simultaneous submission presents a single confirmation surface with no partial submission path and preserves required-state visibility.
  - Provide acceptance criteria + QA notes describing how dependent vs. independent parameter sets are detected and how validation errors are displayed.
- **Execution rules**:
  - Work occurs in repo `chux-pleximesh-awacs` on a dedicated branch off `dev` (e.g., `ui/procedure-ladder-guardrails`), flowing dev → qa → master only after review.
  - UI Agent must raise a PR (`dev` base) referencing this task before merge; include Librarian artifact links.
  - Commit after every prompt execution that changes code or specs, citing the task.
  - Persist all updated specs, diagrams, and QA notes to the Librarian.

## Task: Mission Rail Scaling & Grouping Rules
- **Source**: decisions/architecture/awacs-mission-rail-scaling.md; traced to Guardian follow-up (results/guardian/awacs-vscode-ui-mining-review.md)
- **Owning agent**: UI Agent — Mission Rail owner (PM tracks; Guardian notified once grouping contract is defined)
- **Scope**:
  - Define how Mission Rail transitions from the flat deck to grouped decks as mission modes grow, ensuring groups remain explicit and glanceable and that the active deck is never hidden.
  - Document UI behaviors for selecting groups, surfacing the active deck, and preventing search-only or hidden state flows per the decision file.
  - Capture acceptance criteria for clutter limits, grouping metadata, and observability cues PM/QA will validate.
- **Execution rules**:
  - Use repo `chux-pleximesh-awacs`; create a working branch off `dev` (e.g., `ui/mission-rail-scaling`) and only merge via dev → qa → master progression.
  - UI Agent must open a PR targeting `dev`, referencing this task and linking Librarian artifacts before integration.
  - Commit after every prompt execution with task-aligned changes.
  - Persist finalized Mission Rail spec updates, grouping rules, and QA notes to the Librarian.

## Task: Authority Matrix Certification Workflow
- **Source**: governance/awacs/authority-matrix-certification.md; follow-up captured in results/guardian/awacs-vscode-ui-mining-review.md
- **Owning agent**: Guardian Agent (coordinates with PM proposer, ensures Librarian certification log)
- **Scope**:
  - Author the certification workflow describing how modules declare surfaces/triggers/state predicates, how PM submits declarations, and how the Guardian certifies or rejects them with rationale surfaced to the UI.
  - Define enforcement hooks so rejected declarations surface clearly in AWACS and violations emit persistence events, adhering to the governance file.
  - Produce acceptance criteria describing audit logging expectations and UI notification requirements for certification state.
- **Execution rules**:
  - Work in repo `chux-pleximesh-awacs` on a dedicated branch from `dev` (e.g., `guardian/authority-matrix-cert`), promoting through dev → qa → master after approvals.
  - If UI/engineering updates are needed, those agents must open PRs targeting `dev`; Guardian review is mandatory before merge.
  - Commit after every prompt execution touching the workflow artifacts.
  - Persist the certification workflow document, enforcement plan, and any supporting artifacts to the Librarian.
