// Verificación Fase 2 · directorio de Tiendas.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/tiendas.html`, { waitUntil: 'load' });
  await page.waitForTimeout(600);
  await page.evaluate(() => document.fonts.ready);
  // Las tarjetas bajas usan loading="lazy": sin forzar la carga, contar
  // naturalWidth mide la posición del scroll, no el estado de la página.
  await page.evaluate(() => document.querySelectorAll('img').forEach((i) => { i.loading = 'eager'; }));
  await page.waitForFunction(() => [...document.images].every((i) => i.complete), null, { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(400);

  const base = await page.evaluate(() => {
    const groups = [...document.querySelectorAll('.store-group')];
    const cards = [...document.querySelectorAll('.store-card')];
    const bgs = [...new Set(cards.map((c) => getComputedStyle(c).backgroundColor))];
    const logos = [...document.querySelectorAll('.store-logo img')];
    const heights = [...new Set(logos.map((i) => Math.round(i.getBoundingClientRect().height)))].sort((a, b) => a - b);
    return {
      grupos: groups.length,
      encabezados: groups.map((g) => g.querySelector('h2')?.textContent.trim()),
      conteos: groups.map((g) => g.querySelector('.directory-count')?.textContent.trim()),
      tarjetasPorGrupo: groups.map((g) => g.querySelectorAll('.store-card').length),
      tarjetas: cards.length,
      fondos: bgs,
      subnav: !!document.querySelector('.tiendas-subnav'),
      filtro: !!document.querySelector('#cat-filter'),
      buscador: !!document.querySelector('#store-search'),
      vacio: !!document.querySelector('#directory-empty'),
      opciones: document.querySelectorAll('#cat-filter option').length,
      chips: logos.length,
      alturas: heights,
      cargados: logos.filter((i) => i.naturalWidth > 0).length,
      fondoPagina: getComputedStyle(document.body).backgroundColor,
      columnas: getComputedStyle(document.querySelector('.store-grid')).gridTemplateColumns.split(' ').length,
      logoFiltro: getComputedStyle(logos[0]).filter,
      toTop: !!document.querySelector('.to-top'),
    };
  });
  console.log('base:', JSON.stringify(base));
  ok(base.grupos === 10, `grupos de categoria: ${base.grupos} (esperado 10)`);
  ok(base.tarjetas === 33, `tarjetas de marca: ${base.tarjetas} (esperado 33)`);
  ok(new Set(base.encabezados).size === 10, 'encabezados de categoria repetidos o ausentes');
  ok(base.conteos.every(Boolean), 'alguna categoria sin su conteo');
  ok(base.tarjetasPorGrupo.reduce((a, b) => a + b, 0) === 33,
     `la suma por grupo no da 33: ${base.tarjetasPorGrupo}`);
  ok(base.fondos.length === 1 && base.fondos[0] === 'rgb(255, 255, 255)',
     `las tarjetas deberian ser blancas: ${base.fondos}`);
  ok(!base.subnav, 'sigue el subnav de 11 enlaces');
  ok(base.filtro && base.opciones === 11, `filtro con ${base.opciones} opciones (esperado 11)`);
  ok(base.buscador, 'falta el buscador de tiendas');
  ok(base.vacio, 'falta el estado vacio del directorio');
  ok(base.columnas === 4, `grilla de ${base.columnas} columnas en 1440 (esperado 4)`);
  ok(/invert/.test(base.logoFiltro), `los logos no estan invertidos a tinta: ${base.logoFiltro}`);
  ok(base.alturas.length >= 4, `solo ${base.alturas.length} alturas distintas de logo`);
  ok(base.cargados === 33, `${base.cargados}/33 logos cargados`);
  ok(base.fondoPagina !== 'rgb(255, 255, 255)', 'el fondo de pagina sigue blanco puro');
  ok(base.toTop, 'falta el boton de volver arriba');

  // filtro por categoria: queda un solo grupo, con sus 7 tarjetas
  await page.selectOption('#cat-filter', 'restaurantes');
  await page.waitForTimeout(600);
  const filtrado = await page.evaluate(() => {
    const vis = [...document.querySelectorAll('.store-group')].filter((g) => !g.hidden);
    return { grupos: vis.map((g) => g.id), tarjetas: vis.reduce((n, g) => n + g.querySelectorAll('.store-card:not([hidden])').length, 0) };
  });
  console.log('filtrado:', JSON.stringify(filtrado));
  ok(filtrado.grupos.length === 1 && filtrado.grupos[0] === 'restaurantes' && filtrado.tarjetas === 7,
     `el filtro dejo ${filtrado.grupos.length} grupo(s) y ${filtrado.tarjetas} tarjeta(s)`);

  // buscador: conserva el grupo y su encabezado
  await page.selectOption('#cat-filter', 'all');
  await page.fill('#store-search', 'mcdon');
  await page.waitForTimeout(500);
  const buscado = await page.evaluate(() => {
    const vis = [...document.querySelectorAll('.store-group')].filter((g) => !g.hidden);
    return { grupos: vis.map((g) => g.id), h2: vis.map((g) => g.querySelector('h2').textContent.trim()),
             tarjetas: vis.reduce((n, g) => n + g.querySelectorAll('.store-card:not([hidden])').length, 0),
             status: document.getElementById('filter-status').textContent };
  });
  console.log('buscador "mcdon":', JSON.stringify(buscado));
  ok(buscado.grupos.length === 1 && buscado.grupos[0] === 'restaurantes' && buscado.tarjetas === 1,
     `el buscador dejo ${buscado.grupos.length} grupo(s) y ${buscado.tarjetas} tarjeta(s)`);

  await page.fill('#store-search', 'zzzz');
  await page.waitForTimeout(500);
  const sinResultados = await page.evaluate(() => ({
    grupos: [...document.querySelectorAll('.store-group')].filter((g) => !g.hidden).length,
    vacio: !document.getElementById('directory-empty').hidden }));
  console.log('buscador "zzzz":', JSON.stringify(sinResultados));
  ok(sinResultados.grupos === 0 && sinResultados.vacio, 'el estado vacio no aparece sin resultados');
  await page.fill('#store-search', '');
  await page.waitForTimeout(400);

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
  await page.goto(`${BASE}/tiendas.html#ropa`, { waitUntil: 'load' });
  await page.waitForTimeout(600);
  await page.waitForTimeout(700);
  const hash = await page.evaluate(() => {
    const vis = [...document.querySelectorAll('.store-group')].filter((g) => !g.hidden);
    return { select: document.getElementById('cat-filter').value, grupos: vis.map((g) => g.id),
             tarjetas: vis.reduce((n, g) => n + g.querySelectorAll('.store-card:not([hidden])').length, 0) };
  });
  console.log('hash #ropa:', JSON.stringify(hash));
  ok(hash.select === 'ropa' && hash.grupos.length === 1 && hash.grupos[0] === 'ropa' && hash.tarjetas === 4,
     `el hash no preselecciono la categoria: ${JSON.stringify(hash)}`);

  if (fails.length) { console.log('\n✗ ' + fails.length + ' fallo(s):'); fails.forEach((f) => console.log('  - ' + f)); await browser.close(); process.exit(1); }
  console.log('\n✓ Fase 2 (directorio) verificada.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
