#!/usr/bin/env python3
"""Pins for the middle-name and sibling finders: a name with the ideas the site really gives for it (data/names_pairs.json,
data/names_middle_pages.json), in the frame of the names-index pins. One pin every two days at 10:00 (a slot nothing else uses).
Needs the local server (python3 -m http.server 8765). Writes pins/b1/nf-*.png (+ Desktop copies) and
Desktop/Sapiopedia/Pinterest/pinterest-bulk-upload-finders.csv."""
import csv, datetime, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import index_pins as I   # TEMPLATE (pin frame), shoot (render + empty-box check)

SITE, BOARD, SLOT, START = "https://sapiopedia.com", "Gift ideas", "10:00:00", datetime.date(2026, 11, 26)
PAIRS = json.load(open(os.path.join(I.ROOT, "data", "names_pairs.json"), encoding="utf-8"))
MID = json.load(open(os.path.join(I.ROOT, "data", "names_middle_pages.json"), encoding="utf-8"))
L = {"en": dict(kick_m="Middle name ideas", kick_s="Sibling name ideas", sub_m="Middle names that flow, picked by syllables, sound and style",
                sub_s="Same style and era, a different first letter and ending", sis="Sisters", bro="Brothers",
                url_m="sapiopedia.com", url_s="sapiopedia.com", label="Free middle name finder", label_s="Free sibling name finder",
                tags="Middle names, Baby names, Baby name ideas, French baby names, Sibling names, Middle name ideas, Pregnancy, Unique baby names"),
     "fr": dict(kick_m="Idées de deuxième prénom", kick_s="Prénoms de frère et sœur", sub_m="Des deuxièmes prénoms qui sonnent bien : syllabes, sons et style",
                sub_s="Même style et même époque, une autre initiale et une autre finale", sis="Sœurs", bro="Frères",
                url_m="sapiopedia.com", url_s="sapiopedia.com", label="Trouver un deuxième prénom, gratuit", label_s="Trouver un prénom de frère ou sœur, gratuit",
                tags="Deuxième prénom, Prénoms, Idées de prénoms, Prénom bébé, Prénoms de frère et sœur, Grossesse, Prénoms français")}
PINS = [  # id, lang, mode, name, h1, title (CSV), names shown (from the site's lists)
 ("nf-en-alice", "en", "m", "Alice", "Middle names that go <em>with Alice</em>", "Middle names that go with Alice: Jeanne, Claire, Joséphine…",
  "Jeanne Anne Claire Marie Joséphine Louise Blanche Marguerite"),
 ("nf-fr-louise", "fr", "m", "Louise", "Un deuxième prénom <em>pour Louise</em>", "Un deuxième prénom pour Louise : Marie, Élisabeth, Jeanne…",
  "Marie Élisabeth Jeanne Anne Emma Léa Sophie Hélène"),
 ("nf-en-emma", "en", "s", "Emma", "A brother or sister <em>for Emma</em>", "A brother or sister for Emma: sibling names that match",
  "Lucie Juliette Chloé Léa|Tom Victor Samuel Théo"),
 ("nf-en-arthur", "en", "m", "Arthur", "Middle names that go <em>with Arthur</em>", "Middle names that go with Arthur: Charles, Gabriel, Tom…",
  "Charles Gabriel Tom Paul Marc Aaron Ben Louis"),
 ("nf-fr-gabriel", "fr", "m", "Gabriel", "Un deuxième prénom <em>pour Gabriel</em>", "Un deuxième prénom pour Gabriel : Louis, Jacques, Victor…",
  "Louis Michel Jacques Paul Joseph Victor Samuel Antoine"),
 ("nf-fr-jules", "fr", "s", "Jules", "Un frère ou une sœur <em>pour Jules</em>", "Un frère ou une sœur pour Jules : des prénoms assortis",
  "Rose Anna Agathe Lucie|Gabriel Léo Adam Martin"),
]
CSS = ('<style>.fx{flex:1;min-height:0;border-radius:20px;background:#FBF6F0;box-shadow:0 24px 50px -24px rgba(42,31,38,.45);margin-bottom:36px;padding:30px 44px;display:grid;align-content:center;gap:8px}'
       '.fx .row{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:52px;letter-spacing:-.02em;color:#2A1F26;line-height:1.12;border-bottom:1px solid #E8D9DD;padding:6px 0}'
       '.fx .row:last-child{border-bottom:0}.fx .row em{color:#B8405E}.fx .cols{display:grid;grid-template-columns:1fr 1fr;gap:0 40px}'
       '.fx h3{margin:0 0 6px;font:600 22px "Source Sans 3",sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#8C6F78}.fx .cols .row{font-size:64px;padding:10px 0}.fx .cols h3{font-size:26px;margin-bottom:10px}</style>')

def page(pid, lang, mode, name, h1, names):
    t = L[lang]
    if mode == "m":
        box = "".join(f'<div class="row">{name} <em>{n}</em></div>' for n in names.split())
        kick, sub, url = t["kick_m"], t["sub_m"], t["url_m"]
    else:
        g, b = names.split("|")
        col = lambda h, ns: f'<div><h3>{h}</h3>' + "".join(f'<div class="row">{n}</div>' for n in ns.split()) + "</div>"
        box = f'<div class="cols">{col(t["sis"], g)}{col(t["bro"], b)}</div>'
        kick, sub, url = t["kick_s"], t["sub_s"], t["url_s"]
    h = re.sub(r'<div class="kick">.*?</div>', f'<div class="kick">{kick}</div>', I.TEMPLATE, 1)
    h = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", h, 1).replace("<p class=sub>♀ girls · ♂ boys · ⚥ both, with how to say each one</p>", f"<p class=sub>{sub}</p>")
    h = re.sub(r'<div class="ixf">.*?</div></div>', CSS + f'<div class="fx">{box}</div></div>', h, 1, flags=re.S)
    h = re.sub(r"<script>var f=document.*?</script>", "", h, 1, flags=re.S)
    h = re.sub(r'<div class="u"><b>.*?</b><span>.*?</span>', f'<div class="u"><b>{url}</b><span>{t["label"] if mode == "m" else t["label_s"]}</span>', h, 1)
    open(os.path.join(I.TMP, pid + ".html"), "w", encoding="utf-8").write(h)

def link(lang, mode, name):
    k = f"fr:{name}"
    if mode == "m" and k in MID:   # the name's own middle-name page
        return f'{SITE}{"/en/names/french/" if lang == "en" else "/fr/prenoms/francais/"}{MID[k]["slug"]}/{"middle-names" if lang == "en" else "deuxieme-prenom"}/'
    base = ("/en/names/middle-name-finder/" if mode == "m" else "/en/names/sibling-name-finder/") if lang == "en" else ("/fr/prenoms/deuxieme-prenom/" if mode == "m" else "/fr/prenoms/prenom-frere-soeur/")
    return f"{SITE}{base}#n={name}&b=fr"

if __name__ == "__main__":
    rows, day = [], START
    for pid, lang, mode, name, h1, title, names in PINS:
        allowed = {x[1] for x in PAIRS[f"fr:{name}"]["m" if mode == "m" else "s"]} | {x[1] for g in MID.get(f"fr:{name}", {}).get("groups", {}).values() for x in g}
        assert all(n in allowed for n in names.replace("|", " ").split()), (pid, [n for n in names.replace("|", " ").split() if n not in allowed])   # only what the site really suggests
        page(pid, lang, mode, name, h1, names); I.shoot(pid)
        shown = names.replace("|", " ").split()
        desc = (f"{', '.join(shown[:-1])} and {shown[-1]}: " + (f"middle names that flow with {name}, checked for syllables, sounds and style." if mode == "m" else f"sisters and brothers for {name}, in the same style and era but different enough.")
                + " Try your own names in Sapiopedia's free finder. Free, no sign-up.") if lang == "en" else (
                f"{', '.join(shown[:-1])} et {shown[-1]} : " + (f"des deuxièmes prénoms qui sonnent bien avec {name}, vérifiés pour les syllabes, les sons et le style." if mode == "m" else f"des sœurs et des frères pour {name}, du même style et de la même époque, mais assez différents.")
                + " Essayez vos propres prénoms dans l’outil gratuit de Sapiopedia. Gratuit, sans inscription.")
        rows.append([title, f"{SITE}/pins/b1/{pid}.png", BOARD, "", desc, link(lang, mode, name), f"{day.isoformat()}T{SLOT}", L[lang]["tags"]])
        day += datetime.timedelta(2)
    with open(os.path.join(I.DESK, "pinterest-bulk-upload-finders.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]); w.writerows(rows)
    for r in rows: print(r[6][:16], r[1].rsplit("/", 1)[1], "·", r[0], "→", r[5].replace(SITE, ""))
