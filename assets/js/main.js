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
  const setHeaderMode = () => {
    if (!header) return;
    // If page is at top and has a transparent hero behind header, set on-dark.
    const hasHero = document.querySelector('.hero');
    if (hasHero && window.scrollY < 80) header.classList.add('is-on-dark');
    else header.classList.remove('is-on-dark');
  };
  if (document.querySelector('.hero')) {
    setHeaderMode();
    window.addEventListener('scroll', setHeaderMode, { passive: true });
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

  /* ---------- Tiendas sub-nav active state on scroll (IntersectionObserver) ---------- */
  const tiendasSubnav = document.querySelector('.tiendas-subnav');
  if (tiendasSubnav) {
    const links = tiendasSubnav.querySelectorAll('a[href^="#"]');
    const targets = Array.from(links).map(a => ({
      link: a,
      el: document.querySelector(a.getAttribute('href'))
    })).filter(t => t.el);

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        // pick the entry closest to the top of the visible area
        const visible = entries
          .filter(e => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        const current = visible[0];
        links.forEach(l => l.classList.remove('is-active'));
        if (current) {
          const match = targets.find(t => t.el === current.target);
          if (match) match.link.classList.add('is-active');
        }
      }, {
        rootMargin: '-130px 0px -55% 0px',   /* trigger band: just below header+subnav, top half of viewport */
        threshold: 0
      });
      targets.forEach(t => observer.observe(t.el));
    } else {
      // fallback: scroll listener (legacy)
      const onScroll = () => {
        const scrollY = window.scrollY + 140;
        let active = null;
        targets.forEach(t => { if (t.el.offsetTop <= scrollY) active = t; });
        links.forEach(l => l.classList.remove('is-active'));
        if (active) active.link.classList.add('is-active');
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }
})();
