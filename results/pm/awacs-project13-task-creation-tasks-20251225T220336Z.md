# AWACS Project 13 — Task Entries (2025-12-25T22:03Z)

**Execution ID:** awacs-project13-task-creation-20251225T2203Z  
**Root Directive:** results/pm/awacs-project13-task-creation-prompt-20251225T220336Z.md  
**Project:** https://github.com/orgs/chuxorg/projects/13  
**Repository:** chux-pleximesh-awacs

All three tasks must be entered into Project 13 before work starts, each citing the Librarian sources below. No commits, PRs, or QA handoffs are allowed without persisted artifacts referencing this record.

## Task: Procedure Ladder Guardrails (Simultaneous Parameters)
- **Owner:** UI Agent (Procedure Ladder maintainer)
- **Librarian references:** decisions/architecture/awacs-procedure-ladder-guardrails.md; results/guardian/awacs-vscode-ui-mining-review.md
- **Scope:**
  - Codify the rule set for when Procedure Ladder runs sequentially vs. simultaneously using the decision file as authority.
  - Update the AWACS cockpit spec so simultaneous submission shows every required parameter, required-state indicators, and provenance before actuation.
  - Ensure inline validation feedback is rendered before execution and attach QA plus telemetry acceptance notes describing how these validations are recorded.
- **Execution discipline:**
  - Add this task to AWACS GitHub Project 13 with repo `chux-pleximesh-awacs` before any work begins.
  - Create a dedicated working branch from `dev` (e.g., `ui/procedure-ladder-guardrails`) and keep promotion strictly dev → qa → master under Guardian gating.
  - Commit after every prompt execution that alters code/spec artifacts, citing this Project 13 task.
  - UI Agent must open a PR targeting `dev`, linking to the Librarian references and to this new task before requesting review.
  - Persist updated cockpit specifications, validation rules, QA notes, and telemetry acceptance evidence to the Librarian before moving status.

## Task: Mission Rail Scaling & Grouping Rules
- **Owner:** UI Agent (Mission Rail owner)
- **Librarian references:** decisions/architecture/awacs-mission-rail-scaling.md; results/guardian/awacs-vscode-ui-mining-review.md
- **Scope:**
  - Define deck grouping thresholds, metadata, and clutter limits that match the Mission Rail decision artifact.
  - Document glanceable behaviors for grouped decks, including how the active deck remains surfaced and how operators switch between groups without hidden state.
  - Capture observability cues plus acceptance criteria and QA notes that Guardian/QA can validate.
- **Execution discipline:**
  - Add this task to AWACS GitHub Project 13 with repo `chux-pleximesh-awacs` before any work begins.
  - Use a branch off `dev` (e.g., `ui/mission-rail-scaling`) and keep promotion dev → qa → master with no shortcuts.
  - Commit after each prompt execution affecting Mission Rail artifacts and cite this Project 13 task.
  - UI Agent must open a PR to `dev`, referencing the Librarian decision and review artifacts and attaching persisted spec updates before merge.
  - Persist the grouping rules, clutter limits, QA evidence, and observability notes to the Librarian.

## Task: Authority Matrix Certification Workflow
- **Owner:** Guardian Agent
- **Librarian references:** governance/awacs/authority-matrix-certification.md; results/guardian/awacs-vscode-ui-mining-review.md
- **Scope:**
  - Define module declaration requirements (surfaces, triggers, state predicates) and how PM submissions are certified or rejected.
  - Describe the certification and approval workflow, including enforcement hooks, audit logging, and how violations surface in the AWACS UI.
  - Record acceptance criteria, QA expectations, and telemetry notes covering rejection visibility and persistence events.
- **Execution discipline:**
  - Add this task to AWACS GitHub Project 13 with repo `chux-pleximesh-awacs` before any work begins.
  - Create a Guardian working branch from `dev` (e.g., `guardian/authority-matrix-cert`) and strictly promote via dev → qa → master.
  - Commit after every prompt execution impacting the certification workflow artifacts and cite this Project 13 task.
  - Guardian Agent (and any UI collaborators) must open PRs targeting `dev`; UI-affecting changes cannot merge without PR review plus Guardian sign-off.
  - Persist the certification workflow document, enforcement plan, QA evidence, and any UI notification copy to the Librarian prior to QA handoff.
