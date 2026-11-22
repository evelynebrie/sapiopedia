#!/usr/bin/env python3
"""Ten more pins like ix-en-L (the best performer): the names index itself, opened at one letter, in the pin frame.
Five letters of the French names, five of the German names; one pin a day at 18:00 (a slot no other schedule uses),
French and German alternating, never on a day that already has a pin to the same index page.
Needs the local server (python3 -m http.server 8765 from the repo root) and _pins_batch/ix-en-L.html (tools/pins_batch.py) as the template.
Writes the PNGs to Desktop/Sapiopedia/Pinterest/batch-2026-11/ and pins/b1/, and Desktop/Sapiopedia/Pinterest/pinterest-bulk-upload-index.csv."""
import csv, datetime, json, os, re, shutil, subprocess
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch"); DESK = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest"); OUT = os.path.join(DESK, "batch-2026-11")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE, BOARD, SLOT, START = "https://sapiopedia.com", "Gift ideas", "18:00:00", datetime.date(2026, 11, 23)
TEMPLATE = open(os.path.join(TMP, "ix-en-L.html"), encoding="utf-8").read()
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

def page(pid, S, L, h1):
    h = re.sub(r'<div class="kick">.*?</div>', f'<div class="kick">{S["kick"]}</div>', TEMPLATE, 1)
    h = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", h, 1).replace("<p class=sub>♀ girls · ♂ boys · ⚥ both, with how to say each one</p>", f"<p class=sub>{S['sub']}</p>")
    h = h.replace('src="/en/names/french/"', f'src="{S["base"]}"').replace('"l-L"', f'"l-{L}"')
    h = re.sub(r'<div class="u"><b>.*?</b><span>.*?</span>', f'<div class="u"><b>sapiopedia.com{S["base"]}</b><span>{S["label"]}</span>', h, 1)
    open(os.path.join(TMP, pid + ".html"), "w", encoding="utf-8").write(h)

def shoot(pid):
    out = os.path.join(OUT, pid + ".png")
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--virtual-time-budget=20000", "--window-size=1000,1500", f"--screenshot={out}",
                    f"http://127.0.0.1:8765/_pins_batch/{pid}.html"], capture_output=True, timeout=240)
    shutil.copy(out, os.path.join(ROOT, "pins", "b1", pid + ".png")); return pid

if __name__ == "__main__":
    for pid, S, L, h1, *_ in PINS: page(pid, S, L, h1)
    with cf.ThreadPoolExecutor(4) as ex: print("rendered", list(ex.map(shoot, [p[0] for p in PINS])))
    # days that already have a pin to the same index page (any CSV on the Desktop) are skipped for that page
    busy, titles = set(), set()
    for f in os.listdir(DESK):
        if f.startswith("pinterest-bulk-upload") and f.endswith(".csv") and f != "pinterest-bulk-upload-index.csv":
            for r in csv.DictReader(open(os.path.join(DESK, f), encoding="utf-8")):
                busy.add((r["Link"].split("#")[0], r["Publish date"][:10])); titles.add(r["Title"])
    day, rows = START, []
    for pid, S, L, h1, title, desc in PINS:
        link = SITE + S["base"]
        while (link, day.isoformat()) in busy: day += datetime.timedelta(1)
        assert title not in titles and len(title) <= 100 and len(desc) <= 480, pid
        rows.append([title, f"{SITE}/pins/b1/{pid}.png", BOARD, "", desc + " Free, no sign-up.", f"{link}#l-{L}", f"{day.isoformat()}T{SLOT}", S["tags"].format(L=L)])
        day += datetime.timedelta(1)
    with open(os.path.join(DESK, "pinterest-bulk-upload-index.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]); w.writerows(rows)
    for r in rows: print(r[6][:16], r[1].rsplit("/", 1)[1], "·", r[0])
