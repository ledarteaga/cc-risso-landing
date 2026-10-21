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

TARGET_INK = 34.0     # raíz del área de tinta renderizada, en px
H_MIN, H_MAX = 20, 44
W_MAX, W_MAX_STRIP = 150, 224   # los wordmarks de una línea necesitan más ancho


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
    rules.append(f'.tenant-chip[data-logo="{s}"] img {{ height: {height}px; }}')

# ---------------------------------------------------------------- HTML
html = TIENDAS.read_text()

rows = re.findall(
    r'<div class="directory-row[^"]*" id="([^"]+)"[^>]*>\s*'
    r'<div class="directory-row-head">\s*<h2([^>]*)>(.*?)</h2>\s*(?:<p[^>]*>.*?</p>)?\s*</div>\s*'
    r'<div class="directory-tenants">(.*?)</div>',
    html, re.S)
print("filas encontradas:", len(rows))

blocks = []
for cat_id, h2_attrs, title, tenants in rows:
    logos = re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', tenants)
    chips = []
    for src, alt in logos:
        name = src.rsplit("/", 1)[-1]
        s = slug(name)
        chips.append(f'            <span class="tenant-chip" data-logo="{s}">'
                     f'<img src="{src}" alt="{alt}" loading="lazy"></span>')
    n = len(logos)
    label_id = re.search(r'id="([^"]+)"', h2_attrs)
    label_id = label_id.group(1) if label_id else f"cat-{cat_id}"
    blocks.append(f'''        <div class="directory-row" id="{cat_id}" aria-labelledby="{label_id}">
          <div class="directory-row-head">
            <h2{h2_attrs}>{title}</h2>
            <p class="directory-count">{n} {'tienda' if n == 1 else 'tiendas'}</p>
          </div>
          <div class="directory-tenants">
{chr(10).join(chips)}
          </div>
        </div>''')

directorio = "      <div class=\"directory\">\n" + "\n\n".join(blocks) + "\n      </div>"

# reemplaza el bloque .directory completo
start = html.index('<div class="directory">')
end = html.index("    </section>", start)
html = html[:start] + directorio + "\n" + html[end:]

# ---------------------------------------------------------------- filtro
options = ['          <option value="all">Todas las categorías ({})</option>'.format(
    sum(len(re.findall(r'<img', b)) for b in blocks))]
for cat_id, _, title, tenants in rows:
    n = len(re.findall(r"<img", tenants))
    options.append(f'          <option value="{cat_id}">{title} ({n})</option>')

filtro = '''    <!-- TD-01 · filtro desplegable en lugar de la barra de 11 enlaces -->
    <div class="directory-filter" role="search">
      <div class="directory-filter-inner">
        <label class="kicker" for="cat-filter">Filtrar por categoría</label>
        <div class="select-wrap">
          <select id="cat-filter" class="cat-select" aria-label="Filtrar el directorio por categoría">
''' + "\n".join(options) + '''
          </select>
          <svg class="select-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>
    </div>

'''

subnav_re = re.compile(r'    <!-- =+\n         SUB-NAV · sticky anchor jump\n.*?</nav>\n\n', re.S)
if subnav_re.search(html):
    html = subnav_re.sub(filtro, html)
    print("subnav → filtro")
else:
    print("no encontré el subnav")

TIENDAS.write_text(html)

# ---------------------------------------------------------------- CSS
css = CSS.read_text()
MARK = "/* ==========================================================================\n   FASE 2 · DIRECTORIO DE TIENDAS"
if MARK in css:
    css = css[:css.index(MARK)].rstrip() + "\n"

block = MARK + """
   Todas las categorías comparten el azul de marca: la separación es espacial,
   no cromática (TI-01, TD-02, TD-05). El fondo de la página es un tinte suave.
   ========================================================================== */
.tiendas-page body { background: #F4F7FC; }

.directory { display: grid; grid-template-columns: 1fr; gap: var(--s-3); }
.directory-row {
  padding: clamp(28px, 3vw, 44px) clamp(20px, 3vw, 36px);
  color: var(--fg-on-ink);
  background: var(--brand-blue);
}
.directory-row-head { margin-bottom: var(--s-5); }
.directory-row-head h2 { font-size: var(--fs-display-3); font-weight: 800; letter-spacing: -0.015em; line-height: var(--lh-heading); color: var(--fg-on-ink); margin: 0; }
.directory-count {
  margin-top: var(--s-2);
  font-size: var(--fs-caption);
  letter-spacing: var(--track-caps);
  text-transform: uppercase;
  color: rgba(255,255,255,0.72);
}
.directory-tenants { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2) var(--s-3); }
.tenant-chip {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 64px;
  padding: var(--s-3) var(--s-4);
  background: rgba(255,255,255,0.06);
}
.tenant-chip img { width: auto; max-width: 100%; object-fit: contain; }
.directory-row[hidden] { display: none; }

@media (min-width: 1024px) {
  .directory-row { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.6fr); gap: var(--s-7); align-items: center; }
  .directory-row-head { margin-bottom: 0; }
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
.select-wrap { position: relative; flex: 0 1 320px; }
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
