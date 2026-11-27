# SaWadee Burn: website and brand

The website and brand kit of SaWadee Burn, a community-created, non-profit burn by the sea.
2-7 March 2027, Khanom, Thailand.

- Site (preview): https://sawadee-burn-site.pages.dev
- Brand kit: https://sawadee-burn-site.pages.dev/brand

*This event is not an Official Burning Man event or in any way affiliated with Burning Man Project.*

## Suggest an edit

Spotted a mistake, a broken link or a clearer way to say something?
Open an issue, or change the text and send a pull request. Small fixes are welcome.

- Page text and layout: `src/index.html` (home) and `src/brand.html` (brand kit).
- Questions, travel routes, principles and social links: the lists at the top of `build.py`.
- Then run `python3 build.py` and include the changed `public/` files in your pull request.

## How it is built

Plain HTML, CSS and JavaScript. No framework.

| Path | What |
|---|---|
| `src/` | The pages, styles and scripts you edit |
| `build.py` | Fills in the logo, map, routes, questions and brand kit, and writes `public/` |
| `public/` | The built site. A push to `main` deploys it to Cloudflare Pages |
| `brand-src/` | The logo files (SVG) and the logo motion kit. Fixed: don't redraw them |
| `tools/brand_kit.py` | Makes every brand file in `public/brand/files/` (SVG, PNG, PDF, ZIP). Needs Playwright and Pillow |
| `tools/scenes.html`, `stills.py`, `overprint.py` | Draw the pictures in code and print them in two inks |
| `tools/map.py` | Builds the route map from Natural Earth coastline data |

`build.py` needs only Python 3. It stops if a page breaks a brand rule (for example, a ticket price).

## Using the brand

The logo, colours and pictures are free to use for the burn: a poster, a flag, a camp sign, a post.
The few rules are on the [brand kit page](https://sawadee-burn-site.pages.dev/brand).
Please don't use them on things for sale or next to a sponsor.

## Licence

Apache License 2.0: see `LICENSE`. Copy it, change it, build on it.
The licence does not cover the name and the logo as a trademark (its section 6), so please follow the brand kit rules when you use them.
The fonts in `public/assets/fonts/` are other people's work, under the SIL Open Font License.

## Credits

Fonts: Bricolage Grotesque, Montserrat and Noto Sans Thai (SIL Open Font License).
Route map coastline: Natural Earth. Film map: © OpenStreetMap contributors. Social icons: Simple Icons.
All pictures are drawn in code by the SaWadee Burn team. See `IMAGES.md`.
