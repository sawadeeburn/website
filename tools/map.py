#!/usr/bin/env python3
"""Night-coast regional map for 'Getting there'. Natural Earth 10m land (public domain) -> website/tools/out/map.json
Run: python3 map.py <dir with land.geojson + minor.geojson>   (needs shapely)
Never marks the burn site: Khanom is the town, Don Sak is the pier."""
import json, math, os, sys
from shapely.geometry import shape, box, Polygon, MultiPolygon
from shapely.ops import unary_union

SRC = sys.argv[1]
LON0, LON1, LAT0, LAT1 = 97.95, 100.62, 7.72, 10.42
W = 1000.0
KX = W / ((LON1 - LON0) * math.cos(math.radians(9.1)))   # px per degree of latitude
H = (LAT1 - LAT0) * KX
def P(lon, lat): return ((lon - LON0) * math.cos(math.radians(9.1)) * KX, (LAT1 - lat) * KX)

clip = box(LON0 - .3, LAT0 - .3, LON1 + .3, LAT1 + .3)
geoms = []
for f in ("land.geojson", "minor.geojson"):
    for ft in json.load(open(os.path.join(SRC, f)))["features"]:
        g = shape(ft["geometry"])
        if g.intersects(clip): geoms.append(g.intersection(clip))
land = unary_union(geoms)

def proj(g):
    out = []
    for p in (g.geoms if isinstance(g, MultiPolygon) else [g]):
        if p.geom_type != "Polygon": continue
        out.append(Polygon([P(*c) for c in p.exterior.coords]))
    return unary_union(out)
land = proj(land).buffer(3, join_style=1).buffer(-3, join_style=1)   # round the coarse corners a little
view = box(-20, -20, W + 20, H + 20)

def d(g, prec=1):
    s = ""
    for p in (g.geoms if hasattr(g, "geoms") else [g]):
        if p.geom_type != "Polygon" or p.is_empty: continue
        s += "M" + " ".join(f"{x:.{prec}f} {y:.{prec}f}" for x, y in p.exterior.coords[:-1]) + "Z"
    return s

rings = []
N, STEP = 9, 9
for k in range(1, N + 1):
    r = land.buffer(k * STEP, join_style=1).intersection(view).simplify(.6)
    rings.append({"d": d(r), "o": round(max(.05, .42 * (1 - k / (N + 1)) ** 1.4), 2)})

PLACES = {
    "khanom": (99.86, 9.20), "donsak": (99.69, 9.33), "nst": (99.9447, 8.5396), "urt": (99.1356, 9.1326),
    "kbv": (98.9862, 8.0992), "hkt": (98.3169, 8.1132), "samui": (99.935, 9.535), "phangan": (99.985, 9.711),
    "tao": (99.83, 10.09), "usm": (100.0623, 9.5478), "surat": (99.33, 9.14), "nakhon": (99.96, 8.43),
}
out = {"w": W, "h": round(H, 1), "land": d(land.intersection(view).simplify(.4)), "rings": rings,
       "places": {k: [round(v, 1) for v in P(*ll)] for k, ll in PLACES.items()}}
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"), exist_ok=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "map.json"), "w"))
print("map", out["w"], out["h"], len(out["land"]), sum(len(r["d"]) for r in rings), out["places"])
