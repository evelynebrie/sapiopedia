#!/usr/bin/env python3
"""Video pin: the 3D room turning once, lamps switching every 3 s, inside the usual pin frame.
Needs the local server (python3 -m http.server 8765 from the repo root) and _pins_batch/v-en-rp-turn.html (written by tools/pins_batch.py).
Writes Desktop/Sapiopedia/Pinterest/batch-2026-11/v-en-rp-turn.mp4 and its cover image v-en-rp-turn.png."""
import base64, concurrent.futures as cf, html, io, json, math, os, re, shutil, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch")
OUT = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest/batch-2026-11")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SRC = "/en/tools/room-planner/?preset=evening-living&view=3d&embed=3d&capture=1"
FPS, SECONDS, LIGHT_EVERY = 24, 12, 3          # one full turn in 12 s, lamps switch every 3 s
N, CHUNK = FPS * SECONDS, 48
FRAMES = os.path.join(TMP, "video-frames")

def chrome(args, timeout=600):
    return subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] + args,
                          capture_output=True, text=True, timeout=timeout).stdout

def base():
    """The pin frame, rendered once, and the box the room goes into."""
    page = os.path.join(TMP, "v-en-rp-turn.html")
    probe = open(page, encoding="utf-8").read().replace("</body>", '<script>addEventListener("load",function(){setTimeout(function(){var r=document.getElementById("shot").getBoundingClientRect();'
        'document.body.setAttribute("data-rect",[r.left,r.top,r.width,r.height].join(","));},1500);});</script></body>', 1)
    open(os.path.join(TMP, "_v-probe.html"), "w", encoding="utf-8").write(probe)
    dom = chrome(["--virtual-time-budget=6000", "--window-size=1000,1500", "--dump-dom", "http://127.0.0.1:8765/_pins_batch/_v-probe.html"])
    rect = [float(v) for v in re.search(r'data-rect="([^"]+)"', dom).group(1).split(",")]
    png = os.path.join(TMP, "_v-base.png")
    chrome(["--virtual-time-budget=6000", "--window-size=1000,1500", f"--screenshot={png}", "http://127.0.0.1:8765/_pins_batch/v-en-rp-turn.html"])
    os.remove(os.path.join(TMP, "_v-probe.html"))
    return Image.open(png).convert("RGB"), rect

def capture(first):
    """Frames first..first+CHUNK-1 of the 3D room, as PNGs with a transparent background."""
    last = min(N, first + CHUNK)
    frames = [[math.pi / 4 + 2 * math.pi * f / N, (f // (FPS * LIGHT_EVERY)) % 2 == 0] for f in range(first, last)]
    page = f"""<!doctype html><html><head><meta charset="utf-8"></head><body><pre id="out"></pre>
<iframe id="f" style="width:820px;height:900px;border:0" src="{SRC}"></iframe><script>
var F={json.dumps(frames)},f=document.getElementById("f");
f.onload=function(){{var w=f.contentWindow,go=function(){{if(!w.__frame)return setTimeout(go,200);var out=[],i=0;
 (function next(){{if(i>=F.length){{document.getElementById("out").textContent="FRA"+"MES:"+out.join("|")+":E"+"ND";return;}}
  w.__frame(F[i][0],F[i][1]).then(function(d){{out.push(d.split(",")[1]);i++;next();}},function(e){{document.getElementById("out").textContent="ERR:"+e;}});}})();}};setTimeout(go,1500);}};
</script></body></html>"""
    name = f"_v-cap-{first}.html"; open(os.path.join(TMP, name), "w", encoding="utf-8").write(page)
    dom = html.unescape(chrome(["--virtual-time-budget=240000", "--window-size=900,1000", "--dump-dom", f"http://127.0.0.1:8765/_pins_batch/{name}"], timeout=900))
    os.remove(os.path.join(TMP, name))
    m = re.search(r"FRAMES:(.*?):END", dom, re.S)
    if not m: raise RuntimeError(f"no frames from chunk {first}: " + (re.search(r"ERR:[^<]*", dom) or re.search(r"<pre[^>]*>[^<]{0,300}", dom) or [dom[-300:]])[0])
    data = m.group(1).split("|")
    assert len(data) == last - first, (first, len(data))
    for k, b in enumerate(data): open(os.path.join(FRAMES, f"room_{first + k:03d}.png"), "wb").write(base64.b64decode(b))
    return first

if __name__ == "__main__":
    shutil.rmtree(FRAMES, ignore_errors=True); os.makedirs(FRAMES)
    bg, (x, y, w, h) = base()
    with cf.ThreadPoolExecutor(3) as ex:
        for first in ex.map(capture, range(0, N, CHUNK)): print("captured", first, file=sys.stderr)
    for f in range(N):   # the room, scaled to fit the box, centred, on the pin frame
        room = Image.open(os.path.join(FRAMES, f"room_{f:03d}.png")).convert("RGBA")
        s = min(w / room.width, h / room.height); room = room.resize((round(room.width * s), round(room.height * s)), Image.LANCZOS)
        frame = bg.copy(); frame.paste(room, (round(x + (w - room.width) / 2), round(y + (h - room.height) / 2)), room)
        frame.save(os.path.join(FRAMES, f"pin_{f:03d}.png"))
    mp4 = os.path.join(OUT, "v-en-rp-turn.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "pin_%03d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
    shutil.copy(os.path.join(FRAMES, "pin_000.png"), os.path.join(OUT, "v-en-rp-turn.png"))
    print("wrote", mp4)
