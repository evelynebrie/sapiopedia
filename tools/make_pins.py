#!/usr/bin/env python3
"""Build 10 Pinterest pins (1000x1500) as HTML in _pins/, to be screenshotted by tools/shoot_pins.sh.
Content comes from the site's own data so every pin matches the page it links to."""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_pins"); os.makedirs(OUT, exist_ok=True)
E = {e["id"]: e for e in json.load(open(os.path.join(ROOT, "data", "dreams_en.json")))["entries"]}
N = json.load(open(os.path.join(ROOT, "assets", "names-fr.json"))); IDX = {r[0]: r for r in json.load(open(os.path.join(ROOT, "data", "names_fr_list.json")))}
esc = lambda s: html.escape(s or "")
THUMB = '<svg width="0" height="0" style="position:absolute"><defs><path id="th" d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/></defs></svg>'

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Source+Sans+3:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=Cormorant+Garamond:ital,wght@0,500;1,400&display=swap">
<style>
*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:1500px;overflow:hidden;background:#F7E9EC;color:#2A1F26;font-family:'Source Sans 3',sans-serif;position:relative}
.pin{position:absolute;inset:0;display:flex;flex-direction:column}
.top{padding:70px 72px 0;display:grid;gap:18px}
.kick{font-size:20px;letter-spacing:.24em;text-transform:uppercase;font-weight:700;color:#8E2F48}
h1{font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:84px;line-height:.98;letter-spacing:-.035em;margin:0}
h1 em{color:#B8405E}
.sub{font-family:'Fraunces',Georgia,serif;font-weight:300;font-size:32px;line-height:1.3;color:#4A3C42;margin:0}
.mid{flex:1;padding:36px 72px 0;display:flex;flex-direction:column;justify-content:center;min-height:0}
.band{height:150px;background:#F1DCE1;border-top:2px solid #DCC9CE;display:flex;align-items:center;justify-content:space-between;padding:0 64px}
.band img{height:86px}
.band .u{text-align:right}.band .u b{display:block;font-size:30px;font-weight:700;color:#2A1F26}.band .u span{font-size:21px;color:#6E5A62}
/* old-book card (dreams) */
.book{background:#FCF7F2;border:1px solid #E6D9CC;box-shadow:inset 0 0 0 9px #FCF7F2,inset 0 0 0 10px #E6D9CC,0 18px 40px -20px rgba(42,31,38,.35);padding:46px 52px;font-family:'EB Garamond',Georgia,serif;color:#2B2320}
.book .lead{font-style:italic;font-size:31px;line-height:1.35;text-align:center;margin:0 0 26px}
.book h3{font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:28px;display:flex;align-items:center;gap:16px;margin:0 0 14px}
.book h3::before,.book h3::after{content:"";flex:1;border-top:3px double #BFAE9F}
.book ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.book li{display:grid;grid-template-columns:40px 1fr;gap:6px;font-size:27px;line-height:1.3;color:#3A302B}
.book li i{color:#2B2320}
.th{width:30px;height:30px;margin-top:3px;stroke-width:1.1}
.th.up{fill:#6E8F63;stroke:#3E5638}.th.mid{fill:#D4AE52;stroke:#8A6A22;transform:rotate(-90deg)}.th.down{fill:#B0564A;stroke:#6E2C25;transform:rotate(180deg)}
.dots{color:#8E2F48;letter-spacing:4px}.dots s{text-decoration:none;color:#E2D5CB}
.dtitle{display:grid;grid-template-columns:auto 1fr;gap:0 20px;align-items:center;margin-bottom:22px;border-bottom:3px double #BFAE9F;padding-bottom:18px}
.dtitle .ini{font-family:'IM Fell English',serif;font-size:120px;line-height:.8;color:#8E2F48}
.dtitle h2{font-family:'IM Fell English',serif;font-weight:400;font-size:56px;margin:0;line-height:1}
.dtitle p{margin:8px 0 0;font-style:italic;font-size:24px;color:#5B4A40}
/* name list */
.names{columns:2;column-gap:40px;background:#FCF7F2;border:1px solid #E6D9CC;box-shadow:inset 0 0 0 9px #FCF7F2,inset 0 0 0 10px #E6D9CC;padding:44px 48px;font-family:'EB Garamond',serif}
.names div{break-inside:avoid;padding:10px 0;border-bottom:1px dotted #BFAE9F}
.names b{font-family:'IM Fell English',serif;font-weight:400;font-size:44px;color:#2B2320;display:block;line-height:1}
.names span{font-size:23px;color:#5B4A40}
.sym{font-size:32px;margin-left:8px;vertical-align:4px}
/* question cards */
.q{display:grid;gap:16px}
.q div{background:#fff;border-radius:22px;padding:24px 30px;font-family:'Fraunces',serif;font-size:31px;line-height:1.25;box-shadow:0 6px 16px -10px rgba(42,31,38,.4)}
.q small{display:block;font-family:'Source Sans 3',sans-serif;font-size:17px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;margin-bottom:6px}
.q .t small{color:#2E5F6E}.q .d small{color:#B8405E}
.shot{border-radius:20px;overflow:hidden;box-shadow:0 24px 50px -24px rgba(42,31,38,.45);background:#fff}
.shot img{display:block;width:100%}
.chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.chips span{background:#fff;border-radius:999px;padding:12px 22px;font-size:24px;font-weight:600;color:#8E2F48}
</style></head><body>'''

def band(url, label):
    return f'<div class="band"><img src="/assets/logo-horizontal.png" alt=""><div class="u"><b>{esc(url)}</b><span>{esc(label)}</span></div></div>'

def page(name, kick, title, sub, mid, url, label):
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(
        HEAD + THUMB + f'<div class="pin"><div class="top"><div class="kick">{kick}</div><h1>{title}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div><div class="mid">{mid}</div>{band(url, label)}</div></body></html>')

def dots(n): return '●' * n + f'<s>{"●" * (5 - n)}</s>'

def dream(pid, key, title, n=5):
    e = E[key]; sits = e["situations"]
    pick = [s for s in sits if s[2] == "up"][:2] + [s for s in sits if s[2] == "mid"][:1] + [s for s in sits if s[2] == "down"][:2]
    pick = pick[:n]
    lis = "".join(f'<li><svg class="th {s[2]}" viewBox="0 0 24 24"><use href="#th"/></svg><span><i>{esc(s[0])}:</i> {esc(s[1])}</span></li>' for s in pick)
    mid = (f'<div class="book"><div class="dtitle"><span class="ini">{esc(e["word"][0])}</span><div><h2>{esc(e["title"])}</h2><p><span class="dots">{dots(e["tone"])}</span> {esc(e["tone_label"])}</p></div></div>'
           f'<p class="lead">{esc(e["one"])}</p><h3>What happens in the dream</h3><ul>{lis}</ul></div>')
    page(pid, "Dream dictionary", title, "", mid, f"sapiopedia.com/en/dreams/#{key}", "2,598 dreams, explained in plain words")

def names(pid, g, lst, title, sub, sym):
    rows = ""
    for w in lst:
        c = N[IDX[w][3]]; ipa = re.sub(r"^\^\(\(.*?\)\)", "", c.get("ipa", ""))
        rows += f'<div><b>{esc(w)}</b><span>{esc(ipa)}</span></div>'
    page(pid, "French first names", title, sub, f'<div class="names">{rows}</div>', "sapiopedia.com/en/names/french/", "9,128 French names with pronunciation")

dream("01-dream-snakes", "snake", 'What does it mean to <em>dream of snakes?</em>')
dream("02-dream-teeth", "teeth", 'Dreaming of <em>teeth</em>: what it means')
dream("03-dream-flying", "flying", 'Did you dream you were <em>flying?</em>')
names("04-french-girl-names", "f", ["Adèle", "Agathe", "Alice", "Apolline", "Capucine", "Clémence", "Colette", "Éloïse", "Jeanne", "Juliette", "Louise", "Rose"],
      'French girl names <em>with old-world charm</em>', "With how to say them, the French way", "♀")
names("05-french-boy-names", "m", ["Achille", "Arthur", "Augustin", "Basile", "Côme", "Gabriel", "Gaspard", "Jules", "Léon", "Martin", "Raphaël", "Victor"],
      'Classic French <em>boy names</em>', "With how to say them, the French way", "♂")
names("06-french-unisex-names", "n", ["Camille", "Claude", "Dominique", "Charlie", "Alix", "Andréa", "Ange", "Morgan", "Eden", "Maxence", "Lou", "Céleste"],
      'French names <em>for girls and boys</em>', "Twelve names that work for any baby", "⚥")

page("07-room-planner-3d", "Free room planner", 'Plan your room, <em>then see it in 3D</em>', "Exact sizes, real furniture, your floor and wall colours.",
     '<div class="shot"><img id="shot3d" alt=""></div><div class="chips"><span>2D plan → 3D</span><span>Clearance check</span><span>Lamps & lighting</span><span>PNG export</span></div>',
     "sapiopedia.com/en/tools/room-planner/", "Free, in your browser, no sign-up")
page("08-feng-shui-bed", "Feng shui room planner", 'Is your bed in the <em>right place?</em>', "Draw your room: every piece gets a feng shui verdict.",
     '<div class="shot" id="plan2d" style="padding:20px 10px;background:#FFF8F9"></div><div class="chips"><span>Command position</span><span>Door & window lines</span><span>Free 3D view</span></div>',
     "sapiopedia.com/en/tools/fengshui/", "Free feng shui room planner")
page("09-scratch-gift-card", "Free scratch-off gift card", 'Send a gift they <em>scratch to reveal</em>', "Write your surprise, send the link, add confetti, hearts or snow.",
     '''<div style="background:#f1eee7;border:1px solid #d9d0c6;padding:16px;box-shadow:0 20px 40px -20px rgba(66,38,43,.35)"><div style="border:1px solid #8b827e;padding:10px"><div style="position:relative;aspect-ratio:1.5;background:#ece6df;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;text-align:center">
       <div style="font:600 18px 'Source Sans 3';letter-spacing:.2em;color:#8c7775">FOR CAMILLE</div><div style="font-size:66px;line-height:1;margin-top:12px">A weekend in Paris</div><div style="font-style:italic;font-size:32px;color:#973c55;margin-top:14px">Just because you deserve something wonderful.</div>
       <div style="position:absolute;inset:0;background:linear-gradient(135deg,#c9c7c4,#b9b7b5 55%,#c6c2bf);-webkit-mask:radial-gradient(circle at 30% 50%,transparent 0 120px,#000 121px),radial-gradient(circle at 56% 40%,transparent 0 110px,#000 111px);-webkit-mask-composite:source-in;mask-composite:intersect"></div></div></div></div>
       <div style="position:relative;height:0"><span style="position:absolute;right:20px;top:-430px;font-size:70px">💗</span></div>
       <div class="chips"><span>Free</span><span>No sign-up</span><span>Confetti · hearts · snow</span></div>''',
     "sapiopedia.com/en/tools/scratch-gift-card/", "Make one in a minute")
page("10-truth-or-dare", "Party game", '<em>Truth or Dare</em> questions for adults', "Clean or a bit spicy: draw one at random.",
     '<div class="q"><div class="t"><small>Truth</small>What is the most useless skill you are secretly proud of?</div><div class="d"><small>Dare</small>Describe a random object in the room like a nature documentary narrator.</div><div class="t"><small>Truth</small>Which text message are you most relieved you never sent?</div><div class="d"><small>Dare</small>Speak only in questions until your next turn.</div><div class="t"><small>Truth</small>What did you want to be when you were seven?</div></div>',
     "sapiopedia.com/en/games/truth-or-dare-questions/", "60 truths and dares, clean or a bit spicy")
print("pins written to", OUT)
