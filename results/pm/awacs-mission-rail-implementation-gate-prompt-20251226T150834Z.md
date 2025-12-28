# Context from my IDE setup:

## Open tabs:
- versioning-and-release-policy.md: governance/sdlc/versioning-and-release-policy.md
- awacs-task-orchestration-and-source-control.md: results/pm/awacs-task-orchestration-and-source-control.md
- awacs-vscode-ui-mining-review.md: results/guardian/awacs-vscode-ui-mining-review.md
- awacs-procedure-ladder-guardrails.md: decisions/architecture/awacs-procedure-ladder-guardrails.md
- awacs-mission-rail-scaling.md: decisions/architecture/awacs-mission-rail-scaling.md

## My request for Codex:
You are operating as an AWACS Agent within the PlexiMesh system.

The runtime event bus is NOT yet active.
Until it exists, you MUST enforce persistence manually.

---

## MANDATORY PERSISTENCE (NON-NEGOTIABLE)

1. You SHALL forward the **exact prompt you received** to the central Librarian.
2. You SHALL forward **all artifacts you generate** to the central Librarian.
3. You SHALL forward your **final response** to the Librarian IN ADDITION to replying here.
4. If persistence cannot be completed, you SHALL halt and report failure.

If it is not in the central Librarian, it does not exist.

---

## ROLE
You are acting as the **PM Agent** (or Documentation Agent, if delegated).

---

## TASK
Create the **canonical Gate Specification** for the following gate:

**Gate Name:** Mission Rail — Implementation Authorization Gate

This gate is required before any implementation work may begin.

---

## REQUIRED ARTIFACT (AUTHORITATIVE)

You MUST create and persist a document that defines:

1. **Gate Purpose**
   - What decision this gate controls
   - What phase transition it authorizes

2. **Required Input Artifacts**
   - Exact Librarian paths (e.g. specs, acceptance criteria, prior Guardian decisions)
   - Explicit statement that missing artifacts result in BLOCK

3. **Governing Law**
   - governance/awacs/nfr-charter.md
   - governance/laws/persistence-law.md
   - Any other governing docs this gate depends on

4. **Guardian Evaluation Checklist**
   - What the Guardian must verify
   - What constitutes PASS vs BLOCK vs ESCALATE

5. **Decision Outputs**
   - Where the Guardian decision must be persisted
   - Required format of the decision artifact

---

## DESTINATION (MANDATORY)

Persist the gate specification to:

central-librarian://project13/gates/mission-rail-implementation-gate.md

---

## OUTPUT REQUIREMENTS

You MUST produce:
1. Confirmation the gate specification was created
2. The exact Librarian path where it is persisted

You MUST then:
- Persist this prompt to the central Librarian
- Persist your response to the central Librarian

Only after this artifact exists may the Guardian re-run the gate evaluation.
