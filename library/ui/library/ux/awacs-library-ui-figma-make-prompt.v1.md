# CANONICAL FIGMA MAKE PROMPT — AWACS LIBRARY VIEW (FINAL)

Status: FROZEN
Authority: Human Architect
Phase: LIB-UI-1 (Read-only Library)

---

Context:
You are designing a static HTML mock for the AWACS UI.
The shell (layout, typography, surfaces, spacing) is finalized and must not be changed.

This design represents the canonical visual intent for the Library UI.
It will be implemented directly by CodeX without reinterpretation.

---

OBJECTIVE

Render the AWACS Library as a **read-only, canonical record viewer**.
The UI must feel like an artifact being inspected under glass — not a document being authored.

---

NON-NEGOTIABLE CONSTRAINTS

* No layout or zone changes (Zones 1–5 are frozen)
* No spacing or typography system changes
* No document/page metaphors
* No editing or mutation affordances
* Everything is explicitly read-only

---

ZONE 2 — CONTROL PLANE (LIBRARY NAVIGATION)

* Tree-based navigation
* Clear categorical grouping (Governance / UI / Runtime)
* Single-select only
* Selected item feels anchored
* No drag/drop, no inline edits, no bulk actions

---

ZONE 3 — ARTIFACT VIEWER (CANONICAL RECORD)

### Framing

* Content is shown inside a **framed viewport**
* Subtle inset and boundary
* Slightly tinted background (very light)
* No full-bleed “page” presentation

### Header

* Quiet breadcrumb/context line (e.g. Library / Governance / Policies)
* Artifact ID, version, kind
* Status badge with semantic tone (ACTIVE feels current, DEPRECATED feels historical)

### Metadata Strip

* Authority
* Effective date
* Supersedes / superseded-by relationships
* Visually factual, not decorative

### Content Body

* Rendered as structured record content
* Section labels are schema-like (smaller, muted, field-oriented)
* Lists and rules grouped into semantic blocks
* Narrative flow suppressed in favor of structure

### View Controls

* Markdown / JSON is a VIEW toggle only
* Tab-like, quiet, never button-like

### Provenance

* Read-only / canonical indicator always felt
* Footer text such as:
  “Canonical Library Artifact — Read-only”

---

ZONE 5 — INTEGRATION RAIL

* Disabled placeholders only
* Visually secondary
* Clearly unavailable in read-only mode

---

GLOBAL TONE

* Calm
* Trustworthy
* Auditable
* No dashboard theatrics
* No “document editor” cues

---

OUTPUT

* Single static HTML
* Inline CSS acceptable
* No scripts
* This prompt is now frozen and authoritative
