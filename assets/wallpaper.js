/* Sapiopedia: 2027 phone wallpaper maker (EN/FR via window.WP). Everything is drawn in the browser; the settings live in the link after #. */
(function(){
var L = window.WP || {}, T = function(k, d){ return L[k] != null ? L[k] : d; };   /* French strings come from window.WP */
var STYLES = {
  almanac: {name:T('almanac','Almanac'), bg:'#FBF6F0', ink:'#2A1F26', acc:'#8E2F48', soft:'#8C6F78', line:'#D9C7C2', icon:'#B8405E', stars:'#C9A9B0', ghost:'#2A1F26', la:'#B9CFE0', lb:'#E9A9B8'},
  night:   {name:T('night','Night sky'), bg:'#1F2440', ink:'#F4E6EA', acc:'#E9A9B8', soft:'#B9CFE0', line:'#3A4166', icon:'#E9A9B8', stars:'#F4E6EA', ghost:'#FFFFFF', la:'#5B7A93', lb:'#A8506B'},
  riso:    {name:T('riso','Riso pink'), bg:'#F4D3DB', ink:'#2A1F26', acc:'#B8405E', soft:'#6E5A62', line:'#E3B3C0', icon:'#B8405E', stars:'#B8405E', ghost:'#2A1F26', blobs:true, la:'#B9CFE0', lb:'#F0A3B6'}
};
var ICONS = ['✦','❦','♥','✈','☾','☀','✎'];
var WORDS = T('words', ['Bloom','Courage','Calm','Joy','Roots','Wander','Brave','Gentle','Enough','Create']);
var QUOTES = T('quotes', ['Slowly, then all at once.','Courage over comfort.','Small steps, every day.','Begin where you are.','Make it simple, make it soft.']);
var YEARS = T('years', {riso:'Riso print', italic:'Soft italic', light:'Fine & airy', stacked:'Stacked', vintage:'Old book', moon:'Moon', halftone:'Halftone', arc:'Arc', shadow:'Long shadow', outline:'Outline'});
var style = 'almanac', yearStyle = 'riso';
var $ = function(id){ return document.getElementById(id); };
var cv = $('cv'), ctx = cv.getContext('2d'), MAIN = cv;

function chips(){
  var box = $('styles'); box.innerHTML = '';
  Object.keys(STYLES).forEach(function(k){
    var b = document.createElement('button');
    b.className = 'chip' + (k === style ? ' on' : '');
    b.textContent = STYLES[k].name;
    b.onclick = function(){ style = k; chips(); yearChips(); draw(); save(); };
    box.appendChild(b);
  });
}
function yearChips(){
  var box = $('years'); box.innerHTML = '';
  var keep = yearStyle, mainCv = cv, mainCtx = ctx, sz = size();
  Object.keys(YEARS).forEach(function(k){
    // render a small preview of this year style with the current colours
    var oc = document.createElement('canvas'); cv = oc; ctx = oc.getContext('2d'); yearStyle = k;
    render(sz.w, sz.h);
    var t = document.createElement('canvas'); t.width = 240; t.height = 130;
    var top = Math.round(sz.h * .31 - 190 * sz.w/1179), hh = Math.round(520 * sz.w/1179);
    t.getContext('2d').drawImage(oc, 0, top, sz.w, hh, 0, 0, 240, 130 * (240/240));
    var b = document.createElement('button');
    b.className = 'ychip' + (k === keep ? ' on' : '');
    b.setAttribute('aria-label', YEARS[k]);
    b.appendChild(t);
    var l = document.createElement('span'); l.textContent = YEARS[k]; b.appendChild(l);
    b.onclick = function(){ yearStyle = k; yearChips(); draw(); save(); };
    box.appendChild(b);
  });
  cv = mainCv; ctx = mainCtx; yearStyle = keep;
}
function ideas(id, list, target){
  var el = $(id); el.innerHTML = '';
  list.forEach(function(w, i){
    var a = document.createElement('a'); a.href = '#'; a.textContent = w;
    a.style.color = 'var(--accent)'; a.style.marginRight = '8px';
    a.onclick = function(e){ e.preventDefault(); $(target).value = w; draw(); save(); };
    el.appendChild(a);
  });
}

function size(){ var p = $('size').value.split('x'); return {w:+p[0], h:+p[1]}; }

function wrap(text, maxW){
  var words = text.split(' '), lines = [], line = '';
  for (var i = 0; i < words.length; i++){
    var t = line ? line + ' ' + words[i] : words[i];
    if (ctx.measureText(t).width > maxW && line){ lines.push(line); line = words[i]; } else { line = t; }
  }
  if (line) lines.push(line);
  return lines;
}
function spaced(text, x, y, spacing){
  // centred text with letter spacing
  var w = 0, i;
  for (i = 0; i < text.length; i++) w += ctx.measureText(text[i]).width + (i < text.length - 1 ? spacing : 0);
  var cx = x - w / 2;
  ctx.textAlign = 'left';
  for (i = 0; i < text.length; i++){ ctx.fillText(text[i], cx, y); cx += ctx.measureText(text[i]).width + spacing; }
  ctx.textAlign = 'center';
}
function star(x, y, r){
  ctx.beginPath();
  ctx.moveTo(x, y - r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.quadraticCurveTo(x, y, x, y + r);
  ctx.quadraticCurveTo(x, y, x - r, y);
  ctx.quadraticCurveTo(x, y, x, y - r);
  ctx.fill();
}

function render(W, H){
  var s = STYLES[style], u = W / 1179; // unit scaled from the standard iPhone width
  cv.width = W; cv.height = H;
  ctx.fillStyle = s.bg; ctx.fillRect(0, 0, W, H);

  if (s.blobs){
    ctx.save(); ctx.globalCompositeOperation = 'multiply';
    ctx.fillStyle = 'rgba(185,207,224,.55)'; ctx.beginPath(); ctx.arc(W*.12, H*.62, W*.34, 0, Math.PI*2); ctx.fill();
    ctx.restore();
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.arc(W*.92, H*.9, W*.3, 0, Math.PI*2); ctx.fill();
  }
  // scattered four-point stars
  ctx.fillStyle = s.stars;
  for (var i = 0; i < 34; i++){
    ctx.globalAlpha = i % 3 ? .3 : .75;
    star(((i*37+11) % 100) / 100 * W, ((i*53+7) % 195) / 195 * H, (i % 3 ? 9 : 14) * u);
  }
  ctx.globalAlpha = 1;

  // double frame
  ctx.strokeStyle = s.line;
  ctx.lineWidth = 4*u; ctx.strokeRect(46*u, 46*u, W - 92*u, H - 92*u);
  ctx.lineWidth = 2*u; ctx.strokeRect(62*u, 62*u, W - 124*u, H - 124*u);

  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  var cx = W/2, padX = 150*u, colW = W - padX*2;
  var y = H*0.31 + 250*u; // the top 31 % stays clear for the clock

  y = drawYear(s, cx, y, u, W, H);

  var word = $('word').value.trim(), goals = $('goals').value.split('\n').map(function(g){return g.trim();}).filter(Boolean).slice(0,7), quote = $('quote').value.trim();

  if ($('onWord').checked && word){
    y += 110*u;
    ctx.fillStyle = s.soft; ctx.font = '600 ' + (34*u) + "px 'Source Sans 3', sans-serif";
    spaced(T('kWord','MY WORD FOR THE YEAR'), cx, y, 9*u);
    y += 150*u;
    ctx.fillStyle = s.ink; ctx.font = 'italic 400 ' + (150*u) + "px 'Fraunces', serif";
    ctx.fillText(word, cx, y);
  }

  if ($('onGoals').checked && goals.length){
    y += 130*u;
    ctx.fillStyle = s.soft; ctx.font = '600 ' + (34*u) + "px 'Source Sans 3', sans-serif";
    spaced(T('kGoals','GOALS AND DREAMS'), cx, y, 9*u);
    y += 30*u;
    var fs = (goals.length > 5 ? 54 : 60) * u, rowH = fs * 1.85;
    goals.forEach(function(g, i){
      var top = y, mid = top + rowH/2;
      ctx.textAlign = 'center'; ctx.fillStyle = s.icon; ctx.font = (fs*.9) + "px 'Fraunces', serif";
      ctx.fillText(ICONS[i % ICONS.length], padX + 30*u, mid + fs*.32);
      ctx.textAlign = 'left'; ctx.fillStyle = s.ink; ctx.font = '400 ' + fs + "px 'Fraunces', serif";
      var t = g; while (ctx.measureText(t).width > colW - 90*u && t.length > 3) t = t.slice(0, -2) + '…';
      ctx.fillText(t, padX + 90*u, mid + fs*.33);
      // dotted rule
      ctx.fillStyle = s.line;
      for (var x = padX; x < W - padX; x += 14*u) ctx.fillRect(x, top + rowH, 5*u, 3*u);
      y += rowH;
    });
    ctx.textAlign = 'center';
  }

  if ($('onQuote').checked && quote){
    ctx.font = 'italic 400 ' + (70*u) + "px 'Fraunces', serif";
    var lines = wrap(T('ql', '“') + quote + T('qr', '”'), colW);
    var qy = H - 200*u - (lines.length - 1) * 86*u;
    ctx.fillStyle = s.line; ctx.fillRect(cx - colW*.25, qy - 210*u, colW*.5, 3*u);
    ctx.fillStyle = s.soft; ctx.font = '600 ' + (32*u) + "px 'Source Sans 3', sans-serif";
    spaced(T('kQuote','QUOTE OF THE YEAR'), cx, qy - 130*u, 9*u);
    ctx.fillStyle = s.acc; ctx.font = 'italic 400 ' + (70*u) + "px 'Fraunces', serif";
    lines.forEach(function(l, i){ ctx.fillText(l, cx, qy + i*86*u); });
  }

}

function drawYear(s, cx, y, u, W, H){
  var dark = style === 'night';
  if (yearStyle === 'riso'){
    ctx.font = '600 ' + (310*u) + "px 'Fraunces', serif";
    ctx.save(); ctx.globalCompositeOperation = dark ? 'screen' : 'multiply';
    ctx.fillStyle = s.la; ctx.fillText('2027', cx - 12*u, y + 10*u);
    ctx.fillStyle = s.lb; ctx.fillText('2027', cx + 12*u, y - 8*u);
    ctx.restore();
    ctx.strokeStyle = s.acc; ctx.lineWidth = 3.5*u; ctx.lineJoin = 'round';
    ctx.strokeText('2027', cx, y);
    ctx.fillStyle = s.acc; star(cx + 330*u, y - 250*u, 28*u); star(cx - 340*u, y - 40*u, 16*u);
    return y;
  }
  if (yearStyle === 'italic'){
    ctx.fillStyle = s.acc; ctx.font = 'italic 300 ' + (340*u) + "px 'Fraunces', serif";
    ctx.fillText('2027', cx, y);
    ctx.fillStyle = s.lb; star(cx + 360*u, y - 230*u, 24*u);
    return y;
  }
  if (yearStyle === 'light'){
    ctx.fillStyle = s.acc; ctx.font = '300 ' + (250*u) + "px 'Fraunces', serif";
    spaced('2027', cx, y, 40*u);
    ctx.fillStyle = s.line;
    ctx.fillRect(cx - 420*u, y + 50*u, 340*u, 3*u); ctx.fillRect(cx + 80*u, y + 50*u, 340*u, 3*u);
    ctx.fillStyle = s.acc; star(cx, y + 52*u, 18*u);
    return y + 40*u;
  }
  if (yearStyle === 'stacked'){
    ctx.fillStyle = s.acc; ctx.font = '300 ' + (250*u) + "px 'Fraunces', serif";
    ctx.fillText('20', cx - 70*u, y - 160*u);
    ctx.font = 'italic 600 ' + (250*u) + "px 'Fraunces', serif";
    ctx.fillText('27', cx + 70*u, y + 40*u);
    ctx.fillStyle = s.lb; star(cx + 250*u, y - 330*u, 22*u);
    return y + 40*u;
  }
  if (yearStyle === 'moon'){
    var fs = 300*u; ctx.font = '300 ' + fs + "px 'Fraunces', serif";
    var w2 = ctx.measureText('2').width, w27 = ctx.measureText('27').width, d = fs*.62, gap = 18*u;
    var tot = w2 + gap + d + gap + w27, x0 = cx - tot/2;
    ctx.textAlign = 'left'; ctx.fillStyle = s.acc;
    ctx.fillText('2', x0, y); ctx.fillText('27', x0 + w2 + gap + d + gap, y);
    ctx.textAlign = 'center';
    var mx = x0 + w2 + gap + d/2, my = y - fs*.36;
    ctx.fillStyle = s.lb; ctx.beginPath(); ctx.arc(mx, my, d/2, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = s.bg; ctx.beginPath(); ctx.arc(mx + d*.28, my - d*.12, d*.42, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = s.acc; star(mx + d*.2, my + d*.05, 14*u); star(mx + d*.42, my - d*.32, 9*u);
    return y;
  }
  if (yearStyle === 'halftone'){
    var oc = document.createElement('canvas'); oc.width = W; oc.height = Math.round(420*u);
    var o = oc.getContext('2d'); o.font = '600 ' + (330*u) + "px 'Fraunces', serif"; o.textAlign = 'center'; o.fillStyle = '#000';
    o.fillText('2027', W/2, 340*u);
    var data = o.getImageData(0, 0, oc.width, oc.height).data, step = Math.max(6, Math.round(13*u)), top = y - 340*u;
    for (var yy = 0; yy < oc.height; yy += step){
      for (var xx = 0; xx < oc.width; xx += step){
        if (data[(yy*oc.width + xx)*4 + 3] > 120){
          var t = yy / oc.height;
          ctx.fillStyle = t < .5 ? s.acc : s.lb;
          ctx.beginPath(); ctx.arc(xx, top + yy, step*(.22 + .2*(1 - Math.abs(t - .5)*2)), 0, Math.PI*2); ctx.fill();
        }
      }
    }
    return y;
  }
  if (yearStyle === 'arc'){
    var R = 760*u, ccy = y + 640*u, chars = ['\u2726','2','0','2','7','\u2726'], span = .78;
    chars.forEach(function(c, i){
      var a = -Math.PI/2 - span/2 + span * i/(chars.length - 1);
      ctx.save(); ctx.translate(cx + R*Math.cos(a), ccy + R*Math.sin(a)); ctx.rotate(a + Math.PI/2);
      ctx.fillStyle = (i === 0 || i === 5) ? s.lb : s.acc;
      ctx.font = (i === 0 || i === 5) ? (90*u) + "px 'Fraunces', serif" : 'italic 400 ' + (230*u) + "px 'Fraunces', serif";
      ctx.fillText(c, 0, 0); ctx.restore();
    });
    return y + 20*u;
  }
  if (yearStyle === 'shadow'){
    ctx.font = '600 ' + (300*u) + "px 'Fraunces', serif";
    ctx.fillStyle = s.lb;
    for (var k = 18; k > 0; k--) ctx.fillText('2027', cx + k*1.6*u, y + k*1.6*u);
    ctx.fillStyle = s.acc; ctx.fillText('2027', cx, y);
    return y + 20*u;
  }
  if (yearStyle === 'outline'){
    ctx.font = '600 ' + (310*u) + "px 'Fraunces', serif"; ctx.lineJoin = 'round';
    ctx.strokeStyle = s.la; ctx.lineWidth = 3*u; ctx.strokeText('2027', cx + 10*u, y + 10*u);
    ctx.strokeStyle = s.acc; ctx.lineWidth = 4*u; ctx.strokeText('2027', cx, y);
    ctx.fillStyle = s.acc; star(cx - 300*u, y - 260*u, 20*u); star(cx + 320*u, y - 40*u, 14*u);
    return y;
  }
  ctx.fillStyle = s.acc; ctx.font = (300*u) + "px 'IM Fell English SC', serif";
  ctx.fillText('2027', cx, y);
  return y;
}

function draw(){
  var sz = size();
  $('phone').style.setProperty('--ratio', sz.w + '/' + sz.h);
  render(sz.w, sz.h);
  var g = $('ghost'); g.style.display = $('showGhost').checked ? 'block' : 'none';
  g.style.color = STYLES[style].ghost; g.style.opacity = .28;
}

function blob(){ return new Promise(function(res){ cv.toBlob(res, 'image/png'); }); }
function filename(){ return T('file','my-2027-wallpaper.png'); }

$('dl').onclick = function(){
  draw();
  var a = document.createElement('a'); a.download = filename(); a.href = cv.toDataURL('image/png'); a.click();
  msg(T('saved','Saved. Set it as your lock screen from your photos.'));
};
$('share').onclick = function(){
  draw();
  blob().then(function(b){
    var f = new File([b], filename(), {type:'image/png'});
    if (navigator.canShare && navigator.canShare({files:[f]})){
      navigator.share({files:[f], title:T('shareTitle','My 2027'), text:T('shareText','Made with sapiopedia.com')}).catch(function(){});
    } else { $('dl').click(); }
  });
};
$('link').onclick = function(){
  save();
  var url = location.href;
  if (navigator.clipboard) navigator.clipboard.writeText(url).then(function(){ msg(T('copied','Link copied: open it later to edit your wallpaper.')); });
  else msg(url);
};
function msg(t){ $('msg').textContent = t; setTimeout(function(){ $('msg').textContent = ''; }, 4000); }

// state kept in the link (after #), so nothing is sent to a server
function save(){
  var st = {s:style, y:yearStyle, z:$('size').value, w:$('word').value, g:$('goals').value, q:$('quote').value,
            ow:$('onWord').checked?1:0, og:$('onGoals').checked?1:0, oq:$('onQuote').checked?1:0};
  history.replaceState(null, '', '#' + btoa(unescape(encodeURIComponent(JSON.stringify(st)))));
}
function load(){
  try {
    var st = JSON.parse(decodeURIComponent(escape(atob(location.hash.slice(1)))));
    if (STYLES[st.s]) style = st.s;
    if (YEARS[st.y]) yearStyle = st.y;
    if (st.z) $('size').value = st.z;
    $('word').value = st.w || ''; $('goals').value = st.g || ''; $('quote').value = st.q || '';
    $('onWord').checked = !!st.ow; $('onGoals').checked = !!st.og; $('onQuote').checked = !!st.oq;
  } catch (e) {}
}

if (/android/i.test(navigator.userAgent)) $('size').value = '1080x2400';
if (location.hash.length > 1) load();
chips(); yearChips(); ideas('wordIdeas', WORDS, 'word'); ideas('quoteIdeas', QUOTES, 'quote');
['word','goals','quote'].forEach(function(id){ $(id).addEventListener('input', function(){ draw(); save(); }); });
['onWord','onGoals','onQuote','size','showGhost'].forEach(function(id){ $(id).addEventListener('change', function(){ draw(); save(); }); });
$('size').addEventListener('change', yearChips);

draw();
// redraw once the fonts are ready so the canvas uses them
Promise.all([
  document.fonts.load("300px 'IM Fell English SC'"),
  document.fonts.load("italic 150px 'Fraunces'"),
  document.fonts.load("60px 'Fraunces'"),
  document.fonts.load("300 250px 'Fraunces'"),
  document.fonts.load("600 310px 'Fraunces'"),
  document.fonts.load("italic 300 340px 'Fraunces'"),
  document.fonts.load("italic 600 250px 'Fraunces'"),
  document.fonts.load("italic 400 210px 'Fraunces'"),
  document.fonts.load("600 330px 'Fraunces'"),
  document.fonts.load("600 34px 'Source Sans 3'")
]).then(function(){ yearChips(); draw(); }, draw);
})();
