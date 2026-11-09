/* Sapiopedia Dream Dictionary: search (words + aliases, accents ignored) and "Share this dream" images */
(function () {
  "use strict";
  var C = window.DD || {};
  var fold = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, " ").trim(); };

  /* ---------- search, built from the index already on the page ---------- */
  var items = [];
  document.querySelectorAll(".ixl li").forEach(function (li) {
    var al = li.querySelector(".al");
    if (al) { var first = al.querySelector("a"); if (!first) return;
      items.push({ k: fold(al.firstChild.textContent), label: al.firstChild.textContent.replace(/\s*→\s*$/, ""), href: first.getAttribute("href"), one: first.dataset.one || "", see: Array.prototype.map.call(al.querySelectorAll("a"), function (a) { return a.textContent; }).join(", ") }); }
    else { var a = li.querySelector("a"); items.push({ k: fold(a.textContent), label: a.textContent, href: a.getAttribute("href"), one: a.dataset.one || "" }); }
  });
  var q = document.getElementById("dd-q"), res = document.getElementById("dd-res"), none = document.getElementById("dd-none"), sel = -1;
  function show(list) {
    sel = -1;
    res.innerHTML = list.map(function (it) {
      return '<li><a href="' + it.href + '">' + esc(it.label) + (it.see ? ' <i>→ ' + esc(it.see) + '</i>' : "") + '<small>' + esc(it.one) + "</small></a></li>";
    }).join("");
    res.hidden = !list.length;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function search() {
    var v = fold(q.value);
    if (!v) { res.hidden = true; none.hidden = true; return; }
    var starts = [], inside = [];
    items.forEach(function (it) { if (it.k.indexOf(v) === 0) starts.push(it); else if (it.k.indexOf(" " + v) > 0 || (v.length > 3 && it.k.indexOf(v) > 0)) inside.push(it); });
    var list = starts.sort(function (a, b) { return (!!a.see - !!b.see) || a.k.length - b.k.length; }).concat(inside).slice(0, 12);
    show(list);
    none.hidden = !!list.length; if (!list.length) none.textContent = none.dataset.t.replace("{q}", q.value);
  }
  function go(href) { res.hidden = true; location.href = href; }
  if (q) {
    q.addEventListener("input", search);
    q.addEventListener("keydown", function (e) {
      var links = res.querySelectorAll("a"); if (!links.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel); }); links[sel].scrollIntoView({ block: "nearest" }); }
      else if (e.key === "Enter") { e.preventDefault(); go(links[Math.max(0, sel)].getAttribute("href")); }
      else if (e.key === "Escape") { res.hidden = true; }
    });
    res.addEventListener("click", function (e) { var a = e.target.closest("a"); if (a) { e.preventDefault(); go(a.getAttribute("href")); } });
    document.addEventListener("click", function (e) { if (!e.target.closest(".dd-search")) res.hidden = true; });
  }

  /* ---------- share image ---------- */
  var INK = "#2B2320", SEPIA = "#5B4A40", RULE = "#BFAE9F", WINE = "#8E2F48", PAPER = "#FCF7F2", BODY = "#3A302B";
  var THUMB = new Path2D("M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z");
  var TH = { up: ["#6E8F63", "#3E5638", 0], mid: ["#D4AE52", "#8A6A22", -Math.PI / 2], down: ["#B0564A", "#6E2C25", Math.PI] };
  var F = { fell: "'IM Fell English', Georgia, serif", sc: "'IM Fell English SC', Georgia, serif", gar: "'EB Garamond', Georgia, serif", sans: "'Source Sans 3', Arial, sans-serif" };
  var logo = new Image(); logo.src = "/assets/logo-horizontal.png";

  function read(art) {
    var g = function (s) { var el = art.querySelector(s); return el ? el.textContent.trim() : ""; };
    var guide = art.querySelectorAll(".guide > *");
    var split = function (li) { var i = li.querySelector("i"); var lead = i ? i.textContent : ""; var rest = li.textContent.replace(lead, "").trim(); return [lead.replace(/\s*:\s*$/, ""), rest]; };
    var secs = art.querySelectorAll("section");
    var listOf = function (n) { return secs[n] ? Array.prototype.map.call(secs[n].querySelectorAll("li"), function (li) { return li; }) : []; };
    var sitSec = art.querySelector("ul.sit"), flSecs = art.querySelectorAll("ul.fl");
    return {
      id: art.id, letter: g(".ini"), prev: guide[0] ? guide[0].textContent.replace("←", "").trim() : "", next: guide[2] ? guide[2].textContent.replace("→", "").trim() : "",
      title: g("h1, h2"), names: (art.querySelector(".pos").firstChild.textContent || "").replace(/\s*·\s*$/, ""), toneLabel: (art.querySelector(".pos").lastChild.textContent || "").trim(), tone: (art.querySelector(".dots") ? art.querySelector(".dots").textContent.replace(art.querySelector(".dots s").textContent, "").length : 0),
      lead: g("p.lead"),
      sits: sitSec ? Array.prototype.map.call(sitSec.querySelectorAll("li"), function (li) { return [li.className].concat(split(li)); }) : [],
      feels: flSecs[0] && flSecs[0].closest("section").querySelector("h3").textContent === C.feel ? Array.prototype.map.call(flSecs[0].querySelectorAll("li"), split) : [],
      qs: Array.prototype.slice.call(flSecs).filter(function (u) { return u.closest("section").querySelector("h3").textContent === C.q; }).flatMap(function (u) { return Array.prototype.map.call(u.querySelectorAll("li"), function (li) { return li.textContent; }); }),
      see: Array.prototype.map.call(art.querySelectorAll(".see a, .see"), function (x) { return x; }).length ? (art.querySelector(".see") ? art.querySelector(".see").textContent.replace(C.also, "").trim().split(" · ").slice(0, 5) : []) : [],
      refs: g(".refs").split(new RegExp("\\.\\s+" + (C.searched || "~~") + "\\s*:"))[0].replace(/\.$/, "")
    };
  }
  function thumb(g, kind, x, y, s) { var t = TH[kind] || TH.mid; g.save(); g.translate(x + s / 2, y + s / 2); g.rotate(t[2]); g.scale(s / 24, s / 24); g.translate(-12, -12); g.fillStyle = t[0]; g.fill(THUMB); g.lineWidth = 1.1; g.strokeStyle = t[1]; g.stroke(THUMB); g.restore(); }
  function rich(g, segs, x, y, maxW, lh, draw) {
    var words = []; segs.forEach(function (s) { s[0].split(/(\s+)/).forEach(function (w) { if (w) words.push([w, s[1], s[2]]); }); });
    var line = [], w = 0, lines = [];
    words.forEach(function (wd) { g.font = wd[1]; var ww = g.measureText(wd[0]).width; var sp = /^\s+$/.test(wd[0]);
      if (w + ww > maxW && line.length && !sp) { lines.push(line); line = []; w = 0; } if (!line.length && sp) return; line.push([wd[0], wd[1], wd[2], ww]); w += ww; });
    if (line.length) lines.push(line);
    if (draw) lines.forEach(function (ln, i) { var cx = x; ln.forEach(function (wd) { g.font = wd[1]; g.fillStyle = wd[2] || BODY; g.fillText(wd[0], cx, y + i * lh); cx += wd[3]; }); });
    return y + lines.length * lh;
  }
  function centered(g, text, font, color, cx, y, maxW, lh, draw) {
    g.font = font; var words = text.split(" "), line = "", out = [];
    words.forEach(function (w) { var t = line ? line + " " + w : w; if (g.measureText(t).width > maxW && line) { out.push(line); line = w; } else line = t; }); out.push(line);
    if (draw) { g.fillStyle = color; g.textAlign = "center"; out.forEach(function (l, i) { g.fillText(l, cx, y + i * lh); }); g.textAlign = "left"; }
    return y + out.length * lh;
  }
  function rule2(g, x0, x1, y) { g.fillStyle = RULE; g.fillRect(x0, y, x1 - x0, 1.5); g.fillRect(x0, y + 4, x1 - x0, 1.5); }
  function heading(g, text, cx, y, x0, x1) { g.font = "34px " + F.sc; var tw = g.measureText(text).width; g.fillStyle = INK; g.textAlign = "center"; g.fillText(text, cx, y); g.textAlign = "left"; rule2(g, x0, cx - tw / 2 - 24, y - 12); rule2(g, cx + tw / 2 + 24, x1, y - 12); }
  function fitText(g, text, font, maxW) { g.font = font; if (g.measureText(text).width <= maxW) return text; while (text.length > 4 && g.measureText(text + "…").width > maxW) text = text.slice(0, -1); return text + "…"; }

  function render(E, draw, H) {
    var W = 1080, M = 70, X0 = M + 40, X1 = W - M - 40, CW = X1 - X0, BAND = 190;
    var c = document.createElement("canvas"); c.width = W; c.height = H || 4000; var g = c.getContext("2d");
    if (draw) { g.fillStyle = "#F3E9E0"; g.fillRect(0, 0, W, c.height); g.fillStyle = PAPER; g.fillRect(M, M, W - 2 * M, c.height - 2 * M - BAND + 40);
      g.strokeStyle = "#D9C9BA"; g.lineWidth = 2; g.strokeRect(M + 10, M + 10, W - 2 * M - 20, c.height - 2 * M - BAND + 20); g.lineWidth = 1; g.strokeRect(M + 16, M + 16, W - 2 * M - 32, c.height - 2 * M - BAND + 8); }
    var y = M + 70;
    if (draw) { g.font = "24px " + F.sc; g.fillStyle = SEPIA; if (E.prev) g.fillText("← " + fitText(g, E.prev, "24px " + F.sc, 240), X0, y); g.textAlign = "center"; g.fillText(C.book + " · " + E.letter, W / 2, y);
      g.textAlign = "right"; if (E.next) g.fillText(fitText(g, E.next, "24px " + F.sc, 240) + " →", X1, y); g.textAlign = "left"; rule2(g, X0, X1, y + 16); }
    y += 120;
    var tFont = 72; g.font = tFont + "px " + F.fell; while (g.measureText(E.title).width > CW - 140 && tFont > 40) { tFont -= 4; g.font = tFont + "px " + F.fell; }
    if (draw) { g.font = "190px " + F.fell; g.fillStyle = WINE; g.fillText(E.letter, X0 - 4, y + 52); g.font = tFont + "px " + F.fell; g.fillStyle = INK; g.fillText(E.title, X0 + 128, y);
      g.font = "italic 25px " + F.gar; g.fillStyle = SEPIA; var nm = fitText(g, E.names + "  \u00b7  ", "italic 25px " + F.gar, 360); g.fillText(nm, X0 + 132, y + 46);
      var dx = X0 + 132 + g.measureText(nm).width; for (var k = 0; k < 5; k++) { g.beginPath(); g.arc(dx + 8 + k * 20, y + 37, 6.5, 0, Math.PI * 2); g.fillStyle = k < E.tone ? WINE : "#E2D5CB"; g.fill(); }
      g.fillStyle = SEPIA; g.fillText(fitText(g, E.toneLabel, "italic 25px " + F.gar, X1 - (dx + 112)), dx + 112, y + 46); }
    y += 140;
    y = centered(g, E.lead, "italic 38px " + F.gar, INK, W / 2, y, CW - 60, 50, draw) + 50;
    if (E.sits.length) { if (draw) heading(g, C.sit, W / 2, y, X0, X1); y += 58;
      E.sits.forEach(function (s) { if (draw) thumb(g, s[0], X0, y - 27, 32); y = rich(g, [[s[1] ? s[1] + ": " : "", "italic 30px " + F.gar, INK], [s[2], "30px " + F.gar]], X0 + 50, y, CW - 50, 40, draw) + 12; }); y += 30; }
    if (E.feels.length) { if (draw) heading(g, C.feel, W / 2, y, X0, X1); y += 58;
      E.feels.forEach(function (f) { if (draw) { g.font = "28px " + F.gar; g.fillStyle = RULE; g.fillText("❧", X0, y); } y = rich(g, [[f[0] ? f[0] + ": " : "", "italic 30px " + F.gar, INK], [f[1], "30px " + F.gar]], X0 + 46, y, CW - 46, 40, draw) + 10; }); y += 30; }
    if (E.qs.length) { if (draw) heading(g, C.q, W / 2, y, X0, X1); y += 58;
      E.qs.forEach(function (q) { if (draw) { g.font = "28px " + F.gar; g.fillStyle = RULE; g.fillText("❧", X0, y); } y = rich(g, [[q, "30px " + F.gar]], X0 + 46, y, CW - 46, 40, draw) + 10; }); y += 40; }
    if (E.see.length) { if (draw) { g.textAlign = "center"; g.fillStyle = SEPIA; g.fillText("", 0, 0); g.font = "30px " + F.sc; g.fillText(fitText(g, "❦  " + C.also + "  " + E.see.join("  ·  "), "30px " + F.sc, CW), W / 2, y); g.textAlign = "left"; } y += 44; }
    if (draw) { rule2(g, X0, X1, y); g.font = "italic 22px " + F.gar; g.fillStyle = SEPIA; g.textAlign = "center"; g.fillText(fitText(g, E.refs, "italic 22px " + F.gar, CW), W / 2, y + 40); g.textAlign = "left"; }
    y += 80;
    var total = y + 30 + M - 40 + BAND; if (!draw) return total;
    var by = c.height - BAND; g.fillStyle = "#F7E9EC"; g.fillRect(0, by, W, BAND); g.fillStyle = "#DCC9CE"; g.fillRect(0, by, W, 2);
    if (logo.complete && logo.naturalWidth) { var lh = 100; g.drawImage(logo, M - 10, by + (BAND - lh) / 2, logo.naturalWidth * lh / logo.naturalHeight, lh); }
    g.textAlign = "right"; g.fillStyle = "#2A1F26"; g.font = "600 30px " + F.sans; g.fillText(C.url + E.id + "/", W - M, by + 84);
    g.fillStyle = "#6E5A62"; g.font = "400 22px " + F.sans; g.fillText(C.book + " · " + E.title, W - M, by + 120); g.textAlign = "left";
    return c;
  }
  async function makePNG(art) {
    if (document.fonts) await Promise.all(["72px 'IM Fell English'", "24px 'IM Fell English SC'", "30px 'EB Garamond'", "italic 30px 'EB Garamond'", "600 30px 'Source Sans 3'"].map(function (f) { return document.fonts.load(f).catch(function () {}); }));
    if (!logo.complete) await new Promise(function (r) { logo.onload = logo.onerror = r; });
    var E = read(art); return render(E, true, render(E, false));
  }
  var ov = document.getElementById("dd-ov"), current = null, lastBtn = null;
  document.addEventListener("click", async function (e) {
    var b = e.target.closest(".dd-e .share"); if (!b) return;
    var art = b.closest(".dd-e"), label = b.textContent; b.disabled = true; b.textContent = C.preparing; lastBtn = b;
    try { var c = await makePNG(art); current = { blob: await new Promise(function (r) { c.toBlob(r, "image/png"); }), name: "sapiopedia-dream-" + art.id + ".png" };
      ov.querySelector("img").src = URL.createObjectURL(current.blob); ov.querySelector("img").alt = art.querySelector("h1, h2").textContent; ov.hidden = false; ov.querySelector('[data-a="dl"]').focus(); }
    finally { b.disabled = false; b.textContent = label; }
  });
  ov.addEventListener("click", function (e) {
    var a = e.target.closest("[data-a]");
    if (e.target === ov || (a && a.dataset.a === "close")) { ov.hidden = true; if (lastBtn) lastBtn.focus(); return; }
    if (a && a.dataset.a === "dl" && current) { var l = document.createElement("a"); l.href = URL.createObjectURL(current.blob); l.download = current.name; document.body.appendChild(l); l.click(); l.remove(); }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !ov.hidden) { ov.hidden = true; if (lastBtn) lastBtn.focus(); } });
})();
