# Tooling Compatibility Policy v0

## Purpose

Ensure that development tooling versions are **mutually compatible, supported, and stable**.

---

## Rules

1. **Do not force incompatible dependency resolutions**

   - `--force` and `--legacy-peer-deps` are forbidden in normal development
   - Exceptions require Guardian waiver

2. **Respect upstream compatibility matrices**

   - ESLint, TypeScript, and @typescript-eslint versions must align
   - Major version mismatches are not allowed

3. **Prefer stability over novelty**

   - New major versions may be adopted only after ecosystem support is confirmed
   - Experimental toolchains are not allowed on critical paths

---

## Current Canonical Tooling Set

- ESLint: `^8.56.0`
- @typescript-eslint/parser: `^7.18.0`
- @typescript-eslint/eslint-plugin: `^7.18.0`
- TypeScript: per repo `tsconfig.json`

---

## Definition of Done

A tooling change is acceptable only when:

- `npm install` succeeds without flags
- `npm run lint` passes
- `npm run build` passes
