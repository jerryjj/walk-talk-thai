# PLAN: Audio player visual styling & copy — brand conformance

## Goal
Restyle the site's audio player and all surrounding UI (episode cards, hero, subscribe strip, toolbar, footer) so that every colour, typeface, and user-facing string conforms exactly to the tokens and tone defined in `docs/brand/brand-system-v1.md` and `docs/brand/podcast-listing-copy-v1.md`. The result should feel like it belongs in the "warm cultural / editorial" visual world described in those docs.

## Acceptance criteria
- [x] Brand fonts loaded: Kanit (700, 800) for display, Sarabun (400, 600) for body; both from Google Fonts
- [x] CSS custom-property tokens match brand palette exactly (saffron-amber `#d4891a` as dominant, teal `#2a8873` secondary, etc.)
- [x] Light mode uses warm-cream `#fdf8f2` / white card surface
- [x] Dark mode uses brand base `#18120e` / `#261c14`
- [x] Accent colours consistent in both modes (amber stays amber in dark — no arbitrary lightening)
- [x] h1 "Walk Talk Thai" renders in Kanit Bold; body text in Sarabun
- [x] Episode titles in Kanit Bold
- [x] Play/Pause buttons use amber `#d4891a`; hover via `filter: brightness` (no hardcoded dark/light variants)
- [x] User-facing copy updated: "Copy URL" → "Copy feed URL"; "No episode playing" → "Select an episode to begin"; order options → "Oldest first"/"Newest first"; footer freshened
- [x] mediaSession artist corrected from "Walk & Talk Thai" → "Walk Talk Thai"
- [x] Seek-bar `aria-label` and player `aria-label` updated to clearer strings; dynamic aria-label on play/pause state change
- [x] Zero regressions in JS player logic
- [x] PR opened with before/after screenshots (SVG mockups — no headless browser available in Alpine workspace)

## Approach
1. Write this PLAN.md ✓
2. Create feature branch `feat/brand-player-styling` ✓
3. Capture before-state (from git HEAD before changes) ✓
4. Rewrite `public/index.html` — CSS tokens, fonts, copy, aria-labels, player bar accent rule ✓
5. Add screenshots (SVG mockups — Puppeteer/Playwright unavailable on Alpine/musl) ✓
6. Commit + push branch → open PR ✓

## Notes on implementation
- A parallel Aegis agent committed to this branch at 09:49 UTC covering the same scope (brand fonts,
  CSS tokens, copy, mediaSession fix, episode regex updates). That commit (`7193599`) is also on this
  branch. The two implementations agreed on all design decisions, confirming the brand guidelines
  were unambiguous.
- Screenshots directory contains SVG mockups (before/after, light/dark) generated via Node.js
  string rendering. GitHub renders SVG natively in PR markdown.
- Player bar top border upgraded from `1px solid var(--line)` to `2px solid var(--accent)` —
  a brand-signal detail from the cover art brief (teal accent rule); uses amber here since
  the player is the dominant interactive surface.

## Out of scope
- Podcast cover art redesign (brand/design team deliverable)
- New structural layout sections
- Favicon replacement
