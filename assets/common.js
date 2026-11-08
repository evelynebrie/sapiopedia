// Sapiopedia — shared helpers
window.SP = {
  // Format a number for the current page language
  fmt: function (n, digits) {
    var lang = document.documentElement.lang || 'en';
    return new Intl.NumberFormat(lang, { maximumFractionDigits: digits == null ? 2 : digits }).format(n);
  },
  // Share the current page (Web Share API with clipboard fallback)
  share: function (title, text) {
    var url = location.href;
    if (navigator.share) { navigator.share({ title: title, text: text, url: url }).catch(function () {}); return; }
    try { navigator.clipboard.writeText(url); alert('Link copied'); } catch (e) { prompt('Copy this link', url); }
  },
  // Birthday maths (shared by the home mini-tool and the converter page)
  birth: function (iso, lang) {
    if (!iso) return null;
    var d = new Date(iso + 'T12:00:00'), t = new Date(); t.setHours(12, 0, 0, 0);
    if (isNaN(d) || d > t) return null;
    var days = Math.floor((t - d) / 864e5);
    var months = (t.getFullYear() - d.getFullYear()) * 12 + (t.getMonth() - d.getMonth()) - (t.getDate() < d.getDate() ? 1 : 0);
    return { dow: d.toLocaleDateString(lang || 'en', { weekday: 'long' }), days: days, weeks: Math.floor(days / 7), months: months,
             moons: Math.floor(days / 29.530589), beats: Math.round(days * 1440 * 72 / 1e6), km: Math.round(days * 86400 * 29.8 / 1e6) };
  },
  // Draw a shareable result card (PNG) in the site's rose palette, with the "?" mark
  resultCard: function (opts) {
    var c = document.createElement('canvas'); c.width = 1080; c.height = 1080;
    var g = c.getContext('2d');
    g.fillStyle = '#F7E9EC'; g.fillRect(0, 0, 1080, 1080);
    g.fillStyle = '#F1DCE1'; g.fillRect(90, 90, 900, 900);
    SP._mark(g, 150, 140, 1.75);
    var ink = '#2A1F26', acc = opts.color || '#B8405E';
    g.textAlign = 'left'; g.fillStyle = '#6E5A62';
    g.font = '600 26px "Source Sans 3", system-ui, sans-serif';
    g.fillText((opts.kicker || '').toUpperCase().split('').join(String.fromCharCode(8202)), 170, 560);
    g.fillStyle = acc; g.font = '400 110px Fraunces, Georgia, serif';
    SP._wrap(g, opts.title || '', 170, 680, 760, 112);
    g.fillStyle = ink; g.font = '300 34px Fraunces, Georgia, serif';
    SP._wrap(g, opts.subtitle || '', 170, 830, 760, 44);
    g.fillStyle = '#6E5A62'; g.font = '600 22px "Source Sans 3", system-ui, sans-serif';
    g.fillText('S A P I O P E D I A . C O M', 170, 950);
    return c.toDataURL('image/png');
  },
  // Logo mark: "?" in two offset inks + raspberry line, sparkles, ringed-planet dot (logo.svg coordinates)
  _mark: function (g, x, y, s) {
    var Q = new Path2D('M62 70 C58 36 96 20 124 28 C160 38 164 86 132 104 C114 114 104 122 104 144');
    g.save(); g.translate(x - 30 * s, y - 10 * s); g.scale(s, s); g.lineCap = 'round'; g.lineJoin = 'round';
    function st(col, w, dx, dy) { g.save(); g.translate(dx, dy); g.strokeStyle = col; g.lineWidth = w; g.stroke(Q); g.restore(); }
    st('#B9CFE0', 24, -6, 5); st('#E9A9B8', 24, 6, -4); st('#B8405E', 7, 0, 0);
    function ring(d) { g.save(); g.translate(104, 176); g.rotate(-18 * Math.PI / 180); g.translate(-104, -176); g.strokeStyle = '#B9CFE0'; g.lineWidth = 4; g.stroke(new Path2D(d)); g.restore(); }
    ring('M77.6 176 A26.4 7.2 0 0 1 130.4 176');
    g.fillStyle = '#B8405E'; g.beginPath(); g.arc(104, 176, 12, 0, Math.PI * 2); g.fill();
    ring('M77.6 176 A26.4 7.2 0 0 0 130.4 176');
    ['M108 53 Q108 62 117 62 Q108 62 108 71 Q108 62 99 62 Q108 62 108 53Z',
     'M128 44.5 Q128 48 131.5 48 Q128 48 128 51.5 Q128 48 124.5 48 Q128 48 128 44.5Z',
     'M90 77 Q90 80 93 80 Q90 80 90 83 Q90 80 87 80 Q90 80 90 77Z'].forEach(function (d) { g.fill(new Path2D(d)); });
    g.restore();
  },
  _wrap: function (g, text, x, y, maxW, lh) {
    var words = text.split(' '), line = '', lines = [];
    for (var i = 0; i < words.length; i++) {
      var t = line + words[i] + ' ';
      if (g.measureText(t).width > maxW && line) { lines.push(line); line = words[i] + ' '; } else { line = t; }
    }
    lines.push(line);
    for (var j = 0; j < lines.length && j < 4; j++) g.fillText(lines[j].trim(), x, y + j * lh);
  },
  download: function (dataUrl, name) {
    var a = document.createElement('a'); a.href = dataUrl; a.download = name || 'result.png'; a.click();
  }
};
