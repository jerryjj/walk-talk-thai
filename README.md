# Walk & Talk Thai

A self-hosted weekly Thai-learning podcast. Each episode teaches 10 everyday
words inside real sentences (slow → natural, with a pause to repeat aloud),
plus a recap. Subscribe in any podcast app for auto-downloaded offline episodes.

## Layout

```
vocab.json        # all weeks of vocabulary (edit this to add content)
generator.py      # builds MP3 episodes + RSS feed
requirements.txt  # edge-tts, pydub, feedgen
build.yml         # -> move to .github/workflows/build.yml for weekly cron
public/           # published output (feed.xml + episodes/*.mp3)
```

## One-time setup

1. **Create a GitHub repo** and push these files. Put `build.yml` at
   `.github/workflows/build.yml`.
2. **Edit `vocab.json`** → set `base_url` to your GitHub Pages URL,
   e.g. `https://YOURNAME.github.io/walk-talk-thai`.
3. **Enable GitHub Pages** on the repo: Settings → Pages → deploy from branch,
   folder `/public` (or use a Pages action). The feed will live at
   `<base_url>/feed.xml`.
4. (Optional) add a square `cover.jpg` (1400–3000px) to `public/` for cover art.

## Local test

```bash
pip install -r requirements.txt   # needs ffmpeg installed too
python generator.py               # builds any new weeks + feed.xml
python generator.py --week 1      # force-rebuild one week
python generator.py --feed-only   # rebuild feed only
```

Listen to `public/episodes/episode_01.mp3` and tune the pacing constants near
the top of `generator.py` (`SLOW_RATE`, `GAP_REPEAT`, etc.) on an actual walk.

## Subscribe

In your podcast app choose "Add by URL" / "Add RSS feed" and paste
`<base_url>/feed.xml`. New episodes appear weekly.

## Adding content

Append objects to `episodes[]` in `vocab.json` (increment `week`). Each word
needs `en`, `th`, `roman`, `sentence_th`, `sentence_roman`, `sentence_en`.
The weekly cron picks up the next unbuilt week automatically.

## Notes

- Voices: `th-TH-PremwadeeNeural` (female) / `th-TH-NiwatNeural` (male). Swap
  `TH_VOICE` in `generator.py` to change. English narration uses an English
  voice so the two languages sound distinct.
- Thai is tonal — Edge TTS handles tones reasonably, but always spot-check new
  sentences by ear; the romanization in `vocab.json` is your reference.
