# Context from my IDE setup:

## Open tabs:
- .env.local: .env.local

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
You are acting as the **PM Agent** for AWACS.

Repository:
- chux-pleximesh-awacs

Project:
- AWACS GitHub Project 13

Task:
- Mission Rail Scaling & Grouping Rules — **Implementation Authorization**

---

## AUTHORIZATION INPUTS (AUTHORITATIVE)

You MUST verify the following Guardian decision exists and is persisted:

- central-librarian://project13/mission-rail/review/guardian-decision.md

If this artifact is missing, your ONLY valid response is:
**BLOCK — Guardian approval missing**

---

## OBJECTIVE

Authorize the **UI Agent** to begin **implementation** of the Mission Rail Scaling & Grouping Rules.

This authorization applies ONLY to the Mission Rail task.

---

## REQUIRED PM ACTIONS

1. Update the Mission Rail task card in **Project 13** to:
   - Record Guardian **PASS**
   - Mark the task as **Approved for Implementation**
2. Explicitly restate implementation constraints on the task:
   - Start from `dev`
   - One working branch for this task
   - Commit after every prompt execution
   - Push immediately after commit
   - UI Agent MUST open a PR targeting `dev`
   - No self-merge
   - dev → qa → master promotion only
   - All prompts, artifacts, and responses persisted
3. Notify the UI Agent that:
   - Implementation is authorized
   - Scope is limited strictly to the approved Mission Rail specs
   - Any deviation requires Guardian review

---

## OUTPUT REQUIREMENTS

You MUST produce:
1. Confirmation that Guardian approval was verified
2. Confirmation that the Project 13 task was updated
3. Confirmation that the UI Agent was notified and authorized

You MUST then:
- Persist this prompt to the central Librarian
- Persist your authorization response to the central Librarian

Only after persistence is complete may the UI Agent begin implementation.
