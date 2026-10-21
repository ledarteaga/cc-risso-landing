#!/usr/bin/env python3
"""Fase 2 · banda de las 33 marcas en Inicio (TI-02 movido a index.html).

Problema que resuelve: los logos tienen relaciones de aspecto de 0,82 a 11,4.
Con `max-height: 36px` los logos anchos (Western Union una línea, La Cruz)
quedan a 12-13 px de alto y no se leen. Aquí el alto se calcula por logo a
partir de su ancho de tinta, con dos techos:
  - ancho máximo 150 px (168 para los que son una tira, aspecto > 6)
  - alto máximo 56 px
Así los cuadrados y los tiras quedan con el mismo peso óptico.
"""
import json
import math
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOGOS = ROOT / "assets/img/tenants/logos"
BAND = LOGOS / "band"   # versiones @2x para la banda (los originales llegan a 11000 px)
CSS = ROOT / "assets/css/styles.css"
INDEX = ROOT / "index.html"

# Modelo óptico: el tamaño se normaliza por el área de tinta real del logo,
# no por su caja. Un sello con detalle fino necesita más alto que un wordmark
# ancho para pesar lo mismo en la retícula.
TARGET_INK = 50.0   # raíz del área de tinta renderizada, en px
H_MIN, H_MAX = 20, 64
W_MAX = 196         # cabe en la celda de 216 px con su padding

# Marcas destacadas: 12, elegidas por reconocimiento y por cubrir las 10
# categorías. El resto vive en el directorio, al que apunta el CTA.
FEATURED = [
    "PlazaVea_logo_rgb_blanco.png",              # supermercado
    "BCP_logo_blanco.png",                       # banco
    "WesternUnion_logo_2023_Doslineas_blanco.png",  # financiero
    "mcdonalds-wordmark_logo_blanco.png",
    "El_burrito_logo_blanco.png",                # pollo a la brasa
    "canela_logo_blanco.png",                    # café
    "cineplanet_logo_blanco.png",                # cine
    "Nuevo_Fortuna_Casino_logo_blanco.png",      # entretenimiento
    "kayser_logo_blanco.png",                    # ropa
    "platanitos_logo_blanco.png",                # calzado
    "souvenir_sport_logo_lineal_blanco.png",     # deportes
]
W_SPAN2 = 404       # los wordmarks de una línea ocupan dos celdas
WIDE_ASPECT = 8.3   # a partir de aquí el logo ocupa 2 celdas.
                    # 33 logos + 3 anchos = 36 tracks: cuadra exacto en 2, 3 y 6 columnas.


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.rsplit(".", 1)[0].lower()).strip("-")


def ink_area(path):
    """Píxeles realmente pintados (alfa > 10): mide el peso visual, no la caja."""
    im = Image.open(path).convert("RGBA")
    alpha = im.getchannel("A")
    hist = alpha.histogram()
    return sum(hist[11:]) or (im.width * im.height)


def measure(path):
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox() or (0, 0, *im.size)
    x0, y0, x1, y1 = bbox
    return max(1, x1 - x0), max(1, y1 - y0)


BAND.mkdir(exist_ok=True)
rules, chips, meta = [], [], []
for f in [LOGOS / n for n in FEATURED]:
    w, h = measure(f)
    aspect = w / h
    ink_px = ink_area(f)
    # escala s tal que sqrt(área de tinta renderizada) = TARGET_INK
    s = TARGET_INK / math.sqrt(max(1, ink_px))
    height = s * h
    # 11 logos + el wordmark de McDonald's a 2 celdas = 12 tracks exactos.
    wide = aspect > 7.5
    height = max(26, min(H_MAX, height))
    if wide:
        height = 30.0
        if height * aspect > W_SPAN2:
            height = round(W_SPAN2 / aspect, 1)
    elif height * aspect > W_MAX:
        height = W_MAX / aspect
    height = round(height, 1)
    s = slug(f.name)

    # --- versión optimizada: máximo 400 px de ancho (2x del mayor render de 192)
    src = Image.open(f).convert("RGBA")
    target_w = min(src.width, max(200, round(height * aspect * 2)))
    if src.width > target_w:
        src = src.resize((target_w, max(1, round(src.height * target_w / src.width))), Image.LANCZOS)
    out = BAND / f.name
    src.save(out, "PNG", optimize=True)

    rules.append(f'.marca-chip[data-logo="{s}"] img {{ height: {height}px; }}')
    extra = ' marca-chip--wide' if wide else ''
    chips.append(
        f'          <span class="marca-chip{extra}" data-logo="{s}">'
        f'<img src="assets/img/tenants/logos/band/{f.name}" alt="{s.replace("-", " ").title()}" loading="lazy" '
        f'width="{round(height * aspect)}" height="{height}"></span>'
    )
    meta.append({"file": f.name, "slug": s, "ink": [w, h], "aspect": round(aspect, 2), "css_h": height})

sizes = sorted({m["css_h"] for m in meta})
print(f"logos: {len(meta)} · alturas CSS: {sizes}")
print("tiras (aspecto > 6):", [m["slug"] for m in meta if m["aspect"] > 6])

css_block = """
/* ==========================================================================
   TI-02 · BANDA DE LAS 33 MARCAS (Inicio)
   Los altos se calculan por logo: mismo peso óptico, no mismo max-height.
   Generado por scripts/phase2-marcas-band.py — no editar a mano.
   ========================================================================== */
.marca-band {
  background: var(--brand-blue-deep);
  color: var(--fg-on-ink);
  padding-block: var(--pad-band);
}
.marca-band .kicker { color: rgba(255,255,255,0.72); }
.marca-band h2 { max-width: 26ch; margin-top: var(--s-3); color: var(--fg-on-ink); }
/* Flex en vez de grid: así la última fila incompleta queda CENTRADA en vez de
   dejar un hueco a la derecha. */
.marca-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--s-2);
  margin-top: var(--s-8);
}
.marca-chip {
  display: flex; align-items: center; justify-content: center;
  min-height: 96px;
  padding: var(--s-4) var(--s-3);
  flex: 0 0 calc((100% - var(--s-2)) / 2);          /* 2 por fila */
}
.marca-chip img { width: auto; max-width: 100%; object-fit: contain; }
/* El wordmark de McDonald's es 8:1: en una celda quedaría a 24 px de alto. */
.marca-chip--wide { flex: 0 0 calc(2 * ((100% - var(--s-2)) / 2) + var(--s-2)); }
@media (min-width: 640px) {
  .marca-chip { flex: 0 0 calc((100% - 2 * var(--s-2)) / 3); }   /* 3 por fila */
  .marca-chip--wide { flex: 0 0 calc(2 * ((100% - 2 * var(--s-2)) / 3) + var(--s-2)); }
}
@media (min-width: 1024px) {
  .marca-chip { flex: 0 0 calc((100% - 4 * var(--s-2)) / 5); }   /* 5 por fila */
  .marca-chip--wide { flex: 0 0 calc(2 * ((100% - 4 * var(--s-2)) / 5) + var(--s-2)); }
}
@media (min-width: 1280px) {
  .marca-chip { flex: 0 0 calc((100% - 5 * var(--s-2)) / 6); }   /* 6 por fila */
  .marca-chip--wide { flex: 0 0 calc(2 * ((100% - 5 * var(--s-2)) / 6) + var(--s-2)); }
}
/* Los wordmarks de una sola línea (McDonald's, Western Union, La Cruz) ocupan
   dos celdas: a una sola quedarían con 17-24 px de alto y no se leerían. */

.marca-cta { margin-top: var(--s-8); }
.marca-cta .cta-link {
  color: var(--fg-on-ink);
  border-color: var(--brand-green-light);
}
.marca-cta .cta-link:hover { border-color: var(--fg-on-ink); }
""" + "\n".join(rules) + "\n"

text = CSS.read_text()
# idempotente: corta desde el marcador de la banda hasta el final del archivo
MARK = "/* ==========================================================================\n   TI-02 · BANDA"
if MARK in text:
    text = text[:text.index(MARK)].rstrip() + "\n"
CSS.write_text(text.rstrip() + "\n" + css_block)
print("CSS: banda + 33 reglas de tamaño")

section = """
    <!-- ============================================================
         TI-02 · Las 33 marcas del centro (banda movida desde Descuentos)
         ============================================================ -->
    <section class="marca-band" id="marcas" aria-labelledby="marcas-title">
      <div class="container">
        <p class="kicker">Marcas destacadas</p>
        <h2 id="marcas-title">Las que ya conoces, en un solo piso.</h2>
        <div class="marca-grid">
""" + "\n".join(chips) + """
        </div>
        <p class="marca-cta">
          <a href="tiendas.html" class="cta-link is-on-dark">Ver las 33 tiendas del directorio</a>
        </p>
      </div>
    </section>

"""

idx = INDEX.read_text()
if 'id="marcas"' not in idx:
    anchor = "  </main>"
    i = idx.index(anchor)
    idx = idx[:i] + section.lstrip("\n") + idx[i:]
    INDEX.write_text(idx)
    print("index.html: banda insertada antes de </main>")
else:
    print("index.html: la banda ya existía")

json.dump(meta, open("/tmp/marca-band.json", "w"), indent=1, ensure_ascii=False)
