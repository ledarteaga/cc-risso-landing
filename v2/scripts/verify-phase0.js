// Verificación de Fase 0: escala de 4 niveles + ritmo vertical uniforme.
// Falla con exit 1 si algo se sale de la regla.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const PAGES = ['index', 'tiendas', 'descuentos', 'sobre-risso', 'contacto', 'libro-reclamaciones'];
const ALLOWED_HEADING = [72, 44, 24];
const BAND = 72;

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const fails = [];
  const allHeadings = {};

  for (const name of PAGES) {
    await page.goto(`${BASE}/${name}.html`, { waitUntil: 'load' });
    await page.waitForTimeout(600);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);

    const r = await page.evaluate(() => {
      const px = (v) => Math.round(parseFloat(v) || 0);
      const heads = [...document.querySelectorAll('h1,h2,h3')]
        .filter((e) => !e.closest('footer'))
        .map((e) => ({
          tag: e.tagName, fs: px(getComputedStyle(e).fontSize), text: e.innerText.trim().slice(0, 40),
          sel: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).trim().split(/\s+/)[0] : ''),
        }));
      const body = [...document.querySelectorAll('p')]
        // Metadatos de UI (etiquetas, kickers en <p>, letra chica legal): fuera de la escala por diseño.
        .filter((e) => !e.closest('.kicker, footer, .promo-vigency, .photo-row-cap, .visit-plate, .wizard-error, .error-msg, .field-hint, .reclamo-disclaimer, .legal-note, .toc, .meta, .hero-progress, .directory-count, .filter-status')
                        && !e.matches('.info-cell-label, .promo-marcas-eyebrow, .contact-map-fallback, .photo-row-cap-year, .photo-row-cap-text, .marca-note'))
        .map((e) => ({
          fs: px(getComputedStyle(e).fontSize),
          sel: 'p' + (e.className ? '.' + String(e.className).trim().split(/\s+/)[0] : ''),
          text: e.innerText.trim().slice(0, 34),
        }));
      const sections = [...document.querySelectorAll('main > section')].map((s) => ({
        cls: s.className,
        t: px(getComputedStyle(s).paddingTop), b: px(getComputedStyle(s).paddingBottom),
        exempt: s.classList.contains('hero') || s.classList.contains('photo-band'),
      }));
      const f = document.querySelector('.site-footer');
      return { heads, body, sections, footer: { t: px(getComputedStyle(f).paddingTop), b: px(getComputedStyle(f).paddingBottom) } };
    });

    const headSizes = [...new Set(r.heads.map((h) => h.fs))].sort((a, b) => b - a);
    allHeadings[name] = headSizes;
    headSizes.forEach((s) => { if (!ALLOWED_HEADING.includes(s)) {
      const bad = r.heads.filter((h) => h.fs === s).slice(0, 2).map((h) => `${h.sel} "${h.text}"`).join(', ');
      fails.push(`${name}: titular a ${s}px fuera de {72,44,24} → ${bad}`);
    } });
    r.body.forEach((b) => { if (b.fs !== 17) fails.push(`${name}: ${b.sel} a ${b.fs}px (esperado 17) — "${b.text}"`); });
    r.sections.forEach((s) => {
      if (s.exempt) return;
      if (s.t !== BAND || s.b !== BAND) fails.push(`${name}: sección ${s.cls} = ${s.t}/${s.b} (esperado 72/72)`);
    });
    if (r.footer.t !== BAND || r.footer.b !== BAND) fails.push(`${name}: footer = ${r.footer.t}/${r.footer.b} (esperado 72/72)`);
  }

  console.log('Tamaños de titular por página:');
  for (const [k, v] of Object.entries(allHeadings)) console.log(`  ${k.padEnd(20)} ${v.join(' / ')}`);
  const union = [...new Set(Object.values(allHeadings).flat())].sort((a, b) => b - a);
  console.log(`\nTamaños distintos en el sitio: ${union.length} → ${union.join(' / ')}`);
  console.log(`Ritmo vertical: ${BAND}px exigidos en todas las secciones y en el footer.`);

  if (fails.length) {
    console.log(`\n✗ ${fails.length} incumplimiento(s):`);
    [...new Set(fails)].slice(0, 25).forEach((f) => console.log('  - ' + f));
    await browser.close();
    process.exit(1);
  }
  console.log('\n✓ Fase 0 verificada: 3 tamaños de titular (72/44/24) + cuerpo 17 + ritmo 72/72.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
