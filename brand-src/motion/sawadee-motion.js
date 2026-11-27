/* SaWadee Burn motion kit. Needs assets.js first.
 * Web:   <div data-sawadee="wai" style="height:60vh"></div>   (plays when scrolled into view; click to replay)
 *        options: data-bg="#F2E4D2" | data-bg="none", data-color="#16302F"
 * JS:    const m = SawadeeMotion.mount(el, 'firelight', {bg:'none'}); m.play(); m.seek(1.2);
 * Video: render.py calls mount(...,{width,height}) and seek(t) per frame.
 * Rule baked in: fire and embers never touch the W (the wai). Only the word BURN glows. */
(function () {
  const A = window.SAWADEE_ASSETS;
  const C = { cream: '#F2E4D2', ink: '#16302F', sea: '#072F35', gold: '#F5C65A', tang: '#E4602A' };
  const NS = 'http://www.w3.org/2000/svg';
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const E = {
    out: t => 1 - Math.pow(1 - clamp(t), 3),
    in: t => Math.pow(clamp(t), 3),
    inOut: t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; },
    outBack: t => { t = clamp(t); const c = 1.4; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); },
  };
  const TAU = Math.PI * 2;
  function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; }; }
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  function mix(a, b, t) { const x = hex(a), y = hex(b); return 'rgb(' + x.map((v, i) => Math.round(lerp(v, y[i], clamp(t)))).join(',') + ')'; }
  function ramp(stops, p) { // stops: [[p, colour], ...]
    if (p <= stops[0][0]) return stops[0][1];
    for (let i = 1; i < stops.length; i++) if (p <= stops[i][0]) {
      const [p0, c0] = stops[i - 1], [p1, c1] = stops[i];
      return mix(c0, c1, (p - p0) / (p1 - p0));
    }
    return stops[stops.length - 1][1];
  }
  const markT = (cx, cy, k, px = 120, py = 120) => `translate(${cx} ${cy}) scale(${k}) translate(${-px} ${-py})`;
  function glowFilter(S, name, sd) {
    const f = el('filter', { id: S.id + name, x: '-50%', y: '-50%', width: '200%', height: '200%' }, S.defs);
    el('feGaussianBlur', { stdDeviation: sd, result: 'b' }, f);
    const m = el('feMerge', {}, f); el('feMergeNode', { in: 'b' }, m); el('feMergeNode', { in: 'SourceGraphic' }, m);
    return `url(#${S.id + name})`;
  }
  function radial(S, name, stops, attrs) {
    const g = el('radialGradient', Object.assign({ id: S.id + name }, attrs || {}), S.defs);
    stops.forEach(([o, c, a]) => el('stop', { offset: o, 'stop-color': c, 'stop-opacity': a }, g));
    return `url(#${S.id + name})`;
  }
  function linear(S, name, stops, attrs) {
    const g = el('linearGradient', Object.assign({ id: S.id + name, x1: 0, y1: 0, x2: 0, y2: 1 }, attrs || {}), S.defs);
    stops.forEach(([o, c, a]) => el('stop', { offset: o, 'stop-color': c, 'stop-opacity': a }, g));
    return `url(#${S.id + name})`;
  }
  // Periodic flicker: whole-number cycles per loop, so loops are seamless.
  const flick = (t, per, seed = 0) => .5 + .22 * Math.sin(TAU * (5 * t / per) + seed) + .16 * Math.sin(TAU * (11 * t / per) + 1.7 + seed) + .1 * Math.sin(TAU * (23 * t / per) + 4.1 + seed);

  const ANIMS = {};

  /* 1. WAI: the two halves of the W come together; the palms meet with a line of gold light, then a small bow. */
  ANIMS.wai = {
    dur: 3.4, title: 'The wai',
    build(S) {
      const k = 2.6;
      const bloom = el('circle', { cx: 500, cy: 470, r: 360, fill: radial(S, 'bl', [[0, C.gold, .55], [.5, C.gold, .12], [1, C.gold, 0]]), opacity: 0 }, S.root);
      const g = el('g', {}, S.root);
      [['L', -200, 320.3], ['R', 119.7, 320]].forEach(([n, x, w]) => el('rect', { x, y: -100, width: w, height: 440 }, el('clipPath', { id: S.id + n }, S.defs)));
      const half = n => { const h = el('g', {}, g); el('path', { d: A.mark, fill: S.col }, el('g', { 'clip-path': `url(#${S.id + n})` }, h)); return h; };
      const L = half('L'), R = half('R');
      const seam = el('path', { d: 'M120 66 L120 136', stroke: C.gold, 'stroke-width': 2.4, 'stroke-linecap': 'round', filter: glowFilter(S, 'gl', 2.2), opacity: 0 }, g);
      return t => {
        const a = E.inOut(t / 1.6), ang = 24 * (1 - a), dx = 70 * (1 - a);
        L.setAttribute('transform', `translate(${-dx} 0) rotate(${-ang} 120 178)`);
        R.setAttribute('transform', `translate(${dx} 0) rotate(${ang} 120 178)`);
        g.setAttribute('opacity', E.out(t / .6));
        const e = t - 1.55, v = e < 0 ? 0 : e < .14 ? e / .14 : Math.exp(-(e - .14) * 3.2);
        seam.setAttribute('opacity', v); bloom.setAttribute('opacity', .5 * v);
        const b = Math.sin(Math.PI * clamp((t - 1.65) / .9)); // the bow
        g.setAttribute('transform', markT(500, 500 + 9 * b, k * (1 - .022 * b)));
      };
    },
  };

  /* 2. DRAW: one line starts at the peak, splits both ways round the W, then the W fills in. */
  ANIMS.draw = {
    dur: 2.8, title: 'Draw-on',
    build(S) {
      const k = 2.6;
      const g = el('g', { transform: markT(500, 500, k) }, S.root);
      const fill = el('path', { d: A.mark, fill: S.col, opacity: 0 }, g);
      const probe = el('path', { d: A.mark, fill: 'none' }, g);
      const len = probe.getTotalLength(), N = 720, pts = [];
      for (let i = 0; i < N; i++) { const p = probe.getPointAtLength(len * i / N); pts.push([p.x, p.y]); }
      probe.remove();
      let tip = 0; pts.forEach((p, i) => { if (Math.hypot(p[0] - 120, p[1] - 62) < Math.hypot(pts[tip][0] - 120, pts[tip][1] - 62)) tip = i; });
      const half = N / 2, fwd = [], back = [];
      for (let i = 0; i <= half; i++) { fwd.push(pts[(tip + i) % N]); back.push(pts[(tip - i + N) % N]); }
      const lines = [fwd, back].map(ps => {
        const l = el('polyline', { points: ps.map(p => p.join(',')).join(' '), fill: 'none', stroke: S.col, 'stroke-width': 1.3, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, g);
        l.setAttribute('stroke-dasharray', `${len / 2 + 2} ${len}`); return l;
      });
      return t => {
        const a = E.inOut(t / 1.7);
        lines.forEach(l => { l.setAttribute('stroke-dashoffset', (len / 2 + 2) * (1 - a)); l.setAttribute('opacity', 1 - E.out((t - 2.0) / .5)); });
        fill.setAttribute('opacity', E.out((t - 1.35) / .8));
      };
    },
  };

  /* 3. IGNITE: SAWADEE rises in, then BURN catches letter by letter: ember, tangerine, gold, cream. Only BURN glows. */
  ANIMS.ignite = {
    dur: 4.2, title: 'BURN ignites', endless: true,
    build(S) {
      const [vx, vy, vw, vh] = A.lockupVB, s = 900 / vw;
      const g = el('g', { transform: `translate(500 500) scale(${s}) translate(${-(vx + vw / 2)} ${-(vy + vh / 2)})` }, S.root);
      const under = el('ellipse', { cx: 491, cy: 100, rx: 230, ry: 34, fill: radial(S, 'ug', [[0, C.tang, .45], [1, C.tang, 0]]), opacity: 0 }, g);
      const glowF = `url(#${S.id}bf)`;
      const f = el('filter', { id: S.id + 'bf', x: '-60%', y: '-60%', width: '220%', height: '220%' }, S.defs);
      el('feGaussianBlur', { stdDeviation: 5 }, f);
      const top = [], burn = [];
      A.glyphs.forEach(gl => {
        if (gl.word === 'top') top.push(el('path', { d: gl.d, 'fill-rule': gl.rule, fill: S.col, opacity: 0 }, g));
        else {
          const glow = el('path', { d: gl.d, fill: C.tang, filter: glowF, opacity: 0 }, g);
          burn.push({ glow, p: el('path', { d: gl.d, fill: S.col, opacity: .14 }, g) });
        }
      });
      return t => {
        top.forEach((p, i) => { const a = E.out((t - .1 - i * .1) / .55); p.setAttribute('opacity', a); p.setAttribute('transform', `translate(0 ${18 * (1 - a)})`); });
        burn.forEach((b, j) => {
          const p = (t - 1.35 - j * .3) / 1.1;
          b.p.setAttribute('fill', ramp([[0, S.dim], [.28, C.tang], [.55, C.gold], [1, S.col]], p));
          b.p.setAttribute('opacity', p <= 0 ? .14 : 1);
          const settle = .3 + .25 * flick(t, 6, j * 1.9);
          const peak = p <= 0 ? 0 : p < .3 ? p / .3 : lerp(1, settle, E.out((p - .3) / .7));
          b.glow.setAttribute('opacity', peak);
          b.glow.setAttribute('fill', p < .45 ? C.tang : C.gold);
        });
        under.setAttribute('opacity', E.out((t - 1.5) / 1.2) * (.6 + .4 * flick(t, 6, 3)));
      };
    },
  };

  /* 4. SUNRISE: the gold badge rises out of the sea; its reflection shimmers below. */
  ANIMS.sunrise = {
    dur: 3.4, title: 'Sun over the sea', endless: true, scene: true,
    build(S) {
      const H = 640, k = 1.9;
      el('rect', { x: -5000, y: -5000, width: 10000, height: 5000 + H, fill: C.sea }, S.root);
      const warm = el('rect', { x: -5000, y: H - 520, width: 10000, height: 520, fill: linear(S, 'sk', [[0, C.tang, 0], [.6, C.tang, .18], [1, C.tang, .62]]), opacity: 0 }, S.root);
      el('rect', { x: -5000, y: H, width: 10000, height: 5000, fill: '#04242A' }, S.root);
      el('rect', { x: -5000, y: -5000, width: 10000, height: 5000 + H }, el('clipPath', { id: S.id + 'sky', clipPathUnits: 'userSpaceOnUse' }, S.defs));
      const halo = el('circle', { r: 420, 'clip-path': `url(#${S.id}sky)`, fill: radial(S, 'ha', [[0, C.gold, .35], [.45, C.gold, .1], [1, C.gold, 0]]) }, S.root);
      const sunWrap = el('g', { id: S.id + 'sunw', 'clip-path': `url(#${S.id}sky)` }, S.root);
      const sun = el('g', {}, sunWrap);
      el('circle', { cx: 120, cy: 120, r: 105, fill: C.sea }, sun);
      el('path', { d: A.badge, 'fill-rule': 'evenodd', fill: C.gold }, sun);
      const refl = el('g', { id: S.id + 'refl', transform: `translate(0 ${2 * H}) scale(1 -1)` }, S.defs);
      el('use', { href: `#${S.id}sunw` }, refl);
      const slices = [], SH = 8, NS_ = 44;
      for (let i = 0; i < NS_; i++) {
        el('rect', { x: -5000, y: H + i * SH, width: 10000, height: SH + .6 }, el('clipPath', { id: S.id + 's' + i, clipPathUnits: 'userSpaceOnUse' }, S.defs));
        const o = el('g', { 'clip-path': `url(#${S.id}s${i})`, opacity: .5 * Math.pow(1 - i / NS_, 1.4) }, S.root);
        slices.push(el('use', { href: `#${S.id}refl` }, o));
      }
      el('rect', { x: -5000, y: H - .8, width: 10000, height: 1.6, fill: C.gold, opacity: .35 }, S.root);
      return t => {
        const a = E.out(t / 3.0), cy = lerp(H + 240, 432, a);
        sun.setAttribute('transform', markT(500, cy, k));
        halo.setAttribute('cx', 500); halo.setAttribute('cy', cy); halo.setAttribute('opacity', .4 + .6 * a);
        warm.setAttribute('opacity', .25 + .75 * a);
        slices.forEach((u, i) => u.setAttribute('x', (1.5 + i * .32) * Math.sin(TAU * t / 2 + i * .85) + (.6 + i * .12) * Math.sin(TAU * t / 1 + i * 2.3)));
      };
    },
  };

  /* 5. FIRELIGHT: a seamless 6 s loop. The W stands calm; firelight breathes from below; embers rise and die out before the W. */
  ANIMS.firelight = {
    dur: 6, title: 'Firelight loop', loop: true,
    build(S) {
      const k = 1.9, cy = 450, limit = cy + 58 * k + 90; // embers are gone by here (well below the W)
      const glow = el('ellipse', { cx: 500, rx: 900, fill: radial(S, 'fg', [[0, C.tang, .5], [.45, C.gold, .1], [1, C.gold, 0]]) }, S.root);
      const emG = el('g', { filter: glowFilter(S, 'eg', 2.4) }, S.root);
      const r = rng(11), em = [];
      for (let i = 0; i < 54; i++) {
        const c = el('circle', { r: 1.6 + r() * 3.6, fill: r() < .55 ? C.gold : C.tang }, emG);
        em.push({ c, m: 1 + Math.floor(r() * 2), ph: r(), x0: r(), sway: 8 + r() * 26, sw: r() * TAU, top: r() * 160 });
      }
      el('path', { d: A.mark, fill: S.col, transform: markT(500, cy, k) }, S.root);
      return t => {
        const vb = S.vb, bot = vb.y + vb.h, f = flick(t, 6);
        glow.setAttribute('cy', bot + 60); glow.setAttribute('ry', Math.max(380, (bot - cy) * 1.05));
        glow.setAttribute('opacity', .55 + .45 * f);
        em.forEach(e => {
          const u = ((t / 6) * e.m + e.ph) % 1, y = lerp(bot + 12, limit + e.top, u);
          e.c.setAttribute('cx', vb.x + e.x0 * vb.w + e.sway * Math.sin(TAU * u * 1.5 + e.sw));
          e.c.setAttribute('cy', y);
          e.c.setAttribute('opacity', Math.pow(Math.sin(Math.PI * u), .8) * (.55 + .45 * flick(t, 6, e.sw)));
        });
      };
    },
  };

  /* 6. WIPE: a transition. The W pops in, then we dive into the palms until the next colour fills the frame. */
  ANIMS.wipe = {
    dur: 1.5, title: 'W wipe',
    build(S) {
      const fillC = S.opts.fill || S.col;
      const g = el('g', {}, S.root);
      el('path', { d: A.mark, fill: fillC }, g);
      const cover = el('rect', { x: -5000, y: -5000, width: 10000, height: 10000, fill: fillC, opacity: 0 }, S.root);
      return t => {
        let k, px = 120, py = 120;
        if (t < .35) k = 2 * E.outBack(t / .35);
        else { const z = E.in((t - .35) / 1.1); k = 2 * Math.exp(Math.log(140) * z); py = lerp(120, 128, z); }
        g.setAttribute('transform', markT(500, 500, Math.max(k, .001), px, py));
        cover.setAttribute('opacity', t >= 1.45 ? 1 : 0);
      };
    },
  };

  function mount(container, name, opts) {
    opts = opts || {};
    const def = ANIMS[name];
    if (!def) throw new Error('unknown animation ' + name);
    const svg = el('svg', { xmlns: NS, width: '100%', height: '100%', role: 'img', 'aria-label': 'SaWadee Burn: ' + def.title });
    svg.style.display = 'block'; svg.style.overflow = 'hidden';
    container.appendChild(svg);
    const bgC = opts.bg === 'none' || opts.bg === false ? null : (opts.bg || C.sea);
    const light = bgC && hex(bgC).reduce((a, b) => a + b) > 450;
    const S = { svg, id: 'sw' + Math.random().toString(36).slice(2, 7), opts, vb: { x: 0, y: 0, w: 1000, h: 1000 } };
    S.col = opts.color || (light ? C.ink : C.cream);
    S.dim = light ? C.ink : C.cream;
    S.defs = el('defs', {}, svg);
    const bg = bgC ? el('rect', { fill: bgC }, svg) : null;
    S.root = el('g', {}, svg);
    let lastT = 0;
    function fit() {
      const r = container.getBoundingClientRect();
      const w = opts.width || r.width || 1000, h = opts.height || r.height || 1000;
      const vb = w >= h ? { w: 1000 * w / h, h: 1000 } : { w: 1000, h: 1000 * h / w };
      vb.x = 500 - vb.w / 2; vb.y = 500 - vb.h / 2; S.vb = vb;
      svg.setAttribute('viewBox', `${vb.x} ${vb.y} ${vb.w} ${vb.h}`);
      if (bg) ['x', 'y'].forEach(k => bg.setAttribute(k, vb[k])), bg.setAttribute('width', vb.w), bg.setAttribute('height', vb.h);
    }
    fit();
    const update = def.build(S);
    let raf = 0, start = 0;
    const api = {
      name, dur: def.dur, loop: !!def.loop, endless: !!(def.loop || def.endless), svg,
      seek(t) { lastT = t; update(t); },
      play() {
        cancelAnimationFrame(raf); start = performance.now();
        const tick = now => {
          let t = (now - start) / 1000;
          if (def.loop) t %= def.dur;
          update(t);
          if (api.endless || t < def.dur + .1) raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
      },
      stop() { cancelAnimationFrame(raf); },
    };
    if (!opts.width && window.ResizeObserver) new ResizeObserver(() => { fit(); update(lastT); }).observe(container);
    update(0);
    return api;
  }

  function auto() {
    const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('[data-sawadee]').forEach(node => {
      if (node._sawadee) return;
      const m = mount(node, node.dataset.sawadee, { bg: node.dataset.bg, color: node.dataset.color, fill: node.dataset.fill });
      node._sawadee = m;
      if (reduce) { m.seek(m.loop ? 0 : m.dur); return; }
      node.addEventListener('click', () => m.play());
      if (!window.IntersectionObserver) return m.play();
      let seen = false;
      new IntersectionObserver(es => es.forEach(e => {
        if (e.isIntersecting && (!seen || m.endless)) { seen = true; m.play(); }
        else if (!e.isIntersecting && m.endless) m.stop();
      }), { threshold: .4 }).observe(node);
    });
  }

  window.SawadeeMotion = { mount, auto, ANIMS, C };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto); else auto();
})();
