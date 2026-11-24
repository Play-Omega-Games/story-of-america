#!/usr/bin/env python3
"""Second-pass standards check: download each official document named in plans/standards.json,
convert it to text (needs pdftotext from poppler-utils) and confirm every code's text appears
word for word. Run from the repo root: python3 scripts/check_standards.py
"""
import json, os, re, subprocess, sys, tempfile, urllib.request

std = json.load(open("plans/standards.json", encoding="utf-8"))


def n(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


docs, bad = {}, []
for s in std["standards"]:
    url = s["source"]
    if url not in docs:
        with tempfile.TemporaryDirectory() as d:
            pdf = os.path.join(d, "doc.pdf")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (story-of-america standards check)"})
            open(pdf, "wb").write(urllib.request.urlopen(req, timeout=120).read())
            subprocess.run(["pdftotext", pdf, pdf + ".txt"], check=True, stderr=subprocess.DEVNULL)
            docs[url] = n(open(pdf + ".txt", encoding="utf-8", errors="replace").read())
    ok = n(s["text"]) in docs[url]
    print(f"{'OK ' if ok else 'BAD'} {s['framework']} {s['code']} (grade band {s['band']}, printed page {s['printed_page']})")
    if not ok:
        bad.append(s["code"])
if bad:
    print("NOT FOUND:", ", ".join(bad)); sys.exit(1)
print(f"ALL {len(std['standards'])} STANDARDS VERIFIED word for word against their official documents")
