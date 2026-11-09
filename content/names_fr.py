"""French first names index (Names > French names). Data: data/names_fr_list.json + assets/names-fr.json,
made by tools/extract_names.py from the French Wiktionary dump. Same old-book look as the dream dictionary."""
import html, json, os, re, unicodedata
from sp import PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = {
    "en": dict(all="All names", f="Girls", m="Boys", n="Unisex", search="Search a French name: Camille, Léa, Théo…", search_label="Search the French names",
               ds="French names", ds_sub="First names used in French · {n} names · from the French Wiktionary",
               letters="Letters", none="No name matches “{q}”.", shown="{n} names shown", g={"f": "French girl's name", "m": "French boy's name", "n": "French unisex name: girls and boys", "u": "French name, gender not recorded"},
               hear="Hear it", playing="Playing…", pron="Pronunciation", first="First recorded", other="In other languages", comp="Compound names",
               close="Close", rec="Recording: {by}{acc}, Lingua Libre / Wikimedia Commons (CC BY-SA 4.0).", src="Source: Wiktionnaire (CC BY-SA 4.0).",
               choose="Choose a list", legend="♀ girls · ♂ boys · ⚥ both", also="Also spelled"),
    "fr": dict(all="Tous les prénoms", f="Filles", m="Garçons", n="Mixtes", search="Chercher un prénom français : Camille, Léa, Théo…", search_label="Chercher un prénom français",
               ds="Prénoms français", ds_sub="Prénoms en usage en français · {n} prénoms · d'après le Wiktionnaire",
               letters="Lettres", none="Aucun prénom ne correspond à « {q} ».", shown="{n} prénoms affichés", g={"f": "Prénom féminin français", "m": "Prénom masculin français", "n": "Prénom mixte français : filles et garçons", "u": "Prénom français, genre non indiqué"},
               hear="Écouter", playing="Lecture…", pron="Prononciation", first="Première mention", other="Dans d'autres langues", comp="Prénoms composés",
               close="Fermer", rec="Enregistrement : {by}{acc}, Lingua Libre / Wikimedia Commons (CC BY-SA 4.0).", src="Source : Wiktionnaire (CC BY-SA 4.0).",
               choose="Choisir une liste", legend="♀ filles · ♂ garçons · ⚥ mixtes", also="Autres graphies"),
}
SYM = {"f": "♀", "m": "♂", "n": "⚥", "u": ""}

def fold(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("æ", "ae"))
    return "".join(c for c in s if not unicodedata.combining(c))

def slug(s): return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-") or "x"

def body(lang):
    t = T[lang]
    rows = json.load(open(os.path.join(ROOT, "data", "names_fr_list.json"), encoding="utf-8"))
    count = {k: sum(1 for r in rows if r[1] == k) for k in "fmn"}
    groups = {}
    ids, _ = card_slugs()
    base = "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/"
    for w, g, rec, main in rows:
        s = ids[main]
        L = fold(w)[:1].upper(); L = L if "A" <= L <= "Z" else "#"
        groups.setdefault(L, []).append(f'<li data-g="{g}"><a href="{base}{s}/" data-n="{html.escape(main)}"{f' data-as="{html.escape(w)}"' if w != main else ""}>{html.escape(w)}</a>{f"<span class=s>{SYM[g]}</span>" if SYM[g] else ""}{"<span class=a title=♪>♪</span>" if rec else ""}</li>')
    letters = sorted(groups, key=lambda L: (L == "#", L))
    seg = (f'<div class="nf-seg" role="group" aria-label="{t["choose"]}">'
           f'<button type="button" data-f="all" aria-pressed="true"><b>{t["all"]}</b><span>{len(rows):,}</span></button>'
           f'<button type="button" data-f="f" aria-pressed="false"><b>♀ {t["f"]}</b><span>{count["f"]:,}</span></button>'
           f'<button type="button" data-f="m" aria-pressed="false"><b>♂ {t["m"]}</b><span>{count["m"]:,}</span></button>'
           f'<button type="button" data-f="n" aria-pressed="false"><b>⚥ {t["n"]}</b><span>{count["n"]:,}</span></button></div>')
    if lang == "fr": seg = seg.replace(",", " ")
    lists = "".join(f'<section class="nf-l" id="l-{L}" data-l="{L}"><h2>{L}</h2><ul>{"".join(groups[L])}</ul></section>' for L in letters)
    cfg = {k: t[k] for k in ("hear", "playing", "pron", "first", "other", "comp", "close", "rec", "src", "none", "shown", "also")}
    cfg["g"] = t["g"]; cfg["lang"] = lang
    return f'''<link rel="stylesheet" href="/assets/dreams.css"><link rel="stylesheet" href="/assets/names.css">
<div class="nf" id="nf-top">
<p class="nf-ds"><b>{t["ds"]}</b><span>{t["ds_sub"].format(n=(f"{len(rows):,}".replace(",", " ") if lang == "fr" else f"{len(rows):,}"))}</span></p>
{seg}
<div class="nf-bar">
  <div class="dd-search"><label class="sr" for="nf-q">{t["search_label"]}</label><input id="nf-q" type="search" autocomplete="off" placeholder="{html.escape(t["search"])}"></div>
  <nav class="dd-az" aria-label="{t["letters"]}">{"".join(f'<a href="#l-{L}" data-l="{L}">{L}</a>' for L in letters)}</nav>
  <p class="nf-status"><span id="nf-shown" aria-live="polite"></span> · <span>{t["legend"]}</span></p>
</div>
<p id="nf-none" class="dd-none" hidden></p>
<div class="nf-list" id="nf-list" data-f="all">{lists}</div>
</div>
<script>window.NF={json.dumps(cfg, ensure_ascii=False)};</script>
<script src="/assets/names.js"></script>'''

def register():
    n = len(json.load(open(os.path.join(ROOT, "data", "names_fr_list.json"), encoding="utf-8")))
    PAGES.append({"section": "names", "wide": True,
        "en": ("french", "French first names", f"{n:,} French first names, for girls, boys or both, with pronunciation and native-speaker recordings.", body("en")),
        "fr": ("francais", "Prénoms français", f"{n:,} prénoms français".replace(",", " ") + ", filles, garçons ou mixtes, avec la prononciation et des enregistrements.", body("fr"))})



# ---------------------------------------------------------------- one page per name card
FRL = {"English": "anglais", "Spanish": "espagnol", "Italian": "italien", "German": "allemand", "Portuguese": "portugais", "Dutch": "néerlandais", "Polish": "polonais",
       "Russian": "russe", "Greek": "grec", "Latin": "latin", "Arabic": "arabe", "Hebrew": "hébreu", "Chinese": "chinois", "Japanese": "japonais", "Czech": "tchèque",
       "Hungarian": "hongrois", "Swedish": "suédois", "Danish": "danois", "Norwegian": "norvégien", "Finnish": "finnois", "Catalan": "catalan", "Breton": "breton",
       "Basque": "basque", "Corsican": "corse", "Occitan": "occitan", "Romanian": "roumain", "Turkish": "turc", "Lithuanian": "lituanien", "Latvian": "letton",
       "Irish": "irlandais", "Welsh": "gallois", "Ukrainian": "ukrainien", "Slovak": "slovaque", "Croatian": "croate", "Slovenian": "slovène"}
FRC = {"Great Britain": "Royaume-Uni", "Ireland": "Irlande", "United States": "États-Unis", "Italy": "Italie", "Malta": "Malte", "Spain": "Espagne", "Belgium": "Belgique",
       "Netherlands": "Pays-Bas", "East Frisia": "Frise orientale", "Germany": "Allemagne", "Austria": "Autriche", "Switzerland": "Suisse", "Iceland": "Islande",
       "Denmark": "Danemark", "Norway": "Norvège", "Sweden": "Suède", "Finland": "Finlande", "Estonia": "Estonie", "Latvia": "Lettonie", "Lithuania": "Lituanie",
       "Poland": "Pologne", "Czech Republic": "Tchéquie", "Slovakia": "Slovaquie", "Hungary": "Hongrie", "Romania": "Roumanie", "Bulgaria": "Bulgarie", "Croatia": "Croatie",
       "Serbia": "Serbie", "Slovenia": "Slovénie", "Greece": "Grèce", "Russia": "Russie", "Turkey": "Turquie", "Israel": "Israël", "China": "Chine", "Japan": "Japon",
       "Korea": "Corée", "Vietnam": "Viêt Nam", "Arabia/Persia": "Monde arabe et Iran", "India/Sri Lanka": "Inde et Sri Lanka"}
CL = {
    "en": dict(glance="At a glance", gender="Gender", origin="Origin", first="First recorded", pron="Pronunciation", comp="Compound names", also="Also spelled",
               meaning="Origin and meaning", bears="Who bears it", where="Where it is mostly given", world="Around the world", lit="In literature", about="About",
               gshort={"f": "Feminine", "m": "Masculine", "n": "Feminine and masculine (unisex)", "u": "Not recorded"}, book="French Names", all="All French names ↑",
               title="{n}: meaning, origin and pronunciation", bearsTxt="In France, {f}% of people with this name are women and {m}% are men."),
    "fr": dict(glance="En bref", gender="Genre", origin="Origine", first="Première mention", pron="Prononciation", comp="Prénoms composés", also="Autres graphies",
               meaning="Origine et sens", bears="Qui le porte", where="Où on le donne surtout", world="Dans d'autres langues", lit="En littérature", about="À propos",
               gshort={"f": "Féminin", "m": "Masculin", "n": "Féminin et masculin (mixte)", "u": "Non indiqué"}, book="Prénoms français", all="Tous les prénoms français ↑",
               title="{n} : origine, signification et prononciation", bearsTxt="{f} % des personnes qui portent ce prénom en France sont des femmes, {m} % des hommes."),
}

def card_slugs():
    """One stable slug per card (main spelling), shared by the list and the pages."""
    rows = json.load(open(os.path.join(ROOT, "data", "names_fr_list.json"), encoding="utf-8"))
    used, ids, order = set(), {}, []
    for w, g, rec, main in rows:
        if main in ids: continue
        s = slug(main); k = 2
        while s in used: s = f"{slug(main)}-{k}"; k += 1
        used.add(s); ids[main] = s; order.append(main)
    return ids, order

def lead_line(lang, r):
    o, at = r.get("o"), (r.get("att") or "").replace("c. ", "").replace("c.", "").strip()
    if not o and not at: return ""
    if lang == "fr":
        kind = {"f": "Prénom féminin français", "m": "Prénom masculin français", "n": "Prénom mixte français", "u": "Prénom français"}[r["g"]]
        return kind + ((", issu de l'" if re.match(r"^[aeiouyhéèâ]", o, re.I) else ", issu du ") + o if o else "") + (f", attesté vers {at}" if at else "") + "."
    kind = {"f": "A French girl's name", "m": "A French boy's name", "n": "A French name for girls and boys", "u": "A French first name"}[r["g"]]
    return kind + (f" of {r['oe']} origin" if r.get("oe") else "") + (f", first recorded around {at}" if at else "") + "."

def card_html(lang, name, r, prev, nxt, base, ids):
    t, c, E = T[lang], CL[lang], html.escape
    h3 = lambda x: f"<h3>{x}</h3>"
    rows = f"<tr><th>{c['gender']}</th><td>{c['gshort'][r['g']]}</td></tr>"
    if r.get("o"): rows += f"<tr><th>{c['origin']}</th><td>{E(r['o'].capitalize() if lang == 'fr' else r.get('oe', ''))}</td></tr>"
    if r.get("att"): rows += f"<tr><th>{c['first']}</th><td>{E(r['att'].replace('c. ', 'vers ' if lang == 'fr' else 'about '))}</td></tr>"
    if r.get("ipa"): rows += f"<tr><th>{c['pron']}</th><td>{E(r['ipa'])}</td></tr>"
    if r.get("v"): rows += f"<tr><th>{c['also']}</th><td>{E(', '.join(r['v']))}</td></tr>"
    if r.get("der"): rows += f"<tr><th>{c['comp']}</th><td>{E(', '.join(r['der']))}</td></tr>"
    et = r.get("et") if lang == "fr" else r.get("ete")
    lead = lead_line(lang, r)
    sym = SYM[r["g"]]
    out = (f'<div class="guide">{f"<a href=\"{base}{ids[prev]}/\">← {E(prev)}</a>" if prev else "<span></span>"}<a href="{base}">{c["book"]} · {E(name[0].upper())}</a>{f"<a href=\"{base}{ids[nxt]}/\">{E(nxt)} →</a>" if nxt else "<span></span>"}</div>'
           f'<div class="hd"><span class="ini" aria-hidden="true">{E(name[0])}</span><div><h1>{E(name)}</h1><p class="gl">'
           + (f'<span class="ipa">{E(r["ipa"])}</span>' if r.get("ipa") else "") + (f'<b class="{r["g"]}">{sym}</b>' if sym else "") + f'<span>{E(t["g"][r["g"]])}</span>'
           + (f'<button type="button" class="hear" aria-pressed="false" data-src="{E(r["mp3"])}">▶ {t["hear"]}</button>' if r.get("mp3") else "") + "</p></div></div>"
           + (f'<p class="lead">{E(lead)}</p>' if lead else "")
           + f'<section>{h3(c["glance"])}<table class="facts">{rows}</table></section>'
           + (f'<section>{h3(c["meaning"])}<p class="body">{E(et)}</p></section>' if et else "")
           + (f'<section class="bearers">{h3(c["bears"])}<div class="split"><span class="f" style="width:{r["pf"]}%">♀ {r["pf"]}{" %" if lang == "fr" else "%"}</span><span class="m" style="width:{100 - r["pf"]}%">♂ {100 - r["pf"]}{" %" if lang == "fr" else "%"}</span></div><p>{E(c["bearsTxt"].format(f=r["pf"], m=100 - r["pf"]))}</p></section>' if r.get("pf") is not None else "")
           + (f'<section>{h3(c["where"])}<ul class="places">' + "".join(f"<li>{E(FRC.get(x, x) if lang == 'fr' else x)}</li>" for x in r["c"]) + "</ul></section>" if r.get("c") else "")
           + (f'<section>{h3(c["world"])}<ul class="world">' + "".join(f'<li><span class="lg">{E(FRL.get(l, l) if lang == "fr" else l)}</span><span class="dl"></span><span class="fm">{E(", ".join(ws))}</span></li>' for l, ws in r["tr"].items()) + "</ul></section>" if r.get("tr") else "")
           + (f'<section>{h3(c["lit"])}<blockquote lang="fr">« {E(r["q"][0])} »<footer>{E(r["q"][1])}</footer></blockquote></section>' if r.get("q") else "")
           + f'<p class="cr">{t["src"]}' + (" " + E(t["rec"].format(by=r.get("by", ""), acc=f" ({r['acc']})" if r.get("acc") else "")) if r.get("mp3") else "") + "</p>"
           + f'<p class="back"><a href="{base}">{c["all"]}</a></p>')
    return out, lead

def build_cards(lang, layout, write, add_url):
    from content.dreams import ready_ids
    D = json.load(open(os.path.join(ROOT, "assets", "names-fr.json"), encoding="utf-8"))
    ids, order = card_slugs()
    R = ready_ids("names")
    base = "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/"
    other = "/fr/prenoms/francais/" if lang == "en" else "/en/names/french/"
    t = T[lang]; c = CL[lang]; n_ready = 0
    audio = f'''<script>(function(){{var b=document.querySelector('.nf-box .hear');if(!b)return;var a=new Audio(b.dataset.src),H=b.textContent;
b.addEventListener('click',function(){{if(!a.paused){{a.pause();return;}}a.currentTime=0;var p=a.play();b.textContent='■ {t["playing"]}';b.setAttribute('aria-pressed','true');
a.onended=a.onpause=function(){{b.textContent=H;b.setAttribute('aria-pressed','false');}};if(p&&p.catch)p.catch(a.onended);}});}})();</script>'''
    for i, name in enumerate(order):
        r = D.get(name) or {"g": "u"}
        prev = order[i - 1] if i else None; nxt = order[i + 1] if i + 1 < len(order) else None
        inner, lead = card_html(lang, name, r, prev, nxt, base, ids)
        body = f'<link rel="stylesheet" href="/assets/dreams.css"><link rel="stylesheet" href="/assets/names.css"><div class="nf-ov nf-page"><article class="nf-box">{inner}</article></div>{audio}'
        path, alt = f"{base}{ids[name]}/", f"{other}{ids[name]}/"
        ok = name in R
        write(path + "index.html", layout(lang, c["title"].format(n=name), (lead or t["g"][r["g"]])[:155], body, path, alt, main_class="page names-one", robots=None if ok else "noindex, follow"))
        if ok: add_url(path); n_ready += 1
    print(f"  names {lang}: {len(order)} card pages, {n_ready} indexable")


register()
