# YANZI WORDMARK — FINAL SPEC

## Status
Locked. Approved for production use.

## Scope
Primary brand wordmark for Yanzi.
No symbols. No monogram. Wordmark-only identity.

---

## 1. Wordmark

**Text**
- `yanzi` (all lowercase)

**Typeface Characteristics**
- Modern sans serif
- Neutral proportions
- Low contrast
- No decorative terminals
- Slight forward lean (≈ 6–8°) to imply motion
- No ligatures

The wordmark must feel inevitable and professional, not expressive or trendy.

---

## 2. Underline (Motion Indicator)

The underline is structural, not decorative.

### Geometry
- Single continuous stroke
- Uniform thickness
- No tapering
- No calligraphic variation

### Stroke Weight
- Approximately 70–80% of the primary stem weight of the wordmark

### Curvature
- Near-linear
- Very shallow arc
- Total vertical rise (start to end) ≤ 15% of the wordmark x-height

### Direction
- Begins slightly lower under the `y`
- Ends slightly higher under the `i`
- No exaggerated central curvature

### Ends
- Clean cut or minimal radius matching the wordmark’s terminal radius
- No pointed or swoosh-like ends

### Alignment
- Horizontally centered under the wordmark
- Vertical gap between text and underline ≈ 0.35–0.45 × x-height

If the underline appears almost straight at first glance, it is correct.

---

## 3. Color

**Primary**
- Monochrome only
  - Black on light backgrounds
  - White on dark backgrounds

**Rules**
- Underline always inherits the wordmark color
- No gradients
- No outlines
- No shadows
- No embedded brand color

Color is owned by the product UI, not the logo.

---

## 4. Usage Rules

### Approved
- Product UI
- Navigation bars
- App headers
- Marketing materials
- Documentation
- Light mode / dark mode
- Grayscale and print

### Prohibited
- Stretching or skewing
- Modifying underline curvature
- Removing underline while retaining italic lean
- Adding icons, symbols, or monograms
- Coloring underline independently
- Default animation

---

## 5. Scaling & Legibility

**Minimum Sizes**
- Digital: 24px height
- Print: 10mm height

At very small sizes:
- Underline may visually flatten
- Wordmark legibility takes precedence

---

## 6. Lockups

**Primary Lockup**
- Wordmark with underline only

No alternate lockups.
No standalone symbol.
No monogram.

If an icon is required (favicon, app icon):
- Use the wordmark alone
- Centered
- Underline may be omitted below ~16px if clarity suffers

---

## 7. Implementation Notes

- Deliver as vector (SVG)
- All strokes expanded to outlines
- Clean paths only
- Pixel-fit underline at common UI sizes (24, 32, 48)

---

## 8. Brand Intent (Invariant)

This identity must always communicate:
- Calm authority
- Experience
- Technical credibility
- Motion without urgency
- Confidence without noise

Any future change that increases loudness, trendiness, or overt “AI” signaling is considered a regression.

---

## 9. UI Scaling & Application Guidance

This section defines how the Yanzi wordmark scales across UI, product, and application contexts. These rules are mandatory to preserve clarity and visual discipline.

---

### 9.1 Primary Logo (Full Wordmark + Underline)

**Use cases**
- App chrome (top-left header)
- Marketing pages
- Documentation headers
- Login or splash screens

**Recommended sizes**
- Desktop header: 28–36px height
- Marketing hero: 48–72px height
- Documentation: 24–28px height

**Rules**
- Underline must be present
- Lean must be preserved
- No cropping or distortion

---

### 9.2 UI-Compact Logo (Wordmark, underline optional)

**Use cases**
- Sidebars
- Dense layouts
- Tables, panels, settings pages

**Size range**
- 18–24px height

**Rules**
- If underline remains crisp, retain it
- If underline blurs or aliases, remove it
- Never thicken or modify underline to preserve visibility

Wordmark-only usage is approved in compact UI contexts.

---

### 9.3 App Icon & Favicon Strategy

No symbol or monogram is introduced.

#### Tier A — Wordmark Crop (Preferred)

**Use cases**
- App icons ≥ 32×32
- Desktop dock icons
- PWAs

**Rules**
- Use `yanzi` wordmark only
- No underline
- Centered
- Monochrome
- Generous padding

#### Tier B — Initial Fallback

**Use cases**
- Favicons ≤ 16×16

**Rules**
- Use lowercase `y`
- Same typeface
- No underline
- Monochrome
- Centered

This is a legibility fallback, not a logo variant.

---

### 9.4 Padding & Safe Area

- Minimum padding: 1× x-height on all sides
- App icons should favor additional padding over tight fit

---

### 9.5 Dark / Light Mode

- Light backgrounds: black logo
- Dark backgrounds: white logo
- No opacity, shadows, outlines, or effects

---

### 9.6 Asset Set (Required)

The following SVG assets must be exported and maintained:

- `yanzi-wordmark.svg`
- `yanzi-wordmark-no-underline.svg`
- `yanzi-y.svg` (lowercase y fallback)

All assets must use expanded paths with no strokes.
