#!/usr/bin/env python3
"""Build a publication-ready static output without modifying source or deploying.
Requires explicit --release flag; default is safe preview with noindex.
"""
import argparse, html, re, shutil
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, tostring
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument("--site-url",required=True)
p.add_argument("--output",default="dist")
p.add_argument("--release",action="store_true",help="Remove noindex/robots block; requires separate Owner GO")
a=p.parse_args()
url=a.site_url.rstrip("/")
parsed=urlparse(url)
if parsed.scheme!="https" or not parsed.netloc or parsed.path not in ("","/"):
    p.error("--site-url must be an actual HTTPS site origin")
dest=ROOT/a.output
if dest.resolve()==ROOT.resolve() or ROOT.resolve() not in dest.resolve().parents:
    p.error("Output must be a subfolder of repository")
if dest.exists(): shutil.rmtree(dest)
dest.mkdir(parents=True)
pages=[]
for source in ROOT.rglob("*.html"):
    if dest in source.parents or ".git" in source.parts: continue
    rel=source.relative_to(ROOT)
    pages.append(rel)
    text=source.read_text(encoding="utf-8")
    canonical=url+"/"+str(rel)
    if rel.name=="index.html" and len(rel.parts)==1: canonical=url+"/"
    if a.release:
        text=re.sub(r'<meta\s+name="robots"\s+content="noindex"\s*/?>',"",text,flags=re.I)
        text=text.replace("Content requires editorial verification before publication. No affiliate links are active in this preview.","Research-based editorial content; verify current terms and product specifications before making a decision.")
    if 'rel="canonical"' not in text:
        text=text.replace("</head>",'<link rel="canonical" href="'+html.escape(canonical,quote=True)+'"></head>')
    target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding="utf-8")
for asset in ("styles.css","_headers"):
    if (ROOT/asset).exists():shutil.copy2(ROOT/asset,dest/asset)
root=Element("urlset",xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for rel in sorted(pages):
    u=SubElement(root,"url");SubElement(u,"loc").text=url+("/" if str(rel)=="index.html" else "/"+str(rel))
(dest/"sitemap.xml").write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n'+tostring(root,encoding="utf-8"))
(dest/"robots.txt").write_text(("User-agent: *\nAllow: /\n" if a.release else "User-agent: *\nDisallow: /\n")+"Sitemap: "+url+"/sitemap.xml\n",encoding="utf-8")
print("Built",len(pages),"pages in",dest,"mode",("RELEASE" if a.release else "PREVIEW"))
