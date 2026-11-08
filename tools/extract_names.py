#!/usr/bin/env python3
"""Extract French first names from the French Wiktionary dump (kaikki/wiktextract fr-extract.jsonl)
into assets/names-fr.json (details, loaded by the page) and data/names_fr_list.json (name + gender, used by the build).

Only facts are kept (gender, pronunciation, recording, first record, forms in other languages, compound names):
Wiktionnaire's prose is CC BY-SA, so etymology text is not copied. Recordings stay on Wikimedia Commons and are credited.

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

def gender(d):
    t = set(d.get("tags", [])); c = " ".join(d.get("categories", []))
    f = "feminine" in t or "Prénoms féminins en français" in c
    m = "masculine" in t or "Prénoms masculins en français" in c
    if "Prénoms mixtes en français" in c or (f and m): return "n"
    return "f" if f else "m" if m else "u"

def main():
    lines = subprocess.run(["grep", "-F", '"pos_title": "Prénom"', SRC], capture_output=True, text=True, env={**os.environ, "LC_ALL": "C"}).stdout.splitlines()
    names = {}
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
            m = re.search(r"\b(latin|grec|hébreu|germanique|celte|celtique|arabe|breton|anglais|italien|espagnol|basque|occitan|slave|russe|scandinave|norrois|gaulois|provençal|corse|irlandais|gaélique|persan|turc|sanskrit|hindi|japonais|araméen|égyptien)\b", d["etymology_texts"][0], re.I)
            if m: rec["o"] = m.group(1).lower()
        names[w] = rec
    det = dict(sorted(names.items(), key=lambda kv: kv[0].lower()))
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    json.dump(det, open(os.path.join(ROOT, "assets", "names-fr.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump([[w, r["g"], 1 if "mp3" in r else 0] for w, r in det.items()], open(os.path.join(ROOT, "data", "names_fr_list.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    from collections import Counter
    print(len(det), "names;", Counter(r["g"] for r in det.values()), "; with recording:", sum("mp3" in r for r in det.values()),
          "; origins:", Counter(r.get("o") for r in det.values()).most_common(8))

if __name__ == "__main__":
    main()
