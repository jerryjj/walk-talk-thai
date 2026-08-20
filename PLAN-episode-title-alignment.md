# PLAN: Episode title alignment with brand copy guidelines

## Goal
Align all episode titles and the episode-publishing template with the naming
convention defined in `docs/brand/podcast-listing-copy-v1.md` §5. When done,
every episode in the back-catalogue (vocab.json, feed.xml, website player) and
every future episode produced by the generator will use the canonical format:

    Ep. NN — [Situation or Topic] in Thai: [Specific Focus] (Level)

A dedicated PR (separate from the visual-styling PR #1) will carry only these
title/template changes so the scope is clear to reviewers.

## Acceptance criteria
- [ ] `generator.py`: `episode_title()` helper added; `build_feed()` uses it
      instead of the old `f"Week {week}: {ep['theme']}"` inline f-string
- [ ] Generator fallback template exactly matches the approved brand pattern
- [ ] `vocab.json`: all 12 existing episodes have an explicit `title` field
      following the brand template; no title embeds "Thai" at the start of
      the topic rather than after it (fixes Ep. 08 and Ep. 12)
- [ ] `public/feed.xml`: all 12 `<item><title>` elements renamed to match
- [ ] `public/index.html` JS: episode-number extraction regex, badge text, and
      h3-strip regex updated to parse the new `Ep. NN — …` format
- [ ] No CSS/styling/font/colour changes in this PR (those live in PR #1)

## Approach
1. Write this plan ✓
2. Checkout `feat/episode-title-alignment` from main (local branch already
   exists and is clean / equal to main)
3. Patch `generator.py` — add `episode_title()`, update `build_feed()`
4. Patch `vocab.json` — add `title` fields for all 12 eps; correct Ep. 08 and
   Ep. 12 to use `[Topic] in Thai:` pattern
5. Patch `public/feed.xml` — update the 12 `<item><title>` strings in-place
6. Patch `public/index.html` — update the three JS regex/string locations
7. Verify: diff covers only title-related lines; no stray style changes
8. Commit (sign-off), push, open PR → report URL

## Fixes needed vs feat/brand-player-styling
| Ep | Current title (on that branch)                                  | Fix |
|----|------------------------------------------------------------------|-----|
| 08 | Ep. 08 — Social Thai: 10 Words for Dating & Meeting People …   | → Social Life in Thai: … |
| 12 | Ep. 12 — Thai Tense Markers: Past, Future & Right Now …        | → Tense Markers in Thai: … |

All other 10 titles are already correct in structure.

## Unknowns
- None blocking. Feed.xml will be updated manually (generator requires MP3
  files + edge-tts, neither available in this workspace).

## Out of scope
- CSS tokens, fonts, colour palette changes (PR #1)
- Audio intro script wording — would require regenerating all MP3s
- Podcast cover art
