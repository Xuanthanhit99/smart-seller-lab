#!/usr/bin/env python3
"""Generate sitemap and robots only for an explicitly approved live hostname."""
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape
import os,sys
root=Path(__file__).resolve().parents[1]
url=os.environ.get("SITE_URL","").rstrip("/")
approved=os.environ.get("OWNER_PUBLICATION_APPROVED","")=="yes"
p=urlparse(url)
if not approved or p.scheme!="https" or not p.netloc or p.path not in ("","/"):
    sys.exit("STOP: set an actual HTTPS SITE_URL and OWNER_PUBLICATION_APPROVED=yes after release approval.")
paths=sorted(root.rglob("*.html"))
urls=[url+"/"+str(f.relative_to(root)).replace("index.html","") for f in paths]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+escape(x)+'</loc></url>\n' for x in urls)+'</urlset>\n'
(root/"sitemap.xml").write_text(xml,encoding="utf-8")
(root/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+url+"/sitemap.xml\n",encoding="utf-8")
print("Sitemap and robots generated. IMPORTANT: remove noindex meta tags only after final QA.")
