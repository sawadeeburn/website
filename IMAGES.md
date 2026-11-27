# Pictures on the site

Every picture on the site is drawn by us in code. No photos, no AI images, no people, no faces.
No photos are used.

## How they are made
Since 27 Nov 2026 the pictures come from the film "Not a Festival": its type and Overprint shapes (drum disc,
crossed bars, bowls, halftone), drawn by `marketing/video/not-a-festival/src/site.py` in the team's private repo
(film.html + shapes.js). The older night-beach scenes (`tools/scenes.html`, `tools/stills.py`, `tools/overprint.py`)
are no longer used on the page.

| File (`public/assets/img/`) | Where | What it shows | Source |
|---|---|---|---|
| `build.webp` | Hero | Drum disc with rings, a tower of crossed bars, three bowls and a gift | "Not a Festival" film shapes (`site.py`) |
| `burn.webp` | Not a festival | "Then we burn it together.", the word hot with sparks (no mark near it) | film frame (`site.py`) |
| `tent.webp` | Bring yourself | Gold ground: one orange disc arriving, a hoop | film shapes (`site.py`) |
| `sail.webp` | Bring art | The tower of crossed bars, the drum disc behind | film shapes (`site.py`) |
| `camp.webp` | Bring a camp | Rust ground: five bowls, a gift passed along | film shapes (`site.py`) |
| `dusk.webp` | Khanom | An orange sun over a halftone sea | film shapes (`site.py`) |
| `gather.webp` | Community | Bowls in a ring round the drum disc | film shapes (`site.py`) |
| `share.jpg` | Link preview | The launch post, square: disc, tower, SaWadee Burn, 2-7 March 2027 | launch post 1 |
| `grain.png`, `ink.png` | Everywhere | Paper grain and ink speckle | generated noise |
| Greeter figure | The welcome | Cut-bust greeter, gate only, never burnt | `brand-src/6a-wai-bust-cut-mark.svg` |
| Logo | Nav, footer (animated: BURN glows) | Final lockup | `brand-src/final-lockup.svg` |
| Route map | Getting there | Coast of the Gulf, Khanom town, Don Sak, islands, airports | Natural Earth 10m (public domain), `tools/map.py` |
| `video/film.mp4`, `video/film-poster.webp` | Film | "Not a Festival", the type-only Overprint film (32.7 s), full length; poster = the NOT A FESTIVAL frame | `marketing/video/not-a-festival/film-web.mp4` (private repo), made in code, no AI images |

## Checks done
- No bicycles in any picture.
- No site address, no pin on the site. The map dot is Khanom town. The film has no map.
- No fire near the W or the greeter. The burn picture sits in its own section with no mark in it.
- No temples, Buddha images, monks, royal symbols, alcohol, drugs, fireworks, sky lanterns or figure burns.
- The burning piece is a woven tower of straight timber: no figure, no roof shape.

## Thai text on the page (needs a native check)
- `สวัสดี` in "The welcome".
- `ไทย` in the nav and footer (links to the live Thai site, sawadeeburn.com/th/).
No other Thai copy was written. A Thai version of this new site is not built.

## Icons
Instagram, Facebook and WhatsApp glyphs are from Simple Icons (CC0), drawn in our ink colours.
