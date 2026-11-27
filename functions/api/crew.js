// POST /api/crew: the "Start a crew" form on /crews. Emails the team through Resend; nothing is stored.
// Needs the Pages secret RESEND_API_KEY (a sending-only key for sawadeeburn.com). Without it the page shows the email link.
const TO = ['ticketing@sawadeeburn.com'];
const CC = ['sean.katz@gmail.com'];
const FROM = 'SaWadee Burn crews <crews@sawadeeburn.com>';
const MAX_FLAG = 4 * 1024 * 1024;
const IMG = ['image/png', 'image/jpeg', 'image/webp', 'image/gif'];

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
const clean = (v, n) => String(v || '').replace(/[\r\n\t]+/g, ' ').trim().slice(0, n);
const esc = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const b64 = buf => { let s = ''; const a = new Uint8Array(buf); for (let i = 0; i < a.length; i += 0x8000) s += String.fromCharCode(...a.subarray(i, i + 0x8000)); return btoa(s); };

export async function onRequestPost({ request, env }) {
  let form;
  try { form = await request.formData(); } catch { return json(400, { error: 'Something was off with the form. Try again.' }); }
  if (clean(form.get('website'), 200)) return json(200, { ok: true });          // honeypot: bots get a quiet "ok"
  const crew = clean(form.get('crew'), 40), name = clean(form.get('name'), 40);
  const contact = clean(form.get('contact'), 80), line = clean(form.get('line'), 80);
  if (!crew || !name || !contact) return json(400, { error: 'Please fill in the crew name, your name and how to reach you.' });
  if (!env.RESEND_API_KEY) return json(503, { error: "That didn't go through. Use the email link below." });

  const attachments = [];
  const flag = form.get('flag');
  if (flag && typeof flag === 'object' && flag.size) {
    if (flag.size > MAX_FLAG) return json(400, { error: 'That picture is over 4 MB. Try a smaller one.' });
    if (!IMG.includes(flag.type)) return json(400, { error: 'The flag needs to be a PNG, JPG, WEBP or GIF.' });
    attachments.push({ filename: clean(flag.name, 80) || 'flag', content: b64(await flag.arrayBuffer()) });
  }

  const rows = [['Crew', crew], ['Name', name], ['Contact', contact], ['Line', line || '-'], ['Flag', attachments.length ? 'attached' : 'none']];
  const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact);
  const msg = {
    from: FROM, to: TO, cc: CC,
    subject: `New crew: ${crew}`,
    text: rows.map(([k, v]) => `${k}: ${v}`).join('\n') + '\n\nNext: give them the next free code (marketing/crews/codes.csv) and add them to crews.json.',
    html: '<table>' + rows.map(([k, v]) => `<tr><td><b>${k}</b></td><td>${esc(v)}</td></tr>`).join('') + '</table>' +
          '<p>Next: give them the next free code and add them to crews.json.</p>',
    ...(isEmail ? { reply_to: contact } : {}),
    ...(attachments.length ? { attachments } : {}),
  };
  const r = await fetch(env.RESEND_URL || 'https://api.resend.com/emails', {
    method: 'POST', headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' }, body: JSON.stringify(msg),
  });
  if (!r.ok) { console.log('resend', r.status, (await r.text()).slice(0, 300)); return json(502, { error: "That didn't go through. Use the email link below." }); }
  return json(200, { ok: true });
}

