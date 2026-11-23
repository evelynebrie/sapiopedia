"""Middle-name and sibling finder (Names section). Logic: /assets/name-finder.js on /assets/names-match.json (tools/name_matching.py).
Results link to the name pages; the shortlist lives in the link after #."""
import html, json
from sp import PAGES

T = {
 "en": dict(title="Middle Name & Sibling Name Finder", desc="Find a middle name that flows, or a brother or sister name that matches: French and German names, with the reason for each idea. Free, no sign-up.",
    name="First name", name_ph="Alice, Léo, Frieda…", mode_m="Middle name", mode_s="Brother or sister", sur="Surname (optional, checks the initials)",
    style="Style", any="Any", len="Length", l1="1 syllable", l2="2 syllables", l3="3 or more", origin="Origin", intl="Works in French and English",
    book="Names from", same="the same list", both="French and German lists",
    how=("How it works", "<p>Each suggestion is scored on simple rules. A middle name flows better with a different number of syllables, when it does not rhyme with the first name and does not start with the sound the first name ends on. Names that families really combine (Marie-Alice, Jean-Paul…) get a bonus. For brothers and sisters, the finder looks for the same style and era, but a different first letter and ending, so Léo and Théo are never suggested together. French eras come from the official INSEE birth statistics (1900–2021).</p><p>Tap ♡ to keep a name: your shortlist is saved in the link, ready to share.</p>"),
    js=dict(none="“{q}” is not in our lists yet. Try another spelling.", empty="No name matches these filters.", sisters="Sisters", brothers="Brothers",
            save="Keep this name", list="Your shortlist:", share="Share", copied="Link copied", shareTitle="My name shortlist", style="{s} style",
            why={"pair": "families really pair them", "flow": "flows well", "origin": "same origin", "distinct": "different enough", "init": "initials OK"},
            styles={"short": "short", "classic": "classic", "rare": "rare", "vintage": "vintage", "nature": "nature", "mythological": "mythological", "biblical": "biblical", "international": "international", "modern": "modern"})),
 "fr": dict(title="Trouver un deuxième prénom ou un prénom de frère ou sœur", desc="Trouvez un deuxième prénom qui sonne bien, ou un prénom de frère ou de sœur assorti : prénoms français et allemands, avec la raison de chaque idée. Gratuit, sans inscription.",
    name="Prénom", name_ph="Alice, Léo, Frieda…", mode_m="Deuxième prénom", mode_s="Frère ou sœur", sur="Nom de famille (facultatif, vérifie les initiales)",
    style="Style", any="Tous", len="Longueur", l1="1 syllabe", l2="2 syllabes", l3="3 ou plus", origin="Origine", intl="Fonctionne en français et en anglais",
    book="Prénoms", same="de la même liste", both="français et allemands",
    how=("Comment ça marche", "<p>Chaque suggestion est notée selon des règles simples. Un deuxième prénom sonne mieux s’il n’a pas le même nombre de syllabes, ne rime pas avec le premier et ne commence pas par le son sur lequel le premier se termine. Les prénoms que les familles associent vraiment (Marie-Alice, Jean-Paul…) reçoivent un bonus. Pour un frère ou une sœur, l’outil cherche le même style et la même époque, mais une autre initiale et une autre finale : Léo et Théo ne sont jamais proposés ensemble. Les époques des prénoms français viennent des statistiques officielles de l’INSEE (1900-2021).</p><p>Touchez ♡ pour garder un prénom : votre sélection est enregistrée dans le lien, prête à partager.</p>"),
    js=dict(none="« {q} » n’est pas encore dans nos listes. Essayez une autre orthographe.", empty="Aucun prénom ne correspond à ces filtres.", sisters="Sœurs", brothers="Frères",
            save="Garder ce prénom", list="Votre sélection :", share="Partager", copied="Lien copié", shareTitle="Ma sélection de prénoms", style="style {s}",
            why={"pair": "un vrai prénom composé", "flow": "rythme équilibré", "origin": "même origine", "distinct": "assez différent", "init": "initiales OK"},
            styles={"short": "court", "classic": "classique", "rare": "rare", "vintage": "rétro", "nature": "nature", "mythological": "mythologique", "biblical": "biblique", "international": "international", "modern": "moderne"})),
}
STY = ["short", "classic", "vintage", "modern", "nature", "mythological", "biblical", "rare"]

def body(lang):
    t = T[lang]; e = html.escape; js = dict(t["js"]); js["lang"] = lang
    js["base"] = {"fr": "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/", "de": "/en/names/german/" if lang == "en" else "/fr/prenoms/allemands/"}
    sty = "".join(f'<option value="{s}">{e(t["js"]["styles"][s])}</option>' for s in STY)
    return f'''<link rel="stylesheet" href="/assets/name-finder.css"><div class="nm">
<div class="nm-form">
 <label class="nm-big">{t["name"]}<input id="nm-n" list="nm-names" autocomplete="off" placeholder="{e(t["name_ph"])}"></label><datalist id="nm-names"></datalist>
 <div class="nm-mode" role="radiogroup"><label><input type="radio" name="nm-mode" value="middle" checked> {t["mode_m"]}</label><label><input type="radio" name="nm-mode" value="sibling"> {t["mode_s"]}</label></div>
 <label>{t["sur"]}<input id="nm-s" autocomplete="off"></label>
 <div class="nm-filters">
  <label>{t["style"]}<select id="nm-style"><option value="">{t["any"]}</option>{sty}</select></label>
  <label>{t["len"]}<select id="nm-len"><option value="">{t["any"]}</option><option value="1">{t["l1"]}</option><option value="2">{t["l2"]}</option><option value="3">{t["l3"]}</option></select></label>
  <label>{t["origin"]}<select id="nm-origin"><option value="">{t["any"]}</option></select></label>
  <label>{t["book"]}<select id="nm-book"><option value="same">{t["same"]}</option><option value="both">{t["both"]}</option></select></label>
  <label class="nm-check"><input type="checkbox" id="nm-intl"> {t["intl"]}</label>
 </div>
</div>
<div id="nm-list" class="nm-list"></div>
<div id="nm-out" class="nm-out"></div>
<section class="nm-how"><h2>{t["how"][0]}</h2>{t["how"][1]}</section>
</div>
<script>window.NM={json.dumps(js, ensure_ascii=False)};</script><script src="/assets/name-finder.js"></script>'''

PAGES.append({"section": "names", "wide": True,
    "en": ("middle-name-finder", T["en"]["title"], T["en"]["desc"], body("en")),
    "fr": ("deuxieme-prenom", T["fr"]["title"], T["fr"]["desc"], body("fr"))})
