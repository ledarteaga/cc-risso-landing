// Collect computed typography/layout metrics from the live v2 pages.
const { chromium } = require('/Users/ledarteaga/.hermes/hermes-agent/node_modules/playwright');
const BASE = 'http://127.0.0.1:8787';

const pages = ['index', 'tiendas', 'sobre-risso', 'contacto', 'descuentos'];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const out = {};
  for (const name of pages) {
    await page.goto(`${BASE}/${name}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    out[name] = await page.evaluate(() => {
      const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
      const px = (el, p) => el ? parseFloat(getComputedStyle(el)[p]) : null;
      const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return { w: Math.round(b.width), h: Math.round(b.height), top: Math.round(b.top + scrollY) }; };
      const all = (sel) => [...document.querySelectorAll(sel)];
      const res = { vw: innerWidth, docH: document.documentElement.scrollHeight };

      // hero
      const hc = document.querySelector('.hero-claim');
      if (hc) {
        res.heroClaim = {
          fontSize: px(hc, 'fontSize'), lineHeight: px(hc, 'lineHeight'),
          box: r(hc), wrapBox: r(document.querySelector('.hero-claim-wrap')),
          pctOfViewport: Math.round(r(document.querySelector('.hero-claim-wrap')).w / innerWidth * 100),
          text: hc.innerText.replace(/\n/g, ' '),
        };
        const social = document.querySelector('.hero-socials a');
        res.heroSocials = social ? { icon: r(social.querySelector('svg')), hit: r(social), pad: px(document.querySelector('.hero-socials'), 'padding') } : null;
        res.heroCta = document.querySelector('.hero-cta') ? { exists: true, html: document.querySelector('.hero-cta').innerText.trim() } : { exists: false };
        res.heroSub = document.querySelector('.hero-sub') ? { fs: px(document.querySelector('.hero-sub'), 'fontSize'), w: r(document.querySelector('.hero-sub')).w } : null;
      }

      // headings per section
      res.h1 = all('h1').map(e => ({ text: e.innerText.trim().slice(0, 48), fs: px(e, 'fontSize'), lh: px(e, 'lineHeight'), maxW: cs(e, 'maxWidth') }));
      res.h2 = all('h2').map(e => ({
        text: e.innerText.trim().slice(0, 44), fs: px(e, 'fontSize'), weight: cs(e, 'fontWeight'),
        cls: e.className || null, parent: e.parentElement?.className || null, top: r(e).top,
      }));
      res.h3 = all('h3').slice(0, 6).map(e => ({ text: e.innerText.trim().slice(0, 40), fs: px(e, 'fontSize'), cls: e.className }));

      // timeline
      const tl = document.querySelector('.timeline');
      if (tl) {
        res.timeline = {
          rows: all('.timeline-item').length,
          gap: cs(tl, 'gap'), padTop: px(tl, 'paddingTop'), marginTop: px(tl, 'marginTop'),
          years: all('.timeline-item .year').map(e => e.innerText.trim()),
          isAbovePhotos: tl.getBoundingClientRect().top < (document.querySelector('.photo-row')?.getBoundingClientRect().top ?? 1e9),
        };
      }
      // photo row
      const pr = document.querySelector('.photo-row');
      if (pr) res.photoRow = { count: pr.querySelectorAll('figure').length, h: r(pr).h };

      // sections vertical rhythm
      res.sections = all('main > section').map(s => ({
        cls: s.className, pT: px(s, 'paddingTop'), pB: px(s, 'paddingBottom'), h: r(s).h,
      }));

      // footer
      const f = document.querySelector('.site-footer');
      if (f) {
        const top = f.querySelector('.footer-top');
        res.footer = {
          padTop: px(top, 'paddingTop'), padBottom: px(top, 'paddingBottom'),
          cols: all('.footer-col').length,
          brandW: r(f.querySelector('.footer-brand'))?.w,
          colsW: r(f.querySelector('.footer-cols'))?.w,
          gap: cs(top, 'gap'), gridCols: cs(top, 'gridTemplateColumns'),
          socialIcon: r(f.querySelector('.footer-socials svg')),
        };
      }
      // tiendas specifics
      const rows = all('.directory-row');
      if (rows.length) {
        res.directory = {
          rows: rows.length,
          bg: rows.map(x => getComputedStyle(x).backgroundColor),
          classes: rows.map(x => x.className.replace('directory-row', '').trim()),
          chipMaxH: rows[0].querySelector('.tenant-chip img') ? px(rows[0].querySelector('.tenant-chip img'), 'maxHeight') : null,
          chipImgH: rows[0].querySelector('.tenant-chip img') ? r(rows[0].querySelector('.tenant-chip img')).h : null,
          h2: rows[0].querySelector('h2') ? px(rows[0].querySelector('h2'), 'fontSize') : null,
          gridCols: cs(document.querySelector('.directory'), 'gridTemplateColumns'),
        };
        res.subnav = document.querySelector('.tiendas-subnav') ? { h: r(document.querySelector('.tiendas-subnav')).h, sticky: cs(document.querySelector('.tiendas-subnav'), 'position'), items: all('.tiendas-subnav li').length } : null;
      }
      // top-of-page photo band
      const pb = document.querySelector('.photo-band');
      if (pb) res.photoBand = { h: r(pb).h };
      // map
      const map = document.querySelector('.contact-map-frame');
      if (map) res.map = { h: r(map).h, top: r(map).top, inIframe: true };
      // toc
      const toc = document.querySelector('.toc');
      if (toc) res.toc = { items: toc.querySelectorAll('li').length, h: r(toc).h, fs: px(toc.querySelector('a'), 'fontSize') };
      // body copy sizes
      res.bodyCopy = all('p').slice(0, 8).map(p => ({ cls: p.className, fs: px(p, 'fontSize') }));
      return res;
    });
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
