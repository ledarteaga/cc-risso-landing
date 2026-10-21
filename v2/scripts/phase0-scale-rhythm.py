#!/usr/bin/env python3
"""Fase 0 · Risso v2 — escala tipográfica de 4 niveles + ritmo vertical uniforme.

Idempotente: cada reemplazo se verifica antes de escribir. Si un patrón no
aparece, aborta sin tocar nada.
"""
import re
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]  # v2/
TOKENS = ROOT / "assets/css/tokens.css"
STYLES = ROOT / "assets/css/styles.css"

edits = []  # (path, old, new, label)


def add(path, old, new, label):
    edits.append((path, old, new, label))


# ==========================================================================
# 1. TOKENS · escala de 4 niveles (3 titulares + cuerpo)
# ==========================================================================
add(TOKENS,
    "  /* Display scale (Futura Heavy/Extra Black) */\n"
    "  --fs-display-1:       clamp(40px, 7vw, 96px);    /* hero claim */\n"
    "  --fs-display-2:       clamp(36px, 5.4vw, 76px);   /* page opening */\n"
    "  --fs-display-3:       clamp(28px, 4vw, 56px);    /* section heading */\n"
    "  --fs-display-4:       clamp(22px, 2.7vw, 38px);   /* sub-heading */\n"
    "\n"
    "  --fs-body-lg:         clamp(17px, 1.4vw, 21px);\n"
    "  --fs-body:            clamp(15px, 1.15vw, 17px);\n",
    "  /* Display scale — 4 niveles aprobados en reunión (20 oct 2026).\n"
    "     N1 claim 72 · N2 h1/h2 44 · N3 h3 24 · N4 cuerpo 17.\n"
    "     Un nivel = un tamaño, en las 6 páginas. No agregar excepciones por página. */\n"
    "  --fs-display-1:       clamp(38px, 5vw, 72px);     /* N1 · claim del hero */\n"
    "  --fs-display-2:       clamp(30px, 3.2vw, 44px);   /* N2 · h1 de página y h2 de sección */\n"
    "  --fs-display-3:       clamp(30px, 3.2vw, 44px);   /* N2 · alias histórico, mismo valor */\n"
    "  --fs-display-4:       clamp(19px, 1.7vw, 24px);   /* N3 · h3 / subtítulo de ficha */\n"
    "  --fs-display-5:       clamp(19px, 1.7vw, 24px);   /* N3 · alias (antes indefinido) */\n"
    "\n"
    "  --fs-body-lg:         clamp(16px, 1.1vw, 17px);   /* N4 · cuerpo y entradillas */\n"
    "  --fs-body:            clamp(15px, 1.05vw, 17px);  /* N4 · cuerpo */\n",
    "tokens: escala de 4 niveles")

add(TOKENS,
    "  /* Generous editorial padding · \"more space above a heading than below it\" */\n",
    "  /* Ritmo vertical — un solo valor para todas las secciones y el footer.\n"
    "     GL-03: el footer NO tiene valores propios. */\n"
    "  --pad-band:           72px;\n"
    "  --pad-footer:         72px;\n"
    "  --header-h:           72px;\n"
    "\n"
    "  /* Generous editorial padding · \"more space above a heading than below it\" */\n",
    "tokens: ritmo vertical")

# ==========================================================================
# 2. STYLES · titulares que escapaban de su nivel
# ==========================================================================
# N2 — h2 que estaban en N3
add(STYLES,
    ".beat-body h2 {\n  font-size: var(--fs-display-4); font-weight: 700;",
    ".beat-body h2 {\n  font-size: var(--fs-display-3); font-weight: 800;",
    "N2 · beat h2 38→44")
add(STYLES,
    ".directory-row-head h2 {\n  font-size: var(--fs-display-4); font-weight: 800;",
    ".directory-row-head h2 {\n  font-size: var(--fs-display-3); font-weight: 800;",
    "N2 · directory h2 38→44")
add(STYLES,
    ".reclamo-form h2 { font-size: var(--fs-display-4); font-weight: 700; margin-bottom: var(--s-4); }",
    ".reclamo-form h2 { font-size: var(--fs-display-3); font-weight: 800; margin-bottom: var(--s-4); }",
    "N2 · reclamo h2 38→44")
# N3 — h3 que estaban en N2
add(STYLES,
    ".confirm-card h3 { font-size: var(--fs-display-3); font-weight: 800;",
    ".confirm-card h3 { font-size: var(--fs-display-4); font-weight: 800;",
    "N3 · confirm-card h3 56→24")

# ==========================================================================
# 3. STYLES · tamaños hardcodeados fuera de escala
# ==========================================================================
add(STYLES,
    ".mobile-drawer a {\n  display: block; font-size: clamp(32px, 7vw, 56px); font-weight: 800;",
    ".mobile-drawer a {\n  display: block; font-size: var(--fs-display-2); font-weight: 800;",
    "drawer links → N2")
add(STYLES,
    "  font-size: clamp(17px, 1.35vw, 20px); line-height: 1.5;",
    "  font-size: var(--fs-body-lg); line-height: 1.5;",
    "hero-sub → N4")
add(STYLES,
    "  .anchor-head p { font-size: 22px; line-height: 1.45; max-width: 44ch; padding-left: var(--s-6); }",
    "  .anchor-head p { font-size: var(--fs-body-lg); line-height: 1.45; max-width: 44ch; padding-left: var(--s-6); }",
    "anchor-head p móvil → N4")
add(STYLES,
    ".timeline-item .year {\n  font-size: clamp(20px, 2.4vw, 32px);",
    ".timeline-item .year {\n  font-size: var(--fs-display-4);",
    "timeline year → N3")
add(STYLES,
    ".visit-plate-hours {\n  font-size: clamp(22px, 2vw, 30px);",
    ".visit-plate-hours {\n  font-size: var(--fs-display-4);",
    "visit-plate-hours → N3")
add(STYLES,
    "  font-size: clamp(64px, 9vw, 120px);\n  font-weight: 900; letter-spacing: -0.04em; line-height: 0.85;",
    "  font-size: clamp(48px, 5vw, 72px);   /* nunca mayor que el claim (N1) */\n  font-weight: 900; letter-spacing: -0.04em; line-height: 0.85;",
    "beat-year 120→72")
add(STYLES,
    "  font-size: clamp(24px, 2.4vw, 34px);\n  font-weight: 500;",
    "  font-size: var(--fs-display-4);\n  font-weight: 500;",
    "beat cta → N3")
add(STYLES,
    ".promo-row .promo-discount {\n  font-size: clamp(48px, 5vw, 72px);",
    ".promo-row .promo-discount {\n  font-size: var(--fs-display-1);",
    "promo-discount → N1")
add(STYLES,
    ".anchor-photo-cap-year {\n  font-family: var(--font-sans);\n  font-size: clamp(40px, 4.5vw, 56px);",
    ".anchor-photo-cap-year {\n  font-family: var(--font-sans);\n  font-size: var(--fs-display-4);",
    "anchor-photo-cap-year → N3")
add(STYLES,
    ".photo-row-cap-year {\n  font-family: var(--font-sans);\n  font-size: clamp(28px, 3vw, 40px);",
    ".photo-row-cap-year {\n  font-family: var(--font-sans);\n  font-size: var(--fs-display-4);",
    "photo-row-cap-year → N3")
add(STYLES,
    "  font-size: clamp(17px, 1.25vw, 19px); font-weight: 600;   /* matches the hero text link sitewide */",
    "  font-size: var(--fs-body-lg); font-weight: 600;   /* N4 — matches the hero text link sitewide */",
    "cta-link → N4")
add(STYLES,
    "  font-size: clamp(17px, 1.25vw, 19px); font-weight: 600; font-family: var(--font-sans);",
    "  font-size: var(--fs-body-lg); font-weight: 600; font-family: var(--font-sans);",
    "btn-text → N4")

# ==========================================================================
# 4. STYLES · ritmo vertical uniforme (GL-03)
# ==========================================================================
BAND = "clamp(48px, 4.5vw, 72px)"
for old, label in [
    (f"  padding-block: {BAND};", "banda genérica"),
]:
    pass

# 4a. reemplazo global del clamp de banda por el token (7 reglas)
styles_text = STYLES.read_text()
band_rules = [
    (".anchor {\n  padding-block: clamp(48px, 4.5vw, 72px);", ".anchor {\n  padding-block: var(--pad-band);"),
    (".beats-section { padding-block: clamp(48px, 4.5vw, 72px); }", ".beats-section { padding-block: var(--pad-band); }"),
    (".promo-section { padding-block: clamp(48px, 4.5vw, 72px); }", ".promo-section { padding-block: var(--pad-band); }"),
    (".wizard { padding-block: clamp(48px, 4.5vw, 72px); }", ".wizard { padding-block: var(--pad-band); }"),
    (".gallery-section { padding-block: clamp(48px, 4.5vw, 72px); }", ".gallery-section { padding-block: var(--pad-band); }"),
    (".reclamo-section { padding-block: clamp(48px, 4.5vw, 72px); }", ".reclamo-section { padding-block: var(--pad-band); }"),
    (".info-section--tight { padding-block: clamp(48px, 4.5vw, 72px); }", ".info-section--tight { padding-block: var(--pad-band); }"),
    (".contact-map-section { padding-block: clamp(48px, 4.5vw, 72px); }", ".contact-map-section { padding-block: var(--pad-band); }"),
]
for old, new in band_rules:
    add(STYLES, old, new, "ritmo · " + new.split("{")[0].strip())

# 4b. eliminar los colapsos asimétricos entre secciones hermanas
for old, label in [
    (".beats-section + .gallery-section { padding-top: 0; }",
     "colapso beats+gallery"),
    (".reclamo-section + .reclamo-section { padding-top: 0; }",
     "colapso reclamo+reclamo"),
    (".info-section--tight + .contact-map-section { padding-top: 0; }",
     "colapso info+map"),
]:
    add(STYLES, old, f"/* GL-03: sin colapsos asimétricos — {label} */", label)

# 4c. page-open simétrico + offset del header en main
add(STYLES,
    ".page-open {\n  padding-top: clamp(104px, 14vh, 150px);\n  padding-bottom: clamp(24px, 3vw, 40px);",
    "/* GL-03: apertura simétrica. El hueco del header fijo se resuelve en `main`,\n   no inflando el padding superior — así top === bottom en todas las bandas. */\n"
    "main:has(> .page-open) { margin-top: var(--header-h); }\n"
    ".page-open {\n  padding-block: var(--pad-band);",
    "page-open simétrico")

# 4d. photo-band y directory-section
add(STYLES,
    ".page-open--paper { background: var(--paper); color: var(--fg); }",
    ".page-open--paper { background: var(--paper); color: var(--fg); }\n"
    ".directory-section { padding-block: var(--pad-band); }",
    "directory-section 0→72")

# 4e. footer: mismas reglas que las secciones
add(STYLES,
    ".site-footer {\n  background: var(--ink); color: var(--fg-on-ink);\n  padding: var(--s-9) 0 0;",
    ".site-footer {\n  background: var(--ink); color: var(--fg-on-ink);\n  padding: var(--pad-footer) 0 var(--pad-footer);   /* GL-03: 72/72, igual que una sección */",
    "footer padding 96/0 → 72/72")
add(STYLES,
    ".footer-top {\n  display: grid; gap: var(--s-8); grid-template-columns: 1fr;\n}",
    ".footer-top {\n  display: grid; gap: var(--s-7); grid-template-columns: 1fr;\n}",
    "footer-top gap 64→48")
add(STYLES,
    "  .footer-top { grid-template-columns: minmax(0, 1.15fr) minmax(0, 1.5fr); gap: var(--s-10); }",
    "  .footer-top { grid-template-columns: minmax(0, 1.15fr) minmax(0, 1.5fr); gap: var(--s-7); }",
    "footer-top gap desktop 128→48")
add(STYLES,
    ".footer-bottom {\n  margin-top: var(--s-8);\n  padding-top: var(--s-5);",
    ".footer-bottom {\n  margin-top: var(--s-7);\n  padding-block: var(--s-5) var(--s-5);",
    "footer-bottom cierre con aire")

# ==========================================================================
# apply
# ==========================================================================
by_path = {}
for path, old, new, label in edits:
    by_path.setdefault(path, []).append((old, new, label))

for path, items in by_path.items():
    text = path.read_text()
    for old, new, label in items:
        if new and new in text and not old:
            continue
        if old not in text:
            if new in text:
                print(f"  ~ ya aplicado: {label}")
                continue
            print(f"  ✗ NO ENCONTRADO: {label}")
            print(f"    {old[:90]!r}")
            sys.exit(1)
        text = text.replace(old, new, 1)
        print(f"  ✓ {label}")
    path.write_text(text)

print("\nFase 0 aplicada.")
