# AWACS Project 13 — UI Execution Authorization (2025-12-25T22:12Z)

**Root Prompt:** results/pm/awacs-ui-authorization-prompt-20251225T221253Z.md  
**Authorizing Agent:** PM Agent (AWACS)  
**Project:** https://github.com/orgs/chuxorg/projects/13  
**Repository:** chux-pleximesh-awacs

## Task Verification
- Confirmed that all three required tasks remain defined exactly as persisted in `results/pm/awacs-project13-task-creation-tasks-20251225T220336Z.md:10-50`, covering Procedure Ladder Guardrails, Mission Rail Scaling & Grouping Rules, and Authority Matrix Certification Workflow with their mandated scope and execution discipline.  
- Guardian PASS disposition and follow-up mandates are cited from `results/guardian/awacs-vscode-ui-mining-review.md:1-45`, satisfying the requirement to link Guardian decisions to each task description.

## Librarian References Attached
For every Project 13 task, attach the following references and cite them in the task body:
1. `results/pm/awacs-project13-task-creation-tasks-20251225T220336Z.md` (task definitions)
2. `results/guardian/awacs-vscode-ui-mining-review.md` (Guardian PASS + follow-ups)

Each task description must continue to state:
- Working branch must start from `dev` with single-branch-per-task discipline.
- Promotion order is strictly `dev → qa → master` under Guardian gating.
- Commits occur after **every** prompt execution.
- UI Agent work requires a PR targeting `dev` (Guardian task follows same PR gating when UI artifacts change).
- All prompts, artifacts, QA notes, and telemetry evidence must be persisted to the Librarian before advancing status.

## Owner Assignments & Preconditions
- Procedure Ladder Guardrails → **UI Agent** (Procedure Ladder maintainer). Execution remains blocked unless the task includes the Librarian references above and the UI Agent acknowledges branch/PR/persistence law.
- Mission Rail Scaling & Grouping Rules → **UI Agent** (Mission Rail owner). Execution is blocked until Librarian references are attached and the UI Agent acknowledges the same rules.
- Authority Matrix Certification Workflow → **Guardian Agent**. Guardian must coordinate with UI Agent only if UI surfaces change, maintaining dev-branch workflow and persistence law.

## Notification to UI Agent
> **To:** UI Agent (Procedure Ladder & Mission Rail owners)  
> **Subject:** AWACS Project 13 Tasks Authorized — Procedure Ladder & Mission Rail  
> 
> Your two Project 13 tasks (Procedure Ladder Guardrails and Mission Rail Scaling) are now assigned and reference the canonical Librarian artifacts listed above. Work may begin only after you confirm that each task cites the Librarian paths, you have created a dedicated branch from `dev` per task, and you are prepared to commit after every prompt execution. All work must stay within `dev → qa → master`, every UI change requires a PR targeting `dev`, and every prompt/artifact/response must be persisted to the Librarian referencing the task ID. No execution outside these tasks or without persisted evidence is permitted. Coordinate with the Guardian Agent if any cross-task impacts arise.

## Next Steps
1. Ensure Project 13 cards link to both Librarian artifacts and retain the mandated execution text. If any card diverges, correct it before UI work resumes.  
2. Await UI Agent acknowledgement that the branch/PR/persistence rules are understood; only then may execution commence.  
3. Track Guardian-task progress separately to maintain Authority Matrix certification coverage.
