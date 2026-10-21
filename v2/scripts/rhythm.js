// Audit vertical rhythm: padding-block per section + horizontal container edges
// across all pages, including the footer. Fails loudly on discrepancies.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8787';
const PAGES = ['index', 'tiendas', 'descuentos', 'sobre-risso', 'contacto', 'libro-reclamaciones'];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const report = {};

  for (const name of PAGES) {
    await page.goto(`${BASE}/${name}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);

    report[name] = await page.evaluate(() => {
      const px = (v) => Math.round(parseFloat(v) || 0);
      const cs = (el) => getComputedStyle(el);
      const box = (el) => { const b = el.getBoundingClientRect(); return { left: Math.round(b.left), right: Math.round(innerWidth - b.right), w: Math.round(b.width) }; };

      const sections = [...document.querySelectorAll('main > section, body > footer')].map((s) => ({
        sel: s.tagName.toLowerCase() + (s.className ? '.' + String(s.className).trim().split(/\s+/).join('.') : ''),
        padTop: px(cs(s).paddingTop),
        padBottom: px(cs(s).paddingBottom),
        marginTop: px(cs(s).marginTop),
        marginBottom: px(cs(s).marginBottom),
      }));

      // inner vertical spacing: direct children of main sections (title -> content rhythm)
      const inner = [...document.querySelectorAll('main > section > .container, main > section > .directory, main > section > .photo-row')]
        .slice(0, 8)
        .map((c) => ({
          parent: c.parentElement.className,
          padTop: px(cs(c).paddingTop),
          padBottom: px(cs(c).paddingBottom),
          children: [...c.children].slice(0, 4).map((k) => ({
            tag: k.tagName.toLowerCase() + (k.className ? '.' + String(k.className).trim().split(/\s+/)[0] : ''),
            mt: px(cs(k).marginTop), mb: px(cs(k).marginBottom),
          })),
        }));

      const footer = document.querySelector('.site-footer');
      const footerInner = document.querySelector('.footer-inner');
      const fTop = document.querySelector('.footer-top');
      const fBottom = document.querySelector('.footer-bottom');
      const firstContainer = document.querySelector('main .container');

      return {
        sections,
        inner,
        footer: {
          padTop: px(cs(footer).paddingTop),
          padBottom: px(cs(footer).paddingBottom),
          innerPadLeft: px(cs(footerInner).paddingLeft),
          innerPadRight: px(cs(footerInner).paddingRight),
          innerMaxW: cs(footerInner).maxWidth,
          topGap: px(cs(fTop).gap),
          topGapRow: cs(fTop).rowGap,
          bottomMarginTop: px(cs(fBottom).marginTop),
          bottomPadTop: px(cs(fBottom).paddingTop),
          bottomPadBottom: px(cs(fBottom).paddingBottom),
          edge: box(footerInner),
        },
        mainEdge: firstContainer ? box(firstContainer) : null,
        mainPadLeft: firstContainer ? px(cs(firstContainer).paddingLeft) : null,
      };
    });
  }

  // ---- analysis
  const allSectionPads = [];
  console.log('=== padding-block por sección (desktop 1440) ===');
  for (const [pageName, r] of Object.entries(report)) {
    for (const s of r.sections) {
      allSectionPads.push(s.padTop);
      console.log(`  ${pageName.padEnd(20)} ${s.sel.slice(0, 58).padEnd(58)} top=${String(s.padTop).padStart(3)} bottom=${String(s.padBottom).padStart(3)}`);
    }
  }

  const counts = {};
  allSectionPads.forEach((v) => { counts[v] = (counts[v] || 0) + 1; });
  console.log('\n=== valores distintos de padding-top en secciones ===');
  Object.entries(counts).sort((a, b) => b[1] - a[1]).forEach(([v, n]) => console.log(`  ${v}px x${n}`));

  console.log('\n=== bordes del contenedor vs footer ===');
  for (const [pageName, r] of Object.entries(report)) {
    console.log(`  ${pageName.padEnd(20)} main.left=${r.mainEdge?.left} right=${r.mainEdge?.right} | footer.left=${r.footer.edge.left} right=${r.footer.edge.right} | footer.innerPad=${r.footer.innerPadLeft}/${r.footer.innerPadRight}`);
  }

  const f = report.index.footer;
  console.log('\n=== footer ===');
  console.log(`  padding: ${f.padTop}px arriba / ${f.padBottom}px abajo`);
  console.log(`  footer-top gap: ${f.topGap}`);
  console.log(`  footer-bottom: margin-top ${f.bottomMarginTop} / padding-top ${f.bottomPadTop} / padding-bottom ${f.bottomPadBottom}`);
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
