"""Tools: calculators and converters. Each body is HTML + <script>; use SP.fmt(n, digits) for numbers."""
import json
from sp import tool_page, TODAY, PAGES

def tool_flour():
    def body(lang):
        t = {"en": ("Grams of flour", "Cups", "Convert", "Enter an amount, then press Convert.",
                    "1 cup of all-purpose flour weighs about 125 g (spooned and levelled). Packed flour can reach 150 g, which is why recipes by weight are more reliable.",
                    "Based on USDA FoodData Central density for all-purpose flour (125 g per US cup)."),
             "fr": ("Grammes de farine", "Tasses", "Convertir", "Entrez une quantité, puis appuyez sur Convertir.",
                    "1 tasse de farine tout usage pèse environ 125 g (farine déposée à la cuillère et nivelée). Tassée, elle peut atteindre 150 g : c'est pourquoi les recettes au poids sont plus fiables.",
                    "D'après la densité de l'USDA FoodData Central pour la farine tout usage (125 g par tasse américaine).")}[lang]
        return f"""
<div class="tool" id="t">
  <div class="row">
    <div><label for="g">{t[0]}</label><input id="g" type="number" inputmode="decimal" placeholder="250"></div>
    <div><label for="c">{t[1]}</label><input id="c" type="number" inputmode="decimal" placeholder="2"></div>
  </div>
  <button onclick="calc()">{t[2]}</button>
  <div class="result" id="r">{t[3]}</div>
</div>
<p>{t[4]}</p>
<p class="small">{t[5]}</p>
<script>
var PER_CUP = 125;
function calc(){{
  var g = parseFloat(document.getElementById('g').value), c = parseFloat(document.getElementById('c').value), r = document.getElementById('r');
  if (!isNaN(g) && document.activeElement.id !== 'c') {{ r.textContent = SP.fmt(g,0) + ' g = ' + SP.fmt(g/PER_CUP,2) + ' {"cups" if lang=="en" else "tasses"}'; }}
  else if (!isNaN(c)) {{ r.textContent = SP.fmt(c,2) + ' {"cups" if lang=="en" else "tasses"} = ' + SP.fmt(c*PER_CUP,0) + ' g'; }}
}}
document.getElementById('g').addEventListener('input', function(){{ document.getElementById('c').value=''; calc(); }});
document.getElementById('c').addEventListener('input', function(){{ document.getElementById('g').value=''; calc(); }});
</script>"""
    PAGES.append({"section": "tools",
        "en": ("flour-cups-to-grams", "Flour: cups to grams converter", "Convert cups of all-purpose flour to grams and back. 1 cup = 125 g.", body("en")),
        "fr": ("farine-tasses-en-grammes", "Farine : convertir les tasses en grammes", "Convertissez les tasses de farine tout usage en grammes, et l'inverse. 1 tasse = 125 g.", body("fr"))})

def tool_birth():
    def body(lang):
        t = {"en": ("Date of birth", "Pick your date of birth.", "a <b>{dow}</b> · <b>{days}</b> days lived · <b>{weeks}</b> weeks · <b>{months}</b> months · <b>{moons}</b> full moons · about <b>{beats}</b> million heartbeats · <b>{km}</b> million km travelled around the Sun",
                    "Days, weeks and months are counted from your birthday to today. Full moons use the mean synodic month (29.53 days); heartbeats assume an average 72 beats per minute; the distance uses Earth's mean orbital speed of 29.8 km/s. Everything is computed in your browser and nothing is sent anywhere.", "Share", "Download image", "Born on"),
             "fr": ("Date de naissance", "Choisissez votre date de naissance.", "un <b>{dow}</b> · <b>{days}</b> jours vécus · <b>{weeks}</b> semaines · <b>{months}</b> mois · <b>{moons}</b> pleines lunes · environ <b>{beats}</b> millions de battements de cœur · <b>{km}</b> millions de km parcourus autour du Soleil",
                    "Les jours, semaines et mois sont comptés de votre naissance à aujourd'hui. Les pleines lunes utilisent le mois synodique moyen (29,53 jours) ; les battements supposent 72 par minute ; la distance utilise la vitesse orbitale moyenne de la Terre (29,8 km/s). Tout est calculé dans votre navigateur, rien n'est envoyé.", "Partager", "Télécharger l'image", "Né·e le")}[lang]
        return f"""
<div class="tool">
  <label for="bd">{t[0]}</label><input id="bd" type="date" max="{TODAY}">
  <div class="result" id="r">{t[1]}</div>
  <div class="row" id="acts" style="display:none;margin-top:1rem">
    <button onclick="SP.share(document.title, document.getElementById('r').textContent)">{t[4]}</button>
    <button onclick="SP.download(SP.resultCard({{kicker: '{t[6]} ' + document.getElementById('bd').value, title: document.getElementById('r').textContent.split(' · ')[1], subtitle: document.getElementById('r').textContent}}),'sapiopedia-birthday.png')">{t[5]}</button>
  </div>
</div>
<p>{t[3]}</p>
<script>
(function(){{var el=document.getElementById('bd'),o=document.getElementById('r'),H={json.dumps(t[2], ensure_ascii=False)};
el.addEventListener('input',function(){{var r=SP.birth(el.value,'{lang}');if(!r)return;document.getElementById('acts').style.display='grid';
o.innerHTML=H.replace('{{dow}}',r.dow).replace('{{days}}',SP.fmt(r.days,0)).replace('{{weeks}}',SP.fmt(r.weeks,0)).replace('{{months}}',SP.fmt(r.months,0)).replace('{{moons}}',SP.fmt(r.moons,0)).replace('{{beats}}',SP.fmt(r.beats,0)).replace('{{km}}',SP.fmt(r.km,0));}});}})();
</script>"""
    PAGES.append({"section": "tools",
        "en": ("birthday-converter-days-weeks-moons", "Birthday converter: days, weeks, months and full moons", "Enter your date of birth and see how many days, weeks, months, full moons and heartbeats you have lived.", body("en")),
        "fr": ("convertisseur-de-naissance-jours-semaines-lunes", "Convertisseur de naissance : jours, semaines, mois et pleines lunes", "Entrez votre date de naissance et découvrez combien de jours, semaines, mois, pleines lunes et battements de cœur vous avez vécus.", body("fr"))})

def J(x): return json.dumps(x, ensure_ascii=False)

# ---------------------------------------------------------------- 1. butter
def tool_butter():
    def body(lang):
        t = {"en": dict(cups="Cups", tbsp="Tablespoons", g="Grams", sticks="US sticks", hint="Type an amount in any field; the others fill in.",
                        p="Butter is dense and barely compressible, so volume-to-weight conversion is more reliable than for flour or sugar. We use the standard figures: 1 US cup = 227 g, 1 tablespoon = 14.2 g, and 1 US stick (½ cup, 8 tablespoons) = 113 g. European butter is sold by weight, usually in 250 g blocks, so 1 cup is just under a full block.",
                        s="Assumptions: USDA FoodData Central density for butter (227 g per US cup); US stick = 113 g.",
                        fmt="<b>{cups}</b> cups · <b>{tbsp}</b> tbsp · <b>{g}</b> g · <b>{sticks}</b> sticks"),
             "fr": dict(cups="Tasses", tbsp="Cuillères à soupe", g="Grammes", sticks="Bâtonnets américains", hint="Entrez une quantité dans n'importe quel champ ; les autres se remplissent.",
                        p="Le beurre est dense et se tasse à peine : la conversion du volume en poids est donc plus fiable que pour la farine ou le sucre. Nous utilisons les valeurs de référence : 1 tasse américaine (240 ml) = 227 g, 1 cuillère à soupe = 14,2 g et 1 bâtonnet américain (½ tasse, 8 cuillères) = 113 g. En Europe et au Québec, le beurre se vend au poids, souvent en blocs de 250 g ou 454 g : une tasse représente un peu moins d'un bloc de 250 g.",
                        s="Hypothèses : densité du beurre selon l'USDA FoodData Central (227 g par tasse américaine) ; bâtonnet américain = 113 g.",
                        fmt="<b>{cups}</b> tasses · <b>{tbsp}</b> c. à soupe · <b>{g}</b> g · <b>{sticks}</b> bâtonnets")}[lang]
        return f"""
<div class="tool">
  <div class="row">
    <div><label for="cups">{t['cups']}</label><input id="cups" type="number" inputmode="decimal" placeholder="1"></div>
    <div><label for="tbsp">{t['tbsp']}</label><input id="tbsp" type="number" inputmode="decimal" placeholder="16"></div>
    <div><label for="g">{t['g']}</label><input id="g" type="number" inputmode="decimal" placeholder="227"></div>
    <div><label for="sticks">{t['sticks']}</label><input id="sticks" type="number" inputmode="decimal" placeholder="2"></div>
  </div>
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var H={J(t['fmt'])},ids=['cups','tbsp','g','sticks'],perG={{cups:227,tbsp:14.2,g:1,sticks:113}};
function upd(src){{var v=parseFloat(document.getElementById(src).value);if(isNaN(v)||v<0)return;var g=v*perG[src],out={{}};
ids.forEach(function(k){{out[k]=g/perG[k];if(k!==src)document.getElementById(k).value=Math.round(out[k]*1000)/1000;}});
document.getElementById('r').innerHTML=H.replace('{{cups}}',SP.fmt(out.cups,2)).replace('{{tbsp}}',SP.fmt(out.tbsp,1)).replace('{{g}}',SP.fmt(out.g,0)).replace('{{sticks}}',SP.fmt(out.sticks,2));}}
ids.forEach(function(k){{document.getElementById(k).addEventListener('input',function(){{upd(k);}});}});}})();
</script>"""
    tool_page("tools",
        {"en": "butter-cups-tablespoons-grams-sticks-converter", "fr": "beurre-tasses-cuilleres-grammes-batonnets"},
        {"en": "Butter: cups, tablespoons, grams, sticks converter", "fr": "Beurre : tasses, cuillères, grammes et bâtonnets"},
        {"en": "Convert butter between cups, tablespoons, grams and US sticks. 1 cup = 227 g, 1 tbsp = 14.2 g, 1 stick = 113 g.",
         "fr": "Convertissez le beurre entre tasses, cuillères à soupe, grammes et bâtonnets. 1 tasse = 227 g, 1 c. à soupe = 14,2 g."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 2. sugar
def tool_sugar():
    def body(lang):
        t = {"en": dict(type="Type of sugar", types=[("gran", "Granulated (white) sugar", 200), ("brown", "Brown sugar, packed", 220), ("icing", "Icing / powdered sugar", 120)],
                        cups="Cups", g="Grams", hint="Choose a sugar, then type cups or grams.",
                        p="Sugars differ a lot by volume. Granulated sugar packs tightly and weighs about 200 g per US cup; brown sugar is measured packed in the cup and reaches about 220 g; icing sugar is airy and comes to only about 120 g. Changing the type in the menu recalculates the result instantly.",
                        s="Densities from USDA FoodData Central (granulated 200 g, brown packed 220 g, powdered 120 g per US cup).",
                        fmt="<b>{cups}</b> cups = <b>{g}</b> g"),
             "fr": dict(type="Type de sucre", types=[("gran", "Sucre blanc (granulé)", 200), ("brown", "Cassonade / sucre brun, tassé", 220), ("icing", "Sucre glace (à glacer)", 120)],
                        cups="Tasses", g="Grammes", hint="Choisissez un sucre, puis entrez des tasses ou des grammes.",
                        p="Les sucres n'ont pas du tout le même poids pour un même volume. Le sucre blanc se tasse bien et pèse environ 200 g par tasse américaine (240 ml) ; la cassonade, que l'on mesure tassée dans la tasse, atteint environ 220 g ; le sucre glace, très aéré, ne fait qu'environ 120 g. Changer de type dans le menu recalcule aussitôt le résultat.",
                        s="Densités de l'USDA FoodData Central (granulé 200 g, cassonade tassée 220 g, sucre glace 120 g par tasse américaine).",
                        fmt="<b>{cups}</b> tasses = <b>{g}</b> g")}[lang]
        opts = "".join(f'<option value="{v}">{n}</option>' for _, n, v in t['types'])
        return f"""
<div class="tool">
  <label for="st">{t['type']}</label><select id="st">{opts}</select>
  <div class="row">
    <div><label for="c">{t['cups']}</label><input id="c" type="number" inputmode="decimal" placeholder="1"></div>
    <div><label for="g">{t['g']}</label><input id="g" type="number" inputmode="decimal" placeholder="200"></div>
  </div>
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var H={J(t['fmt'])},st=document.getElementById('st'),c=document.getElementById('c'),g=document.getElementById('g'),r=document.getElementById('r'),last='c';
function calc(){{var d=parseFloat(st.value),cv,gv;
if(last==='c'){{cv=parseFloat(c.value);if(isNaN(cv))return;gv=cv*d;g.value=Math.round(gv);}}
else{{gv=parseFloat(g.value);if(isNaN(gv))return;cv=gv/d;c.value=Math.round(cv*100)/100;}}
r.innerHTML=H.replace('{{cups}}',SP.fmt(cv,2)).replace('{{g}}',SP.fmt(gv,0));}}
c.addEventListener('input',function(){{last='c';calc();}});g.addEventListener('input',function(){{last='g';calc();}});st.addEventListener('change',calc);}})();
</script>"""
    tool_page("tools",
        {"en": "sugar-cups-to-grams-converter", "fr": "sucre-tasses-en-grammes"},
        {"en": "Sugar: cups to grams converter (white, brown, icing)", "fr": "Sucre : convertir les tasses en grammes (blanc, cassonade, glace)"},
        {"en": "Convert cups of granulated, brown or icing sugar to grams and back. 1 cup white sugar = 200 g, brown 220 g, icing 120 g.",
         "fr": "Convertissez les tasses de sucre blanc, de cassonade ou de sucre glace en grammes. 1 tasse de sucre blanc = 200 g."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 3. oven
GAS = [("¼", 225, 110), ("½", 250, 120), ("1", 275, 140), ("2", 300, 150), ("3", 325, 170), ("4", 350, 180), ("5", 375, 190), ("6", 400, 200), ("7", 425, 220), ("8", 450, 230), ("9", 475, 240)]
def tool_oven():
    def body(lang):
        t = {"en": dict(f="Fahrenheit (°F)", c="Celsius (°C)", gas="Gas mark", hint="Type a temperature in °F or °C, or a gas mark.",
                        th=("Gas mark", "°F", "°C", "Description"), desc=["very slow", "very slow", "slow", "slow", "moderately slow", "moderate", "moderately hot", "hot", "hot", "very hot", "very hot"],
                        p="The conversion is the exact formula °C = (°F − 32) × 5⁄9, rounded to the nearest degree. Gas marks are a British scale with no formula behind it: each mark corresponds to a conventional temperature, so we show the nearest mark. Recipes usually round oven temperatures anyway: 350 °F is quoted as 180 °C, not 177 °C. For a fan (convection) oven, most manufacturers suggest lowering the temperature by about 20 °C (25 °F).",
                        s="Gas mark table as published in standard British cookery references (mark 4 = 350 °F = 180 °C).",
                        fmt="<b>{f}</b> °F = <b>{c}</b> °C · gas mark <b>{gas}</b>"),
             "fr": dict(f="Fahrenheit (°F)", c="Celsius (°C)", gas="Thermostat britannique (gas mark)", hint="Entrez une température en °F ou en °C, ou un repère gas mark.",
                        th=("Gas mark", "°F", "°C", "Description"), desc=["très doux", "très doux", "doux", "doux", "assez doux", "moyen", "assez chaud", "chaud", "chaud", "très chaud", "très chaud"],
                        p="La conversion applique la formule exacte °C = (°F − 32) × 5⁄9, arrondie au degré. Le « gas mark » est une échelle britannique sans formule : chaque repère correspond à une température conventionnelle, nous affichons donc le repère le plus proche. Les recettes arrondissent de toute façon : 350 °F se lit 180 °C, et non 177 °C. Pour un four à chaleur tournante, la plupart des fabricants conseillent de baisser d'environ 20 °C (25 °F). À noter : le thermostat français (1 à 10) est une autre échelle, où chaque cran vaut 30 °C.",
                        s="Table des gas marks d'après les ouvrages de cuisine britanniques de référence (repère 4 = 350 °F = 180 °C).",
                        fmt="<b>{f}</b> °F = <b>{c}</b> °C · gas mark <b>{gas}</b>")}[lang]
        rows = "".join(f'<tr><td>{g}</td><td>{f}</td><td>{c}</td><td>{d}</td></tr>' for (g, f, c), d in zip(GAS, t['desc']))
        ths = "".join(f"<th style=\"text-align:left\">{h}</th>" for h in t['th'])
        return f"""
<div class="tool">
  <div class="row">
    <div><label for="f">{t['f']}</label><input id="f" type="number" inputmode="decimal" placeholder="350"></div>
    <div><label for="c">{t['c']}</label><input id="c" type="number" inputmode="decimal" placeholder="180"></div>
  </div>
  <label for="gas">{t['gas']}</label><input id="gas" type="number" inputmode="decimal" min="0.25" max="9" step="0.25" placeholder="4">
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<table style="width:100%;border-collapse:collapse;margin:1rem 0 1.5rem;font-size:.95rem"><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>
<p class="small">{t['s']}</p>
<script>
(function(){{var H={J(t['fmt'])},G={J([[0.25,225,110],[0.5,250,120],[1,275,140],[2,300,150],[3,325,170],[4,350,180],[5,375,190],[6,400,200],[7,425,220],[8,450,230],[9,475,240]])};
var f=document.getElementById('f'),c=document.getElementById('c'),gas=document.getElementById('gas'),r=document.getElementById('r');
function gasLabel(m){{return m===0.25?'¼':m===0.5?'½':String(m);}}
function nearestGas(cel){{var best=G[0];G.forEach(function(x){{if(Math.abs(x[2]-cel)<Math.abs(best[2]-cel))best=x;}});return best;}}
function show(fv,cv){{var gm=nearestGas(cv);var lbl=gasLabel(gm[0]);if(cv<100)lbl='— ('+(document.documentElement.lang==='fr'?'trop bas':'too low')+')';if(cv>250)lbl='9+';
r.innerHTML=H.replace('{{f}}',SP.fmt(Math.round(fv),0)).replace('{{c}}',SP.fmt(Math.round(cv),0)).replace('{{gas}}',lbl);}}
f.addEventListener('input',function(){{var v=parseFloat(f.value);if(isNaN(v))return;var cv=(v-32)*5/9;c.value=Math.round(cv);gas.value=nearestGas(cv)[0];show(v,cv);}});
c.addEventListener('input',function(){{var v=parseFloat(c.value);if(isNaN(v))return;var fv=v*9/5+32;f.value=Math.round(fv);gas.value=nearestGas(v)[0];show(fv,v);}});
gas.addEventListener('input',function(){{var v=parseFloat(gas.value);if(isNaN(v))return;var m=null;G.forEach(function(x){{if(x[0]===v)m=x;}});if(!m)return;f.value=m[1];c.value=m[2];show(m[1],m[2]);}});}})();
</script>"""
    tool_page("tools",
        {"en": "oven-temperature-converter-fahrenheit-celsius-gas-mark", "fr": "temperature-du-four-fahrenheit-celsius-gas-mark"},
        {"en": "Oven temperature converter: °F, °C and gas mark", "fr": "Température du four : convertir °F, °C et gas mark"},
        {"en": "Convert oven temperatures between Fahrenheit, Celsius and British gas marks, with a full reference table.",
         "fr": "Convertissez les températures de four entre Fahrenheit, Celsius et gas mark britannique, avec une table de référence."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 4. baby age
def tool_baby():
    def body(lang):
        t = {"en": dict(bd="Baby's date of birth", dd="Due date (optional, for premature babies)", hint="Pick the date of birth.",
                        fmt="<b>{w}</b> weeks and <b>{d}</b> days old · <b>{m}</b> months and <b>{md}</b> days · <b>{days}</b> days in total",
                        corr=" · corrected age: <b>{cw}</b> weeks and <b>{cd}</b> days (born <b>{early}</b> weeks early)",
                        notyet=" · corrected age starts counting from the due date, in <b>{n}</b> days",
                        p="Weeks and days are counted from the birth date to today; months follow the calendar (a baby born on the 15th turns one month old on the 15th of the next month). If you enter a due date earlier than today and later than the birth, we also show the corrected age, counted from the due date instead of the birth date: this is the age paediatricians use to follow the development of premature babies, usually until about 2 years.",
                        s="Corrected (adjusted) age = chronological age minus the weeks born before the due date, as used by paediatric follow-up services. For any concern about growth or development, ask your doctor or midwife."),
             "fr": dict(bd="Date de naissance de bébé", dd="Date prévue d'accouchement (facultatif, pour les bébés prématurés)", hint="Choisissez la date de naissance.",
                        fmt="<b>{w}</b> semaines et <b>{d}</b> jours · <b>{m}</b> mois et <b>{md}</b> jours · <b>{days}</b> jours en tout",
                        corr=" · âge corrigé : <b>{cw}</b> semaines et <b>{cd}</b> jours (né·e <b>{early}</b> semaines avant terme)",
                        notyet=" · l'âge corrigé commencera à compter à la date prévue, dans <b>{n}</b> jours",
                        p="Les semaines et les jours sont comptés de la naissance à aujourd'hui ; les mois suivent le calendrier (un bébé né le 15 a un mois le 15 du mois suivant). Si vous indiquez une date prévue d'accouchement antérieure à aujourd'hui et postérieure à la naissance, nous affichons aussi l'âge corrigé, compté à partir de la date prévue plutôt que de la naissance : c'est l'âge que les pédiatres utilisent pour suivre le développement des bébés prématurés, en général jusqu'à 2 ans environ.",
                        s="Âge corrigé = âge réel moins les semaines de naissance avant le terme, selon l'usage des services de suivi pédiatrique. Pour toute question sur la croissance ou le développement, parlez-en à votre médecin ou à votre sage-femme.")}[lang]
        return f"""
<div class="tool">
  <label for="bd">{t['bd']}</label><input id="bd" type="date" max="{TODAY}">
  <label for="dd">{t['dd']}</label><input id="dd" type="date">
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var T={J({k: t[k] for k in ('fmt', 'corr', 'notyet')})},bd=document.getElementById('bd'),dd=document.getElementById('dd'),r=document.getElementById('r');
function noon(iso){{var d=new Date(iso+'T12:00:00');return isNaN(d)?null:d;}}
function calc(){{if(!bd.value)return;var b=noon(bd.value),t=new Date();t.setHours(12,0,0,0);if(!b||b>t)return;
var days=Math.round((t-b)/864e5),m=(t.getFullYear()-b.getFullYear())*12+(t.getMonth()-b.getMonth())-(t.getDate()<b.getDate()?1:0);
var anchor=new Date(b);anchor.setMonth(anchor.getMonth()+m);var md=Math.round((t-anchor)/864e5);if(md<0){{md=0;}}
var h=T.fmt.replace('{{w}}',SP.fmt(Math.floor(days/7),0)).replace('{{d}}',days%7).replace('{{m}}',SP.fmt(m,0)).replace('{{md}}',md).replace('{{days}}',SP.fmt(days,0));
if(dd.value){{var d=noon(dd.value);if(d&&d>b){{var early=Math.round((d-b)/864e5);if(d<=t){{var cd=Math.round((t-d)/864e5);h+=T.corr.replace('{{cw}}',SP.fmt(Math.floor(cd/7),0)).replace('{{cd}}',cd%7).replace('{{early}}',SP.fmt(early/7,1));}}
else{{h+=T.notyet.replace('{{n}}',SP.fmt(Math.round((d-t)/864e5),0));}}}}}}
r.innerHTML=h;}}
bd.addEventListener('input',calc);dd.addEventListener('input',calc);}})();
</script>"""
    tool_page("tools",
        {"en": "baby-age-calculator-weeks-months-corrected-age", "fr": "age-de-bebe-semaines-mois-age-corrige"},
        {"en": "Baby age calculator: weeks, months and corrected age", "fr": "Âge de bébé en semaines et en mois, avec âge corrigé"},
        {"en": "Enter your baby's birth date to get the age in weeks, days and months, plus the corrected age for premature babies.",
         "fr": "Entrez la date de naissance de bébé pour obtenir son âge en semaines, jours et mois, et l'âge corrigé s'il est né avant terme."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 5. due date
def tool_due():
    def body(lang):
        t = {"en": dict(lmp="First day of your last period", hint="Pick the first day of your last period.",
                        fmt="Due date: <b>{due}</b> · you are <b>{w}</b> weeks and <b>{d}</b> days pregnant · <b>{left}</b> days to go",
                        past="Due date: <b>{due}</b> · that date was <b>{n}</b> days ago",
                        p="This is Naegele's rule, the method used on most pregnancy wheels: the due date is 280 days (40 weeks) after the first day of the last menstrual period. It assumes a regular 28-day cycle with ovulation on day 14. Only about 4 % of babies arrive on the exact date; most are born within two weeks either side. An early ultrasound often gives a more precise date, and your doctor or midwife may adjust it.",
                        s="Naegele's rule (LMP + 280 days). Not a diagnosis: ask your doctor or midwife to confirm your dates."),
             "fr": dict(lmp="Premier jour de vos dernières règles", hint="Choisissez le premier jour de vos dernières règles.",
                        fmt="Date prévue : <b>{due}</b> · vous êtes enceinte de <b>{w}</b> semaines et <b>{d}</b> jours (aménorrhée) · <b>{left}</b> jours restants",
                        past="Date prévue : <b>{due}</b> · cette date est passée depuis <b>{n}</b> jours",
                        p="C'est la règle de Naegele, celle des disques de grossesse : la date prévue tombe 280 jours (40 semaines) après le premier jour des dernières règles. Elle suppose un cycle régulier de 28 jours avec une ovulation au 14e jour. Les semaines affichées sont des semaines d'aménorrhée (SA), celles qu'utilisent les professionnels en France et au Québec. Seuls 4 % environ des bébés naissent le jour exact ; la plupart arrivent dans les deux semaines autour. Une échographie précoce donne souvent une date plus précise, et votre médecin ou votre sage-femme pourra l'ajuster.",
                        s="Règle de Naegele (dernières règles + 280 jours). Ce n'est pas un diagnostic : demandez à votre médecin ou à votre sage-femme de confirmer vos dates.")}[lang]
        return f"""
<div class="tool">
  <label for="lmp">{t['lmp']}</label><input id="lmp" type="date" max="{TODAY}">
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var T={J({k: t[k] for k in ('fmt', 'past')})},el=document.getElementById('lmp'),r=document.getElementById('r'),L='{lang}';
el.addEventListener('input',function(){{if(!el.value)return;var d=new Date(el.value+'T12:00:00');if(isNaN(d))return;var t=new Date();t.setHours(12,0,0,0);
var due=new Date(d);due.setDate(due.getDate()+280);var ds=due.toLocaleDateString(L,{{weekday:'long',day:'numeric',month:'long',year:'numeric'}});
var ga=Math.round((t-d)/864e5);if(ga<0)return;var left=Math.round((due-t)/864e5);
if(left>=0)r.innerHTML=T.fmt.replace('{{due}}',ds).replace('{{w}}',Math.floor(ga/7)).replace('{{d}}',ga%7).replace('{{left}}',SP.fmt(left,0));
else r.innerHTML=T.past.replace('{{due}}',ds).replace('{{n}}',SP.fmt(-left,0));}});}})();
</script>"""
    tool_page("tools",
        {"en": "pregnancy-due-date-calculator", "fr": "date-prevue-d-accouchement-calculateur"},
        {"en": "Pregnancy due date calculator (from your last period)", "fr": "Date prévue d'accouchement : calculateur à partir des dernières règles"},
        {"en": "Enter the first day of your last period to get your due date (Naegele's rule, 280 days) and your current week of pregnancy.",
         "fr": "Entrez le premier jour de vos dernières règles pour connaître la date prévue d'accouchement et votre semaine de grossesse."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 6. sleep
def tool_sleep():
    def body(lang):
        t = {"en": dict(wake="Time you want to wake up", hint="Pick a wake-up time.",
                        head="To wake at <b>{wake}</b>, go to bed at:", line="<b>{t}</b> ({n} cycles, {h} h of sleep)",
                        p="A night's sleep runs in cycles of roughly 90 minutes, from light sleep through deep sleep to REM. Waking at the end of a cycle, rather than in the middle of deep sleep, usually feels easier. The calculator counts back from your alarm: 15 minutes to fall asleep, then 6, 5 or 4 full cycles (9, 7½ or 6 hours of sleep). Most adults need 7 to 9 hours, so the first two lines are the ones to aim for.",
                        s="Assumptions: 90-minute average sleep cycle and 15 minutes to fall asleep (textbook averages; real cycles vary between 70 and 120 minutes). Adult sleep-duration range from the National Sleep Foundation."),
             "fr": dict(wake="Heure à laquelle vous voulez vous lever", hint="Choisissez une heure de réveil.",
                        head="Pour vous lever à <b>{wake}</b>, couchez-vous à :", line="<b>{t}</b> ({n} cycles, {h} h de sommeil)",
                        p="Une nuit se déroule en cycles d'environ 90 minutes, du sommeil léger au sommeil profond puis au sommeil paradoxal. Se réveiller à la fin d'un cycle, plutôt qu'au milieu du sommeil profond, est généralement plus facile. Le calculateur remonte depuis votre réveil : 15 minutes pour s'endormir, puis 6, 5 ou 4 cycles complets (9 h, 7 h 30 ou 6 h de sommeil). La plupart des adultes ont besoin de 7 à 9 heures : visez donc les deux premières lignes.",
                        s="Hypothèses : cycle moyen de 90 minutes et 15 minutes d'endormissement (moyennes de référence ; les cycles réels varient de 70 à 120 minutes). Durée de sommeil adulte selon la National Sleep Foundation.")}[lang]
        return f"""
<div class="tool">
  <label for="wk">{t['wake']}</label><input id="wk" type="time" value="07:00">
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var T={J({k: t[k] for k in ('head', 'line')})},el=document.getElementById('wk'),r=document.getElementById('r'),L='{lang}';
function hm(min){{min=((min%1440)+1440)%1440;var d=new Date(2000,0,1,Math.floor(min/60),min%60);return d.toLocaleTimeString(L,{{hour:'2-digit',minute:'2-digit'}});}}
function calc(){{var v=el.value;if(!v||v.indexOf(':')<0)return;var p=v.split(':'),w=parseInt(p[0],10)*60+parseInt(p[1],10);if(isNaN(w))return;
var h=T.head.replace('{{wake}}',hm(w));[6,5,4].forEach(function(n){{var hrs=n*1.5;h+='<br>'+T.line.replace('{{t}}',hm(w-15-n*90)).replace('{{n}}',n).replace('{{h}}',SP.fmt(hrs,1));}});r.innerHTML=h;}}
el.addEventListener('input',calc);el.addEventListener('change',calc);window.addEventListener('load',calc);}})();
</script>"""
    tool_page("tools",
        {"en": "sleep-calculator-bedtime-90-minute-cycles", "fr": "calculateur-de-sommeil-heure-du-coucher"},
        {"en": "Sleep calculator: when to go to bed to wake up refreshed", "fr": "Calculateur de sommeil : à quelle heure se coucher"},
        {"en": "Choose your wake-up time and get bedtimes based on 90-minute sleep cycles, plus 15 minutes to fall asleep.",
         "fr": "Choisissez votre heure de réveil et obtenez les heures de coucher idéales selon des cycles de 90 minutes."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 7. paint
def tool_paint():
    def body(lang):
        t = {"en": dict(area="Wall area", unit="Unit", m2="m²", ft2="ft²", open="Doors and windows to subtract", coats="Coats", cov="Coverage (m² per litre)", hint="Enter the wall area to paint.",
                        fmt="<b>{l}</b> litres of paint for <b>{a}</b> m² × {c} coats · buy about <b>{buy}</b> L to allow for losses",
                        p="Litres = (wall area − doors and windows) × number of coats ÷ coverage. Wall area is simply the perimeter of the room multiplied by the height of the walls. A standard door is about 2 m² (20 ft²) and an average window 1.5 m² (16 ft²). Coverage depends on the paint and the surface: 10 m²/L is typical for emulsion on a smooth, primed wall; fresh plaster or textured surfaces absorb more, so check the figure on the tin. The “buy” figure adds 10 % for touch-ups and roller losses, rounded up to the half-litre.",
                        s="Default coverage of 10 m² per litre per coat, the usual figure quoted on interior emulsion tins (manufacturers state 8–14 m²/L)."),
             "fr": dict(area="Surface des murs", unit="Unité", m2="m²", ft2="pi²", open="Portes et fenêtres à retirer", coats="Couches", cov="Rendement (m² par litre)", hint="Entrez la surface des murs à peindre.",
                        fmt="<b>{l}</b> litres de peinture pour <b>{a}</b> m² × {c} couches · prévoyez environ <b>{buy}</b> L pour les pertes",
                        p="Litres = (surface des murs − portes et fenêtres) × nombre de couches ÷ rendement. La surface des murs, c'est simplement le périmètre de la pièce multiplié par la hauteur sous plafond. Une porte standard fait environ 2 m² (20 pi²) et une fenêtre moyenne 1,5 m² (16 pi²). Le rendement dépend de la peinture et du support : 10 m²/L est courant pour une peinture acrylique sur un mur lisse et apprêté ; un plâtre neuf ou une surface rugueuse absorbe davantage, vérifiez donc la valeur indiquée sur le pot. Le chiffre « prévoyez » ajoute 10 % pour les retouches et les pertes du rouleau, arrondi au demi-litre supérieur.",
                        s="Rendement par défaut de 10 m² par litre et par couche, valeur habituelle des pots de peinture d'intérieur (les fabricants indiquent 8 à 14 m²/L).")}[lang]
        return f"""
<div class="tool">
  <div class="row">
    <div><label for="a">{t['area']}</label><input id="a" type="number" inputmode="decimal" placeholder="40"></div>
    <div><label for="u">{t['unit']}</label><select id="u"><option value="m2">{t['m2']}</option><option value="ft2">{t['ft2']}</option></select></div>
    <div><label for="o">{t['open']}</label><input id="o" type="number" inputmode="decimal" placeholder="3.5" value="0"></div>
    <div><label for="k">{t['coats']}</label><input id="k" type="number" inputmode="numeric" min="1" max="5" step="1" value="2"></div>
  </div>
  <label for="cv">{t['cov']}</label><input id="cv" type="number" inputmode="decimal" min="1" step="0.5" value="10">
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
(function(){{var H={J(t['fmt'])},$=function(i){{return document.getElementById(i);}},r=$('r');
function calc(){{var a=parseFloat($('a').value),o=parseFloat($('o').value)||0,k=parseInt($('k').value,10)||1,cv=parseFloat($('cv').value)||10;if(isNaN(a))return;
var f=$('u').value==='ft2'?0.09290304:1,net=Math.max(0,(a-o)*f),l=net*k/cv,buy=Math.ceil(l*1.1*2)/2;
r.innerHTML=H.replace('{{l}}',SP.fmt(l,1)).replace('{{a}}',SP.fmt(net,1)).replace('{{c}}',k).replace('{{buy}}',SP.fmt(buy,1));}}
['a','o','k','cv'].forEach(function(i){{$(i).addEventListener('input',calc);}});$('u').addEventListener('change',calc);}})();
</script>"""
    tool_page("tools",
        {"en": "paint-calculator-litres-needed-wall-area", "fr": "calculateur-de-peinture-litres-necessaires"},
        {"en": "Paint calculator: how many litres for your walls", "fr": "Calculateur de peinture : combien de litres pour vos murs"},
        {"en": "Enter the wall area (m² or ft²), coats and coverage to get the litres of paint needed, minus doors and windows.",
         "fr": "Entrez la surface des murs (m² ou pi²), le nombre de couches et le rendement pour obtenir les litres de peinture nécessaires."},
        {"en": body("en"), "fr": body("fr")})

# ---------------------------------------------------------------- 8. tip
def tool_tip():
    def body(lang):
        t = {"en": dict(bill="Bill total", pre="Pre-tax amount (optional, to tip before tax)", tip="Tip (%)", people="People", hint="Enter the bill amount.",
                        fmt="Tip <b>{tip}</b> · total <b>{total}</b> · <b>{pp}</b> per person ({n} people)",
                        p="Tip = amount × percentage; the total is the bill plus the tip, divided equally between everyone at the table. In the United States 15–20 % is standard for table service. In Quebec and the rest of Canada the custom is to tip on the amount before taxes: in Quebec the two sales taxes add up to just under 15 %, which is why many people simply tip the tax amount. Enter the pre-tax figure in the optional field and the tip will be calculated on it while the total still uses the full bill.",
                        s="Percentages are customs, not rules; adjust to local practice and the service you received."),
             "fr": dict(bill="Montant de l'addition", pre="Montant avant taxes (facultatif, pour un pourboire hors taxes)", tip="Pourboire (%)", people="Personnes", hint="Entrez le montant de l'addition.",
                        fmt="Pourboire <b>{tip}</b> · total <b>{total}</b> · <b>{pp}</b> par personne ({n} personnes)",
                        p="Pourboire = montant × pourcentage ; le total est l'addition plus le pourboire, divisé à parts égales entre les convives. Aux États-Unis, 15 à 20 % est la norme au restaurant. Au Québec et dans le reste du Canada, l'usage est de calculer le pourboire sur le montant avant taxes : au Québec, TPS et TVQ totalisent un peu moins de 15 %, d'où l'habitude de laisser simplement l'équivalent des taxes. Indiquez le montant avant taxes dans le champ facultatif : le pourboire sera calculé sur ce montant, et le total tiendra compte de l'addition complète.",
                        s="Les pourcentages sont des usages, non des règles ; adaptez-les à la pratique locale et au service reçu.")}[lang]
        return f"""
<div class="tool">
  <div class="row">
    <div><label for="b">{t['bill']}</label><input id="b" type="number" inputmode="decimal" placeholder="86.50"></div>
    <div><label for="pre">{t['pre']}</label><input id="pre" type="number" inputmode="decimal" placeholder="75.24"></div>
    <div><label for="tp">{t['tip']}</label><input id="tp" type="number" inputmode="decimal" min="0" step="1" value="18"></div>
    <div><label for="n">{t['people']}</label><input id="n" type="number" inputmode="numeric" min="1" step="1" value="2"></div>
  </div>
  <div style="display:flex;gap:.6rem">
    <button type="button" onclick="setTip(15)" style="margin-top:.8rem;padding:.6rem">15 %</button>
    <button type="button" onclick="setTip(18)" style="margin-top:.8rem;padding:.6rem">18 %</button>
    <button type="button" onclick="setTip(20)" style="margin-top:.8rem;padding:.6rem">20 %</button>
  </div>
  <div class="result" id="r">{t['hint']}</div>
</div>
<p>{t['p']}</p>
<p class="small">{t['s']}</p>
<script>
var H={J(t['fmt'])};
function tipCalc(){{var $=function(i){{return document.getElementById(i);}},b=parseFloat($('b').value),pre=parseFloat($('pre').value),p=parseFloat($('tp').value)||0,n=Math.max(1,parseInt($('n').value,10)||1);if(isNaN(b))return;
var base=(!isNaN(pre)&&pre>0&&pre<=b)?pre:b,tip=base*p/100,total=b+tip;
$('r').innerHTML=H.replace('{{tip}}',SP.fmt(tip,2)).replace('{{total}}',SP.fmt(total,2)).replace('{{pp}}',SP.fmt(total/n,2)).replace('{{n}}',n);}}
function setTip(p){{document.getElementById('tp').value=p;tipCalc();}}
['b','pre','tp','n'].forEach(function(i){{document.getElementById(i).addEventListener('input',tipCalc);}});
</script>"""
    tool_page("tools",
        {"en": "tip-calculator-bill-split", "fr": "calculateur-de-pourboire-partage-addition"},
        {"en": "Tip and bill split calculator", "fr": "Calculateur de pourboire et partage de l'addition"},
        {"en": "Enter the bill, tip percentage and number of people to get the tip, the total and each person's share. Presets 15, 18, 20 %.",
         "fr": "Entrez l'addition, le pourcentage de pourboire et le nombre de convives pour obtenir le total et la part de chacun."},
        {"en": body("en"), "fr": body("fr")})


tool_flour(); tool_birth()
tool_butter(); tool_sugar(); tool_oven(); tool_baby(); tool_due(); tool_sleep(); tool_paint(); tool_tip()
