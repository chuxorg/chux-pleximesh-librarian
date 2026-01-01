# AWACS Workspace Model (v0)

## 1. Workspace Regions
- **Activity Bar (left strip):** Icon-based global navigation (Runs, Missions, Testing, etc.); read-only, no data content.
- **Primary Sidebar (left pane):** Context-specific lists driven by the active activity icon (run/task list, mission rail entries, test summaries); read-only selection list.
- **Main Panel (center):** Detailed view for current selection (task detail, mission execution view, timeline, Guardian “Why” cards); read-only visualization.
- **Secondary Panels (right):** Supplementary context panes (Maestro guidance history, Guardian rationale detail, mission metadata, test report detail); read-only.
- **Bottom / Output Panel:** Collapsible output/log feed showing raw system output, event traces, or Testing Agent logs tied to the selected context; read-only.

## 2. Region Responsibilities
| Region | Shows | Never Shows | Interaction |
| --- | --- | --- | --- |
| Activity Bar | Icons + badges for contexts | Task data, timelines, logs | Icon selection only |
| Primary Sidebar | Task list, mission rail entries, test summaries | Detailed timelines, raw logs | Read-only row selection |
| Main Panel | Task timeline, mission execution, Guardian “Why” cards | Maestro guidance conversation, raw logs | Read-only view |
| Secondary Panels | Maestro guidance, Guardian rationale, mission metadata, test detail | Task lists, raw logs | Read-only |
| Bottom Panel | Raw system output/log feed | Mission/task summaries | Read-only |

## 3. Core Surfaces by Region
- **Task List:** Primary Sidebar.
- **Mission Rail:** Primary Sidebar (list) with detail echoed in Main Panel.
- **Task Detail / Timeline:** Main Panel.
- **Guardian “Why”:** Secondary Panels (right).
- **Maestro Guidance:** Secondary Panels (conversation history, read-only).
- **Test Results:** Summary in Primary Sidebar, detail in Secondary or Bottom Panel.
- **Raw System Output:** Bottom/Output Panel only.

## 4. Routing & Focus Rules
- Activity Bar selection reconfigures the Primary Sidebar context.
- Selecting an item in the Primary Sidebar sets the active context (`run_id`/`task_id`) and populates Main/Secondary/Bottom panels accordingly.
- Selecting events inside the Main Panel highlights related entries in Secondary/Bottom panels but does not change context.
- Allowed actions: select rows, change tabs, expand/collapse panels. Disallowed: execution controls, drag-and-drop, direct editing, free-form chat.
- Context propagates one-way: Sidebar → other regions. Secondary/Bottom panels cannot change the primary selection.

## 5. Non-Goals (Current Phase)
- No execution controls (start/pause/abort) in the UI.
- No drag-and-drop rearrangement or layout editing.
- No editor semantics or inline artifact editing.
- No persistence actions (create/update artifacts) from the workspace.
- No Maestro chat input (guidance is display-only).
- No custom layout/themes beyond the default; focus is on read-only control-plane visibility.

This VS Code–style layout keeps AWACS a calm, operator-focused control plane aligned with the existing runtime and event model while supporting future expansion without heavy refactors.
