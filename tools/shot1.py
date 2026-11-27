#!/usr/bin/env python3
"""One screenshot of a selector, after letting animations finish. shot1.py url out.png selector [width] [scheme] [wait_ms]"""
import sys
from playwright.sync_api import sync_playwright
url, out, sel = sys.argv[1:4]; w = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
scheme = sys.argv[5] if len(sys.argv) > 5 else "light"; wait = int(sys.argv[6]) if len(sys.argv) > 6 else 5500
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": 900 if w > 600 else 844}, color_scheme=scheme)
    pg.goto(url, wait_until="networkidle")
    pg.evaluate("document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager')")
    for s_, o in zip(sel.split("|"), out.split("|")):
        if s_ == "VIEW": pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(1800); pg.screenshot(path=o); continue
        el = pg.locator(s_).first; el.scroll_into_view_if_needed(); pg.wait_for_timeout(wait); el.screenshot(path=o)
    b.close()
