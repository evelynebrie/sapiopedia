#!/usr/bin/env python3
"""Print every item's verdict and reasons for the ready-made rooms: preset_check.py [design|fengshui] [preset ...]"""
import json, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mode = sys.argv[1] if len(sys.argv) > 1 else "design"
names = sys.argv[2:] or ["cosy-bedroom", "small-studio", "living-room", "evening-living", "home-office", "kitchen-diner", "bathroom", "kids-room"]
tool = "/en/tools/room-planner/" if mode == "design" else "/en/tools/fengshui/"
h = tempfile.NamedTemporaryFile("w", suffix=".html", dir=os.path.join(ROOT, "_pins_batch"), delete=False)
h.write('<html><body><pre id="out"></pre><script>var N=' + json.dumps(names) + ',R={},i=0;function next(){if(i>=N.length){document.getElementById("out").textContent="J:"+JSON.stringify(R)+":END";return;}'
        'var n=N[i++],f=document.createElement("iframe");f.style.cssText="width:1100px;height:900px";f.src=' + json.dumps(tool) + '+"?preset="+n;'
        'f.onload=function(){setTimeout(function(){var A=f.contentWindow.FSAPI;R[n]=A.S.items.map(function(it){var o=A.oi(it);return [it.k,Math.round(o.x),Math.round(o.y),it.rot||0,A.verdict(it),A.explain(it).filter(function(c){return c.v!=="good"&&c.v!=="neutral"}).map(function(c){return c.v+": "+c.t})]});f.remove();next();},1500);};document.body.appendChild(f);}next();</script></body></html>')
h.close()
t = subprocess.run([CHROME, "--headless=new", "--virtual-time-budget=60000", "--dump-dom", "http://127.0.0.1:8765/_pins_batch/" + os.path.basename(h.name)], capture_output=True, text=True).stdout
os.unlink(h.name)
R = json.loads(re.search(r"<pre id=\"out\">J:(.*?):END</pre>", t, re.S).group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
for n, items in R.items():
    print(f"== {n}: {sum(1 for x in items if x[4] == 'bad')} bad, {sum(1 for x in items if x[4] == 'caution')} caution")
    for k, x, y, r, v, why in items:
        if v not in ("good", "neutral"): print(f"   {k:11} {x:4},{y:4} r{r:<3} {v:8} {' | '.join(why)}")
