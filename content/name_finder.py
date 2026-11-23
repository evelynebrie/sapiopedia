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

PG = {  # mode: (slug en, slug fr, title en, title fr, meta en, meta fr, name label en/fr, how en/fr)
 "middle": ("middle-name-finder", "deuxieme-prenom", "Middle Name Finder", "Trouver un deuxième prénom",
            "Middle name ideas that go with your child's first name, with the reason for each one.",
            "Des idées de deuxième prénom qui vont avec le prénom de votre enfant, avec la raison de chaque choix.",
            ("Your child's first name", "Le premier prénom"),
            ("<p>A middle name flows better with a different number of syllables, when it does not rhyme with the first name and does not start with the sound the first name ends on. Names that families really combine (Marie-Alice, Jean-Paul…) get a bonus. Add your surname to check the initials and the rhythm of the full name.</p><p>Tap ♡ to keep a name: your shortlist is saved in the link, ready to share.</p>",
             "<p>Un deuxième prénom sonne mieux s’il n’a pas le même nombre de syllabes, ne rime pas avec le premier et ne commence pas par le son sur lequel le premier se termine. Les prénoms que les familles associent vraiment (Marie-Alice, Jean-Paul…) reçoivent un bonus. Ajoutez votre nom de famille pour vérifier les initiales et le rythme du nom complet.</p><p>Touchez ♡ pour garder un prénom : votre sélection est enregistrée dans le lien, prête à partager.</p>")),
 "sibling": ("sibling-name-finder", "prenom-frere-soeur", "Sibling Name Finder", "Trouver un prénom de frère ou sœur",
            "Brother and sister name ideas that match your first child's name, in the same style and era.",
            "Des idées de prénoms de frère ou de sœur assortis au prénom de votre aîné, dans le même style et la même époque.",
            ("Your first child's name", "Le prénom de l’aîné"),
            ("<p>The finder looks for names in the same style and era, but with a different first letter and ending, so Léo and Théo are never suggested together. Eras of French names come from the official INSEE birth statistics (1900–2021).</p><p>Tap ♡ to keep a name: your shortlist is saved in the link, ready to share.</p>",
             "<p>L’outil cherche des prénoms du même style et de la même époque, mais avec une autre initiale et une autre finale : Léo et Théo ne sont jamais proposés ensemble. Les époques des prénoms français viennent des statistiques officielles de l’INSEE (1900-2021).</p><p>Touchez ♡ pour garder un prénom : votre sélection est enregistrée dans le lien, prête à partager.</p>")),
}

def body(lang, mode):
    t = T[lang]; e = html.escape; js = dict(t["js"]); js["lang"] = lang; js["mode"] = mode; pg = PG[mode]; L = 0 if lang == "en" else 1
    js["base"] = {"fr": "/en/names/french/" if lang == "en" else "/fr/prenoms/francais/", "de": "/en/names/german/" if lang == "en" else "/fr/prenoms/allemands/"}
    sty = "".join(f'<option value="{s}">{e(t["js"]["styles"][s])}</option>' for s in STY)
    sur = f'<label>{t["sur"]}<input id="nm-s" autocomplete="off"></label>' if mode == "middle" else ""
    how = t["how"][0]
    return f'''<link rel="stylesheet" href="/assets/name-finder.css"><div class="nm">
<div class="nm-form">
 <label class="nm-big">{pg[6][L]}<input id="nm-n" autocomplete="off" placeholder="{e(t["name_ph"])}"></label><div id="nm-sug" class="nm-sug" aria-live="polite"></div>
 {sur}
 <div class="nm-filters">
  <label>{t["style"]}<select id="nm-style"><option value="">{t["any"]}</option>{sty}</select></label>
  <label>{t["len"]}<select id="nm-len"><option value="">{t["any"]}</option><option value="1">{t["l1"]}</option><option value="2">{t["l2"]}</option><option value="3">{t["l3"]}</option></select></label>
  <label>{t["origin"]}<select id="nm-origin"><option value="">{t["any"]}</option></select></label>
 </div>
</div>
<div id="nm-list" class="nm-list"></div>
<div id="nm-out" class="nm-out"></div>
<section class="nm-how"><h2>{how}</h2>{pg[7][L]}</section>
</div>
<script>window.NM={json.dumps(js, ensure_ascii=False)};</script><script src="/assets/name-finder.js"></script>'''

for mode, pg in PG.items():
    PAGES.append({"section": "names", "wide": True, "nolead": True,
        "en": (pg[0], pg[2], pg[4], body("en", mode)), "fr": (pg[1], pg[3], pg[5], body("fr", mode))})
