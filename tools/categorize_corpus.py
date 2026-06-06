#!/usr/bin/env python3
"""
Cluster corpus/core2000.json entries into proposed podcast weeks.

For each theme, lists candidate entries (id, English gloss, roman-no-tones,
page in PDF). The output is a Markdown roadmap meant for human review — pick
which 10 entries per week we actually teach, then drop them into vocab.json
with tone-correct Thai.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# Each theme is (week_number, title, type, keyword_regex_list).
# A corpus entry matches a theme if any keyword regex matches its English
# gloss. Themes are ordered; an entry can appear in multiple themes (that's
# fine — duplicates flag related concepts).
THEMES: list[tuple[int, str, str, list[str]]] = [
    (13, "At the airport & travel documents", "vocab", [
        r"\bairport\b", r"\bflight\b", r"\bpassport\b", r"\bvisa\b",
        r"\bticket\b", r"\bgate\b", r"\bsuitcase\b", r"\bluggage\b",
        r"\bcheck-in\b", r"\bboarding\b", r"\bdepart", r"\barrive",
        r"\bplane\b", r"\baeroplane\b", r"\baircraft\b", r"\btravel",
    ]),
    (14, "Hotel & accommodation", "vocab", [
        r"\bhotel\b", r"\broom\b", r"\bkey\b", r"\bbed\b", r"\bbreakfast\b",
        r"\bcheckout\b", r"\breserv", r"\bbook(ing)?\b", r"\bguest\b",
        r"\btowel\b", r"\bshower\b", r"\bswim", r"\bpool\b",
    ]),
    (15, "Family & relatives", "vocab", [
        r"\bmother\b", r"\bfather\b", r"\bchild(ren)?\b", r"\bson\b",
        r"\bdaughter\b", r"\bbrother\b", r"\bsister\b", r"\baunt\b",
        r"\buncle\b", r"\bgrandmother\b", r"\bgrandfather\b",
        r"\bcousin\b", r"\bniece\b", r"\bnephew\b", r"\bfamily\b",
        r"\bparent", r"\brelative",
    ]),
    (16, "Numbers 11–100 and counting", "vocab", [
        r"\beleven\b", r"\btwelve\b", r"\bthirteen\b", r"\bfourteen\b",
        r"\bfifteen\b", r"\bsixteen\b", r"\bseventeen\b", r"\beighteen\b",
        r"\bnineteen\b", r"\btwenty\b", r"\bthirty\b", r"\bforty\b",
        r"\bfifty\b", r"\bsixty\b", r"\bseventy\b", r"\beighty\b",
        r"\bninety\b", r"\bhundred\b", r"\bthousand\b", r"\bmillion\b",
    ]),
    (17, "Days, months & dates", "vocab", [
        r"\bmonday\b", r"\btuesday\b", r"\bwednesday\b", r"\bthursday\b",
        r"\bfriday\b", r"\bsaturday\b", r"\bsunday\b",
        r"\bjanuary\b", r"\bfebruary\b", r"\bmarch\b", r"\bapril\b",
        r"\bmay\b", r"\bjune\b", r"\bjuly\b", r"\baugust\b",
        r"\bseptember\b", r"\boctober\b", r"\bnovember\b", r"\bdecember\b",
        r"\b(year|month|week)\b",
    ]),
    (18, "Body & basic health", "vocab", [
        r"\bhead\b", r"\bhair\b", r"\beye\b", r"\bnose\b", r"\bmouth\b",
        r"\bear\b", r"\btooth\b", r"\btongue\b", r"\bneck\b",
        r"\bshoulder\b", r"\barm\b", r"\bhand\b", r"\bfinger\b",
        r"\bleg\b", r"\bfoot\b", r"\bknee\b", r"\bstomach\b",
        r"\bback\b", r"\bchest\b", r"\bbody\b", r"\bbone\b",
        r"\bdoctor\b", r"\bnurse\b", r"\bhospital\b", r"\bmedicine\b",
        r"\bsick\b", r"\bpain\b", r"\billness\b", r"\binjur",
        r"\bfever\b", r"\bcough\b",
    ]),
    (19, "At the restaurant", "vocab", [
        r"\brestaurant\b", r"\bmenu\b", r"\bwaiter\b", r"\border\b",
        r"\bbill\b", r"\bcheck\b", r"\btip\b", r"\bchopstick",
        r"\bfork\b", r"\bspoon\b", r"\bknife\b", r"\bplate\b",
        r"\bglass\b", r"\bcup\b", r"\bdessert\b", r"\bappetizer\b",
    ]),
    (20, "Fruits & vegetables", "vocab", [
        r"\bfruit\b", r"\bapple\b", r"\bbanana\b", r"\bmango\b",
        r"\borange\b", r"\bgrape\b", r"\bpapaya\b", r"\bpineapple\b",
        r"\bwatermelon\b", r"\bcoconut\b", r"\bvegetable\b", r"\bcarrot\b",
        r"\blettuce\b", r"\btomato\b", r"\bcucumber\b", r"\bpotato\b",
        r"\bonion\b", r"\bcabbage\b", r"\bcorn\b", r"\bgarlic\b",
        r"\bbell pepper\b", r"\bspinach\b",
    ]),
    (21, "Meat, fish & seafood", "vocab", [
        r"\bmeat\b", r"\bbeef\b", r"\bpork\b", r"\bchicken\b",
        r"\blamb\b", r"\bduck\b", r"\bfish\b", r"\bseafood\b",
        r"\bshrimp\b", r"\bprawn\b", r"\bcrab\b", r"\bsquid\b",
        r"\boctopus\b", r"\blobster\b", r"\bsalmon\b", r"\btuna\b",
    ]),
    (22, "Colors & sizes", "vocab", [
        r"\bred\b", r"\bblue\b", r"\bgreen\b", r"\byellow\b",
        r"\bblack\b", r"\bwhite\b", r"\bbrown\b", r"\bgray\b",
        r"\bpink\b", r"\bpurple\b", r"\borange\b",
        r"\bbig\b", r"\bsmall\b", r"\btall\b", r"\bshort\b",
        r"\blong\b", r"\bwide\b", r"\bnarrow\b", r"\bthick\b", r"\bthin\b",
    ]),
    (23, "Animals — pets & farm", "vocab", [
        r"\bdog\b", r"\bcat\b", r"\bhorse\b", r"\bcow\b", r"\bpig\b",
        r"\bsheep\b", r"\bgoat\b", r"\brabbit\b", r"\bhamster\b",
        r"\bduck\b", r"\bgoose\b", r"\bbird\b", r"\bfish\b",
    ]),
    (24, "Animals — wild", "vocab", [
        r"\belephant\b", r"\btiger\b", r"\blion\b", r"\bmonkey\b",
        r"\bbear\b", r"\bsnake\b", r"\bcrocodile\b", r"\bdeer\b",
        r"\bfox\b", r"\bwolf\b", r"\bsquirrel\b", r"\bwhale\b",
        r"\bshark\b", r"\bdolphin\b", r"\bseal\b",
    ]),
    (25, "Builder: comparisons (กว่า / ที่สุด / เท่ากัน)", "builder", []),
    (26, "Weather & seasons", "vocab", [
        r"\bweather\b", r"\brain\b", r"\bsnow\b", r"\bsun\b", r"\bsunny\b",
        r"\bcloud", r"\bwind\b", r"\bstorm\b", r"\bthunder", r"\blightning\b",
        r"\bhot\b", r"\bcold\b", r"\bcool\b", r"\bwarm\b", r"\bhumid\b",
        r"\bseason\b", r"\bsummer\b", r"\bwinter\b", r"\bspring\b", r"\bautumn\b",
    ]),
    (27, "Emotions & feelings", "vocab", [
        r"\bhappy\b", r"\bsad\b", r"\bangry\b", r"\btired\b", r"\bbored\b",
        r"\bexcit", r"\bscared\b", r"\bafraid\b", r"\bnervous\b",
        r"\bproud\b", r"\bjealous\b", r"\bsurprised\b", r"\bworried\b",
        r"\bcalm\b", r"\blove\b", r"\bhate\b", r"\bfeel\b", r"\bcry\b",
        r"\blaugh\b", r"\bsmile\b",
    ]),
    (28, "Clothes & shopping", "vocab", [
        r"\bshirt\b", r"\bt-shirt\b", r"\bpants\b", r"\btrousers\b",
        r"\bdress\b", r"\bskirt\b", r"\bsuit\b", r"\bjacket\b",
        r"\bcoat\b", r"\bshoe\b", r"\bsneaker\b", r"\bsock\b",
        r"\bhat\b", r"\bglasses\b", r"\bbelt\b", r"\bwallet\b",
        r"\bpurse\b", r"\bsize\b", r"\bbrand\b", r"\bnecktie\b",
    ]),
    (29, "House & rooms", "vocab", [
        r"\bhouse\b", r"\bbedroom\b", r"\bbathroom\b", r"\bkitchen\b",
        r"\bliving room\b", r"\bdining room\b", r"\bhallway\b",
        r"\bgarage\b", r"\bgarden\b", r"\bdoor\b", r"\bwindow\b",
        r"\bwall\b", r"\bfloor\b", r"\broof\b", r"\bstairs\b",
        r"\bcouch\b", r"\bsofa\b", r"\btable\b", r"\bchair\b",
    ]),
    (30, "Builder: polite requests (ขอ / ได้ไหม / กรุณา)", "builder", []),
    (31, "At school & university", "vocab", [
        r"\bschool\b", r"\buniversit", r"\bclass(room)?\b", r"\bstudent\b",
        r"\bteacher\b", r"\bprofessor\b", r"\bexam\b", r"\btest\b",
        r"\bhomework\b", r"\btextbook\b", r"\bnotebook\b", r"\bpencil\b",
        r"\bpen\b", r"\beraser\b", r"\bruler\b", r"\blibrary\b",
        r"\bgrade\b", r"\blesson\b", r"\bblackboard\b", r"\bwhiteboard\b",
    ]),
    (32, "Sports & exercise", "vocab", [
        r"\bsport", r"\bfootball\b", r"\bsoccer\b", r"\bbasketball\b",
        r"\btennis\b", r"\bgolf\b", r"\bswim", r"\brun\b",
        r"\byoga\b", r"\bgym\b", r"\bexercise\b", r"\bwin\b",
        r"\blose\b", r"\bgame\b", r"\bteam\b", r"\bplayer\b",
        r"\bball\b",
    ]),
    (33, "Music & entertainment", "vocab", [
        r"\bsong\b", r"\bmusic\b", r"\bconcert\b", r"\bmovie\b",
        r"\bfilm\b", r"\bbook\b", r"\bnovel\b", r"\bcomedy\b",
        r"\binstrument\b", r"\bguitar\b", r"\bpiano\b", r"\bdrum\b",
        r"\bsing\b", r"\bdance\b", r"\bband\b", r"\btheater\b",
    ]),
    (34, "Technology & devices", "vocab", [
        r"\bphone\b", r"\bmobile\b", r"\bcomputer\b", r"\blaptop\b",
        r"\btablet\b", r"\bemail\b", r"\binternet\b", r"\bwifi\b",
        r"\bapp\b", r"\bbattery\b", r"\bcharger\b", r"\bcable\b",
        r"\bcamera\b", r"\bmessage\b", r"\bprinter\b",
    ]),
    (35, "Money & banking", "vocab", [
        r"\bbank\b", r"\baccount\b", r"\bcredit card\b", r"\bdebit card\b",
        r"\batm\b", r"\bcash\b", r"\bcoin\b", r"\bbill\b",
        r"\bdeposit\b", r"\bwithdraw\b", r"\bsalary\b", r"\bbudget\b",
        r"\binvest\b", r"\bloan\b", r"\binterest\b", r"\btax\b",
    ]),
    (36, "Builder: causality (เพราะ / ดังนั้น / ถ้า…ก็…)", "builder", []),
    (37, "Travel destinations in Thailand", "vocab", [
        r"\bbangkok\b", r"\bchiang mai\b", r"\bphuket\b", r"\bayutthaya\b",
        r"\bsukhothai\b", r"\bpattaya\b", r"\bgrand palace\b",
        r"\bwat\b", r"\btemple\b", r"\bmarket\b", r"\bbeach\b",
        r"\bisland\b", r"\bmountain\b", r"\bfloating\b", r"\bko\b",
    ]),
]


def main(corpus_path: Path, out_path: Path):
    entries = json.loads(corpus_path.read_text())
    print(f"Loaded {len(entries)} entries", file=sys.stderr)

    lines = []
    lines.append("# Walk & Talk Thai — content roadmap (weeks 13–37)\n")
    lines.append("Auto-generated from `corpus/core2000.json`. The corpus is a ")
    lines.append("word-inventory distilled from ThaiPod101's free *2000 Core ")
    lines.append("Words and Phrases* PDF — **inventory only**, no sample sentences ")
    lines.append("(we write those ourselves to keep voice and politeness consistent).\n\n")
    lines.append("**Workflow per week:** scan candidates → pick 10 → look up the ")
    lines.append("tone-correct Thai script in the source PDF at the noted page → ")
    lines.append("write our own sample sentence → drop into `vocab.json`.\n\n")

    # Pre-compute candidate counts for the summary table.
    summary: list[tuple[int, str, str, int]] = []
    for week, title, kind, patterns in THEMES:
        if kind == "builder":
            summary.append((week, title, kind, -1))
            continue
        compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
        seen = set()
        n = 0
        for e in entries:
            if any(rx.search(e["en"]) for rx in compiled):
                key = e["en"].lower().strip(".!?")
                if key not in seen:
                    seen.add(key)
                    n += 1
        summary.append((week, title, kind, n))

    lines.append("## Roadmap at a glance\n")
    lines.append("| Wk | Theme | Kind | Candidates |")
    lines.append("|----|-------|------|------------|")
    for week, title, kind, n in summary:
        cand = "—" if n < 0 else (f"**{n}**" if n >= 10 else f"⚠️ {n} (need to look up more in PDF)")
        lines.append(f"| {week} | {title} | {kind} | {cand} |")
    lines.append("")
    lines.append("Weeks marked ⚠️ have fewer than 10 corpus matches — the rest come ")
    lines.append("from manual lookup in the source PDF (the extractor lost ~40% of ")
    lines.append("entries due to broken font encoding).\n\n")

    for week, title, kind, patterns in THEMES:
        lines.append(f"## Week {week}: {title}  · *{kind}*\n")
        if kind == "builder":
            lines.append("_Sentence builder — 3 stems × 4 progressive steps. "
                         "Draft from scratch, no corpus entries needed._\n")
            lines.append("")
            continue
        compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
        hits = []
        for e in entries:
            gloss = e["en"]
            if any(rx.search(gloss) for rx in compiled):
                hits.append(e)
        if not hits:
            lines.append("_No corpus matches — draft from scratch._\n")
            lines.append("")
            continue
        # Trim/dedup
        seen_gloss = set()
        deduped = []
        for h in hits:
            key = h["en"].lower().strip(".!?")
            if key in seen_gloss:
                continue
            seen_gloss.add(key)
            deduped.append(h)
        lines.append(f"_{len(deduped)} candidate(s) — pick 10:_")
        lines.append("")
        for h in deduped[:30]:
            lines.append(f"- `#{h['id']:>4}` (p{h['page']}) **{h['en']}** "
                         f"— *{h['roman_no_tones']}*")
        if len(deduped) > 30:
            lines.append(f"- _…and {len(deduped) - 30} more_")
        lines.append("")

    out_path.write_text("\n".join(lines))
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main(Path("corpus/core2000.json"), Path("corpus/roadmap.md"))
