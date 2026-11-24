#!/usr/bin/env python3
"""Offline checks for the Story of America plans.

For both plans/story-of-america.json (about 10 minutes) and plans/story-of-america-5min.json:
- the file parses and every entry has the fields the skills use;
- every reading and story is word for word from its source (whitespace-normalised, in book order),
  and all of them joined equal the whole source: nothing added, nothing dropped;
- readings are split only at paragraph breaks (5-minute parts join back into their 10-minute parent);
- no reading runs past its cap; every high reading has a note and a skip summary;
- every standards tag points at plans/standards.json and a known activity.
Prints plan lengths per pace. Run from the repo root: python3 tests/test_plan.py
"""
import datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P10 = os.path.join(ROOT, "plans", "story-of-america.json")
P5 = os.path.join(ROOT, "plans", "story-of-america-5min.json")
PSTD = os.path.join(ROOT, "plans", "standards.json")
fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)


def norm(s):
    s = s.replace("\r", "").replace("_", "")
    s = re.sub(r"\[Illustration[^\]]*\]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return len(re.findall(r"[A-Za-z0-9’']+", s))


def src(n):
    path = os.path.join(ROOT, "src", f"pg{n}.txt")
    if not os.path.exists(path):
        return None
    t = open(path, encoding="utf-8").read().replace("\r", "")
    s = t.index("\n", t.index("*** START OF THE PROJECT GUTENBERG EBOOK")) + 1
    return t[s:t.index("*** END OF THE PROJECT GUTENBERG EBOOK")]


std = json.load(open(PSTD, encoding="utf-8"))
codes = {s["code"]: s for s in std["standards"]}
activities = set(std["meta"]["activities"])
check(len(codes) == 5 and all(s["text"] and s["source"].startswith("https://") for s in codes.values()),
      "standards.json incomplete")

m_src, b_src = src(3761), src(18442)
if m_src is None or b_src is None:
    print("note: src/ not present; run python3 scripts/build.py --fetch to enable the word-for-word source checks")


def source_checks(plan, label):
    if m_src is None:
        return
    body = m_src[m_src.index("PART I STORIES OF EXPLORERS AND PIONEERS"):]
    mn, pos = norm(body), 0
    for r in plan["readings"]:
        i = mn.find(norm(r["text"]), pos)
        check(i >= 0, f"{label} {r['id']} not word for word in source, in order")
        if i >= 0:
            pos = i + len(norm(r["text"]))
    stripped = re.sub(r"^Chapter \d+ - .+(?:\n\S.+)*$", "", body, flags=re.M)
    stripped = re.sub(r"^(PART [IVX]+:? .+|Part [IVX]+ STORIES .+)$", "", stripped, flags=re.M)
    stripped = re.sub(r"^_{5,}\s*$", "", stripped, flags=re.M)
    check(norm(stripped) == " ".join(norm(r["text"]) for r in plan["readings"]),
          f"{label}: America readings do not equal the source (something added or dropped)")
    bn, pos = norm(b_src), 0
    for s in plan["famous_stories"]:
        i = bn.find(norm(s["text"]), pos)
        check(i >= 0, f"{label} {s['id']} not word for word in source, in order")
        if i >= 0:
            pos = i + len(norm(s["text"]))
    bb = b_src[b_src.index("FIFTY FAMOUS STORIES RETOLD.\n", b_src.index("CONCERNING THESE STORIES")) + 29:]
    titles = {s["title"].upper() + "." for s in plan["famous_stories"]}
    bb = "\n".join(l for l in bb.split("\n") if l.strip() not in titles)
    check(norm(bb) == " ".join(norm(s["text"]) for s in plan["famous_stories"]),
          f"{label}: Famous Stories do not equal the source")


def plan_checks(plan, label, cap):
    need = {"id", "title", "text", "words", "minutes", "chapter", "reading", "of", "timeline", "content", "standards"}
    for r in plan["readings"]:
        check(need <= set(r), f"{label} {r.get('id')} missing fields")
        check(r["words"] <= cap, f"{label} {r['id']} has {r['words']} words, over {cap}")
        check(r["text"] == r["text"].strip() and r["text"], f"{label} {r['id']} empty or untrimmed")
        c = r["content"]
        if c["severity"] in ("medium", "high"):
            check(bool(c["note"]), f"{label} {r['id']} {c['severity']} without a note")
    fneed = {"id", "title", "text", "words", "minutes", "story", "reading", "of", "content", "standards"}
    for s in plan["famous_stories"]:
        check(fneed <= set(s), f"{label} {s.get('id')} missing fields")
        check(s["words"] <= cap, f"{label} {s['id']} over cap")
    for x in plan["meta"]["next_shelf"]:
        check(x["link"] or x.get("link_note"), f"{label}: Next shelf {x['name']} has no link and no note")
    by = {}
    for r in plan["readings"]:
        by.setdefault(r["chapter"], []).append(r)
    check(sorted(by) == list(range(1, 100)), f"{label}: chapters are not exactly 1 to 99")
    for c, rs in by.items():
        check([x["reading"] for x in rs] == list(range(1, rs[0]["of"] + 1)), f"{label} chapter {c} out of order")
    for r in plan["readings"] + plan["famous_stories"]:
        for t in r["standards"]:
            check(t["code"] in codes and t["activity"] in activities and t["wording"] == "supports practice toward",
                  f"{label} {r['id']} bad standards tag {t}")
    ids = [i for n in plan["famous_nights"] for i in n["stories"]]
    check(ids == [s["id"] for s in plan["famous_stories"]], f"{label}: famous nights miss or repeat a story")
    for n in plan["famous_nights"]:
        w = sum(s["words"] for s in plan["famous_stories"] if s["id"] in n["stories"])
        check(w <= cap or len(n["stories"]) == 1, f"{label}: famous night {n['night']} over cap")
    check(any(x["link"] for x in plan["meta"]["next_shelf"]), f"{label}: no live Next shelf link")


p10 = json.load(open(P10, encoding="utf-8"))
p5 = json.load(open(P5, encoding="utf-8"))
for plan, label, cap in ((p10, "10min", 1800), (p5, "5min", 750)):
    plan_checks(plan, label, cap)
    source_checks(plan, label)

# display title fix (1917 printing), reading text untouched
for plan in (p10, p5):
    c51 = plan["chapters"][50]
    check(c51["title"] == "The Boston Tea-Party" and c51.get("source_heading") == "The Boston Tea party",
          "chapter 51 display title")
    check(all(r["title"] == "The Boston Tea-Party" for r in plan["readings"] if r["chapter"] == 51), "chapter 51 reading titles")

# 10-minute plan: content decisions
high = [r for r in p10["readings"] if r["content"]["severity"] == "high"]
check(len(high) == 12, f"expected 12 high readings, found {len(high)}")
check(all(r["content"].get("skip_summary") for r in high), "a high reading has no skip summary")
high5 = [r for r in p5["readings"] if r["content"]["severity"] == "high"]
check(len(high5) == 28 and len({r["parent"] for r in high5}) == 12, "5-minute high parts should be 28 from 12 readings")
check(all(r["content"].get("skip_summary") for r in high5), "a 5-minute high part has no skip summary")

# paragraph boundaries: 10-minute readings are whole paragraphs of their chapter, and
# 5-minute parts join back exactly into their 10-minute parent
paras10 = {r["id"]: r["text"].split("\n\n") for r in p10["readings"] + p10["famous_stories"]}
kids = {}
for r in p5["readings"] + p5["famous_stories"]:
    kids.setdefault(r["parent"], []).append(r)
check(set(kids) == set(paras10), "5-minute parents do not match the 10-minute readings")
for parent, rs in kids.items():
    check("\n\n".join(x["text"] for x in rs) == "\n\n".join(paras10[parent]),
          f"5-minute parts of {parent} do not join back into it exactly (cut inside a paragraph?)")
    pr = next(x for x in p10["readings"] + p10["famous_stories"] if x["id"] == parent)
    for x in rs:
        check(x["content"]["severity"] == pr["content"]["severity"], f"{x['id']} severity differs from parent")
    if pr["content"]["severity"] == "high":
        check(all(x["content"].get("skip_summary") == pr["content"]["skip_summary"] for x in rs),
              f"{parent}: a 5-minute part does not carry its parent's skip summary")
allparas = set()
for r in p10["readings"]:
    allparas.update(r["text"].split("\n\n"))
for r in p5["readings"]:
    for para in r["text"].split("\n\n"):
        check(para in allparas, f"{r['id']}: a paragraph was cut")

# standards placement
for plan, label in ((p10, "10min"), (p5, "5min")):
    for c in range(1, 100):
        rs = [r for r in plan["readings"] if r["chapter"] == c]
        tl = [r for r in rs if any(t["code"] == "D2.His.1.3-5" for t in r["standards"])]
        check(tl == [rs[-1]], f"{label} chapter {c}: timeline tag not on the last reading only")


def end_date(start, n, days):
    d, done = start, 0
    while True:
        if d.weekday() in days:
            done += 1
            if done == n:
                return d
        d += datetime.timedelta(days=1)


start = datetime.date(2026, 12, 1)
paces = {"every night": set(range(7)), "school nights (Sun to Thu)": {6, 0, 1, 2, 3},
         "three nights a week (Mon, Wed, Fri)": {0, 2, 4}}
for plan, label in ((p10, "About 10 minutes"), (p5, "About 5 minutes")):
    N, F = len(plan["readings"]), len(plan["famous_nights"])
    H = sum(1 for r in plan["readings"] if r["content"]["severity"] == "high")
    mins = sorted(r["minutes"] for r in plan["readings"])
    print(f"{label}: America {N} readings (min {mins[0]}, median {mins[len(mins)//2]}, max {mins[-1]} minutes), "
          f"{H} high; Famous Stories {len(plan['famous_stories'])} entries in {F} nights")
    for name, days in paces.items():
        print(f"  {name}: America ends {end_date(start, N, days)}; skipping high {end_date(start, N - H, days)}; "
              f"Famous first then America {end_date(start, N + F, days)}")
tags = {}
for r in p10["readings"] + p10["famous_stories"]:
    for t in r["standards"]:
        tags[t["code"]] = tags.get(t["code"], 0) + 1
print("Standards tags (10-minute plan):", tags)
if fails:
    print(f"FAIL ({len(fails)}):\n" + "\n".join(fails[:60]))
    sys.exit(1)
print("ALL CHECKS PASSED")
