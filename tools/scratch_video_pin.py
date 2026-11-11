#!/usr/bin/env python3
"""Video pins of the scratch card: a fingertip scratches the real card on a phone, the coating fades and the effect plays.
Same frame as 09c-scratch-hearts plus the free badge. The card runs on a clock the page steps itself (60 ticks a second,
one frame every two ticks), so the strokes, the fade and the hearts are the same on every run.
Needs the local server (python3 -m http.server 8765 from the repo root).
Writes Desktop/Sapiopedia/Pinterest/batch-2026-11/vs-<name>.mp4 and a cover image vs-<name>.png (the revealed gift).
ONLY=<regex> limits which pins are made."""
import base64, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "_pins_batch"); os.makedirs(TMP, exist_ok=True)
OUT = os.path.expanduser("~/Desktop/Sapiopedia/Pinterest/batch-2026-11")
FPS, SECONDS = 30, 9
FREE = ('<style>.free{position:absolute;top:18px;right:40px;z-index:5;background:#8E2F48;color:#fff;font:700 24px "Source Sans 3",sans-serif;letter-spacing:.12em;'
        'text-transform:uppercase;padding:9px 18px;border-radius:999px;box-shadow:0 4px 12px -4px rgba(42,31,38,.4)}</style><div class="free">Free · No sign-up</div>')

PINS = [  # name, gift, h1, line under the phone
 ("hearts-lastminute", {"recipient": "Maya", "gift": "Dinner at our favourite place", "message": "Happy birthday, love.", "sender": "Eli", "fx": "hearts"},
  "Perfect for <em>last-minute virtual gifts</em>", "Ready in a minute, sent as a link. They scratch, the gift appears."),
 ("confetti-tickets", {"recipient": "Nora", "gift": "Two tickets to the show", "message": "Saturday, front row!", "sender": "Ben", "fx": "confetti"},
  "Scratch… <em>and confetti!</em>", "Choose the ending: confetti, hearts or snow."),
 ("snow-christmas", {"recipient": "Mia", "gift": "Ice skating, then hot chocolate", "message": "Saturday, 3 pm. Bring mittens.", "sender": "Leo", "fx": "snow"},
  "A Christmas gift they <em>scratch to open</em>", "Write it, send the link, let it snow."),
 ("hearts-distance", {"recipient": "Sam", "gift": "A flight to see you in March", "message": "Only 112 days to go.", "sender": "Alex", "fx": "hearts"},
  "A gift for someone <em>far away</em>", "Sent as a link. They scratch it on their phone, wherever they are."),
]

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:1500px;overflow:hidden;background:#F4E6E9;color:#2A1F26;font-family:'Source Sans 3',sans-serif;position:relative}
h1{position:absolute;left:70px;right:70px;top:100px;margin:0;font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:84px;line-height:1;letter-spacing:-.03em;text-align:center}
h1 em{color:#A83A57}
.phone{position:absolute;left:50%;top:{{PHONE_TOP}}px;transform:translateX(-50%);width:452px;height:930px;border-radius:58px;background:#1f1a1c;padding:16px;box-shadow:0 30px 60px -30px rgba(42,31,38,.55)}
.phone iframe{width:336px;height:718px;transform:scale(1.25);transform-origin:0 0;border:0;border-radius:35px;background:#F7E9EC;display:block}
p{position:absolute;left:50px;right:50px;top:{{P_TOP}}px;margin:0;font-size:32px;line-height:1.35;color:#4A3C42;text-align:center}
.u{position:absolute;left:0;right:0;bottom:46px;text-align:center;font-size:27px;letter-spacing:.04em;color:#6E5A62}.u b{color:#2A1F26;font-weight:600}
#tip{position:absolute;left:0;top:0;width:62px;height:62px;margin:-31px 0 0 -31px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.75) 0,rgba(255,255,255,.45) 45%,rgba(255,255,255,0) 72%);
 border:2px solid rgba(142,47,72,.55);box-shadow:0 6px 18px rgba(42,31,38,.25);opacity:0;z-index:4;pointer-events:none}
</style></head><body>{{FREE}}
<h1>{{H1}}</h1><div class="phone"><iframe id="f" src="{{URL}}"></iframe></div><p>{{P}}</p><div class="u"><b>sapiopedia.com</b> · scratch-off gift card</div><div id="tip"></div>
<script>
var f=document.getElementById('f'),tip=document.getElementById('tip'),FPS={{FPS}};
function ready(cb){var c=f.contentDocument&&f.contentDocument.getElementById("scratch");if(c&&c.width>0){var a=c.getContext("2d").getImageData(c.width>>1,c.height>>1,1,1).data[3];if(a>200)return cb();}setTimeout(function(){ready(cb);},150);}
f.onload=function(){setTimeout(function(){var w=f.contentWindow,d=f.contentDocument;w.dispatchEvent(new Event("resize"));ready(function(){
  w.addEventListener("resize",function(e){e.stopImmediatePropagation();},true);
  /* the card's own clock: performance.now, requestAnimationFrame, CSS transitions and Math.random all follow T */
  var T=0,Q=[],s=20261111;w.performance.now=function(){return T;};w.requestAnimationFrame=function(cb){Q.push(cb);return Q.length;};
  w.Math.random=function(){s=(s+0x6D2B79F5)|0;var t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
  function anims(){d.getAnimations().forEach(function(a){if(a._t0==null){a._t0=T;a.pause();}a.currentTime=Math.min(T-a._t0,5000);});}
  var c=d.getElementById('scratch'),r=c.getBoundingClientRect(),W=r.width,H=r.height,fr=f.getBoundingClientRect();
  function ev(t,x,y){c.dispatchEvent(new PointerEvent(t,{clientX:r.left+x,clientY:r.top+y,pointerId:1,pointerType:"touch",bubbles:true,cancelable:true}));}
  /* the strokes, as points every 9 px (about 540 px a second); null = finger lifted and moved to the next stroke */
  var S=[[.10,.90,.46,23,9,.05],[.86,.16,.60,19,11,-.05],[.26,.76,.33,17,7,0],[.20,.62,.72,21,8,0],[.70,.30,.22,15,6,.04],[.15,.85,.52,20,10,.02]],P=[];
  S.forEach(function(k,j){var a=[],dir=k[1]>k[0]?1:-1;for(var x=W*k[0];dir>0?x<W*k[1]:x>W*k[1];x+=9*dir)a.push([x,H*k[2]+Math.sin(x/k[3])*k[4]+(x-W*k[0])*k[5]]);
    if(j){var p=P[P.length-1],q=a[0];for(var i=1;i<=8;i++)P.push({lift:1,x:p.x+(q[0]-p.x)*i/8,y:p.y+(q[1]-p.y)*i/8});}
    a.forEach(function(p,i){P.push({x:p[0],y:p[1],down:i===0,up:i===a.length-1});});});
  var START=Math.round(1.1*60),k=0,tipA=0,done=false,lastXY=[P[0].x,P[0].y];
  function tick(n){T+=1000/60;
    if(n>=START-24&&!done)tipA=Math.min(1,tipA+1/12);
    if(n>=START&&!done&&k<P.length){var p=P[k++];if(p.down)ev('pointerdown',p.x,p.y);else if(!p.lift)ev('pointermove',p.x,p.y);if(p.up)ev('pointerup',p.x,p.y);lastXY=[p.x,p.y];tip._lift=p.lift;}
    if(!done&&c.classList.contains('gone')){done=true;ev('pointerup',lastXY[0],lastXY[1]);}
    if(done)tipA=Math.max(0,tipA-1/12);
    var q=Q;Q=[];q.forEach(function(cb){cb(T);});anims();}
  var tick0=0;
  window.__step=function(i){while(tick0<=i*60/FPS){tick(tick0);tick0++;}
    tip.style.opacity=tipA;tip.style.transform='translate('+(fr.left+(r.left+lastXY[0])*1.25)+'px,'+(fr.top+(r.top+lastXY[1])*1.25)+'px) scale('+(tip._lift?1.12:.92)+')';
    return new Promise(function(res){requestAnimationFrame(function(){requestAnimationFrame(res);});});};
  window.__ready=true;
});},2500);};
</script></body></html>"""

def b64(d): return base64.urlsafe_b64encode(json.dumps(d, ensure_ascii=False).encode()).decode().rstrip("=")

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    for name, gift, h1, sub in PINS:
        if only and not re.search(only, name): continue
        two = len(re.sub("<.*?>", "", h1)) > 30   # a two-line title pushes the phone down
        html_ = (PAGE.replace("{{FREE}}", FREE).replace("{{H1}}", h1).replace("{{P}}", sub).replace("{{FPS}}", str(FPS))
                 .replace("{{URL}}", "/en/tools/scratch-gift-card/#gift=" + b64(gift)).replace("{{PHONE_TOP}}", "300" if two else "240").replace("{{P_TOP}}", "1268" if two else "1210"))
        page = f"vs-{name}.html"; open(os.path.join(TMP, page), "w", encoding="utf-8").write(html_)
        frames = os.path.join(TMP, f"vs-frames-{name}"); shutil.rmtree(frames, ignore_errors=True)
        subprocess.run(["node", os.path.join(ROOT, "tools", "cdp_frames.mjs"), f"http://127.0.0.1:8765/_pins_batch/{page}", frames, str(FPS * SECONDS)], check=True)
        mp4 = os.path.join(OUT, f"vs-{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", mp4], check=True)
        shutil.copy(os.path.join(frames, f"f_{FPS * SECONDS - 1:04d}.png"), os.path.join(OUT, f"vs-{name}.png"))
        print("wrote", mp4, file=sys.stderr)
