# Agent Artifact Persistence Requirement

This requirement applies to all agents.

---

## Mandatory Behavior

Before completing any task, an agent MUST:

1. Persist the prompt it received to the Librarian
2. Persist all generated artifacts to the Librarian
3. Declare canonical destination paths

If persistence cannot be completed, the agent MUST halt and report failure.

---

## Completion Definition

An agent task is complete only when:

- Artifacts are written
- Paths are declared
- Downstream agents can retrieve them without chat context

---

## Reminder

Agents communicate through artifacts, not conversation.

The Librarian is the shared memory.
agent-artifact-persistence
