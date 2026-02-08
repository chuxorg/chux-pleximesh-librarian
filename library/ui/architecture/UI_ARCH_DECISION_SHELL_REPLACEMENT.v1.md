# UI Architecture Decision: Replace Legacy Shell, Preserve Logic

## Decision

The existing UI shell HTML (current `index.html` and its inline UI layout)
is deprecated and must be replaced.

The authoritative UI foundation for Yanzi is:

* `UI_SHELL_YANZI.v3` (canonical geometry and zone layout)
* `UI_ZONES_YANZI.v1` (zone roles + light/dark semantic token mappings)

All UI implementation work must conform to these canonical artifacts.

## Rationale

* The prior UI effort drifted and failed; the rebuild must start from a
  locked, canonical foundation to prevent repeat failure modes.
* The new shell/zones have been explicitly defined, iterated, and stored
  as authoritative artifacts.
* Existing UI code contains valuable logic that should be retained where
  feasible, but it must be rebound to a stable DOM and zone model.

## Consequences

* Legacy HTML must be replaced with the canonical shell and zone structure.
* DOM selectors and component structure will change to match the new shell.
* Any UI code directly tied to legacy HTML elements must be:

  * rebound to the new DOM structure, or
  * replaced if rebinding is infeasible or unsafe.
* Valuable logic modules (state models, helpers, normalization utilities)
  should be preserved where possible, provided they can be adapted cleanly.

## Legacy Clarification

The following are treated as legacy or non-authoritative with respect to DOM:

* existing `index.html` layout and inline placeholder content
* any DOM-dependent UI code expecting the legacy structure

These may be used as reference only during transition.

## Enforcement

* Agents and CodeX must not modify canonical shell geometry ad hoc.
* All new UI work must render inside the canonical zones.
* Any change to zone geometry requires a new version of `UI_SHELL_YANZI`
  and an explicit follow-on ADR.
