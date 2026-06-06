#!/usr/bin/env python3
"""
Extract ThaiPod101's "2000 Core Words and Phrases" PDF into structured JSON.

NOTE: the PDF embeds Thai glyphs via a custom font with a broken ToUnicode
map, so text extraction yields garbled Thai script and strips tone marks
from the romanization. We therefore extract only:

    * the entry id  (1..2000)
    * the page it lives on (for human cross-reference)
    * the romanization WITHOUT tone marks (e.g. "sa-wat-dii")
    * the English gloss

This is enough to plan a content roadmap by topic. When we curate a week
we look up the tone-correct Thai script and Haas romanization from the
source PDF visually.

Layout of one page (observed):

        x=57            x=82-90               x=220+
        +--+   +------------------------+  +------------------+
        |id|   | Thai (garbled)         |  | Thai (garbled)   |  <- y=row top
        +--+   | romanization           |  | romanization     |  <- y=row top + 22
               | English gloss          |  | English sentence |  <- y=row top + 44
               +------------------------+  +------------------+

The id is at x ~ 57, Vocabulary column lives in x ~ 80-200, Sample Sentence
column lives in x > 220. We grab only Vocabulary column ASCII text.

Usage:
    python tools/extract_core2000.py /path/to/Thai_CORE2000.pdf \
        --out corpus/core2000.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF


CONTENT_START_PAGE = 4              # 1-indexed
ID_X_MAX            = 70            # id column
VOCAB_X_MIN         = 70            # vocab column starts (some glosses begin at x~74)
VOCAB_X_MAX         = 210           # sentence column starts after this
NOISE = re.compile(
    r"^(C..RE WORDS|PAGE\s*\d+|Vocabulary|Sample Sentence|ThaiPod.*\.com)$"
)


def ascii_ratio(s: str) -> float:
    s = s.strip()
    if not s:
        return 0.0
    return sum(1 for ch in s if ord(ch) < 128) / len(s)


def is_latin(line: str) -> bool:
    return ascii_ratio(line) > 0.85


GARBLE_CHARS = set("¥¶§©®™«»·•‰‹›¦¬¯°±²³´µ¸¹º¼½¾¿×÷")
def looks_garbled(s: str) -> bool:
    """Detect the leftover Thai-glyph noise that leaks into Latin lines."""
    if not s:
        return True
    # Many "lines" are random punctuation soup like ",t" or "<:!"
    alnum = sum(1 for c in s if c.isalnum())
    if alnum < 2:
        return True
    if any(c in GARBLE_CHARS for c in s):
        return True
    return False


def clean_gloss(text: str) -> str:
    """Strip trailing garbled-glyph junk that the PDF leaks into English."""
    # Common pattern: "Hello. 61Je) 1 '¥1 'lt" — keep up to the LAST clean
    # English-looking token. We split on whitespace and walk from the end.
    tokens = text.split()
    # Trim trailing tokens that aren't plain English.
    while tokens and not re.match(r"^[A-Za-z][A-Za-z'.,!?:-]*$", tokens[-1]):
        tokens.pop()
    return " ".join(tokens).strip()


GLOSS_HINTS = re.compile(
    r"\b(the|a|an|is|are|was|were|to|of|in|on|at|with|for|you|i|my|me|"
    r"he|she|it|we|they|this|that|have|has|do|does|will|am)\b",
    re.IGNORECASE,
)


def looks_like_gloss(s: str) -> bool:
    """English-sentence glosses contain English stopwords or a trailing period
    with non-hyphenated words. Romanization is hyphen-heavy, no stopwords."""
    if not s:
        return False
    s_clean = s.strip().rstrip(".,!?")
    if "-" not in s_clean and " " in s_clean and not any(ch.isdigit() for ch in s_clean):
        # Likely "Nice to meet you" — multi-word, no hyphens.
        return True
    if GLOSS_HINTS.search(s):
        return True
    # Single-word glosses: "good", "bad", "ten" (no hyphens, all letters)
    if "-" not in s and s_clean.replace("'", "").replace(" ", "").isalpha():
        return True
    return False


def extract_page(page: fitz.Page) -> list[dict]:
    """Pull entries from one page."""
    raw_lines: list[tuple[float, float, str]] = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            text = " ".join(s["text"] for s in ln["spans"]).strip()
            if not text or NOISE.match(text):
                continue
            x0 = ln["bbox"][0]
            y0 = ln["bbox"][1]
            raw_lines.append((y0, x0, text))

    # Find IDs (left column, numeric)
    ids: list[tuple[float, int]] = []
    for y, x, t in raw_lines:
        if x < ID_X_MAX and t.isdigit() and 1 <= int(t) <= 2200:
            ids.append((y, int(t)))
    ids.sort()

    # For each id, gather vocab-column ASCII lines whose y is in the row band
    # (from this id's y to the next id's y).
    entries: list[dict] = []
    for i, (y_id, eid) in enumerate(ids):
        y_next = ids[i + 1][0] if i + 1 < len(ids) else 1e9
        vocab_lines = [
            (y, t) for (y, x, t) in raw_lines
            if VOCAB_X_MIN <= x <= VOCAB_X_MAX
            and y_id - 5 <= y < y_next - 5
            and is_latin(t)
            and not looks_garbled(t)
        ]
        vocab_lines.sort()
        roman_parts: list[str] = []
        gloss_parts: list[str] = []
        for _y, t in vocab_lines:
            if not gloss_parts and not looks_like_gloss(t):
                roman_parts.append(t)
            else:
                gloss_parts.append(t)
        if not roman_parts or not gloss_parts:
            continue
        en = clean_gloss(" ".join(gloss_parts))
        if not en:
            continue
        entries.append({
            "id": eid,
            "roman_no_tones": " ".join(roman_parts).strip(),
            "en": en,
        })
    return entries


def extract_entries(pdf_path: Path) -> list[dict]:
    out: list[dict] = []
    doc = fitz.open(pdf_path)
    for page_idx in range(CONTENT_START_PAGE - 1, doc.page_count):
        page = doc[page_idx]
        page_entries = extract_page(page)
        for e in page_entries:
            e["page"] = page_idx + 1
        out.extend(page_entries)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, default=Path("corpus/core2000.json"))
    args = ap.parse_args()

    if not args.pdf.exists():
        sys.exit(f"PDF not found: {args.pdf}")

    print(f"Reading {args.pdf} ...")
    entries = extract_entries(args.pdf)
    print(f"Extracted {len(entries)} entries.")

    ids = [e["id"] for e in entries]
    if ids:
        rng = f"{min(ids)}..{max(ids)}"
        dups = len(ids) - len(set(ids))
        missing = sorted(set(range(1, max(ids) + 1)) - set(ids))
        print(f"id range: {rng}  duplicates: {dups}  missing: {len(missing)}")
        if missing[:10]:
            print(f"  first missing: {missing[:10]}")

    seen = set()
    deduped = []
    for e in entries:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        deduped.append(e)
    entries = sorted(deduped, key=lambda e: e["id"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(entries, ensure_ascii=False, indent=2))
    print(f"Wrote {args.out}  ({len(entries)} unique entries)")


if __name__ == "__main__":
    main()
