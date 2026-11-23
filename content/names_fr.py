"""First-name books (Names > French names, Names > German names): an A–Z index and one page per name, in the old-book look of the dream dictionary.
French: data/names_fr_list.json + assets/names-fr.json (tools/extract_names.py, French Wiktionary).
German: data/names_de_list.json + assets/names-de.json (tools/extract_names_de.py, German, English and French Wiktionary).
Each book is a key of SETS ("fr", "de"); every function takes it (default "fr")."""
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
T_DE = {
    "en": dict(all="All names", f="Girls", m="Boys", n="Unisex", search="Search a German name: Emma, Lukas, Frieda…", search_label="Search the German names",
               ds="German names", ds_sub="First names used in German · {n} names · from the German, English and French Wiktionary",
               letters="Letters", none="No name matches “{q}”.", shown="{n} names shown", g={"f": "German girl's name", "m": "German boy's name", "n": "German unisex name: girls and boys", "u": "German name, gender not recorded"},
               hear="Hear it", playing="Playing…", pron="Pronunciation", first="First recorded", other="In other languages", comp="Compound names",
               close="Close", rec="Recording{acc}: {link}.", src="Sources: Wiktionary in German, English and French (CC BY-SA 4.0).",
               choose="Choose a list", legend="♀ girls · ♂ boys · ⚥ both", also="Also spelled"),
    "fr": dict(all="Tous les prénoms", f="Filles", m="Garçons", n="Mixtes", search="Chercher un prénom allemand : Emma, Lukas, Frieda…", search_label="Chercher un prénom allemand",
               ds="Prénoms allemands", ds_sub="Prénoms en usage en allemand · {n} prénoms · d'après le Wiktionnaire allemand, anglais et français",
               letters="Lettres", none="Aucun prénom ne correspond à « {q} ».", shown="{n} prénoms affichés", g={"f": "Prénom féminin allemand", "m": "Prénom masculin allemand", "n": "Prénom mixte allemand : filles et garçons", "u": "Prénom allemand, genre non indiqué"},
               hear="Écouter", playing="Lecture…", pron="Prononciation", first="Première mention", other="Dans d'autres langues", comp="Prénoms composés",
               close="Fermer", rec="Enregistrement{acc} : {link}.", src="Sources : Wiktionnaire allemand, anglais et français (CC BY-SA 4.0).",
               choose="Choisir une liste", legend="♀ filles · ♂ garçons · ⚥ mixtes", also="Autres graphies"),
}
SYM = {"f": "♀", "m": "♂", "n": "⚥", "u": ""}

def fold(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("æ", "ae"))
    return "".join(c for c in s if not unicodedata.combining(c))

def slug(s): return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-") or "x"

def body(lang, k="fr"):
    S = SETS[k]; t = S["T"][lang]
    rows = json.load(open(os.path.join(ROOT, "data", S["list"]), encoding="utf-8"))
    count = {k: sum(1 for r in rows if r[1] == k) for k in "fmn"}
    groups = {}
    ids, _ = card_slugs(k)
    base = S["base"][lang]
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
    if os.path.exists(os.path.join(ROOT, "data", SETS["de"]["list"])):
        n = len(json.load(open(os.path.join(ROOT, "data", SETS["de"]["list"]), encoding="utf-8")))
        PAGES.append({"section": "names", "wide": True,
            "en": ("german", "German first names", f"{n:,} German first names, for girls, boys or both, with pronunciation, recordings by native speakers and pet forms.", body("en", "de")),
            "fr": ("allemands", "Prénoms allemands", f"{n:,} prénoms allemands".replace(",", " ") + ", filles, garçons ou mixtes, avec la prononciation, des enregistrements et les diminutifs.", body("fr", "de"))})



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
               title="{n}: meaning, origin and pronunciation", bearsTxt="In France, {f}% of people with this name are women and {m}% are men.",
               nick="Short and pet forms", cf={"m": "Feminine form", "f": "Masculine form"}, vf="Related forms"),
    "fr": dict(glance="En bref", gender="Genre", origin="Origine", first="Première mention", pron="Prononciation", comp="Prénoms composés", also="Autres graphies",
               meaning="Origine et sens", bears="Qui le porte", where="Où on le donne surtout", world="Dans d'autres langues", lit="En littérature", about="À propos",
               gshort={"f": "Féminin", "m": "Masculin", "n": "Féminin et masculin (mixte)", "u": "Non indiqué"}, book="Prénoms français", all="Tous les prénoms français ↑",
               title="{n} : origine, signification et prononciation", bearsTxt="{f} % des personnes qui portent ce prénom en France sont des femmes, {m} % des hommes.",
               nick="Diminutifs et surnoms", cf={"m": "Forme féminine", "f": "Forme masculine"}, vf="Formes apparentées"),
}
CL_DE = {"en": dict(CL["en"], book="German Names", all="All German names ↑"), "fr": dict(CL["fr"], book="Prénoms allemands", all="Tous les prénoms allemands ↑")}
SETS = {
    "fr": dict(T=T, CL=CL, list="names_fr_list.json", cards="names-fr.json", ready="names", qlang="fr",
               base={"en": "/en/names/french/", "fr": "/fr/prenoms/francais/"}),
    "de": dict(T=T_DE, CL=CL_DE, list="names_de_list.json", cards="names-de.json", ready="names_de", qlang="de",
               base={"en": "/en/names/german/", "fr": "/fr/prenoms/allemands/"}),
}

def card_slugs(k="fr"):
    """One stable slug per card (main spelling), shared by the list and the pages."""
    rows = json.load(open(os.path.join(ROOT, "data", SETS[k]["list"]), encoding="utf-8"))
    used, ids, order = set(), {}, []
    for w, g, rec, main in rows:
        if main in ids: continue
        s = slug(main); k = 2
        while s in used: s = f"{slug(main)}-{k}"; k += 1
        used.add(s); ids[main] = s; order.append(main)
    return ids, order

def lead_line(lang, r, k="fr"):
    o, at = r.get("o"), (r.get("att") or "").replace("c. ", "").replace("c.", "").strip()
    if not o and not at: return ""
    if k == "de":
        if lang == "fr":
            kind = {"f": "Prénom féminin allemand", "m": "Prénom masculin allemand", "n": "Prénom mixte allemand", "u": "Prénom allemand"}[r["g"]]
            return kind + ((", issu de l'" if re.match(r"^[aeiouyhéèâ]", o, re.I) else ", issu du ") + o if o else "") + (f", attesté vers {at}" if at else "") + "."
        kind = {"f": "A German girl's name", "m": "A German boy's name", "n": "A German name for girls and boys", "u": "A German first name"}[r["g"]]
        return kind + (f" of {r['oe']} origin" if r.get("oe") else "") + (f", first recorded around {at}" if at else "") + "."
    if lang == "fr":
        kind = {"f": "Prénom féminin français", "m": "Prénom masculin français", "n": "Prénom mixte français", "u": "Prénom français"}[r["g"]]
        return kind + ((", issu de l'" if re.match(r"^[aeiouyhéèâ]", o, re.I) else ", issu du ") + o if o else "") + (f", attesté vers {at}" if at else "") + "."
    kind = {"f": "A French girl's name", "m": "A French boy's name", "n": "A French name for girls and boys", "u": "A French first name"}[r["g"]]
    return kind + (f" of {r['oe']} origin" if r.get("oe") else "") + (f", first recorded around {at}" if at else "") + "."

# ---------------------------------------------------------------- "Goes well with": middle names and siblings (data/names_pairs.json, tools/name_matching.py)
_PAIRS = None
def pairs():
    global _PAIRS
    if _PAIRS is None:
        p = os.path.join(ROOT, "data", "names_pairs.json")
        _PAIRS = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _PAIRS
_MID = None
def mid_pages():
    global _MID
    if _MID is None:
        p = os.path.join(ROOT, "data", "names_middle_pages.json")
        _MID = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _MID
GW = {"en": dict(h="Goes well with", mid="Middle names", sib="Brothers and sisters", more="40 middle names for {n} →", tool="Try your own combinations →",
                 tool_url="/en/tools/middle-name-finder/", mid_slug="middle-names"),
      "fr": dict(h="Va bien avec", mid="Deuxièmes prénoms", sib="Frères et sœurs", more="40 idées de deuxième prénom pour {n} →", tool="Essayer vos propres combinaisons →",
                 tool_url="/fr/outils/deuxieme-prenom/", mid_slug="deuxieme-prenom")}
def goes_with(lang, k, name):
    v = pairs().get(f"{k}:{name}")
    if not v: return ""
    c, E = GW[lang], html.escape
    link = lambda b, n, sl: f'<a href="{SETS[b]["base"][lang]}{sl}/">{E(n)}</a>'
    mids = " · ".join(link(b, n, sl) for b, n, sl, _ in v["m"])
    sibs = " · ".join(link(b, n, sl) for b, n, sl, _ in v["s"])
    base = SETS[k]["base"][lang]; slug = card_slugs(k)[0][name]
    more = f'<a href="{base}{slug}/{c["mid_slug"]}/">{E(c["more"].format(n=name))}</a> · ' if f"{k}:{name}" in mid_pages() else ""
    return (f'<section class="goes">{f"<h3>{c[chr(104)]}</h3>"}<p><b>{c["mid"]}</b> {mids}</p>' + (f'<p><b>{c["sib"]}</b> {sibs}</p>' if sibs else "")
            + f'<p class="small">{more}<a href="{c["tool_url"]}#n={E(name)}&amp;b={k}">{c["tool"]}</a></p></section>')

TWIN = {"en": {"fr": "Also a French name: {n} →", "de": "Also a German name: {n} →"}, "fr": {"fr": "Aussi un prénom français : {n} →", "de": "Aussi un prénom allemand : {n} →"}}

def card_html(lang, name, r, prev, nxt, base, ids, k="fr", twin=None):
    S = SETS[k]; t, c, E = S["T"][lang], S["CL"][lang], html.escape
    h3 = lambda x: f"<h3>{x}</h3>"
    rows = f"<tr><th>{c['gender']}</th><td>{c['gshort'][r['g']]}</td></tr>"
    if r.get("o"): rows += f"<tr><th>{c['origin']}</th><td>{E(r['o'].capitalize() if lang == 'fr' else r.get('oe', ''))}</td></tr>"
    if r.get("att"): rows += f"<tr><th>{c['first']}</th><td>{E(r['att'].replace('c. ', 'vers ' if lang == 'fr' else 'about '))}</td></tr>"
    if r.get("ipa"): rows += f"<tr><th>{c['pron']}</th><td>{E(r['ipa'])}</td></tr>"
    if r.get("v"): rows += f"<tr><th>{c['also']}</th><td>{E(', '.join(r['v']))}</td></tr>"
    if r.get("der"): rows += f"<tr><th>{c['comp']}</th><td>{E(', '.join(r['der']))}</td></tr>"
    if r.get("nick"): rows += f"<tr><th>{c['nick']}</th><td>{E(', '.join(r['nick']))}</td></tr>"
    if r.get("cf") and r["g"] in c["cf"]: rows += f"<tr><th>{c['cf'][r['g']]}</th><td>{E(', '.join(r['cf']))}</td></tr>"
    vf = [x for x in r.get("vf", []) if x not in r.get("v", [])]
    if vf: rows += f"<tr><th>{c['vf']}</th><td>{E(', '.join(vf))}</td></tr>"
    et = r.get("et") if lang == "fr" else r.get("ete")
    lead = lead_line(lang, r, k)
    sym = SYM[r["g"]]
    quote = ("« " + E(r["q"][0]) + " »" if S["qlang"] == "fr" else E(r["q"][0])) if r.get("q") else ""   # German quotations carry their own „…“
    acc = f" ({r['acc']})" if r.get("acc") else ""
    if r.get("file") and acc and lang == "fr": acc = " (" + ", ".join(FRC.get(x, x) for x in r["acc"].split(", ")) + ")"   # Germany, Berlin -> Allemagne, Berlin
    if not r.get("mp3"): credit = ""
    elif r.get("file"): credit = " " + t["rec"].format(acc=E(acc), link=f'<a href="{E(r["file"])}" rel="nofollow">Wikimedia Commons</a>')   # links the recording's Commons page
    else: credit = " " + E(t["rec"].format(by=r.get("by", ""), acc=acc))
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
           + goes_with(lang, k, name)
           + (f'<section>{h3(c["lit"])}<blockquote lang="{S["qlang"]}">{quote}<footer>{E(r["q"][1])}</footer></blockquote></section>' if r.get("q") else "")
           + f'<p class="cr">{t["src"]}' + credit + "</p>"
           + (f'<p class="back"><a href="{twin[0]}">{E(TWIN[lang][twin[1]].format(n=name))}</a></p>' if twin else "")
           + f'<p class="back"><a href="{base}">{c["all"]}</a></p>')
    return out, lead

def build_cards(lang, layout, write, add_url, k="fr"):
    from content.dreams import ready_ids
    S = SETS[k]
    if not os.path.exists(os.path.join(ROOT, "assets", S["cards"])): return
    D = json.load(open(os.path.join(ROOT, "assets", S["cards"]), encoding="utf-8"))
    ids, order = card_slugs(k)
    R = ready_ids(S["ready"])
    base = S["base"][lang]
    other = S["base"]["fr" if lang == "en" else "en"]
    t = S["T"][lang]; c = S["CL"][lang]; n_ready = 0
    k2 = "de" if k == "fr" else "fr"   # the same name in the other book gets a link
    ids2 = card_slugs(k2)[0] if os.path.exists(os.path.join(ROOT, "data", SETS[k2]["list"])) else {}
    audio = f'''<script>(function(){{var b=document.querySelector('.nf-box .hear');if(!b)return;var a=new Audio(b.dataset.src),H=b.textContent;
b.addEventListener('click',function(){{if(!a.paused){{a.pause();return;}}a.currentTime=0;var p=a.play();b.textContent='■ {t["playing"]}';b.setAttribute('aria-pressed','true');
a.onended=a.onpause=function(){{b.textContent=H;b.setAttribute('aria-pressed','false');}};if(p&&p.catch)p.catch(a.onended);}});}})();</script>'''
    for i, name in enumerate(order):
        r = D.get(name) or {"g": "u"}
        prev = order[i - 1] if i else None; nxt = order[i + 1] if i + 1 < len(order) else None
        inner, lead = card_html(lang, name, r, prev, nxt, base, ids, k, (f'{SETS[k2]["base"][lang]}{ids2[name]}/', k2) if name in ids2 else None)
        body = f'<link rel="stylesheet" href="/assets/dreams.css"><link rel="stylesheet" href="/assets/names.css"><div class="nf-ov nf-page"><article class="nf-box">{inner}</article></div>{audio}'
        path, alt = f"{base}{ids[name]}/", f"{other}{ids[name]}/"
        ok = name in R
        write(path + "index.html", layout(lang, c["title"].format(n=name), (lead or t["g"][r["g"]])[:155], body, path, alt, main_class="page names-one", robots=None if ok else "noindex, follow"))
        if ok: add_url(path); n_ready += 1
    print(f"  names {k} {lang}: {len(order)} card pages, {n_ready} indexable")


register()


# ---------------------------------------------------------------- middle-name pages for the best-known names (data/names_middle_pages.json)
WHY = {"en": {"pair": "families really pair them", "flow": "flows well", "origin": "same origin", "distinct": "different enough"},
       "fr": {"pair": "un vrai prénom composé", "flow": "rythme équilibré", "origin": "même origine", "distinct": "assez différent"}}
STY = {"en": {"short": "short", "classic": "classic", "rare": "rare", "vintage": "vintage", "nature": "nature", "mythological": "mythological",
              "biblical": "biblical", "international": "international", "modern": "modern"},
       "fr": {"short": "court", "classic": "classique", "rare": "rare", "vintage": "rétro", "nature": "nature", "mythological": "mythologique",
              "biblical": "biblique", "international": "international", "modern": "moderne"}}
MP = {"en": dict(title="Middle Names for {n}: 40 Names That Flow", desc="40 middle names that go with {n}, sorted into short, classic, rare and international, with the rule behind each one.",
                 groups={"short": "Short", "classic": "Classic", "rare": "Rare", "international": "International", "more": "More ideas"}, faq="Questions",
                 back="← {n}: meaning and pronunciation", tool="Check your own combination, with your surname →"),
      "fr": dict(title="Deuxième prénom pour {n} : 40 idées", desc="40 deuxièmes prénoms qui vont avec {n}, classés en courts, classiques, rares et internationaux, avec la raison de chaque choix.",
                 groups={"short": "Courts", "classic": "Classiques", "rare": "Rares", "international": "Internationaux", "more": "Autres idées"}, faq="Questions",
                 back="← {n} : origine et prononciation", tool="Tester votre propre combinaison, avec votre nom de famille →")}

def why(lang, codes):
    out = []
    for c in codes:
        out.append(f"{STY[lang].get(c[6:], c[6:])} " + ("style" if lang == "en" else "aussi") if c.startswith("style:") else WHY[lang].get(c, c))
    return " · ".join(out)

def middle_intro(lang, k, n, d):
    gender = {"en": {"f": "girl's", "m": "boy's", "n": "unisex"}, "fr": {"f": "féminin", "m": "masculin", "n": "mixte"}}[lang][d["g"]]
    book = {"fr": ("French", "français"), "de": ("German", "allemand")}[k]
    syl = d["syl"]; pr = d["pairs"]
    if lang == "en":
        t = (f"{n} is a {book[0]} {gender} name with {syl} syllable{'s' if syl > 1 else ''}" + (f", of {d['o']} origin" if d["o"] else "") + ". "
             f"Middle names flow best when they have a different number of syllables, do not rhyme with {n}, and do not start with the sound {n} ends on. "
             "Every name below was checked against those three rules and sorted into four groups.")
        if pr: t += f" Some already exist as real compound names, such as {n}-{pr[0]}" + (f" or {n}-{pr[1]}" if len(pr) > 1 else "") + ": families really pair them."
    else:
        t = (f"{n} est un prénom {gender} {book[1]} de {syl} syllabe{'s' if syl > 1 else ''}" + (f", d’origine {d['o']}" if d["o"] and False else "") + ". "
             f"Un deuxième prénom sonne mieux quand il n’a pas le même nombre de syllabes, ne rime pas avec {n} et ne commence pas par le son sur lequel {n} se termine. "
             "Chaque prénom ci-dessous a été vérifié selon ces trois règles, puis classé en quatre groupes.")
        if pr: t += f" Certains existent déjà comme vrais prénoms composés, comme {n}-{pr[0]}" + (f" ou {n}-{pr[1]}" if len(pr) > 1 else "") + " : des familles les associent vraiment."
    return t

def middle_faq(lang, n, d, sib):
    top = [x[1] for g in ("classic", "short", "international", "rare", "more") for x in d["groups"].get(g, [])][:3]
    sis = [x[1] for x in sib if x[0] and True][:0]
    girls = [x[1] for x in sib[:4]][:2]; boys = [x[1] for x in sib[4:]][:2]
    syl = d["syl"]; other = "1 or 3" if syl == 2 else "2" if syl in (1, 3) else "1 or 2"
    if lang == "en":
        return [(f"What is a good middle name for {n}?", f"Names with a different number of syllables flow best with {n}, for example {', '.join(top)}."),
                (f"What sibling names go with {n}?", f"For a sister, {' or '.join(girls)}; for a brother, {' or '.join(boys)}: the same style, but a different first letter and ending." if girls and boys else f"Names of the same style, with a different first letter and ending."),
                (f"Does {n} work as a middle name?", f"Yes. With {syl} syllable{'s' if syl > 1 else ''}, {n} sits best after a first name with {other} syllables.")]
    other = "1 ou 3" if syl == 2 else "2" if syl in (1, 3) else "1 ou 2"
    return [(f"Quel deuxième prénom choisir avec {n} ?", f"Les prénoms qui n’ont pas le même nombre de syllabes sonnent le mieux avec {n}, par exemple {', '.join(top)}."),
            (f"Quel prénom pour le frère ou la sœur de {n} ?", f"Pour une sœur, {' ou '.join(girls)} ; pour un frère, {' ou '.join(boys)} : le même style, mais une autre initiale et une autre finale." if girls and boys else "Un prénom du même style, avec une autre initiale et une autre finale."),
            (f"{n} fonctionne-t-il comme deuxième prénom ?", f"Oui. Avec {syl} syllabe{'s' if syl > 1 else ''}, {n} se place bien après un prénom de {other} syllabes.")]

def build_middle_pages(lang, layout, write, add_url):
    E = html.escape; c = MP[lang]; n_pages = 0
    for key, d in mid_pages().items():
        k, n = key.split(":", 1)
        base = SETS[k]["base"][lang]; other = SETS[k]["base"]["fr" if lang == "en" else "en"]
        mslug = GW[lang]["mid_slug"]; oslug = GW["fr" if lang == "en" else "en"]["mid_slug"]
        path = f"{base}{d['slug']}/{mslug}/"; alt = f"{other}{d['slug']}/{oslug}/"
        groups = "".join(f'<section><h3>{c["groups"][g]}</h3><ul class="grp">' + "".join(
            f'<li><a href="{SETS[b]["base"][lang]}{sl}/">{E(nm)}</a><span>{E(why(lang, w))}</span></li>' for b, nm, sl, w in items) + "</ul></section>"
            for g, items in d["groups"].items() if items)
        faq = middle_faq(lang, n, d, pairs().get(key, {}).get("s", []))
        ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False)
        title = c["title"].format(n=n)
        body = (f'<link rel="stylesheet" href="/assets/dreams.css"><link rel="stylesheet" href="/assets/names.css"><div class="nf-ov nf-page"><article class="nf-box mn">'
                f'<div class="guide"><a href="{base}{d["slug"]}/">{E(c["back"].format(n=n))}</a><span></span><a href="{GW[lang]["tool_url"]}#n={E(n)}&amp;b={k}">{"Finder →" if lang == "en" else "Outil →"}</a></div>'
                f'<h1>{E(title)}</h1><p class="lead" style="text-align:left">{E(middle_intro(lang, k, n, d))}</p>{groups}'
                f'<section class="faq"><h3>{c["faq"]}</h3>' + "".join(f"<h4>{E(q)}</h4><p>{E(a)}</p>" for q, a in faq) + "</section>"
                f'<p class="back"><a href="{GW[lang]["tool_url"]}#n={E(n)}&amp;b={k}">{E(c["tool"])}</a></p></article></div><script type="application/ld+json">{ld}</script>')
        write(path + "index.html", layout(lang, title, c["desc"].format(n=n), body, path, alt, main_class="page names-one"))
        add_url(path); n_pages += 1
    print(f"  middle-name pages {lang}: {n_pages}")
