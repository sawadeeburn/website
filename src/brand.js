/* /brand: pick an ink per mark (preview and download links follow), click a colour to copy it. Works without JS: the deep-sea files are linked by default. */
(function () {
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const NAMES = { sea: 'Deep sea', cream: 'Cream', gold: 'Gold', black: 'Black', white: 'White' };

  $$('.mk[data-key]').forEach(card => {
    const key = card.dataset.key, name = card.querySelector('.ink-name');
    $$('.mk-inks button', card).forEach(btn => btn.addEventListener('click', () => {
      const ink = btn.dataset.ink;
      card.dataset.ink = ink;
      $$('.mk-inks button', card).forEach(b => b.setAttribute('aria-pressed', b === btn));
      $$('.dl', card).forEach(a => { a.href = `/brand/files/sawadee-burn-${key}-${ink}.${a.dataset.ext}`; });
      if (name) name.textContent = NAMES[ink];
    }));
  });

  const said = document.getElementById('copied');
  $$('.sw').forEach(sw => sw.addEventListener('click', () => {
    const hex = sw.dataset.hex;
    const done = () => { if (said) { said.textContent = hex + ' copied'; clearTimeout(said._t); said._t = setTimeout(() => said.textContent = '', 2200); } };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(hex).then(done, () => { if (said) said.textContent = hex; });
    else if (said) said.textContent = hex;
  }));
})();
