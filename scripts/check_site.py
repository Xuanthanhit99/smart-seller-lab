#!/usr/bin/env python3
"""Local pre-release structural QA; no external dependencies or network calls."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
ROOT = Path(__file__).resolve().parents[1]
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.tags=[]; self.title=False; self.desc=False; self.viewport=False; self.noindex=False; self.lang=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append(tag)
        if tag=="html" and a.get("lang")=="en": self.lang=True
        if tag=="a": self.links.append(a.get("href",""))
        if tag=="title": self.title=True
        if tag=="meta" and a.get("name")=="description" and a.get("content"): self.desc=True
        if tag=="meta" and a.get("name")=="viewport": self.viewport=True
        if tag=="meta" and a.get("name")=="robots" and "noindex" in a.get("content",""): self.noindex=True
errors=[]
files=sorted(ROOT.rglob("*.html"))
if len(files)<15: errors.append(f"Expected at least 15 HTML files, got {len(files)}")
for file in files:
    p=Inspect()
    try: p.feed(file.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{file}: parse error {e}"); continue
    for label,ok in [("lang=en",p.lang),("title",p.title),("description",p.desc),("viewport",p.viewport),("prelaunch noindex",p.noindex)]:
        if not ok: errors.append(f"{file.relative_to(ROOT)}: missing {label}")
    for href in p.links:
        if not href or href.startswith(("#","mailto:","tel:","https://","http://")): continue
        u=urlsplit(href)
        if u.scheme: continue
        target=(file.parent / unquote(u.path)).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists(): errors.append(f"{file.relative_to(ROOT)}: broken link {href}")
if not (ROOT/"robots.txt").exists(): errors.append("Missing robots.txt")
if not (ROOT/"_headers").exists(): errors.append("Missing Cloudflare _headers")
print(f"Checked {len(files)} HTML files")
for err in errors: print("FAIL:",err)
if errors: sys.exit(1)
print("PASS: structural, metadata and local-link checks. Browser/mobile/hosted tests are NOT covered.")
