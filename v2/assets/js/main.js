/* ==========================================================================
   main.js — Risso v2 · shared interactivity
   No frameworks. Vanilla JS, IIFE pattern.
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Header scroll state (transparent → solid) ---------- */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => {
      if (window.scrollY > 32) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Mobile drawer (a11y: dialog + focus restoration, impeccable 2026-10) ---------- */
  const drawer = document.querySelector('.mobile-drawer');
  const menuBtn = document.querySelector('.menu-btn');
  const drawerClose = document.querySelector('.drawer-close');
  if (drawer && menuBtn) {
    let lastFocus = null;
    const open = () => {
      if (drawer.classList.contains('is-open')) return;  /* idempotent */
      lastFocus = document.activeElement;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      menuBtn.setAttribute('aria-label', 'Cerrar menú');
      document.body.style.overflow = 'hidden';
      drawer.querySelector('a')?.focus();
    };
    const close = () => {
      if (!drawer.classList.contains('is-open')) return;  /* idempotent */
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-label', 'Abrir menú');
      document.body.style.overflow = '';
      /* Restore focus to the element that opened the drawer (standard dialog pattern) */
      if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
      else menuBtn.focus();
    };
    menuBtn.addEventListener('click', open);
    drawerClose?.addEventListener('click', close);
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* ---------- Hero video: graceful fallback when AV1 unsupported ---------- */
  const video = document.querySelector('.hero-video');
  if (video) {
    // If the browser can't play AV1 in MP4, swap to H.264 source.
    // (We declare both sources in HTML, but as an additional belt-and-suspenders:
    // browsers usually pick the first one they support, so this just nudges them.)
    video.addEventListener('error', () => {
      const sources = video.querySelectorAll('source');
      sources.forEach(s => {
        if (s.dataset.format === 'av1') s.remove();
      });
      video.load();
    }, true);
    // Pause when out of viewport (perf) — but only on small screens where the
    // video isn't the dominant hero element. Skip for now to keep audio/visual continuity.
  }

  /* ---------- Wizard (Contacto multistep) ---------- */
  const wizard = document.querySelector('[data-wizard]');
  if (wizard) {
    const panes = wizard.querySelectorAll('.wizard-pane');
    const steps = wizard.querySelectorAll('.wizard-step');
    const stepperIndex = wizard.querySelectorAll('[data-step]');

    const goTo = (n) => {
      panes.forEach(p => p.classList.toggle('is-active', Number(p.dataset.pane) === n));
      steps.forEach(s => {
        const sn = Number(s.dataset.step);
        s.classList.toggle('is-active', sn === n);
        s.classList.toggle('is-done', sn < n);
      });
      stepperIndex.forEach(b => {
        b.dataset.active = Number(b.dataset.step) === n ? 'true' : 'false';
      });
      wizard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    // Step 1 → Step 2
    const frenteCards = wizard.querySelectorAll('.frente-card');
    const frenteInput = wizard.querySelector('#frente-input');
    frenteCards.forEach(card => {
      card.addEventListener('click', () => {
        frenteCards.forEach(c => c.classList.remove('is-selected'));
        card.classList.add('is-selected');
        if (frenteInput) frenteInput.value = card.dataset.frente;
        // Toggle form panels per frente
        const panels = wizard.querySelectorAll('[data-frente-panel]');
        panels.forEach(p => {
          p.style.display = (p.dataset.frentePanel === card.dataset.frente) ? '' : 'none';
        });
      });
    });
    const next1 = wizard.querySelector('[data-action="next-1"]');
    next1?.addEventListener('click', () => {
      if (!frenteInput?.value) {
        wizard.querySelector('#step1-error').textContent = 'Elige un frente para continuar.';
        return;
      }
      wizard.querySelector('#step1-error').textContent = '';
      goTo(2);
    });

    // Step 2 → Step 3 (validate)
    const validateField = (field) => {
      const input = field.querySelector('input, select, textarea');
      if (!input || !input.required) return true;
      const ok = input.value.trim().length > 0;
      field.classList.toggle('is-error', !ok);
      return ok;
    };
    const next2 = wizard.querySelector('[data-action="next-2"]');
    next2?.addEventListener('click', () => {
      const step2 = wizard.querySelector('[data-pane="2"]');
      // Only validate fields within the currently visible panel
      const visiblePanel = step2.querySelector('[data-frente-panel]:not([style*="display: none"])')
                         || step2.querySelector('[data-frente-panel]');
      const fields = visiblePanel ? visiblePanel.querySelectorAll('.field') : step2.querySelectorAll('.field');
      let allOk = true;
      fields.forEach(f => { if (!validateField(f)) allOk = false; });
      if (!allOk) return;
      // Capture summary (only from visible panel)
      const sum = wizard.querySelector('#confirm-summary');
      if (sum) {
        const data = [];
        fields.forEach(f => {
          const input = f.querySelector('input, select, textarea');
          const lbl = f.querySelector('label')?.textContent || '';
          if (input && input.value.trim()) data.push({ lbl, val: input.value.trim() });
        });
        sum.innerHTML = data.map(d => `<p><strong>${d.lbl}:</strong> ${d.val}</p>`).join('');
      }
      goTo(3);
    });

    const back2 = wizard.querySelector('[data-action="back-2"]');
    back2?.addEventListener('click', () => goTo(1));

    const reset = wizard.querySelector('[data-action="reset"]');
    reset?.addEventListener('click', () => {
      wizard.querySelectorAll('input, select, textarea').forEach(i => i.value = '');
      wizard.querySelectorAll('.field').forEach(f => f.classList.remove('is-error'));
      wizard.querySelectorAll('.frente-card').forEach(c => c.classList.remove('is-selected'));
      wizard.querySelectorAll('[data-frente-panel]').forEach(p => p.style.display = '');
      goTo(1);
    });

    // stepperIndex: clicking on completed steps jumps back
    stepperIndex.forEach(s => {
      s.addEventListener('click', () => {
        const n = Number(s.dataset.step);
        if (s.classList.contains('is-done') || s.classList.contains('is-active')) goTo(n);
      });
    });
  }

  /* ---------- Libro de Reclamaciones: tipo selector ---------- */
  const tipoLabels = document.querySelectorAll('.reclamo-type label');
  if (tipoLabels.length) {
    tipoLabels.forEach(l => {
      l.addEventListener('click', () => {
        tipoLabels.forEach(x => x.classList.remove('is-selected'));
        l.classList.add('is-selected');
        l.querySelector('input').checked = true;
      });
    });
  }

  /* ---------- Header on-dark auto-detect ---------- */
  /* Pages that open on a dark surface start with .is-on-dark in the markup.
     Keep them in dark mode only while the header still sits over that surface,
     using the same 32px threshold as .is-scrolled so the two states never
     overlap (which used to leave a white logo on the white scrolled bar). */
  if (header && header.classList.contains('is-on-dark')) {
    const setHeaderMode = () => {
      header.classList.toggle('is-on-dark', window.scrollY <= 32);
    };
    setHeaderMode();
    window.addEventListener('scroll', setHeaderMode, { passive: true });
  }

  /* ---------- Brand logo: back to the top of the hero (Inicio only) ---------- */
  const brand = document.querySelector('.site-header .brand');
  if (brand && document.querySelector('.hero')) {
    brand.addEventListener('click', e => {
      const target = new URL(brand.href, window.location.href);
      if (target.pathname === window.location.pathname && target.search === window.location.search) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        if (window.location.hash) history.replaceState(null, '', window.location.pathname + window.location.search);
      }
    });
  }

  /* ---------- Smooth scroll for in-page anchors ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id.length > 1) {
        const t = document.querySelector(id);
        if (t) {
          e.preventDefault();
          t.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.replaceState(null, '', id);
        }
      }
    });
  });

  /* ---------- TD-01 · buscador + filtro del directorio de tiendas ---------- */
  const catFilter = document.getElementById('cat-filter');
  if (catFilter) {
    const cards = Array.from(document.querySelectorAll('.store-card'));
    const search = document.getElementById('store-search');
    const status = document.getElementById('filter-status');
    const empty = document.getElementById('directory-empty');

    /* Cada tarjeta es una marca: se filtra por categoria (data-cat) y por
       nombre, leyendo el alt del logo. */
    const render = ({ scroll = false } = {}) => {
      const cat = catFilter.value;
      const q = (search?.value || '').trim().toLowerCase();
      let visibles = 0;
      cards.forEach((card) => {
        const name = (card.querySelector('img')?.alt || '').toLowerCase();
        const okCat = cat === 'all' || card.dataset.cat === cat;
        const okQ = !q || name.includes(q);
        card.hidden = !(okCat && okQ);
        if (!card.hidden) visibles += 1;
      });
      if (empty) empty.hidden = visibles !== 0;
      if (status) {
        status.textContent = (q || cat !== 'all')
          ? `${visibles} ${visibles === 1 ? 'tienda' : 'tiendas'}`
          : '';
      }
      if (scroll) {
        const y = document.getElementById('directory').getBoundingClientRect().top + window.scrollY - 88;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
      return visibles;
    };

    catFilter.addEventListener('change', () => render({ scroll: true }));

    if (search) {
      search.addEventListener('input', () => {
        if (catFilter.value !== 'all') catFilter.value = 'all';
        render();
      });
      search.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') { search.value = ''; render(); }
      });
    }

    /* Enlace directo (#restaurantes, #ropa…): preselecciona la categoria */
    const fromHash = () => {
      const id = location.hash.replace('#', '');
      if (!id) return;
      if ([...catFilter.options].some((o) => o.value === id)) {
        catFilter.value = id;
        render({ scroll: true });
      }
    };
    fromHash();
    window.addEventListener('hashchange', fromHash);
    window.addEventListener('pageshow', fromHash);
  }

  /* ---------- TD-06 · botón de volver arriba ---------- */
  (() => {
    if (document.querySelector('.to-top')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'to-top';
    btn.setAttribute('aria-label', 'Volver arriba');
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="6"/><polyline points="5 12 12 5 19 12"/></svg>';
    document.body.appendChild(btn);

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const toggle = () => btn.classList.toggle('is-visible', window.scrollY > 600);
    window.addEventListener('scroll', toggle, { passive: true });
    toggle();

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      const first = document.querySelector('.skip-link') || document.body;
      if (first.focus) first.focus({ preventScroll: true });
    });
  })();

})();
