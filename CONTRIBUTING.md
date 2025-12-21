# Contributing to the PlexiMesh Librarian

The Librarian is a governance-first repository. Every addition must preserve traceability, cite provenance, and be safe for agent consumption. Follow the rules below whenever you add or update an artifact.

## 1. Intake workflow
1. **Classify before you create.** Decide whether the artifact is governance, prompt, canonical decision, or reference. If it does not fit one of those lanes, do not file it here.
2. **Use the correct directory.** Each folder represents a capability boundary. When in doubt, escalate to the Guardian before merging.
3. **Add metadata.** Every artifact must start with a short metadata block (YAML or table) that names the owner, source repo (if applicable), approval authority, and effective date.
4. **Describe the intent.** Provide a concise rationale or summary so future agents understand why the artifact exists.
5. **Open a PR.** All changes require review from at least one Guardian (process) and one Engineer/PM (domain) before landing.

## 2. Version handling
- **Immutable history.** Never rewrite or delete prior decisions. Supersede them by adding a new version with clear references to the earlier artifact.
- **Version headers.** Use `Version: vMAJOR.MINOR` inside the metadata block. Increment MINOR for clarifications and MAJOR for semantic changes.
- **Change logs.** Append a `## Revision History` section documenting the date, author, and summary of every change.
- **Linkage.** When a decision affects prompts or governance rules, add cross-links (and update impacted files) in the same PR so consumers see the ripple effect.

## 3. Referencing protocol for agents
- **Always cite paths and SHAs.** When an agent relies on an artifact, it must cite `path@commit` inside its response.
- **Cache responsibly.** Agents may cache content locally for a session but must re-fetch when the commit SHA changes.
- **Prompt builders.** Any prompt that references Librarian material should include a “Source” footer pointing to the canonical file.
- **Escalations.** If an agent encounters contradictions between artifacts, it must halt the task and open a Guardian issue before proceeding.

## 4. File hygiene
- Use ASCII unless the artifact already requires extended characters (e.g., legal citations).
- Keep line widths ≤ 100 characters when practical so prompts can be streamed into terminals without reflow.
- Prefer Markdown for readability; use plaintext only when format neutrality is required.

## 5. Inclusion tests
Before merging, verify the change answers **yes** to all of the following:
- Does this belong in governance/prompts/decisions/references?
- Is the provenance and approval chain clear?
- Can both humans and agents ingest it without extra tooling?
- Does it avoid duplicating content maintained elsewhere?

Changes that fail any test go back to backlog triage.
