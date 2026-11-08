"""Feng Shui Room Planner: interactive tool. Logic in /assets/fengshui.js, French strings in /assets/fengshui-fr.js."""
from sp import PAGES

TXT = {
 "en": dict(room="Room", room_aria="Room shape", open_aria="Doors, windows and mirrors", north="North", drag_arrow="drag the arrow",
    dial_aria="North arrow: drag to turn, or use the arrow keys", plan_aria="Room plan", trash="Drag here to remove",
    good="Good", caution="Caution", avoid="Avoid", export="Export PNG",
    add="Add furniture", add_sub="It lands on its best spot and turns to face the room. Drag to try other places.", furn_aria="Furniture",
    check="Room check", inroom="In your room", clear="Clear room",
    about_h="How the planner reads your room",
    about="""<p>The planner applies the classic rules of <strong>form-school</strong> feng shui to a simple floor plan: the <em>command position</em> (seeing the door without being in line with it), a solid wall behind the bed, sofa and desk, no furniture in the straight line between a door and a window, and clear paths from the bed to every opening. It adds a few <strong>compass-school</strong> preferences once you point the arrow north, such as sleeping in the north or east half of the room.</p>
<p>Each piece gets a verdict: <strong>good</strong>, <strong>caution</strong> or <strong>avoid</strong>. While a piece is selected, the floor is coloured to show how it would score anywhere in the room. Your layout is saved in your browser only; nothing is sent anywhere.</p>
<p class="small">Feng shui is a cultural tradition, not a science. Treat the advice as a design checklist for a calmer room, not as a prediction.</p>"""),
 "fr": dict(room="Pièce", room_aria="Forme de la pièce", open_aria="Portes, fenêtres et miroirs", north="Nord", drag_arrow="glissez la flèche",
    dial_aria="Flèche du nord : glissez pour la faire pivoter, ou utilisez les flèches du clavier", plan_aria="Plan de la pièce", trash="Glissez ici pour retirer",
    good="Favorable", caution="Prudence", avoid="À éviter", export="Exporter en PNG",
    add="Ajouter un meuble", add_sub="Il se place au meilleur endroit, tourné vers la pièce. Glissez-le pour essayer d'autres places.", furn_aria="Meubles",
    check="Bilan de la pièce", inroom="Dans votre pièce", clear="Vider la pièce",
    about_h="Comment le planificateur lit votre pièce",
    about="""<p>Le planificateur applique à un plan simple les règles classiques du feng shui de l'<strong>école des formes</strong> : la <em>position de commandement</em> (voir la porte sans être dans son axe), un mur plein derrière le lit, le canapé et le bureau, aucun meuble sur la ligne droite entre une porte et une fenêtre, et des passages dégagés du lit vers chaque ouverture. Une fois la flèche orientée vers le nord, il ajoute quelques préférences de l'<strong>école de la boussole</strong>, comme dormir dans la moitié nord ou est de la pièce.</p>
<p>Chaque meuble reçoit un verdict : <strong>favorable</strong>, <strong>prudence</strong> ou <strong>à éviter</strong>. Quand un meuble est sélectionné, le sol se colore pour montrer sa note partout dans la pièce. Votre plan est enregistré uniquement dans votre navigateur ; rien n'est envoyé.</p>
<p class="small">Le feng shui est une tradition culturelle, pas une science. Voyez ces conseils comme une liste de vérification pour une pièce plus apaisante, pas comme une prédiction.</p>"""),
}

def body(lang):
    t = TXT[lang]
    fr = '<script src="/assets/fengshui-fr.js"></script>' if lang == "fr" else ""
    return f"""<link rel="stylesheet" href="/assets/fengshui.css">
<div class="fs">
<div class="grid">
  <div class="sheet work">
    <div class="toolbar">
      <div class="tgroup" id="shapes" role="group" aria-label="{t['room_aria']}"><span class="tlabel">{t['room']}</span></div>
      <div class="tgroup" id="openings" role="group" aria-label="{t['open_aria']}"></div>
      <div class="compass">
        <span class="deg"><b>{t['north']}</b><br>{t['drag_arrow']}</span>
        <svg id="dial" viewBox="-30 -30 60 60" tabindex="0" role="slider" aria-label="{t['dial_aria']}" aria-valuemin="0" aria-valuemax="355"></svg>
      </div>
    </div>
    <div class="stage">
      <svg id="plan" viewBox="0 0 640 640" aria-label="{t['plan_aria']}"></svg>
      <div class="trash" id="trash" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/></svg><span>{t['trash']}</span></div>
    </div>
    <div class="status"><span id="mode"></span>
      <span class="key"><span><i style="background:var(--good-bg);box-shadow:inset 0 0 0 1px var(--good)"></i>{t['good']}</span><span><i style="background:var(--warn-bg);box-shadow:inset 0 0 0 1px var(--warn)"></i>{t['caution']}</span><span><i style="background:var(--bad-bg);box-shadow:inset 0 0 0 1px var(--bad)"></i>{t['avoid']}</span></span>
      <span class="exp"><button type="button" class="chip solid" id="export" hidden>{t['export']}</button><span id="exp-msg" class="muted" style="font-size:13px"></span></span>
    </div>
    <div class="furn">
      <h2>{t['add']} <span>{t['add_sub']}</span></h2>
      <div class="pieces" id="pieces" role="group" aria-label="{t['furn_aria']}"></div>
    </div>
  </div>
  <div class="side">
    <div class="sheet detail" id="detail" aria-live="polite"></div>
    <div class="sheet block">
      <h2>{t['check']}</h2>
      <ul class="notes" id="notes"></ul>
    </div>
    <div class="sheet block">
      <div class="frow" style="justify-content:space-between;margin-bottom:6px"><h2 style="margin:0">{t['inroom']}</h2><button type="button" class="linkbtn" id="clear">{t['clear']}</button></div>
      <div class="tally" id="tally"></div>
      <ul class="flist" id="list"></ul>
    </div>
  </div>
</div>
</div>
<section class="fs-intro"><h2>{t['about_h']}</h2>{t['about']}</section>
{fr}<script src="/assets/fengshui.js"></script>"""

PAGES.append({"section": "tools", "wide": True,
    "en": ("fengshui", "Feng Shui Room Planner",
           "Draw your room, add your door, windows and furniture, and see where each piece works best according to feng shui.", body("en")),
    "fr": ("fengshui", "Planificateur de pièce feng shui",
           "Tracez votre pièce, ajoutez porte, fenêtres et meubles, et voyez où chaque meuble est le mieux placé selon le feng shui.", body("fr"))})
