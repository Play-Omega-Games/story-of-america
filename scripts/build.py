#!/usr/bin/env python3
"""Build plans/story-of-america.json (about 10 minutes a reading),
plans/story-of-america-5min.json (about 5 minutes) and plans/standards.json from the public-domain source texts in src/.

Text is copied word for word. The build only joins hard-wrapped prose lines,
keeps line breaks in verse, drops picture markers and italic underscores,
and splits long chapters into nightly readings at paragraph breaks.
Run: python3 scripts/build.py [--fetch]
"""
import json, os, re, sys, math, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curation, scan

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "plans", "story-of-america.json")
OUT_SHORT = os.path.join(ROOT, "plans", "story-of-america-5min.json")
OUT_STD = os.path.join(ROOT, "plans", "standards.json")
WPM = 150            # read-aloud pace used across Omega Home Library
TARGET_WORDS = 1500  # about 10 minutes read aloud
MIRRORS = [
    "https://gutenberg.pglaf.org/cache/epub/{n}/pg{n}.txt",
    "https://aleph.gutenberg.org/cache/epub/{n}/pg{n}.txt",
    "https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt",
]
BOOKS = {"marshall": 3761, "baldwin": 18442}


def fetch(n):
    path = os.path.join(SRC, f"pg{n}.txt")
    if os.path.exists(path) and "--fetch" not in sys.argv:
        return
    os.makedirs(SRC, exist_ok=True)
    last = None
    for m in MIRRORS:
        try:
            data = urllib.request.urlopen(m.format(n=n), timeout=60).read()
            open(path, "wb").write(data)
            return
        except Exception as e:  # try the next mirror
            last = e
    raise SystemExit(f"could not download #{n}: {last}")


def body(n):
    t = open(os.path.join(SRC, f"pg{n}.txt"), encoding="utf-8").read().replace("\r", "")
    s = t.index("*** START OF THE PROJECT GUTENBERG EBOOK")
    s = t.index("\n", s) + 1
    e = t.index("*** END OF THE PROJECT GUTENBERG EBOOK")
    return t[s:e]


def words(s):
    return len(re.findall(r"[A-Za-z0-9’']+", s))


def norm(s):
    """Whitespace-normalised form used to prove text matches the source."""
    s = s.replace("_", "")
    s = re.sub(r"\[Illustration[^\]]*\]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def paragraphs(block, verse_by_indent):
    out = []
    for raw in re.split(r"\n\s*\n", block):
        lines = [l for l in raw.split("\n") if l.strip()]
        if not lines:
            continue
        if all(re.fullmatch(r"\s*\[Illustration[^\]]*\]\s*", l) for l in lines):
            continue
        lines = [re.sub(r"\[Illustration[^\]]*\]", "", l) for l in lines]
        lines = [l for l in lines if l.strip()]
        if verse_by_indent:
            verse = all(l.startswith("  ") for l in lines)
        else:
            # Marshall's verse is not indented: every line opens with a capital
            # (or a quote and a capital) and there are at least two lines.
            body_lines = lines[:-1]
            verse = (len(lines) >= 3 or (len(lines) == 2 and max(len(l.rstrip()) for l in lines) < 50)) and all(re.match(r"\s*[\"'(]?[A-Z]", l) for l in lines) \
                and (any(len(l.rstrip()) < 50 for l in body_lines)
                     or all(re.search(r"[,;:.!?\"'-]$", l.rstrip()) for l in body_lines))
        if verse:
            p = "\n".join(re.sub(r"\s+", " ", l.strip()) for l in lines)
        else:
            p = re.sub(r"\s+", " ", " ".join(l.strip() for l in lines))
        p = p.replace("_", "")
        out.append({"text": p, "verse": verse})
    return out


MAX_WORDS = 1800     # a single reading never runs past about 12 minutes
SHORT_MAX_WORDS = 750  # 5-minute option: never past about 5 minutes


def _split_n(paras, n):
    total = sum(words(p["text"]) for p in paras)
    if n == 1:
        return [paras]
    cuts, acc, k = [], 0, 1
    for i, p in enumerate(paras[:-1]):
        acc += words(p["text"])
        goal = k * total / n
        nxt = acc + words(paras[i + 1]["text"])
        if acc >= goal or (nxt > goal and abs(nxt - goal) > abs(acc - goal)):
            cuts.append(i + 1)
            k += 1
            if k == n:
                break
    parts, prev = [], 0
    for c in cuts + [len(paras)]:
        parts.append(paras[prev:c])
        prev = c
    return [p for p in parts if p]


def split_parts(paras, cap=MAX_WORDS):
    """Split at paragraph breaks into the fewest near-equal parts that each stay within cap words."""
    total = sum(words(p["text"]) for p in paras)
    n = max(1, math.ceil(total / cap))
    while True:
        parts = _split_n(paras, n)
        if all(sum(words(p["text"]) for p in part) <= cap for part in parts) or n >= len(paras):
            return parts
        n += 1


YEAR = re.compile(r"\b(9\d\d|1[0-9]\d\d)\b")


def years_in(text):
    ys = [int(y) for y in YEAR.findall(text) if 985 <= int(y) <= 1917]
    return ys


PART_NAMES = {"I": "Stories of Explorers and Pioneers", "II": "Stories of Virginia",
              "III": "Stories of New England", "IV": "Stories of the Middle and Southern Colonies",
              "V": "Stories of the French in America", "VI": "Stories of the Struggle for Liberty",
              "VII": "Stories of the United States under the Constitution"}


def marshall():
    b = body(3761)
    toc_end = b.index("PART I STORIES OF EXPLORERS AND PIONEERS")
    text = b[toc_end:]
    heads = list(re.finditer(r"^Chapter (\d+) - (.+(?:\n\S.+)*)$", text, re.M))
    part_re = re.compile(r"^PART ([IVX]+):? (.+)$|^Part ([IVX]+) (STORIES .+)$", re.M)
    chapters = []
    for i, h in enumerate(heads):
        start = h.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[start:end]
        # drop part headings and rule lines that sit between chapters
        block = part_re.sub("", block)
        block = re.sub(r"^_{5,}\s*$", "", block, flags=re.M)
        title = re.sub(r"\s+", " ", h.group(2)).strip()
        chapters.append({"num": int(h.group(1)), "title": title,
                         "paras": paragraphs(block, False), "raw": block})
    # parts by position
    parts = [(m.start(), re.sub(r"\s+", " ", (m.group(2) or m.group(4))).strip().title())
             for m in part_re.finditer(text) if m.start() > 0 or True]
    parts = [(pos, name) for pos, name in parts if name.lower().startswith("stories")]
    for ch, h in zip(chapters, heads):
        name = [n for pos, n in parts if pos < h.start()][-1]
        num = [m for m in re.finditer(r"^PART ([IVX]+)|^Part ([IVX]+)", text, re.M) if m.start() < h.start()][-1]
        ch["part"] = f"Part {num.group(1) or num.group(2)}: {PART_NAMES[num.group(1) or num.group(2)]}"
    return chapters


def baldwin():
    b = body(18442)
    contents = re.search(r"CONTENTS\.\n(.*?)\nCONCERNING THESE STORIES", b, re.S).group(1)
    titles = [t.strip() for t in contents.split("\n") if t.strip()]
    start = b.index("FIFTY FAMOUS STORIES RETOLD.\n", b.index("CONCERNING THESE STORIES"))
    text = b[start + len("FIFTY FAMOUS STORIES RETOLD.\n"):]
    pos = []
    cursor = 0
    for t in titles:
        m = re.compile(r"^" + re.escape(t.upper()) + r"\.$", re.M).search(text, cursor)
        if not m:
            raise SystemExit(f"Baldwin title not found: {t}")
        pos.append((m.start(), m.end(), t))
        cursor = m.end()
    stories = []
    for i, (s, e, t) in enumerate(pos):
        end = pos[i + 1][0] if i + 1 < len(pos) else len(text)
        block = text[e:end]
        paras = paragraphs(block, True)
        # in-story subheadings (I. THE THREE QUESTIONS.) stay as their own lines
        stories.append({"num": i + 1, "title": t, "paras": paras, "raw": block})
    return stories


def content(rid, text):
    a = scan.assess(rid, text)
    c = {"severity": a["severity"], "topics": a["topics"], "note": a["note"]}
    if c["severity"] == "high":
        c["skip_summary"] = curation.SKIP_SUMMARY[rid]
    return c


def reading_text(paras):
    return "\n\n".join(p["text"] for p in paras)


PERSPECTIVE_TOPICS = {"native_framing", "slavery", "race", "religion"}


def tag(code, activity, ages=None):
    s = curation.STANDARDS[code]
    t = {"framework": s["framework"], "code": code, "band": s["band"], "activity": activity,
         "wording": "supports practice toward", "source": s["source"], "verified": curation.VERIFIED}
    if ages:
        t["ages"] = ages
    return t


def america_standards(c, last_of_chapter):
    out = [tag("SL.2.2", "tellBack"), tag("RI.3.3", "whyQuestion", "9 to 12")]
    if last_of_chapter:
        out.append(tag("D2.His.1.3-5", "timeline"))
    if c["severity"] in ("medium", "high") and c["note"] and PERSPECTIVE_TOPICS & set(c["topics"]):
        out.append(tag("D2.His.4.3-5", "perspective"))
    return out


def famous_standards():
    return [tag("SL.2.2", "tellBack"), tag("RL.2.2", "lesson")]


def entry(base, ps, offset):
    t = reading_text(ps)
    w = words(t)
    e = dict(base)
    e.update({"words": w, "minutes": max(1, round(w / WPM)), "word_offset": offset,
              "starts_with": " ".join(t.split()[:8]), "ends_with": " ".join(t.split()[-8:])})
    return e, t


def group_nights(items, cap):
    nights, cur, cw = [], [], 0
    for s in items:
        if cur and cw + s["words"] > cap:
            nights.append(cur); cur, cw = [], 0
        cur.append(s["id"]); cw += s["words"]
    if cur:
        nights.append(cur)
    return [{"night": i + 1, "stories": n} for i, n in enumerate(nights)]


def build():
    for n in BOOKS.values():
        fetch(n)
    M, B = marshall(), baldwin()
    plans = {}
    for length, cap in (("10", MAX_WORDS), ("5", SHORT_MAX_WORDS)):
        readings, chapters_meta, stories = [], [], []
        for ch in M:
            cid = f"tcoo-{ch['num']:02d}"
            ch = dict(ch)
            if ch["num"] in curation.TITLE_FIXES:
                ch["source_heading"] = ch["title"]
                ch["title"] = curation.TITLE_FIXES[ch["num"]][0]
            tl = curation.TIMELINE[ch["num"]]
            std_parts = split_parts(ch["paras"], MAX_WORDS)
            rows, offset = [], 0
            for k, ps in enumerate(std_parts, 1):
                parent = f"{cid}-{k}"
                c = content(parent, reading_text(ps))
                subs = [ps] if length == "10" else split_parts(ps, cap)
                for sub in subs:
                    rows.append((parent, c, sub, offset))
                    offset += sum(words(p["text"]) for p in sub)
            for idx, (parent, c, sub, off) in enumerate(rows, 1):
                rid = parent if length == "10" else f"{cid}-s{idx}"
                base = {"id": rid, "book": "america", "chapter": ch["num"], "chapter_id": cid,
                        "part_of_book": ch["part"], "title": ch["title"], "reading": idx, "of": len(rows)}
                if length == "5":
                    base["parent"] = parent
                e, t = entry(base, sub, off)
                e["timeline"] = {"when": tl[0], "event": tl[1]}
                # every part inherits its 10-minute parent's content, skip_summary included;
                # the skill shows a summary once per parent when it skips that parent's parts
                e["content"] = dict(c)
                e["standards"] = america_standards(c, idx == len(rows))
                e["text"] = t
                readings.append(e)
            chapters_meta.append({"id": cid, "chapter": ch["num"], "title": ch["title"], "part": ch["part"],
                                  **({"source_heading": ch["source_heading"]} if "source_heading" in ch else {}),
                                  "timeline": {"when": tl[0], "event": tl[1]},
                                  "words": sum(words(p["text"]) for p in ch["paras"]), "readings": len(rows)})
        for st in B:
            std_parts = split_parts(st["paras"], MAX_WORDS)
            rows, offset = [], 0
            for k, ps in enumerate(std_parts, 1):
                parent = f"ffs-{st['num']:02d}" + (f"-{k}" if len(std_parts) > 1 else "")
                c = content(parent, reading_text(ps))
                for sub in ([ps] if length == "10" else split_parts(ps, cap)):
                    rows.append((parent, c, sub, offset))
                    offset += sum(words(p["text"]) for p in sub)
            for idx, (parent, c, sub, off) in enumerate(rows, 1):
                sid = parent if length == "10" else (f"ffs-{st['num']:02d}" + (f"-s{idx}" if len(rows) > 1 else ""))
                base = {"id": sid, "book": "famous", "story": st["num"], "title": st["title"],
                        "reading": idx, "of": len(rows)}
                if length == "5":
                    base["parent"] = parent
                e, t = entry(base, sub, off)
                e["content"] = c
                e["standards"] = famous_standards()
                e["text"] = t
                stories.append(e)
        plans[length] = {
            "meta": {
                "name": "Story of America", "series": "Omega Home Library: Story Shelf",
                "version": 2, "built": "2026-11-24", "length": f"about {length} minutes",
                "read_aloud_wpm": WPM, "max_words_per_reading": cap,
                "books": {
                    "america": {"title": "This Country of Ours", "author": "H. E. Marshall", "year": 1917,
                                "chapters": len(chapters_meta), "readings": len(readings),
                                "words": sum(r["words"] for r in readings)},
                    "famous": {"title": "Fifty Famous Stories Retold", "author": "James Baldwin", "year": 1896,
                               "stories": len({x["story"] for x in stories}), "entries": len(stories),
                               "words": sum(s["words"] for s in stories)},
                },
                "severity_levels": {"none": "nothing flagged", "low": "a passing old-fashioned word or brief violence",
                                    "medium": "dated words used often, one-sided telling, or violent scenes",
                                    "high": "unfair or hurtful framing of a people or faith, or frightening violence, is central"},
                "content_notes": "Approved by Omega Games, Nov 24, 2026. A note comes before every medium and high reading; high readings wait for Read it; families may skip all high readings and get a one-line summary instead.",
                "standards_note": "Each reading supports practice toward the listed standards through the named activity. Not accredited, and not a replacement for any state requirement. Code text is in plans/standards.json.",
                "next_shelf": curation.NEXT_SHELF,
                "note": "Reading text is word for word from public-domain editions published in 1896 and 1917. Spellings such as to-day and the syllable hyphens in the 1896 book are the originals. Readings split only at paragraph breaks.",
            },
            "chapters": chapters_meta,
            "readings": readings,
            "famous_stories": stories,
            "famous_nights": group_nights(stories, cap),
        }
        plans[length]["meta"]["books"]["famous"]["nights"] = len(plans[length]["famous_nights"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(plans["10"], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(plans["5"], open(OUT_SHORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    std = {"meta": {"verified": curation.VERIFIED, "wording": "supports practice toward",
                    "activities": curation.ACTIVITIES,
                    "note": "Code text copied word for word from the official documents named in source. Not accredited."},
           "standards": [dict(code=k, **v) for k, v in curation.STANDARDS.items()]}
    json.dump(std, open(OUT_STD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return plans


if __name__ == "__main__":
    p = build()
    for k, v in p.items():
        print(k, "minutes:", json.dumps(v["meta"]["books"]))
