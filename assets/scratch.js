/* Sapiopedia: Scratch-off gift card. The gift travels in the link (#gift=…), nothing is stored on a server. */
(() => {
  'use strict';
  const S = window.SG || {};
  const root = document.querySelector('.sg');
  const $ = s => root.querySelector(s);
  const els = { recipient: $('#recipient'), gift: $('#gift'), message: $('#message'), sender: $('#sender'), canvas: $('#scratch'), caption: $('#scratchCaption'), panel: $('#sharePanel') };
  const ctx = els.canvas.getContext('2d', { willReadFrequently: true });
  let data = {}, drawn = false, painting = false, last = null, strokes = 0, sharedUrl = '';
  const defaults = S.defaults;
  const forLine = name => name ? S.forPrefix + name.toLocaleUpperCase(S.lang) : S.forAnyone;

  function encode(obj) { return btoa(Array.from(new TextEncoder().encode(JSON.stringify(obj)), x => String.fromCharCode(x)).join('')).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function decode(str) {
    const bytes = Uint8Array.from(atob(str.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
    const o = JSON.parse(new TextDecoder().decode(bytes));
    return { recipient: String(o.recipient || '').slice(0, 70), gift: String(o.gift || '').slice(0, 120), message: String(o.message || '').slice(0, 320), sender: String(o.sender || '').slice(0, 70) };
  }
  function readForm() { return { recipient: els.recipient.value.trim(), gift: els.gift.value.trim(), message: els.message.value.trim(), sender: els.sender.value.trim() }; }
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
    drawn = false; strokes = 0; els.canvas.classList.remove('gone'); els.canvas.style.pointerEvents = 'auto'; els.caption.classList.remove('hidden');
    $('#coveredMode').setAttribute('aria-pressed', 'true'); $('#revealedMode').setAttribute('aria-pressed', 'false');
  }
  function showReveal() {
    if (drawn) return; drawn = true; els.canvas.classList.add('gone'); els.canvas.style.pointerEvents = 'none'; els.caption.classList.add('hidden');
    $('#coveredMode').setAttribute('aria-pressed', 'false'); $('#revealedMode').setAttribute('aria-pressed', 'true');
  }
  function pos(e) { const r = els.canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  function rub(a, b) {
    const r = els.canvas.getBoundingClientRect();
    ctx.globalCompositeOperation = 'destination-out'; ctx.lineWidth = Math.max(24, Math.min(r.width, r.height) * .14); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); ctx.globalCompositeOperation = 'source-over'; els.caption.classList.add('hidden');
  }
  function checkProgress() {
    strokes++; if (strokes % 7 !== 0) return;
    const w = els.canvas.width, h = els.canvas.height; if (!w || !h) return;
    const px = ctx.getImageData(0, 0, w, h).data, step = Math.max(1, Math.floor(Math.sqrt(w * h / 1600)));
    let removed = 0, total = 0;
    for (let y = 0; y < h; y += step) for (let x = 0; x < w; x += step) { total++; if (px[(y * w + x) * 4 + 3] < 60) removed++; }
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
  function initRecipient(obj) { data = obj; setMode(true); show(data); window.scrollTo(0, 0); requestAnimationFrame(paintCover); }
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
  $('#reset').addEventListener('click', paintCover); $('#reveal').addEventListener('click', showReveal);
  $('#coveredMode').addEventListener('click', paintCover); $('#revealedMode').addEventListener('click', showReveal);
  const makeOwn = $('#makeOwn'); if (makeOwn) makeOwn.addEventListener('click', e => { e.preventDefault(); history.pushState(null, '', location.pathname); loadHash(); });
  let resizeTimer;
  window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { const was = drawn; paintCover(); if (was) showReveal(); }, 130); });
  window.addEventListener('hashchange', loadHash);   /* a gift link pasted into an open tab now opens the gift */
  loadHash();
})();
