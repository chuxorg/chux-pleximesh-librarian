# Reference-First Prompts (v0) — Performance Policy

## Purpose
Establish a reference-first prompt workflow to minimize payload size while preserving auditability and replay.

## Scope
Applies to all agent prompts, responses, plans, and task artifacts persisted as dynamic artifacts.

## Policy
1. **Persist-first**
   - Full prompt and response bodies must be stored in Mongo as artifacts before they are referenced in runtime messages.

2. **Reference-first runtime messages**
   - Runtime messages should pass canonical URIs and short summaries instead of embedding full content.
   - Summaries must not introduce new semantics beyond what is stored at the referenced URIs.

3. **Manifested prompt assembly**
   - Prompt construction must use a manifest of URIs (plus optional short snippets) rather than inline bodies.
   - Size limits are defined per mission, gate, or plan; the manifest must record any truncation.

4. **Auditability**
   - Each referenced artifact must include `references` to upstream URIs when applicable.
   - Missing references are treated as a blocking gap and require escalation.

## Non-Goals
- This policy does not define new runtime behavior; it constrains how prompts are assembled and referenced.
- This policy does not alter the Mongo artifact schema.
