#!/usr/bin/env python3
"""Builds the public brand kit for /brand: every mark in every ink as SVG, PNG and PDF, colour tokens, the two-ink
pictures as JPG, and one ZIP with all of it.
Run: python3 website/tools/brand_kit.py     -> website/public/brand/files/ + website/tools/out/brand.json
Sources are the fixed logo files in brand-src/ (never edited). Rendering: headless Chromium (Playwright)."""
import json, re, shutil, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = Path(__file__).resolve().parent
FC = HERE.parent / "brand-src"
OUT = HERE.parent / "public/brand/files"
IMG = HERE.parent / "public/assets/img"

INKS = {"sea": "#072F35", "cream": "#F2E4D2", "gold": "#F5C65A", "black": "#000000", "white": "#FFFFFF"}
TOKENS = [  # name, hex, what it is for (from the brand skill)
    ("sea", "#072F35", "Dark ground. Ink on cream."),
    ("ink", "#16302F", "Text and the mark."),
    ("cream", "#F2E4D2", "Paper ground."),
    ("gold", "#F5C65A", "The badge, lamp light, small touches."),
    ("tang", "#E4602A", "Big shapes and poster-size type only. Too weak for small text on cream."),
    ("rust", "#973913", "Accent text on cream."),
]
# key, title, source file, tight viewBox (or None = the file's own), inks, PNG width, note
MARKS = [
    ("logo", "The logo", "final-lockup.svg", None, ["sea", "cream", "black", "white"], 2400, "Use this first. It is the name, with the W in the middle."),
    ("logo-thai", "The logo with Thai", "final-lockup-thai.svg", None, ["sea", "cream", "black", "white"], 2400, "For Thai readers and Thai places."),
    ("w", "The W", "final-mark.svg", "22 56 196 128", ["sea", "cream", "black", "white"], 1600, "The W of SaWadee. Its peak is two palms pressed together: the wai. For small spaces."),
    ("badge", "The badge", "final-badge-mark.svg", None, ["gold", "sea", "cream", "black", "white"], 1600, "The W cut out of a disc. Gold on deep sea is the classic."),
    ("badge-logo", "Badge and name", "final-badge-lockup.svg", None, ["sea", "cream", "black", "white"], 2400, "The badge with the name beside it, for wide spaces."),
    ("greeter", "The greeter", "6a-wai-bust-cut-mark.svg", "20 10 200 220", ["sea", "cream", "black", "white"], 1600, "Our second picture. Only where the welcome happens: the gate, greeters, a welcome sign. It never burns."),
]

def svg_for(src, vb, ink):
    s = (FC / src).read_text()
    s = re.sub(r'(<svg[^>]*?) color="[^"]*"', rf'\1 color="{INKS[ink]}"', s, count=1)
    s = s.replace('fill="currentColor"', f'fill="{INKS[ink]}"')
    if vb: s = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', s, count=1)
    return s

def vbox(svg): return [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    meta = {"marks": [], "tokens": [{"name": n, "hex": h, "rgb": [int(h[i:i + 2], 16) for i in (1, 3, 5)], "use": u} for n, h, u in TOKENS]}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        def render(svg, name, width):
            x, y, w, h = vbox(svg)
            H = round(width * h / w)
            (OUT / f"{name}.svg").write_text(svg)
            pg.set_viewport_size({"width": width, "height": H})
            pg.set_content(f'<html><body style="margin:0;background:transparent">{re.sub(r"<svg", f"<svg width={width} height={H} style=display:block", svg, count=1)}</body></html>')
            pg.screenshot(path=str(OUT / f"{name}.png"), omit_background=True)
            pw, ph = 800, round(800 * h / w)                                   # PDF page in CSS px; the art stays vector
            pg.set_content(f'<html><head><style>@page{{size:{pw}px {ph}px;margin:0}}body{{margin:0}}</style></head><body>{re.sub(r"<svg", f"<svg width={pw} height={ph} style=display:block", svg, count=1)}</body></html>')
            pg.pdf(path=str(OUT / f"{name}.pdf"), width=f"{pw}px", height=f"{ph}px", print_background=False, page_ranges="1")
        for key, title, src, vb, inks, width, note in MARKS:
            for ink in inks: render(svg_for(src, vb, ink), f"sawadee-burn-{key}-{ink}", width)
            x, y, w, h = vbox(svg_for(src, vb, inks[0]))
            meta["marks"].append({"key": key, "title": title, "inks": inks, "note": note, "ratio": round(w / h, 4),
                                  "svg": re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", svg_for(src, vb, "sea").replace(INKS["sea"], "currentColor"), flags=re.S)})
        # the avatar: gold badge on deep sea, one file, full colour
        av = (FC / "final-badge-avatar.svg").read_text()
        (OUT / "sawadee-burn-avatar.svg").write_text(av)
        for size in (1024, 400):
            pg.set_viewport_size({"width": size, "height": size})
            pg.set_content(f'<html><body style="margin:0">{re.sub(r"<svg", f"<svg width={size} height={size} style=display:block", av, count=1)}</body></html>')
            pg.screenshot(path=str(OUT / f"sawadee-burn-avatar-{size}.png"))
        Image.open(OUT / "sawadee-burn-avatar-1024.png").convert("RGB").save(OUT / "sawadee-burn-avatar-1024.jpg", quality=92)
        b.close()
    # colour tokens
    (OUT / "sawadee-burn-colours.css").write_text(":root{\n" + "".join(f"  --{n}: {h};   /* {u} */\n" for n, h, u in TOKENS) + "}\n")
    (OUT / "sawadee-burn-colours.json").write_text(json.dumps({n: {"hex": h, "rgb": [int(h[i:i + 2], 16) for i in (1, 3, 5)], "use": u} for n, h, u in TOKENS}, indent=2))
    # the two-ink pictures
    pics = []
    for f in sorted(IMG.glob("*.webp")):
        im = Image.open(f).convert("RGB"); name = f"sawadee-burn-print-{f.stem}.jpg"
        im.save(OUT / name, quality=90); pics.append({"file": name, "thumb": f"/assets/img/{f.name}", "w": im.width, "h": im.height})
    meta["pics"] = pics
    (OUT / "README.txt").write_text(
        "SaWadee Burn brand kit\nhttps://sawadeeburn.com/brand\n\n"
        "Name: SaWadee Burn (capital S, W and B). Handles and links: sawadeeburn.\n\n"
        "Files: every mark as SVG and PDF (vector, any size) and PNG (clear background), in deep sea, cream, black and white.\n"
        "The badge also comes in gold. The avatar is the gold badge on deep sea.\n\n"
        "Colours:\n" + "".join(f"  {n:6} {h}  {u}\n" for n, h, u in TOKENS) +
        "\nType: Bricolage Grotesque (weight 800, width 75%, capitals, tight lines) for headlines; Montserrat (700) for small text;\n"
        "Noto Sans Thai for Thai. All three are free on Google Fonts.\n\n"
        "Rules:\n- Don't stretch, recolour outside the palette, outline or rotate the marks.\n- One mark at a time.\n"
        "- The W and the greeter never burn: no flame, spark or ember on them or near them.\n"
        "- Keep them away from temples, Buddha images, monks, royal images and alcohol.\n"
        "- Not for things on sale, and not next to a sponsor.\n"
        "- This event is not an Official Burning Man event or in any way affiliated with Burning Man Project.\n")
    z = OUT / "sawadee-burn-brand-kit.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(OUT.iterdir()):
            if f == z: continue
            sub = "pictures" if f.name.startswith("sawadee-burn-print-") else "colours" if "colours" in f.name else "" if f.name == "README.txt" else f"logos/{f.suffix[1:]}"
            zf.write(f, f"sawadee-burn-brand-kit/{sub}/{f.name}".replace("//", "/"))
    meta["zip_mb"] = round(z.stat().st_size / 1e6, 1)
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out/brand.json").write_text(json.dumps(meta))
    print("brand kit:", len(list(OUT.iterdir())), "files, zip", meta["zip_mb"], "MB")

if __name__ == "__main__":
    main()
