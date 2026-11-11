#!/usr/bin/env python3
"""Video pins of the 2027 phone wallpaper maker: the real tool draws each screen (in a hidden iframe), shown on a phone with a lock-screen clock.
  styles: the year style and colours change every 0.9 s.   goals: the goals are typed in, one line after another.   word: the word of the year is typed, erased, retyped.
Needs the local server (python3 -m http.server 8765 from the repo root). Uses tools/cdp_frames.mjs.
Writes Desktop/Sapiopedia/Pinterest/batch-2026-11/vw-<name>.mp4 and a cover image vw-<name>.png. ONLY=<regex> limits which pins are made."""
import json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch"); os.makedirs(TMP, exist_ok=True)
OUT = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest/batch-2026-11")
FPS, SECONDS = 30, 9
FREE = ('<style>.free{position:absolute;top:18px;right:40px;z-index:5;background:#8E2F48;color:#fff;font:700 24px "Source Sans 3",sans-serif;letter-spacing:.12em;'
        'text-transform:uppercase;padding:9px 18px;border-radius:999px;box-shadow:0 4px 12px -4px rgba(42,31,38,.4)}</style><div class="free">Free · No sign-up</div>')
YEARS = ["riso", "italic", "light", "stacked", "vintage", "moon", "halftone", "arc", "shadow", "outline"]
GOALS = ["See the sea in Portugal", "Read 24 books", "Sunday dinners, phones off", "Finish my first quilt", "Learn to make bread"]

def keyframes(kind):
    """[(seconds, state)], each state a full set of the tool's inputs; the screen shows the latest state reached."""
    base = {"s": 0, "y": "riso", "w": "Bloom", "g": "\n".join(GOALS), "q": "Slowly, then all at once."}
    if kind == "styles":
        return [(i * .9, dict(base, s=i % 3, y=y)) for i, y in enumerate(YEARS)]
    if kind == "goals":   # riso pink, typed at 22 letters a second, a short pause between lines
        ks, t, done = [(0, dict(base, s=2, y="shadow", g=""))], .8, []
        for line in GOALS:
            for n in range(1, len(line) + 1):
                ks.append((t, dict(base, s=2, y="shadow", g="\n".join(done + [line[:n]])))); t += 1 / 22
            done.append(line); t += .35
        return ks
    if kind == "word":    # night sky; each word typed, held, erased
        ks, t = [], 0
        for wd in ["Bloom", "Courage", "Calm", "Wander", "Brave"]:
            for n in range(1, len(wd) + 1): ks.append((t, dict(base, s=1, y="moon", w=wd[:n]))); t += 1 / 14
            t += .85
            if wd != "Brave":
                for n in range(len(wd) - 1, -1, -1): ks.append((t, dict(base, s=1, y="moon", w=wd[:n] or " "))); t += 1 / 30
        return ks
PINS = [
 ("styles", "Free <em>customizable</em> 2027 phone wallpaper", "Word of the year, goals and a quote, made for your screen."),
 ("goals", "Your 2027 goals, <em>free&nbsp;&amp;&nbsp;customizable</em>", "Type them in, download, set as wallpaper. Done in a minute."),
 ("word", "Your word for 2027, <em>free&nbsp;&amp;&nbsp;customizable</em>", "Bloom, Courage, Calm… Put it where you'll see it every day."),
]

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:1500px;overflow:hidden;background:#F4E6E9;color:#2A1F26;font-family:'Source Sans 3',sans-serif;position:relative}
h1{position:absolute;left:70px;right:70px;top:100px;margin:0;font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:84px;line-height:1;letter-spacing:-.03em;text-align:center}
h1 em{color:#A83A57}
.phone{position:absolute;left:50%;top:{{PHONE_TOP}}px;transform:translateX(-50%) scale(1.2);transform-origin:50% 0;width:452px;height:930px;border-radius:58px;background:#1f1a1c;padding:16px;box-shadow:0 30px 60px -30px rgba(42,31,38,.55)}
.scr{position:relative;width:420px;height:898px;border-radius:42px;overflow:hidden;background:#FBF6F0}
.scr img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.clock{position:absolute;left:0;right:0;top:8.5%;text-align:center;font-family:-apple-system,'SF Pro Display',system-ui,sans-serif;opacity:.82}
.clock .d{font-size:22px;font-weight:600}.clock .t{font-size:108px;font-weight:600;line-height:1;letter-spacing:-.02em}
.notch{position:absolute;left:50%;top:14px;width:118px;height:34px;margin-left:-59px;border-radius:20px;background:#0d0b0c}
p{position:absolute;left:50px;right:50px;top:{{P_TOP}}px;margin:0;font-size:32px;line-height:1.35;color:#4A3C42;text-align:center}
.u{position:absolute;left:0;right:0;bottom:46px;text-align:center;font-size:27px;letter-spacing:.04em;color:#6E5A62}.u b{color:#2A1F26;font-weight:600}
#tool{position:absolute;left:-3000px;top:0;width:1300px;height:1500px;border:0}
</style></head><body>{{FREE}}
<h1>{{H1}}</h1><div class="phone"><div class="scr"><img id="a" alt=""><img id="b" alt=""><div class="notch"></div><div class="clock" id="clock"><div class="d">Friday 1 January</div><div class="t">9:41</div></div></div></div>
<div class="u"><b>sapiopedia.com</b> · free 2027 phone wallpaper</div>
<iframe id="tool" src="/en/tools/2027-phone-wallpaper/"></iframe>
<script>
var K={{KEYS}},FPS={{FPS}},FADE={{FADE}},GHOST=['#2A1F26','#FFFFFF','#2A1F26'],shots=[];
var f=document.getElementById('tool'),A=document.getElementById('a'),B=document.getElementById('b'),clock=document.getElementById('clock');
function snap(st){var d=f.contentDocument,w=f.contentWindow;
  var sb=d.querySelectorAll('#styles button')[st.s];if(!sb.classList.contains('on'))sb.click();
  var yb=[].slice.call(d.querySelectorAll('#years .ychip')).filter(function(b){return b.getAttribute('aria-label')===w.__Y[st.y];})[0];if(yb&&!yb.classList.contains('on'))yb.click();
  [['word',st.w],['goals',st.g],['quote',st.q]].forEach(function(p){var el=d.getElementById(p[0]);if(el.value!==p[1]){el.value=p[1];el.dispatchEvent(new w.Event('input'));}});
  var cv=d.getElementById('cv'),o=document.createElement('canvas');o.width=840;o.height=Math.round(840*cv.height/cv.width);
  o.getContext('2d').drawImage(cv,0,0,o.width,o.height);return o.toDataURL('image/jpeg',.92);}
f.onload=function(){var d=f.contentDocument,w=f.contentWindow;d.getElementById('showGhost').checked=false;
  w.__Y={};d.querySelectorAll('#years .ychip').forEach(function(b,i){w.__Y[{{YKEYS}}[i]]=b.getAttribute('aria-label');});
  w.document.fonts.ready.then(function(){setTimeout(function(){
    var cache={};K.forEach(function(k){var j=JSON.stringify(k[1]);shots.push(cache[j]||(cache[j]=snap(k[1])));});
    A.src=shots[0];clock.style.color=GHOST[K[0][1].s];
    Promise.all([A.decode()]).then(function(){window.__ready=true;});},1500);});};
var cur=-1;
window.__step=function(i){var t=i/FPS,k=0;while(k+1<K.length&&K[k+1][0]<=t)k++;
  var p=new Promise(function(r){requestAnimationFrame(function(){requestAnimationFrame(r);});});
  if(k!==cur){B.src=A.src;B.style.opacity=1;A.src=shots[k];cur=k;clock.style.color=GHOST[K[k][1].s];
    var q=p;p=A.decode().then(function(){return q;});}
  /* the previous screen fades out over FADE seconds above the new one */
  B.style.zIndex=1;var since=t-K[k][0];B.style.opacity=FADE?Math.max(0,1-since/FADE):0;
  return p;};
</script></body></html>"""

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    for name, h1, sub in PINS:
        if only and not re.search(only, name): continue
        html_ = (PAGE.replace("{{FREE}}", FREE).replace("{{H1}}", h1).replace("{{P}}", sub).replace("{{FPS}}", str(FPS))
                 .replace("{{KEYS}}", json.dumps(keyframes(name))).replace("{{YKEYS}}", json.dumps(YEARS)).replace("{{FADE}}", ".35" if name == "styles" else "0"))
        two = len(re.sub("<.*?>", "", h1)) > 30   # a two-line title pushes the phone down
        html_ = html_.replace("{{PHONE_TOP}}", "285" if two else "225").replace("{{P_TOP}}", "1268" if two else "1210")
        page = f"vw-{name}.html"; open(os.path.join(TMP, page), "w", encoding="utf-8").write(html_)
        frames = os.path.join(TMP, f"vw-frames-{name}"); shutil.rmtree(frames, ignore_errors=True)
        subprocess.run(["node", os.path.join(ROOT, "tools", "cdp_frames.mjs"), f"http://127.0.0.1:8765/_pins_batch/{page}", frames, str(FPS * SECONDS)], check=True)
        mp4 = os.path.join(OUT, f"vw-{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
        shutil.copy(os.path.join(frames, f"f_{FPS * SECONDS - 1:04d}.png"), os.path.join(OUT, f"vw-{name}.png"))
        print("wrote", mp4, file=sys.stderr)
