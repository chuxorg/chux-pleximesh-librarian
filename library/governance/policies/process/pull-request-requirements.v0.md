# Pull Request Requirements v0

## Purpose

This policy defines **what must be true before a Pull Request may be merged**.
It exists to prevent silent drift, incomplete artifacts, and unverifiable changes.

---

## Required for All PRs

1. **Clear Scope**

   - PR must map to a single task or ticket
   - Mixed-scope PRs are rejected

2. **Passing Build**

   - `npm run build` (or equivalent) must pass
   - TypeScript errors block merge

3. **Lint Compliance**

   - All lint rules must pass
   - No disabled rules without Guardian waiver

4. **Tests**

   - Unit tests required for:

     - UI logic
     - Data normalization
     - Surface contracts

   - If tests are not applicable, PR must state why

5. **Verification Evidence**

   - Runtime validation (if applicable) must be documented in PR comments
   - “Works on my machine” is not acceptable without details

---

## PR Description Must Include

- **What changed**
- **Why it changed**
- **How to verify**
- **Risks / follow-ups**

---

## Merge Authority

- Engineers **do not merge**
- PM merges only after all preconditions pass
- Guardian may block or waive rules explicitly

---

## Definition of Done

A PR is mergeable only when:

- All required checks pass
- Required artifacts exist
- Scope and intent are unambiguous
