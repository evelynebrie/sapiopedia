#!/usr/bin/env python3
"""Capture the room planner's own PNG export (FS3D.png()) headlessly: export_capture.py <tool path with ?preset=…> <out.png>
Needs the site served at http://127.0.0.1:8765 from the repo root."""
import base64, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def capture(path, out):
    os.makedirs(os.path.join(ROOT, "_pins_batch"), exist_ok=True)
    h = tempfile.NamedTemporaryFile("w", suffix=".html", dir=os.path.join(ROOT, "_pins_batch"), delete=False)
    h.write('<html><head><meta charset="utf-8"></head><body><pre id="out"></pre><script>var f=document.createElement("iframe");'
            'f.style.cssText="position:absolute;left:-3000px;width:1100px;height:900px";f.src=' + repr(path) + ';'
            'f.onload=function(){setTimeout(function(){f.contentWindow.FS3D.png().then(function(b){var r=new FileReader();'
            'r.onload=function(){document.getElementById("out").textContent="PNG:"+r.result+":END";};r.readAsDataURL(b);});},4500);};'
            'document.body.appendChild(f);</script></body></html>'); h.close()
    try:
        t = subprocess.run([CHROME, "--headless=new", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--virtual-time-budget=20000", "--dump-dom",
                            "http://127.0.0.1:8765/_pins_batch/" + os.path.basename(h.name)], capture_output=True, text=True, timeout=180).stdout
    finally: os.unlink(h.name)
    m = re.search(r"PNG:data:image/png;base64,([^:]+):END", t)
    if not m: raise RuntimeError("no export from " + path)
    open(out, "wb").write(base64.b64decode(m.group(1)))
if __name__ == "__main__":
    capture(sys.argv[1], sys.argv[2])
