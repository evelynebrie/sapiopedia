"""Dream dictionary: one page per language (index + every entry), built from data/dreams_{en,fr}.json.
Regenerate the JSON with:  python3 tools/parse_dreams.py
Layout: "option 6" (an old dream-book page). A version with engraved plates is kept in design/dream-entry-with-image.html."""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = {
    "en": dict(title="Dream Dictionary", book="Dream Dictionary", search="Search a dream: snake, teeth, falling…", search_label="Search the dictionary",
               index="Index of every word", index_sum="{n} dreams and {a} other words that lead to them", see="see", sit="What happens in the dream",
               feel="How you felt", q="Ask yourself", legend=("good sign", "mixed", "bad sign"), also="See also", src="Source",
               searched="Also searched as", share="Share this dream", top="Back to top", none="No dream matches “{q}”.",
               note="The tone runs from ●○○○○ (very negative omen) to ●●●●● (very positive).",
               sign=("Good sign", "Mixed sign", "Bad sign"), what=": what it means", today="What it often means today", all="All dreams, A to Z ↑",
               intro="Traditional dream meanings, rewritten in plain contemporary English from four public-domain dream books, with a modern reading of the feelings involved and questions for reflection.",
               books="The four books: G. H. Miller, <i>Ten Thousand Dreams Interpreted, or What's in a Dream</i> (1901); F. Fontaine, <i>The Golden Wheel Dream-Book and Fortune-Teller</i> (1862); A. H. Noe, <i>The Witches' Dream Book</i> (1885); and the anonymous <i>Interpretation of Dreams and Moles</i> (1805).", letters="Letters", preview="Your shareable image", download="Download PNG", close="Close", preparing="Preparing image…"),
    "fr": dict(title="Dictionnaire des rêves", book="Dictionnaire des rêves", search="Chercher un rêve : serpent, dents, chute…", search_label="Chercher dans le dictionnaire",
               index="Index de tous les mots", index_sum="{n} rêves et {a} autres mots qui y mènent", see="voir", sit="Ce qui se passe dans le rêve",
               feel="Ce que vous ressentiez", q="Questions à se poser", legend=("bon signe", "mitigé", "mauvais signe"), also="Voir aussi", src="Source",
               searched="Aussi cherché comme", share="Partager ce rêve", top="Haut de page", none="Aucun rêve ne correspond à « {q} ».",
               note="La tonalité va de ●○○○○ (présage très négatif) à ●●●●● (très positif).",
               sign=("Bon signe", "Signe mitigé", "Mauvais signe"), what=" : signification", today="Ce qu'il veut souvent dire aujourd'hui", all="Tous les rêves, de A à Z ↑",
               intro="Significations traditionnelles des rêves, réécrites en français contemporain à partir de quatre recueils du domaine public, avec une lecture moderne des émotions et des questions pour réfléchir.",
               books="Les quatre livres : G. H. Miller, <i>Ten Thousand Dreams Interpreted, or What's in a Dream</i> (1901) ; F. Fontaine, <i>The Golden Wheel Dream-Book and Fortune-Teller</i> (1862) ; A. H. Noe, <i>The Witches' Dream Book</i> (1885) ; et l'anonyme <i>Interpretation of Dreams and Moles</i> (1805).", letters="Lettres", preview="Votre image à partager", download="Télécharger le PNG", close="Fermer", preparing="Préparation de l'image…"),
}
THUMB = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><path id="dd-th" d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/></defs></svg>'

def e(s): return html.escape(s or "", quote=True)
def th(kind, label=""): return f'<svg class="th {kind}" viewBox="0 0 24 24"{f" role=\"img\" aria-label=\"{e(label)}\"" if label else " aria-hidden=\"true\""}><use href="#dd-th"/></svg>'
def dots(n): return '<span class="dots" aria-hidden="true">' + "●" * n + f'<s>{"●" * (5 - n)}</s></span>'

def ready_ids(kind):
    """Entries whose batch date has come (data/ready.json): they are indexable and in the sitemap; the rest are noindex, follow."""
    import datetime
    p = os.path.join(ROOT, "data", "ready.json")
    if not os.path.exists(p): return set()
    today = datetime.date.today().isoformat()
    return {i for b in json.load(open(p, encoding="utf-8"))["batches"] if b["from"] <= today for i in b.get(kind, [])}

def load(lang):
    return json.load(open(os.path.join(ROOT, "data", f"dreams_{lang}.json"), encoding="utf-8"))

def count(lang):
    return len(load(lang)["entries"])

def build(lang, layout, write, add_url, slug, alt_path):
    t, d = T[lang], load(lang)
    E = d["entries"]; ids = {x["id"]: x for x in E}
    letters = []
    for x in E:
        if not letters or letters[-1] != x["letter"]: letters.append(x["letter"])
    sign = dict(zip(("up", "mid", "down"), t["sign"]))
    import unicodedata
    R = ready_ids(f"dreams_{lang}")
    P = lambda i: f"/{lang}/{slug}/{i}/"
    def k(s): return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))
    # ---- synonyms index (words + aliases), every link goes to the entry's own page
    rows = [(x["word"], f'<a href="{P(x["id"])}" data-one="{e(x["one"])}">{e(x["word"])}</a>') for x in E]
    for a, targets in d["aliases"]:
        links = ", ".join(f'<a href="{P(i)}" data-one="{e(ids[i]["one"])}">{e(ids[i]["word"])}</a>' for i in targets if i in ids)
        if links: rows.append((a, f'<span class="al">{e(a)} → <i>{t["see"]}</i> {links}</span>'))
    rows.sort(key=lambda r: k(r[0]))
    by_letter = {}
    for w, h in rows:
        L = (k(w)[:1] or "#").upper(); L = L if L.isalpha() else "#"
        by_letter.setdefault(L, []).append(h)
    index_html = "".join(f'<div class="ixl"><h3>{L}</h3><ul>' + "".join(f"<li>{h}</li>" for h in items) + "</ul></div>" for L, items in sorted(by_letter.items()))
    overlay = f'''<div class="dd-ov" id="dd-ov" hidden role="dialog" aria-modal="true" aria-label="{e(t["preview"])}"><div class="dd-ovbox"><img alt=""><div class="dd-ovact"><button type="button" data-a="close">{t["close"]}</button><button type="button" data-a="dl" class="solid">{t["download"]}</button></div></div></div>'''
    cfg = json.dumps({"lang": lang, "book": t["book"], "sit": t["sit"], "feel": t["feel"], "q": t["q"], "also": t["also"], "src": t["src"], "searched": t["searched"], "preparing": t["preparing"], "share": "❦ " + t["share"], "url": f"sapiopedia.com/{lang}/{slug}/"}, ensure_ascii=False)
    scripts = f'<script>window.DD={cfg};</script><script src="/assets/dreams.js"></script>'
    # ---- one page per entry
    n_ready = 0
    for n, x in enumerate(E):
        prev = E[n - 1] if n else None; nxt = E[n + 1] if n + 1 < len(E) else None
        sits = "".join(f'<li class="{s[2]}">{th(s[2], sign[s[2]])}<span>{f"<i>{e(s[0])}:</i> " if s[0] else ""}{e(s[1])}</span></li>' for s in x["situations"])
        feels = "".join(f'<li>{f"<i>{e(f[0])}:</i> " if f[0] else ""}{e(f[1])}</li>' for f in x["feelings"])
        qs = "".join(f"<li>{e(q)}</li>" for q in x["questions"])
        rel = " · ".join(f'<a href="{P(r[1])}">{e(r[0])}</a>' if r[1] else e(r[0]) for r in x["related"])
        extra = x.get("extra")
        art = f'''<article class="dd-e" id="{x["id"]}" data-l="{x["letter"]}">
<div class="guide">{f'<a href="{P(prev["id"])}">← {e(prev["word"])}</a>' if prev else "<span></span>"}<a href="/{lang}/{slug}/#l-{x["letter"]}">{e(t["book"])} · {x["letter"]}</a>{f'<a href="{P(nxt["id"])}">{e(nxt["word"])} →</a>' if nxt else "<span></span>"}</div>
<header><span class="ini" aria-hidden="true">{e(x["word"][:1].upper())}</span><div><h1>{e(x["title"])}</h1><p class="pos">{e(", ".join([x["word"].lower()] + x["aliases"][:4]))} · {dots(x["tone"])} {e(x["tone_label"])}</p></div></header>
<p class="lead">{e(x["one"])}</p>
{f'<section><h3>{t["sit"]}</h3><ul class="sit">{sits}</ul></section>' if sits else ""}
{f'<section><h3>{t["feel"]}</h3><ul class="fl">{feels}</ul></section>' if feels else ""}
{f'<section><h3>{t["q"]}</h3><ul class="fl">{qs}</ul></section>' if qs else ""}
{f'<section><h3>{t["today"]}</h3><p class="extra">{e(extra)}</p></section>' if extra else ""}
{f'<p class="see">{t["also"]} {rel}</p>' if rel else ""}
<p class="refs">{t["src"]}: {e(x["refs"])}{f". {t['searched']}: {e(', '.join(x['aliases']))}." if x["aliases"] else ""}</p>
<div class="acts"><button type="button" class="share">❦ {t["share"]}</button><a class="top" href="/{lang}/{slug}/">{t["all"]}</a></div>
</article>'''
        body = f'<link rel="stylesheet" href="/assets/dreams.css">{THUMB}<div class="dd dd-one">{art}</div>{overlay}{scripts}'
        ok = x["id"] in R
        write(P(x["id"]) + "index.html", layout(lang, f'{x["title"]}{t["what"]}', x["one"][:155], body, P(x["id"]), alt_path, main_class="page dream", robots=None if ok else "noindex, follow"))
        if ok: add_url(P(x["id"])); n_ready += 1
    # ---- the dictionary page: A–Z list linking to every entry
    groups, cur = [], None
    for x in E:
        if x["letter"] != cur: groups.append([x["letter"], []]); cur = x["letter"]
        groups[-1][1].append(f'<li><a href="{P(x["id"])}"><b>{e(x["word"])}</b> <span class="dots" aria-hidden="true">{"●" * x["tone"]}<s>{"●" * (5 - x["tone"])}</s></span><span class="one">{e(x["one"])}</span></a></li>')
    book = "".join(f'<section class="dd-letter" id="l-{L}" aria-label="{L}"><h2 class="bigl">{L}</h2><ul class="dd-list">{"".join(a)}</ul></section>' for L, a in groups)
    az = "".join(f'<a href="#l-{L}">{L}</a>' for L in letters)
    intro = e(t["intro"])
    body = f'''<link rel="stylesheet" href="/assets/dreams.css">{THUMB}
<div class="dd" id="dd-top">
<p class="lead dd-intro">{intro}</p>
<p class="small dd-note">{t["note"]}</p>
<p class="small dd-note dd-books">{t["books"]}</p>
<div class="dd-bar">
  <div class="dd-search"><label class="sr" for="dd-q">{t["search_label"]}</label><input id="dd-q" type="search" autocomplete="off" placeholder="{e(t["search"])}"><ul id="dd-res" class="dd-res" role="listbox" hidden></ul><p id="dd-none" class="dd-none" hidden data-t="{e(t["none"])}"></p></div>
  <nav class="dd-az" aria-label="{t["letters"]}">{az}</nav>
</div>
<details class="dd-ix"><summary>{t["index"]} <span>({t["index_sum"].format(n=f"{len(E):,}".replace(",", " " if lang == "fr" else ","), a=f"{len(d['aliases']):,}".replace(",", " " if lang == "fr" else ","))})</span></summary><div class="ixc">{index_html}</div></details>
{book}
</div>
{overlay}{scripts}'''
    path = f"/{lang}/{slug}/"
    write(path + "index.html", layout(lang, t["title"], intro[:155], f'<h1>{t["title"]}</h1>' + body, path, alt_path, main_class="page dream"))
    add_url(path)
    print(f"  dreams {lang}: {len(E)} entry pages, {n_ready} indexable")
    return path
