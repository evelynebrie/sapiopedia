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
  q.addEventListener("keydown", function (e) { if (e.key === "Enter") { var first = items.find(function (it) { return !it.li.classList.contains("x") && (filter === "all" || it.g === filter); }); if (first) location.href = first.li.querySelector("a").getAttribute("href"); } });

  /* each name opens its own page; Enter in the search opens the first match */
  apply();
})();
