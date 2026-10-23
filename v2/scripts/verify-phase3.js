// Verificación Fase 3: Contacto (portada con mapa, orden, split) + GL-01.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  // ---------- contacto.html ----------
  await page.goto(`${BASE}/contacto.html`, { waitUntil: 'load' });
  await page.waitForTimeout(600);
  await page.evaluate(() => document.fonts.ready);
  const c = await page.evaluate(() => {
    const px = (v) => Math.round(parseFloat(v) || 0);
    const sections = [...document.querySelectorAll('main > section')].map((s) => s.className);
    const map = document.querySelector('.page-open-map iframe');
    const mapBox = map ? map.getBoundingClientRect() : null;
    const icons = document.querySelectorAll('.frente-card .frente-icon svg').length;
    const descs = [...document.querySelectorAll('.frente-card .frente-desc')].map((e) => e.textContent.trim());
    const bands = [...document.querySelectorAll('main > section')].map((s) => getComputedStyle(s).backgroundColor);
    return {
      photoBand: !!document.querySelector('.photo-band'),
      sections,
      mapInHero: !!map,
      mapTop: mapBox ? Math.round(mapBox.top + scrollY) : null,
      mapWidth: mapBox ? Math.round(mapBox.width) : null,
      frenteIcons: icons,
      maxDescLen: Math.max(...descs.map((d) => d.length)),
      blackBands: bands.filter((b) => b === 'rgb(0, 0, 0)').length,
      dupeKickers: document.querySelectorAll('.wizard-pane[data-pane="2"] .kicker').length,
    };
  });
  console.log('contacto', JSON.stringify(c));
  ok(!c.photoBand, 'contacto: sigue el photo-band');
  ok(c.mapInHero, 'contacto: el mapa no está en la portada');
  ok(c.mapTop < 700, `contacto: el mapa arranca a ${c.mapTop}px (debe verse sin scroll)`);
  ok(c.frenteIcons === 3, `contacto: ${c.frenteIcons} iconos en las tarjetas (esperado 3)`);
  ok(c.maxDescLen <= 50, `contacto: descripción de ${c.maxDescLen} caracteres (máx 50)`);
  ok(c.blackBands === 0, `contacto: ${c.blackBands} banda(s) negra(s) fuera del footer`);
  ok(c.dupeKickers === 0, 'contacto: quedan kickers duplicados en el paso 2');

  // orden: info antes de wizard
  const order = c.sections.join(' | ');
  const iInfo = c.sections.findIndex((s) => s.includes('info-section'));
  const iWiz = c.sections.findIndex((s) => s.includes('wizard'));
  ok(iInfo > -1 && iWiz > -1 && iInfo < iWiz, `contacto: orden incorrecto → ${order}`);

  // ---------- como-llegar.html ----------
  await page.goto(`${BASE}/como-llegar.html`, { waitUntil: 'load' });
  await page.waitForTimeout(600);
  const l = await page.evaluate(() => ({
    title: document.title,
    h1: document.querySelector('h1')?.textContent.trim(),
    map: !!document.querySelector('.page-open-map iframe'),
    links: [...document.querySelectorAll('a[href="contacto.html"]')].length,
    footer: !!document.querySelector('.footer-col--legal'),
    h2s: [...new Set([...document.querySelectorAll('h2')].map((e) => Math.round(parseFloat(getComputedStyle(e).fontSize))))],
  }));
  console.log('como-llegar', JSON.stringify(l));
  ok(l.map, 'como-llegar: sin mapa');
  ok(l.h1 && /Arequipa/.test(l.h1), 'como-llegar: h1 inesperado');
  ok(l.footer, 'como-llegar: footer desincronizado');

  // ---------- grado global: ninguna banda negra fuera del footer ----------
  for (const name of ['index', 'tiendas', 'descuentos', 'sobre-risso', 'libro-reclamaciones', 'como-llegar']) {
    await page.goto(`${BASE}/${name}.html`, { waitUntil: 'load' });
    await page.waitForTimeout(600);
    const black = await page.evaluate(() => [...document.querySelectorAll('main > section')]
      .filter((s) => getComputedStyle(s).backgroundColor === 'rgb(0, 0, 0)').length);
    ok(black === 0, `${name}: ${black} banda(s) negra(s) en main`);
  }

  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Fase 3 verificada.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
