/* SaWadee Burn site. No dependencies. Everything here is an extra: the page reads fine without it. */
(function () {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- poster type: each .fit line fills its column --- */
  function fit() {
    const els = $$('.fit');
    els.forEach(e => { e.style.fontSize = '10px'; });                       // shrink first, so no line props its own column open
    const box = els.map(e => e.parentElement.clientWidth * parseFloat(e.dataset.w || 1));
    els.forEach(e => { e.style.fontSize = '100px'; e.style.display = 'inline-block'; });
    const w = els.map(e => e.getBoundingClientRect().width);
    const cap = innerHeight * .42;
    let fs = els.map((e, i) => box[i] && w[i] ? 100 * box[i] / w[i] : 0);
    for (let pass = 0; pass < 2; pass++) {                                    // the face is not quite linear in size: measure again at the real size
      els.forEach((e, i) => { if (fs[i]) e.style.fontSize = fs[i] + 'px'; });
      const w2 = els.map(e => e.getBoundingClientRect().width);
      fs = fs.map((f, i) => f && w2[i] ? f * box[i] / w2[i] : f);
    }
    els.forEach((e, i) => { e.style.display = ''; e.style.fontSize = fs[i] ? Math.min(fs[i] * .995, cap) + 'px' : ''; });
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  let rw = innerWidth, rt;
  addEventListener('resize', () => { if (innerWidth === rw) return; rw = innerWidth; clearTimeout(rt); rt = setTimeout(fit, 80); });

  /* --- the date band: click or tap to stop it --- */
  const run = $('.ticker-run');
  if (run) run.parentElement.addEventListener('click', () => { run.style.animationPlayState = run.style.animationPlayState === 'paused' ? '' : 'paused'; });

  /* --- phone dock: shows once the hero is behind you --- */
  const dock = $('#dock'), hero = $('.hero');
  if (dock && hero && 'IntersectionObserver' in window) {
    dock.hidden = false;
    new IntersectionObserver(es => dock.classList.toggle('on', !es[0].isIntersecting), { threshold: .05 }).observe(hero);
  }

  /* --- menu --- */
  const mb = $('#menu-btn'), menu = $('#menu');
  if (mb && menu) {
    const set = open => { menu.classList.toggle('open', open); mb.setAttribute('aria-expanded', open); mb.textContent = open ? 'Close' : 'Menu'; document.body.style.overflow = open ? 'hidden' : ''; };
    mb.addEventListener('click', () => set(!menu.classList.contains('open')));
    menu.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('open')) { set(false); mb.focus(); } });
  }

  /* --- day / night print --- */
  const th = $('#theme');
  if (th) th.addEventListener('click', () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('sb-theme', root.dataset.theme); } catch (e) {}
  });

  /* --- getting there: tabs drive the panels and the map --- */
  const tabs = $$('.route-tabs [role=tab]');
  function pick(k, focus) {
    tabs.forEach(t => { const on = t.dataset.route === k; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; if (on && focus) t.focus(); });
    $$('.route').forEach(p => p.hidden = p.dataset.route !== k);
    $$('.map .rt').forEach(g => g.classList.remove('on'));
    $$('.map .edge').forEach(g => g.style.opacity = g.dataset.for.split(' ').includes(k) ? 1 : 0);
    const g = $(`.map .rt[data-route="${k}"]`);
    if (g) { g.getBoundingClientRect(); requestAnimationFrame(() => g.classList.add('on')); }
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(t.dataset.route));
    t.addEventListener('keydown', e => {
      const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
      if (!d) return; e.preventDefault(); pick(tabs[(i + d + tabs.length) % tabs.length].dataset.route, true);
    });
  });
  const map = $('.map');
  if (map && tabs.length) {
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { pick(tabs.find(t => t.getAttribute('aria-selected') === 'true').dataset.route); io.disconnect(); } }, { threshold: .35 });
      io.observe(map);
    } else pick(tabs[0].dataset.route);
  }

  /* --- film --- */
  const v = $('#teaser'), bp = $('#v-play'), bs = $('#v-sound');
  if (v && bp && bs) {
    const sync = () => { const on = !v.paused; bp.setAttribute('aria-pressed', on); bp.textContent = on ? 'Pause the film' : 'Play the film'; };
    bp.addEventListener('click', () => v.paused ? v.play() : v.pause());
    v.addEventListener('click', () => v.paused ? v.play() : v.pause());
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    bs.addEventListener('click', () => { v.muted = !v.muted; bs.setAttribute('aria-pressed', !v.muted); bs.textContent = v.muted ? 'Sound on' : 'Sound off'; if (!v.muted && v.paused) v.play(); });
    if ('IntersectionObserver' in window) {
      let auto = !reduce;
      bp.addEventListener('click', () => auto = false);
      new IntersectionObserver(es => { const e = es[0]; if (e.isIntersecting && auto) v.play().catch(() => {}); else if (!e.isIntersecting && !v.paused) v.pause(); }, { threshold: .5 }).observe(v);
    }
  }

  /* --- stickers peel off: drag them anywhere --- */
  $$('.stk').forEach(st => {
    let sx, sy, ox = 0, oy = 0, on = false;
    st.style.touchAction = 'none'; st.style.cursor = 'grab';
    st.addEventListener('pointerdown', e => { on = true; sx = e.clientX - ox; sy = e.clientY - oy; st.setPointerCapture(e.pointerId); st.style.cursor = 'grabbing'; st.style.transition = 'none'; });
    st.addEventListener('pointermove', e => { if (!on) return; ox = e.clientX - sx; oy = e.clientY - sy; st.style.translate = ox + 'px ' + oy + 'px'; });
    const up = () => { on = false; st.style.cursor = 'grab'; st.style.transition = ''; };
    st.addEventListener('pointerup', up); st.addEventListener('pointercancel', up);
  });

  /* --- FAQ search --- */
  const q = $('#faq-q'), none = $('#faq-none');
  if (q) q.addEventListener('input', () => {
    const words = q.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    $$('.faq-group').forEach(g => {
      let any = false;
      $$('details', g).forEach(d => {
        const hit = !words.length || words.every(w => d.textContent.toLowerCase().includes(w));
        d.hidden = !hit; d.open = hit && words.length > 0; if (hit) { any = true; shown++; }
      });
      g.hidden = !any;
    });
    none.hidden = shown > 0;
  });
  /* --- countdowns: fill in the numbers; a countdown that has run out goes away.
     Each unit keeps its own element, so only a number that changed is printed again (.flip) --- */
  const cds = $$('.cd[data-to]');
  if (cds.length) {
    const pad = n => String(n).padStart(2, '0');
    const tick = () => {
      const now = Date.now();
      cds.forEach(c => {
        const left = Date.parse(c.dataset.to) - now, out = c.querySelector('.cd-n');
        if (left <= 0) { c.hidden = true; return; }
        const s = Math.floor(left / 1000), d = Math.floor(s / 86400), h = Math.floor(s / 3600) % 24, m = Math.floor(s / 60) % 60;
        const parts = [[String(d), d === 1 ? 'day' : 'days'], [pad(h), 'hrs'], [pad(m), 'min']];
        if (!reduce) parts.push([pad(s % 60), 'sec']);
        if (out.children.length !== parts.length) { out.innerHTML = parts.map(([n, u]) => '<i><b>' + n + '</b><small>' + u + '</small></i>').join(''); return; }
        parts.forEach(([n, u], k) => {
          const el = out.children[k], b = el.firstChild;
          if (b.textContent === n) return;
          b.textContent = n; el.lastChild.textContent = u;
          if (u !== 'sec') { el.classList.remove('flip'); void el.offsetWidth; el.classList.add('flip'); }
        });
      });
    };
    tick(); setInterval(tick, reduce ? 30000 : 1000);
  }
  /* --- the fuse on the ticket: the flame sits at (time used / whole first round) along the rule, from the right --- */
  const fuse = $('.tkt .fuse'), fcd = $('.tkt .cd[data-from]');
  if (fuse && fcd) {
    const lit = () => {
      const t0 = Date.parse(fcd.dataset.from), t1 = Date.parse(fcd.dataset.to), now = Date.now();
      if (now < t0 || now >= t1) { fuse.hidden = true; return; }
      fuse.style.setProperty('--p', ((now - t0) / (t1 - t0)).toFixed(4));
      fuse.hidden = false;
    };
    lit(); setInterval(lit, 60000);
  }
})();
