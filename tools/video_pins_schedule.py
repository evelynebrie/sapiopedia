#!/usr/bin/env python3
"""Launch plan for the video pins (scratch card, 3D rooms, 2027 wallpaper): one a day at 21:00, a slot the other schedules leave free.
Same rules as pins_batch.py, checked against every pin already in the Desktop CSVs: >= 7 days between pins of the same page (3 for the scratch videos, see GAP), titles unique.
Pinterest schedules at most ~30 days ahead, so pins after that go to a second CSV to upload later.
Copies each .mp4 and its cover .png to pins/v/ (served at https://sapiopedia.com/pins/v/), and writes
Desktop/Sapiopedia/Pinterest/pinterest-bulk-upload-videos.csv (+ -videos-part2.csv)."""
import base64, csv, datetime, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest"); SRC = os.path.join(DESK, "batch-2026-11")
SITE = "https://sapiopedia.com"; BOARD = "Gift ideas"   # the only board on the account (as in pins_batch.py)
START, SLOT = datetime.date(2026, 11, 13), "21:00:00"
CUT = datetime.date(2026, 11, 11) + datetime.timedelta(29)   # last day Pinterest accepts in today's upload

def wp_link(s, y, w):   # the wallpaper tool opens on the exact design shown in the video
    st = {"s": s, "y": y, "z": "1179x2556", "w": w, "g": "See the sea in Portugal\nRead 24 books\nSunday dinners, phones off\nFinish my first quilt\nLearn to make bread",
          "q": "Slowly, then all at once.", "ow": 1, "og": 1, "oq": 1}
    return f"{SITE}/en/tools/2027-phone-wallpaper/#" + base64.b64encode(json.dumps(st, ensure_ascii=False, separators=(",", ":")).encode()).decode()
SCRATCH, FS, RP = f"{SITE}/en/tools/scratch-gift-card/", f"{SITE}/en/tools/fengshui/", f"{SITE}/en/tools/room-planner/"
SC_TAGS = "Virtual gift, Last minute gift, Gift ideas, Scratch off card, Long distance gift, Birthday gift ideas, Digital gift, Gift for him, Gift for her, Surprise gift"
FS_TAGS = "Feng shui, Feng shui bedroom, Feng shui tips, Feng shui home, Room layout, Bedroom layout, Interior design, Home decor, Good energy home"
RP_TAGS = "Room planner, Room layout, Furniture arrangement, Floor plan, 3D room design, Interior design, Home decor, Small apartment ideas"
WP_TAGS = "2027 wallpaper, Phone wallpaper, Lock screen wallpaper, 2027 goals, Vision board 2027, Word of the year, New year goals, Aesthetic wallpaper, iPhone wallpaper, Manifestation"

# id, title (<= 100, unique), description (<= 500), link, keywords
PINS = [
 ("vs-snow-christmas", "Christmas gift idea: a scratch-off card they open on their phone",
  "Hide your Christmas gift under a scratch-off card and send it as a link. They scratch it on their phone, the gift appears and it starts to snow. Perfect for long-distance Christmas and last-minute gifts. Ready in a minute. Free, no sign-up.",
  SCRATCH, "Christmas gift ideas, Christmas surprise, " + SC_TAGS),
 ("vw-goals", "Free customizable 2027 lock screen with your goals",
  "Write your 2027 goals and dreams, pick a style, download a wallpaper made for your phone's exact screen. Word of the year and quote of the year included. Your vision board, on your lock screen. Free, no sign-up.",
  wp_link("riso", "shadow", "Bloom"), WP_TAGS),
 ("v-en-fs-bedroom-turn", "Feng shui bedroom in 3D, lamps on and off",
  "Open this bedroom in the free feng shui room planner: every piece gets a verdict (bed in command position, door and window lines), then walk around it in 3D with the lamps on or off. Move things until everything is green. Free, no sign-up.",
  f"{FS}?preset=cosy-bedroom&view=3d", FS_TAGS),
 ("vs-hearts-lastminute", "Last-minute virtual gift: scratch to reveal, with hearts",
  "Forgot a gift? Write it on a scratch-off card, send the link, and they scratch it on their phone: dinner, a trip, a promise. Hearts float up when it's revealed. Ready in a minute, perfect for birthdays and anniversaries. Free, no sign-up.",
  SCRATCH, "Anniversary gift, Valentines gift idea, " + SC_TAGS),
 ("v-en-rp-studio-turn", "Small studio layout: see it in 3D before you move a thing",
  "Bed, desk and sofa in a 5.2 × 4 m studio. Open this exact room in the free room planner: real furniture sizes, a clearance check, then a 3D view in your own floor and wall colours. Free, no sign-up.",
  f"{RP}?preset=small-studio&view=3d", "Studio apartment layout, Small studio ideas, " + RP_TAGS),
 ("vw-word", "Your word for 2027: a free customizable phone wallpaper",
  "Bloom, Courage, Calm, Wander, Brave… Choose your word of the year and put it on your lock screen with your goals and a quote. Ten styles for 2027, made for your phone's screen. Free, no sign-up.",
  wp_link("night", "moon", "Brave"), "One word 2027, " + WP_TAGS),
 ("vs-confetti-tickets", "Scratch-off gift card with confetti: send tickets as a surprise",
  "Concert tickets, a show, a trip: hide them under a scratch-off card and send the link. They scratch it on their phone and confetti bursts out. Choose the ending: confetti, hearts or snow. Free, no sign-up.",
  SCRATCH, "Concert tickets gift, Experience gift, " + SC_TAGS),
 ("v-en-fs-living-turn", "Feng shui living room layout, in 3D",
  "Every piece of this living room gets a feng shui verdict: command position, door and window lines, clutter. Then turn it around in 3D. Open it as-is, move the sofa, check again. Free feng shui room planner, no sign-up.",
  f"{FS}?preset=living-room&view=3d", "Feng shui living room, " + FS_TAGS),
 ("vw-styles", "Free customizable 2027 phone wallpaper, 10 styles",
  "Make your 2027 phone wallpaper: word of the year, goals and dreams, quote of the year. Ten styles for the year and three colour themes, sized for iPhone and Android. Download it and set it as your lock screen. Free, no sign-up.",
  wp_link("almanac", "riso", "Bloom"), "New year aesthetic, " + WP_TAGS),
 ("vs-hearts-distance", "Long-distance gift idea: a card they scratch from far away",
  "A flight to see them, a visit, a countdown: write it on a scratch-off card and send the link. Wherever they are, they scratch it on their phone and the gift appears with hearts. Free, no sign-up.",
  SCRATCH, "Long distance relationship gift, LDR gift, " + SC_TAGS),
 ("v-en-rp-office-turn", "Home office layout in 3D, lights on or off",
  "A 3.6 × 3.2 m home office ready to open in the free room planner: desk, chair, shelves at their real sizes, a clearance check, and a 3D view with the lamp on or off. Make it yours, then save the image. Free, no sign-up.",
  f"{RP}?preset=home-office&view=3d", "Home office layout, Home office ideas, " + RP_TAGS),
]

def key(link): return re.sub(r"[&?]view=3d", "", link.split("#")[0])
taken, titles = {}, set()
for f in ("pinterest-bulk-upload.csv", "pinterest-bulk-upload-part2.csv", "pinterest-bulk-upload-fix.csv", "pinterest-bulk-upload-baby.csv"):
    p = os.path.join(DESK, f)
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p, encoding="utf-8")):
        taken.setdefault(key(r["Link"]), []).append(datetime.date.fromisoformat(r["Publish date"][:10])); titles.add(r["Title"])

# the scratch card page already has a pin every week to January: its videos go mid-week, >= 3 days from those pins
GAP = {"vs-snow-christmas": 3, "vs-hearts-lastminute": 3, "vs-confetti-tickets": 3, "vs-hearts-distance": 3}
NOT_BEFORE = {"vs-snow-christmas": datetime.date(2026, 11, 23), "vs-hearts-lastminute": datetime.date(2026, 12, 8)}   # Christmas from late Nov; "last-minute" from 8 Dec
plan, day, queue = [], START, list(PINS)
while queue:   # each day, the first pin in order whose page is free for 7 days either side
    for i, p in enumerate(queue):
        if day >= NOT_BEFORE.get(p[0], START) and all(abs((day - d).days) >= GAP.get(p[0], 7) for d in taken.get(key(p[3]), [])):
            plan.append((day, p)); taken.setdefault(key(p[3]), []).append(day); queue.pop(i); break
    day += datetime.timedelta(1)
    if day > START + datetime.timedelta(120): raise SystemExit(f"cannot place {[p[0] for p in queue]}")

os.makedirs(os.path.join(ROOT, "pins", "v"), exist_ok=True)
cols = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
for name, rows in (("pinterest-bulk-upload-videos.csv", [x for x in plan if x[0] <= CUT]), ("pinterest-bulk-upload-videos-part2.csv", [x for x in plan if x[0] > CUT])):
    path = os.path.join(DESK, name)
    if not rows:
        if os.path.exists(path): os.remove(path)
        continue
    with open(path, "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(cols)
        for d, (pid, title, desc, link, tags) in rows:
            assert len(title) <= 100 and len(desc) <= 500 and title not in titles, pid
            wr.writerow([title, f"{SITE}/pins/v/{pid}.mp4", BOARD, f"{SITE}/pins/v/{pid}.png", desc, link, f"{d.isoformat()}T{SLOT}", tags])
    print(name, len(rows), "pins,", rows[0][0], "to", rows[-1][0])
for d, p in plan:
    for ext in ("mp4", "png"): shutil.copy(os.path.join(SRC, f"{p[0]}.{ext}"), os.path.join(ROOT, "pins", "v", f"{p[0]}.{ext}"))
    print(d, d.strftime("%a"), SLOT[:5], p[0], "·", p[1])
