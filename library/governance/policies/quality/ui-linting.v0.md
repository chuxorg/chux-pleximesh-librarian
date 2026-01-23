# UI Linting Policy v0

## Purpose

This policy enforces **static correctness and contract discipline** in UI code.
Linting exists to catch ambiguity early, before runtime failures.

---

## Non-Negotiable Rules

1. **Lint must pass for all Pull Requests**

   - No warnings treated as “acceptable”
   - No disabling rules without Guardian waiver

2. **TypeScript strictness is required**

   - `noImplicitAny` must be enabled
   - `strictNullChecks` must be enabled
   - Indexing into objects requires closed unions or guards

3. **UI contract violations are lint failures**

   - No indexing with `string` where union types exist
   - No functions returning `boolean | undefined` where `boolean` is required
   - No unchecked external/event data at render boundaries

4. **Linting runs locally and in CI (when available)**

   - Engineers must run lint before opening PRs
   - PM must not merge PRs with failing lint

---

## Allowed Exceptions

- Temporary rule suppression requires:

  - Inline comment explaining why
  - Guardian waiver artifact
  - Follow-up task reference

---

## Definition of Done

A UI change is not complete unless:

- Lint passes with zero warnings
- TypeScript reports zero errors
- No rules are bypassed without approval
