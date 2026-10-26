#!/usr/bin/env python3
"""Copy consistency checks for the Risso v2 site. Stdlib only, no deps.

Run from the v2/ directory:  python3 scripts/copy-check.py
Exit 0 = every FAIL check passed. WARNs never change the exit code.
"""
from __future__ import annotations

import re
import sys
import pathlib

BASE = (
    pathlib.Path(sys.argv[1]).resolve()
    if len(sys.argv) > 1
    else pathlib.Path(__file__).resolve().parent.parent
)
PAGES = [
    "index.html",
    "sobre-risso.html",
    "descuentos.html",
    "tiendas.html",
    "como-llegar.html",
    "contacto.html",
    "libro-reclamaciones.html",
]

# ---------------------------------------------------------------- canonical facts
EMAIL = "contacto@agremsa.pe"   # confirmado por el cliente 2026-10-18
PHONE = ""          # el centro NO tiene línea de contacto pública: no publicar teléfono
HOURS = "10:00 a 22:00"
ADDRESS = "Av. Arequipa 2201"
OPENING_YEAR = "1968"

# Hechos que el cliente todavía no confirmó: se emiten como WARN, no como FAIL.
PENDING: set[str] = {"promos", "response_sla"}

MAX_EMDASH = 2  # presupuesto de rayas por página (WARN si se pasa)

BANNED = [
    # mentiras / datos sin verificar
    "Línea 1",
    "Abiertos todos los días del año",
    "todos los servicios",
    "la mayoría de los vecinos",
    "El directorio se actualiza periódicamente",
    "la agregaremos en la próxima actualización",
    "accesible desde varias líneas",
    "Las tiendas que tienen promos este mes",
    # copy que habla del sitio en vez de la cosa
    "visita la página completa",
    "entra al detalle",
    "Toda la información para encontrarnos",
    "No requiere datos comerciales",
    # preposición equivocada (el local no está encima de la avenida)
    "sobre Av. Arequipa 2201",
    # jerga interna
    "Cada frente tiene",
    "Elegir frente",
    # relleno / tics
    "un mismo piso",
    "tus tiendas favoritas",
    "cerca de todo",
    "todo a un paso",
    "sin caminar media ciudad",
    # restos de plantilla
    "Construido con cuidado",
    "El formato en que publicaremos",
    "las reales aparecen aquí",
]

NAV_EXPECTED = [
    "Inicio",
    "Sobre Risso",
    "Promociones",
    "Tiendas",
    "Cómo llegar",
    "Contáctanos",
]

fails: list[str] = []
warns: list[str] = []


def fail(page: str, msg: str) -> None:
    fails.append(f"FAIL {page}: {msg}")


def warn(page: str, msg: str) -> None:
    warns.append(f"WARN {page}: {msg}")


def strip(html: str) -> str:
    html = re.sub(r"<(script|style|svg)\b[\s\S]*?</\1>", " ", html)
    html = re.sub(r"<!--[\s\S]*?-->", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)


def read(page: str) -> str:
    return (BASE / page).read_text(encoding="utf-8")


def anchors_nav(html: str) -> list[str]:
    blocks = re.findall(r'<nav class="nav"[^>]*>([\s\S]*?)</nav>', html)
    if not blocks:
        return []
    return [strip(a) for a in re.findall(r"<a\b[^>]*>([\s\S]*?)</a>", blocks[0])]


def anchors_drawer(html: str) -> list[str]:
    blocks = re.findall(r'<div class="mobile-drawer"[^>]*>([\s\S]*?)</div>', html)
    if not blocks:
        return []
    return [strip(a) for a in re.findall(r"<a\b[^>]*>([\s\S]*?)</a>", blocks[0])]


def directory_counts() -> tuple[dict[str, int], int, list[tuple[str, str]]]:
    """Cuenta las tiendas por categoría en el directorio de tiendas.html.

    Estructura (ronda OpenDesign 2026-10-26): una <section class="store-group"
    id="slug"> por categoría, con <h2> en .store-group-head y una <li
    class="store-card"> por tienda.
    """
    html = read("tiendas.html")
    secs = list(
        re.finditer(r'<section class="store-group"\s+id="([a-z0-9-]+)"', html)
    )
    counts: dict[str, int] = {}
    order: list[tuple[str, str]] = []
    for i, m in enumerate(secs):
        end = secs[i + 1].start() if i + 1 < len(secs) else len(html)
        chunk = html[m.end():end]
        counts[m.group(1)] = len(re.findall(r'class="store-card"', chunk))
        nm = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", chunk)
        order.append((m.group(1), strip(nm.group(1)) if nm else ""))
    return counts, len(counts), order


def main() -> int:
    # 1 · estructura: los <div> deben cuadrar (un desbalance rompe el copy y el CSS)
    for page in PAGES:
        html = read(page)
        body = re.sub(r"<!--[\s\S]*?-->", "", html)
        opened, closed = len(re.findall(r"<div\b", body)), len(re.findall(r"</div>", body))
        if opened != closed:
            fail(page, f"div desbalanceados: {opened} abren, {closed} cierran")

    # 2 · nav idéntico en todas las páginas y entre desktop y drawer
    for page in PAGES:
        html = read(page)
        nav, drawer = anchors_nav(html), anchors_drawer(html)
        if nav and nav != NAV_EXPECTED:
            fail(page, f"nav desktop {nav} != {NAV_EXPECTED}")
        if drawer and drawer != NAV_EXPECTED:
            fail(page, f"nav drawer {drawer} != {NAV_EXPECTED}")

    # 2b · aria-current correcto: si la página está en el nav, exactamente uno y apuntando a ella;
    # si no está (p. ej. libro-reclamaciones), ninguno.
    for page in PAGES:
        html = read(page)
        nav_block = re.search(r'<nav class="nav"[^>]*>([\s\S]*?)</nav>', html)
        drawer_block = re.search(r'<div class="mobile-drawer"[\s\S]*?</div>', html)
        for label, block in (("nav", nav_block), ("drawer", drawer_block)):
            if not block:
                continue
            chunk = block.group(1) if label == "nav" else block.group(0)
            hrefs = re.findall(r'<a href="([^"]+)"', chunk)
            cur = re.findall(r'<a href="([^"]+)"[^>]*aria-current="page"[^>]*>', chunk)
            if page in hrefs:
                if len(cur) != 1:
                    fail(page, f"{label}: {len(cur)} aria-current (se espera 1)")
                elif cur[0] != page:
                    fail(page, f"{label}: aria-current apunta a {cur[0]}, no a {page}")
            elif cur:
                fail(page, f"{label}: {len(cur)} aria-current en una página que no está en el menú")

    # 3 · frases prohibidas (en TODO el archivo menos comentarios: incluye metas y alts)
    for page in PAGES:
        raw = re.sub(r"<!--[\s\S]*?-->", " ", read(page)).lower()
        for phrase in BANNED:
            if phrase.lower() in raw:
                fail(page, f'frase prohibida: "{phrase}"')

    # 3b · links internos que apuntan a archivos inexistentes
    for page in PAGES:
        for href in set(re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', read(page))):
            if not (BASE / href).exists():
                fail(page, f"link roto: {href}")

    # 4 · hechos canónicos
    for page in PAGES:
        body = strip(read(page))
        if ADDRESS not in body:
            fail(page, f"falta la dirección canónica: {ADDRESS}")
        if page != "libro-reclamaciones.html" and HOURS not in body:
            warn(page, f"no menciona el horario canónico ({HOURS})")

    for page in ("index.html", "sobre-risso.html"):
        if OPENING_YEAR not in strip(read(page)):
            fail(page, f"no menciona el año de apertura ({OPENING_YEAR})")

    # 5 · un solo email en todo el sitio, y el mismo en todas las páginas
    found_emails: set[str] = set()
    for page in PAGES:
        emails = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", read(page)))
        found_emails |= emails
        if len(emails) > 1:
            fail(page, f"más de un email: {sorted(emails)}")
    if len(found_emails) > 1:
        fail("(sitio)", f"emails distintos entre páginas: {sorted(found_emails)}")
    elif found_emails and next(iter(found_emails)) != EMAIL:
        msg = f'email {next(iter(found_emails))} != {EMAIL}'
        (warn if "email" in PENDING else fail)("(sitio)", msg)
    if PHONE:
        for page in ("contacto.html", "index.html"):
            if PHONE not in strip(read(page)):
                (warn if "phone" in PENDING else fail)(page, f"falta el teléfono {PHONE}")
    else:
        # hecho de negocio: el centro no publica línea telefónica de contacto
        for page in PAGES:
            raw = read(page)
            if re.search(r'href="tel:', raw) or "(01)" in raw:
                fail(page, "teléfono publicado, pero el centro no tiene línea de contacto")

    # 6 · el conteo de tiendas del home debe cuadrar con el directorio
    counts, n_cats, order = directory_counts()
    total = sum(counts.values())
    idx = strip(read("index.html"))
    if f"{total} tiendas" not in idx:
        fail("index.html", f"no dice «{total} tiendas» (el directorio tiene {total})")
    if n_cats != 10:
        fail("tiendas.html", f"{n_cats} categorías en el directorio, se esperan 10")
    if "10 categorías" not in strip(read("tiendas.html")):
        warn("tiendas.html", "el lede no menciona las 10 categorías")

    # las tarjetas de categoría del home (href="tiendas.html#cat-N") deben
    # nombrar la categoría N del directorio, en el mismo orden
    cards = re.findall(
        r'<a href="tiendas\.html#cat-(\d+)"[^>]*class="cat-preview"[^>]*>([\s\S]*?)</a>',
        read("index.html"),
    )
    if len(cards) < 4:
        fail("index.html", f"{len(cards)} tarjetas de categoría, se esperan 4")
    for num, chunk in cards:
        nm = re.search(r'class="cat-name">([\s\S]*?)<', chunk)
        got = strip(nm.group(1)) if nm else ""
        pos = int(num) - 1
        want = order[pos][1] if pos < len(order) else None
        if want is None:
            fail("index.html", f"tarjeta cat-{num}: no existe esa categoría en el directorio")
        elif got != want:
            fail(
                "index.html",
                f"tarjeta cat-{num}: dice «{got}», el directorio tiene «{want}»",
            )

    # los conteos que muestra cada grupo del directorio deben ser reales
    tiendas_html = read("tiendas.html")
    for slug, real in counts.items():
        sec = re.search(
            rf'<section class="store-group"\s+id="{re.escape(slug)}"[\s\S]*?</section>',
            tiendas_html,
        )
        if not sec:
            continue
        claimed = re.search(r'class="directory-count">(\d+)\s+tienda', sec.group(0))
        if not claimed:
            fail("tiendas.html", f"el grupo «{slug}» no muestra su conteo")
        elif int(claimed.group(1)) != real:
            fail(
                "tiendas.html",
                f"el grupo «{slug}» dice {claimed.group(1)} tiendas, tiene {real} tarjetas",
            )

    # 7 · <title> únicos y meta description útil
    titles: dict[str, str] = {}
    for page in PAGES:
        html = read(page)
        t = re.search(r"<title>([\s\S]*?)</title>", html)
        d = re.search(r'<meta name="description" content="([^"]*)"', html)
        if not t:
            fail(page, "sin <title>")
        else:
            title = strip(t.group(1))
            if title in titles:
                fail(page, f"<title> repetido con {titles[title]}")
            titles[title] = page
        if not d:
            fail(page, 'sin <meta name="description">')
        else:
            desc = strip(d.group(1))
            if not 120 <= len(desc) <= 165:
                warn(page, f"description de {len(desc)} caracteres (objetivo 120-165)")

    # 8 · presupuesto de rayas (taste, no verdad). Los <option> son placeholders de UI, no copy.
    for page in PAGES:
        prose = re.sub(r"<option\b[\s\S]*?</option>", " ", read(page))
        n = strip(prose).count("—")
        if n > MAX_EMDASH:
            warn(page, f"{n} rayas (—), presupuesto {MAX_EMDASH}")

    # 9 · promesas que el cliente todavía no confirmó
    if "3 días hábiles" in strip(read("contacto.html")) and "response_sla" in PENDING:
        warn("contacto.html", "SLA «3 días hábiles» sin confirmar por el cliente")

    for line in fails:
        print(line)
    for line in warns:
        print(line)
    print(f"\n{len(fails)} FAIL · {len(warns)} WARN · {len(PAGES)} páginas")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
