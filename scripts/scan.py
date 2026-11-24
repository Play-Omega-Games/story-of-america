#!/usr/bin/env python3
"""Sensitive-content scan for Story of America.

A keyword pass over every reading, then hand overrides from curation.CONTENT.
Writes scan/content-scan.json and scan/content-scan.md (internal review file).
Severity: none, low (a passing dated word or brief violence), medium (dated terms used
repeatedly, one-sided framing, or violent scenes), high (framing that demeans a people
or faith is central to the chapter, or frightening violence is central).
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = {
 "native_framing": r"\bsavages?\b|\bsavagery\b|\bred ?m[ae]n\b|\bredskins?\b|\bsquaws?\b|\bpapoose|\bheathens?\b|\bbraves\b|\bwar-?whoops?\b|\bwild (?:men|people|tribes)\b|\bbarbarous\b|\bbarbarians?\b|\bfiend\w*|\bhalf-breeds?\b|\bwily\b|\bfire-water\b|\bpale-?faces?\b",
 "violence": r"\bmassacred?\b|\bscalp(?:s|ed|ing)?\b|\btomahawk\w*|\btortur\w*|\bburn(?:ed|t) (?:alive|to death)|\bbutcher\w*|\bslaughter\w*|\bhanged\b|\bbeheaded\b|\bmurder\w*|\bslain\b|\bslew\b|\bkill(?:ed|ing)?\b",
 "slavery": r"\bslaves?\b|\bslavery\b|\bslave-holders?\b",
 "race_terms": r"\bnegro(?:es)?\b|\bnigger\w*|\bdark(?:e|ie)ys?\b|\bpickaninn\w*|\bmammy\b|\bcarpet-?bagg\w*|\bTopsy\b",
 "other_groups": r"\bChinam[ae]n\b|\bJaps?\b|\bgreasers?\b|\bpapists?\b|\bMormon\w*|\bwitch(?:es|craft)?\b|\bbandits?\b",
}
NATIVE_MENTION = r"\bIndians?\b|\bRedm[ae]n\b"

def hits(text):
    h = {}
    for c, rx in CATS.items():
        ms = re.findall(rx, text, re.I)
        if ms:
            h[c] = dict(collections.Counter(m.lower() for m in ms))
    n = len(re.findall(NATIVE_MENTION, text))
    if n:
        h["native_mentions"] = n
    return h

def default_severity(h):
    cnt = lambda c: sum(h.get(c, {}).values()) if isinstance(h.get(c), dict) else 0
    nf, v, sl, rt, og = (cnt(c) for c in ("native_framing", "violence", "slavery", "race_terms", "other_groups"))
    topics = []
    if nf: topics.append("native_framing")
    if v: topics.append("violence")
    if sl: topics.append("slavery")
    if rt: topics.append("race")
    if og: topics.append("other")
    if (nf >= 5 and v >= 3):
        sev = "high"
    elif nf >= 3 or v >= 5 or rt >= 2 or og >= 5 or sl >= 5:
        sev = "medium"
    elif nf or v or sl or rt or og:
        sev = "low"
    else:
        sev = "none"
    return sev, topics

def default_note(topics, sev):
    if sev in ("none", "low"):
        return None
    parts = []
    if "native_framing" in topics: parts.append(curation.NATIVE_NOTE)
    if "race" in topics: parts.append(curation.SLAVERY_NOTE)
    if "slavery" in topics and not parts: parts.append(curation.SLAVERY_TOPIC_NOTE)
    if "violence" in topics and not parts: parts.append(curation.VIOLENCE_NOTE)
    return " ".join(parts) or None

def assess(rid, text):
    h = hits(text)
    sev, topics = default_severity(h)
    note = default_note(topics, sev)
    source = "rule"
    if rid in curation.CONTENT:
        sev, topics, note = curation.CONTENT[rid]
        source = "reviewed"
    return {"severity": sev, "topics": topics, "note": note, "set_by": source, "hits": h}

if __name__ == "__main__":
    plan = json.load(open(os.path.join(ROOT, "plans", "story-of-america.json"), encoding="utf-8"))
    rows = []
    for r in plan["readings"] + plan["famous_stories"]:
        a = assess(r["id"], r["text"])
        rows.append({"id": r["id"], "title": r["title"], **a})
    os.makedirs(os.path.join(ROOT, "scan"), exist_ok=True)
    json.dump(rows, open(os.path.join(ROOT, "scan", "content-scan.json"), "w"), indent=1, ensure_ascii=False)
    c = collections.Counter(r["severity"] for r in rows if r["id"].startswith("tcoo"))
    f = collections.Counter(r["severity"] for r in rows if r["id"].startswith("ffs"))
    print("America", dict(c), "Famous", dict(f))
