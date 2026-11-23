/* Sapiopedia: middle-name and sibling finder. Same rules as tools/name_matching.py, run in the browser on /assets/names-match.json.
   Row: [book, name, slug, gender, syllables, start sound, end sound, style bits, origin index, popularity 0-100, pool, variants, peak decade]
   The shortlist lives in the link after # (no server). */
(function () {
  "use strict";
  var C = window.NM || {}, $ = function (id) { return document.getElementById(id); };
  var D, R, byName = {}, PAIRS = {}, fold = function (s) { return String(s).toLowerCase().replace(/œ/g, "oe").replace(/æ/g, "ae").normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  var BAD = { en: ["ASS", "PIG", "FAT", "BUM", "DIE", "SAD", "MAD", "BAD", "RAT", "HAG", "COW", "POO", "WTF", "SOS", "FML", "STD", "KKK", "GAY", "SEX", "DUD", "BRA", "PMS", "LSD", "UGH", "BOO"],
             fr: ["CON", "PUE", "PET", "NUL", "CUL", "MOU", "ZOB", "PD", "NAZ", "BOF", "PUR", "SOT", "FOU", "MAL", "RAT", "ZIZ", "VOL", "PIS"] };
  var W = [0.5, 1, 1, 1.5, 1.5, 1.5, 1.5, 1, 1.5];
  var state = { n: "", b: "", mode: "middle", sur: "", style: "", len: "", origin: "", intl: false, book: "same", list: [] };

  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 3;
    var p = [], i, j; for (j = 0; j <= b.length; j++) p[j] = j;
    for (i = 1; i <= a.length; i++) { var c = [i]; for (j = 1; j <= b.length; j++) c[j] = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] !== b[j - 1] ? 1 : 0)); p = c; }
    return p[b.length];
  }
  function near(x, y) {
    var a = fold(x[1]), b = fold(y[1]);
    return lev(a, b) <= 2 || x[11].indexOf(b) >= 0 || y[11].indexOf(a) >= 0 || (a.length >= 4 && b.indexOf(a.slice(0, 4)) === 0) || b.indexOf(a) === 0 || a.indexOf(b) === 0;
  }
  function shared(x, y) { var s = 0, t; for (t = 0; t < W.length; t++) if ((x[7] >> t) & (y[7] >> t) & 1) s += W[t]; return Math.min(s, 3); }
  function firstStyle(x, y, skipRare) { for (var t = 0; t < D.styles.length; t++) if ((x[7] >> t) & (y[7] >> t) & 1 && !(skipRare && D.styles[t] === "rare")) return D.styles[t]; return ""; }
  function isPair(i, j) { return (PAIRS[i] || []).indexOf(j) >= 0; }
  function sylCount(s) { var w = fold(s).replace(/(?<=[^aeiouy])e\b/g, ""); return Math.max(1, (w.match(/[aeiouy]+/g) || []).length); }

  function score(i, j, mode, gender) {
    var x = R[i], y = R[j], s = 0, why = [];
    if (mode === "middle") {
      if (y[3] !== x[3] && x[3] !== "n" && !isPair(i, j)) return null;
      if (isPair(i, j)) { s += 4; why.push("pair"); }
      if (y[4] !== x[4]) { s += 2; why.push("flow"); }
      if (y[4] + x[4] >= 6) s -= 2;
      if (y[6] === x[6]) s -= 3;
      if (y[5] && y[5] === x[6].slice(-1)) s -= 2;
      if (x[8] >= 0 && y[8] === x[8]) s += 0.5;
      s += y[9] / 100;
    } else {
      if (y[3] !== gender) return null;
      s += shared(x, y) * 1.5;
      if (x[8] >= 0 && y[8] === x[8]) { s += 1.5; why.push("origin"); }
      if (fold(y[1])[0] === fold(x[1])[0]) s -= 2;
      if (y[6] === x[6]) s -= 2;
      s -= 3 * Math.abs(y[9] - x[9]) / 100; s += y[9] / 100;
      if (x[12] && y[12]) s -= Math.abs(y[12] - x[12]) / 10 * 1.2; else if (x[12]) s -= 3;
    }
    if (mode === "middle") s += shared(x, y);
    var st = firstStyle(x, y, mode === "middle"); if (st) why.splice(mode === "middle" ? why.length : 0, 0, "style:" + st);
    if (near(x, y)) return null;
    if (mode !== "middle") why.push("distinct");
    return [s, why];
  }

  function initialsOk(first, middle, sur) {
    if (!sur) return true;
    var ini = (first[0] + middle[0] + sur[0]).toUpperCase(), bad = BAD[C.lang] || [];
    return bad.indexOf(ini) < 0 && bad.indexOf(ini.slice(0, 2)) < 0 && BAD.en.indexOf(ini) < 0;
  }

  function filters(y) {
    if (state.style && !((y[7] >> D.styles.indexOf(state.style)) & 1)) return false;
    if (state.len === "1" && y[4] !== 1) return false;
    if (state.len === "2" && y[4] !== 2) return false;
    if (state.len === "3" && y[4] < 3) return false;
    if (state.origin !== "" && y[8] !== +state.origin) return false;
    if (state.intl && !((y[7] >> D.styles.indexOf("international")) & 1)) return false;
    return true;
  }

  function run() {
    var out = $("nm-out"); out.innerHTML = "";
    var key = fold(state.n), i = byName[(state.b || "fr") + ":" + key]; if (i === undefined) i = byName["fr:" + key]; if (i === undefined) i = byName["de:" + key];
    if (i === undefined) { if (state.n) out.innerHTML = '<p class="nm-none">' + C.none.replace("{q}", esc(state.n)) + "</p>"; return; }
    var x = R[i], sur = state.sur.trim(), groups = state.mode === "middle" ? [["", null]] : [[C.sisters, "f"], [C.brothers, "m"]];
    groups.forEach(function (g) {
      var res = [];
      for (var j = 0; j < R.length; j++) {
        var y = R[j]; if (j === i || !y[10] || (state.book === "same" && y[0] !== x[0])) continue;
        if (!filters(y)) continue;
        var sc = score(i, j, state.mode, g[1]); if (!sc) continue;
        var why = sc[1].slice();
        if (sur && state.mode === "middle") {
          if (!initialsOk(x[1], y[1], sur)) continue;
          why.push("init");
          if (x[4] + y[4] + sylCount(sur) > 8) sc[0] -= 1.5;
        }
        res.push([sc[0], j, why]);
      }
      res.sort(function (a, b) { return b[0] - a[0]; });
      var h = g[0] ? "<h3>" + g[0] + "</h3>" : "";
      out.insertAdjacentHTML("beforeend", h + '<ul class="nm-res">' + res.slice(0, 24).map(function (r) {
        var y = R[r[1]], on = state.list.indexOf(y[1]) >= 0, full = state.mode === "middle" ? x[1] + " " + y[1] + (sur ? " " + sur : "") : y[1];
        return '<li><button type="button" class="nm-heart" aria-pressed="' + on + '" data-n="' + esc(y[1]) + '" aria-label="' + C.save + '">' + (on ? "♥" : "♡") + "</button>" +
          '<a href="' + C.base[y[0]] + y[2] + '/">' + esc(full) + "</a><span>" + r[2].map(label).join(" · ") + "</span></li>";
      }).join("") + "</ul>");
    });
    if (!out.textContent.trim()) out.innerHTML = '<p class="nm-none">' + C.empty + "</p>";
  }
  function label(c) { return c.indexOf("style:") === 0 ? C.style.replace("{s}", C.styles[c.slice(6)] || c.slice(6)) : C.why[c] || c; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function save() {
    var h = "n=" + encodeURIComponent(state.n) + "&b=" + state.b + "&m=" + state.mode + (state.sur ? "&s=" + encodeURIComponent(state.sur) : "") + (state.list.length ? "&l=" + encodeURIComponent(state.list.join(",")) : "");
    history.replaceState(null, "", "#" + h); shortlist();
  }
  function load() {
    var q = {}; location.hash.slice(1).split("&").forEach(function (kv) { var p = kv.split("="); if (p[0]) q[p[0]] = decodeURIComponent(p[1] || ""); });
    if (q.n) { state.n = q.n; $("nm-n").value = q.n; } if (q.b) state.b = q.b; if (q.m) state.mode = q.m; if (q.s) { state.sur = q.s; $("nm-s").value = q.s; }
    if (q.l) state.list = q.l.split(",").filter(Boolean);
    document.querySelectorAll("[name=nm-mode]").forEach(function (r) { r.checked = r.value === state.mode; });
  }
  function shortlist() {
    var box = $("nm-list");
    box.innerHTML = state.list.length ? "<b>" + C.list + "</b> " + state.list.map(function (n) { return '<span>' + esc(n) + '</span>'; }).join(" · ") +
      ' <button type="button" id="nm-share" class="btn ghostbtn">' + C.share + "</button>" : "";
    var b = $("nm-share"); if (b) b.onclick = function () { var u = location.href; if (navigator.share) navigator.share({ title: C.shareTitle, url: u }).catch(function () {}); else if (navigator.clipboard) navigator.clipboard.writeText(u).then(function () { b.textContent = C.copied; }); };
  }

  fetch("/assets/names-match.json").then(function (r) { return r.json(); }).then(function (d) {
    D = d; R = d.n; PAIRS = {};
    Object.keys(d.pairs).forEach(function (k) { PAIRS[+k] = d.pairs[k]; });
    R.forEach(function (r, i) { byName[r[0] + ":" + fold(r[1])] = i; r[11].forEach(function (v) { if (byName[r[0] + ":" + v] === undefined) byName[r[0] + ":" + v] = i; }); });
    var dl = $("nm-names"); dl.innerHTML = R.filter(function (r) { return r[10]; }).map(function (r) { return '<option value="' + esc(r[1]) + '">'; }).join("");
    var og = $("nm-origin"); og.insertAdjacentHTML("beforeend", d.origins.map(function (o, k) { return '<option value="' + k + '">' + esc((C.origins || {})[o] || o) + "</option>"; }).join(""));
    load(); run(); shortlist();
  });
  function onChange() {
    state.n = $("nm-n").value.trim(); state.sur = $("nm-s").value; state.style = $("nm-style").value; state.len = $("nm-len").value; state.origin = $("nm-origin").value;
    state.intl = $("nm-intl").checked; state.book = $("nm-book").value;
    var m = document.querySelector("[name=nm-mode]:checked"); state.mode = m ? m.value : "middle";
    if (R) { run(); save(); }
  }
  ["nm-n", "nm-s"].forEach(function (id) { $(id).addEventListener("input", onChange); });
  ["nm-style", "nm-len", "nm-origin", "nm-intl", "nm-book"].forEach(function (id) { $(id).addEventListener("change", onChange); });
  document.querySelectorAll("[name=nm-mode]").forEach(function (r) { r.addEventListener("change", onChange); });
  $("nm-out").addEventListener("click", function (e) {
    var b = e.target.closest(".nm-heart"); if (!b) return; var n = b.dataset.n, k = state.list.indexOf(n);
    if (k >= 0) state.list.splice(k, 1); else state.list.push(n);
    b.setAttribute("aria-pressed", k < 0); b.textContent = k < 0 ? "♥" : "♡"; save();
  });
})();
