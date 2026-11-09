"""Scratch-off cards (Tools). Original design from Desktop/Sapiopedia/Scratch/scratch-gift.html, made bilingual.
Styles: /assets/scratch.css (scoped under .sg). Logic: /assets/scratch.js. The card lives in the link (#gift=…).
Three versions share the same card: a gift, a pregnancy announcement and a gender reveal. Each version overrides
the base texts (T), and may add one-tap suggestions (picks) and a short guide below the card (more)."""
import html, json
from sp import PAGES

FX = {"en": {"none": "No effect", "confetti": "Confetti", "hearts": "Hearts", "snow": "Falling snow", "pink": "Pink confetti", "blue": "Blue confetti"},
      "fr": {"none": "Aucun effet", "confetti": "Confettis", "hearts": "Cœurs", "snow": "Neige qui tombe", "pink": "Confettis roses", "blue": "Confettis bleus"}}

T = {
    "en": dict(h1="Scratch to reveal", h1em="A gift awaits.", label="Create your card", h2="Make it personal.",
               hint="Write your surprise here. See the card come to life beside it.",
               recipient="Recipient's name", gift="Gift or surprise", message="Personal message (optional)", sender="From (optional)", fx="Reveal effect",
               ph=("e.g. Camille", "e.g. A weekend in Paris", "A few words to make it yours…", "Your name"),
               create="Create & share your gift link →", ready="Your card is ready", readyp="Copy the link and send it by text, email or wherever you like.",
               linklabel="Shareable gift link", copy="Copy", copied="Copied", share="Share card", open="Open recipient view",
               fine="The gift details are included in the link, so anyone with the link can read them. Not for secret codes or confidential information.",
               live="Your live preview", covered="Scratch card", revealed="Revealed message", scratch="Scratch here", canvas="Scratch here to reveal your gift",
               belowCreator="Scratch here with your mouse or finger.", belowRecipient="Scratch the grey card to discover your gift.",
               again="Scratch again", all="Reveal all", footer="A little something, just for you", make="Make your own scratch card →",
               forPrefix="FOR ", forAnyone="A GIFT FOR YOU", giftFallback="A lovely surprise", shareTitle="A gift awaits", shareText="I have a little surprise for you.",
               picksLabel="Ideas", fxs=("none", "confetti", "hearts", "snow"), fxDefault="confetti",
               defaults={"recipient": "Camille", "gift": "A weekend in Paris", "message": "Just because you deserve something wonderful.", "sender": "With love"}),
    "fr": dict(h1="À gratter", h1em="Une surprise vous attend.", label="Créez votre carte", h2="Rendez-la personnelle.",
               hint="Écrivez votre surprise ici. La carte prend vie à côté.",
               recipient="Prénom du destinataire", gift="Cadeau ou surprise", message="Message personnel (facultatif)", sender="De la part de (facultatif)", fx="Effet à la découverte",
               ph=("ex. Camille", "ex. Un week-end à Paris", "Quelques mots bien à vous…", "Votre prénom"),
               create="Créer et partager le lien du cadeau →", ready="Votre carte est prête", readyp="Copiez le lien et envoyez-le par texto, courriel ou où vous voulez.",
               linklabel="Lien du cadeau à partager", copy="Copier", copied="Copié", share="Partager la carte", open="Voir comme le destinataire",
               fine="Le contenu du cadeau est inscrit dans le lien : toute personne qui a le lien peut le lire. À éviter pour des codes secrets ou des informations confidentielles.",
               live="Aperçu en direct", covered="Carte à gratter", revealed="Message révélé", scratch="Grattez ici", canvas="Grattez ici pour découvrir votre cadeau",
               belowCreator="Grattez avec la souris ou le doigt.", belowRecipient="Grattez la carte grise pour découvrir votre cadeau.",
               again="Gratter à nouveau", all="Tout révéler", footer="Un petit quelque chose, rien que pour vous", make="Créer votre propre carte à gratter →",
               forPrefix="POUR ", forAnyone="UN CADEAU POUR VOUS", giftFallback="Une jolie surprise", shareTitle="Une surprise vous attend", shareText="J'ai une petite surprise pour vous.",
               picksLabel="Idées", fxs=("none", "confetti", "hearts", "snow"), fxDefault="confetti",
               defaults={"recipient": "Camille", "gift": "Un week-end à Paris", "message": "Juste parce que vous méritez quelque chose de merveilleux.", "sender": "Avec amour"}),
}

PREGNANCY = {
    "en": dict(h1em="Some big news awaits.", label="Create your announcement", h2="Share the news your way.",
               hint="Write who it's for and the news. They scratch the card on their phone to find out.",
               recipient="Who is it for?", gift="The big news", message="A detail to add (optional)",
               ph=("e.g. Mom and Dad", "e.g. You're going to be grandparents!", "e.g. Baby arrives in June", "e.g. Sam and Alex"),
               create="Create & share your announcement link →", ready="Your announcement is ready",
               readyp="Send the link by text or email, or open it together and watch them scratch.",
               linklabel="Shareable announcement link", share="Share announcement",
               fine="The news is included in the link, so anyone with the link can read it. Send it only to the people you want to tell.",
               canvas="Scratch here to reveal the news", belowRecipient="Scratch the grey card to discover the news.",
               footer="Some news is too good to just say", make="Make your own announcement card →",
               forAnyone="SOME BIG NEWS FOR YOU", giftFallback="Some very big news", shareTitle="Some big news awaits", shareText="I have some news to share with you.",
               defaults={"recipient": "Mom and Dad", "gift": "You're going to be grandparents!", "message": "Baby arrives in June. We couldn't wait to tell you.", "sender": "Love, Sam and Alex"},
               picks=[("You're going to be grandparents!", None), ("You're going to be an aunt!", None), ("You're going to be an uncle!", None),
                      ("You're going to be a big sister!", None), ("You're going to be a big brother!", None), ("We're having a baby!", None),
                      ("You're going to be a dad!", None), ("You're going to be great-grandparents!", None)],
               more=("How it works", ["Write who the card is for and your news. Pick an idea above or write your own.",
                                      "Add a detail if you like: the due date, a first ultrasound, a nickname for the baby.",
                                      "Create the link and send it. They scratch the grey card on their phone, and the confetti starts as the news appears."],
                     "Wording ideas", [("For future grandparents", "You're going to be grandparents! · Your new title: Grandma, starting in June · Clear your calendar for babysitting"),
                                       ("For a brother or sister", "You're going to be an aunt! · Promoted to uncle · Someone small will call you Auntie soon"),
                                       ("For an older child", "You're going to be a big sister! · Big brother, reporting for duty in June"),
                                       ("For your partner", "You're going to be a dad! · We're having a baby! · Two pink lines this morning")],
                     "If you are announcing to several people, make one card each: everyone sees their own name, and you can watch each reaction.")),
    "fr": dict(h1em="Une grande nouvelle vous attend.", label="Créez votre annonce", h2="Annoncez-le à votre façon.",
               hint="Indiquez à qui s'adresse l'annonce et la nouvelle. La personne gratte la carte sur son téléphone pour la découvrir.",
               recipient="Pour qui ?", gift="La grande nouvelle", message="Un détail à ajouter (facultatif)",
               ph=("ex. Papa et maman", "ex. Vous allez être grands-parents !", "ex. Bébé arrive en juin", "ex. Léa et Max"),
               create="Créer et partager le lien de l'annonce →", ready="Votre annonce est prête",
               readyp="Envoyez le lien par texto ou par courriel, ou ouvrez-le ensemble et regardez la personne gratter.",
               linklabel="Lien de l'annonce à partager", share="Partager l'annonce",
               fine="La nouvelle est inscrite dans le lien : toute personne qui a le lien peut la lire. Envoyez-le seulement aux personnes à qui vous voulez l'annoncer.",
               canvas="Grattez ici pour découvrir la nouvelle", belowRecipient="Grattez la carte grise pour découvrir la nouvelle.",
               footer="Certaines nouvelles méritent mieux qu'un simple message", make="Créer votre propre carte d'annonce →",
               forAnyone="UNE GRANDE NOUVELLE POUR VOUS", giftFallback="Une très grande nouvelle", shareTitle="Une grande nouvelle vous attend", shareText="J'ai une nouvelle à vous annoncer.",
               defaults={"recipient": "Papa et maman", "gift": "Vous allez être grands-parents !", "message": "Bébé arrive en juin. On avait hâte de vous le dire.", "sender": "Avec amour, Léa et Max"},
               picks=[("Vous allez être grands-parents !", None), ("Tu vas être tante !", None), ("Tu vas être oncle !", None),
                      ("Tu vas être grande sœur !", None), ("Tu vas être grand frère !", None), ("On attend un bébé !", None),
                      ("Tu vas être papa !", None), ("Vous allez être arrière-grands-parents !", None)],
               more=("Comment ça marche", ["Indiquez à qui s'adresse la carte et votre nouvelle. Choisissez une idée ci-dessus ou écrivez la vôtre.",
                                           "Ajoutez un détail si vous voulez : la date prévue, une première échographie, un surnom pour bébé.",
                                           "Créez le lien et envoyez-le. La personne gratte la carte grise sur son téléphone, et les confettis partent quand la nouvelle apparaît."],
                     "Idées de messages", [("Pour les futurs grands-parents", "Vous allez être grands-parents ! · Nouveau titre : mamie, à partir de juin · Libérez vos samedis pour le gardiennage"),
                                           ("Pour un frère ou une sœur", "Tu vas être tante ! · Promu tonton · Quelqu'un de tout petit va bientôt t'appeler tatie"),
                                           ("Pour un aîné", "Tu vas être grande sœur ! · Grand frère, en poste à partir de juin"),
                                           ("Pour votre partenaire", "Tu vas être papa ! · On attend un bébé ! · Deux barres roses ce matin")],
                     "Pour l'annoncer à plusieurs personnes, faites une carte pour chacune : chacun voit son prénom, et vous pouvez voir chaque réaction.")),
}

GENDER = {
    "en": dict(h1em="Boy or girl?", label="Create your reveal", h2="Make the big moment theirs.",
               hint="Pick the answer, add a message, and send the link. The colour of the confetti gives it away too.",
               recipient="Who is it for?", gift="The reveal", message="A message (optional)",
               ph=("e.g. Grandma and Grandpa", "e.g. It's a girl!", "e.g. See you at the baby shower!", "e.g. Sam and Alex"),
               create="Create & share your reveal link →", ready="Your reveal is ready",
               readyp="Send the link, or open it on a big screen at the party and let someone scratch.",
               linklabel="Shareable reveal link", share="Share reveal",
               fine="The answer is included in the link, so anyone with the link can read it. Keep it to the people you want to surprise.",
               canvas="Scratch here to find out", belowRecipient="Scratch the grey card to find out: boy or girl?",
               footer="Boy or girl? Scratch to find out", make="Make your own gender reveal card →",
               forAnyone="THE BIG REVEAL", giftFallback="A very happy surprise", shareTitle="Boy or girl? Scratch to find out", shareText="Scratch the card to find out if it's a boy or a girl.",
               fxs=("none", "pink", "blue", "confetti", "hearts"), fxDefault="pink",
               defaults={"recipient": "Grandma and Grandpa", "gift": "It's a girl!", "message": "Due in May. We can't wait for you to meet the baby.", "sender": "Love, Sam and Alex"},
               picks=[("It's a girl!", "pink"), ("It's a boy!", "blue"), ("It's twins: a girl and a boy!", "confetti"), ("It's twin girls!", "pink"), ("It's twin boys!", "blue")],
               more=("How it works", ["Pick the answer above: the confetti turns pink or blue to match. Or write your own.",
                                      "Add who it's for and a message: the due date, the name if you've chosen it.",
                                      "Create the link and send it, or open it at the party and hand the phone to the guest of honour."],
                     "Ideas for the big moment", [("At a party", "Open the link on a TV or a tablet and let the grandparents scratch it in front of everyone."),
                                                  ("At a distance", "Send one card to each family and ask them to film the moment they scratch it."),
                                                  ("If you don't know yet yourselves", "Give the envelope from the ultrasound to a friend. They make the card and send you the link, and you find out together.")],
                     'Still looking for a name? Browse <a href="/en/names/french/">9,128 French first names</a>, for girls, boys or both, with their pronunciation.')),
    "fr": dict(h1em="Fille ou garçon ?", label="Créez votre révélation", h2="Rendez le grand moment inoubliable.",
               hint="Choisissez la réponse, ajoutez un message et envoyez le lien. La couleur des confettis vend aussi la mèche.",
               recipient="Pour qui ?", gift="La révélation", message="Un message (facultatif)",
               ph=("ex. Mamie et papi", "ex. C'est une fille !", "ex. À bientôt au baby shower !", "ex. Léa et Max"),
               create="Créer et partager le lien →", ready="Votre carte est prête",
               readyp="Envoyez le lien, ou ouvrez-le sur grand écran pendant la fête et laissez quelqu'un gratter.",
               linklabel="Lien de la révélation à partager", share="Partager la carte",
               fine="La réponse est inscrite dans le lien : toute personne qui a le lien peut la lire. Gardez-le pour les personnes que vous voulez surprendre.",
               canvas="Grattez ici pour le découvrir", belowRecipient="Grattez la carte grise : fille ou garçon ?",
               footer="Fille ou garçon ? Grattez pour le savoir", make="Créer votre propre carte →",
               forAnyone="LA GRANDE RÉVÉLATION", giftFallback="Une très belle surprise", shareTitle="Fille ou garçon ? Grattez pour le savoir", shareText="Grattez la carte pour savoir si c'est une fille ou un garçon.",
               fxs=("none", "pink", "blue", "confetti", "hearts"), fxDefault="pink",
               defaults={"recipient": "Mamie et papi", "gift": "C'est une fille !", "message": "Naissance prévue en mai. On a hâte que vous rencontriez bébé.", "sender": "Avec amour, Léa et Max"},
               picks=[("C'est une fille !", "pink"), ("C'est un garçon !", "blue"), ("Des jumeaux : une fille et un garçon !", "confetti"), ("Des jumelles !", "pink"), ("Des jumeaux !", "blue")],
               more=("Comment ça marche", ["Choisissez la réponse ci-dessus : les confettis deviennent roses ou bleus. Ou écrivez la vôtre.",
                                           "Indiquez pour qui et ajoutez un message : la date prévue, le prénom s'il est choisi.",
                                           "Créez le lien et envoyez-le, ou ouvrez-le pendant la fête et tendez le téléphone à l'invité d'honneur."],
                     "Idées pour le grand moment", [("Pendant la fête", "Ouvrez le lien sur une télé ou une tablette et laissez les grands-parents gratter devant tout le monde."),
                                                    ("À distance", "Envoyez une carte à chaque famille et demandez-leur de filmer le moment où ils grattent."),
                                                    ("Si vous ne le savez pas encore vous-mêmes", "Confiez l'enveloppe de l'échographie à une amie. Elle crée la carte et vous envoie le lien : vous le découvrez ensemble.")],
                     'Vous cherchez encore un prénom ? Parcourez <a href="/fr/prenoms/francais/">9 128 prénoms français</a>, filles, garçons ou mixtes, avec leur prononciation.')),
}

def body(lang, over=None):
    v = {**T[lang], **((over or {}).get(lang, {}))}
    t = {k: (html.escape(x) if isinstance(x, str) else x) for k, x in v.items()}
    d = v["defaults"]; ph = [html.escape(p) for p in v["ph"]]
    js = {k: v[k] for k in ("copy", "copied", "belowCreator", "belowRecipient", "forPrefix", "forAnyone", "giftFallback", "shareTitle", "shareText", "defaults")}
    js["lang"] = lang; js["fx"] = v["fxDefault"]
    fx = "".join(f'<button type="button" role="radio" data-fx="{k}" aria-checked="{"true" if k == v["fxDefault"] else "false"}">{FX[lang][k]}</button>' for k in v["fxs"])
    picks = ""
    if v.get("picks"):
        picks = (f'<div class="field"><span class="fx-label">{t["picksLabel"]}</span><div class="quick-choice">'
                 + "".join(f'<button type="button" data-pick="{html.escape(p)}"{f" data-pickfx={chr(34)}{f}{chr(34)}" if f else ""}>{html.escape(p)}</button>' for p, f in v["picks"])
                 + '</div></div>')
    more = ""
    if v.get("more"):
        h_steps, steps, h_ideas, ideas, note = v["more"]
        more = (f'<section class="sg-more"><h2>{html.escape(h_steps)}</h2><ol>' + "".join(f"<li>{html.escape(s)}</li>" for s in steps) + "</ol>"
                f'<h2>{html.escape(h_ideas)}</h2><dl>' + "".join(f"<dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd>" for a, b in ideas) + f"</dl><p>{note}</p></section>")
    return f'''<link rel="stylesheet" href="/assets/scratch.css">
<div class="sg">
<div class="shell">
 <header class="masthead"><h1>{t["h1"]} <em>{t["h1em"]}</em></h1></header>
 <section class="workspace">
  <section class="form-panel" id="creator" aria-label="{t["label"]}">
   <p class="section-label">{t["label"]}</p><h2>{t["h2"]}</h2><p class="hint">{t["hint"]}</p>
   {picks}
   <div class="field"><label for="recipient">{t["recipient"]}</label><input id="recipient" maxlength="70" placeholder="{ph[0]}" value="{html.escape(d["recipient"])}"></div>
   <div class="field"><label for="gift">{t["gift"]}</label><input id="gift" maxlength="120" placeholder="{ph[1]}" value="{html.escape(d["gift"])}"></div>
   <div class="field"><label for="message">{t["message"]}</label><textarea id="message" maxlength="320" placeholder="{ph[2]}">{html.escape(d["message"])}</textarea></div>
   <div class="field"><label for="sender">{t["sender"]}</label><input id="sender" maxlength="70" placeholder="{ph[3]}" value="{html.escape(d["sender"])}"></div>
   <div class="field fx-field"><span class="fx-label" id="fx-label">{t["fx"]}</span><div class="fx-choice" role="radiogroup" aria-labelledby="fx-label">{fx}</div></div>
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
{more}
<script>window.SG={json.dumps(js, ensure_ascii=False)};</script>
<script src="/assets/scratch.js"></script>
<script>/* one-tap ideas: fill the main line (and pick the matching effect) */
document.querySelectorAll('.sg [data-pick]').forEach(function(b){{b.addEventListener('click',function(){{var g=document.getElementById('gift');g.value=b.dataset.pick;g.dispatchEvent(new Event('input'));
var f=b.dataset.pickfx&&document.querySelector('.sg [data-fx="'+b.dataset.pickfx+'"]');if(f)f.click();}});}});</script>'''

PAGES.append({"section": "tools", "wide": True, "main_class": "scratch",
    "en": ("scratch-gift-card", "Scratch-off gift card", "Write a surprise, then send a link: the person you love scratches the card to reveal your gift. Free, no sign-up.", body("en")),
    "fr": ("carte-cadeau-a-gratter", "Carte cadeau à gratter", "Écrivez une surprise et envoyez un lien : la personne grattera la carte pour découvrir votre cadeau. Gratuit, sans inscription.", body("fr"))})
PAGES.append({"section": "tools", "wide": True, "main_class": "scratch",
    "en": ("pregnancy-announcement-scratch-card", "Scratch-off pregnancy announcement",
           "Announce a pregnancy with a scratch-off card sent as a link: they scratch it on their phone and find out they're going to be grandparents, an aunt or a big sister. Free, no sign-up.", body("en", PREGNANCY)),
    "fr": ("annonce-de-grossesse-a-gratter", "Annonce de grossesse à gratter",
           "Annoncez une grossesse avec une carte à gratter envoyée par lien : on la gratte sur son téléphone et on découvre qu'on va être grands-parents, tante ou grande sœur. Gratuit, sans inscription.", body("fr", PREGNANCY))})
PAGES.append({"section": "tools", "wide": True, "main_class": "scratch",
    "en": ("gender-reveal-scratch-card", "Gender reveal scratch card",
           "Boy or girl? Make a scratch-off card and send the link: pink or blue confetti bursts out when they scratch it. For parties or at a distance. Free, no sign-up.", body("en", GENDER)),
    "fr": ("carte-a-gratter-reveler-sexe-bebe", "Carte à gratter pour révéler le sexe du bébé",
           "Fille ou garçon ? Créez une carte à gratter et envoyez le lien : des confettis roses ou bleus jaillissent quand on la gratte. Pendant la fête ou à distance. Gratuit, sans inscription.", body("fr", GENDER))})
