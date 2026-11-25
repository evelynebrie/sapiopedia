#!/usr/bin/env python3
"""Middle-name and sibling matching for the French and German name books.

1. A profile per name card: syllables, first and last sounds, gender, origin, style tags, real pairings
   (the compound names families actually use, e.g. Marie-Alice), variant group.
2. A score per pair (same rules as assets/name-finder.js, which runs them in the browser):
   middle name  + different lengths, - two long names, - rhyming endings, - ending sound = next starting sound,
                + shared style, + the pair exists as a real compound name, + a known name
   sibling      + shared style and origin, - same first letter, - same ending, - near-identical spelling (Léo/Théo),
                - very different popularity
3. Writes
   assets/names-match.json       compact profiles for the tool page (all names; suggestions come from the "pool")
   data/names_pairs.json         8 middle names + 8 siblings (4 + 4) for every card, shown on the name pages
   data/names_middle_pages.json  the most-known names: 40 middle names in 4 groups, for the dedicated pages
Needs numpy; run locally after tools/extract_names*.py:  python3 tools/name_matching.py
"""
import json, os, re, unicodedata
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = ("fr", "de")
STYLES = ["short", "classic", "rare", "vintage", "nature", "mythological", "biblical", "international", "modern"]
INSEE = os.path.expanduser("~/Library/CloudStorage/Dropbox/Sapiopedia/Names/insee_nat2021.csv")   # births per first name and year in France, 1900-2021 (INSEE)

def insee():
    """fold(name) -> (births, peak decade, share born since 2000) from the INSEE national file; {} if absent."""
    if not os.path.exists(INSEE): return {}
    acc = {}
    for line in open(INSEE, encoding="utf-8").read().splitlines()[1:]:
        sexe, nm, yr, n = line.split(";")
        if nm.startswith("_") or not yr.isdigit(): continue
        d = acc.setdefault(fold(nm), {}); dec = int(yr) // 10 * 10; d[dec] = d.get(dec, 0) + int(n)
    out = {}
    for k, d in acc.items():
        tot = sum(d.values()); out[k] = (tot, max(d, key=d.get), sum(v for y, v in d.items() if y >= 2000) / tot)
    return out
OLD = {"Old High German", "Germanic", "Old Norse", "Frankish", "Old French", "Low German", "Old Saxon", "Middle High German", "Gaulish", "Celtic"}
NATURE = r"\b(flower|rose|lily|violet|daisy|jasmine|iris|laurel|olive|tree|oak|forest|wood|sea|river|ocean|wave|star|sun|moon|sky|dawn|bird|dove|wolf|bear|lion|pearl|stone|spring|leaf|fleur|lis|arbre|chêne|forêt|mer|rivière|étoile|soleil|lune|ciel|aube|oiseau|colombe|loup|ours|perle|pierre|printemps|feuille)\b"
MYTH = r"(mytholog|goddess|\bgod\b|nymph|muse|déesse|nymphe|\bdieu\b)"
BIBLE = r"(biblical|\bbible|old testament|new testament|apostle|prophet|biblique|apôtre|prophète)"

def fold(s): return "".join(c for c in unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("æ", "ae")) if not unicodedata.combining(c))

def syllables(name, ipa, book):
    if ipa and book == "fr" and ipa.startswith("\\") and "." in ipa: return ipa.count(".") + 1
    w = fold(name).replace("-", " ")
    if book == "fr": w = re.sub(r"(?<=[^aeiouy])e\b", "", w)            # silent final e: Alice = 2
    n = len(re.findall(r"[aeiouy]+", w))
    return max(1, n)

def sounds(name, book):
    """(start, end) as rough sound keys from the spelling: Alice -> ('a', 'is'), Céleste -> ('s', 'est'), Léa -> ('l', 'a')."""
    w = fold(name).split("-")[0]
    s = w[:2]
    start = "s" if re.match(r"c[eiy]", w) else "f" if w.startswith("ph") else (w[1:2] if w.startswith("h") and book == "fr" else w[:1]) or w[:1]
    e = fold(name).split("-")[-1]
    if book == "fr":
        e = re.sub(r"(?<=[^aeiouy])e$", "", e); e = re.sub(r"(?<=[aeiouy])[stdxz]$", "", e) if len(e) > 3 else e
        e = e.replace("ce", "s").replace("c", "k") if e.endswith("c") else e.replace("ce", "s")
    m = re.search(r"[aeiouy]+[^aeiouy]*$", e)
    return start, (m.group(0) if m else e[-2:])

def lev(a, b):
    if abs(len(a) - len(b)) > 2: return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def main():
    rec, idx = [], {}; IN = insee()
    for book in BOOKS:
        D = json.load(open(os.path.join(ROOT, "assets", f"names-{book}.json"), encoding="utf-8"))
        rows = json.load(open(os.path.join(ROOT, "data", f"names_{book}_list.json"), encoding="utf-8"))
        import importlib.util, sys; sys.path.insert(0, ROOT)
        from content.names_fr import card_slugs
        slugs = card_slugs(book)[0]
        for main_, r in D.items():
            pop = len(r.get("c", [])) + len(r.get("tr", {})) + 3 * bool(r.get("mp3")) + 2 * bool(r.get("ete")) + 2 * bool(r.get("ipa"))
            txt = " ".join([r.get("ete", ""), r.get("et", "")]).lower()
            st, en = sounds(main_, book)
            c = set(r.get("c", []))
            tags = set()
            if len(main_) <= 4 or syllables(main_, r.get("ipa"), book) == 1: tags.add("short")
            if r.get("oe") in OLD: tags.add("vintage")
            if re.search(NATURE, txt): tags.add("nature")
            if re.search(MYTH, txt): tags.add("mythological")
            if r.get("oe") in ("Hebrew", "Aramaic") or re.search(BIBLE, txt): tags.add("biblical")
            eng = {fold(x) for x in r.get("tr", {}).get("English", [])}
            if fold(main_) in eng or (c & {"Great Britain", "United States", "Ireland"} and c & {"France", "Belgium", "Germany", "Austria", "Switzerland"}): tags.add("international")
            births, peak, recent = IN.get(fold(main_), (0, 0, 0)) if book == "fr" else (0, 0, 0)
            if births:   # real eras for French names
                if peak <= 1950 and recent < .2: tags.add("vintage")
                if peak >= 2000: tags.add("modern")
            rec.append(dict(births=births, peak=peak, book=book, name=main_, slug=slugs[main_], g=r["g"], syl=syllables(main_, r.get("ipa"), book), st=st, en=en, f=fold(main_),
                            o=r.get("oe", ""), pop=pop, tags=tags, var=set(map(fold, r.get("v", []) + r.get("vf", []) + r.get("nick", []))), comp="-" in main_))
            idx[(book, main_)] = len(rec) - 1
    # popularity tiers inside each book: classic = top 15 %, rare = bottom 40 %
    for book in BOOKS:
        pops = sorted(x["pop"] for x in rec if x["book"] == book)
        hi, lo = pops[int(len(pops) * .85)], pops[int(len(pops) * .40)]
        for x in rec:
            if x["book"] != book: continue
            if x["births"]:   # French: popularity = births in France since 1900
                x["pop"] = round(np.log10(1 + x["births"]) * 4)
                if x["births"] >= 50000: x["tags"].add("classic")
                if x["births"] < 1000: x["tags"].add("rare")
                x["pool"] = (not x["comp"]) and x["g"] in "fmn" and x["births"] >= 300
                continue
            if x["pop"] >= hi: x["tags"].add("classic")
            if x["pop"] <= lo: x["tags"].add("rare")
            x["pool"] = (not x["comp"]) and x["g"] in "fmn" and x["pop"] >= max(lo + 1, 4) and x["book"] == "de"
    # real pairings from compound names (Marie-Alice: Marie <-> Alice), by folded name inside each book
    by_fold = {(x["book"], x["f"]): i for i, x in enumerate(rec)}
    pairs = {}
    for book in BOOKS:
        for r in json.load(open(os.path.join(ROOT, "data", f"names_{book}_list.json"), encoding="utf-8")):
            parts = [p for p in r[0].split("-") if p]
            if len(parts) == 2:
                a, b = by_fold.get((book, fold(parts[0]))), by_fold.get((book, fold(parts[1])))
                if a is not None and b is not None and a != b: pairs.setdefault(a, set()).add(b); pairs.setdefault(b, set()).add(a)
    # vectors
    N = len(rec); syl = np.array([x["syl"] for x in rec]); pop = np.array([x["pop"] for x in rec], float)
    popn = np.zeros(N)   # popularity as a rank inside each book (0-1), so French and German names compare fairly
    for b in BOOKS:
        ix = np.array([k for k, x in enumerate(rec) if x["book"] == b]); r = np.argsort(np.argsort(pop[ix])); popn[ix] = r / max(1, len(ix) - 1)
    T = np.array([[t in x["tags"] for t in STYLES] for x in rec], float)
    book = np.array([x["book"] for x in rec]); g = np.array([x["g"] for x in rec]); pool = np.array([x["pool"] for x in rec])
    cand = np.array([(not x["comp"]) and x["g"] in "fmn" for x in rec])   # suggestions come from the whole database, French and German alike
    en = np.array([x["en"] for x in rec]); st = np.array([x["st"] for x in rec]); first = np.array([x["f"][:1] for x in rec])
    org = np.array([x["o"] for x in rec]); ends_cons = np.array([x["en"][-1:] for x in rec])
    style_w = np.array([0.5, 1, 1, 1.5, 1.5, 1.5, 1.5, 1, 1.5])           # how much a shared tag counts
    peak = np.array([x["peak"] for x in rec], float); has_era = peak > 0

    def near(i, js):
        a = rec[i]["f"]; return np.array([lev(a, rec[j]["f"]) <= 2 or rec[j]["f"] in rec[i]["var"] or a in rec[j]["var"] or rec[j]["f"].startswith(a[:4]) and len(a) >= 4
                         or rec[j]["f"].startswith(a) or a.startswith(rec[j]["f"]) for j in js], dtype=bool)   # Léo / Léonard

    def middle(i, k=8, same_book=True):
        x = rec[i]; real_m = np.zeros(N, bool); real_m[list(pairs.get(i, ()))] = True
        m = cand & (np.arange(N) != i) & ((g == x["g"]) | (x["g"] == "n") | real_m)   # same gender, unless families really combine them (Jean-Marie)
        js = np.nonzero(m)[0]
        s = np.zeros(len(js)); r = [[] for _ in js]
        d = syl[js] != x["syl"]; s += 2 * d
        s -= 2 * ((syl[js] + x["syl"]) >= 6)
        rhyme = en[js] == x["en"]; s -= 3 * rhyme
        clash = (st[js] == ends_cons[i]) & (np.char.str_len(st[js]) > 0); s -= 2 * clash
        shared = T[js] @ (T[i] * style_w); s += np.minimum(shared, 3)
        real = np.array([j in pairs.get(i, ()) for j in js]); s += 4 * real
        s += popn[js] - 2 * ~pool[js]                                      # every name can come up, known names first
        s += 0.5 * ((org[js] == x["o"]) & (org[js] != ""))
        top = np.argsort(-s)[:k * 4 + 40]                                   # near-duplicates (Léo/Théo) are checked on the best ones only: fast
        keep = top[~near(i, js[top])]
        seen = set(); order = [j for j in js[keep] if not (rec[j]["f"] in seen or seen.add(rec[j]["f"]))][:k]   # same name in both lists: once
        out = []
        for j in order:
            why = []
            if j in pairs.get(i, ()): why.append("pair")
            if syl[j] != x["syl"]: why.append("flow")
            common = [STYLES[t] for t in range(len(STYLES)) if T[i, t] and T[j, t] and STYLES[t] not in ("rare",)]
            if common: why.append("style:" + common[0])
            out.append([rec[j]["book"], rec[j]["name"], rec[j]["slug"], why])
        return out

    def sibling(i, gender, k=4):
        x = rec[i]; m = cand & (np.arange(N) != i) & (g == gender)
        js = np.nonzero(m)[0]
        s = np.minimum(T[js] @ (T[i] * style_w), 3) * 1.5
        s += 1.5 * ((org[js] == x["o"]) & (org[js] != ""))
        s -= 2 * (first[js] == first[i]); s -= 2 * (en[js] == x["en"])
        s -= 3 * np.abs(popn[js] - popn[i])
        if has_era[i]: s -= np.where(has_era[js], np.abs(peak[js] - peak[i]) / 10, 3) * 1.2   # same era: a brother for Léo is not a Roger
        s += popn[js] - 3 * ~pool[js]
        if not has_era[i]:   # no era to compare (German names): a name from the other list must share a real style
            real_style = T[js] @ (T[i] * (style_w * np.array([1, 1, 0, 1, 1, 1, 1, 0, 1])))
            s -= 6 * ((book[js] != x["book"]) & (real_style == 0))
        top = np.argsort(-s)[:k * 4 + 40]; seen = set()
        order = [j for j in js[top[~near(i, js[top])]] if not (rec[j]["f"] in seen or seen.add(rec[j]["f"]))][:k]
        out = []
        for j in order:
            why = []
            common = [STYLES[t] for t in range(len(STYLES)) if T[i, t] and T[j, t]]
            if common: why.append("style:" + common[0])
            if rec[j]["o"] and rec[j]["o"] == x["o"]: why.append("origin")
            why.append("distinct")
            out.append([rec[j]["book"], rec[j]["name"], rec[j]["slug"], why])
        return out

    P = {}
    for i, x in enumerate(rec):
        if x["comp"]: continue
        sib = sibling(i, "f") + sibling(i, "m") if x["g"] in "fmn" else []
        P[f'{x["book"]}:{x["name"]}'] = {"m": middle(i), "s": sib}
    json.dump(P, open(os.path.join(ROOT, "data", "names_pairs.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    # dedicated pages: the best-known names of each book (200 French, 100 German), 40 middle names in 4 groups
    top = []
    for b, n in (("fr", 200), ("de", 100)):
        best = sorted((i for i, x in enumerate(rec) if x["book"] == b and x["pool"] and x["g"] in "fm"), key=lambda i: -rec[i]["pop"])[:n]
        top += best
    pages = {}
    for i in top:
        cands = middle(i, k=160)
        groups = {"short": [], "classic": [], "rare": [], "international": []}; used = set()
        for c in cands:
            j = idx[(c[0], c[1])]; tags = rec[j]["tags"]
            for gname in ("short", "international", "rare", "classic"):
                if gname in tags and len(groups[gname]) < 10 and c[1] not in used: groups[gname].append(c); used.add(c[1]); break
        groups["more"] = []                                               # the best remaining names, so each group keeps its true label
        for c in cands:
            if sum(map(len, groups.values())) >= 40: break
            if c[1] not in used: groups["more"].append(c); used.add(c[1])
        x = rec[i]
        pages[f'{x["book"]}:{x["name"]}'] = {"syl": x["syl"], "o": x["o"], "tags": sorted(x["tags"]), "g": x["g"], "slug": x["slug"],
                                            "pairs": [rec[j]["name"] for j in sorted(pairs.get(i, ()), key=lambda j: -rec[j]["pop"])][:6], "groups": groups}
    json.dump(pages, open(os.path.join(ROOT, "data", "names_middle_pages.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    # the tool's data: every name (autocomplete), compact
    orgs = sorted({x["o"] for x in rec if x["o"]})
    rows = [[x["book"], x["name"], x["slug"], x["g"], x["syl"], x["st"], x["en"], sum(1 << t for t, s in enumerate(STYLES) if s in x["tags"]),
             orgs.index(x["o"]) if x["o"] else -1, round(popn[i] * 100), int(x["pool"]), sorted(x["var"])[:6], x["peak"]] for i, x in enumerate(rec)]
    json.dump({"styles": STYLES, "origins": orgs, "n": rows, "pairs": {str(a): sorted(b) for a, b in pairs.items()}},
              open(os.path.join(ROOT, "assets", "names-match.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    from collections import Counter
    print(f"{N} profiles, pool {int(pool.sum())}, real pairings {sum(len(v) for v in pairs.values()) // 2}; tags",
          dict(Counter(t for x in rec for t in x["tags"])), f"; {len(P)} pair lists, {len(pages)} dedicated pages")

if __name__ == "__main__":
    main()
