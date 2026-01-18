# Dev Workflow Enforcement (v0) — PlexiMesh Governance Law

## Non-negotiables (effective immediately)

1. **Task-specific branches only**

   - Every unit of work occurs on a fresh branch:

     - feature/<task>
     - fix/<task>

   - Agents must not reuse long-lived branches.

2. **No pushes to master/main — ever**

   - master/main is protected by policy and by process.
   - Any attempt to push directly is a process violation.

3. **PR-only merges to development**

   - All changes enter development via PR.
   - PM is the merge authority and must explicitly approve or reject.

4. **Repo sync before work**

   - Before editing files:

     - `git status` must be clean
     - `git pull --rebase` (or equivalent) must be performed
     - If unexpected modified files exist: stash them immediately.

5. **Test gate is absolute**

   - A PR must not be merged unless:

     - `go test ./...` passes

   - No exceptions for “unrelated failures.”

6. **Commit discipline**

   - Agents may commit locally as needed, but:

     - they must not push to protected branches
     - they should push their feature/fix branch when ready for PR review

   - Commits should remain scoped to the task checkpoint.

7. **PM PR checklist**

   - PM must verify:

     - scope matches phase checkpoint
     - tests pass
     - no contract drift (Phase 0 locks remain intact)
     - no unrelated file churn
