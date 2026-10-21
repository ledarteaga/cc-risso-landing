// Verificación Fase 4: footer (grid 12, legal con copyright) + Sobre Risso.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const PAGES = ['index', 'tiendas', 'descuentos', 'sobre-risso', 'contacto', 'libro-reclamaciones'];
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  for (const name of PAGES) {
    await page.goto(`${BASE}/${name}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(() => {
      const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
      const px = (v) => Math.round(parseFloat(v) || 0);
      const top = document.querySelector('.footer-top');
      const legal = document.querySelector('.footer-col--legal');
      const note = document.querySelector('.footer-legal-note');
      const social = document.querySelector('.footer-socials');
      const footer = document.querySelector('.site-footer');
      const navContact = [...document.querySelectorAll('.nav a, .mobile-drawer a')].find((a) => a.getAttribute('href') === 'contacto.html');
      return {
        cols: cs(top, 'gridTemplateColumns').split(' ').length,
        brandW: px(document.querySelector('.footer-brand').getBoundingClientRect().width),
        legalItems: legal ? legal.querySelectorAll('li').length : 0,
        noteW: note ? px(note.getBoundingClientRect().width) : 0,
        socialDir: social ? cs(social, 'flexDirection') : null,
        socialIcon: px(document.querySelector('.footer-socials svg').getBoundingClientRect().width),
        footerPad: [px(cs(footer, 'paddingTop')), px(cs(footer, 'paddingBottom'))],
        rightEdge: Math.round(innerWidth - document.querySelector('.footer-inner').getBoundingClientRect().right),
        navLabel: navContact ? navContact.textContent.trim() : null,
      };
    });
    console.log(name.padEnd(22), JSON.stringify(r));
    ok(r.cols === 12, `${name}: footer con ${r.cols} columnas (esperado 12)`);
    ok(r.legalItems === 1, `${name}: Legal con ${r.legalItems} ítems`);
    ok(r.noteW > 60, `${name}: el copyright no está en la columna Legal`);
    ok(r.socialDir === 'row', `${name}: RRSS del footer en ${r.socialDir}`);
    ok(r.socialIcon === 20, `${name}: icono social ${r.socialIcon}px (esperado 20)`);
    ok(r.footerPad[0] === 72 && r.footerPad[1] === 72, `${name}: footer ${r.footerPad.join('/')}`);
    ok(r.navLabel === 'Contáctanos', `${name}: nav dice "${r.navLabel}"`);
  }

  // Sobre Risso: índice fuera, encabezado nuevo, "Hoy" con peso
  await page.goto(`${BASE}/sobre-risso.html`, { waitUntil: 'networkidle' });
  const sr = await page.evaluate(() => ({
    toc: !!document.querySelector('.toc'),
    intro: !!document.querySelector('.beats-intro h2'),
    hoyFs: Math.round(parseFloat(getComputedStyle(document.querySelector('#hoy-title')).fontSize)),
    h2s: [...new Set([...document.querySelectorAll('h2')].map((e) => Math.round(parseFloat(getComputedStyle(e).fontSize))))].sort((a, b) => b - a),
  }));
  console.log('sobre-risso', JSON.stringify(sr));
  ok(!sr.toc, 'sobre-risso: el índice sigue presente');
  ok(sr.intro, 'sobre-risso: falta el encabezado que reemplaza al índice');
  ok(sr.hoyFs === 44, `sobre-risso: "Hoy" a ${sr.hoyFs}px (esperado 44)`);

  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Fase 4 verificada.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
