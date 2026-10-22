// Fase 5 · verificación transversal: mobile, desbordes y contraste WCAG.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');

const BASE = 'http://127.0.0.1:8787';
const PAGES = ['index', 'tiendas', 'descuentos', 'sobre-risso', 'contacto', 'como-llegar', 'libro-reclamaciones'];
const VIEWPORTS = [
  { w: 390, h: 844, label: 'mobile' },
  { w: 768, h: 1024, label: 'tablet' },
  { w: 1024, h: 768, label: 'small-laptop' },
  { w: 1440, h: 900, label: 'desktop' },
];

function lum(rgb) {
  const [r, g, b] = rgb.map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function ratio(a, b) {
  const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
  return +((l1 + 0.05) / (l2 + 0.05)).toFixed(2);
}

(async () => {
  const browser = await chromium.launch();
  const fails = [];

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await ctx.newPage();
    for (const name of PAGES) {
      await page.goto(`${BASE}/${name}.html`, { waitUntil: 'domcontentloaded' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(250);

      const r = await page.evaluate(() => {
        const de = document.documentElement;
        // desborde horizontal real: algún elemento más ancho que el viewport
        const overflowing = [...document.querySelectorAll('body *')]
          .filter((el) => {
            const b = el.getBoundingClientRect();
            return b.width > 0 && (b.right > innerWidth + 2 || b.left < -2);
          })
          .slice(0, 3)
          .map((el) => el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0]);

        // contraste de texto sobre su fondo efectivo
        const parse = (c) => (c.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
        const bgOf = (el) => {
          let n = el;
          while (n && n !== document.documentElement) {
            const bg = getComputedStyle(n).backgroundColor;
            if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return parse(bg);
            n = n.parentElement;
          }
          return [255, 255, 255];
        };
        const samples = [...document.querySelectorAll('h1, h2, h3, p, a, li')]
          .filter((el) => el.textContent.trim().length > 2 && el.offsetParent !== null)
          // Texto sobre imagen / video / degradado: el contraste real depende del
          // píxel de fondo, no se puede medir con getComputedStyle. Se audita aparte.
          .filter((el) => !el.closest('.hero, .site-header, .page-open, .photo-band, .marca-band, [role="img"]'))
          .slice(0, 120)
          .map((el) => {
            const cs = getComputedStyle(el);
            return {
              sel: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
              fg: parse(cs.color),
              bg: bgOf(el),
              size: parseFloat(cs.fontSize),
              weight: cs.fontWeight,
              text: el.textContent.trim().slice(0, 30),
            };
          });
        return { scrollW: de.scrollWidth, innerW: innerWidth, overflowing, samples };
      });

      if (r.scrollW > r.innerW + 2) {
        fails.push(`${vp.label}/${name}: desborde horizontal (${r.scrollW} > ${r.innerW}) ${JSON.stringify(r.overflowing)}`);
      }

      // contraste: AA normal 4.5, AA grande 3.0 (>=24px o >=18.66px bold)
      const malos = [];
      for (const s of r.samples) {
        const large = s.size >= 24 || (s.size >= 18.66 && parseInt(s.weight) >= 700);
        const need = large ? 3 : 4.5;
        const ratio_ = ratio(s.fg, s.bg);
        if (ratio_ < need) malos.push(`${s.sel} "${s.text}" ${ratio_}:1 (min ${need})`);
      }
      if (malos.length) fails.push(`${vp.label}/${name}: contraste → ${malos.slice(0, 3).join(' | ')}`);

      console.log(`${vp.label.padEnd(13)} ${name.padEnd(21)} scroll=${r.scrollW} ok=${r.scrollW <= r.innerW + 2} contraste=${malos.length === 0 ? 'ok' : malos.length + ' fallos'}`);
    }
    await ctx.close();
  }

  if (fails.length) {
    console.log(`\n✗ ${fails.length} problema(s):`);
    fails.forEach((f) => console.log('  - ' + f));
    await browser.close();
    process.exit(1);
  }
  console.log('\n✓ Fase 5: sin desbordes y contraste AA en 7 páginas × 4 anchos.');
  await browser.close();
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
