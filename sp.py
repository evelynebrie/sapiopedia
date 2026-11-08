"""Shared page registry + helpers used by build.py and the content/ modules."""
import json, datetime
TODAY = datetime.date.today().isoformat()
# ---------------------------------------------------------------- content
# Pages are registered by the modules in content/ (quizzes.py, tools.py, meanings.py, names.py, games.py).
# Each page: {"section": key, "en": (slug, title, description, body_html), "fr": (...)}
PAGES = []

def quiz_page(section, slug, title, desc, Q, R, kicker=None):
    """Generic 4-result quiz. slug/title/desc/kicker/Q/R are dicts {lang: ...}.
    Q[lang] = [(question, [opt A, opt B, opt C, opt D]), ...]  (option k scores result k)
    R[lang] = [(name, colour_hex, text), ...]  (4 entries)"""
    T = {"en": ("Start", "Your result:", "Share", "Download image", "Try again", "Question", "of"),
         "fr": ("Commencer", "Votre résultat :", "Partager", "Télécharger l'image", "Recommencer", "Question", "sur")}
    def body(lang):
        t = T[lang]; k = (kicker or {}).get(lang, t[1])
        return f"""
<div class="tool" id="quiz">
  <div id="qbox"><button onclick="startQ()">{t[0]}</button></div>
  <div id="res" style="display:none">
    <div class="result" id="rtitle"></div>
    <p id="rtext"></p>
    <img id="rimg" alt="" style="width:100%;max-width:420px;border-radius:12px;display:block;margin:1rem auto">
    <div class="row">
      <button onclick="SP.share(document.title, document.getElementById('rtitle').textContent)">{t[2]}</button>
      <button onclick="SP.download(document.getElementById('rimg').src,'sapiopedia-{slug['en']}.png')">{t[3]}</button>
    </div>
    <p class="small"><a href="#" onclick="startQ();return false">{t[4]}</a></p>
  </div>
</div>
<script>
var Q = {json.dumps(Q[lang], ensure_ascii=False)}, R = {json.dumps(R[lang], ensure_ascii=False)}, K = {json.dumps(k, ensure_ascii=False)}, i = 0, score = [0,0,0,0];
function startQ(){{ i = 0; score = [0,0,0,0]; document.getElementById('res').style.display='none'; document.getElementById('qbox').style.display='block'; show(); }}
function show(){{
  var q = Q[i], h = '<p class="small">{t[5]} ' + (i+1) + ' {t[6]} ' + Q.length + '</p><h2 style="margin-top:.2rem">' + q[0] + '</h2>';
  for (var k = 0; k < 4; k++) h += '<button style="margin-top:.5rem" onclick="pick(' + k + ')">' + q[1][k] + '</button>';
  document.getElementById('qbox').innerHTML = h; window.scrollTo({{top: document.getElementById('quiz').offsetTop - 20, behavior: 'smooth'}});
}}
function pick(k){{ score[k]++; i++; if (i < Q.length) show(); else finish(); }}
function finish(){{
  var best = score.indexOf(Math.max.apply(null, score)), r = R[best];
  document.getElementById('qbox').style.display='none'; document.getElementById('res').style.display='block';
  document.getElementById('rtitle').innerHTML = K + ' <b>' + r[0] + '</b>';
  document.getElementById('rtext').textContent = r[2];
  document.getElementById('rimg').src = SP.resultCard({{color: r[1], kicker: K, title: r[0], subtitle: r[2]}});
}}
</script>"""
    PAGES.append({"section": section, "en": (slug["en"], title["en"], desc["en"], body("en")), "fr": (slug["fr"], title["fr"], desc["fr"], body("fr"))})

def article_page(section, slug, title, desc, body):
    """Static article. slug/title/desc/body are dicts {lang: ...}; body is HTML (h2, p, ul, table...)."""
    PAGES.append({"section": section, "en": (slug["en"], title["en"], desc["en"], body["en"]), "fr": (slug["fr"], title["fr"], desc["fr"], body["fr"])})

def tool_page(section, slug, title, desc, body):
    """Interactive tool. body is a dict {lang: html+script}. Use SP.fmt() for numbers."""
    PAGES.append({"section": section, "en": (slug["en"], title["en"], desc["en"], body["en"]), "fr": (slug["fr"], title["fr"], desc["fr"], body["fr"])})


