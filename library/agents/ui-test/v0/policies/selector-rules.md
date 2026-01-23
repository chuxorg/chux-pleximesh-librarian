# UI Test Selector Rules v0

## Primary rule

Use `data-testid` attributes for all test selectors.

## Forbidden selectors

- Deep CSS selectors tied to layout structure
- Text-only selectors for critical paths (allowed only for stable labels)
- Index-based selectors (e.g., nth-child) unless the UI is explicitly ordered and stable

## Naming convention

`data-testid="<surface>:<component>:<role>"`

Examples:

- `workbench:sidebar:runs-tree`
- `runExplorer:runList:item`
- `timeline:eventCard`
- `artifactViewer:content`

## Engineering requirement

When a new surface or component is added, Engineer Agents must add stable test ids for:

- navigation entry
- primary list/tree
- primary details panel
