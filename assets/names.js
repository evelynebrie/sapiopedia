/* Sapiopedia: French first names index. Gender lists, search (accents ignored), A–Z, and a card per name with its recording. */
(function () {
  "use strict";
  var C = window.NF || {}, list = document.getElementById("nf-list"), q = document.getElementById("nf-q"), shown = document.getElementById("nf-shown"), none = document.getElementById("nf-none");
  var fold = function (s) { return String(s).toLowerCase().replace(/œ/g, "oe").replace(/æ/g, "ae").normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  var items = Array.prototype.map.call(list.querySelectorAll("li"), function (li) { var a = li.querySelector("a"); return { li: li, g: li.dataset.g, k: fold(a.textContent) }; });
  var sections = list.querySelectorAll(".nf-l"), filter = "all";
  var nf = new Intl.NumberFormat(C.lang || "en");
  function apply() {
    var v = fold(q.value.trim()), n = 0;
    items.forEach(function (it) { var hit = !v || it.k.indexOf(v) === 0 || (v.length > 2 && it.k.indexOf(v) > 0); it.li.classList.toggle("x", !hit); if (hit && (filter === "all" || it.g === filter)) n++; });
    sections.forEach(function (s) { s.hidden = !Array.prototype.some.call(s.querySelectorAll("li"), function (li) { return !li.classList.contains("x") && (filter === "all" || li.dataset.g === filter); }); });
    document.querySelectorAll(".dd-az a").forEach(function (a) { var s = document.getElementById("l-" + a.dataset.l); a.style.opacity = s && !s.hidden ? "" : ".3"; });
    shown.textContent = C.shown.replace("{n}", nf.format(n));
    none.hidden = n > 0; if (!n) none.textContent = C.none.replace("{q}", q.value);
  }
  document.querySelectorAll(".nf-seg button").forEach(function (b) {
    b.addEventListener("click", function () { filter = b.dataset.f; list.dataset.f = filter;
      document.querySelectorAll(".nf-seg button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); apply(); });
  });
  q.addEventListener("input", apply);
  q.addEventListener("keydown", function (e) { if (e.key === "Enter") { var first = items.find(function (it) { return !it.li.classList.contains("x") && (filter === "all" || it.g === filter); }); if (first) first.li.querySelector("a").click(); } });

  /* ---------- name card ---------- */
  var data = null, card = document.getElementById("nf-card"), box = card.querySelector(".nf-box"), audio = new Audio(), last = null;
  function load() { if (!data) data = fetch("/assets/names-fr.json").then(function (r) { return r.json(); }); return data; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var SYM = { f: "♀", m: "♂", n: "⚥", u: "" };
  var FRL = { English: "anglais", Spanish: "espagnol", Italian: "italien", German: "allemand", Portuguese: "portugais", Dutch: "néerlandais", Polish: "polonais",
    Russian: "russe", Greek: "grec", Latin: "latin", Arabic: "arabe", Hebrew: "hébreu", Chinese: "chinois", Japanese: "japonais", Czech: "tchèque", Hungarian: "hongrois",
    Swedish: "suédois", Danish: "danois", Norwegian: "norvégien", Finnish: "finnois", Catalan: "catalan", Breton: "breton", Basque: "basque", Corsican: "corse",
    Occitan: "occitan", Romanian: "roumain", Turkish: "turc", Lithuanian: "lituanien", Latvian: "letton", Irish: "irlandais", Welsh: "gallois", Ukrainian: "ukrainien",
    Slovak: "slovaque", Croatian: "croate", Slovenian: "slovène" };
  var FRC = { "Great Britain": "Royaume-Uni", Ireland: "Irlande", "United States": "États-Unis", Italy: "Italie", Malta: "Malte", Portugal: "Portugal", Spain: "Espagne",
    France: "France", Belgium: "Belgique", Luxembourg: "Luxembourg", Netherlands: "Pays-Bas", "East Frisia": "Frise orientale", Germany: "Allemagne", Austria: "Autriche",
    Switzerland: "Suisse", Iceland: "Islande", Denmark: "Danemark", Norway: "Norvège", Sweden: "Suède", Finland: "Finlande", Estonia: "Estonie", Latvia: "Lettonie",
    Lithuania: "Lituanie", Poland: "Pologne", "Czech Republic": "Tchéquie", Slovakia: "Slovaquie", Hungary: "Hongrie", Romania: "Roumanie", Bulgaria: "Bulgarie",
    Croatia: "Croatie", Serbia: "Serbie", Slovenia: "Slovénie", Greece: "Grèce", Russia: "Russie", Ukraine: "Ukraine", Turkey: "Turquie", Israel: "Israël",
    China: "Chine", Japan: "Japon", Korea: "Corée", Vietnam: "Viêt Nam", "Arabia/Persia": "Monde arabe et Iran", "India/Sri Lanka": "Inde et Sri Lanka" };
  var FR = C.lang === "fr";
  var L = FR ? { glance: "En bref", gender: "Genre", origin: "Origine", first: "Première mention", pron: "Prononciation", comp: "Prénoms composés",
      meaning: "Origine et sens", bears: "Qui le porte", where: "Où on le donne", world: "Dans d'autres langues", lit: "En littérature", src: "Sources",
      women: "femmes", men: "hommes", bearsTxt: "{f} % des personnes qui portent ce prénom en France sont des femmes, {m} % des hommes.",
      gshort: { f: "Féminin", m: "Masculin", n: "Féminin et masculin (mixte)", u: "Non indiqué" }, book: "Prénoms français", around: "vers" }
    : { glance: "At a glance", gender: "Gender", origin: "Origin", first: "First recorded", pron: "Pronunciation", comp: "Compound names",
      meaning: "Origin and meaning", bears: "Who bears it", where: "Where it is given", world: "Around the world", lit: "In literature", src: "Sources",
      women: "women", men: "men", bearsTxt: "In France, {f}% of people with this name are women and {m}% are men.",
      gshort: { f: "Feminine", m: "Masculine", n: "Feminine and masculine (unisex)", u: "Not recorded" }, book: "French Names", around: "around", inFrench: "In French, from the French Wiktionary:" };
  function origin(r) { if (!r.o) return ""; return FR ? r.o.charAt(0).toUpperCase() + r.o.slice(1) : r.oe; }
  function leadLine(name, r) {
    var o = r.o, at = r.att ? r.att.replace(/^c\.\s*/, "") : "";
    if (!o && !at) return "";
    if (FR) { var kind = { f: "Prénom féminin français", m: "Prénom masculin français", n: "Prénom mixte français", u: "Prénom français" }[r.g];
      return kind + (o ? (/^[aeiouyhéèâ]/i.test(o) ? ", issu de l'" + o : ", issu du " + o) : "") + (at ? ", attesté vers " + at : "") + "."; }
    var kindE = { f: "A French girl's name", m: "A French boy's name", n: "A French name for girls and boys", u: "A French first name" }[r.g];
    return kindE + (r.oe ? " of " + r.oe + " origin" : "") + (at ? ", first recorded around " + at : "") + ".";
  }
  function h3(t) { return "<h3>" + t + "</h3>"; }
  function open(name, id) {
    load().then(function (D) {
      var r = D[name] || { g: "u" };
      var seen = {}, vis = items.filter(function (it) { var n = it.li.querySelector("a").dataset.n; if (seen[n] || it.li.classList.contains("x") || !(filter === "all" || it.g === filter)) return false; seen[n] = 1; return true; });
      var i = vis.findIndex(function (it) { return it.li.querySelector("a").dataset.n === name; });
      var prev = i > 0 ? vis[i - 1].li.querySelector("a") : null, next = i >= 0 && i + 1 < vis.length ? vis[i + 1].li.querySelector("a") : null;
      var gl = function (a, arrow) { return a ? '<a href="' + a.getAttribute("href") + '" data-go="' + esc(a.dataset.n) + '">' + (arrow === "l" ? "← " : "") + esc(a.dataset.n) + (arrow === "r" ? " →" : "") + "</a>" : "<span></span>"; };
      var rows = "<tr><th>" + L.gender + "</th><td>" + L.gshort[r.g] + "</td></tr>" +
        (r.o ? "<tr><th>" + L.origin + "</th><td>" + esc(origin(r)) + "</td></tr>" : "") +
        (r.att ? "<tr><th>" + L.first + "</th><td>" + esc(r.att.replace(/^c\.\s*/, (FR ? "vers " : "about "))) + "</td></tr>" : "") +
        (r.ipa ? "<tr><th>" + L.pron + "</th><td>" + esc(r.ipa) + "</td></tr>" : "") +
        (r.v ? "<tr><th>" + C.also + "</th><td>" + esc(r.v.join(", ")) + "</td></tr>" : "") +
        (r.der ? "<tr><th>" + L.comp + "</th><td>" + esc(r.der.join(", ")) + "</td></tr>" : "");
      var html = '<div class="guide">' + gl(prev, "l") + "<span>" + L.book + " · " + esc(name.charAt(0).toUpperCase()) + "</span>" + gl(next, "r") + "</div>" +
        '<div class="hd"><span class="ini" aria-hidden="true">' + esc(name.charAt(0)) + '</span><div><h2 id="nf-name">' + esc(name) + "</h2>" +
        '<p class="gl">' + (r.ipa ? '<span class="ipa">' + esc(r.ipa) + "</span>" : "") + (SYM[r.g] ? '<b class="' + r.g + '">' + SYM[r.g] + "</b>" : "") + "<span>" + esc(C.g[r.g]) + "</span>" +
        (r.mp3 ? '<button type="button" class="hear" aria-pressed="false">▶ ' + C.hear + "</button>" : "") + "</p></div></div>" +
        (leadLine(name, r) ? '<p class="lead">' + esc(leadLine(name, r)) + "</p>" : "") +
        "<section>" + h3(L.glance) + '<table class="facts">' + rows + "</table></section>" +
        (r.et ? "<section>" + h3(L.meaning) + (FR ? "" : '<p class="small-note">' + L.inFrench + "</p>") + '<p class="body"' + (FR ? "" : ' lang="fr"') + ">" + esc(r.et) + "</p></section>" : "") +
        (r.pf != null ? '<section class="bearers">' + h3(L.bears) + '<div class="split" role="img" aria-label="' + esc(L.bearsTxt.replace("{f}", r.pf).replace("{m}", 100 - r.pf)) + '"><span class="f" style="width:' + r.pf + '%">♀ ' + r.pf + (FR ? " %" : "%") + "</span><span class=\"m\" style=\"width:" + (100 - r.pf) + '%">♂ ' + (100 - r.pf) + (FR ? " %" : "%") + "</span></div><p>" + esc(L.bearsTxt.replace("{f}", r.pf).replace("{m}", 100 - r.pf)) + "</p></section>" : "") +
        (r.c ? "<section>" + h3(L.where) + '<ul class="places">' + r.c.map(function (c) { return "<li>" + esc(FR ? (FRC[c] || c) : c) + "</li>"; }).join("") + "</ul></section>" : "") +
        (r.tr ? "<section>" + h3(L.world) + '<ul class="world">' + Object.keys(r.tr).map(function (l) { return '<li><span class="lg">' + esc(FR ? (FRL[l] || l) : l) + '</span><span class="dl"></span><span class="fm">' + esc(r.tr[l].join(", ")) + "</span></li>"; }).join("") + "</ul></section>" : "") +
        (r.q ? "<section>" + h3(L.lit) + '<blockquote lang="fr">« ' + esc(r.q[0]) + " »<footer>" + esc(r.q[1]) + "</footer></blockquote></section>" : "") +
        '<p class="cr">' + C.src + (r.mp3 ? " " + esc(C.rec.replace("{by}", r.by || "").replace("{acc}", r.acc ? " (" + r.acc + ")" : "")) : "") + "</p>" +
        '<div class="acts"><button type="button" data-close>' + C.close + "</button></div>";
      box.innerHTML = html; box.scrollTop = 0;
      card.hidden = false; history.replaceState(null, "", "#" + id);
      box.querySelectorAll("[data-go]").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); audio.pause(); open(a.dataset.go, a.getAttribute("href").slice(1)); }); });
      var h = box.querySelector(".hear");
      if (h) h.addEventListener("click", function () {
        if (!audio.paused) { audio.pause(); return; }
        audio.src = r.mp3; audio.currentTime = 0; var p = audio.play(); h.setAttribute("aria-pressed", "true"); h.textContent = "■ " + C.playing;
        var idle = function () { h.setAttribute("aria-pressed", "false"); h.textContent = "▶ " + C.hear; };
        audio.onended = audio.onpause = idle; if (p && p.catch) p.catch(idle);
      });
      (h || box.querySelector("[data-close]")).focus();
    });
  }
  function close() { audio.pause(); card.hidden = true; history.replaceState(null, "", location.pathname); if (last) last.focus(); }
  list.addEventListener("click", function (e) { var a = e.target.closest("a[data-n]"); if (!a) return; e.preventDefault(); last = a; open(a.dataset.n, a.getAttribute("href").slice(1)); });
  card.addEventListener("click", function (e) { if (e.target === card || e.target.closest("[data-close]")) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !card.hidden) close(); });
  if (location.hash.length > 1) { var a = list.querySelector('a[href="' + location.hash + '"]'); if (a) { last = a; open(a.dataset.n, location.hash.slice(1)); } }
  apply();
})();
