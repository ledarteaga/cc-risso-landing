// Verificación Fase 1 (Inicio + Historia) y Fase 0 en regresión.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };

(async () => {
  const browser = await chromium.launch();
  for (const [w, h, label] of [[1440, 900, 'desktop'], [390, 844, 'mobile']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: label === 'mobile', hasTouch: label === 'mobile' });
    const page = await ctx.newPage();
    await page.goto(`${BASE}/index.html`, { waitUntil: 'load' });
    await page.waitForTimeout(600);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);

    const r = await page.evaluate(() => {
      const px = (v) => Math.round(parseFloat(v) || 0);
      const claim = document.querySelector('.hero-claim');
      const range = document.createRange(); range.selectNodeContents(claim);
      const textW = range.getBoundingClientRect().width;
      const social = document.querySelector('.hero-socials a');
      const svg = document.querySelector('.hero-socials svg');
      const timeline = document.querySelector('.timeline');
      const photoRow = document.querySelector('.photo-row');
      const figures = photoRow ? photoRow.querySelectorAll('figure').length : 0;
      const years = [...document.querySelectorAll('.photo-row .photo-row-cap-year')].length;
      const heroCta = document.querySelector('.hero-cta');
      const headCta = document.querySelector('.anchor-head-cta');
      const heroH = document.querySelector('.hero').getBoundingClientRect().height;
      const contentH = document.querySelector('.hero-content').getBoundingClientRect().height;
      return {
        claimFs: px(getComputedStyle(claim).fontSize),
        claimUpper: getComputedStyle(claim).textTransform,
        claimTextPct: Math.round(textW / innerWidth * 100),
        claimBoxPct: Math.round(claim.getBoundingClientRect().width / innerWidth * 100),
        socialHit: social ? Math.round(social.getBoundingClientRect().width) : null,
        socialIcon: svg ? Math.round(svg.getBoundingClientRect().width) : null,
        heroCta: !!heroCta,
        heroSub: !!document.querySelector('.hero-sub'),
        headCta: !!headCta,
        photosBeforeTimeline: !!(timeline && photoRow) && photoRow.getBoundingClientRect().top < timeline.getBoundingClientRect().top,
        figures, years,
        heroOverflow: contentH > heroH + 2,
      };
    });

    console.log(`\n[${label}]`, JSON.stringify(r, null, 1));
    ok(r.claimUpper === 'uppercase', `${label}: claim no está en mayúsculas`);
    ok(r.claimBoxPct <= 50, `${label}: claim ocupa ${r.claimBoxPct}% (>50%)`);
    ok(r.socialHit >= 44, `${label}: área táctil RRSS = ${r.socialHit}px (mínimo 44)`);
    ok(r.socialIcon >= 26, `${label}: icono RRSS = ${r.socialIcon}px (mínimo 26)`);
    ok(!r.heroCta, `${label}: el CTA del hero sigue presente`);
    ok(!r.heroSub, `${label}: el sub-claim del hero sigue presente`);
    ok(r.headCta, `${label}: falta el CTA arriba de las fotos`);
    ok(r.photosBeforeTimeline, `${label}: el timeline sigue arriba de las fotos`);
    ok(r.figures === 4, `${label}: hay ${r.figures} fotos (esperado 4)`);
    ok(r.years === 0, `${label}: quedan ${r.years} chips de año duplicados`);
    ok(!r.heroOverflow, `${label}: el contenido del hero desborda la pantalla`);
    await ctx.close();
  }

  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Fase 1 verificada: claim en mayúsculas y ≤50%, RRSS 30/52, sin CTA ni sub-claim en el hero, CTA arriba, 4 fotos antes del timeline, 0 años duplicados.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
