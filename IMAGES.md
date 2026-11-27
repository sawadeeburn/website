# Pictures on the site

Every picture on the site is drawn by us in code. No photos, no AI images, no people, no faces.
No photos are used.

## How they are made
1. `tools/scenes.html` draws a scene on a canvas ("low tide": the night beach from the water, straight timber,
   one warm light, wet sand that mirrors it; people show only as traces).
2. `tools/stills.py <dir>` saves each scene as a PNG.
3. `tools/overprint.py` prints it in two inks (deep sea + tangerine, a touch of gold) on cream paper.

| File (`public/assets/img/`) | Where | What it shows | Source |
|---|---|---|---|
| `build.webp` | Hero | A woven timber tower half built, ladder, one lamp, timber | scene `build` |
| `burn.webp` | Not a festival | The tower burning, hand lights in a wide ring | scene `burn` |
| `tent.webp` | Bring yourself | One lit tent, a flag, footprints, the moon | scene `tent` |
| `sail.webp` | Bring art | Three masts strung with lit string, a ladder | scene `sail` |
| `camp.webp` | Bring a camp | Shade sail, long shared table with lamps, tents | scene `camp` |
| `dusk.webp` | Khanom | Sun going down over the sea | a frame of the earlier `dates` teaser (drawn in code; that scene has since been reworked) |
| `gather.webp` | Community | Hand lights drawing in round one lamp | scene `gather` |
| `share.jpg` | Link preview | Launch post 1 | our first launch post |
| `grain.png`, `ink.png` | Everywhere | Paper grain and ink speckle | generated noise |
| Greeter figure | The welcome | Cut-bust greeter, gate only, never burnt | `brand-src/6a-wai-bust-cut-mark.svg` |
| Logo | Nav, footer (animated: BURN glows) | Final lockup | `brand-src/final-lockup.svg` |
| Route map | Getting there | Coast of the Gulf, Khanom town, Don Sak, islands, airports | Natural Earth 10m (public domain), `tools/map.py` |
| `video/film.mp4` | Film | Our drawn Khanom film (people gather, play, the burn), without its opening map shot | made by the team, drawn in code |

## Checks done
- No bicycles in any picture.
- No site address, no pin on the site. The map dot is Khanom town. The web film starts after the film's opening map shot.
- No fire near the W or the greeter. The burn picture sits in its own section with no mark in it.
- No temples, Buddha images, monks, royal symbols, alcohol, drugs, fireworks, sky lanterns or figure burns.
- The burning piece is a woven tower of straight timber: no figure, no roof shape.

## Thai text on the page (needs a native check)
- `สวัสดี` in "The welcome".
- `ไทย` in the nav and footer (links to the live Thai site, sawadeeburn.com/th/).
No other Thai copy was written. A Thai version of this new site is not built.

## Icons
Instagram, Facebook and WhatsApp glyphs are from Simple Icons (CC0), drawn in our ink colours.
