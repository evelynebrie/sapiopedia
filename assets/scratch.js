/* Sapiopedia: Scratch-off gift card. The gift travels in the link (#gift=…), nothing is stored on a server. */
(() => {
  'use strict';
  const S = window.SG || {};
  const root = document.querySelector('.sg');
  const $ = s => root.querySelector(s);
  const els = { recipient: $('#recipient'), gift: $('#gift'), message: $('#message'), sender: $('#sender'), canvas: $('#scratch'), caption: $('#scratchCaption'), panel: $('#sharePanel') };
  const ctx = els.canvas.getContext('2d', { willReadFrequently: true });
  let data = {}, celebrated = false, drawn = false, painting = false, last = null, strokes = 0, sharedUrl = '';
  const defaults = S.defaults;
  const forLine = name => name ? S.forPrefix + name.toLocaleUpperCase(S.lang) : S.forAnyone;

  function encode(obj) { return btoa(Array.from(new TextEncoder().encode(JSON.stringify(obj)), x => String.fromCharCode(x)).join('')).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function decode(str) {
    const bytes = Uint8Array.from(atob(str.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
    const o = JSON.parse(new TextDecoder().decode(bytes));
    return { recipient: String(o.recipient || '').slice(0, 70), gift: String(o.gift || '').slice(0, 120), message: String(o.message || '').slice(0, 320), sender: String(o.sender || '').slice(0, 70), fx: FX.includes(o.fx) ? o.fx : 'none' };
  }
  const FX = ['none', 'confetti', 'hearts', 'snow', 'pink', 'blue'];   /* pink and blue: one-colour confetti for gender reveals */
  const fxButtons = Array.from(root.querySelectorAll('[data-fx]'));
  let fxChoice = S.fx || 'confetti';
  function readForm() { return { recipient: els.recipient.value.trim(), gift: els.gift.value.trim(), message: els.message.value.trim(), sender: els.sender.value.trim(), fx: fxChoice }; }
  function show(d) {
    $('#displayTo').textContent = forLine(d.recipient);
    $('#displayGift').textContent = d.gift || S.giftFallback;
    $('#displayMessage').textContent = d.message || '';
    $('#displayFrom').textContent = d.sender || '';
  }
  function updateContent() { data = readForm(); show(data); if (!root.classList.contains('recipient-mode')) els.panel.hidden = true; }

  function paintCover() {
    const box = els.canvas.getBoundingClientRect(); if (!box.width || !box.height) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    els.canvas.width = Math.round(box.width * dpr); els.canvas.height = Math.round(box.height * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = box.width, h = box.height, grad = ctx.createLinearGradient(0, 0, w, h);
    grad.addColorStop(0, '#c9c7c4'); grad.addColorStop(.55, '#b9b7b5'); grad.addColorStop(1, '#c6c2bf');
    ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = grad; ctx.fillRect(0, 0, w, h);
    let seed = 41288;
    for (let i = 0; i < Math.round(w * h / 43); i++) { seed = (1664525 * seed + 1013904223) >>> 0; const x = seed / 4294967296 * w; seed = (1664525 * seed + 1013904223) >>> 0; const y = seed / 4294967296 * h; ctx.fillStyle = i % 2 ? 'rgba(255,255,255,.13)' : 'rgba(69,64,64,.065)'; ctx.fillRect(x, y, 1, 1); }
    drawn = false; celebrated = false; strokes = 0; els.canvas.classList.remove('gone'); els.canvas.style.pointerEvents = 'auto'; els.caption.classList.remove('hidden');
    $('#coveredMode').setAttribute('aria-pressed', 'true'); $('#revealedMode').setAttribute('aria-pressed', 'false');
  }
  function showReveal(silent) {
    if (drawn) return; drawn = true; if (silent !== true && !celebrated) { celebrated = true; celebrate(data.fx); } els.canvas.classList.add('gone'); els.canvas.style.pointerEvents = 'none'; els.caption.classList.add('hidden');
    $('#coveredMode').setAttribute('aria-pressed', 'false'); $('#revealedMode').setAttribute('aria-pressed', 'true');
  }
  function pos(e) { const r = els.canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  function rub(a, b) {
    const r = els.canvas.getBoundingClientRect();
    ctx.globalCompositeOperation = 'destination-out'; ctx.lineWidth = Math.max(24, Math.min(r.width, r.height) * .14); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); ctx.globalCompositeOperation = 'source-over'; els.caption.classList.add('hidden');
  }
  function checkProgress() {
    strokes++; if (strokes % 4 !== 0) return;
    const w = els.canvas.width, h = els.canvas.height; if (!w || !h) return;
    const px = ctx.getImageData(0, 0, w, h).data, step = Math.max(1, Math.floor(Math.sqrt(w * h / 1600)));
    let removed = 0, total = 0;
    for (let y = 0; y < h; y += step) for (let x = 0; x < w; x += step) { total++; if (px[(y * w + x) * 4 + 3] < 60) removed++; }
    if (removed / total > .22 && !celebrated) { celebrated = true; celebrate(data.fx); }   /* the effect starts while still scratching */
    if (removed / total > .36) showReveal();
  }
  els.canvas.addEventListener('pointerdown', e => { e.preventDefault(); painting = true; els.canvas.setPointerCapture(e.pointerId); last = pos(e); rub(last, last); });
  els.canvas.addEventListener('pointermove', e => { if (!painting || drawn) return; e.preventDefault(); const p = pos(e); rub(last, p); last = p; checkProgress(); });
  const stop = () => { painting = false; last = null; };
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(t => els.canvas.addEventListener(t, stop));

  function setMode(recipient) {
    root.classList.toggle('recipient-mode', recipient); document.body.classList.toggle('sg-recipient', recipient);
    $('#belowCard').textContent = recipient ? S.belowRecipient : S.belowCreator;
  }
  function initRecipient(obj) { data = obj; setMode(true); fxButtons.forEach(x => x.setAttribute('aria-checked', x.dataset.fx === (obj.fx || 'none'))); show(data); window.scrollTo(0, 0); requestAnimationFrame(paintCover); }
  function initCreator() {
    setMode(false);
    if (!els.recipient.dataset.filled) { Object.entries(defaults).forEach(([k, v]) => { els[k].value = v; }); els.recipient.dataset.filled = '1'; }
    updateContent(); requestAnimationFrame(paintCover);
  }
  function loadHash() {
    const m = location.hash.match(/^#gift=(.+)$/);
    if (m) { try { initRecipient(decode(m[1])); return; } catch (e) { history.replaceState(null, '', location.pathname + location.search); } }
    initCreator();
  }
  [els.recipient, els.gift, els.message, els.sender].forEach(el => el.addEventListener('input', updateContent));
  $('#createLink').addEventListener('click', () => { updateContent(); sharedUrl = location.href.split('#')[0] + '#gift=' + encode(data); $('#shareUrl').value = sharedUrl; els.panel.hidden = false; });
  $('#copy').addEventListener('click', async () => {
    if (!sharedUrl) return;
    try { await navigator.clipboard.writeText(sharedUrl); } catch (e) { $('#shareUrl').focus(); $('#shareUrl').select(); try { document.execCommand('copy'); } catch (_) {} }
    $('#copy').textContent = S.copied; setTimeout(() => { $('#copy').textContent = S.copy; }, 1700);
  });
  $('#share').addEventListener('click', async () => {
    if (!sharedUrl) return;
    if (navigator.share) { try { await navigator.share({ title: S.shareTitle, text: S.shareText, url: sharedUrl }); } catch (e) {} } else { $('#copy').click(); }
  });
  $('#openGift').addEventListener('click', () => { if (sharedUrl) window.open(sharedUrl, '_blank', 'noopener,noreferrer'); });
  $('#reset').addEventListener('click', paintCover); $('#reveal').addEventListener('click', () => showReveal());
  $('#coveredMode').addEventListener('click', paintCover); $('#revealedMode').addEventListener('click', () => showReveal(true));
  const makeOwn = $('#makeOwn'); if (makeOwn) makeOwn.addEventListener('click', e => { e.preventDefault(); history.pushState(null, '', location.pathname); loadHash(); });
  let resizeTimer;
  window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { const was = drawn; paintCover(); if (was) showReveal(true); }, 130); });
  fxButtons.forEach(b => b.addEventListener('click', () => {
    fxChoice = b.dataset.fx; fxButtons.forEach(x => x.setAttribute('aria-checked', x === b)); updateContent(); celebrate(fxChoice, true);
  }));
  root.querySelector('.fx-choice').addEventListener('keydown', e => {
    const i = fxButtons.findIndex(b => b.dataset.fx === fxChoice), d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
    if (!d) return; e.preventDefault(); const nb = fxButtons[(i + d + fxButtons.length) % fxButtons.length]; nb.focus(); nb.click();
  });

  /* ---------- reveal effects: confetti, hearts or falling snow, drawn on a full-screen canvas ---------- */
  let fxCanvas = null, fxRun = 0;
  function celebrate(kind, preview) {
    if (!kind || kind === 'none') return;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!fxCanvas) { fxCanvas = document.createElement('canvas'); fxCanvas.className = 'sg-fx'; fxCanvas.setAttribute('aria-hidden', 'true'); document.body.appendChild(fxCanvas); }
    const run = ++fxRun, g = fxCanvas.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = innerWidth, H = innerHeight; fxCanvas.width = W * dpr; fxCanvas.height = H * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); fxCanvas.style.opacity = '1';
    const dur = reduced ? 1500 : preview ? 3000 : 6500, n = Math.round((reduced ? 0.25 : preview ? 0.6 : 1) * (kind === 'snow' ? 320 : kind === 'hearts' ? 60 : 240));
    const COL = kind === 'pink' ? ['#E58AA6', '#F4B6C8', '#D8648A', '#FAD3DF', '#C94C76', '#F7C4D3'] : kind === 'blue' ? ['#7FB1DE', '#B9D6EF', '#4F8FCB', '#D6E8F7', '#3C78B4', '#A3C9EA'] : ['#973C55', '#E9A9B8', '#D4AE52', '#B9CFE0', '#6E8F63', '#F3D9DF'], R = Math.random, P = [];
    if (kind === 'pink' || kind === 'blue') kind = 'confetti';
    for (let i = 0; i < n; i++) {
      if (kind === 'confetti') {
        if (i % 2) P.push({ x: W / 2 + (R() - .5) * W * .5, y: H * .38 + (R() - .5) * 80, vx: (R() - .5) * 22, vy: -R() * 16 - 4, w: 6 + R() * 6, h: 9 + R() * 8, r: R() * 6, vr: (R() - .5) * .35, c: COL[i % COL.length] });   /* burst from the card */
        else P.push({ x: R() * W, y: R() * H * 1.05 - H * .25, vx: (R() - .5) * 2, vy: 1.5 + R() * 2.5, w: 6 + R() * 6, h: 9 + R() * 8, r: R() * 6, vr: (R() - .5) * .3, c: COL[i % COL.length], rain: true });   /* rain across the screen */
      }
      else if (kind === 'hearts') P.push({ x: R() * W, y: H * .45 + R() * H * .75, vy: -(2 + R() * 2.6), s: 10 + R() * 16, ph: R() * 6, c: COL[i % 2 ? 0 : 1], a: .7 + R() * .3 });
      else P.push({ x: R() * W, y: R() * H * .5 - H * .15, vy: 1.4 + R() * 2, s: 1.5 + R() * 3.5, ph: R() * 6, a: .6 + R() * .4 });
    }
    const heart = (x, y, s) => { g.beginPath(); g.moveTo(x, y + s * .3); g.bezierCurveTo(x, y, x - s * .5, y, x - s * .5, y + s * .3); g.bezierCurveTo(x - s * .5, y + s * .6, x, y + s * .8, x, y + s); g.bezierCurveTo(x, y + s * .8, x + s * .5, y + s * .6, x + s * .5, y + s * .3); g.bezierCurveTo(x + s * .5, y, x, y, x, y + s * .3); g.fill(); };
    const t0 = performance.now();
    (function frame(now) {
      if (run !== fxRun) return;
      const t = now - t0, fade = Math.min(1, Math.max(0, (dur - t) / 1100));
      g.clearRect(0, 0, W, H); g.globalAlpha = fade;
      P.forEach(p => {
        if (kind === 'confetti') { p.vy += p.rain ? .05 : .32; p.vx *= .99; if (p.rain) p.x += Math.sin(t / 400 + p.r) * .6; p.x += p.vx; p.y += p.vy; p.r += p.vr;
          g.save(); g.translate(p.x, p.y); g.rotate(p.r); g.fillStyle = p.c; g.fillRect(-p.w / 2, -p.h / 2 * Math.abs(Math.cos(p.r * 2)), p.w, p.h * Math.abs(Math.cos(p.r * 2)) + 1); g.restore(); }
        else if (kind === 'hearts') { p.y += p.vy; p.x += Math.sin(t / 600 + p.ph) * .8; g.globalAlpha = fade * p.a; g.fillStyle = p.c; heart(p.x, p.y, p.s); }
        else { p.y += p.vy; p.x += Math.sin(t / 900 + p.ph) * .6; g.globalAlpha = fade * p.a; g.beginPath(); g.arc(p.x, p.y, p.s, 0, Math.PI * 2); g.fillStyle = '#FFFFFF'; g.fill(); g.lineWidth = 1; g.strokeStyle = 'rgba(110,130,160,.35)'; g.stroke(); }
      });
      g.globalAlpha = 1;
      if (t < dur) requestAnimationFrame(frame); else { g.clearRect(0, 0, W, H); fxCanvas.style.opacity = '0'; }
    })(t0);
  }
  window.addEventListener('hashchange', loadHash);   /* a gift link pasted into an open tab now opens the gift */
  loadHash();
})();
