# Definition of Done v0

## Purpose

Define the **minimum acceptance criteria** for engineering tasks.

---

## Required for All Engineering Tasks

An engineering task is **not complete** unless all of the following pass:

1. **Dependencies install cleanly**

   ```bash
   npm install
   ```

2. **Lint passes**

   ```bash
   npm run lint
   ```

3. **TypeScript build passes**

   ```bash
   npm run build
   ```

4. **Unit tests pass (if applicable)**

   ```bash
   npm test
   ```

5. **Runtime verification (if applicable)**

   - Electron launches for UI work
   - Verification evidence recorded in PR comments

---

## Prohibited Shortcuts

- Skipping tests
- Forcing installs
- Disabling lint rules
- Suppressing TypeScript errors

Exceptions require Guardian waiver.

---

## Merge Rule

PM must not merge a PR unless Definition of Done is satisfied and verified.
