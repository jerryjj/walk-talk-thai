#!/usr/bin/env python3
"""
Walk & Talk Thai — episode generator.

Generates one MP3 episode per "week" entry in vocab.json, using free Edge TTS
voices, and (re)builds an RSS podcast feed so any podcast app can subscribe.

Usage:
    python generator.py                 # generate any episodes not yet built, rebuild feed
    python generator.py --week 3        # (re)generate only week 3
    python generator.py --feed-only     # just rebuild feed.xml from existing MP3s

Requires: edge-tts, pydub, feedgen   (and ffmpeg on PATH for pydub)
"""

import argparse
import asyncio
import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

import edge_tts
from pydub import AudioSegment
from feedgen.feed import FeedGenerator

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
ROOT = Path(__file__).parent
VOCAB_PATH = ROOT / "vocab.json"
OUT_DIR = ROOT / "public"          # everything here gets published (feed + mp3s)
AUDIO_DIR = OUT_DIR / "episodes"
TMP_DIR = ROOT / ".tmp_audio"

TH_VOICE = "th-TH-PremwadeeNeural"   # Thai narration
EN_VOICE = "en-US-AriaNeural"        # English narration

SLOW_RATE = "-40%"     # for the slow pass of Thai
NATURAL_RATE = "+0%"

# Silence durations (milliseconds)
GAP_SHORT = 400        # between sub-segments of one word
GAP_WORD = 700         # between words
GAP_REPEAT = 2200      # pause for the learner to repeat aloud
GAP_SECTION = 1200     # around intro/recap/outro

# Launch date for episode 1; each week is published 7 days apart.
SERIES_START = datetime(2026, 1, 5, 9, 0, tzinfo=timezone.utc)


# ----------------------------------------------------------------------------
# TTS helpers
# ----------------------------------------------------------------------------
async def _tts(text: str, voice: str, rate: str, path: Path):
    """Render one phrase to an mp3 file via Edge TTS.

    The Edge endpoint intermittently returns an empty stream
    (NoAudioReceived); retry a few times with backoff before giving up so a
    single hiccup doesn't discard a whole episode's worth of work.
    """
    last_err = None
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
            await communicate.save(str(path))
            if path.exists() and path.stat().st_size > 0:
                return
            last_err = RuntimeError("empty audio file")
        except edge_tts.exceptions.NoAudioReceived as e:
            last_err = e
        await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"edge-tts failed after 5 attempts for {text!r}: {last_err}")


def say(text: str, voice: str, rate: str, idx: list) -> AudioSegment:
    """Synthesise text and return it as an AudioSegment. idx is a 1-elem
    counter list so each tmp file gets a unique name."""
    idx[0] += 1
    p = TMP_DIR / f"seg_{idx[0]:04d}.mp3"
    asyncio.run(_tts(text, voice, rate, p))
    return AudioSegment.from_file(p, format="mp3")


def silence(ms: int) -> AudioSegment:
    return AudioSegment.silent(duration=ms)


# ----------------------------------------------------------------------------
# Episode assembly
# ----------------------------------------------------------------------------
def build_word_block(word: dict, idx: list) -> AudioSegment:
    """One vocabulary item, taught in the standard loop."""
    block = AudioSegment.empty()

    # 1. English word -> Thai (slow)
    block += say(word["en"], EN_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)
    block += say(word["th"], TH_VOICE, SLOW_RATE, idx) + silence(GAP_SHORT)
    # 2. Thai again, natural speed
    block += say(word["th"], TH_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)

    # 3. Example sentence: slow then natural
    block += say(word["sentence_th"], TH_VOICE, SLOW_RATE, idx) + silence(GAP_SHORT)
    block += say(word["sentence_th"], TH_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)
    # 4. English meaning
    block += say(word["sentence_en"], EN_VOICE, NATURAL_RATE, idx)

    # 5. Repeat-aloud pause
    block += silence(GAP_REPEAT)
    return block


def build_recap(words: list, idx: list) -> AudioSegment:
    block = say("Let's quickly review today's ten words.", EN_VOICE, NATURAL_RATE, idx)
    block += silence(GAP_SECTION)
    for w in words:
        block += say(w["en"], EN_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)
        block += say(w["th"], TH_VOICE, NATURAL_RATE, idx) + silence(GAP_WORD)
    return block


def build_step_block(step: dict, idx: list) -> AudioSegment:
    """One step inside a sentence-builder stem: slow Thai, natural Thai, English, pause."""
    block = AudioSegment.empty()
    block += say(step["th"], TH_VOICE, SLOW_RATE, idx) + silence(GAP_SHORT)
    block += say(step["th"], TH_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)
    block += say(step["en"], EN_VOICE, NATURAL_RATE, idx)
    block += silence(GAP_REPEAT)
    return block


def build_builder_recap(stems: list, idx: list) -> AudioSegment:
    block = say("Let's review the full sentences.", EN_VOICE, NATURAL_RATE, idx)
    block += silence(GAP_SECTION)
    for stem in stems:
        full = stem["steps"][-1]
        block += say(full["en"], EN_VOICE, NATURAL_RATE, idx) + silence(GAP_SHORT)
        block += say(full["th"], TH_VOICE, NATURAL_RATE, idx) + silence(GAP_WORD)
    return block


def build_vocab_episode(ep: dict, idx: list) -> AudioSegment:
    week, theme, words = ep["week"], ep["theme"], ep["words"]

    intro = say(
        f"Welcome to Walk and Talk Thai, week {week}. "
        f"Today's theme is {theme}. Here are ten useful words. "
        f"After each one, you'll hear a pause. Say it out loud.",
        EN_VOICE, NATURAL_RATE, idx,
    ) + silence(GAP_SECTION)

    body = AudioSegment.empty()
    for w in words:
        body += build_word_block(w, idx) + silence(GAP_WORD)

    recap = silence(GAP_SECTION) + build_recap(words, idx)

    outro = silence(GAP_SECTION) + say(
        "That's it for this week. Keep practising on your next walk. See you again!",
        EN_VOICE, NATURAL_RATE, idx,
    )

    return intro + body + recap + outro


def build_builder_episode(ep: dict, idx: list) -> AudioSegment:
    week, theme, stems = ep["week"], ep["theme"], ep["stems"]

    intro = say(
        f"Welcome to Walk and Talk Thai, week {week}. "
        f"Today we'll build up sentences step by step on the theme: {theme}. "
        f"Each sentence grows by one piece. After each Thai phrase you'll hear a pause. Say it out loud.",
        EN_VOICE, NATURAL_RATE, idx,
    ) + silence(GAP_SECTION)

    body = AudioSegment.empty()
    for stem in stems:
        body += say(stem["intro_en"], EN_VOICE, NATURAL_RATE, idx) + silence(GAP_SECTION)
        for step in stem["steps"]:
            body += build_step_block(step, idx)
        body += silence(GAP_SECTION)

    recap = silence(GAP_SECTION) + build_builder_recap(stems, idx)

    outro = silence(GAP_SECTION) + say(
        "That's it for this week. Try those sentences on your next walk. See you again!",
        EN_VOICE, NATURAL_RATE, idx,
    )

    return intro + body + recap + outro


def build_episode(ep: dict, idx: list) -> AudioSegment:
    kind = ep.get("kind", "vocab")
    if kind == "builder":
        return build_builder_episode(ep, idx)
    return build_vocab_episode(ep, idx)


# ----------------------------------------------------------------------------
# Feed
# ----------------------------------------------------------------------------
def episode_filename(week: int) -> str:
    return f"episode_{week:02d}.mp3"


def mp3_duration(path: Path) -> str:
    """Return HH:MM:SS duration of an mp3 via ffprobe (ships with ffmpeg)."""
    out = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    secs = int(float(out))
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_feed(cfg: dict, episodes: list):
    pod = cfg["podcast"]
    base = pod["base_url"].rstrip("/")
    feed_url = f"{base}/feed.xml"

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(pod["title"])
    # feedgen quirk: the rendered RSS <link> takes whichever entry is LAST,
    # so put the canonical site link last and the atom:self link first.
    fg.link([
        {"href": feed_url, "rel": "self"},
        {"href": base, "rel": "alternate"},
    ])
    fg.description(pod["description"])
    fg.language(pod["language"])
    fg.author({"name": pod["author"], "email": pod.get("owner_email", "")})
    fg.podcast.itunes_author(pod["author"])
    fg.podcast.itunes_summary(pod["description"])
    fg.podcast.itunes_category("Education", "Language Learning")
    fg.podcast.itunes_explicit("no")              # required by Apple
    fg.podcast.itunes_type("episodic")
    if pod.get("owner_email"):
        fg.podcast.itunes_owner(name=pod["author"], email=pod["owner_email"])
    if pod.get("image_url"):
        fg.image(pod["image_url"])
        fg.podcast.itunes_image(pod["image_url"])

    # Newest first is conventional; feedgen reverses internally when needed.
    for ep in episodes:
        week = ep["week"]
        fn = episode_filename(week)
        mp3_path = AUDIO_DIR / fn
        if not mp3_path.exists():
            continue
        url = f"{base}/episodes/{fn}"
        pub = SERIES_START + timedelta(days=7 * (week - 1))

        # Show notes: differ by episode kind.
        notes_lines = [f"Theme: {ep['theme']}", ""]
        if ep.get("kind") == "builder":
            notes_lines.append("Sentences we build this week:")
            for stem in ep["stems"]:
                for step in stem["steps"]:
                    notes_lines.append(
                        f"  {step['th']} ({step['roman']}) — {step['en']}"
                    )
                notes_lines.append("")
        else:
            notes_lines.append("Words this week:")
            for w in ep["words"]:
                notes_lines.append(
                    f"- {w['en']} — {w['th']} ({w['roman']})  |  "
                    f"{w['sentence_th']} ({w['sentence_roman']}) — {w['sentence_en']}"
                )
        notes = "\n".join(notes_lines)

        fe = fg.add_entry()
        fe.id(url)
        fe.title(f"Week {week}: {ep['theme']}")
        fe.description(notes)
        fe.enclosure(url, str(mp3_path.stat().st_size), "audio/mpeg")
        fe.published(pub)
        fe.podcast.itunes_summary(notes)
        fe.podcast.itunes_explicit("no")          # required by Apple per-item
        fe.podcast.itunes_duration(mp3_duration(mp3_path))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fg.rss_file(str(OUT_DIR / "feed.xml"), pretty=True)
    print(f"Wrote {OUT_DIR / 'feed.xml'}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def generate_episode_file(ep: dict):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    idx = [0]
    print(f"Generating week {ep['week']}: {ep['theme']} ...")
    audio = build_episode(ep, idx)
    out = AUDIO_DIR / episode_filename(ep["week"])
    audio.export(out, format="mp3", bitrate="96k")
    # clean tmp
    for f in TMP_DIR.glob("seg_*.mp3"):
        f.unlink()
    dur_min = len(audio) / 60000
    print(f"  -> {out}  ({dur_min:.1f} min)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, help="only (re)build this week")
    ap.add_argument("--feed-only", action="store_true", help="rebuild feed only")
    args = ap.parse_args()

    cfg = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    episodes = cfg["episodes"]

    if not args.feed_only:
        for ep in episodes:
            if args.week and ep["week"] != args.week:
                continue
            target = AUDIO_DIR / episode_filename(ep["week"])
            if args.week is None and target.exists():
                continue  # skip already-built weeks unless forced
            generate_episode_file(ep)

    build_feed(cfg, episodes)


if __name__ == "__main__":
    main()
