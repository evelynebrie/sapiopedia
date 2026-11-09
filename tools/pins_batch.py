#!/usr/bin/env python3
"""Pinterest batch: ~84 pins over 4 weeks following the posting plan.

Weeks 1-2: 2 pins/day (1 seasonal + 1 evergreen); weeks 3-4: 4/day (2 + 2).
Rules checked before writing: same link never twice the same day, >= 7 days between pins of the same page.
Seasonal = Christmas framing of the scratch card and the party games. Evergreen = dreams, names, feng shui, room planner.
Writes _pins_batch/<id>.html (rendered by Chrome), then Desktop/Sapiopedia/Pinterest/batch-2026-11/ + the bulk CSV.
"""
import csv, datetime, json, os, random, re, subprocess, base64, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest")
OUTD = os.path.join(DESK, "batch-2026-11"); os.makedirs(OUTD, exist_ok=True)
TMP = os.path.join(ROOT, "_pins_batch"); os.makedirs(TMP, exist_ok=True)
GAMES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "games.json"), encoding="utf-8"))
src = open(os.path.join(ROOT, "tools", "make_pins.py"), encoding="utf-8").read()
exec(src[:src.index("def band(")])            # HEAD (styles), THUMB, E (EN dreams), N (names), IDX, esc
HEAD = HEAD.replace(".mid{flex:1;", ".main{flex:1;")
EF = {e["id"]: e for e in json.load(open(os.path.join(ROOT, "data", "dreams_fr.json")))["entries"]}
READY = json.load(open(os.path.join(ROOT, "data", "ready.json")))["batches"][0]
random.seed(2026)
SITE = "https://sapiopedia.com"

def band(url, label):
    return f'<div class="band"><img src="/assets/logo-horizontal.png" alt=""><div class="u"><b>{esc(url)}</b><span>{esc(label)}</span></div></div>'

FREE_CSS = '<style>.free{position:absolute;top:26px;right:40px;z-index:5;background:#8E2F48;color:#fff;font:700 21px "Source Sans 3",sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px;box-shadow:0 4px 12px -4px rgba(42,31,38,.4)}</style>'
def free(lang): return f'{FREE_CSS}<div class="free">{"Free · No sign-up" if lang == "en" else "Gratuit · Sans inscription"}</div>'
def page(pid, kick, title, sub, mid, url, label, extra=""):
    lang = "fr" if "/fr/" in url else "en"
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(
        HEAD + THUMB + free(lang) + f'<div class="pin"><div class="top"><div class="kick">{kick}</div><h1>{title}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div><div class="main">{mid}</div>{band(url, label)}</div>{extra}</body></html>')

PINS = []   # dicts: id, group (seasonal/evergreen), link, title, desc, board, tags, render (fast/slow)
def add(**k):
    d = k.get("desc", ""); fr = "/fr/" in k.get("link", "")
    if not re.search(r"no sign-up|sans inscription", d, re.I): d = d.rstrip() + (" Gratuit, sans inscription." if fr else " Free, no sign-up.")
    k["desc"] = d[:500]; PINS.append(k)

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
    pick = ([s for s in sits if s[2] == "up"][:2] + [s for s in sits if s[2] == "mid"][:1] + [s for s in sits if s[2] == "down"][:2])[:5]
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
        board="Christmas gift ideas", tags=("Christmas gift ideas, Virtual gift ideas, Digital gift, Scratch off card, Long distance Christmas, Last minute gifts, Gift card ideas, Christmas surprise" if lang == "en"
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

# ---------------------------------------------------------------- schedule: 28 days from Tue 10 Nov 2026
start = datetime.date(2026, 11, 10)
plan = [(start + datetime.timedelta(d), (["12:00:00"], ["19:00:00"]) if d < 14 else (["09:00:00", "16:00:00"], ["12:00:00", "20:00:00"])) for d in range(28)]
last = {}; queue = {"seasonal": [p for p in PINS if p["group"] == "seasonal"], "evergreen": [p for p in PINS if p["group"] == "evergreen"]}
for q in queue.values():                      # interleave so pins for the same page are far apart
    q.sort(key=lambda p: (0 if p.get("old") else 1, random.random()))
sched = []
for day, (s_times, e_times) in plan:
    today_links = set()
    for grp, times in (("seasonal", s_times), ("evergreen", e_times)):
        for tm in times:
            pick = next((p for p in queue[grp] if p["link"] not in today_links and (p["link"] not in last or (day - last[p["link"]]).days >= 7)), None)
            if not pick: continue
            queue[grp].remove(pick); today_links.add(pick["link"]); last[pick["link"]] = day
            sched.append((f"{day.isoformat()}T{tm}", pick))
sched.sort(key=lambda x: x[0])
# ---- checks
by_link = {}
for when, p in sched: by_link.setdefault(p["link"], []).append(datetime.date.fromisoformat(when[:10]))
bad = [(l, d) for l, d in by_link.items() if any((b - a).days < 7 for a, b in zip(sorted(d), sorted(d)[1:]))]
perday = {}
for when, p in sched: perday[when[:10]] = perday.get(when[:10], 0) + 1
print(f"{len(PINS)} pins prepared, {len(sched)} scheduled; per day: {sorted(set(perday.values()))}; spacing violations: {len(bad)}; unscheduled: {[p['id'] for q in queue.values() for p in q]}")
json.dump([{"when": w, **{k: v for k, v in p.items()}} for w, p in sched], open(os.path.join(TMP, "schedule.json"), "w"), ensure_ascii=False, indent=0)
