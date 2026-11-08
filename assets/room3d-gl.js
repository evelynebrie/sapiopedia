/* Sapiopedia Room Planner: WebGL 3D view (three.js + Kenney Furniture Kit, CC0). View only. */
import * as THREE from "three";
import { GLTFLoader } from "/assets/vendor/three/examples/jsm/loaders/GLTFLoader.js";

const MODEL = {
  bed: "bedDouble", desk: "desk", chair: "chair", table: "table", coffee: "tableCoffee", sofa: "loungeSofa",
  armchair: "loungeChair", tv: "televisionModern", wardrobe: "bookcaseClosedDoors", shelf: "bookcaseOpen",
  appliance: "washer", plant: "pottedPlant", lamp: "lampRoundFloor", countertop: "kitchenCabinet"
};
const EXTRA = ["kitchenSink"];
/* real-world heights in cm (the footprint comes from the plan) */
const HEIGHT = { bed: 95, desk: 75, chair: 90, table: 75, coffee: 42, sofa: 82, armchair: 80, tv: 70, wardrobe: 205, shelf: 185, appliance: 85, plant: 110, lamp: 160, countertop: 90 };

export function create(A, look) {
  const PX = A.PXM, cm = c => c * PX / 100, WALL_H = cm(250), WT = cm(12), SLAB = cm(14), LR = 2.5 * PX;
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.2;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const el = renderer.domElement; el.className = "v3d gl"; el.setAttribute("role", "img");

  const loader = new GLTFLoader(), cache = {};
  const loadAll = Promise.all([...new Set(Object.values(MODEL).concat(EXTRA))].map(n =>
    loader.loadAsync(`/assets/models/${n}.glb`).then(g => { cache[n] = g.scene; }).catch(() => {})));

  /* ---------- materials & textures ---------- */
  const texCache = {};
  function floorTexture(key, F) {
    if (texCache[key]) return texCache[key];
    const c = document.createElement("canvas"); c.width = c.height = 1024; const g = c.getContext("2d");
    g.fillStyle = F.base; g.fillRect(0, 0, 1024, 1024);
    let s = 11; const r = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
    if (F.type === "plank") {
      const rows = 10, ph = 1024 / rows;
      for (let i = 0; i < rows; i++) {
        let x = -r() * 400;
        while (x < 1024) { const len = 260 + r() * 300, t = 0.9 + r() * 0.16;
          g.fillStyle = tint(F.base, t); g.fillRect(x, i * ph, len, ph);
          g.globalAlpha = .08; g.strokeStyle = F.line; for (let k = 0; k < 6; k++) { g.beginPath(); const yy = i * ph + r() * ph; g.moveTo(x, yy); g.bezierCurveTo(x + len * .3, yy + 4, x + len * .6, yy - 4, x + len, yy); g.stroke(); } g.globalAlpha = 1;
          g.fillStyle = F.line; g.fillRect(x, i * ph, 2, ph); x += len; }
        g.fillStyle = F.line; g.fillRect(0, i * ph, 1024, 2);
      }
    } else if (F.type === "tile") {
      g.fillStyle = F.line; for (let i = 0; i <= 4; i++) { g.fillRect(i * 256 - 2, 0, 4, 1024); g.fillRect(0, i * 256 - 2, 1024, 4); }
    } else {
      for (let i = 0; i < 9000; i++) { g.fillStyle = r() > .5 ? tint(F.base, .93) : tint(F.base, 1.06); g.globalAlpha = .5; g.fillRect(r() * 1024, r() * 1024, 2, 2); } g.globalAlpha = 1;
    }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.anisotropy = renderer.capabilities.getMaxAnisotropy(); texCache[key] = t; return t;
  }
  function tint(hex, f) { const n = parseInt(hex.slice(1), 16), c = v => Math.max(0, Math.min(255, Math.round(v * f))); return `rgb(${c(n >> 16)},${c((n >> 8) & 255)},${c(n & 255)})`; }
  const M = (color, o) => new THREE.MeshStandardMaterial(Object.assign({ color, roughness: .85, metalness: 0 }, o || {}));

  /* ---------- scene build ---------- */
  function build(width) {
    const S = A.S, L = look(), FL = L.floors[L.floor] || L.floors.oak, P = A.pts(), n = P.length;
    const scene = new THREE.Scene();
    const [cx, cz] = A.centroid(P);
    const az = Math.PI / 4 + (L.rot || 0) * Math.PI / 2, view = [Math.sin(az), Math.cos(az)];
    const lightsOn = !!S.lights && S.items.some(i => i.k === "lamp");

    /* edges with inward normals */
    const inside = (x, y) => { let c = false; for (let i = 0, j = n - 1; i < n; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; };
    const E = P.map((a, i) => { const b = P[(i + 1) % n], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy); let nx = -dy / len, ny = dx / len;
      if (!inside((a[0] + b[0]) / 2 + nx * 4, (a[1] + b[1]) / 2 + ny * 4)) { nx = -nx; ny = -ny; }
      return { a, b, dx: dx / len, dy: dy / len, len, nx, ny, i, back: nx * view[0] + ny * view[1] > 0.02 }; });

    /* floor + slab */
    const shape = new THREE.Shape(P.map(p => new THREE.Vector2(p[0], p[1])));
    const fg = new THREE.ShapeGeometry(shape); fg.rotateX(Math.PI / 2);
    const tex = floorTexture(L.floor, FL).clone(); tex.needsUpdate = true; const rep = 1 / cm(200); tex.repeat.set(rep, rep);
    const floor = new THREE.Mesh(fg, M(0xffffff, { map: tex, side: THREE.DoubleSide, roughness: .7 })); floor.receiveShadow = true; floor.position.y = 0.2; scene.add(floor);
    const outer = P.map((p, i) => { const e1 = E[(i - 1 + n) % n], e2 = E[i]; return new THREE.Vector2(p[0] - (e1.nx + e2.nx) * WT, p[1] - (e1.ny + e2.ny) * WT); });
    const sg = new THREE.ExtrudeGeometry(new THREE.Shape(outer), { depth: SLAB, bevelEnabled: false }); sg.rotateX(Math.PI / 2);
    const slab = new THREE.Mesh(sg, M(0xEAE7E2)); slab.receiveShadow = true; scene.add(slab);

    /* walls with openings */
    const wallMat = M(new THREE.Color(L.wall || "#F4F2EE"), { roughness: .95 }), capMat = M(0xffffff, { roughness: .9 });
    const white = M(0xFAFAF8, { roughness: .6 }), glass = new THREE.MeshPhysicalMaterial({ color: 0xCFE3EE, roughness: .05, metalness: 0, transmission: 0, transparent: true, opacity: .35 });
    const boxOnEdge = (e, s0, s1, z0, z1, depth0, depth1, mat, cast) => { /* depth measured into the room from the inner wall line (negative = into the wall) */
      const len = s1 - s0, d = depth1 - depth0, m = new THREE.Mesh(new THREE.BoxGeometry(len, z1 - z0, d), mat);
      const sm = (s0 + s1) / 2, dm = (depth0 + depth1) / 2;
      m.position.set(e.a[0] + e.dx * sm + e.nx * dm, (z0 + z1) / 2, e.a[1] + e.dy * sm + e.ny * dm);
      m.rotation.y = Math.atan2(-e.dy, e.dx); m.castShadow = !!cast; m.receiveShadow = true; scene.add(m); return m; };
    const opens = S.opens.map(op => Object.assign({ op }, A.openPos(op))).filter(p => p && isFinite(p.x));
    E.forEach(e => {
      const H = e.back ? WALL_H : cm(8), list = opens.filter(p => p.edge === e.i && p.op.k !== "mirror")
        .map(p => { const c = (p.x - e.a[0]) * e.dx + (p.y - e.a[1]) * e.dy; return { p, s0: c - p.len / 2, s1: c + p.len / 2 }; }).sort((x, y) => x.s0 - y.s0);
      let s = -WT;
      list.forEach(o => {
        boxOnEdge(e, s, o.s0, 0, H, -WT, 0, wallMat, true);
        if (e.back) {
          const lo = o.p.op.k === "window" ? cm(88) : 0, hi = o.p.op.k === "window" ? cm(212) : cm(208);
          if (lo > 0) boxOnEdge(e, o.s0, o.s1, 0, lo, -WT, 0, wallMat, true);
          boxOnEdge(e, o.s0, o.s1, hi, H, -WT, 0, wallMat, true);
          if (o.p.op.k === "window") {
            boxOnEdge(e, o.s0, o.s1, lo + cm(2), hi - cm(2), -WT / 2 - 0.5, -WT / 2 + 0.5, glass);
            [[o.s0, o.s0 + cm(5)], [o.s1 - cm(5), o.s1], [(o.s0 + o.s1) / 2 - cm(2.5), (o.s0 + o.s1) / 2 + cm(2.5)]].forEach(([a, b]) => boxOnEdge(e, a, b, lo, hi, -WT / 2 - cm(3), -WT / 2 + cm(3), white));
            boxOnEdge(e, o.s0, o.s1, lo, lo + cm(5), -WT / 2 - cm(3), -WT / 2 + cm(3), white); boxOnEdge(e, o.s0, o.s1, hi - cm(5), hi, -WT / 2 - cm(3), -WT / 2 + cm(3), white);
            boxOnEdge(e, o.s0 - cm(5), o.s1 + cm(5), lo - cm(3), lo, -cm(2), cm(8), white, true);   /* sill */
          } else {
            boxOnEdge(e, o.s0 + cm(3), o.s1 - cm(3), 0, hi - cm(3), -WT / 2 - cm(2), -WT / 2 + cm(2), M(0xF1EEE9, { roughness: .5 }), true);
            [[o.s0, o.s0 + cm(4)], [o.s1 - cm(4), o.s1]].forEach(([a, b]) => boxOnEdge(e, a, b, 0, hi, -WT, cm(1), white));
            boxOnEdge(e, o.s0, o.s1, hi - cm(4), hi, -WT, cm(1), white);
            const hs = o.s1 - cm(12), k = boxOnEdge(e, hs, hs + cm(10), cm(98), cm(102), -WT / 2 + cm(2), -WT / 2 + cm(5), M(0x8A8A8E, { metalness: .8, roughness: .3 }));
          }
        }
        s = o.s1;
      });
      boxOnEdge(e, s, e.len + WT, 0, H, -WT, 0, wallMat, true);
      boxOnEdge(e, -WT, e.len + WT, H, H + 0.6, -WT, 0, capMat);
      if (e.back) boxOnEdge(e, 0, e.len, 0, cm(7), 0, cm(1.2), M(new THREE.Color(L.wall || "#F4F2EE").multiplyScalar(.93)));
      /* mirrors */
      opens.filter(p => p.edge === e.i && p.op.k === "mirror" && e.back).forEach(p => { const c = (p.x - e.a[0]) * e.dx + (p.y - e.a[1]) * e.dy;
        boxOnEdge(e, c - p.len / 2, c + p.len / 2, cm(95), cm(180), 0, cm(2), M(0xC9AE8A, { roughness: .6 }));
        boxOnEdge(e, c - p.len / 2 + cm(3), c + p.len / 2 - cm(3), cm(98), cm(177), cm(2), cm(2.4), M(0xD3DFE6, { metalness: .15, roughness: .12 })); });
    });

    /* furniture */
    S.items.forEach(it => {
      const f = A.FI(it), o = A.oi(it), grp = new THREE.Group();
      grp.position.set(o.x, 0.2, o.y); grp.rotation.y = Math.atan2(-o.bx, -o.by);
      const add = (name, w, d, h, x, matTweak) => { const src = cache[name]; if (!src) return false; const m = src.clone(true);
        const bb = new THREE.Box3().setFromObject(m), sz = bb.getSize(new THREE.Vector3()), ctr = bb.getCenter(new THREE.Vector3());
        const inner = new THREE.Group(); m.position.sub(new THREE.Vector3(ctr.x, bb.min.y, ctr.z)); inner.add(m);
        inner.scale.set(w / sz.x, h / sz.y, d / sz.z); inner.position.x = x || 0;
        m.traverse(c => { if (c.isMesh) { c.castShadow = true; c.receiveShadow = true; if (matTweak) { c.material = c.material.clone(); matTweak(c.material); } } });
        grp.add(inner); return true; };
      const h = cm(HEIGHT[it.k] || 60);
      const FABRIC = { sofa: 0xBFB8AE, armchair: 0xBFB8AE, bed: 0xC5D1D8 }[it.k];
      const neutral = FABRIC ? (mt => { const hsl = {}; mt.color.getHSL(hsl); if (hsl.s > .25) mt.color.set(FABRIC); }) : null;
      if (it.k === "countertop") {
        const k = Math.max(1, Math.round(f.w / cm(60))), cw = f.w / k;
        for (let i = 0; i < k; i++) add(k >= 2 && i === Math.floor(k / 2) ? "kitchenSink" : "kitchenCabinet", cw, f.h, h, -f.w / 2 + cw * (i + .5));
      } else if (it.k === "screen") {
        const pw = f.w / 3; [0, 1, 2].forEach(i => { const m = new THREE.Mesh(new THREE.BoxGeometry(pw - 1, cm(170), cm(2.5)), M(0xE6D8C2));
          m.position.set(-f.w / 2 + pw * (i + .5), cm(87), (i % 2 ? -1 : 1) * cm(3)); m.castShadow = m.receiveShadow = true; grp.add(m); });
      } else if (it.k === "lamp") {
        add("lampRoundFloor", f.w * 1.1, f.h * 1.1, h, 0, lightsOn ? (m => { m.emissive = new THREE.Color(0xFFD38A); m.emissiveIntensity = .9; }) : null);
        if (lightsOn) { const pl = new THREE.PointLight(0xFFD49A, 2.2, LR * 1.25, 0); pl.position.set(0, cm(150), 0); grp.add(pl);
          const bulb = new THREE.Mesh(new THREE.SphereGeometry(cm(6), 16, 12), new THREE.MeshBasicMaterial({ color: 0xFFF1C9 })); bulb.position.set(0, cm(145), 0); grp.add(bulb); }
      } else if (!add(MODEL[it.k], f.w, f.h, h, 0, neutral)) {
        const m = new THREE.Mesh(new THREE.BoxGeometry(f.w, h, f.h), M(0xC3BBB0)); m.position.y = h / 2; m.castShadow = true; grp.add(m);
      }
      scene.add(grp);
    });

    /* lights */
    const span = Math.max(...P.map(p => Math.hypot(p[0] - cx, p[1] - cz))) + WT * 2;
    const hemi = new THREE.HemisphereLight(0xFFFFFF, 0xE2DAD0, lightsOn ? .18 : 1.7); scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xFFF6EA, lightsOn ? .12 : 1.9);
    const la = az - 1.0; sun.position.set(cx + Math.sin(la) * span * 1.4, span * 2.2, cz + Math.cos(la) * span * 1.4); sun.target.position.set(cx, 0, cz);
    sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); const sc = sun.shadow.camera; sc.left = sc.bottom = -span * 1.3; sc.right = sc.top = span * 1.3; sc.near = 1; sc.far = span * 6;
    sun.shadow.bias = -0.0008; sun.shadow.normalBias = 0.6; sun.shadow.radius = 4; scene.add(sun, sun.target);
    if (lightsOn) scene.add(new THREE.AmbientLight(0x3A3355, .6));

    /* camera: isometric, fitted to the room */
    const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, -10000, 10000), el2 = Math.atan(1 / Math.SQRT2);
    cam.position.set(cx + Math.sin(az) * Math.cos(el2) * 1000, WALL_H * .3 + Math.sin(el2) * 1000, cz + Math.cos(az) * Math.cos(el2) * 1000);
    cam.lookAt(cx, WALL_H * .3, cz); cam.updateMatrixWorld();
    const inv = cam.matrixWorldInverse; let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    outer.forEach(p => [-SLAB, WALL_H].forEach(y => { const v = new THREE.Vector3(p.x, y, p.y).applyMatrix4(inv); x0 = Math.min(x0, v.x); x1 = Math.max(x1, v.x); y0 = Math.min(y0, v.y); y1 = Math.max(y1, v.y); }));
    const m = (x1 - x0) * .04; cam.left = x0 - m; cam.right = x1 + m; cam.top = y1 + m; cam.bottom = y0 - m; cam.updateProjectionMatrix();
    const height = Math.round(width * (cam.top - cam.bottom) / (cam.right - cam.left));
    const marks = S.items.map(it => { const f = A.FI(it), q = A.oi(it), v = new THREE.Vector3(q.x, cm(HEIGHT[it.k] || 60) + cm(18), q.y).project(cam);
      return { id: it.id, x: (v.x + 1) / 2, y: (1 - v.y) / 2 }; });
    return { scene, cam, height, marks };
  }

  async function render(width, dpr) {
    await loadAll;
    const { scene, cam, height, marks } = build(width); api.marks = marks;
    renderer.setPixelRatio(dpr || 1); renderer.setSize(width, height, false);
    el.style.width = "100%"; el.style.height = "auto"; el.style.aspectRatio = `${width} / ${height}`;
    renderer.render(scene, cam);
    const keep = new Set(); Object.values(cache).forEach(m => m.traverse(c => { if (c.isMesh) keep.add(c.geometry); }));
    scene.traverse(o => { if (o.isMesh && !keep.has(o.geometry)) o.geometry.dispose(); });
    return height;
  }
  const api = { el, render, ready: loadAll, marks: [] };
  return api;
}
