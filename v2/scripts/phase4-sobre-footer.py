#!/usr/bin/env python3
"""Fase 4 · Sobre Risso + footer compartido.

SR-02 índice → encabezado · SR-04 protagonismo de "Hoy"
FO-01 grid del footer a 12 columnas, Legal absorbe el copyright
+ nav "Contacto" → "Contáctanos" (CT-01) en las 6 páginas, solo etiqueta.
"""
import pathlib
import re
import sys

# scripts/ -> v2/ (parents[1]). OJO: parents[2] es la raíz del repo, donde viven
# copias legacy del sitio: escribir ahí fue un error que hubo que revertir.
ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ["index", "tiendas", "descuentos", "sobre-risso", "contacto", "libro-reclamaciones"]
fails = []


def note(ok, label):
    print(("  ✓ " if ok else "  ✗ ") + label)
    if not ok:
        fails.append(label)


# ==========================================================================
# FOOTER canónico
# ==========================================================================
FOOTER = '''<footer class="site-footer" role="contentinfo" data-od-id="site-footer">
  <div class="footer-inner">
    <div class="footer-top">

      <div class="footer-brand">
        <img src="assets/img/logo-white.png" alt="Centro Comercial Risso" width="120" height="28">
        <p>Un centro comercial con historia en el corazón de Lince. Más de 50 años reuniendo a vecinos, familias y visitantes en Av. Arequipa 2201.</p>
        <ul class="footer-contact">
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg><span>Av. Arequipa 2201, Lince · Lima</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/></svg><span>Lunes a domingo · 10:00 a 22:00</span></li>
          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/></svg><a href="mailto:contacto@agremsa.pe">contacto@agremsa.pe</a></li>
        </ul>
      </div>

      <nav class="footer-col footer-col--explora" aria-label="Explora">
        <h4>Explora</h4>
        <ul>
          <li><a href="index.html">Inicio</a></li>
          <li><a href="sobre-risso.html">Sobre Risso</a></li>
          <li><a href="descuentos.html">Descuentos</a></li>
          <li><a href="tiendas.html">Tiendas</a></li>
          <li><a href="contacto.html">Contáctanos</a></li>
        </ul>
      </nav>

      <div class="footer-col footer-col--social">
        <h4>Síguenos</h4>
        <ul class="footer-socials">
          <li><a href="https://www.instagram.com/c.c.risso/" target="_blank" rel="noopener" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.9" fill="currentColor" stroke="none"/></svg>
          </a></li>
          <li><a href="https://www.facebook.com/CentroComercialRisso/" target="_blank" rel="noopener" aria-label="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.86.24-1.45 1.47-1.45H16.6V4.43c-.28-.04-1.25-.12-2.38-.12-2.36 0-3.97 1.44-3.97 4.08v2.11H7.75v3h2.5V21h3.25z"/></svg>
          </a></li>
        </ul>
      </div>

      <nav class="footer-col footer-col--legal" aria-label="Legal">
        <h4>Legal</h4>
        <ul>
          <li><a href="libro-reclamaciones.html">Libro de Reclamaciones</a></li>
        </ul>
        <p class="footer-legal-note">© 2026 Centro Comercial Risso<br>Lince, Lima, Perú</p>
      </nav>

    </div>
  </div>
</footer>'''

# ==========================================================================
# 1) Sobre Risso · índice → encabezado, "Hoy" con más peso
# ==========================================================================
s = ROOT / "sobre-risso.html"
t = s.read_text()

toc_re = re.compile(r"    <!-- =+\n         TOC · Índice de capítulos.*?</nav>\n\n", re.S)
m = toc_re.search(t)
note(bool(m), "SR-02 · bloque TOC localizado")
if m:
    t = toc_re.sub('''    <!-- SR-02 · el índice se reemplaza por un encabezado de sección -->
    <section class="beats-intro container" aria-labelledby="capitulos-title">
      <p class="kicker">Tres momentos</p>
      <h2 id="capitulos-title">De la hacienda al Risso de hoy.</h2>
    </section>

''', t)

# "Hoy" con tratamiento de sección real
t = t.replace('<h2 id="hoy-title" class="h2">El mismo lugar, ahora.</h2>',
              '<h2 id="hoy-title">El mismo lugar, ahora.</h2>')
s.write_text(t)
note('class="toc' not in t, "SR-02 · índice eliminado")
note('class="h2"' not in t, "SR-04 · h2 de Hoy sin clase que lo achicaba")

# ==========================================================================
# 2) NAV · Contacto → Contáctanos (solo etiqueta, la URL no se toca)
# ==========================================================================
changed = 0
for name in PAGES:
    p = ROOT / f"{name}.html"
    txt = p.read_text()
    before = txt
    # nav principal y drawer: el texto del enlace hacia contacto.html
    txt = re.sub(r'(<a href="contacto\.html"[^>]*>)\s*Contacto(\s*</a>)', r"\1Contáctanos\2", txt)
    # etiqueta del ancla 04 en Inicio
    txt = txt.replace('<span class="label">Contacto</span>', '<span class="label">Contáctanos</span>')
    if txt != before:
        p.write_text(txt)
        changed += 1
note(changed >= 5, f"CT-01 · etiqueta actualizada en {changed} páginas")

# ==========================================================================
# 3) FOOTER · reemplazo canónico en las 6 páginas
# ==========================================================================
foot_re = re.compile(r"<footer class=\"site-footer\".*?</footer>", re.S)
done = 0
for name in PAGES:
    p = ROOT / f"{name}.html"
    txt = p.read_text()
    if not foot_re.search(txt):
        continue
    txt = foot_re.sub(FOOTER, txt, count=1)
    p.write_text(txt)
    done += 1
note(done == 6, f"FO-01 · footer canónico en {done}/6 páginas")

if fails:
    print("\n✗ Fallaron:", fails)
    sys.exit(1)
print("\nFase 4 (markup) aplicada.")
