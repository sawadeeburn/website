#!/usr/bin/env python3
"""Renders the drawn scenes (tools/scenes.html) to PNG. Usage: stills.py <outdir>. Then tools/overprint.py prints them."""
import sys, base64, pathlib
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
JOBS = {"build": (2400, 1350), "burn": (1500, 2000), "sail": (1600, 2000), "camp": (2000, 1600), "tent": (2000, 1600), "lanterns": (2800, 1200), "gather": (2800, 1200)}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto((pathlib.Path(__file__).parent / "scenes.html").resolve().as_uri())
    for n, (w, h) in JOBS.items():
        if len(sys.argv) > 2 and n not in sys.argv[2:]: continue
        (out / f"{n}.png").write_bytes(base64.b64decode(pg.evaluate(f"draw('{n}',{w},{h})").split(",", 1)[1]))
    b.close()
