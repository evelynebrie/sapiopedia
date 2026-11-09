#!/usr/bin/env python3
"""Add English etymologies to the French names cards (assets/names-fr.json, field "ete"), taken from the English
Wiktionary dump (kaikki raw-wiktextract-data.jsonl.gz). The English site shows "ete"; without it, the origin section
is left out on the English site rather than shown in French. Run after tools/extract_names.py:

  python3 tools/add_english_etymology.py ~/Desktop/Sapiopedia/Names/raw-wiktextract-data.jsonl.gz
"""
import gzip, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/Sapiopedia/Names/raw-wiktextract-data.jsonl.gz")

def clean(et):
    lines = [l.strip() for l in et.replace("\r", "").split("\n") if l.strip()]
    if lines and lines[0].lower().startswith("etymology tree"):
        lines = lines[1:]
        while lines and "." not in lines[0] and len(lines[0]) < 70: lines = lines[1:]   # the tree's node list
    t = " ".join(re.sub(r"^:\s*", "", l) for l in lines)
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) > 12 and "." in t or len(t) > 25 else ""

def is_given_name(d):
    blob = json.dumps(d.get("senses", [])[:3])[:4000] + " ".join(d.get("categories", []))
    return "given name" in blob

def main():
    path = os.path.join(ROOT, "assets", "names-fr.json")
    cards = json.load(open(path, encoding="utf-8"))
    want = set(cards) | {v for r in cards.values() for v in r.get("v", [])}
    proc = subprocess.Popen(f"gzip -dc '{SRC}' | LC_ALL=C grep -F '\"pos\": \"name\"'", shell=True, stdout=subprocess.PIPE)
    fr, en = {}, {}
    for raw in proc.stdout:
        d = json.loads(raw)
        w = d.get("word")
        if w not in want or d.get("lang_code") not in ("fr", "en") or not is_given_name(d): continue
        t = clean(d.get("etymology_text") or "")
        if not t: continue
        (fr if d["lang_code"] == "fr" else en).setdefault(w, t)
    n = 0
    for w, r in cards.items():
        r.pop("ete", None)
        names = [w] + r.get("v", [])
        t = next((fr[x] for x in names if x in fr), None) or next((en[x] for x in names if x in en and not re.match(r"^From French [^.()“]+\.?$", en[x])), None)
        if t and not re.match(r"^From French [^.()“]+\.?$", t): r["ete"] = t[:700]; n += 1
    json.dump(cards, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{n} of {len(cards)} cards have an English etymology ({len(fr)} from French-name entries, {len(en)} English entries found)")

if __name__ == "__main__":
    main()
