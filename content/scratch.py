"""Scratch-off gift card (Tools). Original design from Desktop/Sapiopedia/Scratch/scratch-gift.html, made bilingual.
Styles: /assets/scratch.css (scoped under .sg). Logic: /assets/scratch.js. The gift lives in the link (#gift=…)."""
import html, json
from sp import PAGES

T = {
    "en": dict(h1="Scratch to reveal", h1em="A gift awaits.", label="Create your card", h2="Make it personal.",
               hint="Write your surprise here. See the card come to life beside it.",
               recipient="Recipient's name", gift="Gift or surprise", message="Personal message (optional)", sender="From (optional)",
               ph=("e.g. Camille", "e.g. A weekend in Paris", "A few words to make it yours…", "Your name"),
               create="Create & share your gift link →", ready="Your card is ready", readyp="Copy the link and send it by text, email or wherever you like.",
               linklabel="Shareable gift link", copy="Copy", copied="Copied", share="Share card", open="Open recipient view",
               fine="The gift details are included in the link, so anyone with the link can read them. Not for secret codes or confidential information.",
               live="Your live preview", covered="Scratch card", revealed="Revealed message", scratch="Scratch here", canvas="Scratch here to reveal your gift",
               belowCreator="Scratch here with your mouse or finger.", belowRecipient="Scratch the grey card to discover your gift.",
               again="Scratch again", all="Reveal all", footer="A little something, just for you", make="Make your own scratch card →",
               forPrefix="FOR ", forAnyone="A GIFT FOR YOU", giftFallback="A lovely surprise", shareTitle="A gift awaits", shareText="I have a little surprise for you.",
               defaults={"recipient": "Camille", "gift": "A weekend in Paris", "message": "Just because you deserve something wonderful.", "sender": "With love"}),
    "fr": dict(h1="À gratter", h1em="Une surprise vous attend.", label="Créez votre carte", h2="Rendez-la personnelle.",
               hint="Écrivez votre surprise ici. La carte prend vie à côté.",
               recipient="Prénom du destinataire", gift="Cadeau ou surprise", message="Message personnel (facultatif)", sender="De la part de (facultatif)",
               ph=("ex. Camille", "ex. Un week-end à Paris", "Quelques mots bien à vous…", "Votre prénom"),
               create="Créer et partager le lien du cadeau →", ready="Votre carte est prête", readyp="Copiez le lien et envoyez-le par texto, courriel ou où vous voulez.",
               linklabel="Lien du cadeau à partager", copy="Copier", copied="Copié", share="Partager la carte", open="Voir comme le destinataire",
               fine="Le contenu du cadeau est inscrit dans le lien : toute personne qui a le lien peut le lire. À éviter pour des codes secrets ou des informations confidentielles.",
               live="Aperçu en direct", covered="Carte à gratter", revealed="Message révélé", scratch="Grattez ici", canvas="Grattez ici pour découvrir votre cadeau",
               belowCreator="Grattez avec la souris ou le doigt.", belowRecipient="Grattez la carte grise pour découvrir votre cadeau.",
               again="Gratter à nouveau", all="Tout révéler", footer="Un petit quelque chose, rien que pour vous", make="Créer votre propre carte à gratter →",
               forPrefix="POUR ", forAnyone="UN CADEAU POUR VOUS", giftFallback="Une jolie surprise", shareTitle="Une surprise vous attend", shareText="J'ai une petite surprise pour vous.",
               defaults={"recipient": "Camille", "gift": "Un week-end à Paris", "message": "Juste parce que vous méritez quelque chose de merveilleux.", "sender": "Avec amour"}),
}

def body(lang):
    t = {k: (html.escape(v) if isinstance(v, str) else v) for k, v in T[lang].items()}
    d = T[lang]["defaults"]; ph = [html.escape(p) for p in T[lang]["ph"]]
    js = {k: T[lang][k] for k in ("copy", "copied", "belowCreator", "belowRecipient", "forPrefix", "forAnyone", "giftFallback", "shareTitle", "shareText", "defaults")}
    js["lang"] = lang
    return f'''<link rel="stylesheet" href="/assets/scratch.css">
<div class="sg">
<div class="shell">
 <header class="masthead"><h1>{t["h1"]} <em>{t["h1em"]}</em></h1></header>
 <section class="workspace">
  <section class="form-panel" id="creator" aria-label="{t["label"]}">
   <p class="section-label">{t["label"]}</p><h2>{t["h2"]}</h2><p class="hint">{t["hint"]}</p>
   <div class="field"><label for="recipient">{t["recipient"]}</label><input id="recipient" maxlength="70" placeholder="{ph[0]}" value="{html.escape(d["recipient"])}"></div>
   <div class="field"><label for="gift">{t["gift"]}</label><input id="gift" maxlength="120" placeholder="{ph[1]}" value="{html.escape(d["gift"])}"></div>
   <div class="field"><label for="message">{t["message"]}</label><textarea id="message" maxlength="320" placeholder="{ph[2]}">{html.escape(d["message"])}</textarea></div>
   <div class="field"><label for="sender">{t["sender"]}</label><input id="sender" maxlength="70" placeholder="{ph[3]}" value="{html.escape(d["sender"])}"></div>
   <button class="btn full" id="createLink" type="button">{t["create"]}</button>
   <div class="share-panel" id="sharePanel" hidden>
    <p class="section-label">{t["ready"]}</p><p>{t["readyp"]}</p>
    <div class="link-field"><input readonly id="shareUrl" aria-label="{t["linklabel"]}"><button type="button" id="copy">{t["copy"]}</button></div>
    <div class="small-actions"><button type="button" class="btn outline" id="share">{t["share"]}</button><button type="button" class="btn ghost" id="openGift">{t["open"]}</button></div>
    <p class="fine-print">{t["fine"]}</p>
   </div>
  </section>
  <section class="preview-area" aria-label="{t["covered"]}">
   <div class="preview-head"><p class="preview-sub">{t["live"]}</p>
    <div class="view-switch"><button type="button" id="coveredMode" aria-pressed="true">{t["covered"]}</button><button type="button" id="revealedMode" aria-pressed="false">{t["revealed"]}</button></div>
   </div>
   <div class="card-frame"><div class="card-inner"><div class="scratch-surface" id="surface">
    <div class="gift-content" aria-live="polite"><span class="gift-to" id="displayTo"></span><div class="gift-value" id="displayGift"></div><div class="gift-message" id="displayMessage"></div><div class="gift-from" id="displayFrom"></div></div>
    <canvas class="scratch-canvas" id="scratch" aria-label="{t["canvas"]}"></canvas><div class="scratch-caption" id="scratchCaption">{t["scratch"]}</div>
   </div></div></div>
   <p class="preview-foot" id="belowCard">{t["belowCreator"]}</p>
   <div class="preview-buttons"><button type="button" id="reset">{t["again"]}</button><button type="button" id="reveal">{t["all"]}</button></div>
  </section>
 </section>
 <footer class="footer">{t["footer"].upper()}<br><a href="#" id="makeOwn" class="make-own">{t["make"]}</a></footer>
</div>
</div>
<script>window.SG={json.dumps(js, ensure_ascii=False)};</script>
<script src="/assets/scratch.js"></script>'''

PAGES.append({"section": "tools", "wide": True, "main_class": "scratch",
    "en": ("scratch-gift-card", "Scratch-off gift card", "Write a surprise, then send a link: the person you love scratches the card to reveal your gift. Free, no sign-up.", body("en")),
    "fr": ("carte-cadeau-a-gratter", "Carte cadeau à gratter", "Écrivez une surprise et envoyez un lien : la personne grattera la carte pour découvrir votre cadeau. Gratuit, sans inscription.", body("fr"))})
