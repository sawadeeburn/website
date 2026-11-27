#!/usr/bin/env python3
"""Screenshots of the built site. Usage: shoot.py <url> <outdir> [full]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
full = len(sys.argv) > 3
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h, scheme in [("desktop", 1440, 900, "light"), ("phone", 390, 844, "light"), ("desktop-dark", 1440, 900, "dark"), ("phone-dark", 390, 844, "dark")]:
        if not full and "dark" in name: continue
        pg = b.new_page(viewport={"width": w, "height": h}, color_scheme=scheme, device_scale_factor=1)
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url, wait_until="networkidle")
        pg.evaluate("document.documentElement.style.scrollBehavior='auto';document.querySelectorAll('img[loading]').forEach(i=>i.loading='eager')")
        H = pg.evaluate("document.documentElement.scrollHeight")
        y = 0; i = 0
        while y < H:
            pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(450)
            pg.screenshot(path=str(out / f"{name}-{i:02d}.png")); y += h; i += 1
        ow = pg.evaluate("document.documentElement.scrollWidth")
        print(name, "height", H, "scrollWidth", ow, "errors", errs[:5])
        pg.close()
    b.close()
