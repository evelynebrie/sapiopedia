#!/usr/bin/env python3
"""
Sapiopedia site builder.

Run:  python3 build.py
It writes every HTML page (EN + FR), the sitemap and nothing else.
To add a page: add an entry to PAGES below (or to a content file later) and run again.

Layout: one shared template, one folder per section, one folder per page (index.html inside),
so every page has a clean URL like /en/tools/flour-cups-to-grams/
"""
import os, datetime, html, json

SITE = "https://sapiopedia.com"
# Visit statistics: GoatCounter (no cookies, no personal data). Dashboard: https://sapiopedia.goatcounter.com
ANALYTICS = '<script data-goatcounter="https://sapiopedia.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4904694456946317" crossorigin="anonymous"></script>'
TODAY = datetime.date.today().isoformat()
BIG_MARK = '<svg class="bigmark" aria-hidden="true" viewBox="22 4 160 202"><g style="mix-blend-mode:multiply"><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B9CFE0" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(-6,5)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#E9A9B8" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(6,-4)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B8405E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></g><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 1 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><circle cx="104" cy="176" r="12" fill="#B8405E"/><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 0 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><path d="M108 53 Q108 62 117 62 Q108 62 108 71 Q108 62 99 62 Q108 62 108 53Z" fill="#B8405E"/><path d="M128 44.5 Q128 48 131.5 48 Q128 48 128 51.5 Q128 48 124.5 48 Q128 48 128 44.5Z" fill="#B8405E"/><path d="M90 77 Q90 80 93 80 Q90 80 90 83 Q90 80 87 80 Q90 80 90 77Z" fill="#B8405E"/></svg>'
SMALL_MARK = '<svg aria-hidden="true" viewBox="22 4 160 202"><g style="mix-blend-mode:multiply"><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B9CFE0" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(-6,5)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#E9A9B8" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(6,-4)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B8405E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></g><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 1 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><circle cx="104" cy="176" r="12" fill="#B8405E"/><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 0 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><path d="M108 53 Q108 62 117 62 Q108 62 108 71 Q108 62 99 62 Q108 62 108 53Z" fill="#B8405E"/><path d="M128 44.5 Q128 48 131.5 48 Q128 48 128 51.5 Q128 48 124.5 48 Q128 48 128 44.5Z" fill="#B8405E"/><path d="M90 77 Q90 80 93 80 Q90 80 90 83 Q90 80 87 80 Q90 80 90 77Z" fill="#B8405E"/></svg>'
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" rx="40" fill="#F7E9EC"/><g transform="translate(100,100) scale(0.86) translate(-100,-105)"><g style="mix-blend-mode:multiply"><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B9CFE0" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(-6,5)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#E9A9B8" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" transform="translate(6,-4)"/><path d="M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144" fill="none" stroke="#B8405E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></g><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 1 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><circle cx="104" cy="176" r="12" fill="#B8405E"/><path d="M77.6 176 A26.400000000000002 7.199999999999999 0 0 0 130.4 176" fill="none" stroke="#B9CFE0" stroke-width="4" transform="rotate(-18 104 176)"/><path d="M108 53 Q108 62 117 62 Q108 62 108 71 Q108 62 99 62 Q108 62 108 53Z" fill="#B8405E"/><path d="M128 44.5 Q128 48 131.5 48 Q128 48 128 51.5 Q128 48 124.5 48 Q128 48 128 44.5Z" fill="#B8405E"/><path d="M90 77 Q90 80 93 80 Q90 80 90 83 Q90 80 87 80 Q90 80 90 77Z" fill="#B8405E"/></g></svg>'

SECTIONS = {
    "quizzes":  {"en": ("quizzes", "Quizzes", "Personality tests and quizzes you can share"),
                 "fr": ("quiz", "Quiz", "Tests de personnalité et quiz à partager")},
    "tools":    {"en": ("tools", "Tools", "Room and nursery planners in 2D and 3D, feng shui advice, and scratch-off cards for gifts, pregnancy announcements and gender reveals"),
                 "fr": ("outils", "Outils", "Planificateurs de pièce et de chambre de bébé en 2D et 3D, conseils feng shui et cartes à gratter pour un cadeau, une annonce de grossesse ou le sexe du bébé")},
    "names":    {"en": ("names", "Names", "French first names for girls, boys or both, with origins and pronunciation"),
                 "fr": ("prenoms", "Prénoms", "Prénoms français pour filles, garçons ou mixtes, avec origines et prononciation")},
    "games":    {"en": ("games", "Games", "Truth or dare and other party games, with questions to draw at random"),
                 "fr": ("jeux", "Jeux", "Action ou vérité et autres jeux de groupe, avec des questions à tirer au hasard")},
    "dreams":   {"en": ("dreams", "Dreams", "A dream dictionary from four old dream books, in plain English"),
                 "fr": ("reves", "Rêves", "Un dictionnaire des rêves tiré de quatre anciens recueils")},
}
LEGAL = {
    "en": {"about": "about", "privacy": "privacy", "contact": "contact"},
    "fr": {"about": "a-propos", "privacy": "confidentialite", "contact": "contact"},
}
UI = {
    "en": {"home": "Home", "tagline": "The species that can't stop asking questions.",
           "intro": "Sapiopedia is a growing collection of quizzes, room planners, a dream dictionary, French first names and party games. One question per page, a clear answer, and a result you can share.", "desc": {"quizzes": "Personality quizzes: your colour, your mental age, your season, the country that suits you…", "tools": "Plan a room or a nursery in 2D and 3D, check its feng shui, or send a scratch-off card: a gift, a pregnancy announcement, a gender reveal.", "names": "9,128 French first names for girls, boys or both, with origins, pronunciation and recordings.", "games": "Truth or dare, would you rather, never have I ever: questions for lively tables.", "dreams": "2,598 dreams from four old dream books, in plain words, with what your feelings may say."},
           "explore": "Categories", "related": "Related pages", "about": "About", "privacy": "Privacy", "contact": "Contact",
           "ad": "advertisement", "lang_other": "EN", "footer": "Made in Montréal",
           "kicker": "Tools and Answers Backed by Real Data",
           "h1": "For people who can't stop asking <em>questions</em>.",
           "cta": "What colour are you?", "cta_sub": "· 60 s",
           "mini": "New tool", "mini_t": "Feng Shui Room Planner",
           "note_k": "Method note", "note": "Every answer is built on real, open-source data, with sources when they matter.", "note_a": "How Sapiopedia is made",
           "counts": {"quizzes": "quizzes", "tools": "tools", "meanings": "entries", "names": "first names", "games": "games", "dreams": "dreams"}},
    "fr": {"home": "Accueil", "tagline": "L'espèce qui n'arrête pas de poser des questions.",
           "intro": "Sapiopedia est une collection grandissante de quiz, de planificateurs de pièce, d'un dictionnaire des rêves, de prénoms français et de jeux de groupe. Une question par page, une réponse claire, un résultat à partager.", "desc": {"quizzes": "Tests de personnalité : votre couleur, votre âge mental, votre saison, le pays qui vous ressemble…", "tools": "Aménagez une pièce ou la chambre de bébé en 2D et en 3D, vérifiez son feng shui ou envoyez une carte à gratter : un cadeau, une annonce de grossesse, le sexe du bébé.", "names": "9 128 prénoms français, filles, garçons ou mixtes, avec origines, prononciation et enregistrements.", "games": "Action ou vérité, tu préfères, je n'ai jamais : des questions pour les tablées animées.", "dreams": "2 598 rêves tirés de quatre anciens livres de rêves, en mots simples, avec ce que vos émotions peuvent dire."},
           "explore": "Catégories", "related": "Pages liées", "about": "À propos", "privacy": "Confidentialité", "contact": "Contact",
           "ad": "publicité", "lang_other": "FR", "footer": "Créé à Montréal",
           "kicker": "Outils et réponses appuyés sur de vraies données",
           "h1": "Pour les gens qui ne cessent de poser des <em>questions</em>.",
           "cta": "Quelle couleur êtes-vous ?", "cta_sub": "· 60 s",
           "mini": "Nouvel outil", "mini_t": "Planificateur de pièce feng shui",
           "note_k": "Note de méthode", "note": "Chaque réponse s'appuie sur de vraies données ouvertes, avec ses sources quand elles comptent.", "note_a": "Comment Sapiopedia est fait",
           "counts": {"quizzes": "quiz", "tools": "outils", "meanings": "entrées", "names": "prénoms", "games": "jeux", "dreams": "rêves"}},
}

def esc(s): return html.escape(s, quote=True)

def layout(lang, title, desc, body, path, alt_path, section=None, canonical=None, main_class="page", robots=None):
    u = UI[lang]
    nav = "".join(f'<a href="/{lang}/{SECTIONS[s][lang][0]}/">{SECTIONS[s][lang][1]}</a>' for s in SECTIONS)
    other = "fr" if lang == "en" else "en"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Sapiopedia</title>
<meta name="description" content="{esc(desc)}">{f'<meta name="robots" content="{robots}">' if robots else ""}
<link rel="canonical" href="{SITE}{canonical or path}">
<link rel="alternate" hreflang="{lang}" href="{SITE}{path}">
<link rel="alternate" hreflang="{other}" href="{SITE}{alt_path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{path if lang=='en' else alt_path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:type" content="website">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
{ANALYTICS}
{ADSENSE}
</head>
<body>
<header class="site"><div class="wrap">
  <a class="logo" href="/{lang}/">{SMALL_MARK}Sapiopedia</a>
  <nav class="main">{nav}<span class="lang"><b>{u['lang_other']}</b> / <a href="{alt_path}">{UI[other]['lang_other']}</a></span></nav>
</div></header>
<main class="{main_class}">
{body}
</main>
<footer class="site"><div class="wrap">
  <span>Sapiopedia</span><span>·</span><span>{u['footer']}</span><span>·</span><a href="/{lang}/{LEGAL[lang]['about']}/">{u['about']}</a><span>·</span><a href="/{lang}/{LEGAL[lang]['privacy']}/">{u['privacy']}</a><span>·</span><a href="/{lang}/{LEGAL[lang]['contact']}/">{u['contact']}</a>
</div></footer>
<script src="/assets/common.js"></script>
</body>
</html>
"""

def ad(lang): return ""   # empty ad placeholders hidden during the AdSense review; Auto ads places ads once approved

def write(path, content):
    full = os.path.join(os.path.dirname(__file__), path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

# ---------------------------------------------------------------- content
from sp import PAGES, quiz_page, article_page, tool_page  # noqa
import content  # registers every page (content/*.py)
from content import dreams  # one-page dream dictionary per language

# ---------------------------------------------------------------- build
urls = []
def add_url(p): urls.append(p)

for lang in ("en", "fr"):
    other = "fr" if lang == "en" else "en"
    u = UI[lang]
    # home
    ICON = {"quizzes": '<path d="M16 4c1.2 6.5 5.5 10.8 12 12-6.5 1.2-10.8 5.5-12 12-1.2-6.5-5.5-10.8-12-12 6.5-1.2 10.8-5.5 12-12z" stroke="#B8405E"/>',
            "tools": '<path d="M22 4a6 6 0 0 1 0 12 6 6 0 0 1-6-6V4zM16 10 6 28" stroke="#2E5F6E"/>',
            "meanings": '<path d="M6 26C8 14 16 6 28 5c-1 12-9 20-21 22M6 26l10-10" stroke="#6E4A78"/>',
            "names": '<path d="M16 5c7 0 12 4 12 9.5S23 24 16 24c-1.3 0-2.6-.1-3.8-.4L6 27l1.6-5.2C5.3 20 4 17.4 4 14.5 4 9 9 5 16 5z" stroke="#D9915F"/>',
            "games": '<path d="M9 5h14a2 2 0 0 1 2 2v18a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM16 12l3 4-3 4-3-4z" stroke="#6C8C66"/>',
            "dreams": '<path d="M20 4.5A11 11 0 1 0 27.5 22 9 9 0 0 1 20 4.5zM24 6.5l.8 1.7 1.7.8-1.7.8-.8 1.7-.8-1.7-1.7-.8 1.7-.8z" stroke="#8E2F48"/>'}
    rows = ""
    for i, s_ in enumerate(SECTIONS, 1):
        n = dreams.count(lang) if s_ == "dreams" else len(json.load(open(os.path.join(os.path.dirname(__file__), "data", "names_fr_list.json"), encoding="utf-8"))) if s_ == "names" else len([p for p in PAGES if p["section"] == s_])
        rows += (f'<a class="row" href="/{lang}/{SECTIONS[s_][lang][0]}/"><div class="g"><span class="n">{i:02d}</span>'
                 f'<span class="t">{SECTIONS[s_][lang][1]}</span><span class="d">{u["desc"][s_]}</span><span class="c">{n} {u["counts"][s_]}</span>'
                 f'<svg aria-hidden="true" width="32" height="32" viewBox="0 0 32 32" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICON[s_]}</svg></div><span class="rule"></span></a>')
    def url_of(en_slug):
        p = next(p for p in PAGES if p["en"][0] == en_slug)
        return f"/{lang}/{SECTIONS[p['section']][lang][0]}/{p[lang][0]}/"
    quiz_url = url_of("what-colour-is-your-personality"); fs_url = url_of("fengshui")
    body = f"""<div class="hero-wrap">{BIG_MARK}
<section class="hero">
  <div class="kicker">{u['kicker']}</div>
  <h1>{u['h1']}</h1>
  <div class="cta">
    <a class="btn" href="{quiz_url}">{u['cta']} <span>{u['cta_sub']}</span> <svg aria-hidden="true" width="18" height="12" viewBox="0 0 18 12"><path d="M1 6h15M11 1l5 5-5 5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    <a class="minitool" href="{fs_url}">
      <span class="kicker">{u['mini']}</span>
      <output>{u['mini_t']} →</output>
    </a>
  </div>
</section></div>
<section class="cats"><div class="head"><span class="kicker">{u['explore']}</span><i></i></div>{rows}</section>
<section class="note"><span class="kicker">{u['note_k']}</span><div><p>{u['note']}</p><a href="/{lang}/{LEGAL[lang]['about']}/">{u['note_a']}</a></div></section>
"""
    write(f"/{lang}/index.html", layout(lang, "Sapiopedia", u["intro"], body, f"/{lang}/", f"/{other}/", main_class="home"))
    add_url(f"/{lang}/")
    # sections
    for s, d in SECTIONS.items():
        if s == "dreams":
            dreams.build(lang, layout, write, add_url, d[lang][0], f"/{other}/{d[other][0]}/")
            continue
        slug, title, desc = d[lang]
        items = [p for p in PAGES if p["section"] == s]
        cards = "".join(f'<a href="/{lang}/{slug}/{p[lang][0]}/"><h3>{esc(p[lang][1])}</h3><p>{esc(p[lang][2])}</p></a>' for p in items)
        body = f"<h1>{title}</h1><p class=\"lead\">{desc}</p><div class=\"list\">{cards}</div>{ad(lang)}"
        write(f"/{lang}/{slug}/index.html", layout(lang, title, desc, body, f"/{lang}/{slug}/", f"/{other}/{d[other][0]}/"))
        add_url(f"/{lang}/{slug}/")
        for p in items:
            pslug, ptitle, pdesc, pbody = p[lang]
            rel = "".join(f'<li><a href="/{lang}/{slug}/{q[lang][0]}/">{esc(q[lang][1])}</a></li>' for q in items if q is not p)
            body = f"<h1>{esc(ptitle)}</h1><p class=\"lead\">{esc(pdesc)}</p>{pbody}{ad(lang)}<div class=\"related\"><h2>{u['related']}</h2><ul>{rel or '<li>—</li>'}</ul></div>"
            path = f"/{lang}/{slug}/{pslug}/"; alt = f"/{other}/{d[other][0]}/{p[other][0]}/"
            write(path + "index.html", layout(lang, ptitle, pdesc, body, path, alt, main_class=("page wide " + p.get("main_class", "")).strip() if p.get("wide") else "page"))
            add_url(path)
        if s == "names":
            from content import names_fr
            names_fr.build_cards(lang, layout, write, add_url)
    # legal pages
    legal_text = {
        "en": {"about": ("About Sapiopedia", "<p>Sapiopedia is an independent site that builds small, useful pages: quizzes, room planners, a dream dictionary, French first names and party games. Every tool states its method and its sources. The site is written and maintained by a university professor and data scientist based in Montréal.</p><p>Nothing here is medical, legal or financial advice.</p>"),
               "privacy": ("Privacy policy", "<p>Sapiopedia does not require an account and does not collect personal information. Quiz and calculator inputs are processed in your browser and are not sent to our servers.</p><p>We use privacy-friendly analytics to count visits. We may display advertising served by third parties (such as Google AdSense); these providers may use cookies to show relevant ads. You can opt out of personalised advertising in your Google Ads settings. Visitors in the EU/EEA and UK will be asked for consent before any advertising cookies are set.</p><p>Contact: see the contact page.</p>"),
               "contact": ("Contact", "<p>Questions, corrections or partnership ideas: <a href=\"mailto:hello@sapiopedia.com\">hello@sapiopedia.com</a>.</p>")},
        "fr": {"about": ("À propos de Sapiopedia", "<p>Sapiopedia est un site indépendant qui construit de petites pages utiles : quiz, planificateurs de pièce, dictionnaire des rêves, prénoms français et jeux de groupe. Chaque outil indique sa méthode et ses sources. Le site est écrit et tenu par une professeure d'université et scientifique des données basée à Montréal.</p><p>Rien ici ne constitue un avis médical, juridique ou financier.</p>"),
               "privacy": ("Politique de confidentialité", "<p>Sapiopedia ne demande aucun compte et ne collecte aucune information personnelle. Les réponses aux quiz et les valeurs des calculateurs sont traitées dans votre navigateur et ne sont pas envoyées à nos serveurs.</p><p>Nous utilisons des statistiques de visite respectueuses de la vie privée. Nous pouvons afficher des publicités servies par des tiers (par exemple Google AdSense) ; ces fournisseurs peuvent utiliser des témoins pour afficher des annonces pertinentes. Vous pouvez désactiver la publicité personnalisée dans vos paramètres Google. Les visiteurs de l'UE/EEE et du Royaume-Uni verront une demande de consentement avant tout témoin publicitaire.</p><p>Contact : voir la page contact.</p>"),
               "contact": ("Contact", "<p>Questions, corrections ou idées de partenariat : <a href=\"mailto:hello@sapiopedia.com\">hello@sapiopedia.com</a>.</p>")},
    }
    for key, slug in LEGAL[lang].items():
        title, body = legal_text[lang][key]
        path = f"/{lang}/{slug}/"; alt = f"/{other}/{LEGAL[other][key]}/"
        write(path + "index.html", layout(lang, title, title, f"<h1>{title}</h1>{body}", path, alt))
        add_url(path)

write("/assets/favicon.svg", FAVICON)
write("/ads.txt", "google.com, pub-4904694456946317, DIRECT, f08c47fec0942fa0\n")   # AdSense authorised seller

# root: language chooser with auto-redirect
write("/index.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sapiopedia</title><link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" hreflang="en" href="{SITE}/en/"><link rel="alternate" hreflang="fr" href="{SITE}/fr/"><link rel="alternate" hreflang="x-default" href="{SITE}/en/">
{ADSENSE}
<script>var l=(navigator.language||'en').slice(0,2);location.replace(l==='fr'?'/fr/':'/en/');</script>
</head><body><main><h1>Sapiopedia</h1><p><a href="/en/">English</a> · <a href="/fr/">Français</a></p></main></body></html>
""")
# short link /tools/fengshui/ -> language version
write("/tools/fengshui/index.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feng Shui Room Planner · Sapiopedia</title><link rel="canonical" href="{SITE}/en/tools/fengshui/">
<script>var l=(navigator.language||'en').slice(0,2);location.replace(l==='fr'?'/fr/outils/fengshui/':'/en/tools/fengshui/');</script>
</head><body><p><a href="/en/tools/fengshui/">Feng Shui Room Planner</a> · <a href="/fr/outils/fengshui/">Planificateur feng shui</a></p></body></html>
""")
write("/404.html", """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Not found · Sapiopedia</title><link rel="stylesheet" href="/assets/style.css"></head>
<body><main><h1>Page not found</h1><p><a href="/en/">English home</a> · <a href="/fr/">Accueil français</a></p></main></body></html>""")

# sitemap
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in urls: sm.append(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>")
sm.append("</urlset>")
write("/sitemap.xml", "\n".join(sm))
print(f"Built {len(urls)} pages.")
