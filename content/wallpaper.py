"""2027 phone wallpaper (Tools): word of the year, goals and dreams, quote of the year, drawn on a canvas at the phone's exact size.
Original page: Desktop/Sapiopedia/Phone_Background, made bilingual. Styles: /assets/wallpaper.css (scoped under .wp). Logic: /assets/wallpaper.js."""
import html, json
from sp import PAGES

T = {
 "en": dict(clock="Friday 1 January", ghost="Show where the clock sits (not in the download)", style="Style", year="The year · 10 styles", phone="Phone",
    sizes=["iPhone (standard: 15, 16, 17)", "iPhone Pro (16 Pro, 17 Pro)", "iPhone Pro Max / Plus", "Android (most phones)", "Android (high resolution)"],
    word="Word of the year", word_v="Bloom", ideas="Ideas:", goals="Goals and dreams", goals_ph="One per line, up to 7",
    goals_v="See the sea in Portugal\nRead 24 books\nSunday dinners, phones off\nFinish my first quilt\nLearn to make bread",
    goals_hint="One per line, up to 7, about 32 characters each.", quote="Quote of the year", quote_v="Slowly, then all at once.",
    dl="Download my wallpaper", share="Share", link="Copy edit link", aria="Wallpaper preview",
    how="On iPhone: open the image, tap Share, then “Use as Wallpaper”. On Android: open the image, then “Set as wallpaper”.",
    more=("How it works", "<p>Everything is drawn in your browser at the exact resolution of your phone, so the wallpaper stays sharp. Nothing is sent anywhere: your goals stay on your phone. The top third of the image is left clear for the clock and the date; tick the box under the preview to see where they will sit.</p>"
          "<p>To change it later, tap <em>Copy edit link</em>: the link keeps your words, goals and style, and opens the editor exactly as you left it.</p>"),
    js={}),
 "fr": dict(clock="vendredi 1 janvier", ghost="Montrer où se place l'horloge (pas dans l'image)", style="Style", year="L'année · 10 styles", phone="Téléphone",
    sizes=["iPhone (standard : 15, 16, 17)", "iPhone Pro (16 Pro, 17 Pro)", "iPhone Pro Max / Plus", "Android (la plupart des téléphones)", "Android (haute résolution)"],
    word="Mot de l'année", word_v="Éclore", ideas="Idées :", goals="Objectifs et rêves", goals_ph="Un par ligne, jusqu'à 7",
    goals_v="Voir la mer au Portugal\nLire 24 livres\nSoupers sans téléphone\nFinir ma courtepointe\nApprendre à faire du pain",
    goals_hint="Un par ligne, jusqu'à 7, environ 32 caractères chacun.", quote="Citation de l'année", quote_v="Lentement, puis tout d'un coup.",
    dl="Télécharger mon fond d'écran", share="Partager", link="Copier le lien de modification", aria="Aperçu du fond d'écran",
    how="Sur iPhone : ouvrez l'image, touchez Partager, puis « Utiliser comme fond d'écran ». Sur Android : ouvrez l'image, puis « Définir comme fond d'écran ».",
    more=("Comment ça marche", "<p>Tout est dessiné dans votre navigateur, à la résolution exacte de votre téléphone : le fond d'écran reste net. Rien n'est envoyé nulle part, vos objectifs restent sur votre téléphone. Le tiers supérieur de l'image reste libre pour l'heure et la date ; cochez la case sous l'aperçu pour voir où elles se placeront.</p>"
          "<p>Pour le modifier plus tard, touchez <em>Copier le lien de modification</em> : le lien garde vos mots, vos objectifs et votre style, et rouvre l'éditeur tel que vous l'avez laissé.</p>"),
    js=dict(almanac="Almanach", night="Ciel de nuit", riso="Riso rose",
            words=["Éclore", "Courage", "Calme", "Joie", "Racines", "Voyager", "Audace", "Douceur", "Assez", "Créer"],
            quotes=["Lentement, puis tout d'un coup.", "Le courage avant le confort.", "Un petit pas chaque jour.", "Commence là où tu es.", "Simple et doux."],
            years={"riso": "Riso", "italic": "Italique douce", "light": "Fin et aéré", "stacked": "Superposé", "vintage": "Vieux livre", "moon": "Lune",
                   "halftone": "Trame", "arc": "Arc", "shadow": "Ombre portée", "outline": "Contour"},
            kWord="MON MOT DE L'ANNÉE", kGoals="OBJECTIFS ET RÊVES", kQuote="CITATION DE L'ANNÉE", file="mon-fond-ecran-2027.png",
            saved="Enregistré. Choisissez-le comme écran de verrouillage depuis vos photos.", shareTitle="Mon 2027", shareText="Fait avec sapiopedia.com",
            copied="Lien copié : ouvrez-le plus tard pour modifier votre fond d'écran.", ql="« ", qr=" »")),
}
SIZES = ["1179x2556", "1206x2622", "1290x2796", "1080x2400", "1440x3200"]

def body(lang):
    t = T[lang]; e = lambda k: html.escape(t[k])
    opts = "".join(f'<option value="{v}">{html.escape(n)}</option>' for v, n in zip(SIZES, t["sizes"]))
    return f'''<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IM+Fell+English+SC&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="/assets/wallpaper.css">
<div class="wp">
<div class="app">
  <div class="preview">
    <div class="phone" id="phone">
      <canvas id="cv" aria-label="{e("aria")}"></canvas>
      <div class="ghost" id="ghost"><div class="d">{e("clock")}</div><div class="t">9:41</div></div>
    </div>
    <p class="small" style="margin-top:10px"><label class="tog" style="font-weight:400"><input type="checkbox" id="showGhost" checked> {e("ghost")}</label></p>
  </div>
  <div class="panel">
    <div class="k">{e("style")}</div>
    <div class="chips" id="styles"></div>
    <div class="k">{e("year")}</div>
    <div class="chips" id="years"></div>
    <div class="k">{e("phone")}</div>
    <select id="size" aria-label="{e("phone")}">{opts}</select>
    <div class="k"><label class="tog"><input type="checkbox" id="onWord" checked> {e("word")}</label></div>
    <input type="text" id="word" maxlength="14" value="{e("word_v")}" aria-label="{e("word")}">
    <div class="small" style="margin-top:6px">{e("ideas")} <span id="wordIdeas"></span></div>
    <div class="k"><label class="tog"><input type="checkbox" id="onGoals" checked> {e("goals")}</label></div>
    <textarea id="goals" rows="6" placeholder="{e("goals_ph")}" aria-label="{e("goals")}">{e("goals_v")}</textarea>
    <div class="small">{e("goals_hint")}</div>
    <div class="k"><label class="tog"><input type="checkbox" id="onQuote" checked> {e("quote")}</label></div>
    <input type="text" id="quote" maxlength="60" value="{e("quote_v")}" aria-label="{e("quote")}">
    <div class="small" style="margin-top:6px">{e("ideas")} <span id="quoteIdeas"></span></div>
    <div class="btns">
      <button class="btn" id="dl" type="button">{e("dl")}</button>
      <button class="btn ghostbtn" id="share" type="button">{e("share")}</button>
      <button class="btn ghostbtn" id="link" type="button">{e("link")}</button>
    </div>
    <div class="err" id="msg" role="status"></div>
    <p class="small">{e("how")}</p>
  </div>
</div>
<section class="wp-more"><h2>{html.escape(t["more"][0])}</h2>{t["more"][1]}</section>
</div>
<script>window.WP={json.dumps(t["js"], ensure_ascii=False)};</script>
<script src="/assets/wallpaper.js"></script>'''

PAGES.append({"section": "tools", "wide": True,
    "en": ("2027-phone-wallpaper", "Your 2027 phone wallpaper",
           "Make a 2027 phone wallpaper with your word of the year, your goals and dreams, and your quote of the year. Ten styles for the year, made for your phone's exact screen. Free, no sign-up.", body("en")),
    "fr": ("fond-ecran-2027", "Votre fond d'écran 2027",
           "Créez un fond d'écran 2027 pour votre téléphone avec votre mot de l'année, vos objectifs et vos rêves, et votre citation de l'année. Dix styles, au format exact de votre écran. Gratuit, sans inscription.", body("fr"))})
