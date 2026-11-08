#!/usr/bin/env python3
"""Parse the EN and FR dream dictionaries (data/dreams/dreams_*.txt) into data/dreams_en.json and data/dreams_fr.json.

Each file: an intro, entries grouped under letter headers, then an index ("INDEX OF WORDS COVERED")
whose headwords follow the same order as the entries and whose "x → see Y" lines are aliases.

Writes review files:
  data/dreams_unresolved_related.csv  related-dream names that match no entry or alias (kept as plain text)
  data/dreams_unmatched.csv           entries and index headwords that could not be paired
  data/dreams_polarity.csv            the good / mixed / bad sign given to every situation (keyword rules, for review)
Run:  python3 tools/parse_dreams.py
"""
import csv, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = {
    "en": dict(file="dreams_en.txt", one="In one sentence", tone="Tone:", sit="Depending on what happens in the dream",
               feel="Depending on how you felt", q="Questions to ask yourself", rel="Related dreams:", ref="References:",
               index="INDEX OF WORDS COVERED", see="→ see"),
    "fr": dict(file="dreams_fr.txt", one="En une phrase", tone="Tonalité :", sit="Selon ce qui se passe dans le rêve",
               feel="Selon ce que vous ressentiez", q="Questions à se poser", rel="Rêves proches :", ref="Références :",
               index="INDEX DES MOTS COUVERTS", see="→ voir"),
}

def norm(s):
    s = s.lower().replace("œ", "oe").replace("æ", "ae").replace("ß", "ss").replace("’", "'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def slugify(s):
    return norm(s).replace(" ", "-") or "x"

# keyword rules for the sign of a situation (checked on the meaning, after the colon)
POS = {
    "en": r"\b(success|succeed|happ(y|iness)|joy|good (luck|news|fortune|health)|luck|prosper|wealth|rich|gain|profit|victor|win|triumph|love|marriage|pleasant|pleasure|favou?r|honou?r|reward|recover|peace|content|harmony|promotion|advance|delight|friend(ly|s|ship)? (help|support)|fortune smiles|thriv|abundan|comfort|well-being|a happy sign|bright|promis|blessing|inherit|safe|secur|improv|rise|outwit|overcome|escape)\w*",
    "fr": r"\b(succès|réuss|bonheur|heureu|joie|chance|prospér|richesse|riche|gain|profit|victoire|vainc|triomph|amour|mariage|agréable|plaisir|faveur|honneur|récompense|guéri|rétabli|paix|content|harmonie|promotion|avancement|délice|aisance|abondan|confort|bien-être|bon signe|promet|bénédiction|héritage|sécurité|améliora|surmont|échapp|déjouer?|déjouer)\w*",
}
NEG = {
    "en": r"\b(loss|lose|losing|lost|trouble|ill(ness)?|sick|disease|enem|quarrel|death|die|dying|misfortune|sorrow|grief|fail|danger|poverty|poor|debt|worr|anxi|disappoint|deceit|deceiv|betray|slander|gossip|scandal|jealous|disgrace|shame|setback|obstacle|accident|injur|pain|sad|unhapp|bad news|bad luck|bad influence|ruin|decline|hostil|treacher|false|deception|misery|hardship|tears|mercy of|threat|warn|beware|fear|vex|annoy|thwart|suffer|unfortunate|unlucky|evil|harm|trick|dishonest|cheat|rival|conflict|dispute)\w*",
    "fr": r"\b(perte|perdr|perdu|ennui|malad|ennemi|querelle|dispute|mort|mourir|malheur|chagrin|peine|échec|échou|danger|pauvreté|pauvre|dette|souci|inquiét|angoiss|déception|déçu|tromp|trahi|calomni|médisance|commérage|scandale|jalous|disgrâce|honte|revers|obstacle|accident|blessure|douleur|triste|mauvaise nouvelle|malchance|mauvaise influence|ruine|déclin|hostil|perfid|faux|fausse|misère|difficulté|larmes|merci de|menace|méfie|prudence|peur|contrari|souffr|malheureu|mal\b|nuire|nuisible|rival|conflit|ennemis)\w*",
}

WIN = {"en": r"\b(victor|triumph|overcome|outwit|defeat|conquer|escape|win over|get the better)\w*",
       "fr": r"\b(victoire|triomph|vaincr|vainqu|surmont|déjou|échapp|l'emporter|prendre le dessus)\w*"}

def raw_key(title):
    """The dream word in its original spelling: 'Dreaming of an Abbess' -> 'Abbess', "Rêver d'un œuf" -> 'Œuf'."""
    t = re.sub(r"^(Dreaming of|Rêver)\s+", "", title.replace("’", "'"))
    t = re.sub(r"^((an|a|the|some|your|un|une|le|la|les|des|du|de|d'|l'|être|avoir|d'être|d'avoir)\s*)+", "", t, flags=re.I)
    t = t.strip()
    return t[:1].upper() + t[1:]

def polarity(lang, text):
    t = text.lower()
    if re.search(WIN[lang], t) and not re.search(r"\b(not|never|fail|ne |pas |jamais|échou)", t): return "up"
    p = len(re.findall(POS[lang], t)); n = len(re.findall(NEG[lang], t))
    # "unless ..." / "sauf si ..." flips nothing but softens: treat as mixed when both appear
    if p and not n: return "up"
    if n and not p: return "down"
    if p and n: return "up" if p > n + 1 else "down" if n > p + 1 else "mid"
    return "mid"

def parse(lang):
    c = CFG[lang]
    L = open(os.path.join(ROOT, "data", "dreams", c["file"]), encoding="utf-8").read().replace("\u00a0", " ").replace("\u202f", " ").split("\n")
    idx_at = next(i for i, l in enumerate(L) if l.strip() == c["index"])
    body, index = L[:idx_at], L[idx_at + 1:]
    # intro = everything before the first letter header
    first = next(i for i, l in enumerate(body) if re.match(r"^—+\s+\S\s+—+$", l.strip()))
    intro = [p.replace("\n", " ").strip() for p in "\n".join(body[1:first]).split("\n\n") if p.strip() and not set(p.strip()) <= set("=")]
    # entries
    starts = [i for i in range(len(body) - 1) if body[i].strip() and body[i + 1].startswith("───")]
    hdr, cur = {}, "#"
    for i, l in enumerate(body):
        m = re.match(r"^—+\s+(\S)\s+—+$", l.strip())
        if m: cur = m.group(1).upper()
        hdr[i] = cur
    entries = []
    for k, s in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(body)
        block = [l for l in body[s + 2:end] if not re.match(r"^—+\s+\S\s+—+$", l.strip())]
        e = {"section": hdr[s], "title": body[s].strip(), "one": "", "tone": 0, "tone_label": "", "situations": [], "feelings": [], "questions": [], "related": [], "refs": ""}
        sec, buf = None, []
        def para(lines):
            return " ".join(x.strip() for x in lines).strip()
        def bullets(lines):
            out = []
            for x in lines:
                if x.startswith("•"): out.append(x[1:].strip())
                elif x.startswith("  ") and out: out[-1] += " " + x.strip()
            return out
        def flush():
            nonlocal buf
            if sec == "one": e["one"] = para(buf)
            elif sec in ("situations", "feelings", "questions"): e[sec] = bullets(buf)
            buf = []
        i = 0
        while i < len(block):
            l = block[i]; st = l.strip()
            heads = {c["one"]: "one", c["sit"]: "situations", c["feel"]: "feelings", c["q"]: "questions"}
            if st in heads: flush(); sec = heads[st]; i += 1; continue
            for key, field in ((c["tone"], "tone"), (c["rel"], "related"), (c["ref"], "refs")):
                if st.startswith(key):
                    flush(); sec = None
                    txt = [st[len(key):].strip()]; i += 1
                    while i < len(block) and block[i].strip(): txt.append(block[i].strip()); i += 1
                    t = " ".join(txt)
                    if field == "tone":
                        m = re.match(r"([●○]+)\s*(.*)", t); e["tone"] = m.group(1).count("●") if m else 0; e["tone_label"] = m.group(2).strip() if m else t
                    elif field == "related":
                        e["related"] = [x.strip() for x in re.split(r"\s+·\s+", t) if x.strip()]
                    else:
                        e["refs"] = t
                    break
            else:
                buf.append(l); i += 1
        flush()
        def split_lead(x):
            m = re.match(r"^(.{2,90}?)\s?:\s+(.+)$", x)
            return [m.group(1).strip(), m.group(2).strip()] if m else ["", x]
        e["situations"] = [split_lead(x) for x in e["situations"]]
        e["feelings"] = [split_lead(x) for x in e["feelings"]]
        entries.append(e)
    # index: headwords in entry order + aliases
    heads, aliases = [], []
    for l in index:
        st = l.strip()
        if not st or set(st) <= set("=") or re.match(r"^—\s*\S+\s*—$", st): continue
        if c["see"] in st:
            a, b = st.split(c["see"], 1); aliases.append((a.strip(), b.strip()))
        else:
            heads.append(st)
    # the French file keeps Œ words (œil, œuf…) in their own section after Z: file them under O
    for e in entries:
        if e["section"] == "Œ": e["section"] = "O"
    entries.sort(key=lambda e: e["section"])  # stable: Œ words follow the other O words
    # pair entries with headwords: both lists are alphabetical, so walk them together and match by stem
    def key(t):
        return re.sub(r"^(dreaming of|reve[r]? (de|d|du|des)|reve[r]?)\s+((an?|the|some|un|une|le|la|les|l|d|de|des|du|etre|avoir)\s+)*", "", norm(t))
    def close(a, b):
        a, b = a.replace(" ", ""), b.replace(" ", "")
        if a == b: return True
        n = 0
        while n < min(len(a), len(b)) and a[n] == b[n]: n += 1
        return n >= max(4, int(min(len(a), len(b)) * .7))
    def close_any(k, h0):
        raw = heads_raw.get(h0, h0)
        m = re.match(r"^(.*?)\s*\((.*)\)\s*$", raw)
        cands = [h0] + ([norm(m.group(1)), norm(m.group(2))] if m else [])
        return any(close_one(k, h) for h in cands if h)
    def close_one(k, h):
        if close(k, h): return True
        toks = k.split(); n = len(h.split())
        return any(close(" ".join(toks[i:i + n]), h) for i in range(len(toks)))
    heads_raw = {norm(h): h for h in heads}
    pairs, j, unmatched = [], 0, []
    for e in entries:
        k = key(e["title"]); hit = None
        for d in range(0, 6):
            if j + d < len(heads) and close_any(k, norm(heads[j + d])): hit = j + d; break
        if hit is None: pairs.append(None); unmatched.append(e["title"])
        else: pairs.append(heads[hit]); j = hit + 1
    # second pass: an unpaired entry takes an unused headword that matches it exactly, wherever it sits
    free = {norm(h): h for h in heads if h not in {p for p in pairs if p}}
    for n_, (e, h) in enumerate(zip(entries, pairs)):
        if h is None:
            k = key(e["title"]).replace(" ", "")
            hit = next((h2 for nk, h2 in free.items() if nk.replace(" ", "") == k), None)
            if hit: pairs[n_] = hit; free.pop(norm(hit)); unmatched.remove(e["title"])
    paired_heads = {h for h in pairs if h}
    orphan_heads = [h for h in heads if h not in paired_heads]
    used = {}
    for e, h in zip(entries, pairs):
        w = h or raw_key(e["title"])
        pm = re.match(r"^(.*?)\s*\((.*)\)\s*$", w)
        if pm: w = pm.group(2) if close_one(key(e["title"]), norm(pm.group(2))) else pm.group(1)
        e["word"] = w.capitalize() if w.isupper() else w
        s = slugify(w); n = used.get(s, 0); used[s] = n + 1
        e["id"] = s if not n else f"{s}-{n + 1}"
        e["aliases"] = []
        e["letter"] = e.pop("section")
    heads_by_entry = [(e, h or e["word"]) for e, h in zip(entries, pairs)]
    from collections import Counter
    dup = Counter(norm(e["word"]) for e in entries)
    for e in entries:
        if dup[norm(e["word"])] > 1:
            k = raw_key(e["title"]); e["word"] = k[:1].upper() + k[1:] if k else e["word"]
    by_head = {norm(h): e for e, h in heads_by_entry}
    for e in entries: by_head.setdefault(norm(e["word"]), e)
    unresolved_alias, alias_list = [], []
    for a, b in aliases:
        targets = [x.strip() for x in re.split(r",\s*(?![^()]*\))", b) if x.strip()]
        ids = []
        for tname in targets:
            t = by_head.get(norm(tname)) or by_head.get(norm(re.sub(r"\(.*?\)", "", tname)))
            if not t:
                pm = re.search(r"\((.*?)\)", tname); t = by_head.get(norm(pm.group(1))) if pm else None
            if t:
                if a not in t["aliases"]: t["aliases"].append(a)
                if t["id"] not in ids: ids.append(t["id"])
            else: unresolved_alias.append((a, tname))
        if ids: alias_list.append([a, ids])
    # look-up for related names: headword, title word, alias
    look = dict(by_head)
    for e in entries:
        tw = re.sub(r"^(dreaming of|reve[r]? (de|d|du|des)|reve[r]?)\s+(an?|the|some|un|une|le|la|les|l|d|de|des|du|etre|avoir)?\s*", "", norm(e["title"]))
        look.setdefault(tw, e)
        for a in e["aliases"]: look.setdefault(norm(a), e)
    unresolved = []
    for e in entries:
        rel = []
        for r in e["related"]:
            t = look.get(norm(r)) or look.get(norm(re.sub(r"\(.*?\)", "", r)))
            if t and t is not e: rel.append([r, t["id"]])
            else: rel.append([r, None]); unresolved.append((e["id"], r))
        e["related"] = rel
        for s in e["situations"]: s.append(polarity(lang, s[1] or s[0]))
        order = {"up": 0, "mid": 1, "down": 2}
        e["situations"].sort(key=lambda s: order[s[2]])
    return {"intro": intro, "entries": entries, "aliases": alias_list}, aliases, unresolved_alias, unresolved, unmatched, orphan_heads

def main():
    rep = []
    with open(os.path.join(ROOT, "data", "dreams_unresolved_related.csv"), "w", newline="", encoding="utf-8") as fu, \
         open(os.path.join(ROOT, "data", "dreams_polarity.csv"), "w", newline="", encoding="utf-8") as fp, \
         open(os.path.join(ROOT, "data", "dreams_unmatched.csv"), "w", newline="", encoding="utf-8") as fm:
        wu, wp, wm = csv.writer(fu), csv.writer(fp), csv.writer(fm)
        wm.writerow(["lang", "problem", "text"])
        wu.writerow(["lang", "entry", "related_name"]); wp.writerow(["lang", "entry", "situation", "meaning", "sign"])
        for lang in ("en", "fr"):
            data, aliases, ua, unresolved, unmatched, orphans = parse(lang)
            for t in unmatched: wm.writerow([lang, "entry without index headword", t])
            for h in orphans: wm.writerow([lang, "index headword without entry", h])
            json.dump(data, open(os.path.join(ROOT, "data", f"dreams_{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
            for eid, r in unresolved: wu.writerow([lang, eid, r])
            for a, b in ua: wu.writerow([lang, "(alias) " + a, b])
            sig = {"up": 0, "mid": 0, "down": 0}
            for e in data["entries"]:
                for s in e["situations"]: wp.writerow([lang, e["id"], s[0], s[1], s[2]]); sig[s[2]] += 1
            rep.append(f"{lang.upper()}: {len(data['entries'])} entries, {len(aliases)} aliases ({len(ua)} unresolved), "
                       f"{len(unmatched)} entries without headword, {len(orphans)} headwords without entry, "
                       f"{sum(len(e['related']) for e in data['entries'])} related links ({len(unresolved)} unresolved), "
                       f"signs up/mixed/down = {sig['up']}/{sig['mid']}/{sig['down']}")
    print("\n".join(rep))

if __name__ == "__main__":
    main()
