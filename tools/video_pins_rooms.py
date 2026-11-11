#!/usr/bin/env python3
"""More video pins like v-en-rp-turn: a preset room turning once in 3D, lamps switching, inside the usual pin frame.
Half open the feng shui planner, half the room planner; each varies the room, the title, the chips, the spin direction and the lamp rhythm.
Needs the local server (python3 -m http.server 8765 from the repo root) and the frame page _pins_batch/v-en-rp-turn.html (tools/pins_batch.py).
Writes Desktop/Sapiopedia/Pinterest/batch-2026-11/v-en-<id>.mp4 and a cover image v-en-<id>.png. ONLY=<regex> limits which pins are made."""
import base64, html, json, math, os, re, shutil, subprocess, sys
import concurrent.futures as cf
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import video_pin as V   # chrome(), TMP, OUT, the frame-by-frame __frame hook

FPS, SECONDS = 24, 12
N = FPS * SECONDS
FS = ("Feng shui room planner", "/en/tools/fengshui/", "Free feng shui room planner")
RP = ("Free room planner", "/en/tools/room-planner/", "Free, in your browser")
PINS = [  # id, tool, preset, title, sub, chips, turn direction, seconds per lamp switch
 ("fs-bedroom-turn", FS, "cosy-bedroom", "A feng shui bedroom, <em>day and night</em>", "Place the bed well, then walk around it in 3D.",
  ["Verdict for every piece", "Lights on and off", "Plan ↔ 3D"], 1, 3),
 ("fs-living-turn", FS, "living-room", "Feng shui your living room, <em>in 3D</em>", "Every piece gets a verdict. Then turn the room around.",
  ["Command position", "Door and window lines", "Plan ↔ 3D"], -1, 4),
 ("rp-studio-turn", RP, "small-studio", "Small studio? <em>See it in 3D first</em>", "Bed, desk and sofa in 5.2 × 4 m. Try it first.",
  ["Exact sizes", "Clearance check", "Plan ↔ 3D"], -1, 3),
 ("rp-office-turn", RP, "home-office", "Your home office, <em>lights on or off</em>", "Plan it to the centimetre, then walk around it in 3D.",
  ["Exact sizes", "Your floor and walls", "Lights on and off"], 1, 4),
]
TEMPLATE = open(os.path.join(V.TMP, "v-en-rp-turn.html"), encoding="utf-8").read()

def frame_page(pid, tool, title, sub, chips):
    kick, base, label = tool
    h = re.sub(r'<div class="kick">.*?</div>', f'<div class="kick">{kick}</div>', TEMPLATE, 1)
    h = re.sub(r"<h1>.*?</h1>", f"<h1>{title}</h1>", h, 1)
    h = re.sub(r"<p class=sub>.*?</p>", f"<p class=sub>{sub}</p>", h, 1)
    h = re.sub(r'<div class="chips">.*?</div>', '<div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>", h, 1)
    h = re.sub(r'<div class="u"><b>.*?</b><span>.*?</span>', f'<div class="u"><b>sapiopedia.com{base}</b><span>{label}</span>', h, 1)
    name = f"v-en-{pid}.html"; open(os.path.join(V.TMP, name), "w", encoding="utf-8").write(h); return name

def base_image(name):
    """The pin frame rendered once, and the box the room goes into."""
    probe = open(os.path.join(V.TMP, name), encoding="utf-8").read().replace("</body>", '<script>addEventListener("load",function(){setTimeout(function(){var r=document.getElementById("shot").getBoundingClientRect();'
        'document.body.setAttribute("data-rect",[r.left,r.top,r.width,r.height].join(","));},1500);});</script></body>', 1)
    pn = "_probe-" + name; open(os.path.join(V.TMP, pn), "w", encoding="utf-8").write(probe)
    dom = V.chrome(["--virtual-time-budget=6000", "--window-size=1000,1500", "--dump-dom", f"http://127.0.0.1:8765/_pins_batch/{pn}"])
    rect = [float(v) for v in re.search(r'data-rect="([^"]+)"', dom).group(1).split(",")]
    png = os.path.join(V.TMP, name[:-5] + "-base.png")
    V.chrome(["--virtual-time-budget=6000", "--window-size=1000,1500", f"--screenshot={png}", f"http://127.0.0.1:8765/_pins_batch/{name}"])
    os.remove(os.path.join(V.TMP, pn))
    return Image.open(png).convert("RGB"), rect

def capture(src, frames, todo):
    """Room frames for todo = [(index, angle, lamps on)], as PNGs with a transparent background (same iframe hook as video_pin.py)."""
    first = todo[0][0]
    page = f"""<!doctype html><html><head><meta charset="utf-8"></head><body><pre id="out"></pre>
<iframe id="f" style="width:820px;height:900px;border:0" src="{src}"></iframe><script>
var F={json.dumps([[a, l] for _, a, l in todo])},f=document.getElementById("f");
f.onload=function(){{var w=f.contentWindow,go=function(){{if(!w.__frame)return setTimeout(go,200);var out=[],i=0;
 (function next(){{if(i>=F.length){{document.getElementById("out").textContent="FRA"+"MES:"+out.join("|")+":E"+"ND";return;}}
  w.__frame(F[i][0],F[i][1]).then(function(d){{out.push(d.split(",")[1]);i++;next();}},function(e){{document.getElementById("out").textContent="ERR:"+e;}});}})();}};setTimeout(go,1500);}};
</script></body></html>"""
    name = f"_cap-{os.path.basename(frames)}-{first}.html"; open(os.path.join(V.TMP, name), "w", encoding="utf-8").write(page)
    dom = html.unescape(V.chrome(["--virtual-time-budget=240000", "--window-size=900,1000", "--dump-dom", f"http://127.0.0.1:8765/_pins_batch/{name}"], timeout=900))
    os.remove(os.path.join(V.TMP, name))
    m = re.search(r"FRAMES:(.*?):END", dom, re.S)
    if not m: raise RuntimeError(f"no frames from {name}")
    data = m.group(1).split("|"); assert len(data) == len(todo)
    for (k, _, _), b in zip(todo, data): open(os.path.join(frames, f"room_{k:03d}.png"), "wb").write(base64.b64decode(b))

def make(spec):
    pid, tool, preset, title, sub, chips, sign, every = spec
    src = f"{tool[1]}?preset={preset}&view=3d&embed=3d&capture=1"
    frames = os.path.join(V.TMP, f"video-frames-{pid}"); shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
    bg, (x, y, w, h) = base_image(frame_page(pid, tool, title, sub, chips))
    allf = [(f, math.pi / 4 + sign * 2 * math.pi * f / N, (f // (FPS * every)) % 2 == 0) for f in range(N)]
    with cf.ThreadPoolExecutor(3) as ex:
        list(ex.map(lambda i: capture(src, frames, allf[i:i + 48]), range(0, N, 48)))
    for f in range(N):   # the room, scaled to fit the box, centred, on the pin frame
        room = Image.open(os.path.join(frames, f"room_{f:03d}.png")).convert("RGBA")
        s = min(w / room.width, h / room.height); room = room.resize((round(room.width * s), round(room.height * s)), Image.LANCZOS)
        fr = bg.copy(); fr.paste(room, (round(x + (w - room.width) / 2), round(y + (h - room.height) / 2)), room); fr.save(os.path.join(frames, f"pin_{f:03d}.png"))
    mp4 = os.path.join(V.OUT, f"v-en-{pid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "pin_%03d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
    shutil.copy(os.path.join(frames, "pin_000.png"), os.path.join(V.OUT, f"v-en-{pid}.png"))
    print("wrote", mp4, file=sys.stderr)

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    for spec in PINS:
        if not only or re.search(only, spec[0]): make(spec)
