/* Sapiopedia Room Planner: 3D (isometric cut-away) view. Reads the plan through window.FSAPI. */
(function () {
"use strict";
const A = window.FSAPI; if (!A) return;
const T = A.T, PX = A.PXM, cm = c => c * PX / 100;
const WALL_H = cm(250), WT = cm(12), SLAB = cm(14), LR = 2.5 * PX;
const C30 = Math.cos(Math.PI / 6);
const FLOORS = {
  oak:      { n: "Oak",        base: "#C9AD8A", line: "#B0926E", type: "plank" },
  light:    { n: "Light wood", base: "#DDCBB0", line: "#C7B293", type: "plank" },
  grey:     { n: "Grey wood",  base: "#BDB3A8", line: "#A79C90", type: "plank" },
  walnut:   { n: "Walnut",     base: "#7B5A41", line: "#644732", type: "plank" },
  tile:     { n: "Tile",       base: "#ECE9E3", line: "#D2CCC2", type: "tile" },
  concrete: { n: "Concrete",   base: "#BEBBB6", line: "#B2AEA8", type: "flat" },
  carpet:   { n: "Carpet",     base: "#D6CBBB", line: "#CBBFAE", type: "flat" }
};
const WALLS = ["#F4F2EE", "#EAE2D8", "#D5DCCB", "#C9D6E0", "#EBD3D6", "#3A4656", "#C98A6B"];
const WOOD = "#D8C2A0", FABRIC = "#C3BBB0", WHITE = "#F3F1ED", DARK = "#3B3B3E", METAL = "#5D5D60";

function look() { const S = A.S; if (!S.look) S.look = { floor: "oak", wall: WALLS[0], rot: 0 }; return S.look; }
function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  const c = v => Math.max(0, Math.min(255, Math.round(v * f)));
  return `rgb(${c(r)},${c(g)},${c(b)})`;
}
function rnd(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

/* ---------- geometry helpers ---------- */
function setup(W) {
  const P = A.pts(), [cx, cy] = A.centroid(P), rot = (look().rot || 0) * Math.PI / 2, c = Math.cos(rot), s = Math.sin(rot);
  const R = (x, y) => { const dx = x - cx, dy = y - cy; return [dx * c - dy * s, dx * s + dy * c]; };
  const RN = (nx, ny) => [nx * c - ny * s, nx * s + ny * c];
  const raw = (x, y, z) => { const [a, b] = R(x, y); return [(a - b) * C30, (a + b) * 0.5 - z]; };
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  P.forEach(([x, y]) => [[0], [WALL_H], [-SLAB]].forEach(([z]) => { const [u, v] = raw(x, y, z); x0 = Math.min(x0, u); x1 = Math.max(x1, u); y0 = Math.min(y0, v); y1 = Math.max(y1, v); }));
  const pad = 24, k = (W - pad * 2) / (x1 - x0), H = Math.round((y1 - y0) * k + pad * 2);
  const prj = (x, y, z) => { const [u, v] = raw(x, y, z); return [pad + (u - x0) * k, pad + (v - y0) * k]; };
  const depth = (x, y) => { const [a, b] = R(x, y); return a + b; };
  return { P, prj, depth, RN, k, H, vis: (nx, ny) => { const [a, b] = RN(nx, ny); return a + b > 0.02; } };
}
function poly(g, pts, fill, stroke) {
  g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.closePath();
  if (fill) { g.fillStyle = fill; g.fill(); }
  if (stroke) { g.strokeStyle = stroke; g.lineWidth = 1; g.stroke(); }
}

/* ---------- furniture as boxes: [u0,u1,v0,v1,z0,z1,colour] in local cm-ish px, v<0 = back ---------- */
function parts(it, f) {
  const w = f.w, h = f.h, W2 = w / 2, H2 = h / 2, B = [];
  const box = (u0, u1, v0, v1, z0, z1, col) => B.push([u0, u1, v0, v1, cm(z0), cm(z1), col]);
  const legs = (zt, col, sz) => { const s = sz || cm(4); [[-W2, -H2], [W2 - s, -H2], [-W2, H2 - s], [W2 - s, H2 - s]].forEach(([u, v]) => box(u, u + s, v, v + s, 0, zt, col)); };
  switch (it.k) {
    case "bed": box(-W2, W2, -H2, -H2 + cm(6), 0, 105, WOOD); box(-W2, W2, -H2 + cm(6), H2, 0, 30, WOOD);
      box(-W2 + 2, W2 - 2, -H2 + cm(6), H2 - 2, 30, 52, WHITE); [-1, 1].forEach(sg => box(sg < 0 ? -W2 + cm(10) : cm(6), sg < 0 ? -cm(6) : W2 - cm(10), -H2 + cm(10), -H2 + cm(45), 52, 62, "#FBFAF7"));
      box(-W2 + 1, W2 - 1, -H2 + cm(70), H2 - 1, 52, 56, "#B9C4CC"); break;
    case "desk": legs(72, METAL, cm(4)); box(-W2, W2, -H2, H2, 72, 76, WOOD); box(W2 - cm(40), W2 - cm(2), -H2 + cm(2), H2 - cm(4), 20, 72, shade(WOOD, .95)); break;
    case "table": legs(72, METAL, cm(5)); box(-W2, W2, -H2, H2, 72, 76, WOOD); break;
    case "chair": legs(45, WOOD, cm(3.5)); box(-W2, W2, -H2, H2, 45, 49, FABRIC); box(-W2, W2, -H2, -H2 + cm(3.5), 49, 92, WOOD); break;
    case "sofa": case "armchair": { const arm = Math.min(cm(18), w * .18);
      box(-W2, W2, -H2, H2, 8, 40, FABRIC); box(-W2, W2, -H2, -H2 + cm(20), 40, 82, shade(FABRIC, .97));
      box(-W2, -W2 + arm, -H2, H2, 40, 62, shade(FABRIC, .98)); box(W2 - arm, W2, -H2, H2, 40, 62, shade(FABRIC, .98));
      box(-W2 + arm, W2 - arm, -H2 + cm(20), H2 - cm(2), 40, 47, shade(FABRIC, 1.05)); legs(8, DARK, cm(4)); break; }
    case "tv": box(-W2 * .4, W2 * .4, -H2, H2, 0, 50, DARK); box(-W2, W2, -H2, H2, 50, 112, "#1F2022"); break;
    case "wardrobe": box(-W2, W2, -H2, H2, 0, 205, WHITE); break;
    case "countertop": box(-W2, W2, -H2, H2 - cm(3), 0, 86, WHITE); box(-W2, W2, -H2, H2, 86, 90, "#8D8984"); break;
    case "appliance": box(-W2, W2, -H2, H2, 0, 85, "#E4E6E8"); break;
    case "shelf": box(-W2, W2, -H2, H2, 0, 185, WOOD); break;
    case "screen": box(-W2, W2, -H2, H2, 0, 170, "#E2D3BC"); break;
    case "plant": box(-W2 * .45, W2 * .45, -H2 * .45, H2 * .45, 0, 32, "#B9714B"); B.push({ ball: true, r: W2 * 1.05, z: cm(70), col: "#6F8F5E" }); break;
    case "lamp": box(-W2 * .4, W2 * .4, -H2 * .4, H2 * .4, 0, 3, METAL); box(-cm(1.2), cm(1.2), -cm(1.2), cm(1.2), 3, 135, METAL);
      B.push({ shade: true, r: W2 * .9, z0: cm(130), z1: cm(160), col: "#F1E6CC" }); break;
    default: box(-W2, W2, -H2, H2, 0, 60, FABRIC);
  }
  return B;
}

/* ---------- render ---------- */
function draw(cv, W, dpr) {
  const S = A.S, L = look(), G = setup(W), { P, prj, depth, vis } = G;
  cv.width = Math.round(W * dpr); cv.height = Math.round(G.H * dpr); cv.style.height = G.H + "px";
  const g = cv.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, G.H);
  g.lineJoin = "round";
  const n = P.length, E = P.map((a, i) => {
    const b = P[(i + 1) % n], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy);
    let nx = -dy / len, ny = dx / len; const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
    if (!inside(mx + nx * 4, my + ny * 4, P)) { nx = -nx; ny = -ny; }
    return { a, b, nx, ny, i, back: vis(nx, ny) };
  });
  const out = (p, e, d) => [p[0] - e.nx * d, p[1] - e.ny * d];
  const FL = FLOORS[L.floor] || FLOORS.oak;

  /* floor slab sides (front edges) */
  E.filter(e => !e.back).forEach(e => {
    const a = out(e.a, e, WT), b = out(e.b, e, WT);
    poly(g, [prj(...a, 0), prj(...b, 0), prj(...b, -SLAB), prj(...a, -SLAB)], "#E3E0DB", "#D6D2CC");
  });
  /* floor surface including wall footprint */
  const outer = P.map((p, i) => { const e1 = E[(i - 1 + n) % n], e2 = E[i]; return [p[0] - (e1.nx + e2.nx) * WT, p[1] - (e1.ny + e2.ny) * WT]; });
  poly(g, outer.map(p => prj(p[0], p[1], 0)), "#EEECE8");
  g.save(); poly(g, P.map(p => prj(p[0], p[1], 0)), FL.base); g.clip();
  const xs = P.map(p => p[0]), ys = P.map(p => p[1]), X0 = Math.min(...xs), X1 = Math.max(...xs), Y0 = Math.min(...ys), Y1 = Math.max(...ys);
  g.strokeStyle = FL.line; g.lineWidth = 1;
  const seg = (x1, y1, x2, y2) => { const p1 = prj(x1, y1, 0), p2 = prj(x2, y2, 0); g.beginPath(); g.moveTo(...p1); g.lineTo(...p2); g.stroke(); };
  if (FL.type === "plank") {
    const pw = cm(18), r = rnd(7); let row = 0;
    for (let y = Y0; y < Y1; y += pw, row++) {
      seg(X0, y, X1, y);
      const tone = 0.95 + r() * 0.1; poly(g, [prj(X0, y, 0), prj(X1, y, 0), prj(X1, y + pw, 0), prj(X0, y + pw, 0)], null);
      g.fillStyle = shade(FL.base, tone); g.globalAlpha = .35; g.fill(); g.globalAlpha = 1;
      for (let x = X0 + r() * cm(120); x < X1; x += cm(90) + r() * cm(60)) seg(x, y, x, y + pw);
    }
  } else if (FL.type === "tile") {
    for (let y = Y0; y < Y1; y += cm(50)) seg(X0, y, X1, y);
    for (let x = X0; x < X1; x += cm(50)) seg(x, Y0, x, Y1);
  } else {
    const r = rnd(3); g.fillStyle = FL.line;
    for (let i = 0; i < 900; i++) { const p = prj(X0 + r() * (X1 - X0), Y0 + r() * (Y1 - Y0), 0); g.globalAlpha = .25; g.fillRect(p[0], p[1], 1.4, 1.4); }
    g.globalAlpha = 1;
  }
  g.restore();

  /* back walls: inner face, openings, top cap */
  const wallCol = L.wall || WALLS[0];
  const opens = S.opens.map(op => Object.assign({ op }, A.openPos(op))).filter(p => p && isFinite(p.x));
  E.filter(e => e.back).sort((p, q) => depth((p.a[0] + p.b[0]) / 2, (p.a[1] + p.b[1]) / 2) - depth((q.a[0] + q.b[0]) / 2, (q.a[1] + q.b[1]) / 2)).forEach(e => {
    const [ra, rb] = G.RN(e.nx, e.ny), f = ra > rb ? 0.97 : 0.88;
    poly(g, [prj(...e.a, 0), prj(...e.b, 0), prj(...e.b, WALL_H), prj(...e.a, WALL_H)], shade(wallCol, f));
    /* skirting */
    poly(g, [prj(...e.a, 0), prj(...e.b, 0), prj(...e.b, cm(7)), prj(...e.a, cm(7))], shade(wallCol, f * 0.96));
    opens.filter(p => p.edge === e.i).forEach(p => {
      const hl = p.len / 2, A1 = [p.x - p.tx * hl, p.y - p.ty * hl], B1 = [p.x + p.tx * hl, p.y + p.ty * hl];
      const quad = (z0, z1, inset) => { const a = [A1[0] + p.nx * inset, A1[1] + p.ny * inset], b = [B1[0] + p.nx * inset, B1[1] + p.ny * inset]; return [prj(...a, z0), prj(...b, z0), prj(...b, z1), prj(...a, z1)]; };
      if (p.op.k === "window") {
        poly(g, quad(cm(88), cm(212), 0), shade(wallCol, f * 0.9));
        const glass = quad(cm(93), cm(207), 0.5), gr = g.createLinearGradient(glass[3][0], glass[3][1], glass[1][0], glass[1][1]);
        gr.addColorStop(0, "#DCEAF3"); gr.addColorStop(1, "#B9D2E2"); poly(g, glass, gr, "#FFFFFF");
        const mid = [p.x + p.nx * .5, p.y + p.ny * .5]; g.strokeStyle = "#FFFFFF"; g.lineWidth = Math.max(1.5, G.k * 3);
        g.beginPath(); g.moveTo(...prj(...mid, cm(93))); g.lineTo(...prj(...mid, cm(207))); g.stroke();
        /* sill */
        const s0 = [A1[0] - p.tx * cm(4), A1[1] - p.ty * cm(4)], s1 = [B1[0] + p.tx * cm(4), B1[1] + p.ty * cm(4)], sd = cm(10);
        poly(g, [prj(...s0, cm(88)), prj(...s1, cm(88)), prj(s1[0] + p.nx * sd, s1[1] + p.ny * sd, cm(88)), prj(s0[0] + p.nx * sd, s0[1] + p.ny * sd, cm(88))], "#FFFFFF", "#DDD9D3");
      } else if (p.op.k === "door") {
        poly(g, quad(0, cm(208), 0), "#FFFFFF", "#D9D5CF");
        poly(g, quad(0, cm(203), 0.6), shade(WHITE, .93), "#CFCBC4");
        const hp = [B1[0] - p.tx * cm(10) + p.nx, B1[1] - p.ty * cm(10) + p.ny], q = prj(...hp, cm(100));
        g.fillStyle = METAL; g.beginPath(); g.arc(q[0], q[1], Math.max(1.5, G.k * 2.5), 0, Math.PI * 2); g.fill();
      } else {
        const gr = g.createLinearGradient(...prj(...A1, cm(170)), ...prj(...B1, cm(100)));
        gr.addColorStop(0, "#E9EEF1"); gr.addColorStop(1, "#C5CDD2"); poly(g, quad(cm(100), cm(175), 0.5), gr, "#FFFFFF");
      }
    });
    /* wall top cap */
    poly(g, [prj(...e.a, WALL_H), prj(...e.b, WALL_H), prj(...out(e.b, e, WT), WALL_H), prj(...out(e.a, e, WT), WALL_H)], "#FFFFFF", "#E2DED8");
  });

  /* furniture: collect boxes, painter's sort by depth */
  const items = [];
  S.items.forEach(it => {
    const f = A.FI(it), o = A.oi(it);
    const L2P = (u, v) => [o.x + o.tx * u - o.bx * v, o.y + o.ty * u - o.by * v];
    parts(it, f).forEach(b => {
      if (b.ball || b.shade) { items.push({ d: depth(o.x, o.y) + 0.001, b, o, it }); return; }
      const [u0, u1, v0, v1] = b, c = L2P((u0 + u1) / 2, (v0 + v1) / 2);
      items.push({ d: depth(c[0], c[1]) + b[4] * 0.002, b, L2P, o });
    });
  });
  items.sort((p, q) => p.d - q.d).forEach(({ b, L2P, o }) => {
    if (b.ball) { const c = prj(o.x, o.y, b.z), r = b.r * G.k * 1.1; const gr = g.createRadialGradient(c[0] - r * .3, c[1] - r * .4, r * .1, c[0], c[1], r);
      gr.addColorStop(0, shade(b.col, 1.25)); gr.addColorStop(1, shade(b.col, .8)); g.fillStyle = gr; g.beginPath(); g.arc(c[0], c[1], r, 0, Math.PI * 2); g.fill(); return; }
    if (b.shade) { const c0 = prj(o.x, o.y, b.z0), c1 = prj(o.x, o.y, b.z1), rx = b.r * G.k * 1.22, ry = b.r * G.k * .7, on = A.S.lights;
      g.fillStyle = on ? "#FFE7A8" : b.col; g.beginPath(); g.ellipse(c0[0], c0[1], rx * 1.15, ry * 1.15, 0, 0, Math.PI); g.lineTo(c1[0] - rx * .8, c1[1]);
      g.ellipse(c1[0], c1[1], rx * .8, ry * .8, 0, Math.PI, 0, true); g.closePath(); g.fill(); g.strokeStyle = shade(b.col, .85); g.stroke(); return; }
    const [u0, u1, v0, v1, z0, z1, col] = b, base = [L2P(u0, v0), L2P(u1, v0), L2P(u1, v1), L2P(u0, v1)];
    const sides = [[0, 1, o.bx, o.by], [1, 2, o.tx, o.ty], [2, 3, -o.bx, -o.by], [3, 0, -o.tx, -o.ty]];
    sides.forEach(([i, j, nx, ny]) => { if (!vis(nx, ny)) return; const [ra, rb] = G.RN(nx, ny);
      poly(g, [prj(...base[i], z0), prj(...base[j], z0), prj(...base[j], z1), prj(...base[i], z1)], shade(col.startsWith("#") ? col : "#CCCCCC", ra > rb ? .9 : .78), "rgba(0,0,0,.08)"); });
    poly(g, base.map(p => prj(...p, z1)), col.startsWith("#") ? col : col, "rgba(0,0,0,.08)");
  });

  /* front walls cut low */
  E.filter(e => !e.back).forEach(e => {
    const lo = cm(6), a2 = out(e.a, e, WT), b2 = out(e.b, e, WT);
    poly(g, [prj(...a2, 0), prj(...b2, 0), prj(...b2, lo), prj(...a2, lo)], "#E9E6E1");
    poly(g, [prj(...e.a, lo), prj(...e.b, lo), prj(...b2, lo), prj(...a2, lo)], "#FFFFFF", "#E2DED8");
  });

  /* lights */
  if (S.lights) {
    g.save(); g.globalCompositeOperation = "source-atop"; g.fillStyle = "rgba(24,18,40,.5)"; g.fillRect(0, 0, W, G.H);
    S.items.filter(i => i.k === "lamp").forEach(it => {
      const o = A.oi(it), c = prj(o.x, o.y, 0), r = LR * G.k;
      g.save(); g.translate(c[0], c[1]); g.scale(1.22, 0.707);
      const gr = g.createRadialGradient(0, 0, 0, 0, 0, r); gr.addColorStop(0, "rgba(255,214,140,.75)"); gr.addColorStop(.5, "rgba(255,206,130,.35)"); gr.addColorStop(1, "rgba(255,200,120,0)");
      g.fillStyle = gr; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill(); g.restore();
      const s = prj(o.x, o.y, cm(150)), gs = g.createRadialGradient(s[0], s[1], 0, s[0], s[1], r * .6);
      gs.addColorStop(0, "rgba(255,226,160,.6)"); gs.addColorStop(1, "rgba(255,226,160,0)"); g.fillStyle = gs; g.fillRect(s[0] - r, s[1] - r, r * 2, r * 2);
    });
    g.restore();
  }
  return G.H;
}
function inside(x, y, p) { let c = false; for (let i = 0, j = p.length - 1; i < p.length; j = i++) { const [xi, yi] = p[i], [xj, yj] = p[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; }

/* ---------- UI ---------- */
const stage = document.querySelector(".fs .stage"), plan = document.getElementById("plan"), trash = document.getElementById("trash");
if (!stage) return;
const bar = document.createElement("div"); bar.className = "viewbar";
bar.innerHTML = `<div class="tgroup" role="group" aria-label="${T("View")}"><button type="button" class="chip" data-v="2d">${T("Plan")}</button><button type="button" class="chip" data-v="3d">3D</button></div>
<div class="look" hidden>
  <div class="tgroup" role="group" aria-label="${T("Floor")}"><span class="tlabel">${T("Floor")}</span>${Object.entries(FLOORS).map(([k, f]) => `<button type="button" class="sw" data-f="${k}" title="${T(f.n)}" aria-label="${T(f.n)}" style="background:${f.base}"></button>`).join("")}</div>
  <div class="tgroup" role="group" aria-label="${T("Walls")}"><span class="tlabel">${T("Walls")}</span>${WALLS.map(c => `<button type="button" class="sw" data-w="${c}" aria-label="${c}" style="background:${c}"></button>`).join("")}<label class="sw custom" title="${T("Custom colour")}"><input type="color" aria-label="${T("Custom colour")}"></label></div>
  <button type="button" class="chip" data-rot>⟳ ${T("Rotate")}</button>
</div>`;
stage.parentNode.insertBefore(bar, stage);
const cv = document.createElement("canvas"); cv.className = "v3d"; cv.hidden = true; cv.setAttribute("role", "img"); cv.setAttribute("aria-label", T("3D view of the room")); stage.appendChild(cv);
const lookEl = bar.querySelector(".look"), colorIn = bar.querySelector("input[type=color]");
let on = false;
function sync() {
  bar.querySelectorAll("[data-v]").forEach(b => b.setAttribute("aria-pressed", (b.dataset.v === "3d") === on));
  lookEl.hidden = !on; plan.style.display = on ? "none" : ""; if (trash) trash.style.display = on ? "none" : ""; cv.hidden = !on;
  const L = look(); bar.querySelectorAll("[data-f]").forEach(b => b.setAttribute("aria-pressed", b.dataset.f === L.floor));
  bar.querySelectorAll("[data-w]").forEach(b => b.setAttribute("aria-pressed", b.dataset.w.toLowerCase() === String(L.wall).toLowerCase()));
  colorIn.value = /^#[0-9a-f]{6}$/i.test(L.wall) ? L.wall : "#f4f2ee";
}
function update() { if (!on) return; const W = Math.max(280, stage.clientWidth); draw(cv, W, Math.min(2, window.devicePixelRatio || 1)); }
bar.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return; const L = look();
  if (b.dataset.v) { on = b.dataset.v === "3d"; try { localStorage.setItem("sapiopedia-roomplanner-view", on ? "3d" : "2d"); } catch (_) {} }
  else if (b.dataset.f) L.floor = b.dataset.f;
  else if (b.dataset.w) L.wall = b.dataset.w;
  else if (b.hasAttribute("data-rot")) L.rot = ((L.rot || 0) + 1) % 4;
  else return;
  A.save(); sync(); update();
});
colorIn.addEventListener("input", () => { look().wall = colorIn.value; A.save(); sync(); update(); });
try { on = localStorage.getItem("sapiopedia-roomplanner-view") === "3d"; } catch (_) {}
if (window.ResizeObserver) new ResizeObserver(() => update()).observe(stage);

/* PNG of the 3D view with the Sapiopedia band */
async function png() {
  const W = 1600, c = document.createElement("canvas"), h = draw(c, W - 140, 1), BAND = 200, GAP = 40, H = 70 + h + GAP + BAND;
  const out = document.createElement("canvas"); out.width = W; out.height = H; const x = out.getContext("2d");
  x.fillStyle = "#FFFFFF"; x.fillRect(0, 0, W, H); x.drawImage(c, 70, 70);
  const by = 70 + h + GAP; x.fillStyle = "#F7E9EC"; x.fillRect(0, by, W, BAND); x.fillStyle = "#DCC9CE"; x.fillRect(0, by, W, 2);
  const logo = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = "/assets/logo-horizontal.png"; });
  const lh = 120; x.drawImage(logo, 60, by + (BAND - lh) / 2, logo.width * lh / logo.height, lh);
  const P = A.pts(), xs = P.map(q => q[0]), ys = P.map(q => q[1]), loc = document.documentElement.lang || "en";
  const m = v => (v / PX).toLocaleString(loc, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  x.textAlign = "right"; x.fillStyle = "#2A1F26"; x.font = "600 36px 'Source Sans 3', Arial, sans-serif";
  x.fillText(A.FR ? "sapiopedia.com/fr/outils/planificateur-de-piece" : "sapiopedia.com/en/tools/room-planner", W - 70, by + 82);
  x.fillStyle = "#6E5A62"; x.font = "400 24px 'Source Sans 3', Arial, sans-serif";
  x.fillText(T("Room Planner") + " · " + T("Room ≈ {w} × {h} m", { w: m(Math.max(...xs) - Math.min(...xs)), h: m(Math.max(...ys) - Math.min(...ys)) }), W - 70, by + 124);
  return await new Promise(res => out.toBlob(res, "image/png"));
}
window.FS3D = { update, active: () => on, png };
sync(); update();
})();
