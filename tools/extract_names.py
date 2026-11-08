#!/usr/bin/env python3
"""Extract French first names from the French Wiktionary dump (kaikki/wiktextract fr-extract.jsonl)
into assets/names-fr.json (details, loaded by the page) and data/names_fr_list.json (name + gender, used by the build).

Kept per name: gender, pronunciation, recording, first record, origin language, the etymology text, forms in other
languages, compound names, a quotation from a public-domain book (dated 1925 or earlier), the share of women/men when the
record gives counts, and the countries where the name is given (data/firstnames.csv).
Wiktionnaire text is CC BY-SA 4.0: the page credits it next to the text. Recordings stay on Wikimedia Commons and are credited.

Run:  python3 tools/extract_names.py /path/to/fr-extract.jsonl
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/Sapiopedia/Names/fr-extract.jsonl")
LANGS = {"en": "English", "es": "Spanish", "it": "Italian", "de": "German", "pt": "Portuguese", "nl": "Dutch", "pl": "Polish",
         "ru": "Russian", "el": "Greek", "la": "Latin", "ar": "Arabic", "he": "Hebrew", "zh": "Chinese", "ja": "Japanese",
         "cs": "Czech", "hu": "Hungarian", "sv": "Swedish", "da": "Danish", "nb": "Norwegian", "no": "Norwegian", "fi": "Finnish",
         "ca": "Catalan", "br": "Breton", "eu": "Basque", "co": "Corsican", "oc": "Occitan", "ro": "Romanian", "tr": "Turkish",
         "lt": "Lithuanian", "lv": "Latvian", "ga": "Irish", "cy": "Welsh", "uk": "Ukrainian", "sk": "Slovak", "hr": "Croatian", "sl": "Slovenian"}

ORIG = r"(latin|grec ancien|grec|hébreu|germanique|francique|celte|celtique|gaulois|breton|arabe|anglais|italien|espagnol|basque|occitan|provençal|corse|slave|russe|polonais|scandinave|norrois|danois|suédois|norvégien|irlandais|gaélique|gallois|écossais|persan|turc|sanskrit|hindi|japonais|araméen|égyptien|néerlandais|allemand|portugais|catalan|hongrois|finnois|tchèque|hawaïen|swahili|yoruba|berbère|kabyle|amazigh|vieux haut allemand|ancien français|français)"
ORIG_EN = {"latin": "Latin", "grec ancien": "Ancient Greek", "grec": "Greek", "hébreu": "Hebrew", "germanique": "Germanic", "francique": "Frankish", "celte": "Celtic",
           "celtique": "Celtic", "gaulois": "Gaulish", "breton": "Breton", "arabe": "Arabic", "anglais": "English", "italien": "Italian", "espagnol": "Spanish",
           "basque": "Basque", "occitan": "Occitan", "provençal": "Provençal", "corse": "Corsican", "slave": "Slavic", "russe": "Russian", "polonais": "Polish",
           "scandinave": "Scandinavian", "norrois": "Old Norse", "danois": "Danish", "suédois": "Swedish", "norvégien": "Norwegian", "irlandais": "Irish",
           "gaélique": "Gaelic", "gallois": "Welsh", "écossais": "Scottish", "persan": "Persian", "turc": "Turkish", "sanskrit": "Sanskrit", "hindi": "Hindi",
           "japonais": "Japanese", "araméen": "Aramaic", "égyptien": "Egyptian", "néerlandais": "Dutch", "allemand": "German", "portugais": "Portuguese",
           "catalan": "Catalan", "hongrois": "Hungarian", "finnois": "Finnish", "tchèque": "Czech", "hawaïen": "Hawaiian", "swahili": "Swahili", "yoruba": "Yoruba",
           "berbère": "Berber", "kabyle": "Kabyle", "amazigh": "Amazigh", "vieux haut allemand": "Old High German", "ancien français": "Old French", "français": "French"}

def origin(et):
    """Origin language only when the etymology opens with it ("Du latin…", "De l'hébreu…", "Forme féminine de X, du grec…")."""
    lead = r"(?:Du\s+|De\s+l[’']\s*|Des?\s+|Dérivé\s+du\s+|Issu\s+du\s+|Emprunté\s+au\s+|Emprunt\s+au\s+)"
    m = re.match(r"^\s*(?:\(.*?\)\s*)?" + lead + r"(?:prénom\s+|nom\s+)?" + ORIG + r"\b", et, re.I)
    if not m: m = re.match(r"^[^.]{0,90}?[,;]\s*(?:du\s+|de\s+l[’']\s*|issu\s+du\s+)(?:prénom\s+)?" + ORIG + r"\b", et, re.I)
    return m.group(1).lower() if m else None

def fold(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))

def countries():
    import csv
    p = os.path.join(ROOT, "data", "firstnames.csv")
    if not os.path.exists(p): return {}
    R = list(csv.reader(open(p, encoding="utf-8"), delimiter=";")); head = R[0]; out = {}
    for r in R[1:]:
        if len(r) < 3: continue
        cs = [head[i].replace("Swiss", "Switzerland").replace("the Netherlands", "Netherlands").replace("U.S.A.", "United States") for i in range(2, min(len(r), len(head))) if r[i].strip() and head[i] != "other countries"]
        if cs:
            k = fold(r[0].replace("+", "-"))
            for c in cs:
                if c not in out.setdefault(k, []): out[k].append(c)
    return out

def gender(d):
    t = set(d.get("tags", [])); c = " ".join(d.get("categories", []))
    f = "feminine" in t or "Prénoms féminins en français" in c
    m = "masculine" in t or "Prénoms masculins en français" in c
    if "Prénoms mixtes en français" in c or (f and m): return "n"
    return "f" if f else "m" if m else "u"

# ---------------------------------------------------------------- merging spelling variants
SUBS = [("y", "i"), ("i", "y"), ("k", "c"), ("c", "k"), ("z", "s"), ("s", "z")]

def same_gender(a, b):
    return a == b or "u" in (a, b)

def neighbours(k):
    """Spellings one small step away from k (already folded): a doubled letter, an extra h, a final e, i/y, c/k, s/z."""
    out = set()
    for i in range(len(k)):
        if (i + 1 < len(k) and k[i] == k[i + 1]) or k[i] == "h":
            out.add(k[:i] + k[i + 1:])                       # drop a doubled letter or an h
        for a, b in SUBS:
            if k[i] == a: out.add(k[:i] + b + k[i + 1:])
    for i in range(len(k) + 1):                              # add a doubled letter or an h
        if i > 0: out.add(k[:i] + k[i - 1] + k[i:])
        out.add(k[:i] + "h" + k[i:])
    if k.endswith("e") and len(k) > 2 and k[-2] not in "aeiouy": out.add(k[:-1])   # Anne -> Ann, not Anaé -> Ana
    elif k[-1:] not in "aeiouy": out.add(k + "e")
    out.discard(k)
    return out

def richness(r):
    return sum(1 for f in ("ipa", "mp3", "att", "et", "tr", "der", "c", "q", "pf", "o") if f in r) + len(r.get("tr", {})) / 10

def merge(names):
    """Group names that are accent-only or one-small-step spelling variants (same gender), or declared variants
    ("Variante de X"). Each group becomes one card with pooled information. Index rows: the main spelling plus
    every spelling that differs by more than accents, all pointing to the same card."""
    edges = {w: set() for w in names}
    def link(a, b):
        if a != b and same_gender(names[a]["g"], names[b]["g"]): edges[a].add(b); edges[b].add(a)
    by_fold = {}
    for w in names: by_fold.setdefault(fold(w).replace("œ", "oe").replace("-", " "), []).append(w)
    for ws in by_fold.values():
        for x in ws:
            for y in ws: link(x, y)
    for k, ws in by_fold.items():
        for n in neighbours(k):
            for w2 in by_fold.get(n, []):
                for w in ws: link(w, w2)
    for w, r in names.items():
        for a in r.get("alt", []):
            if a in names: link(w, a)
    # groups: the richest spelling first, then everything within two small steps of it (stops long chains)
    groups, left = [], set(names)
    for w in sorted(names, key=lambda w: (-richness(names[w]), w)):
        if w not in left: continue
        grp, frontier = {w}, {w}
        for _ in range(2):
            frontier = {y for x in frontier for y in edges[x] if y in left and y not in grp}
            grp |= frontier
        left -= grp; groups.append(list(grp))
    groups = {g[0]: g for g in groups}
    det, rows = {}, []
    for members in groups.values():
        main = max(members, key=lambda w: (richness(names[w]), any(ord(ch) > 127 for ch in w), -len(w)))
        rec = dict(names[main])
        for w in members:
            if w == main: continue
            o = names[w]
            for f in ("ipa", "mp3", "by", "acc", "att", "et", "q", "pf", "o", "oe"):
                if f not in rec and f in o: rec[f] = o[f]
            for lang, words in o.get("tr", {}).items():
                cur = rec.setdefault("tr", {}).setdefault(lang, [])
                for x in words:
                    if x not in cur and len(cur) < 4: cur.append(x)
            for f in ("der", "c"):
                for x in o.get(f, []):
                    if x not in rec.setdefault(f, []): rec[f].append(x)
            if rec["g"] == "u": rec["g"] = o["g"]
        rec.pop("alt", None)
        shown = [main] + sorted({w for w in members if w != main and fold(w) != fold(main)}, key=str.lower)
        if len(members) > 1: rec["v"] = [w for w in sorted(members, key=str.lower) if w != main]
        det[main] = rec
        for w in shown: rows.append([w, rec["g"], 1 if "mp3" in rec else 0, main])
    rows.sort(key=lambda r: (fold(r[0]), r[0]))
    det = dict(sorted(det.items(), key=lambda kv: fold(kv[0])))
    print(f"merged {len(names)} spellings into {len(det)} cards; index shows {len(rows)} names")
    return det, rows

def main():
    lines = subprocess.run(["grep", "-F", '"pos_title": "Prénom"', SRC], capture_output=True, text=True, env={**os.environ, "LC_ALL": "C"}).stdout.splitlines()
    names = {}; C = countries()
    for l in lines:
        d = json.loads(l)
        if d.get("lang_code") != "fr": continue
        w = d["word"].strip()
        if not w or w in names: continue
        rec = {"g": gender(d)}
        ipa = next((s["ipa"] for s in d.get("sounds", []) if s.get("ipa", "").startswith("\\")), None) or next((s["ipa"] for s in d.get("sounds", []) if s.get("ipa")), None)
        if ipa: rec["ipa"] = ipa
        snd = next((s for s in d.get("sounds", []) if s.get("mp3_url")), None)
        if snd:
            rec["mp3"] = snd["mp3_url"]
            m = re.match(r"LL-Q\d+ \([a-z]+\)-([^-]+)-", snd.get("audio", ""))
            rec["by"] = m.group(1) if m else "Wikimedia Commons"
            if snd.get("raw_tags"): rec["acc"] = snd["raw_tags"][0]
        att = next((a.get("date") for a in d.get("attestations", []) if a.get("date")), None)
        if att: rec["att"] = att
        tr = {}
        for t in d.get("translations", []):
            lc, word = t.get("lang_code"), t.get("word")
            if lc in LANGS and word and word != w:
                tr.setdefault(LANGS[lc], [])
                if word not in tr[LANGS[lc]] and len(tr[LANGS[lc]]) < 3: tr[LANGS[lc]].append(word)
        if tr: rec["tr"] = dict(list(tr.items())[:14])
        der = [x["word"] for x in d.get("derived", []) if x.get("word") and "-" in x["word"]][:8]
        if der: rec["der"] = der
        if d.get("etymology_texts"):
            et = " ".join(d["etymology_texts"]).strip()
            if len(et) > 8 and not re.search(r"Étymologie manquante|ajouter en cliquant", et):
                et = re.sub(r"\b([Nn]om|[Pp]rénom|[Mm]ot|[Tt]oponyme|ou)(composé|dérivé)", r"\1 \2", et)  # the dump glues these words
                rec["et"] = et[:700]
                o = origin(et)
                if o: rec["o"] = o; rec["oe"] = ORIG_EN.get(o, o.capitalize())
        for sn in d.get("senses", []):
            for ex in sn.get("examples", []):
                y = re.findall(r"\b(1[0-9]{3})\b", ex.get("ref", ""))
                if ex.get("text") and y and int(y[-1]) <= 1925 and 20 < len(ex["text"]) < 420:
                    rec["q"] = [ex["text"], ex["ref"]]; break
            if "q" in rec: break
        for n in d.get("notes", []):
            f = re.search(r"([\d\s\u202f\u00a0.]+)\s*\S*\s*au féminin", n); m_ = re.search(r"([\d\s\u202f\u00a0.]+)\s*\S*\s*au masculin", n)
            if f and m_:
                fv = int(re.sub(r"\D", "", f.group(1)) or 0); mv = int(re.sub(r"\D", "", m_.group(1)) or 0)
                if fv + mv > 0: rec["pf"] = round(100 * fv / (fv + mv))
        alt = [a["word"] for sn in d.get("senses", []) for a in sn.get("alt_of", []) if a.get("word")]
        if alt: rec["alt"] = alt
        cs = C.get(fold(w))
        if cs: rec["c"] = cs[:10]
        names[w] = rec
    det, index_rows = merge(names)
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    json.dump(det, open(os.path.join(ROOT, "assets", "names-fr.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(index_rows, open(os.path.join(ROOT, "data", "names_fr_list.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    from collections import Counter
    print(len(det), "cards;", Counter(r["g"] for r in det.values()), "; with recording:", sum("mp3" in r for r in det.values()),
          "; origins:", Counter(r.get("o") for r in det.values()).most_common(8))

if __name__ == "__main__":
    main()
