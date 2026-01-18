# Authority Matrix — Certification & Enforcement Workflow

## Purpose

Define who certifies module declarations and how violations surface to the UI.

---

## Certification Authority

- Guardian is the certifying authority
- PM proposes, Guardian approves
- Librarian records certification artifacts

---

## Declaration Requirements

Modules must declare:

- Surfaces requested
- Triggers exposed
- State predicates required

Declarations are declarative and auditable.

---

## Enforcement

- Uncertified declarations are rejected
- Rejections surface in the UI with rationale
- Violations emit events and are persisted by the Librarian

---

## Charter & Law Alignment

- Truthful observability (§8)
- Anti-spoofing via governance
- Persistence Law (mandatory recording)
