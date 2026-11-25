#!/usr/bin/env python3
"""Pins for the seven dreams that have an engraved plate (data/dream_images.json), in English and French, in the layout of
Desktop/Sapiopedia/Dreams/dream_images.zip (*_pin.png) but with the whole plate. One English and one French pin every two days.
Needs the local server (python3 -m http.server 8765 from the repo root).
Writes pins/b1/dp-<lang>-<id>.png (+ a copy in Desktop/Sapiopedia/Pinterest/batch-2026-11/) and
Desktop/Sapiopedia/Pinterest/pinterest-bulk-upload-dreams.csv."""
import csv, datetime, json, os, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch"); DESK = os.path.expanduser("~/Library/CloudStorage/Dropbox/Sapiopedia/Pinterest"); OUT = os.path.join(DESK, "batch-2026-11")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE, BOARD, START = "https://sapiopedia.com", "Gift ideas", datetime.date(2026, 11, 24)
SLOT = {"en": "15:00:00", "fr": "12:00:00"}   # two times no other schedule uses
# (en id, fr id, en title, en teaser, fr title, fr teaser), in publishing order; death/mort last: a French pin to /fr/reves/mort/ goes out on 25 Nov
PINS = [
 ("mouse", "souris", "What does it mean to dream of a <em>mouse</em>?", "Seeing one, killing one, petting one: the old meanings",
  "Rêver de <em>souris</em> : signification", "En voir, en tuer, les laisser s’échapper…"),
 ("fish", "poisson", "Dreaming of <em>fish</em>: what it means", "Catching a big one, clear water, a dead fish…",
  "Rêver de <em>poissons</em> : bon signe ?", "En pêcher un gros, une eau claire, un poisson mort…"),
 ("wedding", "mariage", "Dreaming of a <em>wedding</em>: what it means", "Attending one, a merry wedding, marrying in secret…",
  "Rêver de <em>mariage</em> : ce que ça annonce", "Y assister, se marier, un ancien amour à la cérémonie…"),
 ("ghost", "fantome", "What does it mean to dream of a <em>ghost</em>?", "A ghost that speaks, a parent, a friend who has died",
  "Que veut dire rêver d’un <em>fantôme</em> ?", "Un fantôme qui parle, un parent, un ami disparu"),
 ("mother", "mere", "Dreaming of your <em>mother</em>: what it means", "Talking with her, a quarrel, hearing her call you",
  "Rêver de sa <em>mère</em> : signification", "Lui parler, se disputer, l’entendre vous appeler"),
 ("blood", "sang", "What does it mean to dream of <em>blood</em>?", "On your hands, on your clothes, from a wound",
  "Rêver de <em>sang</em> : signification", "Sur les mains, sur les vêtements, d’une blessure"),
 ("death", "mort", "Dreaming of <em>death</em>: is it a bad sign?", "Your own death, a loved one, news of a death",
  "Rêver de la <em>mort</em> : est-ce un mauvais signe ?", "Sa propre mort, un proche, une nouvelle qu’on vous annonce"),
]
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..500&family=EB+Garamond:ital@0;1&family=Source+Sans+3:wght@600&display=swap">
<style>*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:1500px;overflow:hidden;background:#FAF4EF;position:relative;color:#2A1F26}
.fr1{position:absolute;inset:28px;border:2px solid #E3D2CC}.fr2{position:absolute;inset:40px;border:1px solid #EBDDD8}
.pl{position:absolute;left:86px;right:86px;top:86px;height:800px;display:flex;align-items:center;justify-content:center}
.pl img{max-width:100%;max-height:100%;display:block;box-shadow:0 0 0 1px #E3D2CC}
.k{position:absolute;left:0;right:0;top:930px;text-align:center;font:600 21px 'Source Sans 3',sans-serif;letter-spacing:.28em;text-transform:uppercase;color:#8C6F78}
h1{position:absolute;left:90px;right:90px;top:978px;margin:0;text-align:center;font:400 74px/1.06 Fraunces,Georgia,serif;letter-spacing:-.025em}
h1 em{color:#B8405E}
p{position:absolute;left:110px;right:110px;top:1250px;margin:0;text-align:center;font:italic 34px/1.3 'EB Garamond',Georgia,serif;color:#6E5A62}
.u{position:absolute;left:0;right:0;bottom:84px;text-align:center;font:600 22px 'Source Sans 3',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#B8405E}
</style></head><body><div class="fr1"></div><div class="fr2"></div>
<div class="pl"><img src="/assets/dreams/{IMG}.webp" alt=""></div><div class="k">{KICK}</div><h1>{H1}</h1><p>{TEASER}</p><div class="u">sapiopedia.com{PATH}</div></body></html>"""
KICK = {"en": "Dream dictionary", "fr": "Dictionnaire des rêves"}
TAGS = {"en": "Dream meanings, Dream interpretation, Dream dictionary, {w} dream meaning, Spiritual meaning, Dreams, Symbolism, Vintage engraving, Superstitions",
        "fr": "Signification des rêves, Interprétation des rêves, Dictionnaire des rêves, Rêve {w}, Symbolique, Rêves, Gravure ancienne, Superstitions"}

def render(pid, html_):
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(html_)
    out = os.path.join(ROOT, "pins", "b1", pid + ".png")
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--virtual-time-budget=8000", "--window-size=1000,1500", f"--screenshot={out}",
                    f"http://127.0.0.1:8765/_pins_batch/{pid}.html"], capture_output=True, timeout=120)
    shutil.copy(out, os.path.join(OUT, pid + ".png"))

if __name__ == "__main__":
    IMG = json.load(open(os.path.join(ROOT, "data", "dream_images.json"), encoding="utf-8"))
    E = {l: {x["id"]: x for x in json.load(open(os.path.join(ROOT, "data", f"dreams_{l}.json"), encoding="utf-8"))["entries"]} for l in ("en", "fr")}
    titles = set()
    for f in os.listdir(DESK):
        if f.startswith("pinterest-bulk-upload") and f.endswith(".csv") and f != "pinterest-bulk-upload-dreams.csv":
            titles |= {r["Title"] for r in csv.DictReader(open(os.path.join(DESK, f), encoding="utf-8"))}
    rows, day = [], START
    for en_id, fr_id, en_t, en_p, fr_t, fr_p in PINS:
        for lang, i, h1, teaser in (("en", en_id, en_t, en_p), ("fr", fr_id, fr_t, fr_p)):
            path = f"/{lang}/{'dreams' if lang == 'en' else 'reves'}/{i}/"; pid = f"dp-{lang}-{i}"
            render(pid, PAGE.replace("{IMG}", IMG[lang][i]["img"]).replace("{KICK}", KICK[lang]).replace("{H1}", h1).replace("{TEASER}", teaser).replace("{PATH}", path))
            title = h1.replace("<em>", "").replace("</em>", ""); x = E[lang][i]
            desc = x["one"] + (" Every version of the dream, good signs and bad, from the old dream books. Free, no sign-up." if lang == "en"
                               else " Toutes les versions du rêve, bons et mauvais signes, d’après les anciens livres des songes. Gratuit, sans inscription.")
            assert title not in titles and len(title) <= 100 and len(desc) <= 500, pid
            rows.append([title, f"{SITE}/pins/b1/{pid}.png", BOARD, "", desc, SITE + path, f"{day.isoformat()}T{SLOT[lang]}", TAGS[lang].format(w=x["word"])])
        day += datetime.timedelta(2)
    with open(os.path.join(DESK, "pinterest-bulk-upload-dreams.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]); w.writerows(rows)
    for r in rows: print(r[6][:16], r[1].rsplit("/", 1)[1], "·", r[0])
