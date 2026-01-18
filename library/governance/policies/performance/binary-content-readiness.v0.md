# Binary Content Readiness (v0) — Performance Policy

## Purpose
Enable future binary or compressed artifact storage without changing the Mongo artifact schema.

## Scope
Applies to any artifact whose `content` cannot be safely stored as plain text (large files, binary outputs, or compressed blobs).

## Policy
1. **Explicit encoding metadata**
   - When `content` is encoded or compressed, metadata must include:
     - `metadata.content_encoding`
     - `metadata.compression`
     - `metadata.sha256`

2. **Integrity preservation**
   - `metadata.sha256` must represent the decoded, canonical content payload.
   - `content_format` must still describe the logical format (e.g., json, markdown, text).

3. **Replay safety**
   - Any consumer that cannot decode the content must treat the artifact as opaque and request rehydration from the Librarian.

## Non-Goals
- This policy does not mandate a specific encoding or compression algorithm.
- This policy does not modify the existing artifact envelope schema.
