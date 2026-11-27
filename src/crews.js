/* /crews: shuffle the board. The points don't matter, so the order shouldn't either. */
(() => {
  const btn = document.getElementById('shuffle'), list = document.getElementById('crew-list');
  if (!btn || !list) return;
  const words = ['Shuffle it', 'Again', 'Once more', 'See? Still fine', 'Shuffle it'];
  let n = 0;
  btn.addEventListener('click', () => {
    const items = [...list.children];
    const first = new Map(items.map(el => [el, el.getBoundingClientRect()]));
    for (let i = items.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [items[i], items[j]] = [items[j], items[i]]; }
    items.forEach(el => { el.style.setProperty('--r', ((Math.random() * 6) - 3).toFixed(1) + 'deg'); list.appendChild(el); });
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) items.forEach(el => {
      const a = first.get(el), b = el.getBoundingClientRect();
      el.animate([{ translate: `${a.left - b.left}px ${a.top - b.top}px` }, { translate: '0 0' }], { duration: 600, easing: 'cubic-bezier(.16,1,.3,1)' });
    });
    btn.textContent = words[++n % words.length];
  });
})();

/* /crews: the start-a-crew form posts in the background; the email link stays as a fallback. */
(() => {
  const f = document.getElementById('crew-form'), msg = document.getElementById('crew-msg');
  if (!f) return;
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const file = f.flag.files[0];
    if (file && file.size > 4 * 1024 * 1024) { msg.textContent = 'That picture is over 4 MB. Try a smaller one.'; return; }
    const btn = f.querySelector('button'); btn.disabled = true; msg.textContent = 'Sending...';
    try {
      const r = await fetch(f.action, { method: 'POST', body: new FormData(f) });
      const d = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(d.error || 'failed');
      f.reset();
      msg.textContent = "Got it. We'll send your crew link soon.";
    } catch (err) {
      msg.textContent = err.message && err.message !== 'failed' ? err.message : "That didn't go through. Use the email link below.";
    } finally { btn.disabled = false; }
  });
})();
