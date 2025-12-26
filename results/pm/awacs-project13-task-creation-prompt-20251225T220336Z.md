# Context from my IDE setup:

## Open tabs:
- .env.local: .env.local

## My request for Codex:
You are operating as an AWACS Agent within the PlexiMesh system.

The runtime event bus is NOT yet active.
Until it exists, you are required to enforce persistence manually.

---

## MANDATORY PERSISTENCE (NON-NEGOTIABLE)

1. You SHALL forward the **exact prompt you received** to the Librarian.
2. You SHALL forward **all artifacts you generate** to the Librarian.
3. You SHALL forward your **final response** to the Librarian IN ADDITION to replying here.
4. If persistence cannot be completed, you SHALL halt and report failure.

If it is not in the Librarian, it does not exist.

---

## TASK TO PERFORM — PM ROLE

You are acting as the **PM Agent**.

Project:
- AWACS GitHub Project: https://github.com/orgs/chuxorg/projects/13
Repository:
- chux-pleximesh-awacs

Governing policies are already persisted. You must not restate or reinterpret them.

---

## TASKS TO CREATE IN PROJECT 13

Create the following three tasks exactly as specified below.  
Do NOT invent scope. Do NOT merge tasks. Do NOT loosen execution rules.

---

### 1. Procedure Ladder Guardrails (Simultaneous Parameters)

**Owner:** UI Agent (Procedure Ladder maintainer)

**Scope:**
- Codify rules for sequential vs simultaneous parameter entry
- Update cockpit spec so simultaneous execution surfaces all parameters
- Inline validation must be visible before actuation
- Capture QA and telemetry acceptance notes

**Execution Discipline (MANDATORY):**
- Working branch from `dev`
- Commit after every prompt execution
- UI Agent MUST open a PR to `dev`
- dev → qa → master promotion only
- All artifacts persisted to the Librarian

---

### 2. Mission Rail Scaling & Grouping Rules

**Owner:** UI Agent (Mission Rail owner)

**Scope:**
- Define deck grouping thresholds and metadata
- Specify glanceable behaviors and clutter limits
- Define observability cues when missions are grouped
- Capture acceptance criteria and QA notes

**Execution Discipline (MANDATORY):**
- Working branch from `dev`
- Commit after every prompt execution
- UI Agent MUST open a PR to `dev`
- dev → qa → master promotion only
- All artifacts persisted to the Librarian

---

### 3. Authority Matrix Certification Workflow

**Owner:** Guardian Agent

**Scope:**
- Define declaration requirements for modules
- Define certification and approval workflow
- Define enforcement and audit expectations
- Define how violations surface in the UI
- Capture acceptance criteria and QA notes

**Execution Discipline (MANDATORY):**
- Working branch from `dev`
- Commit after every prompt execution
- PR required for any UI-affecting changes
- dev → qa → master promotion only
- All artifacts persisted to the Librarian

---

## TASK CREATION RULES

For EACH task you create:
- Add it to **GitHub Project 13**
- Assign the correct owner
- Reference the relevant Librarian artifacts
- State branch, PR, and persistence requirements explicitly

You MAY NOT:
- Allow work to begin without a task
- Allow commits without a task
- Allow PRs without persisted artifacts
- Bypass QA or Guardian involvement

---

## OUTPUT REQUIREMENTS

You MUST produce:
1. A concise task list as entered into Project 13
2. Confirmation of owner assignment per task

You MUST then:
- Persist this prompt to the Librarian
- Persist the task definitions to the Librarian
- Persist your final response to the Librarian

Only after persistence is complete may the task be considered finished.
