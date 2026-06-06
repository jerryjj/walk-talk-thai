# Walk Talk Thai — Brand System v1

*Prepared 2026-06-04 · By Niran, Marketing Specialist*

---

## Brand Read

Reading this as: **cultural language-learning brand for curious adults (expats in Thailand, tourists, heritage learners), in a warm tropical-editorial visual world, with no regulated-industry constraints and a strong differentiation mandate against clinical and juvenile competitors.**

---

## Strategy

- **Represents**: Joyful Thai immersion — language learning that opens doors to real human connection, absorbed in motion.
- **For**: The curious adult who wants to *speak* Thai, not just study it — expats building a life in Thailand, tourists going deeper than the tourist trail, heritage learners reconnecting with their roots. Not the grammar-obsessed student; the person who learns while moving.
- **Core metaphor**: *The walk as a living classroom.* Every step is a new word; every street, a new conversation. Language is not memorized at a desk — it moves with you.
- **Avoids**: Pimsleur's sterile corporate audio-course aesthetic; Duolingo's streak-anxiety gamification and green-owl infantilism; generic "Asia" visual clichés (chopstick fonts, lotus flowers, red-and-gold iconography); Thai tourism board pastels; flat SaaS blue-and-white; any look that could belong to a corporate language app.
- **Position**: Warm challenger — boutique, culturally specific, and human-first — against clinical giants (Pimsleur) and chaotic DIY alternatives (YouTube channels).

---

## Logo Direction

**Method chosen**: Method 3 — Metaphor Fusion (primary) + Method 2 — Product Action (secondary).
**Why**: The brand's core metaphor — walking + learning + Thai cultural specificity — is strong enough to fuse into a single ownable mark. The product action (speaking while moving) provides functional grounding without being literal.

---

### Concept A — "The Talking Path" *(Wordmark-led)*

A pure wordmark lockup. "Walk Talk Thai" is set in Kanit Bold in a single horizontal line, word-spaced with a natural rhythm that mirrors the three-beat cadence of the name. The sole design detail: the counter of the "a" in "Talk" is replaced by a micro waveform — three short horizontal bars, like a sound-equalizer pulse — rendered in the teal accent (`#2a8873`). The word "Thai" is set in the saffron-amber accent (`#d4891a`) rather than the cream foreground color, creating an effortless hierarchy: this is *specifically* about Thai. No separate icon is needed; the waveform-in-letterform IS the detail that rewards close inspection. Scales cleanly from a 55px podcast thumbnail to a full-width billboard. The waveform signals "audio" without the cliché of a literal microphone.

---

### Concept B — "The Footstep Glyph" *(Icon + Wordmark)* ⭐ Preferred

A two-part lockup: a standalone icon mark above the wordmark. The icon is an abstract geometric shape derived from the flowing, path-like calligraphic structure of the Thai consonant ว (waw) — but crucially, *not* a reproduction of that character. The two looping strokes of ว are redrawn as two smooth forward-curving arcs that read simultaneously as footsteps advancing on a path. The result is a mark that carries the feeling of Thai calligraphic rhythm and forward motion without copying sacred script directly. Rendered in amber (`#d4891a`) on the deep base, it is warm, specific, and unmistakably purposeful. The wordmark "Walk Talk Thai" in Kanit Medium sits beneath with slight additional letter-spacing. The icon functions independently as a favicon, app icon, and social avatar. This mark occupies visual territory no language-learning competitor currently holds — the fusion of Thai script lineage with a walking/movement reading is genuinely ownable.

---

### Concept C — "Stride + Signal" *(Icon + Wordmark, global variant)*

A more universal mark for future brand expansion. The icon is an abstracted walking stride: a bold diagonal slash representing a footstep, with a semi-circular arc above it that reads simultaneously as a headphone ear-cup and a speech bubble opening. The whole composition is optionally contained in a warm rounded-square frame. Wordmark in Kanit Medium below. This is the most legible mark at very small sizes and the most flexible if the brand ever expands into other languages beyond Thai. However, it sacrifices the cultural specificity that makes Concept B distinctive. Recommended only if the brand explicitly decides to de-emphasize its Thai identity.

---

**Preferred: Concept B.**
**Reason**: Cultural specificity is a *feature*, not a risk — it makes the mark ownable and directly expresses the brand's Thai identity at a glance, while remaining abstract enough to feel designed rather than appropriated. It also gives designers a richer brief for podcast cover art, social assets, and eventual merchandise.

---

## Visual Mode

**Warm Cultural / Editorial.**
**Why**: Walk Talk Thai sits between "cultural/experimental" (energy, distinctiveness) and "dark nature / calm system" (warmth, trustworthiness). The night-market palette — deep warm darks, amber glow, teal river accent — gives the brand cinematic credibility for podcast cover art while remaining approachable in web and social contexts. Warm and human; not clinical, not dark-tech, not pastel.

---

## Color Tokens

```
--brand-base:          #18120e   /* near-black with warm amber undertone — teak, charcoal, night market backdrop */
--brand-surface:       #261c14   /* warm dark surface — cards, panels, episode tiles */
--brand-accent:        #d4891a   /* rich saffron-amber — monk robe gold, temple flame, dominant accent */
--brand-accent-2:      #2a8873   /* deep Thai teal — river water, temple jade; NOT spa turquoise */
--brand-accent-3:      #c45c3a   /* terracotta — temple clay, roof tile; tertiary warmth */
--brand-neutral:       #a09282   /* warm stone-dust — aged concrete, temple surface, secondary text */
--brand-fg:            #f7ede0   /* warm off-white — rice paper, cream; primary text on dark backgrounds */
```

**Light-surface variant** (web body, social cards with light treatment):
```
--brand-base-light:    #fdf8f2   /* warm cream / rice paper */
--brand-surface-light: #f3e8d8   /* warm sand */
```

**Usage discipline**:
- `--brand-accent` (amber `#d4891a`) is the dominant accent: headlines, CTAs, icon color, podcast cover dominant
- `--brand-accent-2` (teal `#2a8873`) is the secondary accent: links, highlights, supporting UI elements, geometric details
- `--brand-accent-3` (terracotta `#c45c3a`) is strictly tertiary: use as a warm shadow or a single supporting element; never pair all three accents in one composition
- Never use more than two accents simultaneously in a single layout
- `--brand-fg` is primary text on dark backgrounds; use `--brand-base` text color on light backgrounds
- Saturation is deliberately below 80% across all accents — warm, rich, not garish

---

## Typography

```
display: Kanit Bold / ExtraBold   (Google Fonts — full Thai + Latin support)
body:    Sarabun Regular / SemiBold   (Google Fonts — full Thai + Latin support)
mono:    IBM Plex Mono   (Google Fonts — phonetic annotations and pronunciation guides only)
```

**Usage**:
- **Kanit ExtraBold** at ≥ 48px for podcast cover art, social card headlines, and hero text. **Kanit Bold** at 32–48px for episode titles, section headers, and marketing headlines. Kanit's geometric structure gives authority; its slight warmth avoids coldness.
- **Sarabun Regular** at 14–18px for body copy, episode descriptions, and show notes. **Sarabun SemiBold** at 16–24px for subheadings, callouts, and Thai phrase annotations.
- Both fonts include complete Thai script glyph sets — essential for mixing Latin and Thai text on web, social, and in-app.
- **IBM Plex Mono** exclusively for romanized pronunciation guides (e.g., `sà-wàt-dee`), phonetic IPA, or vocabulary tables. Use sparingly; it signals technical precision, not the brand's general warmth.
- Never mix Kanit and Sarabun at similar optical sizes — maintain a clear minimum 1.5× size ratio between display and body.
- Line height: 1.4× for body (Sarabun); 1.1× for display (Kanit headlines).

---

## Tagline Candidates

1. **"Learn Thai. Keep walking."** — Short, imperative, double meaning: persevere on the language AND keep your literal walk going. Encouraging without hype. The most ownable option.
2. **"Real Thai, one step at a time."** — Emphasizes authenticity (counters Pimsleur's artificiality) and patience. Appeals to both absolute beginners and intermediate learners who are frustrated with gamified apps.
3. **"Thai that travels with you."** — Focuses on mobility and accessibility; resonates with expats and tourists in transit. Warm, practical, slightly poetic.
4. **"Move. Listen. Speak Thai."** — Three-step action sequence mirroring the podcast format itself (walk, hear, repeat). Energetic and instructional without feeling textbook.
5. **"Every step, a new word."** — Visual, optimistic, beginner-friendly. Works at episode level as well as brand level — versatile for social cards.

**Preferred: #1 — "Learn Thai. Keep walking."**
**Reason**: The verb "keep walking" operates on two registers simultaneously — persevere (language learning is a long walk) and literally continue your walk — which is rare in a tagline. It acknowledges that language learning is genuinely hard and responds with encouragement rather than hype or false ease. It differentiates directly from Duolingo's gamified streak anxiety and Pimsleur's clinical authority.

---

## Application Targets

Where this brand needs to show up, in priority order:

1. **Podcast cover art** — 3000×3000px, Apple Podcasts / Spotify compliant — highest-visibility asset, always shown first
2. **Social profile images** — Instagram, Facebook — 1:1 format derived from cover art master
3. **Episode social cards** — 1200×630px template for Instagram Stories and Twitter/X link previews — recurring asset needing a repeatable template
4. **Website** — jerryjj.github.io/walk-talk-thai — header, color system, type stack, episode listing
5. **Podcast chapter art** — optional in-episode visual reinforcement for apps that display chapter thumbnails

---

## Podcast Cover Art — Creative Brief

**Project**: Walk Talk Thai — Podcast Cover Art v1
**Deliverable**: 1 primary cover image (+ layered source file)
**Dimensions**: 3000 × 3000 px
**Format**: JPEG max 500KB (export at 85% quality sRGB) + PNG backup
**Color space**: RGB (sRGB)
**Platform specs**: Apple Podcasts compliant; must legibly render the brand name at 55×55px (smallest thumbnail) and 300×300px (typical mobile grid)

---

### Art Direction

**Mood**: Cinematic warmth. Imagine a traveler pausing at a Bangkok side street at dusk — amber lanterns casting warm pools of light on worn stone, a faint suggestion of Thai shophouse script in the background, someone moving forward with earbuds in. Not a tourist brochure. Not a textbook cover. A place you want to go back to.

**Preferred composition**:

1. **Background**: Full-bleed deep dark (`#18120e`). No gradients at the macro level — the darkness is flat and rich, like a proper cinema letterbox.
2. **Glow element**: A large soft-edged amber circle or oval (~1400–1600px diameter) positioned center-upper third of the canvas. This is the lantern/light metaphor — it should feel like a warm light source, not a graphic shape. Use a radial gradient from `#d4891a` (core) fading to `#18120e` (edge) over approximately 200px.
3. **Icon mark**: The Footstep Glyph (Concept B) centered within the amber glow, rendered in warm off-white (`#f7ede0`), approximately 380–420px in height. The two curved forward-moving arcs should be clean, confident strokes — not hair-thin, not overweight.
4. **Wordmark**: "Walk Talk Thai" in **Kanit ExtraBold**, centered below the glow element, in `#f7ede0`. Approximate type size: 160–200px. "Thai" may optionally be set in `#d4891a` (amber) to reinforce the linguistic identity — test both treatments.
5. **Tagline**: "Learn Thai. Keep walking." in **Sarabun SemiBold**, centered, in `#a09282` (warm stone-dust neutral). Approximate type size: 52–64px. Sufficient vertical spacing below the wordmark (~80px gap).
6. **Accent line**: A single horizontal rule in `#2a8873` (teal), 4px weight, approximately 560px wide, centered — positioned between the wordmark and the tagline. This introduces the teal accent without competing with the amber dominant.
7. **Optional texture layer**: A subtle Thai textile diamond-weave or silk grid pattern at 4–6% opacity over the full background. Adds material depth and a handcrafted quality without competing with the typography. Use a warm-tone monochrome texture only.
8. **Optional Thai script element**: The Thai transliteration วอล์คทอล์คไทย in **Kanit ExtraBold** at very large scale (700–900px type size), set at approximately 8–10% opacity, centered vertically as a soft background texture layer beneath all other elements. This grounds the cover in Thai culture without asking for legibility.

---

### What to Avoid

- Clip art Thai imagery: no temples, no elephants, no lotus flowers, no tuk-tuks, no literal Thai flag elements
- Gradients that read "generic podcast" (the multi-color app-store default)
- Light or white backgrounds — this cover must read on dark app interfaces (Overcast dark mode, Spotify, Apple Podcasts dark UI)
- Any text set below 80px — nothing smaller than the tagline line
- More than 3 typefaces or 4 distinct colors in the final composition
- Drop shadows, bevels, lens flare, or any photographic stock asset

---

### Typography on Cover

| Element | Font | Weight | Size | Color |
|---|---|---|---|---|
| Wordmark | Kanit | ExtraBold | ~180px | `#f7ede0` |
| "Thai" (optional accent) | Kanit | ExtraBold | same | `#d4891a` |
| Tagline | Sarabun | SemiBold | ~58px | `#a09282` |
| Background Thai script (optional) | Kanit | ExtraBold | ~800px | `#f7ede0` @ 9% opacity |

---

### Color Usage on Cover

| Role | Hex | Name |
|---|---|---|
| Background | `#18120e` | Night |
| Glow / dominant accent | `#d4891a` | Saffron |
| Icon + wordmark | `#f7ede0` | Rice Paper |
| Secondary text / tagline | `#a09282` | Stone Dust |
| Accent rule | `#2a8873` | River |
| Warm shadow on glow (optional) | `#c45c3a` | Temple Clay |

---

### Designer Checklist

- [ ] Export and test at 55×55px — "Walk Talk Thai" wordmark in Kanit ExtraBold must still be legible (the font is designed for small-size strength)
- [ ] Test on both dark and light podcast app interfaces: Apple Podcasts (light + dark), Spotify (dark), Overcast (dark)
- [ ] All fonts sourced from Google Fonts — no commercial font licensing needed
- [ ] No copyrighted photography or third-party illustration
- [ ] Export as sRGB JPEG at 85% quality — verify file is under 500KB
- [ ] Also export as PNG at full resolution as backup / source master
- [ ] Deliver layered source file (Figma, Illustrator, or Photoshop) with named layers

---

## Image-Gen Prompt

*Note: Image generation is not available in this environment. The prompt below is ready to paste into DALL-E, Midjourney, Adobe Firefly, or any image-gen tool of your choice.*

```
Create a premium podcast brand-kit overview image for "Walk Talk Thai".

Brand strategy:
- category: cultural language-learning podcast
- audience: expats in Thailand, tourists preparing for a trip, heritage learners — curious adults, absolute beginners to intermediate level
- personality: warm, encouraging, culturally grounded, credible, a little playful — NOT clinical, NOT gamified, NOT juvenile
- core metaphor: the walk as a living classroom — language absorbed in motion, every step a new word
- logo idea: abstract Thai-calligraphy-inspired footstep-path glyph (two forward-moving curved arcs derived from the looping strokes of the Thai consonant ว, redrawn as footsteps advancing on a path) rendered in amber, above the wordmark "Walk Talk Thai" in a warm geometric sans

Layout:
3×3 grid on a deep warm dark (#18120e) presentation canvas with strong gutters, clean alignment, and refined negative space.

Panels:
1. Logo cover: large soft amber glow circle, footstep glyph icon centered in cream-white, wordmark "Walk Talk Thai" below in warm off-white, tagline "Learn Thai. Keep walking." in muted warm grey, minimal composition, deep dark background
2. Logo construction: breakdown of the footstep glyph showing the two forward-curving arcs derived from Thai calligraphic stroke structure, geometric grid, construction lines, amber marks on dark field
3. Digital application: podcast app interface mockup (dark UI, Spotify or Overcast style), showing the cover art thumbnail and episode list in brand typography — Kanit titles, Sarabun body, amber accent chips
4. Brand essence / tagline panel: "Learn Thai. Keep walking." in Kanit ExtraBold, very large, centered, deep dark background, amber underline accent, warm off-white text
5. Color system: six branded color swatches — Night (#18120e), Saffron (#d4891a), River (#2a8873), Temple Clay (#c45c3a), Stone Dust (#a09282), Rice Paper (#f7ede0) — labeled with both names and hex codes
6. Typography specimen: large Thai + Latin type sample — Kanit ExtraBold display "วอล์คทอล์คไทย / Walk Talk Thai", Sarabun Regular body text sample mixing Thai and Latin script naturally
7. Physical application: podcast cover art 3000×3000px mockup shown in square format, dark amber teal composition, cinematic
8. Image direction: cinematic Thai street scene — warm amber lanterns at dusk, motion blur of a person walking with earbuds, warm incandescent light on worn stone, editorial photography style, NOT tourist stock photo, NOT generic Asia cliché
9. System detail: episode card UI strip — amber episode number chip, Kanit episode title, Sarabun duration and description text, teal accent bar, dark card surface

Visual mode:
Warm cultural / editorial. Deep dark panels with amber glow accents. Rich and cinematic, not tech/developer dark. Thai street warmth, not corporate.

Palette:
#18120e (Night), #d4891a (Saffron), #2a8873 (River), #c45c3a (Temple Clay), #a09282 (Stone Dust), #f7ede0 (Rice Paper)

Style:
Premium, sparse, cinematic, intentional, polished brand-guidelines deck. No clutter. No clip-art Thai imagery (absolutely no elephants, no lotus flowers, no temples as decorative elements, no chopstick fonts). Warm editorial photography sensibility. Feels like a boutique travel journal crossed with a premium audio product.

Typography:
Kanit ExtraBold for all display text. Sarabun Regular/SemiBold for body. High typographic hierarchy. Readable at all panel sizes. Thai script integrated naturally and proudly alongside Latin — both scripts are first-class citizens.

Logo:
Professional, symbolic, warm amber, derived from Thai calligraphic motion abstracted as two forward-moving curved strokes. Reproduced consistently across all nine panels. Never treated as clip art.
```

---

*Document version: 1.0 · Status: Draft — pending Malee (CMO) review*
*Image generation not available in current toolset — image-gen prompt above is ready for external tools.*
