#!/usr/bin/env python3
"""Builds website/public/index.html from src/index.html + the fixed logo, the route map and the content below.
Run: python3 website/build.py     (map data: python3 website/tools/map.py <natural-earth dir>, kept in tools/out/map.json)
Facts follow the live sawadeeburn.com (checked 26 Nov 2026). No ticket price, no site address, no exact pin."""
import json, re, shutil, time, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
FC = HERE / "brand-src"            # the fixed logo files and the motion kit
PUB = HERE / "public"
TICKETS = "https://www.ticketmelon.com/MarkusHouse/SawadeeBurn2027"

# ---------- fixed logo: paths copied as they are; each path keeps its own fill-rule ----------
def paths(fn): return re.findall(r'<path[^>]*d="([^"]*)"', (FC / fn).read_text())
_l = paths("final-lockup.svg")
_i = _l[0].index(" M344.6 96")
SAW, BURN, WPATH = _l[0][:_i], _l[0][_i + 1:], _l[1]
MARKD = paths("final-mark.svg")[0]
GREET = paths("6a-wai-bust-cut-mark.svg")[0]

LOGO = ('<svg class="logo" viewBox="-23 -159 1029 284" role="img" aria-label="SaWadee Burn">'
        f'<path class="l-saw" fill="currentColor" d="{SAW}"/><path class="l-w" fill="currentColor" fill-rule="evenodd" d="{WPATH}"/>'
        f'<path class="l-burn" fill="currentColor" d="{BURN}"/></svg>')
MARK = f'<svg class="mark" viewBox="22 56 196 128" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{MARKD}"/></svg>'
GREETER = f'<svg class="greeter-fig" viewBox="20 10 200 220"><path fill="currentColor" fill-rule="evenodd" d="{GREET}"/></svg>'

DOT = '<i class="dot"></i>'
TICKER = "".join(f'<span>2-7 March 2027</span>{DOT}<span>Khanom, Thailand</span>{DOT}<span>Come participate</span>{DOT}<span>Come create</span>{DOT}' for _ in range(4))

# ---------- principles (the live site's own summaries, shortened) ----------
PRINCIPLES = [
    ("Radical Inclusion", "Anyone may take part. We welcome the stranger. There are no conditions for belonging."),
    ("Gifting", "A gift is given freely. Nothing is expected back, not even a trade."),
    ("Decommodification", "No sponsors, no buying and selling, no advertising. The gift culture stays clear of commerce."),
    ("Radical Self-Reliance", "Trust what you carry in you, and take care of your own needs."),
    ("Radical Self-Expression", "You decide what your gift is. Offer it with respect for the people who receive it."),
    ("Communal Effort", "We build, support and protect our shared spaces and art together."),
    ("Civic Responsibility", "We look after each other and follow local law: here, the laws and customs of Thailand."),
    ("Leaving No Trace", "We clean up after ourselves, take out what we brought, and leave the land better if we can."),
    ("Participation", "Change comes from taking part fully. Take part instead of watching."),
    ("Immediacy", "Be here now. Drop what stands between you and the people and place around you."),
]

# ---------- FAQ: 16 questions (the live site's 30, merged). Answers follow the live site; open points stay open.
# Answers are HTML (links allowed). ----------
MAIL = '<a href="mailto:ticketing@sawadeeburn.com">ticketing@sawadeeburn.com</a>'
FAQ = [
    ("The basics", [
        ("Is it a festival? Is it Burning Man?", "Neither. The people who come make all of it: there is no lineup, no main stage and no VIP area. We are inspired by the 10 Principles of Burning Man, but this is not an Official Burning Man event and is not affiliated with Burning Man Project."),
        ("I have never been to a burn. Can I come?", "Yes. First-timers and seasoned burners are equally welcome. Come self-reliant, with what you need for six days."),
        ("Where, when and how big?", "2-7 March 2027 in Khanom, on Thailand's Gulf coast. The exact site address goes out with your ticket. We plan for 1,000 to 1,500 people. It is our first full-length burn, so that number may change."),
        ("How do I get a ticket?", 'Only on Ticketmelon, and only in advance: <a href="#tickets">see the ticket rules</a>.'),
        # refund wording = our Ticketmelon event page (ticketing/ticketmelon/raw/10-advanced-setting.txt): refund policy + organizer's disclaimer. Never "full refund".
        ("Can I transfer my ticket, or get a refund?", f"All sales are final. There are no refunds unless the event is cancelled or postponed. If we don't sell enough tickets to make the event happen, all ticket payments will be refunded, minus Ticketmelon's processing fee. The rules for transfers and name changes are not published yet. If you need an answer before you buy, email {MAIL}."),
        ("How do I get there?", 'By ferry from Koh Samui or Koh Phangan, or by air to Nakhon Si Thammarat or Surat Thani and then by road. <a href="#getting-there">Pick your route on the map</a>.'),
    ]),
    ("Camping and packing", [
        ("Where do I sleep?", "In your tent. Everyone camps: in a theme camp, or in free camping, which means camping outside a camp, not free entry. Bring shade and earplugs. Campervans and sleeping in cars are not settled yet, so don't book one."),
        ("What do I bring?", "Enough for six days without shops: shelter and shade, sleeping gear, food, water, a reusable cup and plate, sun and rain cover, insect repellent, your own medication, a small first-aid kit, a torch with spare batteries, a battery pack, rubbish bags and sturdy shoes. The full list comes in the Survival Guide."),
        ("Is there food, water or power?", "Plan as if there is none. Food is not for sale, so bring all of yours. Bring your own water: four litres a day each is a sensible baseline, and water on site is not confirmed yet. Power goes to approved art and camps only, so you cannot charge a phone."),
        ("What is there on site?", "Toilets and showers, and medical and welfare cover. No shops and no public Wi-Fi. Don't count on phone signal: download your ticket and directions before you leave."),
    ]),
    ("On site", [
        ("Can I buy or sell anything?", "No. No vendors, no paid services, no brand promotion and no bartering either. If an essential such as ice has to be sold, we will say so well ahead."),
        ("What about fire, cooking and swimming?", "All three are still being settled with the venue. Assume nothing burns without written approval. Assume there are no lifeguards: nobody swims alone."),
        ("Can I take photos?", "Ask first, every time, and ask again before you post. Coming to a burn is not consent to appear on the internet. Never photograph children without their parent. Professional shoots and drones need approval in advance."),
        ("What is not allowed?", "Pets, personal generators, weapons, fireworks, sky lanterns, glitter, loose feathers, and drones without approval. Leaving anything behind: your rubbish goes home with you, all of it. Thai law applies completely, and so do the venue's rules. The one full list comes later."),
    ]),
    ("People and care", [
        ("Can I bring children or a pet?", f"Children, yes: a child must be registered, and a parent or legal guardian is responsible the whole time. There is no childcare. Write to {MAIL} for a child's ticket. Pets, no: it is too hot, too loud and too far from a vet. For a legally recognised assistance animal, contact us before you book."),
        ("What if I need help?", 'For a medical problem or immediate danger, get the emergency team. If you feel unsafe, go to the <a href="#safer-zone">Safer Zone</a>, a Nomad, the Welfare team or anyone on the organising team. Bring travel insurance that covers Thailand: ambulances and hospitals here are not free.'),
        ("Is the site accessible?", f"We do not know yet. It is a coastal site with sand and uneven ground. Tell us what you need: {MAIL}."),
    ]),
]

# ---------- routes ----------
# Ranges like "1 h 10 to 1 h 20" were confusing, and the old site's "Samui 1 h" was too short. So: one figure
# per leg, the total first, and checked numbers instead of the live site's:
#   drives = Google Maps to the site (checked 26 Nov 2026): Don Sak 25 min, NST "1 hr 41 min",
#            URT "1 hr 44 min", Krabi "3 hr 24 min", Phuket "4 hr 11 min";
#   Samui car ferry about 1 h 30 min (Rome2Rio 1h 37m, Ferryscanner 1h 30m, Direct Ferries "average 1 h 30 m");
#   Phangan ferry 2 h 30 min (Openferry, Direct Ferries); flights and train: a flight and train search of Nov 2026, rounded.
# option: (name, big figure, its label, legs [(kind, time)], one plain line)
ROUTES = [
    ("islands", "Samui and Phangan", "From the islands", [
        ("Koh Samui", "1 h 55 min", "in all", [("ferry", "1 h 30 min"), ("drive", "25 min")], "Car ferry to Don Sak pier, then the road to Khanom."),
        ("Koh Phangan", "2 h 55 min", "in all", [("ferry", "2 h 30 min"), ("drive", "25 min")], "Ferry to Don Sak pier, then the road to Khanom."),
    ], "The ferries carry cars and scooters. Ferries from Koh Tao come in to Don Sak too."),
    ("bangkok", "Bangkok", "From Bangkok", [
        ("Fly to Nakhon Si Thammarat", "2 h 55 min", "in all", [("fly", "1 h 15 min"), ("drive", "1 h 40 min")], "Then a car or minivan from the airport."),
        ("Fly to Surat Thani", "3 h", "in all", [("fly", "1 h 15 min"), ("drive", "1 h 45 min")], "Then a car or minivan from the airport."),
        ("Night train", "14 h", "in all", [("train", "13 h"), ("drive", "1 h")], "Sleeper to Surat Thani, then a minivan to Khanom."),
    ], "Bangkok has two airports. Most flights south leave from Don Mueang (DMK), not Suvarnabhumi (BKK)."),
    ("south", "Surat Thani and Nakhon", "From the nearest airports", [
        ("Nakhon Si Thammarat (NST)", "1 h 40 min", "by road", [("drive", "1 h 40 min")], "Airport to Khanom."),
        ("Surat Thani (URT)", "1 h 45 min", "by road", [("drive", "1 h 45 min")], "Airport to Khanom."),
    ], "Both towns also have buses and minivans towards Khanom."),
    ("andaman", "Phuket and Krabi", "From the Andaman coast", [
        ("Krabi (KBV)", "3 h 25 min", "by road", [("drive", "3 h 25 min")], "Across the peninsula to Khanom."),
        ("Phuket (HKT)", "4 h 10 min", "by road", [("drive", "4 h 10 min")], "Across the peninsula to Khanom."),
    ], "Coming with friends? One car across is the simple way."),
    ("asia", "Asia", "From around Asia", [
        ("Singapore", "3 h 55 min", "in all", [("fly", "2 h"), ("ferry", "1 h 30 min"), ("drive", "25 min")], "Non-stop to Koh Samui, then as from Samui."),
        ("Bali", "4 h 30 min", "to Bangkok", [("fly", "4 h 30 min")], "Non-stop. From Bangkok add about 3 h."),
        ("Kuala Lumpur, Hong Kong", "1 stop", "in Bangkok", [], "Change planes in Bangkok. From there add about 3 h."),
    ], "Flight times are from a search in November 2026. Check the airlines for March."),
    ("world", "The world", "From further away", [
        ("Europe", "11 h", "to Bangkok", [("fly", "11 h")], "Non-stop from London or Frankfurt. From Bangkok add about 3 h."),
        ("North America", "23 h", "to Bangkok", [("fly", "23 h")], "With one stop. From Bangkok add about 3 h."),
    ], "Long flights land at Suvarnabhumi (BKK). Flights south mostly leave from Don Mueang (DMK). Leave a few hours to cross town, or stay a night."),
]
ICON = {
    "drive": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 15l2-6h14l2 6v4H3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="7.500" cy="19" r="2" fill="currentColor"/><circle cx="16.500" cy="19" r="2" fill="currentColor"/></svg>',
    "ferry": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 14h18l-3 5H6z M7 14V9h10v5 M10 9V5h4v4" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "fly": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 14l20-7-7 13-3-6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "train": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M5 11h14 M8 21l2-4 M16 21l-2-4" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
}
KIND = {"drive": "Drive", "ferry": "Ferry", "fly": "Flight", "train": "Train"}

# Words the pages must never carry (the brand rules). Private ones (names, places) live in banned.local.txt, which is not in the repo.
BANNED = ["thb", "one price", " city", "on sale", "early bird", "guests", "volunteer", "shift", "bike", "bicycle"]
_local = HERE / "banned.local.txt"
if _local.exists(): BANNED += [w.strip().lower() for w in _local.read_text().splitlines() if w.strip()]

def route_tabs():
    return "".join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="route-{k}" aria-selected="{"true" if i == 0 else "false"}" data-route="{k}"{"" if i == 0 else " tabindex=-1"}>{html.escape(lab)}</button>'
                   for i, (k, lab, *_) in enumerate(ROUTES))

def route_panels():
    out = ""
    for i, (k, lab, title, opts, note) in enumerate(ROUTES):
        body = ""
        for name, big, biglab, legs, line in opts:
            chain = "".join(f'<li class="lg lg-{kind}">{ICON[kind]}<span><i class="vh">{KIND[kind]} </i>{t}</span></li>' for kind, t in legs) if len(legs) > 1 else ""
            chain = f'<ol class="chain">{chain}</ol>' if chain else ""
            body += (f'<div class="opt"><p class="tot"><b>{big}</b><span>{biglab}</span></p>'
                     f'<div class="opt-b"><h4>{html.escape(name)}</h4>{chain}<p>{html.escape(line)}</p></div></div>')
        out += (f'<div class="route" role="tabpanel" id="route-{k}" aria-labelledby="tab-{k}" data-route="{k}"{"" if i == 0 else " hidden"}>'
                f'<h3 class="big">{html.escape(title)}</h3>{body}<p class="small">{html.escape(note)}</p></div>')
    return out

# ---------- social links: icons over text, in several places ----------
SOC_ICON = {'whatsapp': 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z', 'instagram': 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077', 'facebook': 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z'}
WA_UPDATES = "https://chat.whatsapp.com/DsnkBWqcZJBJFKlb3BZ7hG"                # news only, made 27 Nov 2026
WA_COMMUNITY = "https://chat.whatsapp.com/JHGfzF6utfO6M5jJKNe80o?mode=gi_t"   # the open chat, 200+ people (the group the old site linked)
TG_COMMUNITY = "https://t.me/sawadeeburn"
REPO = "https://github.com/sawadeeburn/website"
SOC_ICON["telegram"] = "M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"
SOCIALS = [
    ("instagram", "Instagram", "SaWadee Burn on Instagram", "https://www.instagram.com/sawadeeburn/"),
    ("facebook", "Facebook", "The SaWadee Burn Facebook group", "https://www.facebook.com/share/g/19vpA2Yy2N/"),
    ("whatsapp", "Updates", "WhatsApp updates group", WA_UPDATES),
]
COMMUNITY = [("whatsapp", "Community chat on WhatsApp", WA_COMMUNITY), ("telegram", "Community chat on Telegram", TG_COMMUNITY)]
def _svg(icon): return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{SOC_ICON[icon]}"/></svg>'
def social(cls, only_live=False):
    out = "".join(f'<li><a class="soc soc-{icon}" href="{url}" rel="noopener" aria-label="{aria}">{_svg(icon)}<span>{label}</span></a></li>' for icon, label, aria, url in SOCIALS)
    if not only_live:      # the community chats: two small links in the space of one, kept quiet on purpose
        duo = "".join(f'<a href="{url}" rel="noopener" aria-label="{aria}">{_svg(icon)}</a>' if url else f'<span class="soon" role="img" aria-label="{aria}: opens soon">{_svg(icon)}</span>' for icon, aria, url in COMMUNITY)
        out += f'<li><div class="soc duo"><span class="duo-ring">{duo}</span><span>Community</span></div></li>'
    return f'<ul class="social {cls}">{out}</ul>'

# ---------- the map ----------
def map_svg():
    m = json.loads((HERE / "tools/out/map.json").read_text())
    P = m["places"]; W, H = m["w"], m["h"]
    def q(a, b, bend=.18):   # a gentle arc between two points
        (x1, y1), (x2, y2) = a, b
        mx, my = (x1 + x2) / 2 - (y2 - y1) * bend, (y1 + y2) / 2 + (x2 - x1) * bend
        return f"M{x1:.0f} {y1:.0f}Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}"
    K, D = P["khanom"], P["donsak"]
    top1, top2 = (560, -10), (700, -10)
    se = (W + 10, 900)
    routes = {
        "islands": [("ferry", q(P["samui"], D, -.15)), ("ferry", q(P["phangan"], D, .22)), ("drive", q(D, K, -.2))],
        "bangkok": [("fly", q(top1, P["urt"], .12)), ("fly", q(top2, P["nst"], -.22)), ("drive", q(P["urt"], K, -.12)), ("drive", q(P["nst"], K, .1))],
        "south": [("drive", q(P["urt"], K, -.12)), ("drive", q(P["nst"], K, .1))],
        "andaman": [("drive", q(P["hkt"], P["kbv"], -.1)), ("drive", q(P["kbv"], K, -.14))],
        "asia": [("fly", q(se, P["usm"], .2)), ("ferry", q(P["samui"], D, -.15)), ("drive", q(D, K, -.2)), ("fly", q(top1, P["urt"], .12))],
        "world": [("fly", q(top1, P["urt"], .12)), ("fly", q(top2, P["nst"], -.22)), ("drive", q(P["urt"], K, -.12)), ("drive", q(P["nst"], K, .1))],
    }
    s = [f'<svg class="map" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Map of the Gulf coast of southern Thailand: Khanom, the Don Sak piers, Koh Samui, Koh Phangan and the airports at Nakhon Si Thammarat, Surat Thani, Krabi and Phuket.">']
    s.append('<g class="rip" fill="none">' + "".join(f'<path d="{r["d"]}" stroke-opacity="{r["o"]}"/>' for r in m["rings"]) + '</g>')
    s.append(f'<path class="land" d="{m["land"]}"/><path class="shore" fill="none" d="{m["land"]}"/>')
    for k, legs in routes.items():
        s.append(f'<g class="rt" data-route="{k}">' + "".join(f'<path class="r-{kind}" d="{d}" pathLength="1"/>' for kind, d in legs) + '</g>')
    def lab(key, text, dx=14, dy=5, cls="", anchor="start", sub=None):
        x, y = P[key]
        t = f'<g class="pl {cls}" data-place="{key}"><circle cx="{x}" cy="{y}" r="6"/><text x="{x + dx}" y="{y + dy}" text-anchor="{anchor}">{text}</text>'
        if sub: t += f'<text class="sub" x="{x + dx}" y="{y + dy + 22}" text-anchor="{anchor}">{sub}</text>'
        return t + '</g>'
    s.append(lab("hkt", "Phuket", 0, -18, "air", "middle", "HKT"))
    s.append(lab("kbv", "Krabi", 0, 30, "air", "middle", "KBV"))
    s.append(lab("urt", "Surat Thani", -14, -4, "air", "end", "URT"))
    s.append(lab("nst", "Nakhon Si Thammarat", -14, 6, "air", "end", "NST"))
    s.append(lab("donsak", "Don Sak piers", -14, -12, "pier", "end"))
    s.append(lab("samui", "Koh Samui", 60, 30, "isle"))
    s.append(lab("phangan", "Koh Phangan", 26, -8, "isle"))
    s.append(lab("tao", "Koh Tao", 18, 6, "isle"))
    kx, ky = K
    s.append(f'<g class="pl khanom"><circle class="ring" cx="{kx}" cy="{ky}" r="22"/><circle class="ring r2" cx="{kx}" cy="{ky}" r="22"/><circle cx="{kx}" cy="{ky}" r="9"/>'
             f'<text x="{kx + 30}" y="{ky + 12}">Khanom</text></g>')
    s.append(f'<g class="edge" data-for="bangkok world asia"><text x="630" y="34" text-anchor="middle">Bangkok, 650 km north</text></g>')
    s.append(f'<g class="edge" data-for="asia"><text x="{W - 16:.0f}" y="950" text-anchor="end">Singapore</text></g>')
    s.append(f'<text class="sea-lab" x="850" y="640" text-anchor="middle">Gulf of Thailand</text>')
    s.append('</svg>')
    return "".join(s)

def principles():
    return "".join(f'<li><h3 class="big">{html.escape(n)}</h3><p>{html.escape(t)}</p></li>' for n, t in PRINCIPLES)

def faq():
    out = ""
    for group, qs in FAQ:
        out += f'<div class="faq-group"><h3>{html.escape(group)}</h3>'
        for qn, an in qs:
            out += f'<details><summary>{html.escape(qn)}</summary><p>{an}</p></details>'
        out += '</div>'
    return out

# ---------- /brand: the brand kit page (files come from tools/brand_kit.py) ----------
INK_NAME = {"sea": "Deep sea", "cream": "Cream", "gold": "Gold", "black": "Black", "white": "White"}
INK_HEX = {"sea": "#072F35", "cream": "#F2E4D2", "gold": "#F5C65A", "black": "#000000", "white": "#FFFFFF"}
PIC_ALT = {"build": "a woven timber tower half built on the beach", "burn": "the timber tower burning, hand lights in a ring", "camp": "a shade sail over a long shared table",
           "dusk": "the sun going down over the sea", "gather": "hand lights gathering round one lamp", "sail": "three masts strung with lit string", "tent": "one lit tent under the moon"}
def build_brand(v):
    m = json.loads((HERE / "tools/out/brand.json").read_text())
    cards = ""
    for k in m["marks"]:
        first = k["inks"][0]
        inks = "".join(f'<button type="button" data-ink="{i}" aria-pressed="{"true" if i == first else "false"}" style="--c:{INK_HEX[i]}" aria-label="{INK_NAME[i]}"></button>' for i in k["inks"])
        dl = "".join(f'<a class="dl" data-ext="{e}" href="/brand/files/sawadee-burn-{k["key"]}-{first}.{e}" download>{e.upper()}</a>' for e in ("svg", "png", "pdf"))
        cards += (f'<article class="mk{" mk-square" if k["ratio"] < 1.6 else ""}" data-key="{k["key"]}" data-ink="{first}"><div class="mk-stage" aria-hidden="true">{k["svg"]}</div>'
                  f'<div class="mk-body"><h3 class="big">{html.escape(k["title"])}</h3><p>{html.escape(k["note"])}</p>'
                  f'<div class="mk-inks" role="group" aria-label="Ink for {html.escape(k["title"]).lower()}">{inks}<span class="ink-name" aria-live="polite">{INK_NAME[first]}</span></div>'
                  f'<p class="mk-dl">{dl}</p></div></article>')
    toks = ""
    for t in m["tokens"]:
        dark = sum(t["rgb"]) < 400
        toks += (f'<li><button type="button" class="sw" data-hex="{t["hex"]}" style="--c:{t["hex"]};--t:{"#F2E4D2" if dark else "#072F35"}" aria-label="Copy {t["name"]}, {t["hex"]}">'
                 f'<span class="sw-chip">{t["name"]}</span><span class="sw-meta"><b>{t["hex"]} &nbsp; RGB {t["rgb"][0]} {t["rgb"][1]} {t["rgb"][2]}</b><span>{html.escape(t["use"])}</span></span></button></li>')
    pics = "".join(f'<li><a href="/brand/files/{p["file"]}" download><img src="{p["thumb"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" alt="Two-ink print: {PIC_ALT.get(p["file"].split("print-")[1].split(".")[0], "the beach at night")}"><span>Download JPG</span></a></li>' for p in m["pics"])
    t = (HERE / "src/brand.html").read_text()
    rep = {"REPO": REPO, "LOGO": LOGO, "MARK_CARDS": cards, "TOKENS": toks, "PICS": pics, "ZIP_MB": str(m["zip_mb"]), "SOCIAL_ROW": social("s-row", True), "V": v}
    for k, val in rep.items(): t = t.replace("{{" + k + "}}", val)
    assert "{{" not in t, "placeholder left on the brand page"
    low = re.sub(r"<[^>]+>", " ", t).lower()
    for bad in BANNED:
        assert bad not in low or bad in (" city", "guests", "shift"), f"banned text on the brand page: {bad}"
    (PUB / "brand").mkdir(exist_ok=True)
    (PUB / "brand/index.html").write_text(t)
    for f in ("brand.css", "brand.js"): shutil.copy(HERE / "src" / f, PUB / "assets" / f)
    print("built", PUB / "brand/index.html", len(t) // 1024, "KB")

# ---------- /crews: the crew board. Data in crews.json (opt-in, public). Points don't matter, no prizes. ----------
# Each crew: slug (a-z0-9-, its short link), name, flag (file in crews-flags/ or ""), code (3 characters from the
# pre-made pool; the Ticketmelon affiliate link is aff1=crew-<code>, e.g. crew-kzt, so names can change any time), tickets (from that
# link), line (optional, one short line), live (true once its Ticketmelon link exists).
CREW_START = ("mailto:ticketing@sawadeeburn.com?subject=Start%20a%20crew&body=Crew%20name%3A%20%0A"
              "Your%20first%20name%3A%20%0AWhatsApp%3A%20%0AOne%20line%20about%20your%20crew%20(optional)%3A%20%0A%0A"
              "Attach%20a%20picture%20for%20your%20flag%20if%20you%20have%20one.")
FLAG_INKS = [("var(--gold)", "var(--sea)"), ("var(--tang)", "#04191D"), ("var(--sea)", "var(--cream)"), ("var(--rust)", "var(--cream)")]

def crew_flag(c):
    if c.get("flag"):
        return f'<img class="flag" src="/crews/flags/{html.escape(c["flag"])}" alt="" width="96" height="96" loading="lazy">'
    bg, fg = FLAG_INKS[sum(map(ord, c["slug"])) % len(FLAG_INKS)]
    ini = "".join(w[0] for w in re.findall(r"[A-Za-z0-9]+", c["name"])[:2]).upper() or "?"
    return f'<span class="flag flag-ini" style="--fb:{bg};--ff:{fg}" aria-hidden="true">{html.escape(ini)}</span>'

def build_crews(v, head, foot, data=None):
    crews = data if data is not None else json.loads((HERE / "crews.json").read_text())
    for c in crews:
        assert re.fullmatch(r"[a-z0-9-]{2,40}", c["slug"]), f"bad crew slug: {c['slug']}"
    crews = sorted(crews, key=lambda c: (-c.get("tickets", 0), c["name"].lower()))
    rows = ""
    for i, c in enumerate(crews):
        n = int(c.get("tickets", 0))
        lamps = "".join(f'<i style="--d:{(j % 12) * 60}ms"></i>' for j in range(n)) or '<em>No lamps yet. Soon.</em>'
        line = f'<p class="crew-line">{html.escape(c["line"])}</p>' if c.get("line") else ""
        link = f'<a class="crew-link" href="/crew/{c["slug"]}">sawadeeburn.com/crew/{c["slug"]}</a>' if c.get("live") else ""
        rows += (f'      <li class="crew" style="--r:{((i * 37) % 7 - 3) * .4}deg">{crew_flag(c)}<div class="crew-body">'
                 f'<h3>{html.escape(c["name"])}</h3>{line}<p class="lamps" aria-label="{n} lamp{"s" if n != 1 else ""} lit">{lamps}</p>{link}</div></li>\n')
    if not crews:
        rows = '      <li class="crew crew-empty"><span class="flag flag-ini" style="--fb:var(--gold);--ff:var(--sea)" aria-hidden="true">?</span><div class="crew-body"><h3>Your crew here</h3><p class="crew-line">The board is empty. Be the first flag on it.</p></div></li>\n'
    note = "The order changes every time someone buys a ticket. Or every time you press the button." if len(crews) > 1 else "Crews show up here as they start."
    t = (HERE / "src/crews-body.html").read_text()
    for k, val in {"BOARD": rows, "BOARD_NOTE": note, "START_URL": CREW_START, "SHUFFLE_HIDDEN": "" if len(crews) > 1 else "hidden"}.items():
        t = t.replace("{{" + k + "}}", val)
    page = (head.replace("<title>SaWadee Burn", "<title>Crews · SaWadee Burn", 1)
                .replace('content="A community-created', 'content="Start a crew, get your own link, light lamps on the board. Points don\'t matter. A community-created', 1)
            + t + foot)
    assert "{{" not in page, re.findall(r"\{\{\w+\}\}", page)
    low = re.sub(r"<[^>]+>", " ", page).lower()
    for bad in BANNED:
        assert bad not in low, f"banned text on the crews page: {bad}"
    (PUB / "crews").mkdir(exist_ok=True)
    (PUB / "crews/index.html").write_text(page)
    flags = HERE / "crews-flags"
    if flags.is_dir():
        shutil.copytree(flags, PUB / "crews/flags", dirs_exist_ok=True)
    # short links: /crew/<slug> -> Ticketmelon with the crew's affiliate code (only once its link exists there)
    redir = "".join(f'/crew/{c["slug"]} {TICKETS}?aff1=crew-{c["code"]} 302\n' for c in crews if c.get("live"))
    (PUB / "_redirects").write_text(redir)
    print("built", PUB / "crews/index.html", len(crews), "crews,", redir.count("\n"), "links")

def site_shell(t):
    """Header and footer of the home page, with links made absolute, for the sub-pages."""
    fix = lambda s: s.replace('"assets/', '"/assets/').replace('"favicon.svg', '"/favicon.svg').replace('href="#', 'href="/#').replace('href="brand/', 'href="/brand/')
    head = fix(t.split("<main")[0])
    foot = fix(t[t.index('<footer'):]).replace('</body>', '<script src="/assets/crews.js?v=' + str(int(time.time())) + '" defer></script>\n</body>')
    return head, foot

def build():
    t = (HERE / "src/index.html").read_text()
    rep = {"LOGO": LOGO, "MARK": MARK, "GREETER": GREETER, "TICKER": TICKER, "TICKETS": TICKETS, "MAP": map_svg(),
           "ROUTE_TABS": route_tabs(), "ROUTE_PANELS": route_panels(), "PRINCIPLES": principles(), "FAQ": faq(), "SOCIAL_ROW": social("s-row", True), "SOCIAL_BIG": social("s-big"), "SOCIAL_FOOT": social("s-row s-foot", True), "SOCIAL_BAND": social("s-big s-band"), "REPO": REPO, "V": str(int(time.time()))}
    for k, v in rep.items(): t = t.replace("{{" + k + "}}", v)
    assert "{{" not in t, re.findall(r"\{\{\w+\}\}", t)
    low = re.sub(r"<[^>]+>", " ", t).lower()
    for bad in BANNED:
        assert bad not in low, f"banned text on the page: {bad}"
    PUB.mkdir(exist_ok=True)
    (PUB / "index.html").write_text(t)
    for f in ("site.css", "site.js", "crews.js"): shutil.copy(HERE / "src" / f, PUB / "assets" / f)
    (PUB / "assets/motion").mkdir(exist_ok=True)
    for f in ("assets.js", "sawadee-motion.js"): shutil.copy(FC / "motion" / f, PUB / "assets/motion" / f)
    shutil.copy(FC / "final-badge-avatar.svg", PUB / "favicon.svg")   # the W badge stays the tab icon (the symbol blurs at 16px)
    shutil.copy(HERE / "src/draft-concept.html", PUB / "draft-concept.html")   # CONCEPT only
    (PUB / "draft-avatar.html").write_text((HERE / "src/draft-avatar.html").read_text().replace("{{LOGO}}", LOGO))   # CONCEPT only: Artem's symbol as the avatar
    for f in ("artem-avatar.svg", "artem-avatar-plain.svg", "artem-mark.svg", "final-badge-avatar.svg"): shutil.copy(FC / f, PUB / "assets/img" / f)
    (PUB / "404.html").write_text(t.split("<main")[0].replace("<title>", "<title>Not found · ").replace('"assets/', '"/assets/').replace('"favicon.svg', '"/favicon.svg').replace('href="#', 'href="/#') +
        '<main id="main"><section class="hero f-paper lost"><div class="wrap"><h1 class="big"><span class="fit">Lost on the beach.</span></h1>'
        '<p class="lede">This page does not exist. The burn does.</p><p><a class="btn" href="/">Back to the start</a></p></div></section></main>'
        f'<script src="/assets/site.js" defer></script></body></html>')
    (PUB / "_headers").write_text("/*\n  X-Robots-Tag: noindex\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
                                  "/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/img/*\n  Cache-Control: public, max-age=86400\n/assets/video/*\n  Cache-Control: public, max-age=86400\n/brand/files/*\n  Cache-Control: public, max-age=3600\n")
    (PUB / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print("built", PUB / "index.html", len(t) // 1024, "KB")
    build_brand(rep["V"])
    build_crews(rep["V"], *site_shell(t))

if __name__ == "__main__":
    build()
