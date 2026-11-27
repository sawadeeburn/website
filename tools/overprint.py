#!/usr/bin/env python3
"""Two-ink 'Overprint' print of an image: deep-sea ink + tangerine (and optional gold) halftones on cream paper.
Usage: overprint.py in.png out.webp [--crop x0,y0,x1,y1 (0-1)] [--w 1600] [--cell 7] [--lo .04 --hi .55] [--gold]"""
import sys, argparse
import numpy as np
from PIL import Image, ImageFilter

SEA, TANG, GOLD, CREAM = (7, 47, 53), (228, 96, 42), (245, 198, 90), (242, 228, 210)

def screen(cov, cell, angle):
    """AM halftone: round dots on a rotated grid; cov 0..1 -> ink mask 0..1 (soft edge)."""
    h, w = cov.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle); c, s = np.cos(a), np.sin(a)
    u = (x * c + y * s) / cell; v = (-x * s + y * c) / cell
    d = np.hypot(u - np.round(u), v - np.round(v))           # 0 at dot centre, ~.707 at the corner
    r = np.sqrt(np.clip(cov, 0, 1)) * 0.74                    # dot radius grows with coverage; >.5 dots join
    return np.clip((r - d) * cell / 1.2 + .5, 0, 1)

def run(a):
    im = Image.open(a.src).convert("RGB")
    if a.crop:
        x0, y0, x1, y1 = [float(v) for v in a.crop.split(",")]
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im = im.resize((a.w, round(a.w * im.height / im.width)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=6, percent=a.sharp, threshold=0))
    rgb = np.asarray(im.filter(ImageFilter.GaussianBlur(a.cell / 7)), np.float32) / 255
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lum = .3 * r + .59 * g + .11 * b
    tone = np.clip((lum - a.lo) / (a.hi - a.lo), 0, 1) ** a.gamma       # 0 dark .. 1 light
    warm = np.clip((r - .5 * (g + b)) * a.warm, 0, 1) * np.clip(tone * 2.2, 0, 1)
    hot = np.clip((lum - a.hot) / (1 - a.hot), 0, 1)                    # brightest: bare paper / gold
    sea = screen(1 - tone, a.cell, 22) * (1 - hot)
    tang = screen(np.clip(warm * 1.25, 0, 1), a.cell, 67) * (1 - .8 * hot)
    rs = np.random.RandomState(4)
    paper = np.array(CREAM, np.float32)[None, None] / 255 * (1 - .035 * rs.rand(*lum.shape, 1))
    out = paper.copy()
    if a.gold:
        gold = np.clip(hot * 1.6 + warm * .5, 0, 1)[..., None]
        out = out * (1 - gold) + out * (np.array(GOLD, np.float32) / 255) * gold
    def mul(out, ink, m, k=1.0):
        inkc = np.array(ink, np.float32) / 255
        speck = (rs.rand(*m.shape) > .035).astype(np.float32)             # tiny pinholes in the ink, like a real pull
        m = (m * speck * k)[..., None]
        return out * (1 - m) + out * inkc * m
    out = mul(out, TANG, tang, .96)
    # shift the sea plate by a couple of pixels: misregistration
    sea = np.roll(sea, (a.shift, -a.shift), (0, 1))
    out = mul(out, SEA, sea, .97)
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(a.dst, quality=a.q, method=6)
    print(a.dst, im.size)

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--crop"); p.add_argument("--w", type=int, default=1600); p.add_argument("--cell", type=float, default=7)
    p.add_argument("--lo", type=float, default=.03); p.add_argument("--hi", type=float, default=.5); p.add_argument("--gamma", type=float, default=.8)
    p.add_argument("--warm", type=float, default=3.0); p.add_argument("--hot", type=float, default=.82); p.add_argument("--shift", type=int, default=2)
    p.add_argument("--sharp", type=int, default=160); p.add_argument("--gold", action="store_true"); p.add_argument("--q", type=int, default=82)
    run(p.parse_args())
