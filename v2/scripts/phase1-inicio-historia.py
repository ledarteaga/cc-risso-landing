#!/usr/bin/env python3
"""Fase 1 · Risso v2 — Inicio e Historia.

IN-01 claim en mayúsculas · IN-02 claim <= 50vw · IN-03 RRSS 24/44
IN-09 quitar CTA del hero · IN-08 fotos antes del timeline · HI-01 4ª foto
HI-02 ritmo · HI-03 sin años duplicados · HI-04 CTA arriba de las fotos
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets/css/styles.css"

fails = []


def edit(path, old, new, label, count=1):
    text = path.read_text()
    if old and new in text and old not in text:
        print(f"  ~ ya aplicado: {label}")
        return
    if text.count(old) < count:
        fails.append(label)
        print(f"  ✗ no encontrado: {label}")
        return
    path.write_text(text.replace(old, new, count))
    print(f"  ✓ {label}")


# ---------------------------------------------------------------- INDEX HTML
edit(INDEX, '          <h1 class="hero-claim">',
     '          <h1 class="hero-claim is-upper">',
     "IN-01 · clase is-upper en el claim")

edit(INDEX,
     '''        <div class="hero-cta">
          <a href="sobre-risso.html" class="cta-link is-on-dark">Conoce nuestra historia</a>
        </div>
''', "", "IN-09 · CTA del hero eliminado")

edit(INDEX,
     '''            <h2 id="anchor-1-title">Una historia que empezó en una hacienda.</h2>
          </div>''',
     '''            <h2 id="anchor-1-title">Una historia que empezó en una hacienda.</h2>
            <a href="sobre-risso.html" class="cta-link anchor-head-cta">Conoce la historia completa</a>
          </div>''',
     "HI-04 · CTA al anchor-head")

# ------------------------------------------------- IN-08 + HI-01 + HI-03
# Reemplaza el bloque completo: timeline arriba + photo-row de 3 + CTA abajo
# por: photo-row de 4 (sin años duplicados) + timeline debajo.
old_block = '''        <!-- Mini-timeline: 4 hitos en columnas -->
        <div class="timeline" role="list">
          <div class="timeline-item" role="listitem">
            <span class="year">S. XIX</span>
            <span class="label">Casa Hacienda</span>
            <span class="blurb">La familia Risso Diggione levanta su casa hacienda en el Fundo Lobatón, en el camino a Lince.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">1966</span>
            <span class="label">Construcción</span>
            <span class="blurb">Arranca la obra del centro comercial, con Todos y Monterrey como primeras tiendas ancla.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">1968</span>
            <span class="label">Apertura</span>
            <span class="blurb">Abre sus puertas con Yompián, Labrousse y Marcantonio entre sus primeras tiendas.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">Hoy</span>
            <span class="label">Renovación</span>
            <span class="blurb">33 tiendas en 10 categorías, en el mismo lugar. Nos renovamos pensando en ti.</span>
          </div>
        </div>
      </div>

      <!-- Diptych: now vs then, full-bleed, alto fijo, sin gap -->
      <div class="photo-row">
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/quienessomos1_MG_4568.jpg" alt="La Casa Hacienda de los Risso Diggione, sobre cuyo solar se construyó el Centro Comercial Risso" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-year">S. XIX</span>
            <span class="photo-row-cap-text">Casa hacienda de los Risso Diggione.</span>
          </figcaption>
        </figure>
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/quienessomos_3.jpg" alt="Centro Comercial Risso recién inaugurado en 1968, con la tienda ancla Monterrey" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-year">1968</span>
            <span class="photo-row-cap-text">Recién inaugurado. Tienda ancla: Monterrey.</span>
          </figcaption>
        </figure>
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/galeria1_MG_4933.jpg" alt="Fachada actual del Centro Comercial Risso sobre Av. Arequipa" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-year">Hoy</span>
            <span class="photo-row-cap-text">La fachada en Av. Arequipa.</span>
          </figcaption>
        </figure>
      </div>

      <div class="container">
        <div class="anchor-foot">
          <a href="sobre-risso.html" class="cta-link">Conoce la historia completa</a>
        </div>
      </div>
'''

new_block = '''      </div>

      <!-- IN-08 + HI-01 · primero la galería (4 fotos), después el timeline.
           HI-03 · el año vive solo en el timeline: los pies de foto lo repiten
           pero como leyenda numerada, sin chip de año duplicado. -->
      <div class="photo-row photo-row--4">
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/quienessomos1_MG_4568.jpg" alt="La Casa Hacienda de los Risso Diggione, sobre cuyo solar se construyó el Centro Comercial Risso" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-text">Casa hacienda de los Risso Diggione.</span>
          </figcaption>
        </figure>
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/quienessomos_3.jpg" alt="Centro Comercial Risso recién inaugurado en 1968, con la tienda ancla Monterrey" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-text">Recién inaugurado. Tienda ancla: Monterrey.</span>
          </figcaption>
        </figure>
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/galeria3_MG_5035.jpg" alt="Galería techada del centro comercial, con tragaluces y locales a ambos lados" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-text">La galería techada, el corazón del recorrido.</span>
          </figcaption>
        </figure>
        <figure class="photo-row-item">
          <img src="assets/img/cc/ccrisso/galeria1_MG_4933.jpg" alt="Fachada actual del Centro Comercial Risso sobre Av. Arequipa" loading="lazy">
          <figcaption class="photo-row-cap">
            <span class="photo-row-cap-text">La fachada en Av. Arequipa.</span>
          </figcaption>
        </figure>
      </div>

      <div class="container">
        <!-- Mini-timeline: 4 hitos en columnas, ahora al cierre del bloque -->
        <div class="timeline" role="list">
          <div class="timeline-item" role="listitem">
            <span class="year">S. XIX</span>
            <span class="label">Casa Hacienda</span>
            <span class="blurb">La familia Risso Diggione levanta su casa hacienda en el Fundo Lobatón, en el camino a Lince.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">1966</span>
            <span class="label">Construcción</span>
            <span class="blurb">Arranca la obra del centro comercial, con Todos y Monterrey como primeras tiendas ancla.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">1968</span>
            <span class="label">Apertura</span>
            <span class="blurb">Abre sus puertas con Yompián, Labrousse y Marcantonio entre sus primeras tiendas.</span>
          </div>
          <div class="timeline-item" role="listitem">
            <span class="year">Hoy</span>
            <span class="label">Renovación</span>
            <span class="blurb">33 tiendas en 10 categorías, en el mismo lugar. Nos renovamos pensando en ti.</span>
          </div>
        </div>
'''

edit(INDEX, old_block, new_block, "IN-08 + HI-01 + HI-03 · fotos → timeline, 4 fotos, sin años duplicados")

# ---------------------------------------------------------------- CSS
# IN-01 · mayúsculas (Futura XBlack en caja alta necesita menos tracking negativo)
edit(CSS,
     """  letter-spacing: -0.025em;
  color: var(--fg-on-ink);
  margin: 0;
  text-shadow: 0 1px 2px rgba(0,0,0,0.45), 0 2px 14px rgba(0,0,0,0.25);   /* subtle legibility shadow over the video */""",
     """  letter-spacing: -0.005em;   /* IN-01: caja alta — menos tracking negativo para que no se toquen */
  color: var(--fg-on-ink);
  margin: 0;
  text-shadow: 0 1px 2px rgba(0,0,0,0.45), 0 2px 14px rgba(0,0,0,0.25);   /* subtle legibility shadow over the video */""",
     "IN-01 · tracking del claim")

edit(CSS, ".hero-claim-wrap {\n  max-width: clamp(360px, 72vw, 1100px);",
     ".hero-claim-wrap {\n  max-width: min(50vw, 720px);   /* IN-02: el claim nunca supera la mitad del ancho */",
     "IN-02 · claim a 50vw")

edit(CSS, ".hero-socials a {\n  display: inline-flex; align-items: center; justify-content: center;\n  width: 32px; height: 32px;",
     ".hero-socials a {\n  display: inline-flex; align-items: center; justify-content: center;\n  width: 44px; height: 44px;   /* IN-03: mínimo táctil WCAG 2.5.5 */",
     "IN-03 · hit area 44px")

edit(CSS, ".hero-socials svg { width: 18px; height: 18px; }",
     ".hero-socials svg { width: 24px; height: 24px; }   /* IN-03 */",
     "IN-03 · icono 24px")

# IN-09 · la regla del CTA del hero ya no aplica
edit(CSS, ".hero-cta { margin-top: var(--s-7); display: flex; gap: var(--s-5); flex-wrap: wrap; opacity: 1; transform: none; }",
     "/* IN-09: .hero-cta eliminado — el acceso a la historia vive en el ancla 01 y el navbar */",
     "IN-09 · regla del CTA retirada")

# HI-04 · CTA dentro del anchor-head
edit(CSS, ".anchor .photo-row { margin-top: clamp(28px, 3.5vw, 48px); }",
     """.anchor .photo-row { margin-top: clamp(28px, 3.5vw, 48px); }
.anchor-head-cta { display: inline-block; margin-top: var(--s-5); }   /* HI-04 */""",
     "HI-04 · estilo del CTA en el head")

if fails:
    print("\n✗ Fallaron:", fails)
    sys.exit(1)
print("\nFase 1 aplicada.")
