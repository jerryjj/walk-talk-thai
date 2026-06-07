# PLAN: Audio player visual styling & copy — brand conformance

## Goal
Restyle the site's audio player and all surrounding UI (episode cards, hero, subscribe strip, toolbar, footer) so that every colour, typeface, and user-facing string conforms exactly to the tokens and tone defined in `docs/brand/brand-system-v1.md` and `docs/brand/podcast-listing-copy-v1.md`. The result should feel like it belongs in the "warm cultural / editorial" visual world described in those docs.

## Acceptance criteria
- [ ] Brand fonts loaded: Kanit (700, 800) for display, Sarabun (400, 600) for body; both from Google Fonts
- [ ] CSS custom-property tokens match brand palette exactly (saffron-amber `#d4891a` as dominant, teal `#2a8873` secondary, etc.)
- [ ] Light mode uses warm-cream `#fdf8f2` / `#f3e8d8` surface variant
- [ ] Dark mode uses brand base `#18120e` / `#261c14`
- [ ] Accent colours consistent in both modes (amber stays amber in dark — no arbitrary lightening)
- [ ] h1 "Walk Talk Thai" renders in Kanit Bold; body text in Sarabun
- [ ] Episode titles in Kanit Bold
- [ ] Play/Pause buttons use amber `#d4891a`; hover via `filter: brightness` (no hardcoded dark/light variants)
- [ ] User-facing copy updated: "Copy URL" → "Copy feed URL"; "No episode playing" → "Select an episode to begin"; order options simplified; footer freshened
- [ ] mediaSession artist corrected from "Walk & Talk Thai" → "Walk Talk Thai"
- [ ] Seek-bar `aria-label` and player `aria-label` updated to clearer strings
- [ ] Zero regressions in JS player logic
- [ ] PR opened with before/after screenshots

## Approach
1. Write this PLAN.md ✓
2. Create feature branch `feat/brand-player-styling`
3. Capture before-state screenshot (headless or static)
4. Rewrite `public/index.html` — CSS + HTML copy only; JS logic untouched except artist name fix
5. Verify HTML validity (quick sanity check)
6. Commit + push branch
7. Capture after-state screenshot
8. Self-review diff
9. Open GitHub PR with screenshot embeds

## Unknowns
- Whether puppeteer/playwright or a screenshot tool is available in the workspace (will check)
- GitHub push credentials (git remote may already be authenticated via SSH or token)

## Out of scope
- Podcast cover art redesign (that is the brand/design team's deliverable)
- New structural sections (no new layout blocks added)
- Feed XML or episode content changes
- Favicon replacement
