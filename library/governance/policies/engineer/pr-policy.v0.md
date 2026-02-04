# Engineer Pull Request (PR) Policy

## Purpose

Ensure atomic, reviewable, and auditable changes while allowing **explicit, controlled exceptions** when real-world engineering uncovers unexpected requirements.

This policy prioritizes **predictability and drift prevention** over convenience.

---

## Core Rule

> **A task defines not only _what_ may change, but _where_ changes are allowed.**

Any deviation from expected files or layers must be **explicitly declared, justified, and approved**.

---

## Default Expectations (Strict Mode)

Unless stated otherwise in the task:

### Allowed

- Files and layers explicitly implied by the task description
- Test files required to validate task scope
- Tooling or lint changes strictly required by the above

### Forbidden

- Renderer changes
- State-layer changes
- Runtime or dev-loop changes
- Refactors unrelated to the task
- Opportunistic cleanups

**Undeclared forbidden changes result in automatic PR rejection.**

---

## UI Structure & Zone Immutability

UI structure, zones, and shell immutability are governed by `UI-CONTRACT-AWACS.v1`.

Any PR modifying frozen UI structure or zones requires a prior UI contract revision and authorization artifact.

No other PR rules, scopes, or enforcement mechanisms are modified by this clause.

---

## Declared Scope Exceptions (Escape Hatch)

Unexpected files may be modified **only if** they are declared in the PR.

### Required PR Section

```markdown
### Scope Exceptions

Unexpected files modified or created:

- File: <path>
  Category: <one allowed category>
  Reason: <concise explanation>
  Impact: <behavioral / non-behavioral>
  Alternatives considered: <if applicable>
```

If this section is omitted or incomplete, the PR is evaluated under **Strict Mode**.

---

## Allowed Justification Categories

Exceptions must fit **one** of the following:

- Contract mismatch discovered
- Testability blocker
- Lint/tooling dependency
- Bug uncovered by task execution
- Type system inconsistency

### Explicitly Disallowed Justifications

- "Cleaner"
- "While I was here"
- "Future-proofing"
- "Minor improvement"
- "Refactor opportunity"

If it doesn’t map to an allowed category, it is not allowed.

---

## Approval Flow

1. **Engineer**

   - Declares scope exceptions (if any)
   - Limits blast radius

2. **PM (Guardian Role)**

   - Verifies declarations
   - Confirms category validity
   - Assesses scope containment

3. **Guardian Decision**

   - ✅ Authorize PM approval
   - ⏫ Escalate to Human (high-risk layers)
   - ❌ Reject (policy violation)

Guardian **does not invent or improve justification** — only validates.

---

## Human Escalation Criteria

Escalation is required when:

- Core architectural layers are crossed (renderer, state, runtime)
- Behavioral semantics change
- Multiple exceptions compound risk

---

## Enforcement Notes

- Small diffs do not reduce scope violations
- Size is irrelevant; **layer ownership matters**
- Silent drift is the primary failure mode this policy prevents

---

## Outcome

This policy allows:

- Legitimate discovery
- Explicit risk acknowledgment
- Auditability and rollback safety

While preventing:

- Silent scope creep
- Unreviewable PRs
- Architectural erosion

---

**Summary Rule:**

> Unexpected file changes are forbidden unless explicitly declared, justified under an approved category, and authorized by Guardian or escalated to Human.
