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
  function open(name, id) {
    load().then(function (D) {
      var r = D[name] || { g: "u" }, rows = "";
      if (r.ipa) rows += "<tr><th>" + C.pron + "</th><td>" + esc(r.ipa) + "</td></tr>";
      if (r.att) rows += "<tr><th>" + C.first + "</th><td>" + esc(r.att.replace(/^c\.\s*/, "c. ")) + "</td></tr>";
      if (r.tr) rows += "<tr><th>" + C.other + "</th><td>" + Object.keys(r.tr).map(function (l) { return "<i>" + esc(l) + "</i> " + esc(r.tr[l].join(", ")); }).join(" · ") + "</td></tr>";
      if (r.der) rows += "<tr><th>" + C.comp + "</th><td>" + esc(r.der.join(", ")) + "</td></tr>";
      box.innerHTML = '<div class="hd"><span class="ini" aria-hidden="true">' + esc(name.charAt(0)) + '</span><div><h2 id="nf-name">' + esc(name) + "</h2>" +
        '<p class="gl">' + (SYM[r.g] ? '<b class="' + r.g + '">' + SYM[r.g] + "</b>" : "") + "<span>" + esc(C.g[r.g]) + "</span>" +
        (r.mp3 ? '<button type="button" class="hear" aria-pressed="false">▶ ' + C.hear + "</button>" : "") + "</p></div></div>" +
        (rows ? "<table>" + rows + "</table>" : "") +
        '<p class="cr">' + C.src + (r.mp3 ? " " + esc(C.rec.replace("{by}", r.by || "").replace("{acc}", r.acc ? " (" + r.acc + ")" : "")) : "") + "</p>" +
        '<div class="acts"><button type="button" data-close>' + C.close + "</button></div>";
      card.hidden = false; history.replaceState(null, "", "#" + id);
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
