// Verificación Fase 2 · directorio de Tiendas.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/tiendas.html`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const base = await page.evaluate(() => {
    const rows = [...document.querySelectorAll('.directory-row')];
    const bgs = [...new Set(rows.map((r) => getComputedStyle(r).backgroundColor))];
    const logos = [...document.querySelectorAll('.tenant-chip img')];
    const heights = [...new Set(logos.map((i) => Math.round(i.getBoundingClientRect().height)))].sort((a, b) => a - b);
    return {
      filas: rows.length,
      fondos: bgs,
      subnav: !!document.querySelector('.tiendas-subnav'),
      filtro: !!document.querySelector('#cat-filter'),
      opciones: document.querySelectorAll('#cat-filter option').length,
      parrafos: document.querySelectorAll('.directory-row-head > p:not(.directory-count)').length,
      chips: logos.length,
      alturas: heights,
      cargados: logos.filter((i) => i.naturalWidth > 0).length,
      fondoPagina: getComputedStyle(document.body).backgroundColor,
      toTop: !!document.querySelector('.to-top'),
    };
  });
  console.log('base:', JSON.stringify(base));
  ok(base.filas === 10, `filas: ${base.filas}`);
  ok(base.fondos.length === 1, `las filas tienen ${base.fondos.length} fondos distintos (esperado 1): ${base.fondos}`);
  ok(!base.fondos.includes('rgb(0, 0, 0)'), 'hay una fila negra');
  ok(!base.subnav, 'sigue el subnav de 11 enlaces');
  ok(base.filtro && base.opciones === 11, `filtro con ${base.opciones} opciones (esperado 11)`);
  ok(base.parrafos === 0, `quedan ${base.parrafos} párrafos de parafraseo`);
  ok(base.alturas.length >= 4, `solo ${base.alturas.length} alturas distintas de logo`);
  ok(base.cargados === 33, `${base.cargados}/33 logos cargados`);
  ok(base.fondoPagina !== 'rgb(255, 255, 255)', `el fondo de página sigue blanco puro`);
  ok(base.toTop, 'falta el botón de volver arriba');

  // filtro funcional
  await page.selectOption('#cat-filter', 'restaurantes');
  await page.waitForTimeout(600);
  const filtrado = await page.evaluate(() => {
    const vis = [...document.querySelectorAll('.directory-row')].filter((r) => !r.hidden);
    return { visibles: vis.length, id: vis[0]?.id };
  });
  console.log('filtrado:', JSON.stringify(filtrado));
  ok(filtrado.visibles === 1 && filtrado.id === 'restaurantes', `el filtro dejó ${filtrado.visibles} fila(s) visibles`);

  // botón volver arriba
  await page.evaluate(() => window.scrollTo(0, 2000));
  await page.waitForTimeout(500);
  const visible = await page.evaluate(() => {
    const b = document.querySelector('.to-top');
    return { visible: b.classList.contains('is-visible'), y: Math.round(window.scrollY) };
  });
  console.log('to-top:', JSON.stringify(visible));
  ok(visible.visible, 'el botón de volver arriba no aparece tras 600px');

  await page.click('.to-top');
  await page.waitForTimeout(1200);
  const yTop = await page.evaluate(() => Math.round(window.scrollY));
  ok(yTop < 40, `tras pulsar volver arriba, scrollY = ${yTop}`);

  // enlace directo por hash
  await page.goto(`${BASE}/tiendas.html#ropa`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(700);
  const hash = await page.evaluate(() => {
    const vis = [...document.querySelectorAll('.directory-row')].filter((r) => !r.hidden);
    return { select: document.getElementById('cat-filter').value, visibles: vis.length, id: vis[0]?.id };
  });
  console.log('hash #ropa:', JSON.stringify(hash));
  ok(hash.select === 'ropa' && hash.visibles === 1, `el hash no preseleccionó la categoría: ${JSON.stringify(hash)}`);

  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Fase 2 (directorio) verificada.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
