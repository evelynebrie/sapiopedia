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
    used, groups, ids = set(), {}, {}
    for w, g, rec, main in rows:
        if main not in ids:
            s = slug(main); k = 2
            while s in used: s = f"{slug(main)}-{k}"; k += 1
            used.add(s); ids[main] = s
        s = ids[main]
        L = fold(w)[:1].upper(); L = L if "A" <= L <= "Z" else "#"
        groups.setdefault(L, []).append(f'<li data-g="{g}"><a href="#{s}" data-n="{html.escape(main)}"{f' data-as="{html.escape(w)}"' if w != main else ""}>{html.escape(w)}</a>{f"<span class=s>{SYM[g]}</span>" if SYM[g] else ""}{"<span class=a title=♪>♪</span>" if rec else ""}</li>')
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
<div class="dd-ov nf-ov" id="nf-card" hidden role="dialog" aria-modal="true" aria-labelledby="nf-name"><div class="nf-box"></div></div>
<script>window.NF={json.dumps(cfg, ensure_ascii=False)};</script>
<script src="/assets/names.js"></script>'''

def register():
    n = len(json.load(open(os.path.join(ROOT, "data", "names_fr_list.json"), encoding="utf-8")))
    PAGES.append({"section": "names", "wide": True,
        "en": ("french", "French first names", f"{n:,} French first names, for girls, boys or both, with pronunciation and native-speaker recordings.", body("en")),
        "fr": ("francais", "Prénoms français", f"{n:,} prénoms français".replace(",", " ") + ", filles, garçons ou mixtes, avec la prononciation et des enregistrements.", body("fr"))})

register()
