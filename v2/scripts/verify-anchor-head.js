// Verifica el layout del encabezado de banda (anchor-head):
// 1) el divisor del texto cae exactamente en el 50% del contenedor
// 2) el cuerpo de la derecha arranca a la misma altura que el h2
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');

(async () => {
  const browser = await chromium.launch();
  const fails = [];
  for (const [w, label] of [[1440, 'desktop'], [1200, 'laptop'], [390, 'mobile']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 950 } });
    const page = await ctx.newPage();
    await page.goto('http://127.0.0.1:8787/index.html', { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);

    const out = await page.evaluate(() => {
      const heads = [...document.querySelectorAll('.anchor-head')];
      return heads.map((h) => {
        const c = h.getBoundingClientRect();
        const p = h.querySelector('p');
        const h2 = h.querySelector('h2');
        const pr = p.getBoundingClientRect();
        const hr = h2.getBoundingClientRect();
        return {
          divisorPct: +(((pr.left - c.left) / c.width) * 100).toFixed(1),
          pTop: Math.round(pr.top),
          h2Top: Math.round(hr.top),
          deltaTop: Math.round(pr.top - hr.top),
          pFirstLine: Math.round(parseFloat(getComputedStyle(p).fontSize) * 1.5),
          pBeforeH2: pr.top < hr.top - 2,
        };
      });
    });

    out.forEach((r, i) => {
      console.log(`${label} anchor${i + 1}: divisor=${r.divisorPct}%  pTop-h2Top=${r.deltaTop}px`);
      if (label !== 'mobile') {
        if (Math.abs(r.divisorPct - 50) > 1.5) fails.push(`${label} anchor${i + 1}: divisor en ${r.divisorPct}% (esperado 50%)`);
        if (Math.abs(r.deltaTop) > 3) fails.push(`${label} anchor${i + 1}: el cuerpo arranca ${r.deltaTop}px respecto del h2`);
      }
    });
    await ctx.close();
  }
  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Encabezados alineados: divisor al 50% y cuerpo a la altura del h2.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
