#!/usr/bin/env python3
"""Pinterest batch: ~84 pins over 4 weeks following the posting plan.

Weeks 1-2: 2 pins/day (1 seasonal + 1 evergreen); weeks 3-4: 4/day (2 + 2).
Rules checked before writing: same link never twice the same day, >= 7 days between pins of the same page.
Seasonal = Christmas framing of the scratch card and the party games. Evergreen = dreams, names, feng shui, room planner.
Writes _pins_batch/<id>.html (rendered by Chrome), then Desktop/Sapiopedia/Pinterest/batch-2026-11/ + the bulk CSV.
"""
import csv, datetime, json, os, random, re, subprocess, base64, html, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest")
OUTD = os.path.join(DESK, "batch-2026-11"); os.makedirs(OUTD, exist_ok=True)
TMP = os.path.join(ROOT, "_pins_batch"); os.makedirs(TMP, exist_ok=True)
GAMES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "games.json"), encoding="utf-8"))
src = open(os.path.join(ROOT, "tools", "make_pins.py"), encoding="utf-8").read()
exec(src[:src.index("def band(")])            # HEAD (styles), THUMB, E (EN dreams), N (names), IDX, esc
HEAD = HEAD.replace(".mid{flex:1;", ".main{flex:1;").replace(".top{padding:70px ", ".top{padding:104px ")   # room under the free badge
EF = {e["id"]: e for e in json.load(open(os.path.join(ROOT, "data", "dreams_fr.json")))["entries"]}
READY = json.load(open(os.path.join(ROOT, "data", "ready.json")))["batches"][0]
random.seed(2026)
SITE = "https://sapiopedia.com"

def band(url, label):
    return f'<div class="band"><img src="/assets/logo-horizontal.png" alt=""><div class="u"><b>{esc(url)}</b><span>{esc(label)}</span></div></div>'

FREE_CSS = '<style>.free{position:absolute;top:18px;right:40px;z-index:5;background:#8E2F48;color:#fff;font:700 24px "Source Sans 3",sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px;box-shadow:0 4px 12px -4px rgba(42,31,38,.4)}</style>'
def free(lang): return f'{FREE_CSS}<div class="free">{"Free · No sign-up" if lang == "en" else "Gratuit · Sans inscription"}</div>'
def page(pid, kick, title, sub, mid, url, label, extra=""):
    lang = "fr" if "/fr/" in url else "en"
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(
        HEAD + THUMB + free(lang) + f'<div class="pin"><div class="top"><div class="kick">{kick}</div><h1>{title}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div><div class="main">{mid}</div>{band(url, label)}</div>{extra}</body></html>')

PINS = []   # dicts: id, group (seasonal/evergreen), link, title, desc, board, tags, render (fast/slow)
def add(**k):
    d = k.get("desc", ""); fr = "/fr/" in k.get("link", "")
    if not re.search(r"no sign-up|sans inscription", d, re.I): d = d.rstrip() + (" Gratuit, sans inscription." if fr else " Free, no sign-up.")
    k["desc"] = d[:500]; k["title"] = html.unescape(k.get("title", "")); PINS.append(k)

# ---------------------------------------------------------------- existing 12 pins (already on the site under /pins/)
old = list(csv.DictReader(open(os.path.join(DESK, "pins.csv"), encoding="utf-8")))
for r in old:
    seasonal = r["file"].startswith(("09", "10"))
    add(id=r["file"][:-4], file=r["file"], old=True, group="seasonal" if seasonal else "evergreen", link=r["link"], title=r["title"],
        desc=r["description"], board=r["board"], tags=r["tags"].replace(";", ","))

# ---------------------------------------------------------------- dreams (single entry pins, EN + FR)
def dots(n): return "●" * n + f'<s>{"●" * (5 - n)}</s>'
def dream_pin(pid, e, lang, h1):
    sits = e["situations"]
    pick = ([s for s in sits if s[2] == "up"][:2] + [s for s in sits if s[2] == "mid"][:1] + [s for s in sits if s[2] == "down"][:1])[:4]
    lis = "".join(f'<li><svg class="th {s[2]}" viewBox="0 0 24 24"><use href="#th"/></svg><span><i>{esc(s[0])}:</i> {esc(s[1])}</span></li>' for s in pick)
    lab = "What happens in the dream" if lang == "en" else "Ce qui se passe dans le rêve"
    mid = (f'<div class="book"><div class="dtitle"><span class="ini">{esc(e["word"][0])}</span><div><h2>{esc(e["title"])}</h2><p><span class="dots">{dots(e["tone"])}</span> {esc(e["tone_label"])}</p></div></div>'
           f'<p class="lead">{esc(e["one"])}</p><h3>{lab}</h3><ul>{lis}</ul></div>')
    slug = "dreams" if lang == "en" else "reves"
    page(pid, "Dream dictionary" if lang == "en" else "Dictionnaire des rêves", h1, "", mid, f"sapiopedia.com/{lang}/{slug}/{e['id']}/",
         "2,598 dreams, explained in plain words" if lang == "en" else "2 598 rêves expliqués simplement")
    return f"{SITE}/{lang}/{slug}/{e['id']}/"

used_dreams = {"snake", "teeth", "flying"}
for i, did in enumerate([d for d in READY["dreams_en"] if d not in used_dreams][:14]):
    e = E[did]; w = re.sub(r"^Dreaming of ", "", e["title"]).lower()
    h1 = [f"What does it mean to <em>dream of {esc(w)}?</em>", f"Dreaming of <em>{esc(w)}</em>: what it means", f"Did you dream of <em>{esc(w)}?</em>"][i % 3]
    link = dream_pin(f"d-en-{did}", e, "en", h1)
    add(id=f"d-en-{did}", group="evergreen", link=link, title=re.sub("<.*?>", "", h1).replace("&#x27;", "'"),
        desc=f"{e['one']} Look up every version of the dream, good signs and bad, in Sapiopedia's dream dictionary.", board="Dream meanings",
        tags=f"Dream meanings, Dream interpretation, {re.sub(r'^(an?|the) ', '', w).capitalize()} dream meaning, Dream dictionary, Spiritual meaning, Dreams, Symbolism, Self reflection")
for i, did in enumerate(READY["dreams_fr"][:8]):
    e = EF[did]; w = re.sub(r"^Rêver (d['’]une? |de la |du |des |de |d['’])", "", e["title"])
    h1 = [f"Rêver <em>{esc(w)}</em> : que signifie ce rêve ?", f"Que veut dire <em>{esc(e['title'].lower())}</em> ?"][i % 2]
    link = dream_pin(f"d-fr-{did}", e, "fr", h1)
    add(id=f"d-fr-{did}", group="evergreen", link=link, title=re.sub("<.*?>", "", h1),
        desc=f"{e['one']} Toutes les versions de ce rêve, bons et mauvais signes, dans le dictionnaire des rêves de Sapiopedia.", board="Dream meanings",
        tags=f"Signification des rêves, Interprétation des rêves, Rêve {w}, Dictionnaire des rêves, Spiritualité, Rêves, Symbolisme")

# ---------------------------------------------------------------- names (single card pins, link to the name's own page)
SYMB = {"f": "♀", "m": "♂", "n": "⚥", "u": ""}
GLAB = {"en": {"f": "French girl's name", "m": "French boy's name", "n": "French name for girls and boys", "u": "French first name"},
        "fr": {"f": "Prénom féminin français", "m": "Prénom masculin français", "n": "Prénom mixte français", "u": "Prénom français"}}
import sys; sys.path.insert(0, ROOT); from content.names_fr import card_slugs  # noqa: E402
def name_pin(pid, name, lang):
    r = N[name]; ids, _ = card_slugs()
    base = "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/"
    ipa = re.sub(r"^\^\(\(.*?\)\)", "", r.get("ipa", ""))
    rows = []
    if r.get("oe" if lang == "en" else "o"): rows.append(("Origin" if lang == "en" else "Origine", (r["oe"] if lang == "en" else r["o"].capitalize())))
    if r.get("att"): rows.append(("First recorded" if lang == "en" else "Première mention", r["att"].replace("c. ", "about " if lang == "en" else "vers ")))
    if r.get("v"): rows.append(("Also spelled" if lang == "en" else "Autres graphies", ", ".join(r["v"][:5])))
    if r.get("tr"): rows.append(("Around the world" if lang == "en" else "Ailleurs", " · ".join(f"{', '.join(v[:2])}" for k, v in list(r["tr"].items())[:4])))
    et = r.get("ete") if lang == "en" else r.get("et")
    mid = (f'<div class="book" style="padding:60px 60px"><div class="dtitle"><span class="ini" style="font-size:170px">{esc(name[0])}</span><div><h2 style="font-size:116px">{esc(name)}</h2>'
           f'<p style="font-size:38px">{esc(ipa)} · <b style="font-style:normal;color:#8E2F48">{SYMB[r["g"]]}</b> {esc(GLAB[lang][r["g"]])}</p></div></div>'
           + (f'<p class="lead" style="font-size:38px;margin:10px 0 34px">{esc(et[:230] + ("…" if len(et) > 230 else ""))}</p>' if et else "")
           + '<ul style="gap:26px">' + "".join(f'<li style="grid-template-columns:300px 1fr;font-size:34px"><span style="font-family:IM Fell English SC,serif;color:#5B4A40">{esc(a)}</span><span>{esc(b)}</span></li>' for a, b in rows) + "</ul></div>")
    url = f"{SITE}{base}{ids[name]}/"
    page(pid, "French first names" if lang == "en" else "Prénoms français",
         (f"<em>{esc(name)}</em>: meaning, origin and how to say it" if lang == "en" else f"<em>{esc(name)}</em> : origine, signification et prononciation"),
         "", mid, url.replace("https://", ""), "9,128 French names with pronunciation" if lang == "en" else "9 128 prénoms avec leur prononciation")
    return url
nm = [n for n in READY["names"] if N.get(n, {}).get("ipa")]
for i, name in enumerate(nm[:8]):
    link = name_pin(f"n-en-{i}", name, "en")
    add(id=f"n-en-{i}", group="evergreen", link=link, title=f"{name}: French name meaning, origin and pronunciation",
        desc=f"{name} is a {GLAB['en'][N[name]['g']].lower()}. Its origin, how to say it the French way, and its versions in other languages.", board="French baby names",
        tags=f"French baby names, {name} name meaning, Baby names, Baby name ideas, Name meanings, Unique baby names, Pregnancy, French aesthetic")
for i, name in enumerate(nm[8:12]):
    link = name_pin(f"n-fr-{i}", name, "fr")
    add(id=f"n-fr-{i}", group="evergreen", link=link, title=f"{name} : origine, signification et prononciation du prénom",
        desc=f"{name}, {GLAB['fr'][N[name]['g']].lower()} : son origine, sa prononciation et ses équivalents dans d'autres langues.", board="French baby names",
        tags=f"Prénoms, Idées de prénoms, Prénom {name}, Signification des prénoms, Prénoms français, Grossesse, Bébé")

# ---------------------------------------------------------------- party games, framed for Christmas gatherings
GAME_H1 = {
 "truth-or-dare-questions": (["<em>Truth or Dare</em> for your Christmas party", "Truth or Dare questions for <em>holiday game night</em>", "Clean <em>Truth or Dare</em> for the whole family"],
                             ["<em>Action ou vérité</em> pour votre soirée de Noël", "Action ou vérité : des questions <em>pour les Fêtes</em>", "<em>Action ou vérité</em> tout public pour Noël"]),
 "would-you-rather-questions": (["<em>Would You Rather</em> questions for Christmas dinner", "Would You Rather: <em>holiday edition night</em>", "<em>Would You Rather</em> for the family table"],
                                ["<em>Tu préfères</em> : des questions pour le repas de Noël", "Des <em>Tu préfères</em> pour les soirées des Fêtes", "<em>Tu préfères</em> en famille à Noël"]),
 "never-have-i-ever-questions": (["<em>Never Have I Ever</em> for your holiday party", "Never Have I Ever: <em>clean and funny</em>", "<em>Never Have I Ever</em> for Christmas night"],
                                 ["<em>Je n'ai jamais</em> pour votre soirée des Fêtes", "Je n'ai jamais : <em>drôle et sans alcool</em>", "<em>Je n'ai jamais</em> pour le soir de Noël"]),
 "icebreaker-questions-for-groups": (["Icebreakers for your <em>office Christmas party</em>", "Questions for the <em>family Christmas dinner</em>", "<em>Icebreakers</em> for holiday get-togethers"],
                                     ["Brise-glace pour le <em>party de bureau</em>", "Des questions pour le <em>souper de Noël en famille</em>", "<em>Brise-glace</em> pour les réunions des Fêtes"]),
 "two-truths-and-a-lie-ideas": (["<em>Two Truths and a Lie</em> for holiday parties", "Two Truths and a Lie: <em>ideas that work</em>", "A Christmas party game: <em>two truths, one lie</em>"],
                                ["<em>Deux vérités, un mensonge</em> pour les Fêtes", "Deux vérités, un mensonge : <em>des idées qui marchent</em>", "Un jeu pour Noël : <em>deux vérités, un mensonge</em>"]),
 "first-date-questions": (["Cosy <em>date night</em> questions for winter", "<em>First date</em> questions for the holidays", "Questions for a <em>holiday date</em>"],
                          ["Questions pour un <em>tête-à-tête d'hiver</em>", "Des questions de <em>premier rendez-vous</em> pour les Fêtes", "Questions pour un <em>rendez-vous de décembre</em>"]),
}
def game_pin(pid, slug, lang, v):
    g = GAMES[slug]; groups = g["groups"][lang]
    gi = v % len(groups); head, items = groups[gi]
    pick = random.sample(items, min(5, len(items)))
    if slug == "truth-or-dare-questions":   # clean set only for Christmas pins: truths then dares
        t = random.sample(groups[0][1], 3); d = random.sample(groups[2][1], 2)
        cards = "".join(f'<div class="t"><small>{"Truth" if lang == "en" else "Vérité"}</small>{esc(x)}</div>' for x in t) + "".join(f'<div class="d"><small>{"Dare" if lang == "en" else "Action"}</small>{esc(x)}</div>' for x in d)
    else:
        cards = "".join(f'<div class="t"><small>{esc(head)}</small>{esc(x)}</div>' for x in pick)
    h1 = GAME_H1[slug][0 if lang == "en" else 1][v % 3]
    base = f"/en/games/{slug}/" if lang == "en" else f"/fr/jeux/{g['slug']['fr']}/"
    page(pid, "Christmas party games" if lang == "en" else "Jeux pour les Fêtes", h1, "Draw one at random on your phone." if lang == "en" else "Tirez-en une au hasard sur votre téléphone.",
         f'<div class="q">{cards}</div>', f"sapiopedia.com{base}", g["title"][lang])
    return f"{SITE}{base}", re.sub("<.*?>", "", h1), g["title"][lang]
for slug in GAMES:
    for lang, n in (("en", 3), ("fr", 3)):
        for v in range(n):
            if slug == "truth-or-dare-questions" and lang == "en" and v == 0: continue   # the existing pin 10 covers this one
            pid = f"g-{lang}-{slug[:12]}-{v}"
            link, title, gname = game_pin(pid, slug, lang, v)
            add(id=pid, group="seasonal", link=link, title=title,
                desc=(f"{gname}: real questions you can draw at random on your phone. Perfect for Christmas dinners, holiday parties and game nights. Free." if lang == "en"
                      else f"{gname} : des questions à tirer au hasard sur votre téléphone. Parfait pour les repas de Noël et les soirées des Fêtes. Gratuit."),
                board="Christmas party games", tags=("Christmas party games, Christmas games, Holiday party ideas, Family game night, Party games for adults, Game night ideas, Christmas activities, Fun questions" if lang == "en"
                      else "Jeux de Noël, Jeux de société, Soirée entre amis, Jeux en famille, Idées soirée, Noël, Jeux pour adultes"))

# ---------------------------------------------------------------- scratch card, Christmas (real tool on a phone, falling snow)
def b64(d): return base64.urlsafe_b64encode(json.dumps(d, ensure_ascii=False).encode()).decode().rstrip("=")
XMAS = [
 ("en", {"recipient": "Mia", "gift": "Ice skating, then hot chocolate", "message": "Saturday, 3 pm. Bring mittens.", "sender": "Leo", "fx": "snow"}, "A Christmas gift they <em>scratch to open</em>", "Perfect for virtual gifts: write it, send the link, let it snow."),
 ("fr", {"recipient": "Chloé", "gift": "Un week-end au chalet", "message": "Feu de foyer, chocolat chaud et zéro réveil.", "sender": "Thomas", "fx": "snow"}, "Un cadeau de Noël <em>à gratter</em>", "Écrivez la surprise, envoyez le lien, et la neige tombe."),
 ("fr", {"recipient": "Maman", "gift": "Une journée au spa", "message": "Pour toi, parce que tu le mérites.", "sender": "Julie", "fx": "hearts"}, "Le cadeau virtuel <em>parfait pour Noël</em>", "Carte à gratter envoyée par lien. Gratuit, sans appli."),
 ("fr", {"recipient": "Lucas", "gift": "Deux billets pour le match", "message": "On y va ensemble le 27.", "sender": "Ton frère", "fx": "confetti"}, "Noël à distance ? <em>Envoyez une carte à gratter</em>", "Elle se gratte sur le téléphone, avec confettis, cœurs ou neige."),
 ("fr", {"recipient": "Inès", "gift": "Un cours de poterie", "message": "Le 10 janvier, on y va ensemble.", "sender": "Sarah", "fx": "snow"}, "Une surprise de Noël <em>en un seul lien</em>", "Prête en une minute. Parfait pour les cadeaux de dernière minute."),
]
PHONE = (open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch_pin_template.html"), encoding="utf-8").read())
for i, (lang, gift, h1, sub) in enumerate(XMAS):
    base = "/en/tools/scratch-gift-card/" if lang == "en" else "/fr/outils/carte-cadeau-a-gratter/"
    pid = f"s-{lang}-xmas-{i}"
    html_ = PHONE.replace("{{H1}}", h1).replace("{{P}}", sub).replace("{{URL}}", base + "#gift=" + b64(gift)).replace("{{TARGET}}", "0.25").replace("{{FOOT}}", "scratch-off gift card" if lang == "en" else "carte cadeau à gratter")
    html_ = html_.replace("<body>", "<body>" + free(lang), 1)
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(html_)
    add(id=pid, group="seasonal", link=SITE + base, title=re.sub("<.*?>", "", h1), slow=True,
        desc=("A scratch-off Christmas card you send as a link: they scratch on their phone and the gift appears under falling snow. Perfect for virtual gifts and long-distance Christmas. Free." if lang == "en"
              else "Une carte de Noël à gratter, envoyée par lien : on gratte sur son téléphone et le cadeau apparaît. Idéal pour les cadeaux virtuels et Noël à distance. Gratuit."),
        board="Gift ideas", tags=("Christmas gift ideas, Virtual gift ideas, Digital gift, Scratch off card, Long distance Christmas, Last minute gifts, Gift card ideas, Christmas surprise" if lang == "en"
              else "Idées cadeaux Noël, Cadeau virtuel, Carte à gratter, Cadeau de dernière minute, Noël à distance, Idée cadeau, Surprise"))

# ---------------------------------------------------------------- feng shui and room planner variants (FR pages + a second EN angle)
for pid, lang, kind, h1, sub in [("fs-fr-0", "fr", "fengshui", "Votre lit est-il <em>bien placé ?</em>", "Dessinez votre chambre : chaque meuble reçoit un verdict feng shui."),
                                 ("fs-en-1", "en", "fengshui", "3 bed placement <em>mistakes to avoid</em>", "Feet toward the door, under a window, between door and window: check yours."),
                                 ("rp-fr-0", "fr", "room-planner", "Aménagez votre pièce, <em>puis voyez-la en 3D</em>", "Tailles exactes, vrais meubles, vos couleurs de sol et de murs."),
                                 ("rp-en-1", "en", "room-planner", "Try your <em>sofa layout</em> before you move it", "Exact sizes, clearance check, then a 3D view in your colours.")]:
    tool = "fengshui" if kind == "fengshui" else ("room-planner" if lang == "en" else "planificateur-de-piece")
    base = f"/{lang}/{'tools' if lang == 'en' else 'outils'}/{tool}/"
    html_ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{kind}_pin_template.html"), encoding="utf-8").read()
    html_ = html_.replace("{{H1}}", h1).replace("{{SUB}}", sub).replace("{{TOOL}}", base).replace("{{URL}}", "sapiopedia.com" + base).replace("{{KICK}}", ("Feng shui room planner" if kind == "fengshui" else "Free room planner") if lang == "en" else ("Planificateur feng shui" if kind == "fengshui" else "Planificateur de pièce gratuit"))
    html_ = html_.replace("{{VARIANT}}", pid)
    html_ = html_.replace('<div class="pin">', free(lang) + '<div class="pin">', 1)
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(html_)
    add(id=pid, group="evergreen", link=SITE + base, title=re.sub("<.*?>", "", h1), slow=True,
        desc=(sub + " Free, in your browser." if lang == "en" else sub + " Gratuit, dans votre navigateur."),
        board="Feng shui bedroom" if kind == "fengshui" else "Room layout ideas",
        tags=("Feng shui bedroom, Bed placement, Bedroom layout, Feng shui tips, Bedroom ideas, Interior design" if kind == "fengshui" else "Room layout, Room planner, Living room layout, Furniture arrangement, Interior design, Floor plan")
        if lang == "en" else ("Feng shui chambre, Aménagement chambre, Déco chambre, Feng shui, Disposition du lit" if kind == "fengshui" else "Aménagement salon, Plan de pièce, Déco intérieur, Disposition des meubles"))

# ---------------------------------------------------------------- the room planner's ready-made rooms, shown big in 3D (one link per room)
ROOMS = {
 "cosy-bedroom": ("A cosy bedroom, <em>ready to try in 3D</em>", "Une chambre douillette <em>à essayer en 3D</em>", "Bedroom layout", "Aménagement chambre"),
 "small-studio": ("Small studio? <em>Make it all fit</em>", "Petit studio ? <em>Tout peut rentrer</em>", "Studio apartment layout", "Aménagement studio"),
 "living-room": ("A living room layout <em>that flows</em>", "Un salon <em>bien aménagé</em>", "Living room layout", "Aménagement salon"),
 "evening-living": ("See your room <em>with the lamps on</em>", "Votre pièce <em>lampes allumées</em>", "Cozy living room", "Salon cosy"),
 "home-office": ("A home office <em>in 3.6 × 3.2 m</em>", "Un bureau à la maison <em>en 3,6 × 3,2 m</em>", "Home office layout", "Bureau à la maison"),
 "kitchen-diner": ("Kitchen and dining <em>in one room</em>", "Cuisine et salle à manger <em>dans une pièce</em>", "Kitchen layout", "Aménagement cuisine"),
 "bathroom": ("Plan your bathroom <em>before you renovate</em>", "Votre salle de bain, <em>planifiée avant les travaux</em>", "Bathroom layout", "Aménagement salle de bain"),
 "kids-room": ("A kids' room <em>with a bunk bed</em>", "Une chambre d'enfant <em>avec lits superposés</em>", "Kids room ideas", "Chambre enfant"),
}
def rp_base(lang, fs=False):
    return f"/{lang}/{'tools' if lang == 'en' else 'outils'}/{'fengshui' if fs else ('room-planner' if lang == 'en' else 'planificateur-de-piece')}/"
CAP3D = ('<script>var f=document.createElement("iframe");f.style.cssText="position:absolute;left:-4000px;width:1300px;height:1000px";f.src="{SRC}";'
         'f.onload=function(){setTimeout(function(){var c=f.contentDocument.querySelector(".v3dwrap canvas");if(c){var i=new Image();i.src=c.toDataURL("image/png");'
         'i.style.cssText="width:100%;display:block";document.getElementById("shot").appendChild(i);}},5000);};document.body.appendChild(f);</script>')
for key, (h_en, h_fr, tag_en, tag_fr) in ROOMS.items():
    for lang in ("en", "fr"):
        base = rp_base(lang); h1 = h_en if lang == "en" else h_fr; pid = f"r3d-{lang}-{key}"
        chips = ["Exact sizes", "Your floor and walls", "Plan ↔ 3D"] if lang == "en" else ["Tailles exactes", "Vos sols et murs", "Plan ↔ 3D"]
        page(pid, "Free room planner" if lang == "en" else "Planificateur de pièce gratuit", h1,
             "Open this exact room, then make it yours." if lang == "en" else "Ouvrez cette pièce, puis adaptez-la.",
             '<div class="shot" id="shot" style="background:#fff;padding:10px"></div><div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>",
             "sapiopedia.com" + base, "Free, in your browser" if lang == "en" else "Gratuit, dans votre navigateur", extra=CAP3D.replace("{SRC}", f"{base}?preset={key}&view=3d"))
        add(id=pid, group="room", slow=True, link=f"{SITE}{base}?preset={key}&view=3d", title=re.sub("<.*?>", "", h1),
            desc=("This room is ready to open in Sapiopedia's free room planner: real furniture at real sizes, a clearance check, and a 3D view in your own floor and wall colours. Move anything, then save it as an image."
                  if lang == "en" else "Cette pièce s'ouvre telle quelle dans le planificateur gratuit de Sapiopedia : vrais meubles aux vraies tailles, vérification des passages et vue 3D dans vos couleurs. Déplacez tout, puis enregistrez l'image."),
            board="Room layout ideas", tags=(f"{tag_en}, Room planner, Room layout, Furniture arrangement, Interior design, Home decor, Floor plan, 3D room design" if lang == "en"
                                             else f"{tag_fr}, Plan de pièce, Disposition des meubles, Déco intérieur, Aménagement, Plan 3D"))

FS3D = {
 "cosy-bedroom": ("A feng shui bedroom, <em>in 3D</em>", "Une chambre feng shui, <em>en 3D</em>"),
 "small-studio": ("Feng shui for a <em>small studio</em>", "Le feng shui <em>dans un petit studio</em>"),
 "living-room": ("A feng shui <em>living room</em> layout", "Un salon <em>feng shui</em>"),
 "evening-living": ("Warm light, <em>good energy</em>", "Lumière douce, <em>bonne énergie</em>"),
 "home-office": ("Feng shui your <em>home office</em>", "Un bureau <em>feng shui</em>"),
 "kitchen-diner": ("Feng shui for <em>kitchen and dining</em>", "Cuisine et salle à manger <em>feng shui</em>"),
 "bathroom": ("A calm <em>feng shui bathroom</em>", "Une salle de bain <em>feng shui</em>"),
 "kids-room": ("Feng shui for a <em>kids' room</em>", "Une chambre d'enfant <em>feng shui</em>"),
}
for key, (h_en, h_fr) in FS3D.items():
    for lang in ("en", "fr"):
        base = rp_base(lang, True); h1 = h_en if lang == "en" else h_fr; pid = f"f3d-{lang}-{key}"
        chips = ["Verdict for every piece", "Door and window lines", "Plan ↔ 3D"] if lang == "en" else ["Un verdict par meuble", "Lignes porte-fenêtre", "Plan ↔ 3D"]
        page(pid, "Feng shui room planner" if lang == "en" else "Planificateur feng shui", h1,
             "Open this room and see the feng shui verdict for each piece." if lang == "en" else "Ouvrez cette pièce et voyez le verdict feng shui de chaque meuble.",
             '<div class="shot" id="shot" style="background:#fff;padding:10px"></div><div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>",
             "sapiopedia.com" + base, "Free feng shui room planner" if lang == "en" else "Planificateur feng shui gratuit", extra=CAP3D.replace("{SRC}", f"{base}?preset={key}&view=3d"))
        bed = key in ("cosy-bedroom", "kids-room", "small-studio")
        add(id=pid, group="room", slow=True, link=f"{SITE}{base}?preset={key}&view=3d", title=re.sub("<.*?>", "", h1),
            desc=("This room opens as-is in Sapiopedia's free feng shui planner: every piece gets a verdict (command position, door and window lines, clutter), with a 3D view in your own colours. Move things until everything is green."
                  if lang == "en" else "Cette pièce s'ouvre telle quelle dans le planificateur feng shui gratuit : chaque meuble reçoit un verdict (position de commandement, lignes porte-fenêtre), avec une vue 3D dans vos couleurs."),
            board="Feng shui bedroom" if bed else "Feng shui home",
            tags=("Feng shui, Feng shui tips, Feng shui home, Feng shui bedroom, Good energy home, Room layout, Interior design, Home decor" if lang == "en"
                  else "Feng shui, Feng shui maison, Feng shui chambre, Aménagement, Déco intérieur, Énergie positive"))

# ---------------------------------------------------------------- the exact PNG the room planner saves (2D plan + 3D view), used as the pin image as-is
EXPORTS = [("en", "living-room", False), ("en", "cosy-bedroom", False), ("en", "small-studio", False), ("en", "kitchen-diner", False), ("en", "home-office", False),
           ("fr", "evening-living", False), ("fr", "bathroom", False), ("fr", "kids-room", False), ("en", "cosy-bedroom", True), ("fr", "living-room", True),
           ("en", "evening-living", False), ("en", "bathroom", False), ("en", "kids-room", False), ("fr", "living-room", False), ("fr", "cosy-bedroom", False),
           ("fr", "small-studio", False), ("fr", "kitchen-diner", False), ("fr", "home-office", False),
           ("en", "small-studio", True), ("en", "living-room", True), ("en", "home-office", True), ("en", "kids-room", True),
           ("fr", "cosy-bedroom", True), ("fr", "bathroom", True), ("fr", "evening-living", True), ("fr", "small-studio", True)]
for lang, key, fs in EXPORTS:
    base = rp_base(lang, fs); pid = f"x-{'fs' if fs else 'rp'}-{lang}-{key}"
    nm = re.sub("<.*?>", "", ROOMS[key][0 if lang == "en" else 1])
    if fs:
        title = (f"{nm}: feng shui check, plan and 3D in one image" if lang == "en" else f"{nm} : vérification feng shui, plan et 3D en une image")
        desc = ("This is the image the free feng shui room planner saves: every piece coloured by its verdict on the plan, next to the 3D view. Draw your own room and get yours."
                if lang == "en" else "Voici l'image qu'enregistre le planificateur feng shui gratuit : chaque meuble coloré selon son verdict sur le plan, à côté de la vue 3D. Dessinez votre pièce pour obtenir la vôtre.")
        board, tags = "Feng shui bedroom", ("Feng shui bedroom, Feng shui, Bedroom layout, Bed placement, Floor plan, Interior design" if lang == "en" else "Feng shui, Feng shui chambre, Plan de pièce, Aménagement, Déco intérieur")
    else:
        title = (f"{nm}: plan and 3D view, saved in one image" if lang == "en" else f"{nm} : le plan et la vue 3D en une image")
        desc = ("What you get when you save from the free Room Planner: the 2D plan with every piece checked for clearance, next to the 3D view. This room opens as-is from the link."
                if lang == "en" else "Ce que vous obtenez en enregistrant depuis le planificateur gratuit : le plan 2D avec chaque meuble vérifié, à côté de la vue 3D. Cette pièce s'ouvre telle quelle depuis le lien.")
        board, tags = "Room layout ideas", (f"{ROOMS[key][2]}, Floor plan, Room planner, Room layout, Furniture arrangement, Interior design" if lang == "en" else f"{ROOMS[key][3]}, Plan de pièce, Disposition des meubles, Aménagement, Déco intérieur")
    add(id=pid, group="room", export=f"{base}?preset={key}", link=f"{SITE}{base}?preset={key}", title=title, desc=desc, board=board, tags=tags)

# ---------------------------------------------------------------- the scratch card as the recipient sees it once scratched (a phone screen, nothing else)
REVEAL = [("en", {"recipient": "Sam", "gift": "Concert tickets for two", "message": "Friday, 8 pm. I'll drive.", "sender": "Alex", "fx": "confetti"},
           "What they see when they scratch your gift", "Gift ideas", "evergreen"),
          ("en", {"recipient": "Emma", "gift": "A weekend in Québec City", "message": "Happy anniversary. Pack light.", "sender": "Noah", "fx": "hearts"},
           "A virtual gift, revealed with hearts", "Gift ideas", "evergreen"),
          ("fr", {"recipient": "Léa", "gift": "Un souper au restaurant", "message": "Joyeux anniversaire ! Samedi, 19 h.", "sender": "Max", "fx": "confetti"},
           "Ce que voit la personne qui gratte votre cadeau", "Gift ideas", "evergreen"),
          ("fr", {"recipient": "Papa", "gift": "Une journée de pêche", "message": "Joyeux Noël. Je m'occupe du café.", "sender": "Camille", "fx": "snow"},
           "Un cadeau de Noël révélé sous la neige", "Gift ideas", "seasonal")]
REVEAL_HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch_reveal_template.html"), encoding="utf-8").read()
for i, (lang, gift, title, board, grp) in enumerate(REVEAL):
    base = "/en/tools/scratch-gift-card/" if lang == "en" else "/fr/outils/carte-cadeau-a-gratter/"
    pid = f"sr-{lang}-{i}"
    badge = '<style>body{position:relative}.free{top:28px;right:17px;font-size:10px;padding:4px 8px}</style>'   # the page is 420 px wide, shot at 2.4x
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(REVEAL_HTML.replace("{{URL}}", base + "#gift=" + b64(gift)).replace("<body>", "<body>" + free(lang) + badge, 1))
    add(id=pid, group=grp, slow=True, win=(420, 630, 2.4), link=SITE + base, title=title, board=board,
        desc=("A scratch-off card you send as a link: this is the screen they see once it's scratched, with the effect you picked (confetti, hearts or snow)."
              if lang == "en" else "Une carte à gratter envoyée par lien : voici l'écran qu'on voit une fois la carte grattée, avec l'effet choisi (confettis, cœurs ou neige)."),
        tags=("Virtual gift ideas, Scratch off card, Digital gift, Surprise reveal, Gift ideas, Birthday surprise, Anniversary gift ideas, Gift card ideas" if lang == "en"
              else "Cadeau virtuel, Carte à gratter, Idée cadeau, Surprise, Cadeau d'anniversaire, Cadeau de Noël"))

# ---------------------------------------------------------------- baby pins (Nov 2026): gender reveal, pregnancy announcement, two nurseries.
# Group "baby" is left out of the schedule below (the first 103 pins were already uploaded): they get their own CSV, pinterest-bulk-upload-baby.csv.
BABY_CARDS = [("bc-en-gender", "/en/tools/gender-reveal-scratch-card/",
               {"recipient": "Grandma and Grandpa", "gift": "It's a girl!", "message": "Due in May. We can't wait for you to meet the baby.", "sender": "Love, Sam and Alex", "fx": "pink"},
               "Gender reveal scratch card: pink or blue confetti",
               "Boy or girl? Make a scratch-off card and send the link: they scratch it on their phone and pink or blue confetti bursts out. For a party or at a distance.",
               "Gender reveal ideas, Gender reveal, Baby gender reveal, Boy or girl, Gender reveal party, Baby shower ideas, Pregnancy announcement, Scratch off card"),
              ("bc-en-pregnancy", "/en/tools/pregnancy-announcement-scratch-card/",
               {"recipient": "Mom and Dad", "gift": "You're going to be grandparents!", "message": "Baby arrives in June. We couldn't wait to tell you.", "sender": "Love, Sam and Alex", "fx": "confetti"},
               "Scratch-off pregnancy announcement for grandparents",
               "Tell them with a scratch-off card sent as a link: they scratch it on their phone and find out they're going to be grandparents. Ideas for aunts, uncles and big sisters too.",
               "Pregnancy announcement, Pregnancy announcement to grandparents, Baby announcement, Pregnancy reveal ideas, Grandparents announcement, Baby announcement ideas, Scratch off card, Pregnancy")]
for pid, base, gift, title, desc, tags in BABY_CARDS:
    badge = '<style>body{position:relative}.free{top:28px;right:17px;font-size:10px;padding:4px 8px}</style>'   # the page is 420 px wide, shot at 2.4x
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(REVEAL_HTML.replace("{{URL}}", base + "#gift=" + b64(gift)).replace("<body>", "<body>" + free("en") + badge, 1))
    add(id=pid, group="baby", slow=True, win=(420, 630, 2.4), link=SITE + base, title=title, board="Gift ideas", desc=desc, tags=tags)
NURSERIES = [("n3d-en-nursery", "nursery", "Plan the nursery <em>before baby arrives</em>", "Open this nursery, then make it yours.",
              "Crib, changing table, glider and storage at real sizes, with safety checks: the crib away from windows and blind cords, tall furniture flagged for anchoring. In 2D and 3D.",
              "Nursery ideas, Nursery layout, Baby room ideas, Nursery decor, Small nursery ideas, Baby nursery, Nursery inspiration, Room planner"),
             ("n3d-en-shared-nursery", "shared-nursery", "Baby in your room: <em>where the bassinet fits</em>", "A bassinet beside your bed, planned in 3D.",
              "Many parents keep the baby in their room for the first months. Open this bedroom with a bassinet beside the bed and a glider for night feeds, then move things to fit your room.",
              "Bassinet in parents room, Room sharing with baby, Nursery in master bedroom, Small space nursery, Baby room ideas, Nursery ideas, Bedroom layout, Room planner")]
for pid, key, h1, sub, desc, tags in NURSERIES:
    base = "/en/tools/nursery-planner/"
    page(pid, "Free nursery planner", h1, sub,
         '<div class="shot" id="shot" style="background:#fff;padding:10px"></div><div class="chips">' + "".join(f"<span>{c}</span>" for c in ["Crib, changing table, glider", "Safety checks", "Plan ↔ 3D"]) + "</div>",
         "sapiopedia.com" + base, "Free, in your browser", extra=CAP3D.replace("{SRC}", f"{base}?preset={key}&view=3d"))
    add(id=pid, group="baby", slow=True, link=f"{SITE}{base}?preset={key}&view=3d", title=re.sub("<.*?>", "", h1), board="Gift ideas", desc=desc, tags=tags)

# ---------------------------------------------------------------- the French names index itself, scrolled to one letter
IXCSS = '<style>.ixf{flex:1;min-height:0;border-radius:20px;overflow:hidden;box-shadow:0 24px 50px -24px rgba(42,31,38,.45);background:#F6E9EC;margin-bottom:36px}.ixf iframe{width:560px;height:720px;border:0;display:block;transform:scale(1.53);transform-origin:0 0}</style>'
IXJS = ('<script>var f=document.getElementById("ix");f.onload=function(){setTimeout(function(){var d=f.contentDocument,w=f.contentWindow;'
        'd.querySelectorAll("*").forEach(function(el){var p=w.getComputedStyle(el).position;if(p==="sticky"||p==="fixed")el.style.position="static";});'
        'd.querySelectorAll("section.nf-l").forEach(function(x){if(x.id!=="l-{L}")x.style.display="none";});function go(){var e=d.getElementById("l-{L}");w.scrollTo(0,e.getBoundingClientRect().top+w.scrollY-14);}go();setTimeout(go,800);setTimeout(go,2000);},1200);};</script>')
for lang, L in (("en", "L"), ("fr", "C")):
    base = "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/"; pid = f"ix-{lang}-{L}"
    h1 = "9,128 French names, <em>from A to Z</em>" if lang == "en" else "9 128 prénoms, <em>de A à Z</em>"
    page(pid, "French first names" if lang == "en" else "Prénoms français", h1,
         "♀ girls · ♂ boys · ⚥ both, with how to say each one" if lang == "en" else "♀ filles · ♂ garçons · ⚥ mixtes, avec leur prononciation",
         IXCSS + f'<div class="ixf"><iframe id="ix" src="{base}"></iframe></div>', "sapiopedia.com" + base,
         "Every name with its origin and a recording" if lang == "en" else "Chaque prénom avec son origine et un enregistrement", extra=IXJS.replace("{L}", L))
    add(id=pid, group="evergreen", slow=True, link=SITE + base, title=re.sub("<.*?>", "", h1),
        desc=("The full list of French first names, A to Z, marked for girls, boys or both. Open any name for its origin, its French pronunciation and a recording."
              if lang == "en" else "La liste complète des prénoms français de A à Z, pour filles, garçons ou mixtes. Chaque prénom a son origine, sa prononciation et un enregistrement."),
        board="French baby names", tags=("French baby names, French girl names, French boy names, Baby names, Baby name ideas, Unique baby names, Pregnancy, French aesthetic" if lang == "en"
                                         else "Prénoms, Idées de prénoms, Prénoms français, Prénom fille, Prénom garçon, Grossesse, Bébé"))

# ---------------------------------------------------------------- the original 07, 08 and 09a-c, rebuilt in the bigger style (same files, same rows)
page("07-room-planner-3d", "Free room planner", 'Plan your room, <em>then see it in 3D</em>', "Exact sizes, real furniture, your floor and wall colours.",
     '<div class="shot" id="shot" style="background:#fff;padding:10px"></div><div class="chips"><span>2D plan → 3D</span><span>Clearance check</span><span>Lamps & lighting</span></div>',
     "sapiopedia.com/en/tools/room-planner/", "Free, in your browser", extra=CAP3D.replace("{SRC}", "/en/tools/room-planner/?preset=living-room&view=3d"))
fsh = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fengshui_pin_template.html"), encoding="utf-8").read()
fsh = (fsh.replace("{{H1}}", "Is your bed in the <em>right place?</em>").replace("{{SUB}}", "Draw your room: every piece gets a feng shui verdict.").replace("{{TOOL}}", "/en/tools/fengshui/")
       .replace("{{URL}}", "sapiopedia.com/en/tools/fengshui/").replace("{{KICK}}", "Feng shui room planner").replace("{{VARIANT}}", "fs-en-1").replace('<div class="pin">', free("en") + '<div class="pin">', 1))
open(os.path.join(TMP, "08-feng-shui-bed.html"), "w", encoding="utf-8").write(fsh)
for pid, gift, h1, sub, target in [
        ("09a-scratch-mid", {"recipient": "Camille", "gift": "A weekend in Paris", "message": "Just us two, in May.", "sender": "Jules", "fx": ""}, "The prettiest way to send <em>a virtual gift</em>", "Hide it under a scratch-off card and send the link.", "0.25"),
        ("09b-scratch-confetti", {"recipient": "Nora", "gift": "Two tickets to the show", "message": "Saturday, front row!", "sender": "Ben", "fx": "confetti"}, "Scratch… <em>and confetti!</em>", "Choose the ending: confetti, hearts or snow.", "0.3"),
        ("09c-scratch-hearts", {"recipient": "Maya", "gift": "Dinner at our favourite place", "message": "Happy birthday, love.", "sender": "Eli", "fx": "hearts"}, "Perfect for <em>last-minute gifts</em>", "Ready in a minute. They scratch it on their phone.", "0.3")]:
    h = (PHONE.replace("{{H1}}", h1).replace("{{P}}", sub).replace("{{URL}}", "/en/tools/scratch-gift-card/#gift=" + b64(gift)).replace("{{TARGET}}", target)
         .replace("{{FOOT}}", "scratch-off gift card").replace("<body>", "<body>" + free("en"), 1))
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(h)
for p in PINS:
    if p.get("old") and p["id"][:2] in ("07", "08", "09"): p["slow"] = True
for p in PINS:
    if "/fengshui/" in p["link"] or "room-planner" in p["link"] or "planificateur" in p["link"]: p["group"] = "room"
for p in PINS:   # 01-06 and 10 come from tools/make_pins.py (_pins/), with the free badge added
    if p.get("old") and not os.path.exists(os.path.join(TMP, p["id"] + ".html")):
        h = open(os.path.join(ROOT, "_pins", p["id"] + ".html"), encoding="utf-8").read()
        open(os.path.join(TMP, p["id"] + ".html"), "w", encoding="utf-8").write(h.replace("<body>", "<body>" + free("en"), 1))

# ---------------------------------------------------------------- schedule from Tue 10 Nov 2026: weeks 1-2 three a day (2 room/feng shui), then five a day (3 room/feng shui).
# Room planner and feng shui pins are at least half of every day; party games and the Christmas scratch card come first among the rest before Christmas.
# Pins that don't fit stay in reserve (unscheduled).
start = datetime.date(2026, 11, 10)
def key(link): return re.sub(r"[&?]view=3d", "", link.split("#")[0])
queue = {g: [p for p in PINS if p["group"] == g] for g in ("room", "seasonal", "evergreen")}
for q in queue.values(): q.sort(key=lambda p: (0 if p.get("old") or p["id"].startswith(("sr-", "ix-", "s-en")) else 1, random.random()))
last, sched, day = {}, [], start
while queue["room"] and (day - start).days < 60:
    d = (day - start).days
    slots = (["room", "other", "room"], ["09:00:00", "13:00:00", "19:00:00"]) if d < 14 else \
            (["room", "other", "room", "other", "room"], ["08:00:00", "11:00:00", "14:00:00", "17:00:00", "20:00:00"])
    today = set(); nroom = nother = 0
    for grp, tm in zip(*slots):
        ok = lambda p: key(p["link"]) not in today and (key(p["link"]) not in last or (day - last[key(p["link"])]).days >= 7)
        if grp == "room": order = ["room"]
        else:
            if nother >= nroom: continue       # never more other pins than room pins on a day
            order = (["seasonal", "evergreen"] if day < datetime.date(2026, 12, 25) else ["evergreen"]) if d % 2 == 0 or day >= datetime.date(2026, 12, 25) else ["evergreen", "seasonal"]
        pick = next((p for g in order for p in queue[g] if ok(p)), None)
        if not pick: continue
        queue[pick["group"]].remove(pick); today.add(key(pick["link"])); last[key(pick["link"])] = day; nroom += grp == "room"; nother += grp != "room"
        sched.append((f"{day.isoformat()}T{tm}", pick))
    day += datetime.timedelta(1)
by = {}
for w, p in sched: by.setdefault(key(p["link"]), []).append(datetime.date.fromisoformat(w[:10]))
bad = [l for l, ds in by.items() if any((b - a).days < 7 for a, b in zip(sorted(ds), sorted(ds)[1:]))]
perday = {}
for w, p in sched: perday[w[:10]] = perday.get(w[:10], 0) + 1
late_seasonal = [p["id"] for w, p in sched if p["group"] == "seasonal" and w[:10] > "2026-12-24"]
nr = sum(1 for w, p in sched if p["group"] == "room")
print(f"room/feng shui {nr} of {len(sched)} ({nr * 100 // len(sched)}%); days below half: {[k for k in perday if sum(1 for w, p in sched if w[:10] == k and p['group'] == 'room') * 2 < perday[k]]}")
print(f"{len(PINS)} pins, {len(sched)} scheduled, {sched[0][0][:10]} to {sched[-1][0][:10]}; per day {sorted(set(perday.values()))}; spacing violations {len(bad)}; "
      f"seasonal after Christmas {late_seasonal}; reserve {len([p for q in queue.values() for p in q])}: {[p['id'] for q in queue.values() for p in q]}")

# ---------------------------------------------------------------- render
import concurrent.futures, shutil, sys as _s
_s.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from export_capture import capture  # noqa: E402
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def outfile(p): return os.path.join(DESK, p["file"]) if p.get("old") else os.path.join(OUTD, p["id"] + ".png")
def shoot(rel, out, w, h, s, budget):
    subprocess.run([CHROME, "--headless=new", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--hide-scrollbars", f"--force-device-scale-factor={s}",
                    f"--virtual-time-budget={budget}", f"--window-size={w},{h}", f"--screenshot={out}", f"http://127.0.0.1:8765/{rel}"],
                   capture_output=True, timeout=240)
def render(p):
    out = outfile(p)
    if p.get("export"):   # the planner's own PNG export under a title band that names the tool and carries the free badge
        raw = os.path.join(TMP, p["id"] + "-raw.png"); capture(p["export"], raw)
        w, h = (x // 2 for x in struct.unpack(">II", open(raw, "rb").read()[16:24]))
        lang = "fr" if "-fr-" in p["id"] else "en"; band_h = 120
        title = ({"en": "Feng shui <em>room planner</em>", "fr": "Planificateur <em>feng shui</em>"} if p["id"].startswith("x-fs-") else
                 {"en": "Room planner <em>in 2D and 3D</em>", "fr": "Plan de pièce <em>en 2D et 3D</em>"})[lang]
        open(os.path.join(TMP, p["id"] + "-badge.html"), "w", encoding="utf-8").write(
            '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400&family=Source+Sans+3:wght@700&display=swap">'
            f'<style>html,body{{margin:0;width:{w}px;height:{h + band_h}px;overflow:hidden;background:#F7E9EC;position:relative}}img{{display:block;width:{w}px;height:{h}px}}'
            f'.t{{height:{band_h}px;display:flex;align-items:center;padding:0 40px;font:400 50px/1 "Fraunces",Georgia,serif;letter-spacing:-.02em;color:#2A1F26}}.t em{{color:#A83A57}}'
            f'body .free{{top:{(band_h - 48) // 2}px}}</style></head>'
            f'<body>{free(lang)}<div class="t"><span>{title}</span></div><img src="{p["id"]}-raw.png" alt=""></body></html>')
        shoot(f"_pins_batch/{p['id']}-badge.html", out, w, h + band_h, 2, 6000); return p["id"]
    src = os.path.join(TMP, p["id"] + ".html")
    rel = f"_pins_batch/{p['id']}.html" if os.path.exists(src) else f"_pins/{p['id']}.html"
    w, h, s = p.get("win", (1000, 1500, 1))
    shoot(rel, out, w, h, s, 20000 if p.get("slow") else 6000)
    return p["id"]
only = os.environ.get("ONLY")
todo = [p for p in PINS if (not only or re.search(only, p["id"])) and (only or os.environ.get("RENDER") == "all" or not os.path.exists(outfile(p)))]
with concurrent.futures.ThreadPoolExecutor(4) as ex:
    for r in ex.map(render, todo): pass
print("rendered", len(todo))
# the baby pins have their own CSV and dates (16:00, a slot the main schedule never uses)
BABY_DATES = {"n3d-en-nursery": "2026-11-11T16:00:00", "bc-en-gender": "2026-11-13T16:00:00", "bc-en-pregnancy": "2026-11-15T16:00:00", "n3d-en-shared-nursery": "2026-11-17T16:00:00"}
with open(os.path.join(DESK, "pinterest-bulk-upload-baby.csv"), "w", encoding="utf-8", newline="") as fh:
    wr = csv.writer(fh); wr.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"])
    for p in sorted((p for p in PINS if p["group"] == "baby"), key=lambda p: BABY_DATES[p["id"]]):
        wr.writerow([p["title"][:100], f"{SITE}/pins/b1/{p['id']}.png", "Gift ideas", "", p["desc"], p["link"], BABY_DATES[p["id"]], p["tags"]])
if only or os.environ.get("DRY"): raise SystemExit

# ---------------------------------------------------------------- bulk-upload CSVs (Pinterest schedules up to ~30 days ahead: part 2 is uploaded later), overview, site copies
def media(p): return f"{SITE}/pins/{p['file']}" if p.get("old") else f"{SITE}/pins/b1/{p['id']}.png"
cut1 = (start + datetime.timedelta(28)).isoformat()
cols = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
dup = [t for t in {p["title"][:100] for w, p in sched} if sum(p["title"][:100] == t for w, p in sched) > 1]
if dup: raise SystemExit(f"Pinterest rejects pins that share a title: {dup}")
BOARD = "Gift ideas"   # the only board on the account; set to None to use each pin's own board once those exist
for name, rows in (("pinterest-bulk-upload.csv", [x for x in sched if x[0][:10] <= cut1]), ("pinterest-bulk-upload-part2.csv", [x for x in sched if x[0][:10] > cut1])):
    with open(os.path.join(DESK, name), "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(cols)
        for w, p in rows: wr.writerow([p["title"][:100], media(p), BOARD or p["board"], "", p["desc"], p["link"], w, p["tags"]])
    print(name, len(rows), "pins", rows[0][0][:10] if rows else "", "to", rows[-1][0][:10] if rows else "")
fig = "".join(f'<figure><img src="{os.path.relpath(outfile(p), DESK)}" loading="lazy" alt=""><figcaption><b>{w[:10]} · {w[11:16]}</b><span>{html.escape(p["title"])}</span><i>{html.escape(BOARD or p["board"])}</i>'
              f'<a href="{html.escape(p["link"])}">{html.escape(p["link"].replace("https://", ""))}</a></figcaption></figure>' for w, p in sched)
open(os.path.join(DESK, "overview.html"), "w", encoding="utf-8").write(
    f'<!doctype html><html><head><meta charset="utf-8"><title>Sapiopedia pins</title><style>body{{font-family:-apple-system,system-ui,sans-serif;background:#F7E9EC;color:#2A1F26;margin:0;padding:28px}}h1{{font-weight:600;margin:0 0 4px}}p{{margin:0 0 22px;color:#6E5A62}}'
    '.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}figure{margin:0;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)}'
    'img{width:100%;display:block;aspect-ratio:2/3;object-fit:contain;background:#f3eef0}figcaption{padding:10px 12px;display:grid;gap:3px;font-size:13px}figcaption b{color:#8E2F48}figcaption i{color:#6E5A62}figcaption a{color:#2E5F6E;word-break:break-all}</style></head>'
    f'<body><h1>Sapiopedia pins</h1><p>{len(sched)} pins, {sched[0][0][:10]} to {sched[-1][0][:10]}, in publishing order. Upload pinterest-bulk-upload.csv now and pinterest-bulk-upload-part2.csv after {cut1}.</p><div class="g">{fig}</div></body></html>')
os.makedirs(os.path.join(ROOT, "pins", "b1"), exist_ok=True)
for w, p in sched: shutil.copy(outfile(p), os.path.join(ROOT, "pins", p["file"]) if p.get("old") else os.path.join(ROOT, "pins", "b1", p["id"] + ".png"))
json.dump([{"when": w, **p} for w, p in sched], open(os.path.join(TMP, "schedule.json"), "w"), ensure_ascii=False, indent=0)
print("copied to pins/")
