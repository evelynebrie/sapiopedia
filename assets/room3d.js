/* Sapiopedia Room Planner: 3D (isometric cut-away) view. Reads the plan through window.FSAPI. */
(function () {
"use strict";
const A = window.FSAPI; if (!A) return;
const VKEY = A.DESIGN ? "sapiopedia-roomplanner-view" : "sapiopedia-fengshui-view";
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
  let r, g, b;
  if (hex[0] === "#") { const n = parseInt(hex.slice(1), 16); r = n >> 16; g = (n >> 8) & 255; b = n & 255; }
  else { const m = String(hex).match(/[\d.]+/g) || [200, 200, 200]; [r, g, b] = m.map(Number); }
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

/* ---------- furniture models: primitives in local px (u along width, v<0 = back), heights in cm ---------- */
function parts(it, f) {
  const w = f.w, h = f.h, W2 = w / 2, H2 = h / 2, B = [];
  const box = (u0, u1, v0, v1, z0, z1, col, deco) => { const b = { t: "box", u0, u1, v0, v1, z0: cm(z0), z1: cm(z1), col, deco: deco || [] }; B.push(b); return b; };
  const cyl = (u, v, r, z0, z1, col, top) => B.push({ t: "cyl", u, v, r, z0: cm(z0), z1: cm(z1), col, top: top || col });
  const ball = (u, v, r, z, col) => B.push({ t: "ball", u, v, r, z: cm(z), col });
  const fl = (u0, u1, z0, z1, col) => ({ face: "front", seg: [[u0, z0], [u1, z1]], col: col || "rgba(0,0,0,.18)" }); /* line on the front face */
  const legs = (zt, col, s, inset) => { const i = inset || 0; [[-W2 + i, -H2 + i], [W2 - s - i, -H2 + i], [-W2 + i, H2 - s - i], [W2 - s - i, H2 - s - i]].forEach(([u, v]) => box(u, u + s, v, v + s, 0, zt, col)); };
  switch (it.k) {
    case "bed": {
      legs(10, DARK, cm(5), cm(3));
      box(-W2, W2, -H2, -H2 + cm(7), 10, 112, "#CBBDA9");                       /* upholstered headboard */
      box(-W2, W2, -H2 + cm(7), H2, 10, 30, WOOD);                               /* frame */
      box(-W2 + cm(2), W2 - cm(2), -H2 + cm(7), H2 - cm(2), 30, 52, "#FAF9F6");  /* mattress */
      const pw = (w - cm(14)) / 2;
      [0, 1].forEach(i => box(-W2 + cm(5) + i * (pw + cm(4)), -W2 + cm(5) + i * (pw + cm(4)) + pw, -H2 + cm(11), -H2 + cm(45), 52, 64, "#FFFFFF"));
      box(-W2 - 1, W2 + 1, -H2 + cm(62), H2 + 1, 50, 57, "#AFC2CC");           /* duvet */
      box(-W2 - 1, W2 + 1, -H2 + cm(56), -H2 + cm(66), 52, 59, "#C9D6DD");      /* folded edge */
      break; }
    case "desk":
      legs(72, METAL, cm(3), cm(2));
      box(W2 - cm(42), W2 - cm(4), -H2 + cm(4), H2 - cm(4), 18, 72, shade(WOOD, .96), [fl(W2 - cm(42), W2 - cm(4), 45, 45), fl(W2 - cm(28), W2 - cm(18), 58, 58, METAL), fl(W2 - cm(28), W2 - cm(18), 31, 31, METAL)]);
      box(-W2, W2, -H2, H2, 72, 75, WOOD); break;
    case "coffee":
      legs(36, shade(WOOD, .8), cm(4), cm(3)); box(-W2 + cm(3), W2 - cm(3), -H2 + cm(3), H2 - cm(3), 10, 12, shade(WOOD, .92)); box(-W2, W2, -H2, H2, 36, 40, WOOD); break;
    case "table":
      legs(72, shade(WOOD, .85), cm(5), cm(4)); box(-W2, W2, -H2, H2, 72, 76, WOOD); break;
    case "chair": {
      const s = cm(3);
      legs(45, shade(WOOD, .9), s, cm(1));
      box(-W2, W2, -H2, H2, 45, 48, shade(WOOD, .95));
      box(-W2 + cm(2), W2 - cm(2), -H2 + cm(4), H2 - cm(2), 48, 51, "#CFC5B6");   /* seat pad */
      box(-W2 + cm(1), -W2 + cm(1) + s, -H2 + cm(1), -H2 + cm(1) + s, 48, 92, shade(WOOD, .9));
      box(W2 - cm(1) - s, W2 - cm(1), -H2 + cm(1), -H2 + cm(1) + s, 48, 92, shade(WOOD, .9));
      box(-W2 + cm(1), W2 - cm(1), -H2 + cm(1), -H2 + cm(1) + s, 82, 91, WOOD);   /* top rail */
      box(-W2 + cm(1), W2 - cm(1), -H2 + cm(1), -H2 + cm(1) + s, 64, 68, WOOD);   /* slat */
      break; }
    case "sofa": case "armchair": {
      const arm = Math.min(cm(18), w * .2), back = cm(20), n = it.k === "sofa" ? (w > cm(170) ? 3 : 2) : 1, cw = (w - arm * 2) / n, FAB = "#BDB6AC";
      legs(10, DARK, cm(4), cm(3));
      box(-W2, W2, -H2, H2, 10, 38, shade(FAB, .95));
      box(-W2, W2, -H2, -H2 + cm(12), 38, 82, shade(FAB, .93));
      box(-W2, -W2 + arm, -H2, H2, 38, 62, FAB); box(W2 - arm, W2, -H2, H2, 38, 62, FAB);
      for (let i = 0; i < n; i++) {
        const u0 = -W2 + arm + i * cw + 1, u1 = u0 + cw - 2;
        box(u0, u1, -H2 + back, H2 - cm(2), 38, 48, shade(FAB, 1.06));          /* seat cushion */
        box(u0, u1, -H2 + cm(12), -H2 + back, 44, 78, shade(FAB, 1.02));        /* back cushion */
      }
      break; }
    case "tv":
      box(-cm(15), cm(15), -H2, H2, 0, 2, DARK); box(-cm(3), cm(3), -H2 + cm(4), -H2 + cm(8), 2, 60, DARK);
      box(-W2, W2, -H2, -H2 + cm(5), 58, 58 + w / PX * 100 * 0.56, "#1C1D20"); break;
    case "wardrobe": {
      const ww = w / 2;
      box(-W2, W2, -H2, H2, 0, 6, shade(WHITE, .85));
      box(-W2, W2, -H2, H2, 6, 205, WHITE, [fl(0, 0, 8, 203), fl(-cm(5), -cm(5), 95, 125, METAL), fl(cm(5), cm(5), 95, 125, METAL)].concat(ww > cm(70) ? [fl(-W2 / 2 * 0 - ww / 2, -ww / 2, 8, 203)] : []));
      break; }
    case "countertop": {
      const doors = Math.max(1, Math.round(w / cm(60))), dw = w / doors, deco = [];
      for (let i = 1; i < doors; i++) deco.push(fl(-W2 + i * dw, -W2 + i * dw, 10, 84));
      for (let i = 0; i < doors; i++) deco.push(fl(-W2 + i * dw + cm(6), -W2 + i * dw + dw - cm(6), 78, 78, METAL));
      box(-W2 + cm(2), W2 - cm(2), -H2, H2 - cm(6), 0, 10, DARK);
      box(-W2, W2, -H2, H2 - cm(3), 10, 86, WHITE, deco);
      box(-W2, W2, -H2, H2, 86, 90, "#9A958F"); break; }
    case "appliance":
      box(-W2, W2, -H2, H2, 0, 85, "#ECEEEF", [fl(-W2 + cm(2), W2 - cm(2), 72, 72), fl(-W2 + cm(10), W2 - cm(10), 40, 40, "rgba(0,0,0,.25)"), fl(-W2 + cm(10), -W2 + cm(10), 20, 60, "rgba(0,0,0,.25)"), fl(W2 - cm(10), W2 - cm(10), 20, 60, "rgba(0,0,0,.25)")]); break;
    case "shelf": {
      const t = cm(2), BOOKS = ["#9C6B5A", "#5F7A8A", "#C8A96A", "#7E8C6B", "#B9877A", "#4F5B66"], r = rnd(it.id * 31 + 7);
      box(-W2, W2, -H2, -H2 + cm(1.5), 0, 185, shade(WOOD, .9));
      [0, 45, 90, 135, 183].forEach(z => box(-W2, W2, -H2, H2, z, z + 2, WOOD));
      [45, 90, 135].forEach(z0 => { let u = -W2 + t + cm(2); while (u < W2 - t - cm(8)) { const bw = cm(3 + r() * 3), bh = 26 + r() * 12; if (r() > .2) box(u, u + bw, -H2 + cm(4), H2 - cm(4), z0 + 2, z0 + 2 + bh, BOOKS[Math.floor(r() * BOOKS.length)]); u += bw + cm(.5); } });
      box(-W2, -W2 + t, -H2, H2, 0, 185, WOOD); box(W2 - t, W2, -H2, H2, 0, 185, WOOD); break; }
    case "screen": { const pw = w / 3; [0, 1, 2].forEach(i => box(-W2 + i * pw + 1, -W2 + (i + 1) * pw - 1, (i % 2 ? -1 : 1) * cm(3) - cm(1.5), (i % 2 ? -1 : 1) * cm(3) + cm(1.5), 4, 170, "#E6D8C2")); break; }
    case "plant":
      cyl(0, 0, W2 * .48, 0, 34, "#B66E4A", "#5A4636");
      [[0, 0, .62, 78], [-.35, .2, .45, 64], [.35, -.15, .45, 66], [.1, .35, .4, 92], [-.15, -.3, .42, 96]].forEach(([u, v, r, z], i) => ball(u * W2, v * W2, r * W2, z, ["#6E9461", "#5F8656", "#7FA36F", "#6A9060", "#88AC77"][i])); break;
    case "lamp":
      cyl(0, 0, W2 * .5, 0, 3, "#4A4A4D", "#5E5E62");
      cyl(0, 0, cm(1), 3, 132, "#55555A", "#55555A");
      cyl(0, 0, W2 * .72, 130, 160, A.S.lights ? "#FFE3A0" : "#EFE4D0", A.S.lights ? "#FFF2CC" : "#F7EFE2"); break;
    default: box(-W2, W2, -H2, H2, 0, 60, "#C3BBB0");
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
        poly(g, quad(cm(95), cm(180), 0.4), "#C9AE8A");
        const gr = g.createLinearGradient(...prj(...A1, cm(176)), ...prj(...B1, cm(99)));
        gr.addColorStop(0, "#F6F9FB"); gr.addColorStop(.5, "#DCE5EA"); gr.addColorStop(1, "#C3CFD6"); poly(g, quad(cm(99), cm(176), 0.8), gr);
      }
    });
    /* wall top cap */
    poly(g, [prj(...e.a, WALL_H), prj(...e.b, WALL_H), prj(...out(e.b, e, WT), WALL_H), prj(...out(e.a, e, WT), WALL_H)], "#FFFFFF", "#E2DED8");
  });

  /* contact shadows */
  g.save(); g.filter = "blur(" + Math.max(2, G.k * 5).toFixed(1) + "px)"; g.fillStyle = "rgba(60,45,35,.16)";
  S.items.forEach(it => { const f = A.FI(it), o = A.oi(it);
    if (f.round) { const c = prj(o.x, o.y, 0); g.beginPath(); g.ellipse(c[0], c[1], f.w / 2 * G.k * 1.1, f.w / 2 * G.k * .64, 0, 0, Math.PI * 2); g.fill(); return; }
    const L2P = (u, v) => [o.x + o.tx * u - o.bx * v, o.y + o.ty * u - o.by * v], W2 = f.w / 2 + 2, H2 = f.h / 2 + 2;
    poly(g, [L2P(-W2, -H2), L2P(W2, -H2), L2P(W2, H2), L2P(-W2, H2)].map(p => prj(p[0], p[1], 0)), "rgba(60,45,35,.16)"); });
  g.restore();

  /* furniture: painter's sort of primitives by depth */
  const items = [];
  S.items.forEach(it => {
    const f = A.FI(it), o = A.oi(it), L2P = (u, v) => [o.x + o.tx * u - o.bx * v, o.y + o.ty * u - o.by * v];
    parts(it, f).forEach((b, idx) => {
      const c = b.t === "box" ? L2P((b.u0 + b.u1) / 2, (b.v0 + b.v1) / 2) : L2P(b.u, b.v);
      items.push({ d: depth(c[0], c[1]) + (b.z0 != null ? b.z0 : b.z) * 0.004 + idx * 1e-6, b, L2P, o });
    });
  });
  items.sort((p, q) => p.d - q.d).forEach(({ b, L2P, o }) => {
    if (b.t === "ball") { const p = L2P(b.u, b.v), c = prj(p[0], p[1], b.z), r = b.r * G.k * 1.1;
      const gr = g.createRadialGradient(c[0] - r * .35, c[1] - r * .45, r * .1, c[0], c[1], r);
      gr.addColorStop(0, shade(b.col, 1.22)); gr.addColorStop(1, shade(b.col, .78)); g.fillStyle = gr; g.beginPath(); g.arc(c[0], c[1], r, 0, Math.PI * 2); g.fill(); return; }
    if (b.t === "cyl") { const p = L2P(b.u, b.v), c0 = prj(p[0], p[1], b.z0), c1 = prj(p[0], p[1], b.z1), rx = b.r * G.k * 1.2247, ry = b.r * G.k * .7071;
      const gr = g.createLinearGradient(c0[0] - rx, 0, c0[0] + rx, 0); gr.addColorStop(0, shade(b.col, 1.08)); gr.addColorStop(.55, shade(b.col, .95)); gr.addColorStop(1, shade(b.col, .78));
      g.beginPath(); g.moveTo(c0[0] + rx, c0[1]); g.ellipse(c0[0], c0[1], rx, ry, 0, 0, Math.PI); g.lineTo(c1[0] - rx, c1[1]); g.lineTo(c1[0] + rx, c1[1]); g.closePath(); g.fillStyle = gr; g.fill();
      g.beginPath(); g.ellipse(c1[0], c1[1], rx, ry, 0, 0, Math.PI * 2); g.fillStyle = b.top; g.fill(); g.strokeStyle = "rgba(0,0,0,.08)"; g.lineWidth = 1; g.stroke(); return; }
    const { u0, u1, v0, v1, z0, z1, col } = b, base = [L2P(u0, v0), L2P(u1, v0), L2P(u1, v1), L2P(u0, v1)];
    const sides = [[0, 1, o.bx, o.by, "back"], [1, 2, o.tx, o.ty, "right"], [2, 3, -o.bx, -o.by, "front"], [3, 0, -o.tx, -o.ty, "left"]], shown = {};
    sides.forEach(([i, j, nx, ny, name]) => { if (!vis(nx, ny)) return; shown[name] = true; const [ra, rb] = G.RN(nx, ny);
      poly(g, [prj(...base[i], z0), prj(...base[j], z0), prj(...base[j], z1), prj(...base[i], z1)], shade(col, ra > rb ? .92 : .8), "rgba(0,0,0,.06)"); });
    poly(g, base.map(p => prj(...p, z1)), col, "rgba(0,0,0,.06)");
    if (shown.front) b.deco.forEach(dc => { const [[ua, za], [ub, zb]] = dc.seg, pa = L2P(ua, v1 + .3), pb = L2P(ub, v1 + .3);
      g.strokeStyle = dc.col; g.lineWidth = Math.max(1, G.k * 1.4); g.lineCap = "round"; g.beginPath(); g.moveTo(...prj(...pa, cm(za))); g.lineTo(...prj(...pb, cm(zb))); g.stroke(); });
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
bar.innerHTML = `<div class="seg" role="group" aria-label="${T("View")}"><button type="button" data-v="2d"><svg viewBox="0 0 20 20" aria-hidden="true"><rect x="2.5" y="2.5" width="15" height="15" rx="1.5"/><path d="M2.5 9h7v8.5M9.5 9V2.5"/></svg>${T("2D plan")}</button><button type="button" data-v="3d"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2 17.5 6v8L10 18 2.5 14V6z"/><path d="M2.5 6 10 10l7.5-4M10 10v8"/></svg>${T("3D view")}</button></div>
<div class="look" hidden>
  <div class="tgroup" role="group" aria-label="${T("Floor")}"><span class="tlabel">${T("Floor")}</span>${Object.entries(FLOORS).map(([k, f]) => `<button type="button" class="sw" data-f="${k}" title="${T(f.n)}" aria-label="${T(f.n)}" style="background:${f.base}"></button>`).join("")}</div>
  <div class="tgroup" role="group" aria-label="${T("Walls")}"><span class="tlabel">${T("Walls")}</span>${WALLS.map(c => `<button type="button" class="sw" data-w="${c}" aria-label="${c}" style="background:${c}"></button>`).join("")}<label class="sw custom" title="${T("Custom colour")}"><input type="color" aria-label="${T("Custom colour")}"></label></div>
  <button type="button" class="chip" data-rot>⟳ ${T("Rotate")}</button>
</div>`;
const work = document.querySelector(".fs .work"); work.insertBefore(bar, work.firstChild); const lookEl0 = bar.querySelector(".look"); stage.parentNode.insertBefore(lookEl0, stage);
const cv = document.createElement("canvas"); cv.className = "v3d"; cv.hidden = true; cv.setAttribute("role", "img"); cv.setAttribute("aria-label", T("3D view of the room")); stage.appendChild(cv);
const lookEl = lookEl0, colorIn = lookEl0.querySelector("input[type=color]");
let on = false;
function sync() {
  bar.querySelectorAll("[data-v]").forEach(b => b.setAttribute("aria-pressed", (b.dataset.v === "3d") === on));
  lookEl.hidden = !on; plan.style.display = on ? "none" : ""; if (trash) trash.style.display = on ? "none" : ""; cv.hidden = !on || !!GL; if (GL) WRAP.hidden = !on;
  const L = look(); lookEl.querySelectorAll("[data-f]").forEach(b => b.setAttribute("aria-pressed", b.dataset.f === L.floor));
  lookEl.querySelectorAll("[data-w]").forEach(b => b.setAttribute("aria-pressed", b.dataset.w.toLowerCase() === String(L.wall).toLowerCase()));
  colorIn.value = /^#[0-9a-f]{6}$/i.test(L.wall) ? L.wall : "#f4f2ee";
}
/* WebGL view (three.js + Kenney models), loaded on first use; the drawn view above is the fallback */
let GL = null, glp = null, busy = false, again = false;
const WRAP = document.createElement("div"); WRAP.className = "v3dwrap"; const MARKS = document.createElement("div"); MARKS.className = "marks3d"; MARKS.setAttribute("aria-hidden", "true");
const SYM = { good: "✓", caution: "!", bad: "✕" };
function placeMarks(gl) { if (A.DESIGN || !gl) { MARKS.innerHTML = ""; return; }
  MARKS.innerHTML = gl.marks.map(m => { const it = A.S.items.find(i => i.id === m.id), v = it && A.verdict(it); return v && SYM[v] ? `<span class="fsmark ${v}" style="left:${(m.x * 100).toFixed(2)}%;top:${(m.y * 100).toFixed(2)}%">${SYM[v]}</span>` : ""; }).join(""); }
function ensureGL() {
  if (!glp) glp = import("/assets/room3d-gl.js").then(m => { GL = m.create(A, () => Object.assign({}, look(), { floors: FLOORS }));
    GL.el.setAttribute("aria-label", T("3D view of the room")); WRAP.appendChild(GL.el); WRAP.appendChild(MARKS); WRAP.hidden = !on; stage.appendChild(WRAP); cv.hidden = true; return GL; })
    .catch(err => { console.warn("3D view fallback:", err); GL = null; return null; });
  return glp;
}
function update() {
  if (!on) return; const W = Math.max(280, stage.clientWidth), dpr = Math.min(2, window.devicePixelRatio || 1);
  if (busy) { again = true; return; } busy = true;
  ensureGL().then(gl => gl ? gl.render(W, dpr).then(() => placeMarks(gl)) : draw(cv, W, dpr)).catch(() => draw(cv, W, dpr))
    .finally(() => { busy = false; if (again) { again = false; update(); } });
}
const onClick = e => {
  const b = e.target.closest("button"); if (!b) return; const L = look();
  if (b.dataset.v) { on = b.dataset.v === "3d"; try { localStorage.setItem(VKEY, on ? "3d" : "2d"); } catch (_) {} }
  else if (b.dataset.f) L.floor = b.dataset.f;
  else if (b.dataset.w) L.wall = b.dataset.w;
  else if (b.hasAttribute("data-rot")) L.rot = ((L.rot || 0) + 1) % 4;
  else return;
  A.save(); sync(); update();
};
bar.addEventListener("click", onClick); lookEl.addEventListener("click", onClick);
colorIn.addEventListener("input", () => { look().wall = colorIn.value; A.save(); sync(); update(); });
try { on = localStorage.getItem(VKEY) === "3d"; } catch (_) {}
if (window.ResizeObserver) new ResizeObserver(() => update()).observe(stage);

/* PNG export: 2D plan on the left, 3D view on the right, Sapiopedia band below */
async function png() {
  const plan = await A.planShot();
  const W = 2200, PAD = 70, GAP = 70, COL = (W - PAD * 2 - GAP) / 2, HEAD = 64;
  const gl = await ensureGL(); let c3, h3;
  if (gl) { h3 = await gl.render(COL, 1); c3 = gl.el; } else { c3 = document.createElement("canvas"); h3 = draw(c3, COL, 1); }
  const pw = COL, ph = Math.round(plan.h * COL / plan.w), bodyH = Math.max(ph, h3) + 60, BAND = 200;
  const H = PAD + HEAD + bodyH + BAND;
  const out = document.createElement("canvas"); out.width = W; out.height = H; const x = out.getContext("2d");
  x.fillStyle = "#FFFFFF"; x.fillRect(0, 0, W, H);
  x.font = "600 22px 'Source Sans 3', Arial, sans-serif"; x.fillStyle = "#6E5A62"; x.textAlign = "left";
  const sp = s => s.toUpperCase().split("").join(String.fromCharCode(8202));
  x.fillText(sp(T("2D plan")), PAD, PAD + 24); x.fillText(sp(T("3D view")), PAD + COL + GAP, PAD + 24);
  const top = PAD + HEAD, mid = top + (bodyH - 60) / 2;
  x.drawImage(plan.img, PAD, mid - ph / 2, pw, ph);
  x.drawImage(c3, PAD + COL + GAP, mid - h3 / 2);
  if (gl && !A.DESIGN) gl.marks.forEach(m => { const it = A.S.items.find(i => i.id === m.id), v = it && A.verdict(it); if (!v || !SYM[v]) return;
    const cx = PAD + COL + GAP + m.x * COL, cy = mid - h3 / 2 + m.y * h3; x.beginPath(); x.arc(cx, cy, 15, 0, Math.PI * 2);
    x.fillStyle = v === "good" ? "#3F8A68" : v === "bad" ? "#C2503B" : "#B58A2E"; x.fill(); x.lineWidth = 3; x.strokeStyle = "#fff"; x.stroke();
    x.fillStyle = "#fff"; x.font = "800 18px 'Source Sans 3', Arial, sans-serif"; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(SYM[v], cx, cy + 1); x.textAlign = "left"; x.textBaseline = "alphabetic"; });
  x.fillStyle = "#EADDE1"; x.fillRect(PAD + COL + GAP / 2 - 1, top, 2, bodyH - 60);
  /* legend under the plan */
  const LEG = [[plan.VL.good, "rgba(63,138,104,.18)", "#3f8a68"], [plan.VL.caution, "rgba(181,138,46,.17)", "#b58a2e"], [plan.VL.bad, "rgba(194,80,59,.16)", "#c2503b"]];
  x.font = "500 22px 'Source Sans 3', Arial, sans-serif"; x.textBaseline = "middle"; let lx = PAD; const ly = top + bodyH - 30;
  LEG.forEach(([t, bg, st]) => { x.fillStyle = bg; x.fillRect(lx, ly - 11, 22, 22); x.strokeStyle = st; x.lineWidth = 2.5; x.strokeRect(lx + 1, ly - 10, 20, 20); x.fillStyle = "#2A1F26"; x.fillText(t, lx + 32, ly + 1); lx += 32 + x.measureText(t).width + 36; });
  x.textBaseline = "alphabetic";
  const by = H - BAND; x.fillStyle = "#F7E9EC"; x.fillRect(0, by, W, BAND); x.fillStyle = "#DCC9CE"; x.fillRect(0, by, W, 2);
  const lh = 120; x.drawImage(plan.logo, PAD - 10, by + (BAND - lh) / 2, plan.logo.width * lh / plan.logo.height, lh);
  x.textAlign = "right"; x.fillStyle = "#2A1F26"; x.font = "600 36px 'Source Sans 3', Arial, sans-serif";
  x.fillText(A.DESIGN ? (A.FR ? "sapiopedia.com/fr/outils/planificateur-de-piece" : "sapiopedia.com/en/tools/room-planner") : (A.FR ? "sapiopedia.com/fr/outils/fengshui" : "sapiopedia.com/en/tools/fengshui"), W - PAD, by + 82);
  x.fillStyle = "#6E5A62"; x.font = "400 24px 'Source Sans 3', Arial, sans-serif";
  x.fillText((A.DESIGN ? T("Room Planner") : T("Feng Shui Room Planner")) + " · " + plan.dims, W - PAD, by + 124);
  x.fillText(`${plan.counts.good} ${plan.VW.good} · ${plan.counts.caution} ${plan.VW.caution} · ${plan.counts.bad} ${plan.VW.bad}`, W - PAD, by + 158);
  const blob = await new Promise(res => out.toBlob(res, "image/png")); update(); return blob;
}
window.FS3D = { update, active: () => on, png };
sync(); update();
})();
