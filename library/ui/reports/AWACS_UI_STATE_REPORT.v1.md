artifact_id: AWACS_UI_STATE_REPORT
version: v1
kind: ui-analysis
domain: ui
scope: awacs
status: canonical
authority: librarian
mutability: read-only

provenance:
  source_type: external-ui-snapshot
  referenced_file: index.html
  repository: awacs-ui-workspace
  method: forensic-ui-analysis
  phase: pre-mvp-ui-stabilization

# AWACS_UI_STATE_REPORT

**Artifact ID:** AWACS_UI_STATE_REPORT
**Version:** v1
**Kind:** UI Analysis
**Status:** Canonical
**Authority:** Librarian

**Grounding Source:**
Consolidated HTML/CSS snapshot (`index.html`) from the AWACS UI workspace (external repository).

---

## 1. Observed UI Facts (Inventory)

### Primary Layout Regions

* Application shell: `div.app-shell`
* Top header: `header.topbar`
* Main layout grid: `main.main-grid`
* Footer/status bar: `footer.status-bar`

### Navigation

* Sidebar: `aside.sidebar`
* Navigation container: `nav.nav-items`
* Seven navigation entries: `div.nav-item`
* Sidebar footer/version label: `div.nav-footer`

### Task Context Panel

* Container: `section.task-panel`
* Header: `div.panel-header`
* Task list: `div.task-list`
* Rows: `div.task-item`

### Primary Detail Panel

* Container: `section.detail-panel`
* Header: `div.detail-header`
* Sections: `div.detail-section`
* Metadata grid: `div.meta-grid`
* Text blocks: `p.detail-text`
* Artifact list: `ul.artifact-list > li.artifact-item`

### Inspector Rail

* Utility rail: `aside.inspector`
* Placeholder control: `div.inspector-button`

### Footer / Status

* Footer container: `footer.status-bar`
* Status groups: `div.status-group`
* Toggles: `div.status-toggle`
* Indicators: `div.status-indicator`
* Help icon: `div.help-icon`

---

## 2. Interaction & State (Observed)

* No interactive HTML elements (`button`, `input`, `select`, `textarea`) are present
* All affordance elements include:

  * `data-interactive="false"`
  * `aria-disabled="true"`
* Visual state hooks exist:

  * `.nav-item.active`
  * `.task-item.selected`
  * `.status-toggle.active` (CSS-defined, unused)

---

## 3. Information Hierarchy (Observed)

* Primary emphasis:

  * `.detail-title`
  * `.section-title`
* Secondary:

  * `.task-title`
  * `.task-meta`
* Tertiary:

  * `.meta-label`, `.meta-value`
  * Artifact type labels
  * Status indicators and timestamps

---

## 4. Derived Intent (Explicitly Labeled)

* **Operational model:** read-only by default
* **Philosophy:** audit-first, deterministic presentation
* **User role:** operator / reviewer / auditor
* **Mental model:**
  navigation -> task context -> detailed inspection -> auxiliary utilities -> system status

---

## 5. Derived UI Requirements (Explicitly Labeled)

### MVP

* The UI MUST preserve the current app shell and layout regions
* The UI MUST preserve explicit read-only signaling via data attributes
* The UI MUST NOT introduce interactive controls without redefining the read-only contract

### Mid-Term

* The UI SHOULD formalize status semantics between header and footer
* The UI SHOULD define behavior for pre-provisioned state classes
* The UI SHOULD declare the inspector's role

### Long-Term

* The UI MUST preserve canonical contract markers
* The UI MUST retain read-only operation unless explicitly reauthorized
* The UI SHOULD formalize system status into machine-readable tokens

---

## 6. Intent Gaps (Observed)

* Navigation semantics are undeclared
* Status scope and authority are ambiguous
* Inspector purpose is unspecified
* Task lifecycle states are not formally defined

---

**End of Canonical Report**
