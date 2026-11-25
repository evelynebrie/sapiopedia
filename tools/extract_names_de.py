#!/usr/bin/env python3
"""Extract German first names into assets/names-de.json (details, one card per name) and data/names_de_list.json (index rows),
in the same format as the French names (tools/extract_names.py), so content/names_fr.py builds both.

Sources (kaikki/wiktextract dumps, in ~/Library/CloudStorage/Dropbox/Sapiopedia/Names):
  de-extract.jsonl.gz          German Wiktionary, "Vorname" entries: gender, pronunciation, recording, origin, other languages,
                               short and pet forms, the feminine or masculine form, a dated quotation (1925 or earlier)
  raw-wiktextract-data.jsonl.gz English Wiktionary, German given names: the English etymology (field "ete", shown on the English site)
  fr-extract.jsonl             French Wiktionary, German "Prénom" entries: the French etymology (field "et", shown on the French site)
  data/firstnames.csv          the countries where each name is given
The German etymology itself is not shown (the site is in English and French); the origin language is read from it.
Wiktionary text is CC BY-SA 4.0 and credited on each page; recordings stay on Wikimedia Commons, linked from the page.

Run:  python3 tools/extract_names_de.py [names folder]
"""
import gzip, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_names as EN
from extract_names import LANGS, countries, fold, merge          # same helpers as the French names
_nb = EN.neighbours   # German keeps Hanna/Hannah apart from Anna: a leading h is not a spelling variant here
EN.neighbours = lambda k: {n for n in _nb(k) if n != "h" + k and k != "h" + n}
from add_english_etymology import clean as clean_en

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Library/CloudStorage/Dropbox/Sapiopedia/Names")

# origin languages as German etymologies write them -> (French, English), checked longest first
ORIG = {"altgriechisch": ("grec ancien", "Ancient Greek"), "griechisch": ("grec", "Greek"), "lateinisch": ("latin", "Latin"), "hebräisch": ("hébreu", "Hebrew"),
        "althochdeutsch": ("vieux haut allemand", "Old High German"), "mittelhochdeutsch": ("moyen haut-allemand", "Middle High German"),
        "altsächsisch": ("vieux saxon", "Old Saxon"), "niederdeutsch": ("bas allemand", "Low German"), "germanisch": ("germanique", "Germanic"),
        "friesisch": ("frison", "Frisian"), "altnordisch": ("norrois", "Old Norse"), "nordisch": ("norrois", "Old Norse"), "skandinavisch": ("scandinave", "Scandinavian"),
        "schwedisch": ("suédois", "Swedish"), "dänisch": ("danois", "Danish"), "norwegisch": ("norvégien", "Norwegian"), "isländisch": ("islandais", "Icelandic"),
        "finnisch": ("finnois", "Finnish"), "keltisch": ("celte", "Celtic"), "irisch": ("irlandais", "Irish"), "gälisch": ("gaélique", "Gaelic"), "walisisch": ("gallois", "Welsh"),
        "englisch": ("anglais", "English"), "französisch": ("français", "French"), "italienisch": ("italien", "Italian"), "spanisch": ("espagnol", "Spanish"),
        "portugiesisch": ("portugais", "Portuguese"), "niederländisch": ("néerlandais", "Dutch"), "slawisch": ("slave", "Slavic"), "russisch": ("russe", "Russian"),
        "polnisch": ("polonais", "Polish"), "tschechisch": ("tchèque", "Czech"), "ungarisch": ("hongrois", "Hungarian"), "litauisch": ("lituanien", "Lithuanian"),
        "arabisch": ("arabe", "Arabic"), "aramäisch": ("araméen", "Aramaic"), "persisch": ("persan", "Persian"), "türkisch": ("turc", "Turkish"),
        "sanskrit": ("sanskrit", "Sanskrit"), "japanisch": ("japonais", "Japanese"), "ägyptisch": ("égyptien", "Egyptian"), "baskisch": ("basque", "Basque"),
        "albanisch": ("albanais", "Albanian"), "armenisch": ("arménien", "Armenian"), "georgisch": ("géorgien", "Georgian"), "rumänisch": ("roumain", "Romanian"),
        "kroatisch": ("croate", "Croatian"), "serbisch": ("serbe", "Serbian"), "bulgarisch": ("bulgare", "Bulgarian")}
ORIG_RE = re.compile(r"(?<![a-zäöü])(" + "|".join(sorted(ORIG, key=len, reverse=True)) + r")(?:e[nrms]?)?\b", re.I)
EN_ORIG = {v[1]: v for v in ORIG.values()} | {"Old French": ("ancien français", "Old French"), "Latvian": ("letton", "Latvian"), "Yiddish": ("yiddish", "Yiddish")}

def origin_de(et):
    """The first origin language named early in the German etymology (the name's own source, not a later mention)."""
    m = ORIG_RE.search(et[:160])
    return ORIG[m.group(1).lower()] if m else None

def origin_en(et):
    m = re.match(r"^(?:Borrowed from|From|Derived from|Of)\s+(?:the\s+)?(" + "|".join(sorted(EN_ORIG, key=len, reverse=True)) + r")\b", et)
    return EN_ORIG[m.group(1)] if m else None

def gender_de(d):
    c = d.get("categories", []); f, m = "Vorname f (Deutsch)" in c, "Vorname m (Deutsch)" in c
    return "n" if f and m else "f" if f else "m" if m else "u"

def gender_en(d):
    g = " ".join(" ".join(s.get("glosses", [])) for s in d.get("senses", []))
    f, m = "female given name" in g, "male given name" in g.replace("female given name", "")
    return "n" if f and m else "f" if f else "m" if m else "u"

def lines(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, env={**os.environ, "LC_ALL": "C"}).stdout.splitlines()

def sound(d):
    """Prefer a recording made in Germany; credit: the Commons file page."""
    snds = [s for s in d.get("sounds", []) if s.get("mp3_url")]
    if not snds: return {}
    s = next((s for s in snds if "Germany" in s.get("tags", [])), None) or next((s for s in snds if not s.get("tags")), snds[0])
    out = {"mp3": s["mp3_url"], "by": "Wikimedia Commons", "file": "https://commons.wikimedia.org/wiki/File:" + s["audio"].replace(" ", "_")}
    if s.get("tags"): out["acc"] = ", ".join(s["tags"])
    return out

def main():
    C = countries(); names = {}
    # ---------------------------------------------------------------- German Wiktionary
    for l in lines(f"gzip -dc '{SRC}/de-extract.jsonl.gz' | grep -F '\"pos_title\": \"Vorname\"' | grep -F '\"lang_code\": \"de\"'"):
        d = json.loads(l)
        if d.get("lang_code") != "de" or d.get("pos_title") != "Vorname": continue
        w = d["word"].strip()
        if not w or w in names or " " in w: continue
        r = {"g": gender_de(d)}
        ipa = next((s["ipa"] for s in d.get("sounds", []) if s.get("ipa") and "…" not in s["ipa"]), None)
        if ipa: r["ipa"] = ipa
        r.update(sound(d))
        et = " ".join(d.get("etymology_texts", [])).strip()
        if et:
            o = origin_de(re.sub(r"^\[\d+\]\s*", "", et))
            if o: r["o"], r["oe"] = o
            m = re.match(r"^(?:\[\d+\]\s*)?(?:Nebenform|Variante|Schreibvariante)\s+(?:von|zu)\s+([A-ZÄÖÜ][a-zäöüß]+)", et)
            if m: r["alt"] = [m.group(1)]
        tr = {}
        for t in d.get("translations", []):
            lc, x = t.get("lang_code"), t.get("word")
            if lc in LANGS and lc != "de" and x and x != w:
                cur = tr.setdefault(LANGS[lc], [])
                if x not in cur and len(cur) < 3: cur.append(x)
        if tr: r["tr"] = dict(list(tr.items())[:14])
        forms = lambda *tags: [f["form"] for f in d.get("forms", []) if set(f.get("tags", [])) & set(tags) and f.get("form") and f["form"] != w and " " not in f["form"] and not f["form"].endswith(".")]
        nick = list(dict.fromkeys(forms("abbreviation", "affective", "diminutive")))[:8]
        if nick: r["nick"] = nick
        cf = list(dict.fromkeys(forms("feminine" if r["g"] == "m" else "masculine")))[:4] if r["g"] in "mf" else []
        if cf: r["cf"] = cf
        vf = list(dict.fromkeys(forms("variant", "alternative")))[:8]
        if vf: r["vf"] = vf
        for sn in d.get("senses", []):
            for ex in sn.get("examples", []):
                y = re.findall(r"\b(1[0-9]{3})\b", ex.get("ref", ""))
                if ex.get("text") and y and int(max(y)) <= 1925 and 20 < len(ex["text"]) < 420:
                    r["q"] = [ex["text"], ex["ref"]]; break
            if "q" in r: break
        names[w] = r
    n_de = len(names)
    # ---------------------------------------------------------------- English Wiktionary: German given names (English etymology; names the German Wiktionary lacks)
    en = {}
    for l in lines(f"gzip -dc '{SRC}/raw-wiktextract-data.jsonl.gz' | grep -F '\"lang_code\": \"de\"' | grep -F '\"pos\": \"name\"' | grep -F 'given name'"):
        d = json.loads(l)
        if d.get("lang_code") != "de" or d.get("pos") != "name" or gender_en(d) == "u": continue
        w = d["word"].strip()
        if " " in w: continue
        e = en.setdefault(w, {"g": gender_en(d)})
        t = clean_en(d.get("etymology_text") or "")
        if t and "ete" not in e: e["ete"] = t[:700]
        if "ipa" not in e:
            ipa = next((s["ipa"] for s in d.get("sounds", []) if s.get("ipa") and "…" not in s["ipa"]), None)
            if ipa: e["ipa"] = ipa
        if "mp3" not in e: e.update(sound(d))
    for w, e in en.items():
        r = names.setdefault(w, {"g": e["g"]})
        if r["g"] == "u": r["g"] = e["g"]
        for k in ("ete", "ipa", "mp3", "by", "file", "acc"):
            if k in e and k not in r: r[k] = e[k]
        if "o" not in r and e.get("ete"):
            o = origin_en(e["ete"])
            if o: r["o"], r["oe"] = o
    n_en = len(names) - n_de
    # ---------------------------------------------------------------- French Wiktionary: German first names (French etymology)
    for l in lines(f"grep -F '\"pos_title\": \"Prénom\"' '{SRC}/fr-extract.jsonl' | grep -F '\"lang_code\": \"de\"'"):
        d = json.loads(l)
        if d.get("lang_code") != "de": continue
        w = d["word"].strip()
        ets = [x.strip() for x in d.get("etymology_texts", []) if x.strip()]
        ets = [re.sub(r"^\(Prénom\)\s*\.?\s*", "", x) for x in ets if x.startswith("(Prénom)")] or ([ets[0]] if len(ets) == 1 and not ets[0].startswith("(") else [])
        et = " ".join(ets)
        if w not in names and " " not in w and w[:1].isupper():   # a German name only the French Wiktionary has
            t = set(d.get("tags", [])); g = "n" if {"feminine", "masculine"} <= t else "f" if "feminine" in t else "m" if "masculine" in t else "u"
            if g != "u":
                names[w] = {"g": g}
                ipa = next((s["ipa"] for s in d.get("sounds", []) if s.get("ipa") and "…" not in s["ipa"]), None)
                if ipa: names[w]["ipa"] = ipa
        if w in names and len(et) > 8 and not re.search(r"Étymologie manquante|ajouter en cliquant", et):
            names[w]["et"] = re.sub(r"\b([Nn]om|[Pp]rénom|[Mm]ot|ou)(composé|dérivé)", r"\1 \2", et)[:700]
    for w, r in names.items():
        cs = C.get(fold(w))
        if cs: r["c"] = cs[:10]
    det, rows = merge(names)
    json.dump(det, open(os.path.join(ROOT, "assets", "names-de.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(rows, open(os.path.join(ROOT, "data", "names_de_list.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    from collections import Counter
    print(f"{n_de} names from the German Wiktionary, {n_en} more from the English one; {len(det)} cards;", dict(Counter(r["g"] for r in det.values())))
    print({k: sum(k in r for r in det.values()) for k in ("ipa", "mp3", "o", "et", "ete", "tr", "nick", "cf", "vf", "c", "q", "v")})
    print("origins:", Counter(r.get("oe") for r in det.values()).most_common(10))

if __name__ == "__main__":
    main()
