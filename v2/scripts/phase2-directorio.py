#!/usr/bin/env python3
"""Fase 2 · Directorio de Tiendas.

TI-01 todas las cajas en azul marca · TD-01 filtro desplegable en vez de subnav
TD-02/TD-05 fuera el negro y el código de color · TD-03 tamaños de logo por
peso visual (área de tinta) · TD-04 fondo blando · TD-07 copy sin parafraseo.

Reescribe el directorio de tiendas.html a partir de la estructura actual
(ids, títulos y logos) y añade el CSS. Idempotente por bloques marcados.
"""
import json
import math
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIENDAS = ROOT / "tiendas.html"
CSS = ROOT / "assets/css/styles.css"
LOGOS = ROOT / "assets/img/tenants/logos/band"

TARGET_INK = 46.0     # raíz del área de tinta renderizada, en px
H_MIN, H_MAX = 24, 54
W_MAX, W_MAX_STRIP = 140, 180   # los wordmarks de una línea necesitan más ancho


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.rsplit(".", 1)[0].lower()).strip("-")


def metrics(path):
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox() or (0, 0, *im.size)
    w, h = max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])
    ink = sum(im.getchannel("A").histogram()[11:]) or (im.width * im.height)
    return w, h, ink


sizes, rules = {}, []
for f in LOGOS.glob("*.png"):
    w, h, ink = metrics(f)
    aspect = w / h
    height = TARGET_INK / math.sqrt(ink) * h
    # Un wordmark de 8:1 o más se lee por el alto de la letra: se le da ancho
    # extra en vez de dejarlo caer a 13 px.
    wmax = W_MAX_STRIP if aspect > 7 else W_MAX
    height = max(H_MIN, min(H_MAX, height))
    if height * aspect > wmax:
        height = wmax / aspect
    height = max(round(height, 1), 18)
    height = round(height, 1)
    s = slug(f.name)
    sizes[s] = height
    rules.append(f'.store-logo img[data-logo="{s}"] {{ height: {height}px; }}')

# ---------------------------------------------------------------- HTML
html = TIENDAS.read_text()

rows = re.findall(
    r'<div class="directory-row[^"]*" id="([^"]+)"[^>]*>\s*'
    r'<div class="directory-row-head">\s*<h2([^>]*)>(.*?)</h2>\s*(?:<p[^>]*>.*?</p>)?\s*</div>\s*'
    r'<div class="directory-tenants">(.*?)</div>',
    html, re.S)
print("filas encontradas:", len(rows))

blocks = []
cat_titles = {cat_id: title for cat_id, _, title, _ in rows}
total = 0
for cat_id, h2_attrs, title, tenants in rows:
    logos = re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', tenants)
    for src, alt in logos:
        name = src.rsplit("/", 1)[-1]
        s = slug(name)
        total += 1
        blocks.append(f'''          <li class="store-card" data-cat="{cat_id}">
            <span class="store-logo"><img src="{src}" alt="{alt}" data-logo="{s}" loading="lazy"></span>
            <span class="store-cat">{title}</span>
          </li>''')
print("tarjetas de marca:", len(blocks))

empty_state = ('\n\n        <p class="directory-empty" id="directory-empty" hidden>'
               'No encontramos esa tienda. Prueba con otra palabra o cambia la categoría.</p>')
directorio = ("      <ul class=\"directory\" id=\"directory\">\n"
              + "\n".join(blocks) + empty_state + "\n      </ul>")

# reemplaza el bloque .directory completo
start = html.index('<div class="directory"')
end = html.index("    </section>", start)
html = html[:start] + directorio + "\n" + html[end:]

# ---------------------------------------------------------------- filtro
options = ['            <option value="all">Todas las categorías ({})</option>'.format(len(blocks))]
for cat_id, _, title, tenants in rows:
    n = len(re.findall(r"<img", tenants))
    options.append(f'          <option value="{cat_id}">{title} ({n})</option>')

filtro = '''    <!-- TD-01 · filtro desplegable + buscador -->
    <div class="directory-filter" role="search">
      <div class="directory-filter-inner">
        <div class="filter-field filter-field--search">
          <label class="sr-only" for="store-search">Buscar tienda por nombre</label>
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
          <input type="search" id="store-search" class="store-search" placeholder="Buscar tienda" autocomplete="off" aria-controls="directory">
        </div>
        <div class="filter-field">
          <label class="sr-only" for="cat-filter">Filtrar por categoría</label>
          <div class="select-wrap">
            <select id="cat-filter" class="cat-select" aria-label="Filtrar el directorio por categoría">
''' + "\n".join(options) + '''
            </select>
            <svg class="select-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
        <p class="filter-status" id="filter-status" role="status" aria-live="polite"></p>
      </div>
    </div>

'''

subnav_re = re.compile(r'    <!-- =+\n         SUB-NAV · sticky anchor jump\n.*?</nav>\n\n', re.S)
filtro_re = re.compile(r'    <!-- TD-01 · filtro desplegable[^\n]*-->\n    <div class="directory-filter".*?\n    </div>\n\n', re.S)
if subnav_re.search(html):
    html = subnav_re.sub(filtro, html)
    print("subnav → filtro")
elif filtro_re.search(html):
    html = filtro_re.sub(filtro, html)
    print("filtro existente → filtro con buscador")
else:
    print("AVISO: no encontré ni subnav ni filtro")

TIENDAS.write_text(html)

# ---------------------------------------------------------------- CSS
css = CSS.read_text()
MARK = "/* ==========================================================================\n   FASE 2 · DIRECTORIO DE TIENDAS"
if MARK in css:
    css = css[:css.index(MARK)].rstrip() + "\n"

block = MARK + """
   Variante B (aprobada): mosaico de 2 columnas sobre fondo blando. Cada
   categoría es una tarjeta con altura según contenido; el azul de marca se
   mantiene como superficie y la separación es espacial, no cromática.
   El conteo aparece UNA vez, en línea con el título (sin badge ni segunda
   numeración).
   ========================================================================== */
.tiendas-page body { background: #F4F7FC; }

/* Grilla de marcas: una tarjeta por tienda. 2 en móvil, 3 en tablet,
   4 desde 1100px. La categoria va como meta al pie de la tarjeta. */
.directory {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  align-items: stretch;
  list-style: none;
  padding: 0;
  margin: 0;
}
@media (min-width: 720px) {
  .directory { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
}
@media (min-width: 1100px) {
  .directory { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
}

.store-card {
  position: relative;
  background: #fff;
  border: 1px solid rgba(43,88,168,0.16);
  box-shadow: 0 1px 2px rgba(10,10,20,0.04);
  display: flex;
  flex-direction: column;
  gap: var(--s-4);
  padding: clamp(18px, 1.6vw, 24px) clamp(14px, 1.4vw, 20px);
  min-height: 148px;
  transition: border-color var(--t-base) var(--ease-out), transform var(--t-base) var(--ease-out);
}
.store-card::before {
  content: "";
  position: absolute; left: 0; top: 0; height: 3px; width: 100%;
  background: var(--brand-blue);
}
.store-card:hover { border-color: rgba(43,88,168,0.4); transform: translateY(-1px); }
.store-card[hidden] { display: none; }

.store-logo {
  flex: 1 1 auto;
  display: flex; align-items: center; justify-content: center;
  padding-block: var(--s-2);
}
/* Los 33 logos son blancos: sobre tarjeta blanca se invertían a nada.
   filter los lleva a tinta sin tocar los archivos. */
.store-logo img {
  width: auto; max-width: 100%; object-fit: contain;
  filter: invert(1) brightness(0.18);
}
.store-cat {
  flex: none;
  font-size: var(--fs-caption);
  letter-spacing: var(--track-caps);
  text-transform: uppercase;
  color: var(--brand-blue);
  opacity: 0.8;
  padding-top: var(--s-3);
  border-top: 1px solid var(--border);
}
/* ---- TD-01 · filtro desplegable ---- */
.directory-filter {
  position: sticky; top: 72px; z-index: calc(var(--z-nav) - 1);
  background: rgba(244,247,252,0.94);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  padding-block: var(--s-3);
}
.directory-filter-inner {
  max-width: var(--maxw-content);
  margin-inline: auto;
  padding-inline: var(--gutter);
  display: flex; align-items: center; gap: var(--s-4); flex-wrap: wrap;
}
.directory-filter .kicker { color: var(--fg-muted); margin: 0; }
.filter-field { display: flex; align-items: center; gap: var(--s-3); }
.filter-field--search { position: relative; flex: 1 1 260px; min-width: 200px; }
.select-wrap { position: relative; flex: 0 1 280px; min-width: 220px; }

.store-search {
  width: 100%;
  font: inherit; font-size: var(--fs-body);
  color: var(--fg);
  background: var(--ground);
  border: 1px solid var(--border-strong);
  border-radius: var(--r-sm);
  padding: var(--s-3) var(--s-4) var(--s-3) var(--s-9);
  appearance: none;
}
.store-search::placeholder { color: var(--fg-muted); }
.store-search:focus-visible { outline: 2px solid var(--brand-green-deep); outline-offset: 2px; }
.search-icon {
  position: absolute; left: var(--s-4); top: 50%; transform: translateY(-50%);
  width: 17px; height: 17px; color: var(--fg-muted); pointer-events: none;
}
.filter-status {
  margin: 0; margin-left: auto;
  font-size: var(--fs-caption);
  letter-spacing: var(--track-caps); text-transform: uppercase;
  color: var(--fg-muted);
}
.filter-status:empty { display: none; }

/* Estado vacío del directorio */
.directory-empty {
  grid-column: 1 / -1;
  padding: var(--s-7) var(--s-4);
  text-align: center;
  font-size: var(--fs-body); color: var(--fg-muted);
  border: 1px dashed var(--border-strong);
}
.directory-empty[hidden] { display: none; }
.cat-select {
  width: 100%;
  appearance: none;
  font: inherit;
  font-size: var(--fs-body);
  font-weight: 600;
  color: var(--fg);
  background: var(--ground);
  border: 1px solid var(--border-strong);
  border-radius: var(--r-sm);
  padding: var(--s-3) var(--s-8) var(--s-3) var(--s-4);
  cursor: pointer;
}
.cat-select:focus-visible { outline: 2px solid var(--brand-green-deep); outline-offset: 2px; }
.select-caret {
  position: absolute; right: var(--s-3); top: 50%; transform: translateY(-50%);
  width: 18px; height: 18px; pointer-events: none; color: var(--fg-muted);
}

/* ---- TD-06 · volver arriba ---- */
.to-top {
  position: fixed; right: clamp(16px, 3vw, 32px);
  bottom: calc(clamp(16px, 3vw, 32px) + env(safe-area-inset-bottom, 0px));
  z-index: calc(var(--z-nav) + 1);
  width: 48px; height: 48px;
  display: inline-flex; align-items: center; justify-content: center;
  border: 0; border-radius: 999px;
  background: var(--brand-green-deep); color: var(--fg-on-ink);
  box-shadow: 0 6px 18px rgba(0,0,0,0.22);
  opacity: 0; visibility: hidden; transform: translateY(8px);
  transition: opacity var(--t-base) var(--ease-out), transform var(--t-base) var(--ease-out), visibility var(--t-base);
  cursor: pointer;
}
.to-top.is-visible { opacity: 1; visibility: visible; transform: none; }
.to-top svg { width: 22px; height: 22px; }
@media (prefers-reduced-motion: reduce) { .to-top { transition: none; } }
""" + "\n".join(rules) + "\n"

CSS.write_text(css.rstrip() + "\n\n" + block)
print("CSS del directorio escrito ·", len(rules), "reglas de logo")
json.dump(sizes, open("/tmp/directory-sizes.json", "w"), indent=1)
