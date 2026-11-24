#!/usr/bin/env python3
"""Live checks.

Default: download both source texts fresh from the mirrors in scripts/build.py and confirm every
reading in both plans is word for word in the live text.
--raw: also confirm the plan files served at the raw GitHub URLs the bot loads equal the local files.
Run from the repo root: python3 scripts/check_links.py [--raw]
"""
import hashlib, json, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import MIRRORS, BOOKS  # noqa: E402

RAW = "https://raw.githubusercontent.com/Play-Omega-Games/story-of-america/main/"
FILES = ["plans/story-of-america.json", "plans/story-of-america-5min.json", "plans/standards.json"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (story-of-america check)"})
    return urllib.request.urlopen(req, timeout=90).read()


def norm(s):
    s = s.replace("\r", "").replace("_", "")
    s = re.sub(r"\[Illustration[^\]]*\]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


bad = []
live = {}
for key, n in (("america", BOOKS["marshall"]), ("famous", BOOKS["baldwin"])):
    for m in MIRRORS:
        try:
            live[key] = norm(get(m.format(n=n)).decode("utf-8"))
            print(f"OK  #{n} from {m.format(n=n)}")
            break
        except Exception as e:
            print(f"..  #{n} failed at {m.format(n=n)}: {e}")
    if key not in live:
        bad.append(f"could not download #{n}")
for f in FILES[:2]:
    plan = json.load(open(f, encoding="utf-8"))
    for book, items in (("america", plan["readings"]), ("famous", plan["famous_stories"])):
        if book not in live:
            continue
        miss = [r["id"] for r in items if norm(r["text"]) not in live[book]]
        print(f"{'OK ' if not miss else 'BAD'} {f} {book}: {len(items) - len(miss)} of {len(items)} found in the live text")
        bad += [f"{f} {i} not in live text" for i in miss]
if "--raw" in sys.argv:
    for f in FILES:
        try:
            same = hashlib.sha256(get(RAW + f)).hexdigest() == hashlib.sha256(open(f, "rb").read()).hexdigest()
        except Exception as e:
            same = False
            print(f"BAD {RAW + f}: {e}")
        print(f"{'OK ' if same else 'BAD'} raw {f}")
        if not same:
            bad.append(f"raw {f} differs or is missing")
if bad:
    print(f"{len(bad)} PROBLEMS"); [print(" ", b) for b in bad[:40]]; sys.exit(1)
print("ALL LIVE CHECKS PASSED")
