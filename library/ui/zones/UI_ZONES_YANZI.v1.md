artifact_id: UI_ZONES_YANZI
version: v1
kind: ui_layout
status: active
authority: system
scope: global-ui
mutability: controlled
related_contracts:
  - UI_SHELL_YANZI.v3

description:
  Defines the canonical Yanzi UI zone layout, including geometry,
  zone roles, and base palette assignments for both light and dark
  modes. This artifact captures intent, not component contracts.
  Zone boundaries are considered stable; internal content and
  controls may evolve independently.

display_modes:
  - light
  - dark

geometry_invariants:
  - Canvas: 1440 x 900

zones:
  zone_1_top_app_bar:
    geometry: 1440 x 44
    role: global context and utility chrome
    notes: fixed height; visually calm; may include subtle bottom separator at implementation level

  zone_2a_left_toolbar_rail:
    geometry: 72 x 828
    role: primary tool/navigation rail

  zone_2b_context_navigation_panel:
    geometry: 280 x 828
    header_height: 32
    role: navigation trees, filters, scoped context

  zone_3_main_content_area:
    geometry: 1040 x 828
    role: primary workspace; may contain tabs and scrollable content
    notes: content must not alter zone boundaries

  zone_4_inspector_utility_rail:
    geometry: 48 x 828
    role: secondary utilities and integrations
    notes: visually recessed; minimal emphasis

  zone_5_status_bar:
    geometry: 1440 x 28
    role: passive system and connection status

palette_intent:
  note: The UI uses semantic surface tokens rather than fixed colors.
  semantic_surfaces:
    - chrome
    - content
    - nav_body
    - rail
    - panel_header
    - separator
    - text_primary
    - text_secondary
    - text_muted

light_mode_token_mapping:
  chrome: "#FAFAFA"
  content: "#F5F5F5"
  nav_body: "#ECECEC"
  rail: "#E5E5E5"
  panel_header: "#E5E5E5"
  separator: "#E5E5E5"
  text_primary: "#262626"
  text_secondary: "#525252"
  text_muted: "#737373"

dark_mode_token_mapping:
  chrome: "#141414"
  content: "#1A1A1A"
  nav_body: "#202020"
  rail: "#262626"
  panel_header: "#262626"
  separator: "#2E2E2E"
  text_primary: "#EDEDED"
  text_secondary: "#BDBDBD"
  text_muted: "#8A8A8A"

usage_rules:
  - Zone geometry must remain consistent with UI_SHELL_YANZI.v3
  - Geometry is mode-independent
  - Display modes may only alter token mappings, not structure
  - Visual separators (borders/dividers) are implementation details
  - Components and controls must live strictly within zone boundaries

supporting_material:
  note: non-canonical, informational
  items:
    - Zone 1 SVG
    - Zone 2 SVG (2a / 2b-c combined)
    - Zone 3 SVG
    - Zone 4 SVG
    - Zone 5 SVG
