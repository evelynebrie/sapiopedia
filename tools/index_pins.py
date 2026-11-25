#!/usr/bin/env python3
"""Ten more pins like ix-en-L (the best performer): the names index itself, opened at one letter, in the pin frame.
Five letters of the French names, five of the German names; one pin a day at 18:00 (a slot no other schedule uses),
French and German alternating, never on a day that already has a pin to the same index page.
Needs the local server (python3 -m http.server 8765 from the repo root) and _pins_batch/ix-en-L.html (tools/pins_batch.py) as the template.
Writes the PNGs to Desktop/Sapiopedia/Pinterest/batch-2026-11/ and pins/b1/, and Desktop/Sapiopedia/Pinterest/pinterest-bulk-upload-index.csv."""
import csv, datetime, json, os, re, shutil, subprocess
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch"); DESK = os.path.expanduser("~/Library/CloudStorage/Dropbox/Sapiopedia/Pinterest"); OUT = os.path.join(DESK, "batch-2026-11")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE, BOARD, SLOT, START = "https://sapiopedia.com", "Gift ideas", "18:00:00", datetime.date(2026, 11, 23)
TEMPLATE = open(os.path.join(TMP, "ix-en-L.html"), encoding="utf-8").read().replace(   # hide the status line above the letter (its last pixels showed above the rule)
    'd.querySelectorAll("section.nf-l")', 'var _s=d.createElement("style");_s.textContent=".nf-status,.dd-az,.nf-none{visibility:hidden!important}";d.head.appendChild(_s);d.querySelectorAll("section.nf-l")', 1)
N = {k: len(json.load(open(os.path.join(ROOT, "data", f"names_{k}_list.json"), encoding="utf-8"))) for k in ("fr", "de")}

FR = dict(kick="French first names", base="/en/names/french/", label="Every name with its origin and a recording", sub="♀ girls · ♂ boys · ⚥ both, with how to say each one",
          tags="French baby names, French girl names, French boy names, Baby names, Baby name ideas, Unique baby names, Pregnancy, French aesthetic, Names starting with {L}")
DE = dict(kick="German first names", base="/en/names/german/", label="Every name with a recording and its pet forms", sub="♀ girls · ♂ boys · ⚥ both, with how to say each one",
          tags="German baby names, German girl names, German boy names, Baby names, Baby name ideas, Unique baby names, Old German names, Pregnancy, Names starting with {L}")
PINS = [  # id, set, letter, h1 (image), title (CSV, unique), description
 ("ixde-en-F", DE, "F", f"{N['de']:,} German names, <em>from A to Z</em>", f"{N['de']:,} German names, from A to Z",
  "Frieda, Friedrich, Felix, Finn: the full list of German first names, A to Z, marked for girls, boys or both. Open any name to hear it said by a native speaker, with its origin and pet forms."),
 ("ixfr-en-M", FR, "M", "French names <em>starting with M</em>", "French names starting with M: girls, boys and unisex",
  "Margaux, Mathilde, Maël, Marius: every French first name starting with M, marked for girls, boys or both. Open any name for its origin, its French pronunciation and a recording."),
 ("ixde-en-H", DE, "H", "German names <em>starting with H</em>", "German names starting with H, with how to say each one",
  "Hannah, Heidi, Heinrich, Henry: every German first name starting with H, for girls, boys or both. Open any name to hear it, with its origin and its pet forms (Heinrich → Heini)."),
 ("ixfr-en-C", FR, "C", "French baby names, <em>letter&nbsp;C</em>", "French baby names, letter C: Camille, Capucine, Clément…",
  "Camille, Capucine, Céleste, Clément: every French first name starting with C, marked for girls, boys or both, with its origin, its French pronunciation and a recording."),
 ("ixde-en-K", DE, "K", "German baby names, <em>letter K</em>", "German baby names, letter K: Karl, Klara, Konrad…",
  "Karl, Klara, Konrad, Klaus: every German first name starting with K, for girls, boys or both. Hear each one said by a native speaker, with its origin and pet forms."),
 ("ixfr-en-G", FR, "G", "French names <em>that start with G</em>", "French names that start with G, with how to say each one",
  "Gabriel, Gabrielle, Gaspard, Gustave: every French first name starting with G, for girls, boys or both. Open any name for its origin, its French pronunciation and a recording."),
 ("ixde-en-W", DE, "W", "Old German names <em>starting with W</em>", "Old German names starting with W: Wilhelm, Wolfgang…",
  "Wilhelm, Wolfgang, Wilhelmine, Walter: every German first name starting with W, from old classics to rare finds. Hear each one, with its origin and its pet forms (Wolfgang → Wolfi)."),
 ("ixfr-en-E", FR, "E", "French girl and boy names, <em>letter E</em>", "French girl and boy names, letter E: Éloïse, Élise, Émile…",
  "Éloïse, Élise, Émile, Étienne: every French first name starting with E, marked for girls, boys or both, with its origin, its French pronunciation and a recording."),
 ("ixde-en-L", DE, "L", "German names <em>that start with L</em>", "German names that start with L: Lina, Lukas, Ludwig…",
  "Lina, Lena, Lukas, Ludwig: every German first name starting with L, for girls, boys or both. Hear each one said by a native speaker, with its origin and pet forms."),
 ("ixfr-en-A", FR, "A", f"{N['fr']:,} French names, <em>starting with&nbsp;A</em>", f"{N['fr']:,} French names, starting with A: Adèle, Agathe, Apolline…",
  "Adèle, Agathe, Apolline, Arthur: the French first names starting with A, marked for girls, boys or both. Open any name for its origin, its French pronunciation and a recording."),
]

# curated lists: the most beautiful names (picked by hand among cards with a pronunciation), shown as a list in the same box
CUR = [  # id, set, gender, h1, title, names
 ("cur-fr-girls", FR, "f", "The most beautiful <em>French girl names</em>", "The most beautiful French girl names, with how to say them",
  "Adèle Agathe Apolline Capucine Clémence Colette Héloïse Joséphine Juliette Louise Margaux Rose"),
 ("cur-de-boys", DE, "m", "The most beautiful <em>German boy names</em>", "The most beautiful German boy names, with how to say them",
  "Anton Emil Felix Friedrich Heinrich Jakob Konrad Leopold Ludwig Moritz Oskar Theodor"),
 ("cur-fr-boys", FR, "m", "The most beautiful <em>French boy names</em>", "The most beautiful French boy names, with how to say them",
  "Arthur Augustin Bastien Côme Émile Gabriel Gaspard Jules Léon Louis Lucien Raphaël"),
 ("cur-de-girls", DE, "f", "The most beautiful <em>German girl names</em>", "The most beautiful German girl names, with how to say them",
  "Antonia Charlotte Clara Emilia Frieda Helene Johanna Lotte Magdalena Marlene Rosa Theresa"),
 ("cur-fr-unisex", FR, "n", "Beautiful French names <em>for girls and boys</em>", "Beautiful French unisex names, for girls and boys",
  "Alix Anouk Camille Céleste Charlie Claude Dominique Eden Lou Maxime"),
]
CUR_CSS = ('<style>.cur{flex:1;min-height:0;border-radius:20px;background:#FBF6F0;box-shadow:0 24px 50px -24px rgba(42,31,38,.45);margin-bottom:36px;'
           'padding:34px 44px;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:0 40px;align-content:stretch}'
           '.cur div{display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #E8D9DD;padding:4px 0}'
           '.cur div:nth-last-child(-n+2){border-bottom:0}.cur b{font-family:Fraunces,Georgia,serif;font-weight:400;font-size:46px;letter-spacing:-.02em;color:#2A1F26;line-height:1.05}'
           '.cur b i{font-style:normal;font-size:30px;color:#B8405E;margin-left:10px;vertical-align:4px}.cur span{font-family:Fraunces,Georgia,serif;font-style:italic;font-weight:300;font-size:25px;color:#6E5A62}</style>')
SYMB = {"f": "♀", "m": "♂", "n": "⚥"}

def card(k, w):
    """(name shown, gender, pronunciation) from the site's own data."""
    rows = {r[0]: r[3] for r in json.load(open(os.path.join(ROOT, "data", f"names_{k}_list.json"), encoding="utf-8"))}
    D = json.load(open(os.path.join(ROOT, "assets", f"names-{k}.json"), encoding="utf-8"))
    r = D[rows[w]]; ipa = (r.get("ipa") or "").strip("\\")
    return w, r["g"], (f"/{ipa}/" if ipa and not ipa.startswith(("[", "/")) else ipa)

def page_cur(pid, S, g, h1, names):
    k = "de" if S is DE else "fr"
    items = "".join(f'<div><b>{w}<i>{SYMB.get(gg, "")}</i></b><span>{ipa}</span></div>' for w, gg, ipa in (card(k, w) for w in names.split()))
    h = re.sub(r'<div class="kick">.*?</div>', f'<div class="kick">{S["kick"]}</div>', TEMPLATE, 1)
    h = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", h, 1).replace("<p class=sub>♀ girls · ♂ boys · ⚥ both, with how to say each one</p>",
        f"<p class=sub>{len(names.split())} favourites, with how to say each one</p>")
    h = re.sub(r'<div class="ixf">.*?</div></div>', CUR_CSS + f'<div class="cur">{items}</div></div>', h, 1, flags=re.S)
    h = re.sub(r"<script>var f=document.*?</script>", "", h, 1, flags=re.S)
    h = re.sub(r'<div class="u"><b>.*?</b><span>.*?</span>', f'<div class="u"><b>sapiopedia.com{S["base"]}</b><span>{S["label"]}</span>', h, 1)
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(h)

def page(pid, S, L, h1):
    h = re.sub(r'<div class="kick">.*?</div>', f'<div class="kick">{S["kick"]}</div>', TEMPLATE, 1)
    h = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", h, 1).replace("<p class=sub>♀ girls · ♂ boys · ⚥ both, with how to say each one</p>", f"<p class=sub>{S['sub']}</p>")
    h = h.replace('src="/en/names/french/"', f'src="{S["base"]}"').replace('"l-L"', f'"l-{L}"')
    h = re.sub(r'<div class="u"><b>.*?</b><span>.*?</span>', f'<div class="u"><b>sapiopedia.com{S["base"]}</b><span>{S["label"]}</span>', h, 1)
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(h)

def filled(png):
    """True when the box shows the list (a blank box is one flat colour)."""
    from PIL import Image, ImageStat
    return ImageStat.Stat(Image.open(png).convert("L").crop((100, 520, 900, 1250))).stddev[0] > 10

def shoot(pid, w=1000, h=1500):
    out = os.path.join(TMP, pid + "-shot.png")   # only a filled render reaches the Desktop and pins/b1
    for budget in (20000, 30000, 45000):   # a screenshot taken before the index has loaded shows an empty box: check and retry
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", f"--virtual-time-budget={budget}", f"--window-size={w},{h}", f"--screenshot={out}",
                        f"http://127.0.0.1:8765/_pins_batch/{pid}.html"], capture_output=True, timeout=300)
        if filled(out): break
    else: raise SystemExit(f"{pid}: the box is still empty")
    shutil.copy(out, os.path.join(OUT, pid + ".png")); shutil.copy(out, os.path.join(ROOT, "pins", "b1", pid + ".png")); return pid

if __name__ == "__main__":
    for pid, S, L, h1, *_ in PINS: page(pid, S, L, h1)
    for pid, S, g, h1, title, names in CUR: page_cur(pid, S, g, h1, names)
    only = os.environ.get("ONLY")
    with cf.ThreadPoolExecutor(2) as ex: print("rendered", list(ex.map(shoot, [p[0] for p in PINS + CUR if not only or re.search(only, p[0])])))
    # days that already have a pin to the same index page (any CSV on the Desktop) are skipped for that page
    busy, titles = set(), set()
    for f in os.listdir(DESK):
        if f.startswith("pinterest-bulk-upload") and f.endswith(".csv") and "-index" not in f and "names-dreams" not in f:   # not its own output
            for r in csv.DictReader(open(os.path.join(DESK, f), encoding="utf-8")):
                busy.add((r["Link"].split("#")[0], r["Publish date"][:10])); titles.add(r["Title"])
    day, rows = START, []
    for pid, S, L, h1, title, desc in PINS:
        link = SITE + S["base"]
        while (link, day.isoformat()) in busy: day += datetime.timedelta(1)
        assert title not in titles and len(title) <= 100 and len(desc) <= 480, pid
        rows.append([title, f"{SITE}/pins/b1/{pid}.png", BOARD, "", desc + " Free, no sign-up.", f"{link}#l-{L}", f"{day.isoformat()}T{SLOT}", S["tags"].format(L=L)])
        day += datetime.timedelta(1)
    for pid, S, g, h1, title, names in CUR:
        link = SITE + S["base"]
        while (link, day.isoformat()) in busy: day += datetime.timedelta(1)
        lang = "German" if S is DE else "French"; who = {"f": "girls", "m": "boys", "n": "girls and boys"}[g]
        ns = names.split(); desc = (f"{', '.join(ns[:-1])} and {ns[-1]}: {len(ns)} beautiful {lang} names for {who}, with how to say each one. "
                                    f"Open the {lang} names on Sapiopedia to hear every name and see its origin. Free, no sign-up.")
        assert title not in titles and len(title) <= 100 and len(desc) <= 500, pid
        rows.append([title, f"{SITE}/pins/b1/{pid}.png", BOARD, "", desc, link, f"{day.isoformat()}T{SLOT}",
                     S["tags"].split(", Names starting")[0] + f", Beautiful {lang} names, {lang} {'unisex' if g == 'n' else ('girl' if g == 'f' else 'boy')} names"])
        day += datetime.timedelta(1)
    for r in rows:   # re-rendered after the first upload (empty box, then a sliver of text above the letter): new image URL so Pinterest fetches the fixed one
        if "/ix" in r[1]: r[1] += "?v=3"
    cols = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
    with open(os.path.join(DESK, "pinterest-bulk-upload-index.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
    with open(os.path.join(DESK, "pinterest-bulk-upload-index-update.csv"), "w", encoding="utf-8", newline="") as fh:   # for an account that already has the first ten
        w = csv.writer(fh); w.writerow(cols); w.writerows([r for r in rows if "?v=3" in r[1] or "/cur-" in r[1]])
    for r in rows: print(r[6][:16], r[1].rsplit("/", 1)[1], "·", r[0])
