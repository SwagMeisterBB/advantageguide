# Design System — AdvantageGuide

## Product Context
- **What this is:** An editorially reviewed Medicare Advantage benefits guide helping members discover and claim covered home health products
- **Who it's for:** Seniors and Medicare Advantage beneficiaries — readability and trust are paramount
- **Space/industry:** Medicare health benefits, consumer health information
- **Project type:** Editorial/content site with interactive product discovery tool
- **Peers:** Medicare.gov, NerdWallet Medicare, Boomer Benefits, AARP

## Aesthetic Direction
- **Direction:** Editorial/Magazine
- **Decoration level:** Intentional — subtle warmth through background tones and card treatments, not flat and sterile, not busy
- **Mood:** A trustworthy health publication, not a SaaS dashboard. Think Consumer Reports meets AARP Bulletin. Warm, authoritative, approachable.
- **Reference sites:** Medicare.gov (Open Sans + Bitter pairing, warm approach), GoodRx (humanized healthcare design)

## Typography
- **Display/Hero:** Merriweather (serif) — warm, authoritative, highly readable at large sizes. Signals "editorial publication" not "startup landing page." (Originally spec'd as Bitter; Merriweather was chosen during implementation for its superior readability at heading sizes.)
- **Body:** Source Sans 3 — Adobe's open-source humanist sans-serif. Wider letterforms than Inter, better readability at 18px+ for older eyes.
- **UI/Labels:** Source Sans 3 semibold
- **Data/Tables:** Source Sans 3 (supports tabular-nums)
- **Code:** Not applicable (no code on this site)
- **Loading:** Google Fonts CDN — `https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+3:wght@300;400;500;600;700;800&display=swap`
- **Scale:**
  - H1: 48px / 3rem — Merriweather 700, line-height 1.15, letter-spacing -0.02em
  - H2: 32px / 2rem — Merriweather 700, line-height 1.2
  - H3: 22px / 1.375rem — Merriweather 600, line-height 1.3
  - Body: 18px / 1.125rem — Source Sans 3 400, line-height 1.65
  - Small: 15px / 0.9375rem — Source Sans 3 400, line-height 1.55
  - Caption: 13px / 0.8125rem — Source Sans 3 600, letter-spacing 0.02em, uppercase
  - UI Label: 14px / 0.875rem — Source Sans 3 600, letter-spacing 0.01em

### Senior Readability Rules
- Minimum body text: 18px (never smaller for primary content)
- Minimum touch target: 48px (buttons, links, interactive elements)
- Always support the existing A+/A- text size controls
- No decorative flourishes that complicate character recognition

## Color
- **Approach:** Restrained — color is meaningful when it appears, not decorative
- **Primary:** #1E5FAD — deeper, warmer blue. More authoritative than electric blue. Used for links, selected states, primary buttons.
- **Primary Dark:** #154A8A — hover/active states for primary elements
- **Primary Light:** #E8F0FA — selected card backgrounds, info alert backgrounds
- **Accent:** #B45309 — warm amber for CTAs and highlights. Stands out from the sea of blue in the Medicare space.
- **Accent Light:** #FEF3E2 — warning backgrounds, accent card tints
- **Background:** #FDFAF6 — warm cream instead of cold gray-50. Feels editorial, not tech.
- **Card Background:** #FFFFFF
- **Text:** #3D3935 — warm dark gray, not pure black
- **Text Heading:** #2A2623 — slightly darker for headings
- **Text Secondary:** #8A8580 — metadata, captions, secondary info
- **Border:** #E5E0DA — warm gray borders
- **Border Light:** #F0EDE8 — subtle separators
- **Semantic:**
  - Success: #1A7431 (bg: #E8F5EC) — "Your plan covers this"
  - Warning: #B45309 (bg: #FEF3E2) — "Coverage varies"
  - Error: #C43B2F (bg: #FDE8E6) — "Requires prior authorization"
  - Info: #1E5FAD (bg: #E8F0FA) — general informational callouts
- **Dark mode strategy:** CSS custom properties swap. Reduce saturation 10-20%, lighten text, darken surfaces. See preview file for full dark palette.

### Badge Colors (product categories)
- DME: success green (#E8F5EC / #1A7431)
- Home Safety: info blue (#E8F0FA / #1E5FAD)
- OTC: purple (#F3E8FF / #7C3AED)
- Out-of-Pocket: neutral (#F3F4F6 / #4B5563)
- Editorially Reviewed: primary light (#E8F0FA / #1E5FAD)

## Spacing
- **Base unit:** 8px
- **Density:** Comfortable — seniors benefit from generous breathing room
- **Scale:** 2xs(2px) xs(4px) sm(8px) md(16px) lg(24px) xl(32px) 2xl(48px) 3xl(64px)
- **Card padding:** 24px minimum (32px preferred)
- **Card gap:** 24px
- **Section padding:** 48px vertical

## Layout
- **Approach:** Grid-disciplined — strict max-width, predictable card grid. Every page should feel like the same site.
- **Grid:** Single column (content) with card grids for product listings
- **Max content width:** 64rem (1024px) for content, 80rem (1280px) for full-width sections
- **Border radius:** sm: 4px, md: 8px, lg: 12px, full: 9999px (pills only)
- **Breakpoints:** Mobile-first. Cards stack to single column below 640px.

## Motion
- **Approach:** Minimal-functional — motion only aids comprehension
- **Easing:** enter(ease-out) exit(ease-in) move(ease-in-out)
- **Duration:** micro(50-100ms) short(150-250ms) medium(250-400ms)
- **Current animation:** 0.25s fadeIn with 6px translateY — keep this, it works
- **Rules:** No scroll animations. No parallax. No bouncing. No auto-playing anything. Seniors should never feel disoriented by motion.

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-21 | Initial design system created | Created by /design-consultation. Researched Medicare.gov design system, senior UX guidelines, and competitor landscape. Moved from Inter + electric blue to Bitter + Source Sans 3 + warm editorial palette. |
| 2026-03-21 | Chose Bitter for headlines | Same slab serif family used by Medicare.gov. Warm, authoritative, readable at large sizes. Signals editorial credibility. |
| 2026-03-21 | Chose Source Sans 3 for body | Wider letterforms than Inter, better readability at 18px+ for older eyes. Adobe open-source, excellent Google Fonts support. |
| 2026-03-21 | Warm cream background (#FDFAF6) | Moves site out of "generic AI-generated" cold gray territory into editorial warmth. Reduces eye strain for extended reading. |
| 2026-03-21 | Amber accent (#B45309) for CTAs | Differentiates from the wall-to-wall blue in the Medicare web space. High-contrast on white (4.6:1). Demands attention for conversion actions. |
